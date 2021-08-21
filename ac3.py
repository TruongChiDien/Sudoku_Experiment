from utils import is_different

"""
Lan truyền ràng buộc với AC-3
Mã giả tại @ https://en.wikipedia.org/wiki/AC-3_algorithm
"""
def AC3(csp, queue=None):

    if queue == None:
        queue = list(csp.binary_constraints)

    solvable = True

    while queue:

        #Lấy ra 1 cung ràng buộc 2 ngôi để kiểm tra miền giá trị
        (xi, xj) = queue.pop(0)

        # Nếu có lượt bỏ trong miền giá trị
        if remove_inconsistent_values(csp, xi, xj): 

            # Nếu cell bị lượt bỏ hết giá trị trong miền giá trị
            if len(csp.possibilities[xi]) == 0:
                solvable = False
            
            # Thêm lại tất cả các ràng buộc có cell_i nằm ở đầu cung ràng buộc
            for Xk in csp.related_cells[xi]:
                if Xk != xi:
                    queue.append((Xk, xi))
                    
    return solvable

"""
Loại bỏ các giá trị không nhất quán tại 1 cell liền kề của cell hiện tại
"""
def remove_inconsistent_values(csp, cell_i, cell_j):

    removed = False

    # Duyệt qua miền giá trị của cell phía đuôi của cung ràng buộc
    for value in csp.possibilities[cell_i]:

        # Nếu không tồn tại giá trị nào trong miền giá trị cell phía đầu cung thỏa ràng buộc
        if not any([is_different(value, poss) for poss in csp.possibilities[cell_j]]):
            
            # Loại giá trị này ra khỏi miền giá trị của cell_i
            csp.possibilities[cell_i].remove(value)
            removed = True

    # Trả về True nếu có remove
    return removed
