#!/usr/bin/env bash

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:$(dirname $(pwd))/opus-binaries/e4d4b74/x64-linux/lib/pkgconfig"

echo "PKG_CONFIG_PATH: ${PKG_CONFIG_PATH}"

pkg-config --exists opus
echo $?

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
  --pkg-config-flags="--static" \ #reference: https://stackoverflow.com/questions/28884676/error-installing-ffmpeg-on-ubuntu-opus-not-found-using-pkg-config
  --prefix=../4.4.1/x64-linux
