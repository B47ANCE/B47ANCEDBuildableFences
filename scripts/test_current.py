"""Run current regressions; explicitly report unavailable original-baseline gates."""
import argparse
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from test_fences import BASELINE

BASELINE_METHODS = {
    'test_existing_entities_preserved_except_approved_expansion_and_skills',
    'test_installed_baseline_is_untouched',
    'test_post_conversion_is_only_an_allowlist_extension',
    'test_exact_released_identity_map_and_complete_faces',
    'test_native_assets_ids_and_legacy_ui_definitions_retained',
}


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--available', action='store_true', help='Run available tests, reporting missing original-baseline checks as BLOCKED')
    args = parser.parse_args()
    all_tests = list(flatten(unittest.defaultTestLoader.discover(str(ROOT / 'tests'))))
    selected = []
    for test in all_tests:
        if args.available and not BASELINE.exists() and test._testMethodName in BASELINE_METHODS:
            print('BLOCKED missing original installed baseline:', test.id(), flush=True)
        else:
            selected.append(test)
    print('Environment: offline Python/Lupa; no PZ runtime', flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected))
    raise SystemExit(not result.wasSuccessful())
