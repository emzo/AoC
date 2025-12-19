# import time
# import timeit

def largest_joltage(line, k):
    """Find largest k-digit number by selecting k digits in order from line."""
    line = line.strip()
    to_remove = len(line) - k
    stack = []
    
    for digit in line:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    
    return ''.join(stack[:k])


def main(filename, digits=12):
    total = 0
    
    with open(filename) as f:
        # start= time.time()
        for line in f:
            jolt = largest_joltage(line, digits)
            print(f"jolt: {jolt}")
            total += int(jolt)
        # end = time.time()
    
    # print(total, "in", (end - start) * 1000, "ms")
    print(total)


if __name__ == "__main__":
    from sys import argv
    
    filename = argv[1]
    digits = int(argv[2]) if len(argv) > 2 else 12
    
    # start= time.time()
    main(filename, digits)
    # end = time.time()

    # t = timeit.timeit(lambda: main(filename, digits), number=1000)
    # print(t)

    # print((end - start) * 1000, "ms")