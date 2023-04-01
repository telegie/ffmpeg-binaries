#!/bin/bash

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/c/Users/hanseul/repos/librgbd/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/x64-windows/lib/pkgconfig:/c/Users/hanseul/repos/librgbd/deps/ffmpeg-binaries/opus-binaries/e4d4b74/x64-windows/lib/pkgconfig"

../FFmpeg/configure \
  --target-os=mingw64 \
  --arch=x86_64 \
  --toolchain=msvc \
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
  --prefix=../output/x64-windows
