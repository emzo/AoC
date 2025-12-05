
if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    
    ranges = []
    count = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if '-' in line:
                start, end = line.split('-')
                ranges.append((int(start), int(end)))
            elif not line:
                continue
            else:
                i = int(line)
                if any([i in range(start, end + 1) for start, end in ranges]):
                    count += 1
    print(count)