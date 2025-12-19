def count_final_only(pos, new_pos, dist, direction):
    return 1 if new_pos == 0 else 0

def count_all_crossings(pos, new_pos, dist, direction):
    if direction == 'L':
        first_zero = pos if pos > 0 else 100
        return (dist - first_zero) // 100 + 1 if dist >= first_zero else 0
    return (pos + dist) // 100

def solve(filepath, counter):
    position, count = 50, 0
    
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            direction, dist = line[0], int(line[1:])
            new_pos = (position - dist if direction == 'L' else position + dist) % 100
            
            count += counter(position, new_pos, dist, direction)
            position = new_pos
    
    return count

def solve_part1(filepath):
    return solve(filepath, count_final_only)

def solve_part2(filepath):
    return solve(filepath, count_all_crossings)

if __name__ == "__main__":
    print("Part 1:", solve_part1("input.txt"))
    print("Part 2:", solve_part2("input.txt"))