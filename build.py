#!/usr/bin/env python3
import os
import platform
import subprocess
from pathlib import Path


def build_libvpx():
    here = Path(__file__).parent.resolve()
    subprocess.run(["python3", f"{here}/libvpx-binaries/build.py"])


def build_opus():
    here = Path(__file__).parent.resolve()
    subprocess.run(["python3", f"{here}/opus-binaries/build.py"])


def build_arm64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    pkg_config_path=f"{here}/opus-binaries/install/arm64-mac/lib/pkgconfig"

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=darwin",
                    "--arch=arm64",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-videotoolbox",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libvpx_vp9,libopus",
                    "--enable-decoder=vp8,vp9,libopus",
                    "--disable-encoder=opus",
                    "--disable-decoder=libvpx_vp8,libvpx_vp9,opus",
                    f"--extra-cflags=-I{here}/libvpx-binaries/1.10.0/arm64-mac/include",
                    f"--extra-ldflags=-L{here}/libvpx-binaries/1.10.0/arm64-mac/lib",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/install/arm64-mac"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def main():
    build_libvpx()
    build_opus()

    if platform.system() == "Darwin":
        if platform.machine() == "arm64":
            build_arm64_mac_binaries()
            return

    raise Exception(f"ffmpeg build not supported.")


if __name__ == "__main__":
	main()