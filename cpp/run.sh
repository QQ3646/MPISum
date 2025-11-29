#!/usr/bin/env bash

EXECUTABLE_NAME="mpiSum"
DEFAULT_PROCS=4

BUILD_TYPE="Debug"
NUM_PROCS=$DEFAULT_PROCS

for arg in "$@"
do
    if [ "$arg" == "--release" ]; then
        BUILD_TYPE="Release"
    elif [[ "$arg" =~ ^[0-9]+$ ]]; then
        NUM_PROCS="$arg"
    fi
done

if [ "$BUILD_TYPE" == "Release" ]; then
    BUILD_DIR="cmake-build-release"
else
    BUILD_DIR="cmake-build-debug"
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR" || exit

cmake -DCMAKE_BUILD_TYPE=$BUILD_TYPE ..
cmake --build . --parallel

if [ $? -eq 0 ]; then
    if [ -f "./$EXECUTABLE_NAME" ]; then
        mpirun -np "$NUM_PROCS" "./$EXECUTABLE_NAME"
    else
        exit 1
    fi
else
    exit 1
fi
