def largest(line):
    char = line[0]
    index = 0
    for i, c in enumerate(line):
        if c > char:
            char = c
            index = i
    return char, index + 1

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    digits = int(argv[2]) if len(argv) == 3 else 2

    with open(filename) as f:
        jolts = []

        for line in f:
            line = line.strip()
            length = digits
            start = 0
            jolt = ""
            while length > 0:
                end = len(line) - length + 1
                val, offset = largest(line[start:end])
                start = start + offset
                jolt = jolt + val
                length = length - 1
            print("jolt:", jolt)
            jolts.append(jolt)
    print(sum([int(j) for j in jolts]))