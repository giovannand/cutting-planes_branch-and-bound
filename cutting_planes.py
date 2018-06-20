#!/usr/bin/python
# # -*- coding: utf-8 -*-
import numpy as np
from pdb import set_trace
import math

from commons import put_tableux_form, parse_to_fpi, canonical_form
from primal_simplex import solve as solve_primal_simplex
from dual_simplex import dual_simplex as solve_dual_simplex
from auxiliary_lp import solve as solve_auxiliary_lp
from commons import get_solution, canonical_form
from printing_solutions import optimal_situation, unlimited_certificate, print_float_matrix, non_viability_certificate


def verify_method(matrix):
    begin_c_columns = 0
    end_c_columns = matrix.shape[1]-2

    # Positive vectors C and B - (0) Simplex Primal
    # Vector C Negative and B Non-positive - (1) Simplex Dual
    # Vectors C Non-negative and B Non-positive - (2) PL Auxiliar

    if (all(i >= 0 for i in matrix[0, begin_c_columns:end_c_columns])) and (all(i >=0 for i in matrix[1:, -1])):
        return 0
    elif (all(i <= 0 for i in matrix[0, begin_c_columns:end_c_columns])) \
            and (not (all(i >= 0 for i in matrix[1:, -1]))):
        return 1
    elif (not all(i <= 0 for i in matrix[0, begin_c_columns:end_c_columns])) \
            and (not (all(i >= 0 for i in matrix[1:, -1]))):
        return 2


def simplex(matrix):
    method = verify_method(matrix)

    if method == 0:
        return solve_primal_simplex(matrix)
    elif method == 1:
        return solve_dual_simplex(matrix)
    else:
        return solve_auxiliary_lp(matrix)


def adds_new_restriction(matrix, base_columns, solution):
    new_column = np.zeros(matrix.shape[0]+1)
    new_line = np.zeros(matrix.shape[1])
    #set_trace()
    new_column[-1] = 1
    new_line = matrix[1, :]
    for index in range(0, len(new_line)):
        number = np.array(new_line[index], dtype=float)
        if number.tolist().is_integer() == False:
            new_line[index] = math.floor(new_line[index])
    matrix = np.insert(matrix, matrix.shape[0], new_line, axis=0)
    matrix = np.insert(matrix, -1, new_column, axis=1)
    print("-----------------------Matrix com nova restrição")
    print_float_matrix(matrix)
    return matrix

def define_solution_set(matrix, base_columns, solution):
    #Sset_trace()
    is_integer_number = True
    if solution == "optimal":
        solution_vector = get_solution(matrix, base_columns)
        for x in range(1, len(solution_vector)):
            number = np.array(solution_vector[x], dtype=float)
            is_integer_number = number.tolist().is_integer() 
            if is_integer_number is False:
                return "rational"
    return "integer"


def solve_cutting_planes(matrix):
    simplex_tuple = simplex(matrix)
    optimal_situation(simplex_tuple[0],simplex_tuple[1])
    solution_set = define_solution_set(simplex_tuple[0], simplex_tuple[1], simplex_tuple[2])
    print_float_matrix(simplex_tuple[0])
    while solution_set == "rational" and simplex_tuple[2] == "optimal":
        #adiciona nova restrição
        new_matrix = adds_new_restriction(simplex_tuple[0], simplex_tuple[1], simplex_tuple[2])
        base_columns = np.insert(simplex_tuple[1], simplex_tuple[1].shape[0], 0 )
        #coloca nova matrix em forma canonica
        canonical_form(new_matrix, base_columns)
        #executa simplex dual
        simplex_tuple = solve_dual_simplex(new_matrix, base_columns)
        print("----------------------Nova solução")
        print_float_matrix(simplex_tuple[0])
        set_trace()
        solution_set = define_solution_set(simplex_tuple[0], simplex_tuple[1], simplex_tuple[2])

    if simplex_tuple[2] == "optimal":
        optimal_situation(simplex_tuple[0], simplex_tuple[1])
    elif simplex_tuple[2] == "unlimited":
        unlimited_certificate(simplex_tuple[0], simplex_tuple[1])
    elif simplex_tuple[2] == "non_viability":
        non_viability_certificate(simplex_tuple[0], simplex_tuple[1])


def solve(matrix):
    solve_cutting_planes(matrix)
