# Custom mod icon

Project Version: 1.1.0-dev.17

User-selected 2026-10-18: use only the wooden fence subject from the approved
Fences & Gates thumbnail. Authoring source assets/artwork/fence-icon.png is
512x512 RGBA, with transparent gaps/background and no lettering or shadows.
The 64x64 mod icon at media/ui/B47ANCEDBuildableFences_icon.png is a Lanczos
resize of that source. Original vanilla wooden fence artwork is retained;
no wire or iron fencing is included in the icon. No AI-generated fence art.

This compatible PATCH iteration changes the mod-list icon only. Existing
poster.png, fallback branding assets and the live Workshop thumbnail remain
unchanged. The upload VDF omits previewfile, and the public preview hash is
compared before/after upload. No gameplay/recipe/authority/configuration changes.
No new gameplay sandbox option is needed for this presentation-only asset.

Source SHA-256: 88b28b3dd7088fc82feb862f77e5ae2859e5643418ab1aa4d8a4ea73226fc30a.
Runtime icon SHA-256: 50d2a0cddaa9e593e92245491ec8e91b5853fc47b7a80812559a1ed7e0be433e.

## Historical dev.16 icon

The earlier three-fence subject was replaced at the user's direction before a
successful dev.16 upload. Its source SHA-256 was
0c20461cd3e375daece3a15de1bae9174cc05273b83e717f6b19396b8b92e11d;
its runtime SHA-256 was
ed65f65709dd73dab3d70c2a60812800b9336d3d763b24a85f124af3275409ba.
The failed authentication attempt did not change Workshop content or thumbnail.

## Historical fallback branding

# Fallback artwork

Historical authoring version: 1.1.0-dev.11

Use manually supplied artwork first, independently for each role. Only missing roles use assets/branding/B47_ICON_SMALL.png (64x64 mod icon) and B47_ICON.png (128x128 poster) and B47_THUMBNAIL.png (512x512 Workshop thumbnail). Copy bytes without resizing or regenerating. Existing Eyewear thumbnail and Buildable Fences poster are custom and preserved. Future custom replacements take precedence. No UI project is included.

User-provided art on 2026-10-14. SHA-256 small: 60e2a193a6c1e1190941e6c342ec23c673a561dbed895c80067fe2b89c7f7e83; large: 0e30a776c77dbf66eeb9acfa7596c7f850cb5b334e8873ef94acbb3b071582c3.

This is asset-only work. Current version headers/mirrors identify this authoring iteration; all prior gameplay/API/runtime evidence remains historical at 1.1.0-dev.10 and its original source commits. No prior PASS is promoted to current evidence. No new game/dedicated tests, packages, deployment or publication. Projects without production mod.info retain these as authoring assets, not a fabricated runtime package.

Workshop thumbnail correction: B47_THUMBNAIL.png is a direct 512x512 resize of the user-supplied B47.png. Its SHA-256 is f775bff1783d59af91f331652740d5279fd5603f66d431c6349f38cbd2d9915b. Preserve custom thumbnails; the mod icon remains 64x64 and poster remains 128x128.
