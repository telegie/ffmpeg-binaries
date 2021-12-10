#!/usr/bin/env bash

PKG_CONFIG_PATH="/Users/hanseuljun/repos/telegie/deps/ffmpeg-binaries/opus-binaries/e4d4b74/arm64-mac/lib/pkgconfig"

../FFmpeg/configure \
  --target-os=darwin \
  --arch=arm64 \
  --disable-debug \
  --disable-programs \
  --disable-doc \
  --disable-videotoolbox \
  --enable-libvpx \
  --enable-libopus \
  --enable-encoder=libvpx_vp8,libvpx_vp9,libopus \
  --enable-decoder=vp8,vp9,libopus \
  --disable-encoder=opus \
  --disable-decoder=libvpx_vp8,libvpx_vp9,opus \
  --extra-cflags='-I/Users/hanseuljun/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/arm64-mac/include' \
  --extra-ldflags='-L/Users/hanseuljun/repos/telegie/deps/ffmpeg-binaries/libvpx-binaries/1.10.0/arm64-mac/lib' \
  --env="PKG_CONFIG_PATH=$PKG_CONFIG_PATH" \
  --prefix=../4.4.1/arm64-mac
