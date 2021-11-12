# ffmpeg-binaries

## Windows x64 build

https://www.ffmpeg.org/platform.html#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows

https://trac.ffmpeg.org/wiki/CompilationGuide/MSVC

- Install msys2

- Open mingw64_shell.

- ../FFmpeg/configure --target-os=mingw64 --arch=x86_64 --enable-shared --prefix=../install

- ../FFmpeg/configure --target-os=mingw64 --arch=x86_64 --enable-shared --prefix=../install --enable-libvpx --extra-cflags="-I /c/tools/msys64/usr/include -I /c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/include"

--sysroot=/c/tools/msys64



- ../FFmpeg/configure --target-os=mingw64 --arch=x86_64 --enable-shared --prefix=../install --enable-libvpx --extra-cflags="-I/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/include" --extra-ldflags="-L/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/lib/x64" --enable-encoder=libvpx_vp8 --enable-decoder=libvpx_vp8



- make -j8

- make install




bin/libiconv-2.dll is from mingw64/bin.




- Open msys2 from x64 Native Tools Command Prompt for VS 2022 with the following to open a msys2 shell inheriting PATH environment variable of the command prompt: msys2_shell.cmd -full-path





- ../FFmpeg/configure --target-os=win64 --arch=x86_64 --enable-shared --enable-libvpx --toolchain=msvc --prefix=../install --extra-cflags="-I/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-vs16/include -lmsvcrtd -std=c11" --extra-ldflags="-LIBPATH:/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-vs16/lib/x64" --enable-encoder=libvpx_vp8 --enable-decoder=libvpx_vp8

- ../FFmpeg/configure --target-os=win64 --arch=x86_64 --enable-shared --enable-libvpx --toolchain=mingw --prefix=../install --extra-cflags="-I/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-vs16/include -lmsvcrtd -std=c11" --extra-ldflags="-LIBPATH:/c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-vs16/lib/x64" --enable-encoder=libvpx_vp8 --enable-decoder=libvpx_vp8
