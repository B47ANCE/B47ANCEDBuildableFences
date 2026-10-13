"""Removal contract: no spawn command, menu or kit code in current runtime."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class KitRemoval(unittest.TestCase):
    def test_no_runtime_kit_hooks_or_translations(self):
        for base in (ROOT / 'src/B47ANCEDBuildableFences/42', ROOT / 'prototypes/cohesive/42'):
            self.assertFalse(list(base.rglob('B47_FenceTestKit*')))
            for path in base.rglob('*.lua'):
                text = path.read_text(encoding='utf-8')
                self.assertNotIn('B47FenceTestKit', text, str(path))
                self.assertNotIn('b47fencetestkit', text, str(path))
            for path in base.glob('media/lua/shared/Translate/*/IG_UI.json'):
                self.assertFalse(any('TestKit' in key for key in json.loads(path.read_text(encoding='utf-8'))))

    def test_existing_construction_and_selector_behavior_preserved(self):
        before = ROOT / 'docs/evidence/history/1.1.0-dev.5'
        for folder in ('src/B47ANCEDBuildableFences/42', 'prototypes/cohesive/42'):
            for path in (ROOT / folder).rglob('*.lua'):
                relative = path.relative_to(ROOT)
                self.assertEqual(path.read_bytes().replace(b'1.1.0-dev.6', b'1.1.0-dev.5'), (before / relative).read_bytes(), str(relative))
