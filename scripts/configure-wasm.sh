#!/bin/bash

# from: https://itnext.io/build-ffmpeg-webassembly-version-ffmpeg-js-part-2-compile-with-emscripten-4c581e8c9a16

CFLAGS="-s USE_PTHREADS"
LDFLAGS="$CFLAGS -s INITIAL_MEMORY=33554432"

# Using --disable-everything to reduce the byte size of the resulting library.
emconfigure ../FFmpeg/configure \
  --target-os=none \
  --arch=x86_32 \
  --enable-cross-compile \
  --disable-x86asm \
  --disable-inline-asm \
  --disable-stripping \
  --disable-programs \
  --disable-doc \
  --extra-cflags="$CFLAGS" \
  --extra-cxxflags="$CFLAGS" \
  --extra-ldflags="$LDFLAGS" \
  --nm="llvm-nm" \
  --ar=emar \
  --ranlib=emranlib \
  --cc=emcc \
  --cxx=em++ \
  --objcc=emcc \
  --dep-cc=emcc \
  --disable-everything \
  --enable-decoder=vp8 \
  --enable-parser=vp8 \
  --prefix=../install
