#!/usr/bin/env python3
import argparse
import os
import platform
import urllib.request
import shutil
import subprocess
import sys
from pathlib import Path


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


def build_arm64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/arm64-mac/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/arm64-mac/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=darwin",
                    "--arch=arm64",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-videotoolbox",
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/arm64-mac"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_x64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/x64-mac/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/x64-mac/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=darwin",
                    "--arch=x86_64",
                    "--enable-cross-compile",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-videotoolbox",
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    "--extra-cflags=-arch x86_64",
                    "--extra-ldflags=-arch x86_64",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/x64-mac"],
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
    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/arm64-ios/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/arm64-ios/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphoneos",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphone_sdk_path = xcrun_output.stdout.decode("utf-8").strip()

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
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    "--extra-cflags=-mios-version-min=14.0",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/arm64-ios"],
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
    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/arm64-iphonesimulator/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/arm64-iphonesimulator/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphonesimulator",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphonesimulator_sdk_path = xcrun_output.stdout.decode("utf-8").strip()

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
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    "--extra-cflags=-miphonesimulator-version-min=14.0",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/arm64-iphonesimulator"],
                   cwd=build_path,
                   check=True,
                   env={"PATH": path})

    subprocess.run(["make", "-C", build_path, "-j8"], check=True, env={"PATH": path})
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_x64_linux_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-linux"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/x64-linux/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/x64-linux/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    subprocess.run([f"{here}/FFmpeg/configure",
                    "--target-os=linux",
                    "--arch=x86_64",
                    "--disable-debug",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-videotoolbox",
                    "--disable-lzma",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libvpx_vp9,libopus",
                    "--enable-decoder=vp8,vp9,libopus",
                    "--disable-encoder=opus",
                    "--disable-decoder=libvpx_vp8,libvpx_vp9,opus",
                    "--extra-cflags=-fPIC",
                    "--pkg-config-flags=--static",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/x64-linux"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_wasm32_emscripten_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/wasm32-emscripten"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    # llvm_nm = "/opt/homebrew/Cellar/emscripten/3.1.23/libexec/llvm/bin/llvm-nm"
    llvm_nm = "/Users/hanseuljun/repos/emsdk/upstream/bin/llvm-nm"

    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/wasm32-emscripten/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/wasm32-emscripten/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    subprocess.run(["emconfigure",
                    f"{here}/FFmpeg/configure",
                    "--target-os=none",
                    "--arch=x86_32",
                    "--enable-cross-compile",
                    f"--nm={llvm_nm}",
                    "--ar=emar",
                    "--ranlib=emranlib",
                    "--cc=emcc",
                    "--cxx=em++",
                    "--objcc=emcc",
                    "--dep-cc=emcc",
                    "--disable-debug",
                    "--disable-pthreads",
                    "--disable-x86asm",
                    "--disable-inline-asm",
                    "--disable-stripping",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    "--disable-pthreads",
                    "--extra-cflags=-fPIC -O3",
                    "--extra-ldflags=-s INITIAL_MEMORY=33554432",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/wasm32-emscripten"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "install"], check=True)


def build_wasm32_emscripten_mt_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/wasm32-emscripten-mt"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    llvm_nm = "/opt/homebrew/Cellar/emscripten/3.1.23/libexec/llvm/bin/llvm-nm"

    libvpx_pkgconfig = f"{here}/libvpx-binaries/output/wasm32-emscripten/lib/pkgconfig"
    opus_pkgconfig = f"{here}/opus-binaries/output/wasm32-emscripten/lib/pkgconfig"
    pkg_config_path = f"{libvpx_pkgconfig}:{opus_pkgconfig}"

    subprocess.run(["emconfigure",
                    f"{here}/FFmpeg/configure",
                    "--target-os=none",
                    "--arch=x86_32",
                    "--enable-cross-compile",
                    f"--nm={llvm_nm}",
                    "--ar=emar",
                    "--ranlib=emranlib",
                    "--cc=emcc",
                    "--cxx=em++",
                    "--objcc=emcc",
                    "--dep-cc=emcc",
                    "--disable-debug",
                    "--disable-pthreads",
                    "--disable-x86asm",
                    "--disable-inline-asm",
                    "--disable-stripping",
                    "--disable-programs",
                    "--disable-doc",
                    "--disable-everything",
                    "--enable-libvpx",
                    "--enable-libopus",
                    "--enable-encoder=libvpx_vp8,libopus",
                    "--enable-decoder=libvpx_vp8,libopus",
                    "--enable-parser=vp8,opus",
                    "--enable-pthreads",
                    "--extra-cflags=-pthread -s USE_PTHREADS=1 -fPIC -O3",
                    "--extra-ldflags=-pthread -s INITIAL_MEMORY=33554432",
                    f"--env=PKG_CONFIG_PATH={pkg_config_path}",
                    f"--prefix={here}/output/wasm32-emscripten-mt"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "install"], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--targets", type=str)
    parser_args = parser.parse_args()

    if parser_args.targets is None:
        if platform.system() == "Windows":
            raise Exception("To build ffmpeg, run build_windows.sh in msys2 with access to cl.exe")
        elif platform.system() == "Darwin":
            targets = ["arm64-mac",
                       "x64-mac",
                       "arm64-ios",
                       "arm64-iphonesimulator",
                       "wasm32-emscripten"]
        elif platform.system() == "Linux":
            targets = ["x64-linux"]
        else:
            raise Exception(f"ffmpeg build not supported.")
    else:
        targets = parser_args.targets.split(",")

    here = Path(__file__).parent.resolve()
    subprocess.run(["python3", f"{here}/libvpx-binaries/build.py"] + sys.argv[1:], check=True)
    subprocess.run(["python3", f"{here}/opus-binaries/build.py"] + sys.argv[1:], check=True)

    if parser_args.rebuild:
        build_path = Path(f"{here}/build")
        output_path = Path(f"{here}/output")
        if build_path.exists():
            shutil.rmtree(build_path)
        if output_path.exists():
            shutil.rmtree(output_path)

    if "arm64-mac" in targets:
        build_arm64_mac_binaries()
    if "x64-mac" in targets:
        build_x64_mac_binaries()
    if "x64-linux" in targets:
        build_x64_linux_binaries()
    if "arm64-ios" in targets:
        build_arm64_ios_binaries()
    if "arm64-iphonesimulator" in targets:
        build_arm64_iphonesimulator_binaries()
    if "wasm32-emscripten" in targets:
        build_wasm32_emscripten_binaries()


if __name__ == "__main__":
	main()