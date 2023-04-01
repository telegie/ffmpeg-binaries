set -e

echo "start ffmpeg mingw_build"

pushd $2
"$1/FFmpeg/configure" \
    "--target-os=win64" \
    "--arch=x86_64" \
    "--enable-cross-compile" \
	"--prefix=$1/output/x64-windows"

echo "mingw_build - 1"

make -j8
make install
pushd $2

echo "end ffmpeg mingw_build"
