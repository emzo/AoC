# def octree(points, max_depth=10):
#     """
#     Create an octree spatial partitioning of 3D points.
    
#     Args:
#         points: List of [x, y, z] coordinates
#         max_depth: Number of times we partition the space
        
#     Returns:
#         (bin_depths, bin_parents, bin_corners, point_bins)
#     """
#     # Find bounding box
#     min_corner = [min(p[i] for p in points) for i in range(3)]
#     max_corner = [max(p[i] for p in points) for i in range(3)]
    
#     # Initialize root bin
#     bin_depths = [0]
#     bin_parents = [0]
#     bin_corners = [min_corner + max_corner]
#     point_bins = [0] * len(points)
    
#     def divide(bin_no):
#         # Exit if max depth reached
#         if bin_depths[bin_no] >= max_depth:
#             return
        
#         # Count points in this bin
#         bin_point_count = sum(1 for pb in point_bins if pb == bin_no)
        
#         # Don't subdivide if too few points in bin
#         if bin_point_count <= 1:
#             return
        
#         # Calculate center point
#         corners = bin_corners[bin_no]
#         mid = [(corners[i] + corners[i+3]) / 2 for i in range(3)]
        
#         # Create 8 octants
#         for octant in range(8):
#             # Determine octant corners
#             octant_min = [mid[i] if octant & (4 >> i) else corners[i] for i in range(3)]
#             octant_max = [corners[i+3] if octant & (4 >> i) else mid[i] for i in range(3)]
            
#             # Add new bin
#             new_bin_no = len(bin_depths)
#             bin_depths.append(bin_depths[bin_no] + 1)
#             bin_parents.append(bin_no)
#             bin_corners.append(octant_min + octant_max)
            
#             # Assign points to this octant
#             for i, point in enumerate(points):
#                 if point_bins[i] == bin_no:
#                     in_octant = all(octant_min[j] <= point[j] < octant_max[j] for j in range(3))
#                     if in_octant:
#                         point_bins[i] = new_bin_no
            
#             # Recursively divide
#             divide(new_bin_no)
    
#     divide(0)
#     return bin_depths, bin_parents, bin_corners, point_bins

# def find_nearest_octree_pairs(points, point_bins, bin_corners):
#     """Find the n shortest distances between any pair of points."""
    
#     # Group points by bin
#     bin_to_points = {}
#     for i, bin_no in enumerate(point_bins):
#         bin_to_points.setdefault(bin_no, []).append(i)
    
#     def bins_touch(bin1, bin2):
#         """Check if bins are neighbors."""
#         c1, c2 = bin_corners[bin1], bin_corners[bin2]
#         for dim in range(3):
#             if c1[dim+3] < c2[dim] or c2[dim+3] < c1[dim]:
#                 return False
#         return True
    
#     distances = []
    
#     # Check each bin and its neighbors
#     for bin_no, indices in bin_to_points.items():
#         neighbors = [b for b in bin_to_points if bins_touch(bin_no, b)]
#         candidates = [i for b in neighbors for i in bin_to_points[b]]
        
#         # Calculate all distances within candidates
#         for i in indices:
#             for j in candidates:
#                 if i < j:
#                     dist_sq = sum((points[i][k] - points[j][k])**2 for k in range(3))
#                     distances.append((dist_sq**0.5, i, j))
    
#     return sorted(distances)

def find_nearest_pairs(points):
    """Brute force - check ALL pairs."""
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist_sq = sum((points[i][k] - points[j][k])**2 for k in range(3))
            distances.append((dist_sq**0.5, i, j))
    return sorted(distances)

if __name__ == "__main__":
    from sys import argv
    import math
    filename = argv[1]
    num_pairs = int(argv[2]) if len(argv) == 3 else 1000

    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            point = line.split(',')
            point = map(int, point)
            points.append(list(point))
    pairs = find_nearest_pairs(points)

    # Initially I tried to be too clever and put in an
    # optimizations to significantly reduce the number
    # of points we have to check in order to find pairs
    # but it gave the wrong results!
    # What do they say about premature optimisation? ;)

    # depths, parents, corners, bins = octree(points)
    # pairs = find_nearest_octree_pairs(points, bins, corners)

    circuits = []
    for _, a, b in pairs[:num_pairs]:
        # Find which circuits contain a and b
        circuit_a = None
        circuit_b = None
        for c in circuits:
            if a in c:
                circuit_a = c
            if b in c:
                circuit_b = c
        
        if circuit_a is circuit_b and circuit_a is not None:
            # Already in same circuit, do nothing
            pass
        elif circuit_a is not None and circuit_b is not None:
            # Merge two different circuits
            circuit_a.update(circuit_b)
            circuits.remove(circuit_b)
        elif circuit_a is not None:
            circuit_a.add(b)
        elif circuit_b is not None:
            circuit_b.add(a)
        else:
            # Create new circuit
            circuits.append({a, b})

    lengths = list(map(len, circuits))
    sorted_lengths = sorted(lengths, reverse=True)
    print(sorted_lengths[:3])
    print(math.prod(sorted_lengths[:3]))