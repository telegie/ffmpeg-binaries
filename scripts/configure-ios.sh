#!/bin/bash

# need to install https://github.com/libav/gas-preprocessor

# from https://github.com/kewlbear/FFmpeg-iOS-build-script
../FFmpeg/configure \
  --target-os=darwin \
  --arch=arm64 \
  --enable-cross-compile \
  --cc="xcrun -sdk iphoneos clang" \
  --sysroot=$(xcrun --sdk iphoneos --show-sdk-path) \
  --disable-debug \
  --disable-programs \
  --disable-doc \
  --disable-videotoolbox \
  --disable-audiotoolbox \
  --disable-iconv \
  --enable-encoder=libvpx_vp8 \
  --extra-cflags="-I/Users/hanseuljun/repos/telegie/deps/libvpx-binaries/1.10.0/arm64-darwin-gcc/include" \
  --extra-ldflags="-L/Users/hanseuljun/repos/telegie/deps/libvpx-binaries/1.10.0/arm64-darwin-gcc/lib -lvpx" \
  --prefix=../install
