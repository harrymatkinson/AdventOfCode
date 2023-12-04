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

print(f"pt1: {pt1}")


## TRY: PT 2
# 1. function that fills in a number from finding one digit (by going left and right along the row)
# 2. store the index positions and values of each number in a dict, to prevent double counting of overlapping numbers
# 3. store the index positions of each "*" and compare to the dict in [2]