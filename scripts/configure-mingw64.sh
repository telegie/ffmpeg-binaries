#!/bin/bash


../FFmpeg/configure \
  --target-os=mingw64 \
  --arch=x86_64 \
  --enable-shared \
  --disable-debug \
  --disable-programs \
  --disable-doc \
  --disable-iconv \
  --enable-libvpx \
  --enable-encoder=libvpx_vp8 \
  --extra-cflags='-I /c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/include' \
  --extra-ldflags='-L /c/Users/hanseul/repos/telegie/deps/libvpx-binaries/1.10.0/x86_64-win64-gcc/lib' \
  --prefix=../install
