# /// script
# dependencies = ["pulp"]
# ///

if __name__ == "__main__":
    from sys import argv
    from ast import literal_eval
    from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger # Linear Programming library
    filename = argv[1]
    total = 0

    with open(filename) as f:
        for line in f:
            line = line.strip()
            pieces = line.split()
            # lights = pieces[0]
            # lights = lights[1:-1]
            # lights = list(lights)
            # end_state = list(map(lambda x: 1 if x == '#' else 0, lights))
            switches = pieces[1:-1]
            switches = list(map(lambda x: tuple([int(x[1:-1])]) if len(x) == 3 else literal_eval(x), switches))
            joltages = pieces[-1]
            joltages = joltages[1:-1]
            joltages = literal_eval(f"[{joltages}]")

            prob = LpProblem("MyProblem", LpMinimize)
            x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(len(switches))]
            prob += lpSum(x)

            for j, target in enumerate(joltages):
                prob += lpSum(x[i] for i, switch in enumerate(switches) if j in switch) == target
            prob.solve()

            presses = sum(v.varValue for v in x)
            total += int(presses)

    print(total)