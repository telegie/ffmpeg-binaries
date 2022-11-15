#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
from pathlib import Path
import urllib.request
import stat


# Need this perl script for building iOS binaries.
# from https://github.com/kewlbear/FFmpeg-iOS-build-script
def download_gas_preprocessor():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    gas_preprocessor_path = f"{build_path}/gas-preprocessor.pl"
    if os.path.exists(gas_preprocessor_path):
        return build_path

    urllib.request.urlretrieve("https://github.com/libav/gas-preprocessor/raw/master/gas-preprocessor.pl",
                               gas_preprocessor_path)
    subprocess.run(["chmod", "+x", gas_preprocessor_path], check=True)
    return build_path


def build_libvpx():
    here = Path(__file__).parent.resolve()
    subprocess.run(["python3", f"{here}/libvpx-binaries/build.py"], check=True)


def build_opus():
    here = Path(__file__).parent.resolve()
    subprocess.run(["python3", f"{here}/opus-binaries/build.py"], check=True)


def build_arm64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    libvpx_pkgconfig = f"{here}/libvpx-binaries/install/arm64-mac/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/install/arm64-mac/lib/pkgconfig"
    pkg_config_path=f"{libvpx_pkgconfig}:{opus_pkgconfig}"

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
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/install/arm64-mac"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_arm64_ios_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-ios"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    gas_preprocessor_dir = download_gas_preprocessor()
    env = os.environ.copy()
    path = env["PATH"]
    path = f"{gas_preprocessor_dir}:{path}"

    cc = "xcrun --sdk iphoneos clang"
    libvpx_pkgconfig = f"{here}/libvpx-binaries/install/arm64-ios/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/install/arm64-ios/lib/pkgconfig"
    pkg_config_path=f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphoneos",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphone_sdk_path = xcrun_output.stdout.decode("utf-8")

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=darwin",
                    "--arch=arm64",
                    "--enable-cross-compile",
                    f"--cc={cc}",
                    f"--as=gas-preprocessor.pl -arch aarch64 -- {cc}",
                    f"--sysroot={iphone_sdk_path}",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-videotoolbox",
                    "--disable-audiotoolbox",
                    "--disable-iconv",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libvpx_vp9,libopus",
                    "--enable-decoder=vp8,vp9,libopus",
                    "--disable-encoder=opus",
                    "--disable-decoder=libvpx_vp8,libvpx_vp9,opus",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/install/arm64-ios"],
                   cwd=build_path,
                   check=True,
                   env={"PATH": path})

    subprocess.run(["make", "-C", build_path, "-j8"], check=True, env={"PATH": path})
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_arm64_iphonesimulator_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-iphonesimulator"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    gas_preprocessor_dir = download_gas_preprocessor()
    env = os.environ.copy()
    path = env["PATH"]
    path = f"{gas_preprocessor_dir}:{path}"

    cc = "xcrun --sdk iphonesimulator clang"
    libvpx_pkgconfig = f"{here}/libvpx-binaries/install/arm64-iphonesimulator/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/install/arm64-iphonesimulator/lib/pkgconfig"
    pkg_config_path=f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphonesimulator",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphonesimulator_sdk_path = xcrun_output.stdout.decode("utf-8")

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=darwin",
                    "--arch=arm64",
                    "--enable-cross-compile",
                    f"--cc={cc}",
                    f"--as=gas-preprocessor.pl -arch aarch64 -- {cc}",
                    f"--sysroot={iphonesimulator_sdk_path}",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--enable-pic",
                    "--disable-videotoolbox",
                    "--disable-audiotoolbox",
                    "--disable-iconv",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libvpx_vp9,libopus",
                    "--enable-decoder=vp8,vp9,libopus",
                    "--disable-encoder=opus",
                    "--disable-decoder=libvpx_vp8,libvpx_vp9,opus",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/install/arm64-iphonesimulator"],
                   cwd=build_path,
                   check=True,
                   env={"PATH": path})

    subprocess.run(["make", "-C", build_path, "-j8"], check=True, env={"PATH": path})
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def main():
    build_libvpx()
    build_opus()

    if platform.system() == "Darwin":
        if platform.machine() == "arm64":
            build_arm64_mac_binaries()
            build_arm64_ios_binaries()
            build_arm64_iphonesimulator_binaries()
            return

    raise Exception(f"ffmpeg build not supported.")


if __name__ == "__main__":
	main()