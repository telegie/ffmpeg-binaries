#!/usr/bin/env bash

PKG_CONFIG_PATH="$(dirname $(pwd))/opus-binaries/e4d4b74/x64-linux/lib/pkgconfig"

../FFmpeg/configure \
  --target-os=linux \
  --arch=x86_64 \
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
  --extra-cflags="-I$(dirname $(pwd))/libvpx-binaries/1.10.0/x64-linux/include" \
  --extra-ldflags="-L$(dirname $(pwd))/libvpx-binaries/1.10.0/x64-linux/lib" \
  --env="PKG_CONFIG_PATH=$PKG_CONFIG_PATH" \
  --prefix=../4.4.1/x64-linux
