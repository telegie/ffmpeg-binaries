# ffmpeg-binaries

## Windows x64 build

https://www.ffmpeg.org/platform.html#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows

https://trac.ffmpeg.org/wiki/CompilationGuide/MSVC

- Install msys2

- Open msys2 from x64 Native Tools Command Prompt for VS 2022 with the following to open a msys2 shell inheriting PATH environment variable of the command prompt: msys2_shell.cmd -full-path

- ../FFmpeg/configure --target-os=win64 --arch=x86_64 --enable-shared --enable-libvpx --toolchain=msvc --prefix=../install --extra-cflags="-I/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/libvpx" --extra-ldflags="-LIBPATH:/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-vs16/release" --enable-encoder=libvpx_vp8 --enable-decoder=libvpx_vp8


C:\Users\hanseul\repos\telegie

- make -j8

- make install
