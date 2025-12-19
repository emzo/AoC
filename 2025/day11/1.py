def find_all_paths(graph, start, end, path=[]):
    """Find all paths from start to end in a graph"""
    path = path + [start]
    
    if start == end:
        return [path]
    
    if start not in graph:
        return []
    
    paths = []
    for node in graph[start]:
        if node not in path:  # Avoid cycles
            newpaths = find_all_paths(graph, node, end, path)
            paths.extend(newpaths)
    
    return paths

if __name__ == "__main__":
    from sys import argv
    filename = argv[1]

    graph = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            node, children = line.split(': ')
            children = children.split(' ')
            graph[node] = children
   
    paths = find_all_paths(graph, 'you', 'out')
    print(len(paths))
