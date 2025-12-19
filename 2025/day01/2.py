
def read_lines(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')

def turn_dial(pos, amt):
    return (pos + amt) % 100

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    passwd = 0
    pos = 50
    for line in read_lines(filename):
        dir = -1 if line[0].upper() == 'L' else 1
        amt = number = int(line[1:])
        while amt > 0:
            pos = turn_dial(pos, dir)
            if pos == 0:
                passwd = passwd + 1
            amt = amt - 1
    print(passwd)
