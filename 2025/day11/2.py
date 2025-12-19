def count_paths_memo(graph, start, end, exclude=frozenset(), memo=None):
    """Count paths using memoization (works for DAGs)"""
    if memo is None:
        memo = {}
    
    if start in exclude:
        return 0
    
    if start in memo:
        return memo[start]
    
    if start == end:
        return 1
    
    if start not in graph:
        return 0
    
    count = 0
    for child in graph[start]:
        count += count_paths_memo(graph, child, end, exclude, memo)
    
    memo[start] = count
    return count

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
    
    # Inclusion-exclusion with memoization
    total = count_paths_memo(graph, 'svr', 'out')
    print(f"Total paths: {total}")
    
    avoid_dac = count_paths_memo(graph, 'svr', 'out', exclude={'dac'})
    print(f"Paths avoiding dac: {avoid_dac}")
    
    avoid_fft = count_paths_memo(graph, 'svr', 'out', exclude={'fft'})
    print(f"Paths avoiding fft: {avoid_fft}")
    
    avoid_both = count_paths_memo(graph, 'svr', 'out', exclude={'dac', 'fft'})
    print(f"Paths avoiding both: {avoid_both}")
    
    through_both = total - avoid_dac - avoid_fft + avoid_both
    print(f"\nPaths through both dac and fft: {through_both}")