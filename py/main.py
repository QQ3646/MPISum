# Распределенное суммирование массива с использованием MPI

from mpi4py import MPI
from numpy import arange, empty, int32, float64, sum
from time import time

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    numprocs = comm.Get_size()

    # Синхронизация перед началом замера
    comm.Barrier()
    start_time = time()

    # Параметры массива
    if rank == 0:
        M = 100_000_000
        a = arange(1, M + 1, dtype=float64)
    else:
        a = None

    # Вычисляем данные для каждого процесса
    if rank == 0:
        ave, res = divmod(M, numprocs)
        rcounts = empty(numprocs, dtype=int32)
        displs = empty(numprocs, dtype=int32)

        displs[0] = 0
        for k in range(numprocs):
            if k < res:
                rcounts[k] = ave + 1
            else:
                rcounts[k] = ave
            if k > 0:
                displs[k] = displs[k - 1] + rcounts[k - 1]
        print(f"\nРаспределение элементов: {rcounts}\n")
        print("-" * 60)
    else:
        rcounts = None
        displs = None

    # Рассылаем каждому процессу его размер локальной части
    local_count = empty(1, dtype=int32)
    comm.Scatter(rcounts, local_count, root=0)
    M_part = local_count[0]

    local_a = empty(M_part, dtype=float64)
    comm.Scatterv([a, rcounts, displs, MPI.DOUBLE], local_a, root=0)

    local_sum = sum(local_a)
    print(f"Процесс {rank}: получен массив {local_a}, промежуточная сумма = {local_sum}")

    step = 1
    while step < numprocs:
        if (rank // step) % 2 == 0:
            # Процесс-получатель
            partner_rank = rank + step
            if partner_rank < numprocs:
                remote_sum = empty(1, dtype=float64)
                comm.Recv(remote_sum, source=partner_rank)
                local_sum += remote_sum[0]
                print(f"Процесс {rank} получил {remote_sum[0]} от процесса {partner_rank}, обновленная сумма = {local_sum}")
        else:
            # Процесс-отправитель
            partner_rank = rank - step
            comm.Send(local_sum, dest=partner_rank)
            break
        step *= 2

    if rank == 0:
        print("\n" + "-" * 60)
        print(f"\nФинальная сумма массива: {local_sum}")

    # Замер времени окончания
    comm.Barrier()
    end_time = time()
    total_time = end_time - start_time

    # Сбор времени выполнения на процессе 0
    times = comm.gather(total_time, root=0)

    if rank == 0:
        print("\n" + "-" * 60)
        print(f"\nВремя выполнения: {max(times):.6f} секунд")


if __name__ == "__main__":
    main()