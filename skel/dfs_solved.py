
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

frontier = [(1, 1)]

TREE = 3
BEAR = 1
RASP = 2
FREE = 0
PASSED = 4

dx = [0, 0, 1, -1]
dy = [-1, 1, 0, 0]

def next_move(matrix):
    global frontier
    px, py = frontier[-1]
    matrix[px][py] = PASSED
    #pop front
    frontier = frontier[:-1]

    for i in xrange(len(dx)):
        x, y = px, py
        x += dx[i]
        y += dy[i]
        if matrix[x][y] == FREE or matrix[x][y] == RASP:
            frontier.append((x, y))

    return px, py


