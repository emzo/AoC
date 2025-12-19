
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
        dir = line[0]
        amt = number = int(line[1:]) * (-1 if dir.upper() == 'L' else 1)
        pos = turn_dial(pos, amt)
        if pos == 0:
            passwd = passwd + 1
    print(passwd)
