def process_line(line, previous):
    count = []
    new = []
    for i, (prev, char) in enumerate(zip(previous, line)):
        match (prev, char):
            case ('.', '.'):
                new.append('.')
            case ('S', '.'):
                new.append('|')
            case ('|', '.'):
                new.append('|')
            case ('|', '|'):
                new.append('|')
            case ('.', '^'):
                new.append('^')
            case ('^', '.'):
                new.append('.')
            case ('|', '^'):
                new.append('^')
                count.append(i)
    for i in count:
        new[i-1] = '|'
        new[i+1] = '|'
    return ''.join(new), len(count)

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    with open(filename) as f:
        previous_line = None
        splits = 0
        for line in f:
            line = line.strip()
            if previous_line == None:
                previous_line = line
                continue
            previous_line, s = process_line(line, previous_line)
            splits += s
        print(splits)
