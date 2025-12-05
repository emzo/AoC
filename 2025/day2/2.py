import re

def solve(input):
    total = 0
    pattern = re.compile(r"^(\d+)\1+$")
    ranges = input.split(",")
    for r in ranges:
        start, end = r.split("-")
        for num in range(int(start), int(end) + 1):
            m = pattern.search(str(num))
            if m:
                # print(f"{num}: {m}")
                total = total + num
    print(total)

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    with open(filename) as f:
        solve(f.read())

