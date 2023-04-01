# ffmpeg-binaries

## Windows x64 build

references:
- https://www.ffmpeg.org/platform.html#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64
- https://trac.ffmpeg.org/wiki/CompilationGuide/MinGW

- Install msys2
- Open Native Tools Command Prompt for VS 2022 (the cmd with VS 2022 environment variables set, these variables are needed to use MSVC from MSYS2 later)
- Run "msys2_shell.cmd -use-full-path" (this opens an MSYS2 with VS 2022 environment variables included)
(why -use-full-path: https://github.com/msys2/MSYS2-packages/issues/2140)

- pacman -S pkg-config

- mkdir build
- cd build
- ../scripts/configure-windows.sh
- make -j8
- make install

Working on making build.py (with mingw_build.sh) work but it doesn't work yet.

## Others

Run build.py
