#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
from pathlib import Path


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
    subprocess.run(args,
                   check=check)


def run_autogen_windows():
    here = Path(__file__).parent.resolve()
    run_in_mingw(["/bin/bash",
                  "--login",
                  f"{here}/opus/autogen.sh"],
                  check=True)


def run_autogen():
    here = Path(__file__).parent.resolve()
    subprocess.run([f"{here}/opus/autogen.sh"],
                   check=True)


def build_x64_windows_binaries(rebuild):
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-windows"
    output_path = f"{here}/output/x64-windows"

    if not rebuild and os.path.exists(output_path):
        print("opus x64-windows build already built")
        return

    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run(["cmake",
                    "-S", f"{here}/opus",
                    "-B", build_path,
                    "-D", "OPUS_FORTIFY_SOURCE=OFF",
                    "-D", "OPUS_STACK_PROTECTOR=OFF",
                    "-D", f"CMAKE_INSTALL_PREFIX={output_path}"],
                    check=True)
    subprocess.run(["msbuild",
                    f"{build_path}/INSTALL.vcxproj",
                    "/p:Configuration=RelWithDebInfo"],
                    check=True)


def build_arm64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-doc",
                    "--disable-extra-programs",
                    "--host=arm-apple-darwin",
                    f"--prefix={here}/output/arm64-mac",
                    "CFLAGS=-arch arm64 -O2"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["make", "install"], cwd=build_path, check=True)


def build_x64_mac_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-mac"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-doc",
                    "--disable-extra-programs",
                    "--host=x86_64-apple-darwin",
                    f"--prefix={here}/output/x64-mac",
                    "CFLAGS=-arch x86_64 -O2"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["make", "install"], cwd=build_path, check=True)


def build_arm64_ios_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-ios"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphoneos",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)
    iphone_sdk_path = xcrun_output.stdout.decode("utf-8").strip()
    cflags=f"-arch arm64 -mios-version-min=14.0 -isysroot {iphone_sdk_path} -O2"

    subprocess.run([f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-doc",
                    "--disable-extra-programs",
                    "--host=arm-apple-darwin",
                    f"--prefix={here}/output/arm64-ios",
                    f"CFLAGS={cflags}"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["make", "install"], cwd=build_path, check=True)


def build_arm64_iphonesimulator_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/arm64-iphonesimulator"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    xcrun_output = subprocess.run(["xcrun",
                                   "--sdk", "iphonesimulator",
                                   "--show-sdk-path"],
                                  capture_output=True,
                                  check=True)

    iphonesimulator_sdk_path = xcrun_output.stdout.decode("utf-8").strip()
    cflags=f"-arch arm64 -miphonesimulator-version-min=14.0 -isysroot {iphonesimulator_sdk_path} -O2"

    subprocess.run([f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-doc",
                    "--disable-extra-programs",
                    "--host=arm-apple-darwin",
                    f"--prefix={here}/output/arm64-iphonesimulator",
                    f"CFLAGS={cflags}"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["make", "install"], cwd=build_path, check=True)


def build_x64_linux_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/x64-linux"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    subprocess.run([f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-doc",
                    "--disable-extra-programs",
                    f"--prefix={here}/output/x64-linux",
                    "CFLAGS=-fPIC -O2"],
                   cwd=build_path,
                   check=True)
    subprocess.run(["make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["make", "install"], cwd=build_path, check=True)


def build_wasm32_emscripten_binaries():
    here = Path(__file__).parent.resolve()
    build_path = f"{here}/build/wasm32-emscripten"
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    env = os.environ.copy()
    env["CFLAGS"] = "-fPIC -O3"

    subprocess.run(["emconfigure",
                    f"{here}/opus/configure",
                    "--disable-shared",
                    "--disable-asm",
                    "--disable-intrinsics",
                    "--disable-doc",
                    "--disable-extra-programs",
                    "--disable-stack-protector",
                    f"--prefix={here}/output/wasm32-emscripten"],
                   cwd=build_path,
                   check=True,
                   env=env)
    subprocess.run(["emmake", "make", "-j8"], cwd=build_path, check=True)
    subprocess.run(["emmake", "make", "install"], cwd=build_path, check=True)


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
            raise Exception(f"opus build not supported.")
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

    if platform.system() == "Windows":
        build_x64_windows_binaries(parser_args.rebuild)
    elif platform.system() == "Darwin":
        run_autogen()
    elif platform.system() == "Linux":
        run_autogen()

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
        build_wasm32_emscripten_binaries()


if __name__ == "__main__":
	main()
