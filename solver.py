import argparse
from random import sample
from sudoku import Sudoku
from ac3 import AC3
from backtrack import recursive_backtrack_algorithm
from utils import print_grid
from generate_input import Sudoku_Gen_Input, Gen_Input_Random
import time


"""
Hàm giải Sudoku bằng AC-3 và backtracking
"""


def solve(grid, index, total, n):

    # print("\nSudoku {}/{} : \n{}".format(index, total, print_grid(grid, n)))
    print("\nSudoku {}/{}\nCreating...".format(index, total))
    
    # Tạo một Sudoku
    sudoku = Sudoku(grid, n)

    print("{}/{} : AC3 starting".format(index, total))

    # Chạy AC-3    
    print('\n-----Before AC-3')
    num_arc = len(sudoku.binary_constraints)
    tolal_val = 0
    largest_domain = 0
    for cell in sudoku.possibilities:
        tolal_val += len(sudoku.possibilities[cell])
        largest_domain = max(len(sudoku.possibilities[cell]), largest_domain)
    print(f'Number of arcs: {num_arc}\nTotal values: {tolal_val}\nSize of largest domain: {largest_domain}')

    start = time.time()
    AC3(sudoku)
    print('\n-----AC-3 take {} ms'.format(time.time() - start))
    
    print('\n-----After AC-3')
    tolal_val = 0
    largest_domain = 0
    for cell in sudoku.possibilities:
        tolal_val += len(sudoku.possibilities[cell])
        largest_domain = max(len(sudoku.possibilities[cell]), largest_domain)
    print(f'Total values: {tolal_val}\nSize of largest domain: {largest_domain}')




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Solve a Sudoku with CSP')
    parser.add_argument('--edge', type=int, default=3,
                        help='Edge of a square, if edge = 3 then Sudoku have size 9*9')
    parser.add_argument('--sample', type=int, default=10,
                        help='Number of sample')
    parser.add_argument('--level', type=float, default=0.2,
                        help='ratio of position have value (default: %(default)s)')
    args = parser.parse_args()

    if args.edge > 10:
        print('Edge is too large, must be between 2 and 10')
        exit(0)

    if args.level > 0.4:
        print('Ratio is too large, must be between 0.1 and 0.4')
        exit(0)

    # samples = Sudoku_Gen_Input(args.edge**2, args.sample, args.level)

    # for i in range(args.sample):
    #     solve(samples.grid[i], i+1, args.sample, args.edge**2)

    samples = Gen_Input_Random(args.edge**2, args.sample, args.level)

    for i in range(args.sample):
        solve(samples[i], i+1, args.sample, args.edge**2)

