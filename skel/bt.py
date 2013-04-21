
nodes = []

def bfs(n, edges):
    global nodes

    nodes.append(n)

    for (u, v) in edges:
        if u == n:
            tree_traversal(v, edges)

def tree_traversal(n, edges):
    global nodes
    nodes.append(n)

    bfs(n, edges)

    return nodes
