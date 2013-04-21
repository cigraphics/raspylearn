
nodes = []
component = []

def dfs(n, edges):
    global nodes, component

    component.append(n)
    nodes.append(n)

    for (u, v) in edges:
        if u == n and v not in nodes:
            dfs(v, edges)

def graph(n, edges):
    global nodes, component
    res = []

    for i in range(n):
        component = []

        if i not in nodes:
            dfs(i, edges)
            res.append(component)

    return res

