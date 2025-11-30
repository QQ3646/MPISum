#!/usr/bin/env bash

if type module > /dev/null 2>&1; then
    module load mpi 2>/dev/null || true
fi

# 2. Проверка наличия mpiexec перед запуском
if ! command -v mpiexec > /dev/null 2>&1; then
    echo "Ошибка: mpiexec не найден. Установите MPI (OpenMPI) или загрузите модуль."
    exit 1
fi
mpiexec -n $1 python main.py