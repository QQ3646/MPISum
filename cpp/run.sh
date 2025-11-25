#!/usr/bin/env bash

cmake --build .
mpirun -np $1 ./mpiSum