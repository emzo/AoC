def merge_intervals(intervals):
    intervals.sort()
    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    ranges = []

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if '-' in line:
                start, end = map(int, line.split('-'))
                ranges.append((start, end))
            if not line:
                break

    merged = merge_intervals(ranges)

    total = sum(end - start + 1 for start, end in merged)

    print(total)
