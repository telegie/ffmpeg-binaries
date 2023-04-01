set -e

echo "start ffmpeg mingw_build"

echo $1
echo $PATH

libvpx_pkgconfig="$1/libvpx-binaries/output/x64-windows/lib/pkgconfig"
opus_pkgconfig="$1/opus-binaries/output/x64-windows/lib/pkgconfig"
export PKG_CONFIG_PATH="$libvpx_pkgconfig:$opus_pkgconfig"
# export PKG_CONFIG_PATH="$opus_pkgconfig"

echo "PKG_CONFIG_PATH: $PKG_CONFIG_PATH"

pkg_result=$(pkg-config --exists --print-errors opus)
# pkg_result=$(pwd)

echo "pkg_result: ${pkg_result}"

echo "mingw_build - 1"

pushd $2
"$1/FFmpeg/configure" \
    "--target-os=win64" \
    "--arch=x86_64" \
    "--toolchain=msvc" \
    "--enable-cross-compile" \
    "--enable-shared" \
    "--disable-debug" \
    "--disable-programs" \
    "--disable-doc" \
    "--disable-bzlib" \
    "--disable-iconv" \
    "--disable-lzma" \
    "--enable-libvpx" \
    "--enable-libopus" \
    "--enable-encoder=libvpx_vp8,libvpx_vp9,libopus" \
    "--enable-decoder=vp8,vp9,libopus" \
    "--disable-encoder=opus" \
    "--disable-decoder=libvpx_vp8,libvpx_vp9,opus" \
    "--env=PKG_CONFIG_PATH=$opus_pkgconfig" \
	"--prefix=$1/output/x64-windows"

echo "mingw_build - 2"

make -j8
make install
popd

echo "end ffmpeg mingw_build"
