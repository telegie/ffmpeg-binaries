# ffmpeg-binaries

## Windows x64 build

https://www.ffmpeg.org/platform.html#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows

- Install msys2

- Open msys2 from x64 Native Tools Command Prompt for VS 2019 with the following to open a msys2 shell inheriting PATH environment variable of the command prompt: msys2_shell.cmd -full-path

- ../FFmpeg/configure --toolchain=msvc --prefix=../install

- make -j8

- make install
