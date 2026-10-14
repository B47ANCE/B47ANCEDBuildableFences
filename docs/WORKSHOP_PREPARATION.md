# Workshop preparation

Project Version: 1.1.0-dev.8

PATCH-compatible cleanup within the existing 1.1.0 development series. The user
clarified that only code shipped inside the mod is to be stripped of testing
hooks; all offline regression tests are retained. Removed the startup diagnostic
print and test-only tooltip export. Tests now inspect the actual rendered tooltip.
The prior test kit stays absent. Runtime behavior, six family selectors, original
per-part costs/skills, gate, authority and save identities remain unchanged.

## Bounded cleanup and retention record

No files, packages, archives, research or historical evidence are deleted or
moved. Source roots remain src/B47ANCEDBuildableFences/42 plus the established
prototypes/cohesive/42 overlay. Only runtime diagnostic lines are removed, with
before/after source preserved by Git. Offline tests, tools and fixtures remain
repository-only. Old ignored packages, local test installations, evidence and
the user's unrelated AGENTS.md edit are protected and untouched.

## Reproducible candidate

Python commands from repository root, with Lupa installed for regression tests:
```powershell
$env:PYTHONPATH=(Resolve-Path .test-dependencies).Path
$py='C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py scripts/test_current.py --available
& $py scripts/check_versions.py --root .
& $py scripts/prepare_workshop.py
# Only after the intended source/metadata commit is pushed and verified:
& $py scripts/prepare_workshop.py --prepare
& $py scripts/check_versions.py --root . --release
```

The builder composes only the two established source roots, rejects test/debug
hooks and unexpected file types, case collisions, escaping links, unexpected
source overrides and case-incorrect custom requires. It refuses existing output
paths, untracked payload or uncommitted inputs and requires HEAD to match its
upstream. Candidate is ignored under dist/workshop-candidates/<VERSION>;
ZIP is under dist/development-current. The manifest binds Git SHA, version,
Mod ID, Workshop ID, exact file hashes and package SHA-256. It verifies exact
source/stage/archive parity, member traversal, duplicates and CRC/data integrity.
The upload VDF targets existing item 3817174798, App ID 108600, and preserves real
newlines. It omits title/preview/visibility changes; a future authorized publisher
must verify the current remote metadata and required release gates.

Only preparation is authorized. No SteamCMD upload, local deployment, live-server
changes, game launch or server launch occurs. The candidate manifest explicitly
sets publish_ready=false. G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED;
stable G8 BLOCKED. The post lifecycle/input-validation issues recorded in the
prior audit are not repaired or certified by this diagnostic-cleanup slice.

## Current validation

[TESTED Windows offline, 2026-10-14] 37 runnable regressions PASS. Five checks
against the absent original installed Workshop baseline remain explicitly BLOCKED.
Shipped-content preflight PASS: 94 composed runtime files, no runtime tests,
diagnostic prints, test kit or custom Java/JAR. Version consistency PASS.
Packaging results are reported separately after candidate generation; package
integrity is not native SP/MP evidence or stable-release approval.
