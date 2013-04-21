
nodes = []

def dfs(n, edges):
    global nodes

    nodes.append(n)

    for (u, v) in edges:
        if u == n:
            dfs(v, edges)

def tree_traversal(n, edges):
    global nodes
    nodes.append(n)

    dfs(n, edges)

    return nodes
