import bisect

def solve(filename):
    with open(filename) as f:
        red_tiles = [tuple(map(int, line.strip().split(','))) for line in f]
    
    # Build edges connecting consecutive red tiles
    vertical_edges = []
    horizontal_edges = []
    
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        
        if x1 == x2:
            vertical_edges.append((x1, min(y1, y2), max(y1, y2)))
        else:
            horizontal_edges.append((y1, min(x1, x2), max(x1, x2)))
    
    # Critical y-values where polygon shape can change
    critical_ys = sorted(set(y for _, y1, y2 in vertical_edges for y in (y1, y2)))
    
    def get_ranges(y, include_horizontal=True):
        """Get valid x-ranges at a given y using scanline"""
        # Count edge crossings (include bottom endpoint, exclude top)
        crossings = sorted(x for x, y1, y2 in vertical_edges if y1 <= y < y2)
        
        # Interior ranges from pairs of crossings
        ranges = [[crossings[i], crossings[i+1]] for i in range(0, len(crossings)-1, 2)]
        
        # Add horizontal boundary segments
        if include_horizontal:
            ranges += [[x1, x2] for y0, x1, x2 in horizontal_edges if y0 == y]
        
        # Merge overlapping ranges
        if not ranges:
            return []
        ranges.sort()
        merged = [ranges[0]]
        for r in ranges[1:]:
            if r[0] <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], r[1])
            else:
                merged.append(r)
        return merged
    
    # Build bands: (y_start, y_end, valid_ranges)
    bands = []
    for i, y in enumerate(critical_ys):
        bands.append((y, y + 1, get_ranges(y)))
        if i < len(critical_ys) - 1 and y + 1 < critical_ys[i + 1]:
            bands.append((y + 1, critical_ys[i + 1], get_ranges(y + 1, False)))
    
    band_starts = [b[0] for b in bands]
    
    def rectangle_fits(min_x, max_x, min_y, max_y):
        """Check if rectangle is entirely within polygon"""
        y = min_y
        while y <= max_y:
            idx = bisect.bisect_right(band_starts, y) - 1
            if idx < 0 or y >= bands[idx][1]:
                return False
            _, y_end, ranges = bands[idx]
            if not any(r[0] <= min_x and max_x <= r[1] for r in ranges):
                return False
            y = y_end
        return True
    
    # Check all pairs of red tiles
    max_area = 0
    for i, (x1, y1) in enumerate(red_tiles):
        for x2, y2 in red_tiles[i+1:]:
            if x1 != x2 and y1 != y2:
                if rectangle_fits(min(x1,x2), max(x1,x2), min(y1,y2), max(y1,y2)):
                    max_area = max(max_area, (abs(x2-x1)+1) * (abs(y2-y1)+1))
    
    return max_area

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]
    print(solve(filename))