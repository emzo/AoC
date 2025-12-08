def find_nearest_pairs(points):
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

    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            point = line.split(',')
            point = map(int, point)
            points.append(list(point))
    pairs = find_nearest_pairs(points)

    circuits = []
    for _, a, b in pairs:
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

        if len(circuits) == 1 and len(circuits[0]) == len(points):
            final_connecting_pair = (points[a], points[b])
            break

    # print(final_connecting_pair)
    print(final_connecting_pair[0][0] * final_connecting_pair[1][0])