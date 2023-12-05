from commonfunctions.fileimport import import_path, test_path
from re import search

path = import_path(4)
# path = test_path(4)

# store data as a dict
# keys: card number
# values: list with 3 elements = the winning numbers, my numbers, and the no. of copies of this card
scratchcards = {}

with open(path) as raw_data:
    for line in raw_data:
        card_no = int(search(r"(\d{1,3}):",line).group(1))
        # some numbers have extra leading spaces so splitting on " " leads to some empty strings as list elements
        # this isn't an issue though as we can ignore them later
        winning_nums = search(r": (.+) \|",line).group(1).split(" ")
        my_nums = search(r"\| (.+)$",line).group(1).split(" ")
        scratchcards[card_no] = [winning_nums,my_nums,1]

total_points = 0
# for each scratchcard, the total points is equal to:
# total_points = 2^(n-1), where n is the number of matching numbers
for scratchcard in scratchcards:
    win_total = 0 # how many matching numbers this scratchcard has
    winning_nums = scratchcards[scratchcard][0]
    my_nums = scratchcards[scratchcard][1]
    for m in my_nums:
        if m != "" and m in winning_nums:
            win_total += 1
    if win_total:
        total_points += 2**(win_total-1)

print(f"pt1: {total_points}")

## PT2
total_copies = 0

for scratchcard in scratchcards:
    # number of copies of each scratchcard is stored in the dict value as another list element
    n_copies = scratchcards[scratchcard][2]
    # loop through every copy of this card
    for copy in range(n_copies):
        win_total = 0 # how many matching numbers this scratchcard has
        winning_nums = scratchcards[scratchcard][0]
        my_nums = scratchcards[scratchcard][1]
        for m in my_nums:
            if m != "" and m in winning_nums:
                win_total += 1
        if win_total:
            # loop through each card number to be copied
            for i in range(int(scratchcard)+1, int(scratchcard)+win_total+1):
                scratchcards[i][2] += 1 # increment the copies number for this card
    total_copies += n_copies

print(f"pt2: {total_copies}")