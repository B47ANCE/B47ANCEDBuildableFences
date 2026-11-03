# Bounded third-party environment observation

Project Version: 1.1.0-dev.19

Date: 2026-11-01. Purpose: explain a changed installed-Lua fingerprint during
the construction menu recipe audit, not reproduce the reporter's mod list.
Local path class: media/lua/client/pzopt and media/lua/shared/pzopt. Mod title,
author, source URL/Workshop ID, exact version, license and permissions: UNKNOWN.
No external implementation source was read or imported. Observations were
limited to names, timestamps and an identifier search for ISBuildPanel,
GetAllBuildableEntities, GetBuildableEntities, BuildLogic, filterRecipeList and
SpriteConfigManager in the client overlay directory; no matches were found.
That negative search does not establish compatibility or absence of indirect
hooks. No attribution of the external Workshop report is made.

The recipe audit's only changed fields were installed Lua count (1,407 to
1,409) and whole-Lua index digest. Recipe-script index, recorded native UI source
hashes, atlas/tile hashes and per-recipe overlap findings remained unchanged.
The independent partial-list regression and menu fix were written before this
bounded overlay observation. Requirements and implementation rely only on the
project's own source, original tests and verified vanilla Lua calls.

Clean-room checklist: code/assets/text imported NONE; external files modified
NONE; external code executed NONE; new dependency NONE; attribution obligations
for reuse N/A because no reuse occurred. Source-only review; runtime NOT TESTED.
Independent reviewer signoff on this environment note remains pending in the PR.
Unknown rights block copying, not this metadata-only observation.
