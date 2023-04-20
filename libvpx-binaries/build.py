#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
from pathlib import Path


COMMON_OPTIONS = [
    "--enable-ccache",
    "--disable-install-bins",
    "--disable-examples",
    "--disable-tools",
    "--disable-docs",
    "--disable-unit-tests",
    "--disable-vp9",
    "--disable-webm-io",
    "--disable-libyuv"
]


def find_msys64_env():
    path1 = "c:/msys64/usr/bin/env.exe"
    if os.path.exists(path1):
        return path1
    path2 = "c:/tools/msys64/usr/bin/env.exe"
    if os.path.exists(path2):
        return path2
    return None
    

def run_in_mingw(extra_args, check=False):
    msys64_env_path = find_msys64_env()
    if msys64_env_path == None:
        raise "No msys64 env"

    args = [msys64_env_path, "MSYSTEM=MINGW64"]
    args = args + extra_args
    subprocess.run(args, check=check)


def build_x64_windows_binaries(rebuild):
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-windows"
    output_path = f"{here}/output/x64-windows"

    if not rebuild and os.path.exists(output_path):
       print("libvpx x64-windows build already built")
       return

    if not os.path.exists(build_path):
        os.makedirs(build_path)

    # TODO: Support other drives than C drive.
    mingw_here = str(here).replace("C:\\", "/c/").replace("\\", "/")
    run_in_mingw(["/bin/bash",
                  "--login",
                  f"{here}/mingw_build.sh",
                  mingw_here,
                  build_path],
                  check=True)
    subprocess.run(["MSBuild.exe",
                    f"{build_path}/vpx.sln",
                    "/p:Configuration=Release"],
                    check=True)
    run_in_mingw(["/bin/bash",
                  "--login",
                  f"{here}/mingw_install.sh",
                  build_path],
                  check=True)
    # Rename the outcome .lib file to vpx.lib as ffmpeg expects the filename
    # to be vpx.lib.
    os.rename(f"{output_path}/lib/x64/vpxmt.lib", f"{output_path}/lib/x64/vpx.lib")


def build_arm64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/libvpx/configure",
                    "--target=arm64-darwin20-gcc",
                    f"--prefix={here}/output/arm64-mac"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_x64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/libvpx/configure",
                    "--target=x86_64-darwin20-gcc",
                    f"--prefix={here}/output/x64-mac"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_arm64_ios_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-ios"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/libvpx/configure",
                    "--target=arm64-darwin-gcc",
                    f"--prefix={here}/output/arm64-ios"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_arm64_iphonesimulator_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-iphonesimulator"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    cc = "xcrun --sdk iphonesimulator clang"
    cxx = "xcrun --sdk iphonesimulator clang++"

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphonesimulator",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphonesimulator_sdk_path = xcrun_output.stdout.decode("utf-8").strip()
    cflags=f"-arch arm64 -isysroot {iphonesimulator_sdk_path}"

    env = {"CC": cc, "CXX": cxx, "EXTRA_CFLAGS": cflags}

    subprocess.run([f"{here}/libvpx/configure",
                    "--target=generic-gnu",
                    f"--prefix={here}/output/arm64-iphonesimulator"],
                   cwd=build_path,
                   check=True,
                   env=env)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_x64_linux_binaries():
    subprocess.run(["sudo", "apt", "install", "-y", "yasm"], check=True)

    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-linux"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/libvpx/configure",
                    "--target=x86_64-linux-gcc",
                    "--enable-pic",
                    f"--prefix={here}/output/x64-linux"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["make", "-C", build_path, "install"], check=True)


def build_wasm32_emscripten():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/wasm32-emscripten"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run(["emconfigure",
                    f"{here}/libvpx/configure",
                    "--target=generic-gnu",
                    f"--prefix={here}/output/wasm32-emscripten"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "install"], check=True)


def build_wasm32_emscripten_mt():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/wasm32-emscripten-mt"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    env = os.environ.copy()
    env["LDFLAGS"] = "-pthread"

    subprocess.run(["emconfigure",
                    f"{here}/libvpx/configure",
                    "--target=generic-gnu",
                    f"--prefix={here}/output/wasm32-emscripten-mt",
                    "--extra-cflags=-pthread -s USE_PTHREADS=1",
                    "--enable-multithread"] + COMMON_OPTIONS,
                   cwd=build_path,
                   check=True,
                   env=env)
    subprocess.run(["emmake", "make", "-C", build_path, "-j8"], check=True)
    subprocess.run(["emmake", "make", "-C", build_path, "install"], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--targets", type=str)
    parser_args = parser.parse_args()

    if parser_args.targets is None:
        if platform.system() == "Windows":
            targets = ["x64-windows"]
        elif platform.system() == "Darwin":
            targets = ["arm64-mac",
                       "x64-mac",
                       "arm64-ios",
                       "arm64-iphonesimulator",
                       "wasm32-emscripten"]
        elif platform.system() == "Linux":
            targets = ["x64-linux"]
        else:
            raise Exception(f"libvpx build not supported.")
    else:
        targets = parser_args.targets.split(",")

    here = Path(__file__).parent.resolve()
    if parser_args.rebuild:
        build_path = Path(f"{here}/build")
        output_path = Path(f"{here}/output")
        if build_path.exists():
            shutil.rmtree(build_path)
        if output_path.exists():
            shutil.rmtree(output_path)

    if "x64-windows" in targets:
        build_x64_windows_binaries(parser_args.rebuild)
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
        build_wasm32_emscripten()


if __name__ == "__main__":
	main()
