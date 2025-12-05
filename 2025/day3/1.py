def largest(line):
    # print(line)
    char = line[0]
    index = 0
    for i, c in enumerate(line):
        if c > char:
            char = c
            index = i
    return char, index+1

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    jolts = []
    with open(filename) as f:
        for line in f:
            print(line.strip())
            first, index = largest(line.strip()[:-1])
            # print(first, index)
            second, _ = largest(line.strip()[index:])
            jolt = first + second
            print(jolt)
            jolts.append(jolt)
            # print("")
    # print(jolts)
    print(sum([int(j) for j in jolts]))