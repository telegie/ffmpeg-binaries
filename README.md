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

brew install emscripten

mkdir build

cd build

Run configure-wasm.sh

emmake make -j8

## iOS

reference: https://github.com/kewlbear/FFmpeg-iOS-build-script/blob/master/build-ffmpeg.sh

brew install yasm

- mkdir build

- cd build

- ../scripts/configure-ios.sh

- make -j8

- make install

## Mac

Same as iOS, but with its own configure .sh file.
