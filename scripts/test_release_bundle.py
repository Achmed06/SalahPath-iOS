#!/usr/bin/env python3
"""Negative regression tests for archive validation using an isolated bundle."""
import plistlib
import shutil
import tempfile
import unittest
from pathlib import Path
from verify_release_bundle import ROOT, RESOURCE_HASHES, verify_bundle


class ReleaseBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Path(self.temp.name) / 'SalahPath.app'
        self.app.mkdir()
        self.info = {
            'CFBundleShortVersionString': '3.62', 'CFBundleVersion': '79',
            'CFBundleIdentifier': 'com.achmed06.salahpath',
            'CFBundleDisplayName': 'SalahPath', 'CFBundleExecutable': 'SalahPath',
            'CFBundlePackageType': 'APPL', 'CFBundleSupportedPlatforms': ['iPhoneOS'],
            'UIBackgroundModes': ['audio'], 'ITSAppUsesNonExemptEncryption': False,
            'CFBundleLocalizations': ['de', 'tr'], 'NSLocationWhenInUseUsageDescription': 'Purpose',
            'DTSDKName': 'iphoneos26.0', 'DTXcode': '2600', 'MinimumOSVersion': '17.0',
            'CFBundleIcons': {'CFBundlePrimaryIcon': {'CFBundleIconName': 'AppIcon'}},
        }
        self.save_info()
        (self.app / 'SalahPath').write_bytes(b'fixture executable without internal markers')
        shutil.copy(ROOT / 'SalahZeit/PrivacyInfo.xcprivacy', self.app)
        for filename in [*RESOURCE_HASHES, 'ThirdPartyNotices.txt']:
            shutil.copy(ROOT / 'SalahZeit/Resources' / filename, self.app)
        for language in ('de', 'tr'):
            shutil.copytree(ROOT / 'SalahZeit/Resources' / f'{language}.lproj', self.app / f'{language}.lproj')

    def save_info(self):
        (self.app / 'Info.plist').write_bytes(plistlib.dumps(self.info))

    def test_valid_fixture(self):
        self.assertEqual(verify_bundle(self.app)['verification'], 'passed')

    def test_rejects_missing_background_mode(self):
        del self.info['UIBackgroundModes']
        self.save_info()
        with self.assertRaisesRegex(ValueError, 'background mode'):
            verify_bundle(self.app)

    def test_rejects_old_sdk(self):
        self.info['DTSDKName'] = 'iphoneos18.0'
        self.save_info()
        with self.assertRaisesRegex(ValueError, 'SDK 26'):
            verify_bundle(self.app)

    def test_rejects_stale_build_identity(self):
        self.info['CFBundleVersion'] = '78'
        self.save_info()
        with self.assertRaisesRegex(ValueError, 'CFBundleVersion'):
            verify_bundle(self.app)

    def test_rejects_internal_marker_at_binary_end(self):
        (self.app / 'SalahPath').write_bytes(b'x' * 500000 + b'SALAH_QA_SCREEN')
        with self.assertRaisesRegex(ValueError, 'Internal test marker'):
            verify_bundle(self.app)

    def test_rejects_altered_quran(self):
        (self.app / 'quran-uthmani.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'audited resource'):
            verify_bundle(self.app)

    def test_rejects_missing_turkish_permissions(self):
        (self.app / 'tr.lproj/InfoPlist.strings').unlink()
        with self.assertRaisesRegex(ValueError, 'tr permission'):
            verify_bundle(self.app)


if __name__ == '__main__':
    unittest.main()
