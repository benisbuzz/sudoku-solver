from copy import deepcopy


def display_grid(matrix):
    output = ""
    for i, row in enumerate(matrix):
        if i % 3 == 0 and i != 0:
            output += "-" * 21 + "\n"
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                output += "| "
            output += (str(val) if isinstance(val, int) else ".") + " "
        output += "\n"
    return output


### Step 1


def transform_sudoku_string(sudoku_string: str):
    long_list = [int(digit) for digit in sudoku_string]
    sudoku = [long_list[i : i + 9] for i in range(0, len(long_list), 9)]
    for row in sudoku:
        for i in range(len(row)):
            if row[i] == 0:
                row[i] = list(range(1, 10))
    return sudoku


### Step 2
def get_boxes(matrix: list[list]) -> list[list[list]]:
    boxes = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = [matrix[x][j : j + 3] for x in range(i, i + 3)]
            boxes.append(box)
    return boxes


def undo_boxes(boxes: list[list[list]]) -> list[list]:
    grid = [[0] * 9 for _ in range(9)]
    for index, box in enumerate(boxes):
        start_row = (index // 3) * 3
        start_col = (index % 3) * 3
        for i in range(3):
            for j in range(3):
                grid[start_row + i][start_col + j] = box[i][j]
    return grid


def pop_sector(matrix: list[list]) -> list[list]:
    boxes = get_boxes(matrix)
    for sector in boxes:
        sector_values = [i for sublist in sector for i in sublist if type(i) == int]
        for row in sector:
            for i in range(len(row)):
                if type(row[i]) == list:
                    row[i] = list(set(row[i]).symmetric_difference(sector_values))
    return undo_boxes(boxes)


### Step 3
def transpose(matrix: list[list]) -> list[list]:
    return [list(col) for col in zip(*matrix)]


def pop_rows_cols(matrix: list[list]) -> list[list]:
    matrix_copy = deepcopy(matrix)
    for row_num in range(9):
        for col_num in range(9):
            if type(matrix[row_num][col_num]) == int:
                continue
            row_values = [i for i in matrix_copy[row_num] if type(i) == int]
            col_values = [i for i in transpose(matrix_copy)[col_num] if type(i) == int]
            impossible_nums = list(set(col_values + row_values))
            matrix_copy[row_num][col_num] = [
                ele
                for ele in matrix_copy[row_num][col_num]
                if ele not in impossible_nums
            ]
    return matrix_copy


### Step 4
def extract_single_lists(matrix: list[list]) -> list[list]:
    matrix_copy = deepcopy(matrix)
    for row in matrix_copy:
        for i in range(len(row)):
            if type(row[i]) == list and len(row[i]) == 1:
                row[i] = row[i][0]
    return matrix_copy


### Step 5
def fill_unique_sector_notes(matrix: list[list]) -> list[list]:
    def get_values_to_fill(sector):
        result = []
        for sublist in sector:
            for item in sublist:
                if isinstance(item, list):
                    result.extend(item)
        return [i for i in result if result.count(i) == 1]

    boxes = get_boxes(matrix)
    for sector in boxes:
        values_to_fill = get_values_to_fill(sector)
        for value in values_to_fill:
            for row in sector:
                for i in range(len(row)):
                    if type(row[i]) == list and value in row[i]:
                        row[i] = value
    return undo_boxes(boxes)


def fill_unique_line_notes(matrix: list[list], transpose_it: bool) -> list[list]:
    matrix_copy = deepcopy(matrix)
    if transpose_it:
        matrix_copy = transpose(matrix_copy)
    for line in matrix_copy:
        notes = []
        for item in line:
            if isinstance(item, list):
                notes.extend(item)
        values_to_fill = [note for note in notes if notes.count(note) == 1]
        for value in values_to_fill:
            for i in range(len(line)):
                if type(line[i]) == list and value in line[i]:
                    line[i] = value
    if transpose_it:
        return transpose(matrix_copy)
    return matrix_copy


### Step 6
def solve_sudoku(sudoku_string: str):
    counter = 1
    sudoku = transform_sudoku_string(sudoku_string)
    print("Unsolved Sudoku:\n")
    print(display_grid(sudoku))
    while counter < 100:
        sudoku = fill_unique_line_notes(
            fill_unique_line_notes(
                fill_unique_sector_notes(
                    extract_single_lists(pop_rows_cols(pop_sector(sudoku)))
                ),
                False,
            ),
            True,
        )
        all_solved = True
        for row in sudoku:
            for cell in row:
                if not isinstance(cell, int):
                    all_solved = False
                    break
            if not all_solved:
                break
        if all_solved:
            print(f"Solved in {counter} iterations \n")
            print(display_grid(sudoku))
            return sudoku
        counter += 1
    return sudoku
