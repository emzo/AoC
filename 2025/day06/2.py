if __name__ == "__main__":
    from sys import argv
    from itertools import groupby

    filename = argv[1]

    with open(filename) as f:
        lines = f.read().splitlines()
        operators = lines[-1:][0].split()
        lines = lines[:-1]
        transposed = [''.join(col) for col in zip(*lines)]
        groups = [list(group) for key, group in groupby(transposed, key=lambda x: x.strip() != '') if key]

        total = 0
        results = []
        for nums, op in zip(groups, operators):
            match op:
                case '+':
                    result = sum([int(n) for n in nums])
                case '*':
                    result = 1
                    for n in nums:
                        result *= int(n)
            total += result
        
        print(total)
