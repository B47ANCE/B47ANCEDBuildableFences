"""Offline-only checks for shipped content and candidate archive integrity."""
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_workshop import MOD, runtime_files, verify_zip


class WorkshopPreparation(unittest.TestCase):
    def test_actual_payload_has_no_test_exports_or_diagnostics(self):
        files = runtime_files()
        self.assertEqual(len(files), 94)
        self.assertIn('media/lua/shared/B47_CohesiveModel.lua', files)
        presentation = files['media/lua/client/B47_CohesivePresentation.lua'].read_text()
        self.assertNotIn('V.description=', presentation)
        self.assertNotIn('cohesive selector 1.1.0-dev.', presentation)

    def test_development_files_and_case_collisions_fail_preflight(self):
        for relative in ('debug.jar', 'tests/helper.lua', 'media/lua/debug.lua'):
            with self.subTest(path=relative), tempfile.TemporaryDirectory(prefix='b47-payload-') as folder:
                root = Path(folder)
                target = root / ('src/' + MOD + '/42') / relative
                target.parent.mkdir(parents=True)
                target.write_text('print("testing")')
                with self.assertRaises(ValueError):
                    runtime_files(root)

    def test_unexpected_translation_overrides_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix='b47-override-') as folder:
            root = Path(folder)
            for source in ('src/' + MOD + '/42', 'prototypes/cohesive/42'):
                target = root / source / 'mod.info'
                target.parent.mkdir(parents=True)
                target.write_text('id=' + MOD)
            with self.assertRaises(ValueError):
                runtime_files(root)

    def test_archive_rejects_unexpected_and_unsafe_members(self):
        expected = {MOD + '/42/mod.info': b'id=' + MOD.encode()}
        with tempfile.TemporaryDirectory(prefix='b47-archive-') as folder:
            for extra in (None, '../escape', 'tests/probe.lua'):
                target = Path(folder) / ('valid.zip' if extra is None else 'invalid.zip')
                with zipfile.ZipFile(target, 'w') as archive:
                    archive.writestr(MOD + '/common/', '')
                    for name, data in expected.items():
                        archive.writestr(name, data)
                    if extra:
                        archive.writestr(extra, 'invalid')
                if extra:
                    with self.assertRaises(ValueError):
                        verify_zip(target, expected)
                else:
                    verify_zip(target, expected)
