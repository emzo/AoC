def merge_ranges(ranges):
    # Sort by range start
    ranges = sorted(ranges, key=lambda r: r.start)
    merged = []

    for r in ranges:
        if not merged:
            merged.append(r)
            continue

        last = merged[-1]

        # If non-overlapping and not touching
        if r.start > last.stop:
            merged.append(r)
        else:
            # Overlaps or touches — merge
            merged[-1] = range(last.start, max(last.stop, r.stop))

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
                ranges.append(range(start, end + 1))
            if not line:
                break

    merged = merge_ranges(ranges)

    total = sum(r.stop - r.start for r in merged)

    print(total)
