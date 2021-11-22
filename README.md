# ffmpeg-binaries

## Windows x64 build


references:

https://www.ffmpeg.org/platform.html#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64

https://trac.ffmpeg.org/wiki/CompilationGuide/MinGW

- Install msys2

- Open mingw64 shell.

Run scripts/configure-windows.sh

- make -j8

- make install

## WASM using a mac

reference: https://itnext.io/build-ffmpeg-webassembly-version-ffmpeg-js-part-2-compile-with-emscripten-4c581e8c9a16

Install emscripten via source (not brew) following https://emscripten.org/docs/getting_started/downloads.html.

Add $EMSDK_ROOT/upstream/bin to path for llvm-ranlib, llvm-as, llvm-nm

Run scripts/configure-wasm.sh

emmake make -j8

## iOS

reference: https://github.com/kewlbear/FFmpeg-iOS-build-script/blob/master/build-ffmpeg.sh

brew install yasm

Run scripts/configure-ios.sh

- make -j8

- make install
