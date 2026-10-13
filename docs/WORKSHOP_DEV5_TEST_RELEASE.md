# Authorized untested Workshop test release

Project Version: 1.1.0-dev.5

The user explicitly authorized publishing an untested prerelease so it can be
tested on a dedicated server. This is a bounded exception to publication gates,
not runtime evidence, stable promotion or release-readiness approval. G6/G7
remain NOT TESTED and stable G8 remains BLOCKED. The developer kit is included
for this explicitly requested test distribution.

The package composes unchanged production source with the current corrected
Wrought Iron selector/gate/test-kit overlay. It retains all legacy definitions,
collision axes and existing post conversion. No dev.3 topology is included.
Source/code stays 1.1.0-dev.5. Stable target remains 1.1.0. Visibility and item
identity are preserved; update target is the existing Workshop item 3810187215.

Canonical player-facing description: WORKSHOP_DESCRIPTION.txt. The update note
is WORKSHOP_CHANGE_NOTE.txt. Generated staging and ZIP are built and hash-checked
by scripts/prepare_workshop_test.py, not hand-edited. The downloaded Workshop
baseline is never a build input that gets modified.

Exact preparation/verification commands from the workspace root:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\prepare_workshop_test.py
& .\tools\Validate-WorkshopLayout.ps1 -ProjectRoot 'C:\Users\willi\Zomboid\Workshop\B47ANCEDBuildableFences' -ExpectedModId B47ANCEDBuildableFences -ExpectedVersion 1.1.0-dev.5
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\check_versions.py --root B47ANCEDBuildableFences --release
```

SteamCMD uploads the generated VDF using the cached publisher account. A zero
process exit alone is insufficient: record the explicit published-file success
message and keep the complete upload log. Current preparation/upload state is
in docs/evidence/workshop-test-package.json and workshop-test-upload.txt.
Do not claim successful publication until SteamCMD confirms that exact item.

[VERIFIED SteamCMD upload] Published dev.5 to existing item 3810187215. The
generated VDF targets that exact ID; the retry process returned exit 0 and
`Committing update...Success.`. The first upload failed with Limit exceeded
during preview handling; its complete log is retained separately as
workshop-test-upload-preview-failed.txt. The successful retry omitted
previewfile, preserving the existing preview/title/visibility.

All 97 staged files still match the verified composition and archive. The
existing Steam-downloaded baseline was not written by this task. New subscribers
and test servers will receive the deliberately untested candidate; fully restart
server/clients and ensure both load dev.5 before native testing. All SP/dedicated
and legacy-save outcomes remain NOT TESTED. Stable release readiness remains
BLOCKED; no native gate was waived into a PASS.

## New listing, 2026-10-10

[VERIFIED SteamCMD upload] Old item 3810187215 returned File Not Found. At the user's direction a new public item 3817174798 was created for unchanged dev.5 content.
Preview upload failed with Limit exceeded; content-only retry committed successfully.
Logs: evidence/workshop-create-20261010.txt and evidence/workshop-create-retry-20261010.txt.
The old upload record remains historical evidence. G6/G7 NOT TESTED; stable G8 BLOCKED.
