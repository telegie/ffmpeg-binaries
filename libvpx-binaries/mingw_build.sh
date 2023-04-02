set -e

pushd $2
# run configure to create Makefile
"$1/libvpx/configure" --target=x86_64-win64-vs17 "--prefix=$1/output/x64-windows"
# run make to create VS .sln file and .vcxproj files.
make -j8
popd