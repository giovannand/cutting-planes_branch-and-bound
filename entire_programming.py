#!/usr/bin/python
# # -*- coding: utf-8 -*-
import os, sys
import numpy as np
from pdb import set_trace
from cutting_planes import solve as solve_cutting_planes

def main():
    f = open(sys.argv[1], 'r')
    method = int(f.readline())
    lines = int(f.readline()) + 1
    columns = int(f.readline()) + 1

    matrix_str = f.readline()
    matrix = np.array(np.mat(matrix_str).reshape(lines, columns), dtype=float)
    matrix = matrix.astype('object')
    #set_trace()
    if method == 0:
        solve_cutting_planes(matrix)
    elif method == 1:
        pass
        #solve_branch_and_bound(matrix)
    f.close()


main()
