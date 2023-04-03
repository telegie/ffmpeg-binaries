# ffmpeg-binaries

## Windows x64 build

- python3 bootstrap.py

- Install msys2 and Visual Studio 2022

- Open x64 Native Tools Command Prompt for VS 2022 Current (the cmd with VS 2022 environment variables set, these variables are needed to use MSVC from MSYS2 later)

- Run "msys2_shell.cmd -use-full-path" (this opens an MSYS2 with VS 2022 environment variables included)
(why -use-full-path: https://github.com/msys2/MSYS2-packages/issues/2140)

- pacman -S pkg-config (inside the msys2 window from here)
- mkdir build (from the root directory of this repository)
- cd build
- ../build_windows.sh

references:
- https://www.ffmpeg.org/platform.html#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64
- https://trac.ffmpeg.org/wiki/CompilationGuide/MinGW


### Why not build.py for Windows?

The reason windows x64 build has a separate way of doing is due to FFmpeg requiring the following two things in configuration:
1. it should run autotools
2. it should have access to the complier for testing things.

The issue is that our target compiler is MSVC and it is hard to setup an environment that can run autotools (e.g., msys2) to have access to MSVC.

Opening msys2 from x64 Native Tools Command Prompt for VS 2022 is a way to do it as above.
Doing the equivalent of this in Python would allow merging our Windows build process into build.py but it is considered too time consuming for now.
Maybe someone can do this in the future... 


## Others

Run build.py
