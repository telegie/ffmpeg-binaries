# libvpx-binaries

## How to Build

- git submodule update --init --recursive
- python3 build.py

## For Windows x64 Build

1. Open mingw64.
2. mkdir build
3. mkdir install
4. cd build
5. ../libvpx/configure --target=x86_64-win64-gcc --prefix=../1.10.0/x64-windows
6. make -j8
7. make install
