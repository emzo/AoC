def process_line(line, prev_count):
    for i, (char, count) in enumerate(zip(line, prev_count)):
        match (char, count > 0):
            case ('^', True):
                prev_count[i-1] += count
                prev_count[i] = 0
                prev_count[i+1] += count
            case ('.', True):
                prev_count[i] = prev_count[i]
    return prev_count

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    with open(filename) as f:
        counts = None
        for line in f:
            line = line.strip()
            if counts == None:
                counts = list(map(lambda x: 1 if x == 'S' else 0, line))
                continue
            counts = process_line(line, counts)
        print(sum(counts))
