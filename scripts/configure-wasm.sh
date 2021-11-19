#!/bin/sh

# reference: https://itnext.io/build-ffmpeg-webassembly-version-ffmpeg-js-part-2-compile-with-emscripten-4c581e8c9a16



CFLAGS="-s USE_PTHREADS"
LDFLAGS="$CFLAGS -s INITIAL_MEMORY=33554432"
# PKG_CONFIG_PATH as an environment needs to be set this way. Probably because of emconfigure.
PKG_CONFIG_PATH="/Users/hanseuljun/repos/telegie/deps/ffmpeg-binaries/opus-binaries/e4d4b74/wasm32-emscripten/lib/pkgconfig"

# Using --disable-everything to reduce the byte size of the resulting library.
emconfigure ../FFmpeg/configure \
  --target-os=none \
  --arch=x86_32 \
  --enable-cross-compile \
  --nm="llvm-nm" \
  --ar=emar \
  --ranlib=emranlib \
  --cc=emcc \
  --cxx=em++ \
  --objcc=emcc \
  --dep-cc=emcc \
  --disable-x86asm \
  --disable-inline-asm \
  --disable-stripping \
  --disable-programs \
  --disable-doc \
  --enable-libopus \
  --disable-everything \
  --enable-decoder=vp8,libopus \
  --enable-parser=vp8,opus \
  --extra-cflags="$CFLAGS" \
  --extra-cxxflags="$CFLAGS" \
  --extra-ldflags="$LDFLAGS" \
  --env="PKG_CONFIG_PATH=$PKG_CONFIG_PATH" \
  --prefix=../install
