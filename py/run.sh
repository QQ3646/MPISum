#!/bin/bash

module load mpi
mpiexec -n $1 python main.py