# RenFletPy 2D Test

A pure-2D isometric tactics experiment built on the RenFletPy architecture derived from the separate `SDK-` repository.

`SDK-` is treated as **read-only upstream reference**. This repository does not modify it.

## What this test is trying to prove

The battlefield is logical 3D data:

```python
board[z][y][x]
```

but rendering is entirely 2D.

The renderer does **not** draw three complete Z planes as disconnected slabs. Instead, every walkable surface produces independent draw items:

- top face
- exposed left cliff/fascia
- exposed right cliff/fascia
- units

Those items are painter-sorted at **face level**. Solid raised terrain generates cliff faces down to lower neighboring terrain. Shelf/bridge tiles generate only a thin fascia, so the space underneath remains visually and logically usable.

The demo deliberately contains:

- a full ground floor
- a solid raised platform
- a thin shelf/bridge over ground
- a second-storey balcony
- a unit underneath an upper shelf
- a unit standing on the upper shelf
- height-aware movement and jump rules

## Android build

GitHub Actions builds an installable APK.

The workflow pins the upstream `SDK-` repository to a specific commit, checks it out into the CI workspace, overlays this repository's `game/`, applies a small RenFletPy test-host patch, and then runs the upstream Android builder.

The patch only affects the temporary CI copy:

- Android application id becomes `io.renfletpy.twodtest`
- app label becomes `RenFletPy 2D Test`
- the embedded Flutter/Flet panel is collapsed to 1 px so the Ren'Py tactics renderer can use essentially the full display

The original `SDK-` repository is never changed.

After a successful workflow run, Android users can download the current phone build directly:

https://github.com/hujuhhujuh9-max/2d-test/releases/download/phone-latest/renfletpy-2d-test-arm64.apk

This is an **arm64** build for normal modern Android phones. It avoids the much larger universal/x86 test package produced internally by the upstream validation build.

On Android: tap the link, allow the browser to download the APK, then open it and allow installation from that browser if Android asks.

## Controls

- Tap a blue unit to select it.
- Reachable surfaces turn blue.
- Tap a blue surface to move.
- `RESET` restores the demo.
- `QUIT` exits.

## Upstream architecture

The pinned RenFletPy base keeps Ren'Py/SDL as Android startup owner and the single Python interpreter. Flutter/Flet remains embedded in that host, but is visually collapsed for this graphics-focused test.
