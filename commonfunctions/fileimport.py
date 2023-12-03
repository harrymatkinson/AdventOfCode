root = "C:\\Code\\AdventOfCode\\"

# generate the import path for each day based on the dir structure
def import_path(day):
    return f"{root}\\day{day}\\data.txt"

def test_path(day):
    return f"{root}\\day{day}\\test.txt"