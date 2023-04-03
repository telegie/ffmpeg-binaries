set -e

pushd $2

# --enable-static-msvcrt is required to make the resulting static library (.lib) file useful.
# Without this option, the .lib file becomes a wierd file that expects msvcrt to be provided
# for it as if it is a .dll file while it is a static file.
# In other words, without --enable-static-msvcrt, the build happens with the /MD option while
# it should happen with the /MT option.
# ref: https://openssl-dev.openssl.narkive.com/fZg2LuB1/win32-compile-mode-static-and-dynamic-msvcrt
# ref: https://learn.microsoft.com/en-us/cpp/build/reference/md-mt-ld-use-run-time-library

# run configure to create Makefile
"$1/libvpx/configure" --target=x86_64-win64-vs17 "--prefix=$1/output/x64-windows" --enable-static-msvcrt
# run make to create VS .sln file and .vcxproj files.
make -j8
popd
