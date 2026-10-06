#!/usr/bin/env python3
"""Exercise the basic demo through Android taps and actual rendered pixels."""

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import time

from PIL import Image, ImageChops


PACKAGE = "io.renfletpy.twodtest"
BACKGROUND = (17, 19, 24)
REACHABLE = (69, 151, 191)
SELECTED = (214, 181, 69)


def adb(*args):
    return subprocess.check_output(["adb", *args], timeout=120)


def capture(path):
    image = Image.open(BytesIO(adb("exec-out", "screencap", "-p"))).convert("RGB")
    image.save(path)
    return image


def screen_position(image, x, y):
    # Find the game's opaque background, excluding Android bars and letterboxing.
    difference = ImageChops.difference(image, Image.new("RGB", image.size, BACKGROUND))
    mask = difference.convert("L").point(lambda value: 255 if value < 3 else 0)
    bounds = mask.getbbox()
    if bounds is None:
        raise AssertionError("The game background is missing")
    left, top, right, bottom = bounds
    return round(left + x * (right - left) / 1280), round(top + y * (bottom - top) / 720)


def tap(image, x, y):
    px, py = screen_position(image, x, y)
    adb("shell", "input", "tap", str(px), str(py))
    time.sleep(1)


def expect_color(image, x, y, expected):
    actual = image.getpixel(screen_position(image, x, y))
    if max(abs(a - b) for a, b in zip(actual, expected)) > 3:
        raise AssertionError(f"At game position {(x, y)}: expected {expected}, got {actual}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("android-smoke"))
    args = parser.parse_args()
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)

    try:
        adb("wait-for-device")
        adb("install", "-r", str(args.apk))
        adb("shell", "input", "keyevent", "82")
        adb("shell", "settings", "put", "system", "accelerometer_rotation", "0")
        adb("shell", "settings", "put", "system", "user_rotation", "1")
        adb("shell", "am", "force-stop", PACKAGE)
        adb("logcat", "-c")
        adb("shell", "am", "start", "-W", "-n", PACKAGE + "/org.sdk.runner.RunnerActivity")

        deadline = time.monotonic() + 90
        while True:
            image = capture(output / "launch.png")
            colors = {color: count for count, color in image.getcolors(image.width * image.height)}
            if colors.get(REACHABLE, 0) > 100 and colors.get((76, 136, 211), 0) > 30:
                break
            if time.monotonic() >= deadline:
                raise AssertionError("The board and player did not render within 90 seconds")
            time.sleep(2)

        tap(image, 430, 350)
        tap(image, 376, 347)
        image = capture(output / "moved.png")
        expect_color(image, 376, 368, SELECTED)

        tap(image, 442, 284)
        image = capture(output / "raised.png")
        expect_color(image, 442, 306, SELECTED)

        tap(image, 1080, 27)
        image = capture(output / "reset.png")
        expect_color(image, 350, 350, REACHABLE)
        expect_color(image, 430, 350, (74, 170, 157))

        tap(image, 1190, 27)
        deadline = time.monotonic() + 10
        while True:
            activities = adb("shell", "dumpsys", "activity", "activities").decode()
            resumed = [line for line in activities.splitlines()
                       if "mResumedActivity" in line or "topResumedActivity" in line]
            if resumed and all(PACKAGE not in line for line in resumed):
                break
            if time.monotonic() >= deadline:
                raise AssertionError("QUIT did not leave the game activity")
            time.sleep(1)

        print("Android basic demo passed: launch, move, height change, reset, and quit.")
    finally:
        logs = subprocess.run(["adb", "logcat", "-d", "-v", "time"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
        (output / "logcat.txt").write_bytes(logs.stdout)


if __name__ == "__main__":
    main()
