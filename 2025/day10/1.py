if __name__ == "__main__":
    from sys import argv
    from ast import literal_eval
    from itertools import combinations
    filename = argv[1]
    total = 0

    with open(filename) as f:
        for line in f:
            line = line.strip()
            pieces = line.split()
            lights = pieces[0]
            lights = lights[1:-1]
            lights = list(lights)
            end_state = list(map(lambda x: 1 if x == '#' else 0, lights))
            switches = pieces[1:-1]
            switches = list(map(lambda x: tuple([int(x[1:-1])]) if len(x) == 3 else literal_eval(x), switches))
            # joltages = pieces[-1]
            # joltages = joltages[1:-1]
            # joltages = literal_eval(f"[{joltages}]")

            presses = len(end_state) + 1
            for n in range(1, len(switches) + 1):
                found = False
                for buttons in combinations(switches, n):
                    state = [0] * len(end_state)
                    for button in buttons:
                        for i in button:
                            state[i] ^= 1  # XOR for toggling
                    if state == end_state:
                        presses = n
                        found = True
                        break
                if found:
                    total += presses
                    break

    print(total)