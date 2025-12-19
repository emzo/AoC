if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    points = []
    max_area = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            a, b = line.split(',')
            points.append((int(a), int(b)))
        for x1, y1 in points:
            for x2, y2 in points:
                area = (max(x1, x2) - min(x1, x2) + 1) * (max(y1, y2) - min(y1, y2) + 1)
                if area > max_area:
                     max_area = area
    print(max_area)
        