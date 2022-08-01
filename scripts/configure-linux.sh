#!/usr/bin/env bash

export PKG_CONFIG_PATH="$(dirname $(pwd))/libvpx-binaries/1.10.0/x64-linux/lib/pkgconfig:$(dirname $(pwd))/opus-binaries/e4d4b74/x64-linux/lib/pkgconfig"

#reference: https://stackoverflow.com/questions/28884676/error-installing-ffmpeg-on-ubuntu-opus-not-found-using-pkg-config
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
  --extra-cflags="-fPIC" \
  --pkg-config-flags="--static" \
  --prefix="$(dirname $(pwd))/4.4.1/x64-linux"
