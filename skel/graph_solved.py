
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

nodes = []
component = []

# Get one component via DFS
def dfs(n, edges):
    global nodes, component

    component.append(n)
    nodes.append(n)

    for (u, v) in edges:
        if u == n and v not in nodes:
            dfs(v, edges)

# Determine SCCs
def graph(n, edges):
    global nodes, component
    res = []

    for i in range(n):
        component = []

        if i not in nodes:
            dfs(i, edges)
            res.append(component)

    return res

