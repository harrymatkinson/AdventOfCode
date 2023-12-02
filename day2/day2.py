from re import search

max_red = 12
max_green = 13
max_blue = 14

sum_ids = 0
sum_powers = 0

input = "C:\\Code\\AdventOfCode\\day2\\data.txt"

game_dict = {} # build a dict of all games with ID numbers as the keys

with open(input) as raw_file:
    for line in raw_file:
        game_id = search(r"^Game (\d{1,3}):",line).group(1)
        games_str = search(r"^Game \d{1,3}: (.+)$",line).group(1)
        games = games_str.split(sep=";")
        game_dict[game_id] = games

## SOLUTION FOR PT 1
for game_id in game_dict:
    n_red = 0
    n_green = 0
    n_blue = 0
    # "min" variables represent the fewest n of each colour that makes each game possible
    # in other words, they're the highest n of each colour across all sets in each game
    min_red = n_red
    min_green = n_green
    min_blue = n_blue
    exceeded = False
    # loop through each "game" under each ID and find the count of each colour
    for game in game_dict[game_id]:
        re_red = search(r"(\d{1,2}) red",game)
        if re_red:
            n_red = int(re_red.group(1))
            if n_red > min_red:
                min_red = n_red
        re_green = search(r"(\d{1,2}) green",game)
        if re_green:
            n_green = int(re_green.group(1))
            if n_green > min_green:
                min_green = n_green
        re_blue = search(r"(\d{1,2}) blue",game)
        if re_blue:
            n_blue = int(re_blue.group(1))
            if n_blue > min_blue:
                min_blue = n_blue

        # if any count exceeds its max, we can stop
        if n_red > max_red or n_green > max_green or n_blue > max_blue:
            exceeded = True
            break
    
    # check if we have exceeded a max on any games under this ID
    # if we haven't, we can add it to the answer
    if not(exceeded):
        sum_ids += int(game_id)

print(f"pt 1: {sum_ids}")

## SOLUTION FOR PT2
for game_id in game_dict:
    n_red = 0
    n_green = 0
    n_blue = 0
    # "min" variables represent the fewest n of each colour that makes each game possible
    # in other words, they're the highest n of each colour across all sets in each game
    min_red = n_red
    min_green = n_green
    min_blue = n_blue
    # loop through each "game" under each ID and find the count of each colour
    # then if this count is higher than the corresponding "min" variable, save it
    for game in game_dict[game_id]:
        re_red = search(r"(\d{1,2}) red",game)
        if re_red:
            n_red = int(re_red.group(1))
            if n_red > min_red:
                min_red = n_red
        re_green = search(r"(\d{1,2}) green",game)
        if re_green:
            n_green = int(re_green.group(1))
            if n_green > min_green:
                min_green = n_green
        re_blue = search(r"(\d{1,2}) blue",game)
        if re_blue:
            n_blue = int(re_blue.group(1))
            if n_blue > min_blue:
                min_blue = n_blue

    power = min_red * min_green * min_blue
    sum_powers += power

print(f"pt 2: {sum_powers}")