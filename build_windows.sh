#!/bin/bash

here="$(pwd)/.."
echo "here: ${here}"

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:${here}/opus-binaries/output/x64-windows/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:${here}/opus-binaries/output/x64-windows/lib/pkgconfig"

echo "PKG_CONFIG_PATH: ${PKG_CONFIG_PATH}"
echo ""

msys_libvpx_include="${here}/libvpx-binaries/output/x64-windows/include"
msys_libvpx_lib="${here}/libvpx-binaries/output/x64-windows/lib/x64"
msys_opus_include="${here}/opus-binaries/output/x64-windows/include"
msys_opus_lib="${here}/opus-binaries/output/x64-windows/lib"

windows_libvpx_include=$(cygpath -m $msys_libvpx_include)
windows_libvpx_lib=$(cygpath -m $msys_libvpx_lib)
windows_opus_include=$(cygpath -m $msys_opus_include)
windows_opus_lib=$(cygpath -m $msys_opus_lib)

export INCLUDE="$INCLUDE;${windows_libvpx_include}"
export LIB="$LIB;${windows_libvpx_lib}"
export INCLUDE="$INCLUDE;${windows_opus_include}"
export LIB="$LIB;${windows_opus_lib}"

echo "INCLUDE: ${INCLUDE}"
echo ""
echo "LIB: ${LIB}"
echo ""

../FFmpeg/configure \
  --target-os=win64 \
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
  --enable-encoder=libvpx_vp8,libopus \
  --enable-decoder=vp8,libopus \
  --disable-encoder=opus,libvpx_vp9 \
  --disable-decoder=vp9,libvpx_vp8,libvpx_vp9,opus \
  --prefix=../output/x64-windows

make -j8
make install
