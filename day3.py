from commonfunctions.fileimport import import_path, test_path

# check if a part symbol is on the left
def check_left(matrix, row, col):
    try:
        check = matrix[row][col-1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check if a part symbol is on the right
def check_right(matrix, row, col):
    try:
        check = matrix[row][col+1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check if a part symbol is one up
def check_up(matrix, row, col):
    try:
        check = matrix[row-1][col]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check if a part symbol is one down
def check_down(matrix, row, col):
    try:
        check = matrix[row+1][col]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False

# check diagonal up+left
def check_upleft(matrix, row, col):
    try:
        check = matrix[row-1][col-1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check diagonal up+right
def check_upright(matrix, row, col):
    try:
        check = matrix[row-1][col+1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check diagonal down+left
def check_downleft(matrix, row, col):
    try:
        check = matrix[row+1][col-1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False
    
# check diagonal down+right
def check_downright(matrix, row, col):
    try:
        check = matrix[row+1][col+1]
    except IndexError: # out of bounds
        return False
    if check not in non_symbols:
        return True
    else:
        return False


path = import_path(3)
# path = test_path(3)

schematic = [] # build out the schematic as a list of lists

non_symbols = ["0","1","2","3","4","5","6","7","8","9","."] # these are the characters that can be ignored when checking

with open(path) as raw_data:
    for line in raw_data:
        line_list = [] # create a list object for each line that stores all the chars in order
        for char in line:
            if char != "\n": # ignore newline chars
                line_list.append(char)
        schematic.append(line_list) # then append this to the schematic

current_num = ""
save_num = False
pt1 = 0

# loop through every element in the schematic, first by row and then by col
for row in range(len(schematic)):
    for col in range(len(schematic[row])):
        # if element is a digit, we want to do the following:
        # 1. continue building the current number (i.e. 1,2,3 needs to become 123)
        # 2. check all 8 directions for parts
        # 3. if any checks pass, mark this as a number to be saved to the answer
        if schematic[row][col].isdigit():
            current_num += str(schematic[row][col])
            # check all 8 directions for parts
            left = check_left(schematic, row, col)
            right = check_right(schematic, row, col)
            up = check_up(schematic, row, col)
            down = check_down(schematic, row, col)
            upleft = check_upleft(schematic, row, col)
            upright = check_upright(schematic, row, col)
            downleft = check_downleft(schematic, row, col)
            downright = check_downright(schematic, row, col)
            # if any digit in the number is adjacent to a part, we want to mark it to be saved
            if left or right or up or down or upleft or upright or downleft or downright:
                save_num = True
        # if we are on a non-digit or at the end of a row, do the following:
        # 1. if the current number is marked to be saved, add to the answer
        # 2. reset the current number and also the saved marker
        if not(schematic[row][col].isdigit()) or col == len(schematic[row])-1:
            if save_num:
                pt1 += int(current_num)
            current_num = ""
            save_num = False

# print(f"pt1: {pt1}")


## TRY: PT 2
# 1. function that fills in a number from finding one digit (by going left and right along the row)
# 2. store the index positions and values of each number in a dict, to prevent double counting of overlapping numbers
# 3. store the index positions of each "*" and compare to the dict in [2]

# looks for the leftmost digit of a number and fills in the rest along the row
# returns the number and index position
def expand_num(matrix, row, col):
    start_col = col
    number = str(matrix[row][col])
    # loop as long as the element is a number, and we aren't at the end of the row
    while matrix[row][col].isdigit() and col < len(matrix[row])-1:
        col += 1
        if matrix[row][col].isdigit():
            number += str(matrix[row][col])
    # return the number and its position as a list
    return [number, (row, start_col)]

num_positions = {}
gear_positions = {}

for row in range(len(schematic)):
    for col in range(len(schematic[row])):
        # find numbers and populate their positions in a dict
        if schematic[row][col].isdigit():
            # look one element behind, if this isn't a number then we must be at the start of a number
            if not(schematic[row][col-1].isdigit()) and col > 0:
                num_data = expand_num(schematic, row, col)
            # if we are at the start of a row, it must be the start of a number
            if col == 0:
                num_data = expand_num(schematic, row, col)
            num_positions[num_data[1]] = num_data[0]
        # find gears and populate their positions in a dict
        elif schematic[row][col] == "*":
            gear_positions[(row, col)] = 1

sum_ratios = 0

# for a gear to be adjacent to a number, both the row and col need to be within 1 of a number's row/col
for gear in gear_positions:
    adj_count = 0 # count how many numbers this gear is adjacent to
    gear_ratio = 1
    gear_row = gear[0]
    gear_col = gear[1]
    for num in num_positions:
        adjacent = False # check if a gear/number pair is adjacent
        num_len = len(num_positions[num])
        num_row = num[0]
        start_col = num[1]
        # loop through the full range of the number, from start to end
        for col in range(start_col,start_col+num_len):
            if abs(gear_row - num_row) < 2 and abs(gear_col - col) < 2:
                adjacent = True
        if adjacent:
            adj_count += 1
            gear_ratio *= int(num_positions[num]) # find gear ratio by multiplying by the adjacent numbers
    if adj_count == 2:
        sum_ratios += gear_ratio

print(f"pt2: {sum_ratios}")