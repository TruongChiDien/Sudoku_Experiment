from heuristics import select_unassigned_variable, order_domain_values
from utils import is_consistent, assign, unassign

"""
Thuật toán backtracking

"""
def recursive_backtrack_algorithm(assignment, sudoku):

    # Nếu tất cả các cell đã được gán giá trị thì kết thúc thuật toán
    if len(assignment) == len(sudoku.cells):
        return assignment

    # chọn cell còn ít giá trị nhất (MRV)
    cell = select_unassigned_variable(assignment, sudoku)

    # Chọn giá trị ít ảnh hưởng ràng buộc nhất (LCV)
    for value in order_domain_values(sudoku, cell):

        # Kiếm tra xem giá trị có ảnh hưởng ràng buộc hay không
        if is_consistent(sudoku, assignment, cell, value):

            # Gán giá trị và cắt bỏ miền giá trị của các ô liền kề
            check = assign(sudoku, cell, value, assignment)

            # Nếu sau khi lượt bỏ có cell mất hết giá trị trong miền giá trị
            if not check:
                unassign(sudoku, cell, assignment)
                return False

            result = recursive_backtrack_algorithm(assignment, sudoku)

            if result:
                return result

            # Nếu gán không cho ra kết quả thì trả lại như ban đầu
            unassign(sudoku, cell, assignment)
   
    return False