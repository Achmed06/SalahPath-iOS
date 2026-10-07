#!/usr/bin/env python3
"""Reject incorrect distribution credentials before a costly signed archive or upload."""
import copy
import datetime as dt
import hashlib
import unittest

from verify_store_signing import TIME_SENSITIVE, select_identity, verify_profile, verify_signed_entitlements


class StoreSigningTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026, 10, 7, tzinfo=dt.timezone.utc)
        self.team = "TESTTEAM01"
        self.cert = b"synthetic certificate fixture; not a real credential"
        self.entitlements = {"application-identifier": "LEGACYPFX1.com.achmed06.salahpath",
                             "com.apple.developer.team-identifier": self.team,
                             "get-task-allow": False, "beta-reports-active": True, TIME_SENSITIVE: True}
        self.profile = {"ExpirationDate": dt.datetime(2027, 1, 1), "TeamIdentifier": [self.team],
                        "Platform": ["iOS"], "ApplicationIdentifierPrefix": ["LEGACYPFX1"],
                        "UUID": "12345678-1234-1234-1234-123456789ABC",
                        "DeveloperCertificates": [self.cert], "Entitlements": copy.deepcopy(self.entitlements)}

    def test_valid_legacy_app_prefix_is_not_confused_with_team_id(self):
        self.assertEqual(verify_profile(self.profile, self.team, self.now)["profile_verification"], "passed")
        verify_signed_entitlements(self.profile, self.entitlements, self.cert, self.team)

    def test_expired_profile(self):
        self.profile["ExpirationDate"] = self.now
        with self.assertRaisesRegex(ValueError, "expired"):
            verify_profile(self.profile, self.team, self.now)

    def test_wrong_team(self):
        with self.assertRaisesRegex(ValueError, "another team"):
            verify_profile(self.profile, "OTHERTEAM1", self.now)

    def test_non_store_profiles(self):
        for field, value in (("ProvisionedDevices", []), ("ProvisionsAllDevices", True)):
            with self.subTest(field=field):
                profile = copy.deepcopy(self.profile)
                profile[field] = value
                with self.assertRaisesRegex(ValueError, "not App Store"):
                    verify_profile(profile, self.team, self.now)

    def test_wrong_app_and_missing_capabilities(self):
        for key, value in (("application-identifier", "LEGACYPFX1.*"),
                           ("get-task-allow", True), ("beta-reports-active", False), (TIME_SENSITIVE, False)):
            with self.subTest(key=key):
                profile = copy.deepcopy(self.profile)
                profile["Entitlements"][key] = value
                with self.assertRaises(ValueError):
                    verify_profile(profile, self.team, self.now)

    def test_identity_must_match_profile_and_be_valid(self):
        fingerprint = hashlib.sha1(self.cert).hexdigest().upper()
        identities = f'  1) {fingerprint} "Apple Distribution: Test"\n     1 valid identities found\n'
        self.assertEqual(select_identity(self.profile, identities), fingerprint)
        for value in ("0 valid identities found", identities.replace(fingerprint, "F" * 40),
                      identities.replace('Test"', 'Test" (CSSMERR_TP_CERT_EXPIRED)')):
            with self.assertRaises(ValueError):
                select_identity(self.profile, value)

    def test_signed_app_identity_mismatch(self):
        self.entitlements["application-identifier"] = "WRONGPFX01.com.achmed06.salahpath"
        with self.assertRaisesRegex(ValueError, "does not match"):
            verify_signed_entitlements(self.profile, self.entitlements, self.cert, self.team)

    def test_export_certificate_mismatch(self):
        with self.assertRaisesRegex(ValueError, "certificate not allowed"):
            verify_signed_entitlements(self.profile, self.entitlements, b"different certificate", self.team)

    def test_development_or_missing_signed_capability(self):
        for key, value in (("get-task-allow", True), (TIME_SENSITIVE, False)):
            with self.subTest(key=key):
                signed = dict(self.entitlements, **{key: value})
                with self.assertRaises(ValueError):
                    verify_signed_entitlements(self.profile, signed, self.cert, self.team)


if __name__ == "__main__":
    unittest.main()
