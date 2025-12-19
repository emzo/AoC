from functools import lru_cache

def rotate_90(piece):
    return tuple(tuple(row) for row in zip(*piece[::-1]))

def flip_h(piece):
    return tuple(tuple(reversed(row)) for row in piece)

@lru_cache(maxsize=None)
def get_orientations(piece):
    orientations = set()
    for p in [piece, flip_h(piece)]:
        current = p
        for _ in range(4):
            orientations.add(current)
            current = rotate_90(current)
    return tuple(orientations)

@lru_cache(maxsize=None)
def count_cells(piece):
    return sum(sum(row) for row in piece)

@lru_cache(maxsize=None)
def piece_to_row_masks(orientation):
    return tuple(sum(1 << x for x, cell in enumerate(row) if cell) for row in orientation)

@lru_cache(maxsize=None)
def get_placements_covering(piece, target_row, target_col, grid_width, grid_height):
    placements = []
    for orientation in get_orientations(piece):
        row_masks = piece_to_row_masks(orientation)
        piece_height = len(orientation)
        piece_width = len(orientation[0])
        
        for py, row in enumerate(orientation):
            for px, cell in enumerate(row):
                if cell:
                    start_row = target_row - py
                    start_col = target_col - px
                    if (start_row >= 0 and start_col >= 0 and
                        start_row + piece_height <= grid_height and
                        start_col + piece_width <= grid_width):
                        shifted = tuple(m << start_col for m in row_masks)
                        placements.append((start_row, shifted))
    return tuple(placements)

def solve(grid_width, grid_height, shapes, counts):
    shapes_tuple = tuple(shapes[i] for i in range(len(counts)))
    piece_cells = tuple(count_cells(s) for s in shapes_tuple)
    full_row = (1 << grid_width) - 1
    
    cache = {}
    
    def can_pack(grid_masks, piece_counts):
        key = (grid_masks, piece_counts)
        if key in cache:
            return cache[key]
        
        # Calculate cells still needed
        cells_needed = sum(piece_cells[i] * piece_counts[i] for i in range(len(piece_counts)))
        if cells_needed == 0:
            return True
        
        # Find first empty cell
        first_empty = None
        for r, row in enumerate(grid_masks):
            if row != full_row:
                for c in range(grid_width):
                    if not (row & (1 << c)):
                        first_empty = (r, c)
                        break
                if first_empty:
                    break
        
        if first_empty is None:
            cache[key] = False
            return False
        
        target_row, target_col = first_empty
        
        # Early termination: count empty cells
        empty_cells = sum((full_row ^ r).bit_count() for r in grid_masks)
        if cells_needed > empty_cells:
            cache[key] = False
            return False
        
        # Try each piece type
        for piece_idx in range(len(piece_counts)):
            if piece_counts[piece_idx] == 0:
                continue
            
            piece = shapes_tuple[piece_idx]
            placements = get_placements_covering(piece, target_row, target_col, grid_width, grid_height)
            
            for start_row, shifted_masks in placements:
                # Check validity
                can_place = True
                for dy, mask in enumerate(shifted_masks):
                    if grid_masks[start_row + dy] & mask:
                        can_place = False
                        break
                
                if can_place:
                    # Create new state
                    new_grid = list(grid_masks)
                    for dy, mask in enumerate(shifted_masks):
                        new_grid[start_row + dy] |= mask
                    
                    new_counts = list(piece_counts)
                    new_counts[piece_idx] -= 1
                    
                    if can_pack(tuple(new_grid), tuple(new_counts)):
                        cache[key] = True
                        return True
        
        # No piece fits - mark cell as permanently blocked
        new_grid = list(grid_masks)
        new_grid[target_row] |= (1 << target_col)
        result = can_pack(tuple(new_grid), piece_counts)
        cache[key] = result
        return result
    
    initial_grid = tuple([0] * grid_height)
    initial_counts = tuple(counts)
    
    return can_pack(initial_grid, initial_counts)

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    packable = 0
    shapes = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.endswith(':') and line[:-1].isdigit():
                idx = int(line[:-1])
                shape = []
            elif len(line) == 3 and set(line) <= {'#', '.'}:
                shape.append(tuple(1 if x == '#' else 0 for x in line))
            elif line == '':
                if shape:
                    shapes[idx] = tuple(shape)
            elif 'x' in line:
                grid_spec, pieces = line.split(': ')
                cols, rows = map(int, grid_spec.split('x'))
                counts = list(map(int, pieces.split()))
                
                if solve(cols, rows, shapes, counts):
                    packable += 1
                    print(line, True)
                else:
                    print(line, False)
    
    print(packable)