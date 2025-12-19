def get_neighbours(grid, y, x):
    h = len(grid) -1
    w = len(grid[0]) -1
    if y == 0 and x == 0:
        return [grid[0][1], grid[1][1], grid[1][0]]
    elif y == 0 and x == w:
        return [grid[0][w-1], grid[1][w-1], grid[1][w]]
    elif y == h and x == 0:
        return [grid[0][h-1], grid[1][h-1], grid[1][h]]
    elif y == h and x == w:
        return [grid[w][h-1], grid[w-1][h-1], grid[w-1][h]]
    elif y == 0:
        return [
            grid[y][x-1], grid[y][x+1],
            grid[y+1][x-1], grid[y+1][x], grid[y+1][x+1],
        ]
    elif y == h:
        return [
            grid[y-1][x-1], grid[y-1][x], grid[y-1][x+1],
            grid[y][x-1], grid[y][x+1],
        ]
    elif x == 0:
        return [
            grid[y-1][x], grid[y-1][x+1],
            grid[y][x+1],
            grid[y+1][x], grid[y+1][x+1],
        ]
    elif x == w:
        return [
            grid[y-1][x-1], grid[y-1][x],
            grid[y][x-1],
            grid[y+1][x-1], grid[y+1][x],
        ]
    else:
        return [
            grid[y-1][x-1], grid[y-1][x], grid[y-1][x+1],
            grid[y][x-1], grid[y][x+1],
            grid[y+1][x-1], grid[y+1][x], grid[y+1][x+1],
        ]
    

def solve(grid):
    count = 0
    for y, line in enumerate(grid):
        for x, pos in enumerate(line):
            neighbours = get_neighbours(grid, y, x)
            if pos == '@' and neighbours.count('@') < 4:
                grid[y][x] = 'x'
                count += 1
    return count, grid

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    with open(filename) as f:
        grid = [list(line.strip()) for line in f]
    count, grid = solve(grid)
    total = count
    while count > 0:
        count, grid = solve(grid)
        total += count
    print(total)