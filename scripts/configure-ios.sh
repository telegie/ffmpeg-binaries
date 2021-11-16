#!/bin/bash

# need to install https://github.com/libav/gas-preprocessor

# from https://github.com/kewlbear/FFmpeg-iOS-build-script

if [ ! `which gas-preprocessor.pl` ]
then
    echo 'gas-preprocessor.pl not found. Trying to install...'
    (curl -L https://github.com/libav/gas-preprocessor/raw/master/gas-preprocessor.pl \
        -o /usr/local/bin/gas-preprocessor.pl \
        && chmod +x /usr/local/bin/gas-preprocessor.pl) \
        || exit 1
fi

CC='xcrun --sdk iphoneos clang'

../FFmpeg/configure \
  --target-os=darwin \
  --arch=arm64 \
  --enable-cross-compile \
  --cc="$CC" \
  --as="gas-preprocessor.pl -arch aarch64 -- $CC" \
  --sysroot=$(xcrun --sdk iphoneos --show-sdk-path) \
  --disable-debug \
  --disable-programs \
  --disable-doc \
  --enable-pic \
  --disable-videotoolbox \
  --disable-audiotoolbox \
  --disable-iconv \
  --enable-libvpx \
  --enable-encoder=libvpx_vp8 \
  --extra-cflags='-mios-version-min=14.0 -I/Users/hanseuljun/repos/telegie/deps/libvpx-binaries/1.10.0/arm64-darwin-gcc/include' \
  --extra-ldflags='-L/Users/hanseuljun/repos/telegie/deps/libvpx-binaries/1.10.0/arm64-darwin-gcc/lib' \
  --prefix=../install
