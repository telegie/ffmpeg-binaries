#!/bin/bash

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/opus-binaries/e4d4b74/x86_64-w64-mingw32/lib/pkgconfig"

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
  --enable-libvpx \
  --enable-libopus \
  --enable-encoder=libvpx_vp8,libvpx_vp9,libopus \
  --enable-decoder=vp8,vp9,libopus \
  --disable-encoder=opus \
  --disable-decoder=libvpx_vp8,libvpx_vp9,opus \
  --extra-cflags='-I /c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/x64-windows/include' \
  --extra-ldflags='-L /c/Users/hanseul/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/x64-windows/lib' \
  --prefix=../4.4.1/x64-windows
