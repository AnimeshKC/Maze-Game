import random as r
from copy import deepcopy


class Maze:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.maze_list = self.build_array()

        # starting node at (1, 1)
        self.path = [(1, 1)]
        self.visited = [(1, 1)]
        self.finish_path = list()
        self.random_maze = self.randomize_maze()

    def randomize_maze(self):
        # now go through the entire maze breaking walls until the bottom right corner is reached
        self.break_wall(1, 1)
        return self.maze_list

    def build_array(self):
        maze_list = list()
        # start off with the base maze with no broken walls
        for row in range(self.rows * 2 + 1):
            row_list = list()
            for column in range(self.columns):
                if not row % 2:  # row is even
                    row_list.append(1)
                    row_list.append(1)
                else:  # row is odd
                    row_list.append(1)
                    row_list.append(0)
            row_list.append(1)
            maze_list.append(row_list)

        # put in the finish block
        maze_list[self.rows * 2 - 1][self.columns * 2 - 1] = 3

        return maze_list

    def break_wall(self, x, y):
        start_path = len(self.path)
        old_path = deepcopy(self.path)
        # direction is 0 down, 1 left, 2 up, 3 right
        # add nodes not in path to path
        node = (x, y + 2)
        if node not in self.visited and not y + 2 > len(self.maze_list)-1:
            self.path.append(node)
        node = (x - 2, y)
        if node not in self.visited and not x - 2 < 1:
            self.path.append(node)
        node = (x, y - 2)
        if node not in self.visited and not y - 2 < 1:
            self.path.append(node)
        node = (x + 2, y)
        if node not in self.visited and not x + 2 > len(self.maze_list[0])-1:
            self.path.append(node)

        end_path = len(self.path)

        path_change = end_path - start_path  # should be 0, 1, 2 or 3

        if path_change == 0 and x == 1 and y == 1:  # now at the origin and cannot find anywhere else to go
            # finished randomisation
            return

        if path_change == 0:  # no more choices but also not at orgin, go back
            del self.path[-1]
            (x, y) = self.path[-1]
            self.break_wall(x, y)

        else:  # there is a choice to make
            # choosing a random path to take
            rand_int = r.randint(0, path_change - 1)  # either 0, 1 or 2
            old_path.append(self.path[-(rand_int+1)])
            self.path = deepcopy(old_path)
            self.visited.append(self.path[-1])

            # choice is made: make change in maze list
            (x_1, y_1) = self.path[-2]
            (x_2, y_2) = self.path[-1]
            x_diff = x_1 - x_2
            y_diff = y_1 - y_2

            if x_diff == 2:  # left
                self.maze_list[y_1][x_1-1] = 0
            elif x_diff == -2:  # right
                self.maze_list[y_1][x_1+1] = 0
            elif y_diff == 2:  # up
                self.maze_list[y_1-1][x_1] = 0
            elif y_diff == -2:  # down
                self.maze_list[y_1+1][x_1] = 0

            if self.path[-1] == (self.rows * 2 - 1, self.columns * 2 - 1):
                # found the end tile
                self.finish_path = self.path
                del self.path[-1]
                (x, y) = self.path[-1]
                self.break_wall(x, y)
            else:
                (x, y) = self.path[-1]
                self.break_wall(x, y)
        return
