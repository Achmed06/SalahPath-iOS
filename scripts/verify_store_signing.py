#!/usr/bin/env python3
"""Check decoded App Store profile data; macOS codesign verifies the signature separately."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import plistlib
import re
import uuid
from pathlib import Path

BUNDLE_ID = "com.achmed06.salahpath"
TIME_SENSITIVE = "com.apple.developer.usernotifications.time-sensitive"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_profile(profile: dict, team: str, now: dt.datetime | None = None) -> dict:
    require(re.fullmatch(r"[A-Z0-9]{10}", team) is not None, "Invalid Team ID")
    now = now or dt.datetime.now(dt.timezone.utc)
    expiration = profile.get("ExpirationDate")
    require(isinstance(expiration, dt.datetime), "Missing profile expiration")
    expiration = expiration.replace(tzinfo=dt.timezone.utc) if expiration.tzinfo is None else expiration
    require(expiration > now, "Provisioning profile expired")
    require(profile.get("TeamIdentifier") == [team], "Profile belongs to another team")
    require("iOS" in profile.get("Platform", []), "Not an iOS profile")
    require("ProvisionedDevices" not in profile and not profile.get("ProvisionsAllDevices"),
            "Development, Ad Hoc or enterprise profile is not App Store distribution")
    entitlements = profile.get("Entitlements", {})
    require(entitlements.get("get-task-allow") is False, "Profile permits development debugging")
    require(entitlements.get("beta-reports-active") is True, "Missing App Store profile entitlement")
    require(entitlements.get("com.apple.developer.team-identifier") == team, "Wrong profile team entitlement")
    require(entitlements.get(TIME_SENSITIVE) is True, "Profile lacks Time Sensitive Notifications")
    prefixes = profile.get("ApplicationIdentifierPrefix", [])
    app_id = entitlements.get("application-identifier")
    require(any(app_id == f"{prefix}.{BUNDLE_ID}" for prefix in prefixes), "Wrong or wildcard profile App ID")
    profile_uuid = str(uuid.UUID(profile.get("UUID", ""))).upper()
    certificates = profile.get("DeveloperCertificates", [])
    require(bool(certificates) and all(isinstance(cert, bytes) and cert for cert in certificates),
            "Missing profile signing certificates")
    return {"profile_uuid": profile_uuid, "team_id": team, "application_identifier": app_id,
            "profile_expires": expiration.isoformat(), "profile_verification": "passed"}


def select_identity(profile: dict, identities: str) -> str:
    allowed = {hashlib.sha1(cert).hexdigest().upper() for cert in profile["DeveloperCertificates"]}
    available = set(re.findall(r'^\s*\d+\) ([A-Fa-f0-9]{40}) "[^"\r\n]+"\s*$', identities, re.MULTILINE))
    matches = {value.upper() for value in available} & allowed
    require(len(matches) == 1, "Need exactly one valid signing identity matching this profile")
    return matches.pop()


def verify_signed_entitlements(profile: dict, entitlements: dict, certificate: bytes, team: str) -> None:
    require(entitlements.get("com.apple.developer.team-identifier") == team, "Wrong signed team")
    require(entitlements.get("application-identifier") == profile["Entitlements"]["application-identifier"],
            "Signed App ID does not match the profile")
    require(entitlements.get("get-task-allow", False) is False, "Development-signed export")
    require(entitlements.get(TIME_SENSITIVE) is True, "Signed app lacks Time Sensitive Notifications")
    require(certificate in profile["DeveloperCertificates"], "Signing certificate not allowed by profile")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("--team", required=True)
    parser.add_argument("--identities", type=Path)
    parser.add_argument("--entitlements", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        profile = plistlib.loads(args.profile.read_bytes())
        report = verify_profile(profile, args.team)
        if args.identities:
            report["certificate_sha1"] = select_identity(profile, args.identities.read_text())
        require(bool(args.entitlements) == bool(args.certificate), "Supply both entitlements and certificate")
        if args.entitlements:
            verify_signed_entitlements(profile, plistlib.loads(args.entitlements.read_bytes()),
                                       args.certificate.read_bytes(), args.team)
            report["signed_entitlements_verification"] = "passed"
        output = json.dumps(report, indent=2) + "\n"
        if args.report:
            args.report.write_text(output)
        print(output, end="")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, plistlib.InvalidFileException) as error:
        raise SystemExit(f"SIGNING VERIFICATION FAILED: {error}") from error


if __name__ == "__main__":
    main()
