# ffmpeg-binaries

## Windows x64 build

https://www.ffmpeg.org/platform.html#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows

- Install msys2

- Open msys2 from x64 Native Tools Command Prompt for VS 2019 with the following to open a msys2 shell inheriting PATH environment variable of the command prompt: msys2_shell.cmd -full-path

- ../FFmpeg/configure --arch=x86_64 --toolchain=msvc --enable-cross-compile

- make -j8








https://www.ffmpeg.org/platform.html#Cross-compilation-for-Windows-with-Linux-1

Clone repository using in WSL2 and continue with WSL2.

mkdir build

cd build

sudo apt install gcc-mingw-w64-x86-64

../FFmpeg/configure --arch=x86_64 --target-os=mingw64 --cross-prefix=x86_64-w64-mingw32- --prefix=../install

make

make install




../FFmpeg/configure --arch=x86_64 --target-os=mingw64 --cross-prefix=i386-mingw32msvc- --prefix=../install