from commonfunctions.fileimport import import_path, test_path
from re import search

path = import_path(5)
# path = test_path(5)

# store the line numbers where the corresponding map data starts
seed_soil_map_start = 0
soil_fert_map_start = 0
fert_wate_map_start = 0
wate_ligh_map_start = 0
ligh_temp_map_start = 0
temp_humi_map_start = 0
humi_loca_map_start = 0

# loop through file once to get the start positions of each map, and the seed nos
with open(path) as raw_data:
    for i, line in enumerate(raw_data):
        re_seeds = search(r"^seeds: (.+)$",line)
        if re_seeds:
            raw_seed_nos = re_seeds.group(1)
            raw_seed_nos = raw_seed_nos.split()
        if search(r"seed-to-soil map:",line):
            seed_soil_map_start = i
        elif search(r"soil-to-fertilizer map:",line):
            soil_fert_map_start = i
        elif search(r"fertilizer-to-water map:",line):
            fert_wate_map_start = i
        elif search(r"water-to-light map:",line):
            wate_ligh_map_start = i
        elif search(r"light-to-temperature map:",line):
            ligh_temp_map_start = i
        elif search(r"temperature-to-humidity map:",line):
            temp_humi_map_start = i
        elif search(r"humidity-to-location map:",line):
            humi_loca_map_start = i

for i in range(len(raw_seed_nos)):
    raw_seed_nos[i] = int(raw_seed_nos[i])

# store the raw lines for each map
seed_soil_lines = []
soil_fert_lines = []
fert_wate_lines = []
wate_ligh_lines = []
ligh_temp_lines = []
temp_humi_lines = []
humi_loca_lines = []

# strip and split a line of raw data
# then convert all values to ints
def clean_line(line):
    line = line.strip().split()
    for i in range(len(line)):
        line[i] = int(line[i])
    return line

with open(path) as raw_data:
    for i, line in enumerate(raw_data):
        if i > seed_soil_map_start and i < (soil_fert_map_start-1):
            seed_soil_lines.append(clean_line(line))
        elif i > soil_fert_map_start and i < (fert_wate_map_start-1):
            soil_fert_lines.append(clean_line(line))
        elif i > fert_wate_map_start and i < (wate_ligh_map_start-1):
            fert_wate_lines.append(clean_line(line))
        elif i > wate_ligh_map_start and i < (ligh_temp_map_start-1):
            wate_ligh_lines.append(clean_line(line))
        elif i > ligh_temp_map_start and i < (temp_humi_map_start-1):
            ligh_temp_lines.append(clean_line(line))
        elif i > temp_humi_map_start and i < (humi_loca_map_start-1):
            temp_humi_lines.append(clean_line(line))
        elif i > humi_loca_map_start:
            humi_loca_lines.append(clean_line(line))

# for a source val, find the corresponding mapped val
# by looking through the lines of data for the mapping
def find_mapped_val(source, lines):
    dest = source # default value
    for line in lines:
        if source in range(line[1],line[1]+line[2]):
            # dest = current_source - source_start + dest_start
            dest = source - line[1] + line[0]
            break
    return dest

# modified version of find_mapped_val that works on a single line
def find_mapped_val_line(source, line):
    dest = "" # if we can't find it, use a blank string to denote this
    if source in range(line[1],line[1]+line[2]):
        # dest = current_source - source_start + dest_start
        dest = source - line[1] + line[0]
    return dest

# loop through the lines data and see if the current source range can be mapped to a dest range
# this also splits ranges in case they don't fit exactly into a mapping
# therefore we should return a list of mapped ranges, instead of just one
def find_mapped_range(source_ranges, lines, dest_ranges):
    for source_range in source_ranges:
        dest_range = ["",""]
        for line in lines:
            # define the line bounds
            left = line[1]
            right = line[1]+line[2]
            # try to insert the source range bounds into the line bounds
            # if source range fits completely, we can map both bounds and return all mapped ranges to this point
            if source_range[0] in range(left,right) and source_range[1] in range(left,right):
                dest_range[0] = find_mapped_val_line(source_range[0], line)
                dest_range[1] = find_mapped_val_line(source_range[1], line)
                dest_ranges.append(dest_range)
                break # once the source range is fully mapped, break out of lines loop
            # only the left source bound is within the line bounds
            elif source_range[0] in range(left,right):
                # if source bound is smaller than line bounds
                if source_range[1] < left:
                    # split_range is the part that doesn't fit in the line bounds
                    split_range = [[source_range[1],left-1]]
                    # we can map the other part and add it to dest_ranges
                    source_range = [left,source_range[0]]
                    dest_range[0] = find_mapped_val_line(source_range[0], line)
                    dest_range[1] = find_mapped_val_line(source_range[1], line)
                    dest_ranges.append(dest_range)
                    # then run function recursively with the split range until it is mapped
                    dest_ranges = find_mapped_range(split_range, lines, dest_ranges)
                    break
                # if source bound is larger than line bounds
                elif source_range[1] > right:
                    split_range = [[right,source_range[1]]]
                    source_range = [source_range[0],right-1]
                    dest_range[0] = find_mapped_val_line(source_range[0], line)
                    dest_range[1] = find_mapped_val_line(source_range[1], line)
                    dest_ranges.append(dest_range)
                    dest_ranges = find_mapped_range(split_range, lines, dest_ranges)
                    break
            # only the right source bound is within the line bounds
            elif source_range[1] in range(left,right):
                # if source bound is smaller than line bounds
                if source_range[0] < left:
                    # split_range is the part that doesn't fit in the line bounds
                    split_range = [[source_range[0],left-1]]
                    # we can map the other part and add it to dest_ranges
                    source_range = [left,source_range[1]]
                    dest_range[0] = find_mapped_val_line(source_range[0], line)
                    dest_range[1] = find_mapped_val_line(source_range[1], line)
                    dest_ranges.append(dest_range)
                    # then run function recursively with the split range until it is mapped
                    dest_ranges = find_mapped_range(split_range, lines, dest_ranges)
                    break
                # if source bound is larger than line bounds
                elif source_range[0] > right:
                    split_range = [[right+1,source_range[0]]]
                    source_range = [source_range[1],right]
                    dest_range[0] = find_mapped_val_line(source_range[0], line)
                    dest_range[1] = find_mapped_val_line(source_range[1], line)
                    dest_ranges.append(dest_range)
                    dest_ranges = find_mapped_range(split_range, lines, dest_ranges)
                    break

        # if either dest bounds aren't mapped after all that looping/recursion, set to the source bounds and return
        if dest_range[0] == "" and dest_range[1] == "":
            dest_ranges.append(source_range)
        elif dest_range[0] == "":
            dest_range[0] = source_range[0]
            dest_ranges.append(dest_range)
        elif dest_range[1] == "":
            dest_range[1] = source_range[1]
            dest_ranges.append(dest_range)

    # after mapping everything, return the dest_ranges
    return dest_ranges


# PT1
locations = []
for seed in raw_seed_nos:
    soil = find_mapped_val(seed, seed_soil_lines)
    fert = find_mapped_val(soil, soil_fert_lines)
    wate = find_mapped_val(fert, fert_wate_lines)
    ligh = find_mapped_val(wate, wate_ligh_lines)
    temp = find_mapped_val(ligh, ligh_temp_lines)
    humi = find_mapped_val(temp, temp_humi_lines)
    loca = find_mapped_val(humi, humi_loca_lines)
    locations.append(loca)

print(f"pt1: {min(locations)}")


# PT2
locations = []
current_seeds = ["",""] # store the range for the current raw_seed_nos pair
for i in range(len(raw_seed_nos)):
    # if an even indexed value, its just a seed no so make this the lower bound of current_range
    if i % 2 == 0:
        current_seeds[0] = raw_seed_nos[i]
    # if an odd indexed value, its a range from the previous seed no
    # use this to form the upper bound of current_range
    # then try to fit them into the lines from the mapping data
    else:
        current_seeds[1] = current_seeds[0] + raw_seed_nos[i] - 1
        current_seeds = [current_seeds]
        current_soils = find_mapped_range(current_seeds, seed_soil_lines, dest_ranges=[])
        current_ferts = find_mapped_range(current_soils, soil_fert_lines, dest_ranges=[])
        current_wates = find_mapped_range(current_ferts, fert_wate_lines, dest_ranges=[])
        current_lighs = find_mapped_range(current_wates, wate_ligh_lines, dest_ranges=[])
        current_temps = find_mapped_range(current_lighs, ligh_temp_lines, dest_ranges=[])
        current_humis = find_mapped_range(current_temps, temp_humi_lines, dest_ranges=[])
        current_locas = find_mapped_range(current_humis, humi_loca_lines, dest_ranges=[])
        locations.append(min(current_locas))
        current_seeds = ["",""]

print(f"pt2: {min(min(locations))}")

