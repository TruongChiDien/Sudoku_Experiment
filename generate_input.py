import itertools
import math
from heuristics import select_unassigned_variable, order_domain_values
from utils import assign, is_consistent, unassign
import random


def Gen_Input_Random(n, sample, rate):
    assignments = []
    for i in range(sample):
        assignment =[]
        for _ in range(n*n):
            if random.random() <= rate:
                assignment.append(random.randint(1, n))
            else:
                assignment.append(0)
        assignments.append(assignment)

    return [' '.join(map(str, x)) for x in assignments]




'''
Tương tự như hàm backtracking nhưng có thêm tỉ lệ giữa việc gán giá trị và gán = 0
'''
def recursive_backtrack_algorithm(assignment, sudoku, rate):

    for cell in sudoku.cells:
        if random.random() > rate:
            assignment[cell] = 0

        else:
            assigned = False
            for value in order_domain_values(sudoku, cell):
                if is_consistent(sudoku, assignment, cell, value):
                    if not assign(sudoku, cell, value, assignment):
                        unassign(sudoku, cell, assignment)
                        assigned = False
                    else:
                        assigned = True
                        break
                    
            if assigned == False:
                assignment[cell] = 0
                

    # if len(assignment) == len(sudoku.cells):
    #     return assignment

    # cell = select_unassigned_variable(assignment, sudoku)

    # if random.random() <= rate:
    #     for value in sudoku.possibilities[cell]:

    #         if is_consistent(sudoku, assignment, cell, value):

    #             assignment[cell] = value

    #             result = recursive_backtrack_algorithm(assignment, sudoku, rate)

    #             if result:
    #                 return result

    #             del assignment[cell]
    #     return False

    # else:
    #     assignment[cell] = 0

    #     result = recursive_backtrack_algorithm(assignment, sudoku, rate)

    #     if result:
    #         return result
   
    # return False


'''
Lớp sinh input, có thể sinh ra input không có lời giải
Tương tự như lớp Sudoku
'''
class Sudoku_Gen_Input:
    def  __init__(self, order=9, sample=5, rate=0.2) -> None:

        self.grid = ['']*sample

        # sudoku n*n
        self.n = order 

        self.rate = rate

        # Sinh ra số lượng Sudoku theo yêu cầu
        for i in range (sample):
            # Sinh tập các tọa độ [(1, 1), (1, 2, ..., (n, n))]
            self.cells = list()
            self.cells = self.generate_coords()

            # Sinh miền giá trị cho mỗi cell
            self.possibilities = dict()
            self.possibilities = self.generate_possibilities()
    
            # Sinh tập ràng buộc dòng, cột, ô vuông 
            rule_constraints = self.generate_rules_constraints()

            # Chuyển tập ràng buộc thành tập ràng buộc 2 ngôi
            self.binary_constraints = list()
            self.binary_constraints = self.generate_binary_constraints(rule_constraints)

            # Sinh dict bao gồm tập các cell có ràng buộc đối với mỗi cell
            self.related_cells = dict()
            self.related_cells = self.generate_related_cells()

            # Dict các gias trị cắt bỏ liên quan đến mỗi cell
            self.pruned = dict()
            self.pruned = {v: list() for v in self.cells}

            # Khởi tạo dict lưu giá trị được gán cho mỗi cell
            assignment = {}

            # Sinh Sudoku bằng backtracking
            recursive_backtrack_algorithm(assignment, self, rate)

            temp = []
            for cell in sorted(assignment):
                temp.append(str(assignment[cell]))
            self.grid[i] = ' '.join(temp)


    def generate_coords(self):

        all_cells_coords = []

        for col in range(1, self.n+1):

            for row in range(1, self.n+1):
                
                new_coords = (col, row)
                all_cells_coords.append(new_coords)

        return all_cells_coords

    def generate_possibilities(self):

        possibilities = dict()

        for cell in self.cells:
            possibilities[cell] = list(range(1, self.n+1))
            # random.shuffle(possibilities[cell])

        return possibilities

    def generate_rules_constraints(self):
        
        row_constraints = []
        column_constraints = []
        square_constraints = []

        rows = cols = list(range(1, self.n+1)) 

        for row in rows:
            row_constraints.append([(col, row) for col in cols]) 

        for col in cols:
            column_constraints.append([(col, row) for row in rows])


        edge_square  = int(math.sqrt(self.n)) 

        rows_square_coords = (cols[i:i+edge_square] for i in range(0, len(rows), edge_square))
        rows_square_coords = list(rows_square_coords)

        cols_square_coords = (rows[i:i+edge_square] for i in range(0, len(cols), edge_square))
        cols_square_coords = list(cols_square_coords)

        for row in rows_square_coords:
            for col in cols_square_coords:

                current_square_constraints = []
                
                for x in row:
                    for y in col:
                        current_square_constraints.append((x, y))

                square_constraints.append(current_square_constraints)

        return row_constraints + column_constraints + square_constraints # [[r1], [r2], ..., [square(sqrt(n))]]

    def generate_binary_constraints(self, rule_constraints):
        generated_binary_constraints = list()

        for constraint_set in rule_constraints:

            binary_constraints = list()

            for tuple_of_constraint in itertools.permutations(constraint_set, 2):
                binary_constraints.append(tuple_of_constraint)

            for constraint in binary_constraints:

                constraint_as_list = list(constraint)
                if(constraint_as_list not in generated_binary_constraints):
                    generated_binary_constraints.append(constraint_as_list)

        return generated_binary_constraints

    def generate_related_cells(self):
        related_cells = dict()

        for cell in self.cells:

            related_cells[cell] = list()

            for constraint in self.binary_constraints:
                if cell == constraint[0]:
                    related_cells[cell].append(constraint[1])

        return related_cells


