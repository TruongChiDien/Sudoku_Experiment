from utils import number_of_conflicts

"""
Chọn cell có miền giá trị nhỏ nhất (MRV) heuristic
"""
def select_unassigned_variable(assignment, sudoku):

    unassigned = []

    # Chọn ra tập các cell chưa được gán giá trị
    for cell in sudoku.cells:

        if cell not in assignment:

            unassigned.append(cell)

    # Hàm lấy ra độ lớn của miền giá trị
    criterion = lambda cell: len(sudoku.possibilities[cell])

    # Trả về cell có miền giá trị nhỏ nhất
    return min(unassigned, key=criterion)

"""
Hàm sắp xếp các giá trị theo thứ tự ít ảnh hưởng ràng buộc nhất (LCV) heuristic
"""
def order_domain_values(sudoku, cell):

    # Nếu miền giá trị chỉ có 1 giá trị thì lấy luôn
    if len(sudoku.possibilities[cell]) == 1:
        return sudoku.possibilities[cell]

    criterion = lambda value: number_of_conflicts(sudoku, cell, value)
    return sorted(sudoku.possibilities[cell], key=criterion)