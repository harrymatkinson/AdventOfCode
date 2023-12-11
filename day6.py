from commonfunctions.fileimport import import_path, test_path
from re import search

path = import_path(6)
# path = test_path(6)
with open(path) as raw_data:
    for line in raw_data:
        re_times = search(r"^Time:(.+)$",line)
        if re_times:
            raw_times = re_times.group(1)
        re_distances = search(r"^Distance:(.+)$",line)
        if re_distances:
            raw_distances = re_distances.group(1)

raw_times = raw_times.split()
raw_distances = raw_distances.split()

races = {int(raw_times[i]):int(raw_distances[i]) for i in range(len(raw_times))}

results = {x:0 for x in range(len(races))}

race_no = 0
for race_time in races:
    # speed = distance / time, so the min speed must be this + 1 (as we can't have a floating point speed)
    min_speed = races[race_time] // race_time + 1
    
    # loop through all possible times up to the time required to build up to min_speed
    for t in reversed(range(race_time-min_speed+1)):
        speed = race_time-t # speed is the race time minus the available moving time
        max_d = t*speed # max distance = time * speed
        # if we beat the current distance record
        if max_d > races[race_time]:
            results[race_no] += 1
    
    race_no += 1

ans = 1
for result in results:
    ans *= results[result]

print(f"pt1: {ans}")


pt2_time = int("".join(raw_times))
pt2_distance = int("".join(raw_distances))

# equation is x = -1(s^2) + ts - d
# a = -1
# b = t
# c = -d
def find_quad_roots(a, b, c):
    # round roots up to nearest int
    x_1 = int((-b + ((b**2 - 4*(a*c)))**0.5) / 2*a)+1
    x_2 = int((-b - ((b**2 - 4*(a*c)))**0.5) / 2*a)+1
    return [x_1,x_2]

roots = find_quad_roots(a=-1, b=pt2_time, c=-pt2_distance)

pt2_ans = len(range(roots[0],roots[1]))

print(f"pt2: {pt2_ans}")
