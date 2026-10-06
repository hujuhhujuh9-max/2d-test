#!/usr/bin/env python3
"""Patch a temporary SDK- checkout for the independent RenFletPy 2D test."""

from pathlib import Path
import sys


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare_upstream.py PATH_TO_SDK_CHECKOUT")

    root = Path(sys.argv[1]).resolve()

    replace_once(
        root / "android/app/build.gradle",
        'applicationId "org.sdk.runner"',
        'applicationId "io.renfletpy.twodtest"',
    )

    replace_once(
        root / "android/app/src/main/AndroidManifest.xml",
        'android:label="Runner integration"',
        'android:label="RenFletPy 2D Test"',
    )

    replace_once(
        root / "android/app/src/main/java/org/sdk/runner/RunnerActivity.java",
        "int fletHeight = Math.max(1, available * 2 / 5);",
        "int fletHeight = 1;",
    )

    print("Prepared temporary RenFletPy test host:", root)


if __name__ == "__main__":
    main()
