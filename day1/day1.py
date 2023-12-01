from re import search

input = "C:\\Code\\AdventOfCode\\day1\\test.txt"

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

format_num = lambda x: num_map[x] if x in num_map else x

word_candidates = ["o","on","one","t","tw","two","th","thr","thre","three","f","fo","fou","four",\
                   "fi","fiv","five","s","si","six","se","sev","seve","seven","e","ei","eig","eigh","eight","n","ni","nin","nine"]
rev_word_candidates = ["e","en","eno","o","ow","owt","ee","eer","eerh","eerht","r","ru","ruo","ruof",\
                       "ev","evi","evif","x","xi","xis","n","ne","nev","neve","neves","t","th","thg","thgi","thgie","eni","enin"]

## TRY: looping through each letter and looking ahead up to 4 extra letters to find potential words
# (use pointers for this instead of just looping through the list)

with open(input) as raw_file:
    for line in raw_file:
        print(f"line: {line}")

        ## find the first number
        first_word = "" # track number words (e.g. "one", "two")
        first_digit = 0

        for letter in line:
            if not(letter.isdigit()):
                first_word += letter
                print(first_word)
                if first_word not in word_candidates:
                    first_word = letter
                elif first_word in num_map:
                    break
            else:
                first_digit = letter
                break
        
        # if we have found a digit first, use this
        if first_digit:
            first_num = first_digit
        # otherwise we must have found a word first, so use this
        else:
            first_num = num_map[first_word]
        ## first number found


        ## find the last number
        last_word = ""
        last_digit = 0

        for letter in reversed(line):
            if not(letter.isdigit()):
                last_word += letter
                if last_word not in rev_word_candidates:
                    last_word = letter
                elif last_word[::-1] in num_map:
                    break
            else:
                last_digit = letter
                break
        
        # if we have found a digit first, use this
        if last_digit:
            last_num = last_digit
        # otherwise we must have found a word first, so use this
        else:
            last_num = num_map[last_word[::-1]]
        ## last number found

        print(f"first_num: {first_num}")
        print(f"last_num: {last_num}")

        concat_num = int(str(first_num) + str(last_num))
        sum += concat_num

print(sum)