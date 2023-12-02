from re import search

input = "C:\\Code\\AdventOfCode\\day1\\data.txt"

sum = 0

## SOLUTION FOR FIRST STAR

# with open(input) as raw_file:
#     for line in raw_file:
#         first_num = search(r"(\d{1})",str(line)).group(1)
#         # negative lookahead ensures that we find the digit that isn't followed by any other digits
#         second_num = search(r"(\d{1})(?!.*\d{1})",str(line)).group(1)
#         concat_num = int(str(first_num) + str(second_num))
#         sum += concat_num

# print(sum)

## SOLUTION FOR SECOND STAR

num_map = {
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9,
}

with open(input) as raw_file:
    for line in raw_file:

        first_num = 0
        second_num = 0
        first_word = ""
        second_word = ""

        # track the index positions of the first word and digit
        # these start at infinity because we are trying to find the lowest one
        first_word_i = float("inf")
        first_digit_i = float("inf")

        # find index position of first digit
        for i in range(len(line)):
            if line[i].isdigit():
                first_digit_i = i
                break

        # find index position of first word
        for i in range(len(line)-2):
            # if we go past the first digit, then we can stop
            if i >= first_digit_i:
                break
            word = str(line[i]) + str(line[i+1]) + (line[i+2])
            try:
                if word in num_map:
                    first_word_i = i
                    first_word = word
                    break
                elif word + str(line[i+3]) in num_map:
                    first_word_i = i
                    first_word = word + str(line[i+3])
                    break
                elif word + str(line[i+3]) + str(line[i+4]) in num_map:
                    first_word_i = i
                    first_word = word + str(line[i+3]) + str(line[i+4])
                    break
            # we search past the end of the line, therefore word is not found
            except IndexError:
                break

        if first_digit_i < first_word_i:
            first_num = line[first_digit_i]
        else:
            first_num = num_map[first_word]

        # index positions for the second word and digit
        # we search backwards so they start at 0 (trying to find the highest)
        second_word_i = 0
        second_digit_i = 0

        # find index position of second digit
        for i in reversed(range(len(line))):
            if line[i].isdigit():
                second_digit_i = i
                break

        # find index position of second word
        for i in reversed(range(2,len(line))):
            # if we go past the second digit, then we can stop
            if i <= second_digit_i:
                break
            word = str(line[i-2]) + str(line[i-1]) + (line[i]) # assemble the word backwards
            try:
                if word in num_map:
                    second_word_i = i
                    second_word = word
                    break
                elif str(line[i-3]) + word in num_map:
                    second_word_i = i
                    second_word = str(line[i-3]) + word
                    break
                elif str(line[i-4]) + str(line[i-3]) + word in num_map:
                    second_word_i = i
                    second_word = str(line[i-4]) + str(line[i-3]) + word
                    break
            # we search past the end of the line, therefore word is not found
            except IndexError:
                break

        if second_digit_i >= second_word_i:
            second_num = line[second_digit_i]
        else:
            second_num = num_map[second_word]

        concat_num = int(str(first_num) + str(second_num))
        sum += concat_num

print(sum)