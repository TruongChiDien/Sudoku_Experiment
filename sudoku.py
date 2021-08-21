import itertools
import math

class Sudoku:
    def  __init__(self, grid, order=9) -> None:
        game = list(map(int, grid.split()))
        # Sudoku n*n
        self.n = order 

        # Sinh tọa độ cho Sudoku [(1, 1), (1, 2), ..., (n, n)]
        self.cells = list()
        self.cells = self.generate_coords()

        # Sinh miền giá trị cho mỗi cell
        self.possibilities = dict()
        self.possibilities = self.generate_possibilities(game)
   
        # Sinh tập ràng buộc dòng, cột, ô vuông
        rule_constraints = self.generate_rules_constraints()

        # Chuyển tập ràng buộc thành tập ràng buộc 2 ngôi (dùng cho AC-3 sau này)
        self.binary_constraints = list()
        self.binary_constraints = self.generate_binary_constraints(rule_constraints)

        # Sinh dict tập các cell liên quan cho mỗi cell
        self.related_cells = dict()
        self.related_cells = self.generate_related_cells()

        # Dict các gias trị cắt bỏ liên quan đến mỗi cell
        self.pruned = dict()
        self.pruned = {v: list() if game[i] == 0 else [(v, game[i])] for i, v in enumerate(self.cells)}


    """
    Hàm sinh tọa độ cho các cell (cột, dòng)
    """
    def generate_coords(self):

        all_cells_coords = []

        for col in range(1, self.n+1):

            for row in range(1, self.n+1):
                
                # (1,1), (1,2), (1,2), ...,  (n,n)
                new_coords = (col, row)
                all_cells_coords.append(new_coords)

        return all_cells_coords

    """
    Hàm sinh miền giá trị cho mỗi cell
    """
    def generate_possibilities(self, grid_as_list):

        possibilities = dict()

        for index, coords in enumerate(self.cells):
            # Nếu cell chưa được điền thì miền giá trị nó trong đoạn [1, n]
            if grid_as_list[index] == 0:
                possibilities[coords] = list(range(1, self.n+1))

            # Nếu cell đã được gán thì miền giá trị của nó chỉ có 1 giá trị
            else:
                possibilities[coords] = [grid_as_list[index]]

        return possibilities

    """
    Hàm sinh tập các ràng buộc dòng ,cột, ô vuông
    """
    def generate_rules_constraints(self):
        
        row_constraints = []
        column_constraints = []
        square_constraints = []

        rows = cols = list(range(1, self.n+1)) #[1, 2, 3, ..., n]

        # Ràng buộc dòng
        for row in rows:
            row_constraints.append([(col, row) for col in cols]) # [[(1, 2), (1, 3), ..., (n, n)]]

        # Ràng buộc cột
        for col in cols:
            column_constraints.append([(col, row) for row in rows])

        # Chia chiều dài và chiều rộng thành các đoạn có độ dài bằng cạnh của ô vuông
        edge_square  = int(math.sqrt(self.n)) 

        rows_square_coords = (cols[i:i+edge_square] for i in range(0, len(rows), edge_square))
        rows_square_coords = list(rows_square_coords)

        cols_square_coords = (rows[i:i+edge_square] for i in range(0, len(cols), edge_square))
        cols_square_coords = list(cols_square_coords)

        # Ràng buộc ô vuông
        for row in rows_square_coords:
            for col in cols_square_coords:

                current_square_constraints = []
                
                for x in row:
                    for y in col:
                        current_square_constraints.append((x, y))

                square_constraints.append(current_square_constraints)

        return row_constraints + column_constraints + square_constraints # [[r1], [r2], ..., [square(sqrt(n))]]

    """
    Sinh tập ràng buộc 2 ngôi từ tập ràng buộc
    """
    def generate_binary_constraints(self, rule_constraints):
        generated_binary_constraints = list()

        # Duyệt qua từng tập ràng buộc [ràng buộc dòng 1], [ràng buộc dòng 2], ...
        for constraint_set in rule_constraints:

            binary_constraints = list()

            # Lấy tất cả trong tập hoán vị các ràng buộc (Hoán vị để dùng cho AC-3)
            for tuple_of_constraint in itertools.permutations(constraint_set, 2):
                binary_constraints.append(tuple_of_constraint)

            for constraint in binary_constraints:

                # Kiểm tra ràng buộc có tồn tại chưa
                constraint_as_list = list(constraint)
                if(constraint_as_list not in generated_binary_constraints):
                    generated_binary_constraints.append(constraint_as_list)

        return generated_binary_constraints

    """
    Sinh dict tập các cell liên quan cho mỗi cell
    """
    def generate_related_cells(self):
        related_cells = dict()

        # Duyệt qua n*n cell
        for cell in self.cells:

            related_cells[cell] = list()

            for constraint in self.binary_constraints:
                if cell == constraint[0]:
                    related_cells[cell].append(constraint[1])

        return related_cells

    """
    Hàm kiểm tra Sudoku đã được giải chưa
    Nếu tất cả các cell chỉ có 1 giá trị duy nhất thì Sudoku đã được giải
    """
    def isFinished(self):
        for coords, possibilities in self.possibilities.items():
            if len(possibilities) > 1:
                return False
        
        return True
    
    """
    Hàm trả về định dạng bảng Sudoku
    """
    def __str__(self):

        output = ""
        count = 1
        
        for cell in self.cells:

            # Nếu như Sudoku xong ngay sau khi AC-3 được chạy
            value = self.possibilities[cell]
            if type(self.possibilities[cell]) == list:
                value = str(self.possibilities[cell][0])

            if self.n < 10:
                output += "[{}]".format(value)
            elif self.n <100:
                output += "[{0:02d}]".format(value)

            if count >= self.n:
                count = 0
                output += "\n"
            
            count += 1
        
        return output
