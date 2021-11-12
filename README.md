# ffmpeg-binaries

## Windows x64 build


references:

https://www.ffmpeg.org/platform.html#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64

https://trac.ffmpeg.org/wiki/CompilationGuide/MinGW

- Install msys2

- Open mingw64_shell.

- ../FFmpeg/configure --target-os=mingw64 --arch=x86_64 --enable-shared --prefix=../install --enable-libvpx --enable-encoder=libvpx_vp8 --extra-cflags="-I /c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/include" --extra-ldflags="-L /c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/lib"

- make -j8

- make install



bin/libiconv-2.dll is from mingw64/bin. It is needed for using ffmpeg binaires built by mingw64.


## WASM using a mac

reference: https://itnext.io/build-ffmpeg-webassembly-version-ffmpeg-js-part-2-compile-with-emscripten-4c581e8c9a16

Install emscripten via source (not brew) following https://emscripten.org/docs/getting_started/downloads.html.

Add $EMSDK_ROOT/upstream/bin to path for llvm-ranlib, llvm-as, llvm-nm

Run scripts/configure-wasm.sh

emmake make -j8

## iOS

reference: https://github.com/kewlbear/FFmpeg-iOS-build-script

brew install yasm
