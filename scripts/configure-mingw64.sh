#!/bin/bash

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/opus-binaries/e4d4b74/x86_64-w64-mingw32/lib/pkgconfig"

# libssp is required due to opus using fortified functions, which are not included in mingw by default.
# libssp provides the fortified functions.

../FFmpeg/configure \
  --target-os=mingw64 \
  --arch=x86_64 \
  --enable-cross-compile \
  --enable-shared \
  --disable-debug \
  --disable-programs \
  --disable-doc \
  --disable-bzlib \
  --disable-iconv \
  --disable-lzma \
  --disable-zlib \
  --disable-encoders \
  --disable-decoders \
  --enable-libvpx \
  --enable-libopus \
  --enable-encoder=libvpx_vp8,libvpx_vp9,libopus \
  --enable-decoder=vp8,vp9,libopus \
  --extra-cflags='-I /c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/x86_64-win64-gcc/include' \
  --extra-ldflags='-L /c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/x86_64-win64-gcc/lib -lssp' \
  --prefix=../install
