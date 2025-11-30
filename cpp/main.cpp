#include <iostream>
#include <vector>
#include <numeric>
#include <mpi.h>

#ifndef NDEBUG
    #define DLOG if(true) std::cout
#else
    #define DLOG if(false) std::cout
#endif

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, numprocs;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);

    const long long M = 10000000;

    std::vector<double> a;
    std::vector<int> rcounts;
    std::vector<int> displs;

    if (rank == 0) {
        a.resize(M);
        std::iota(a.begin(), a.end(), 1.0);

        const int ave = M / numprocs;
        const int res = M % numprocs;

        rcounts.resize(numprocs);
        displs.resize(numprocs);

        displs[0] = 0;
        for (int k = 0; k < numprocs; ++k) {
            if (k < res) {
                rcounts[k] = ave + 1;
            } else {
                rcounts[k] = ave;
            }
            if (k > 0) {
                displs[k] = displs[k - 1] + rcounts[k - 1];
            }
        }

        DLOG << "Распределение рассчитано." << std::endl;
    }

    int local_count = 0;
    MPI_Scatter(rank == 0 ? rcounts.data() : nullptr, 1, MPI_INT,
                &local_count, 1, MPI_INT,
                0, MPI_COMM_WORLD);

    std::vector<double> local_a(local_count);

    MPI_Scatterv(rank == 0 ? a.data() : nullptr,
                 rank == 0 ? rcounts.data() : nullptr,
                 rank == 0 ? displs.data() : nullptr,
                 MPI_DOUBLE,
                 local_a.data(), local_count, MPI_DOUBLE,
                 0, MPI_COMM_WORLD);


    MPI_Barrier(MPI_COMM_WORLD);
    double start_time = MPI_Wtime();

    double local_sum = std::accumulate(local_a.begin(), local_a.end(), 0.0);

    int step = 1;
    while (step < numprocs) {
        if (rank / step % 2 == 0) {
            if (const int partner_rank = rank + step; partner_rank < numprocs) {
                double remote_sum = 0.0;
                MPI_Recv(&remote_sum, 1, MPI_DOUBLE, partner_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

                DLOG << "Процесс " << rank << " получил " << remote_sum
                          << " от процесса " << partner_rank << std::endl;

                local_sum += remote_sum;

                DLOG << "Процесс " << rank << ": обновленная сумма = " << local_sum << std::endl;
            }
        } else {
            const int partner_rank = rank - step;
            MPI_Send(&local_sum, 1, MPI_DOUBLE, partner_rank, 0, MPI_COMM_WORLD);
            break;
        }
        step *= 2;
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double end_time = MPI_Wtime();

    if (rank == 0) {
        std::cout << "Финальная сумма массива: " << local_sum << std::endl;
        std::cout << "Время выполнения: " << (end_time - start_time) << " секунд" << std::endl;
    }

    MPI_Finalize();
    return 0;
}