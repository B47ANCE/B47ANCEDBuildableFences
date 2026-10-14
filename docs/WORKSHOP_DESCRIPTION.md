# Workshop candidate description

Project Version: 1.1.0-dev.8

Canonical BBCode: WORKSHOP_DESCRIPTION.txt. Candidate describes six fence-family
selectors, each with native per-part recipes, plus a separate iron gate.
No upload performed for this iteration. Preserve real newlines and current
Workshop identity 3817174798. Native SP/dedicated acceptance remains pending.

---

## Historical dev.6 notes

The following is retained for provenance, not current instructions or dev.7
validation. Current family selection and test gates are described above and
in docs/FAMILY_SELECTORS.md.

# Current candidate Workshop documentation

Historical Project Version: 1.1.0-dev.6

Technical ID B47ANCEDBuildableFences; Workshop ID 3817174798.
workshop-update.properties preserves workshopid=3817174798. The user explicitly
authorized an untested Workshop prerelease for dedicated testing. Canonical
player-facing BBCode is WORKSHOP_DESCRIPTION.txt at project root. See
WORKSHOP_DEV5_TEST_RELEASE.md; this is not a readiness claim.

B47ANCE'd Buildable Fences provides 21 vanilla-art buildable fence pieces:
seven tall-wooden variants; four military; three Security; three Razor; four
wrought iron. The authorized test package also includes the native iron gate.
For Wrought Iron, one Fence entry cycles all existing pieces/faces using Q/E.
The gate is separate and selects W/N closed placement. Other families retain
manual menus pending native/dedicated validation.

Construction skills for every variant: Tall Wooden Straight Top requires
Carpentry 4; Tall Wooden Sloped Top requires Carpentry 7; Security and Razor-Wire
Security require Welding 4; Military requires Welding 7. Wrought Iron remains
Welding 7. Materials, XP rewards and health fields are unchanged by the rebalance.

Security and Razor require one mixed Concrete Use for straight/end sections
and two Concrete Uses for corners, plus their welding inputs. Razor retains
Barbed Wire. A full metal/carved mixed-concrete bucket has four uses.
Blowtorch Uses and rod uses consume capacity, not entire full containers.

Standalone posts retain the baseline nonblocking conversion and accepted
same-tile rendering limitation. Wooden cutaway parity is unresolved. Material
audio and dedicated persistence require runtime evidence. The candidate has
not passed runtime release gates. An explicitly untested package is prepared
for dedicated testing under the user's bounded publication exception.

Development note: 1.0.37 entity/sprite identities remain defined. Native
old-save compatibility is untested; no save-safe claim. Prototype startup
phase fix awaits native verification.

## Description polish, 2026-10-10

[VERIFIED Steam API] Published text matches WORKSHOP_DESCRIPTION.txt exactly;
real paragraph breaks, zero literal newline escapes, public visibility.
The description leads with fence styles and uses short sections for skills,
placement, sandbox health, known issues and the optional test kit. Internal
startup implementation details remain in development docs.

Publishing VDFs must retain real line breaks inside quoted values. The shared
workspace generator and the fence preparation script now preserve them.
Use scripts/prepare_workshop_metadata.py --visibility Public --output <new-vdf>
for an explicitly authorized description-only update to this public listing;
it reads the current WORKSHOP_ID.txt and does not upload gameplay files.

[TESTED Windows offline] tools/tests/Test-WorkshopVdf.ps1: 15 checks PASS.
scripts/check_versions.py --root B47ANCEDBuildableFences --release: PASS.
Full Lua suite remains blocked by missing lupa in the documented interpreter.
No PZ runtime test was performed; G6/G7 remain NOT TESTED and stable G8 BLOCKED.

[UNKNOWN browser rendering] Steam Community returned a hidden/permission error
on refresh despite public visibility and matching text in the official API.
See evidence/workshop-description-verification-20261010.json and
workshop-description-final-20261010.txt for publication evidence.

## Current dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.
