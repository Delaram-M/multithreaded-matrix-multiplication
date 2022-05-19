# to execute the program using MPI, enter the following command in terminal in file's path:
# mpiexec -n 5 python mpi_multiplication.py

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    matrix1 = [[1, 2],
               [3, 4]]
    matrix2 = [[1, 3],
               [2, 4]]

    # extract rows and columns
    row1 = matrix1[0]
    row2 = matrix1[1]
    column1 = [matrix2[i][0] for i in range(2)]
    column2 = [matrix2[i][1] for i in range(2)]

    # send rows and columns to other threads using message passing
    comm.send(row1, dest=1)
    comm.send(column1, dest=1)
    comm.send(row1, dest=2)
    comm.send(column2, dest=2)
    comm.send(row2, dest=3)
    comm.send(column1, dest=3)
    comm.send(row2, dest=4)
    comm.send(column2, dest=4)

    # receive each element from other threads
    element11 = comm.recv(source=1)
    element12 = comm.recv(source=2)
    element21 = comm.recv(source=3)
    element22 = comm.recv(source=4)

    # print the result
    multiplied = [[element11, element12],
                  [element21, element22]]
    print(multiplied)

if rank != 0:
    # receive assigned row and column and return the sum of multiplication to rank 0 using message passing
    row = comm.recv(source=0)
    column = comm.recv(source=0)
    element = sum([row[i] * column[i] for i in range(2)])
    comm.send(element, dest=0)

