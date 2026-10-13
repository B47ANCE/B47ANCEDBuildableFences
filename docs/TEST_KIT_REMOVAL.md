# Developer kit removal

Project Version: 1.1.0-dev.6

Compatible PATCH-scope cleanup in the existing 1.1.0 prerelease series. Archived
dev.5 source, overlay, tests and records remain immutable. Removed three kit Lua
files and all four kit keys from each of 29 overlay translations. The surviving
Lua matches dev.5 byte-for-byte after neutralizing version markers. Native fence
construction, recipes, selector/gate and server authority remain unchanged.

[TESTED Windows offline] 2 removal tests PASS; 26 independent tests PASS with
project-local Lupa 2.8. Full discovery ran 31 tests; five baseline-dependent
methods are BLOCKED because Workshop 3810187215 is no longer installed.
No native game/server launched. G6/G7 NOT TESTED; stable G8 BLOCKED.

Commands from workspace:
- Python -m unittest discover -s B47ANCEDBuildableFences/tests -p test_no_testkit.py -v
- Python -m unittest discover -s B47ANCEDBuildableFences/tests -v (five methods blocked)
- Python B47ANCEDBuildableFences/scripts/check_versions.py --root B47ANCEDBuildableFences --release
- tools/Validate-WorkshopLayout.ps1 -ProjectRoot C:/Users/willi/Zomboid/Workshop/B47ANCEDBuildableFences -ExpectedModId B47ANCEDBuildableFences -ExpectedVersion 1.1.0-dev.6
Python: C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
PYTHONPATH: B47ANCEDBuildableFences/.test-dependencies
Independent-suite selection is recorded by its named excluded methods and full
results in evidence/dev6-independent-tests.txt; full results in dev6-offline-tests.txt.

User selected Workshop item 3817174798 as deployment destination. Local test mods
were not changed. Fresh staging contains 94 hash-verified source/overlay files.
Current package record: evidence/workshop-dev6-package.json.
