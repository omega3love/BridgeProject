from batoocolors import *

class placement(object):

    def __init__(self):

        self.history = []

    def place(self, grid, color):

        if self.is_placable(grid, color):
            self.history.append([grid, color, 1])  # 1 denotes it survives at this moment

    def is_placable(self, grid, color):

        p = self.is_placed(grid, color)
        if p:
            if p == 'hidden':
                return 'hidden'
            return False

        elif self.is_surrounded(grid, color):
            catching_list = self.is_catching(grid, color, 1)
            if not catching_list:  # self-confined
                return False
            elif len(catching_list) == 1:  # pae fight
                caught = catching_list[0]
                if caught == self.history[-1][0]:
                    return False

        return True


    def is_placed(self, grid, color = None):

        for h in self.history:
            if h[-1] == 2 and grid == h[0]:  # discover adv's hidden
                opcol = self.color_toggle(color)
                if h[1] == opcol:
                    return 'hidden'
                else:
                    return h[1]
            elif h[-1] >= 1 and grid == h[0]:
                return h[1]

        return False


    def is_surrounded(self, grid, color):

        bunch = self.bunch(grid, color)
        sur = self.surrounding_grid(bunch)
        hidden = True

        for point in sur:
            p = self.is_placed(point, color)
            if p == 'hidden':
                hidden = point
            elif not p:
                return False

        return hidden


    def is_catching(self, grid, color, only_catching = 0):

        opcol = self.color_toggle(color)
        sur = self.surrounding_grid(grid)
        catching_list = []
        hidden_catcher = [] # hidden catches the other stones
        fix = 0

        if not self.is_placed(grid):
            self.history.append([grid, color, 1])
            fix = 1

        for point in sur:
            if self.is_placed(point) == opcol:
                surded = self.is_surrounded(point, opcol)
                if surded:
                    caught = self.bunch(point, opcol)
                    for stone in caught:
                        if stone not in catching_list:
                            catching_list.append(stone)
                    if type(surded) != bool:
                        h = [ surded, color, 2 ]
                        if not h in hidden_catcher:
                            hidden_catcher.append(h)
        if fix:
            self.history.pop()

        if len(catching_list) == 0:
            return False
        elif only_catching:
            return catching_list
        else:
            return catching_list, hidden_catcher


    def color_toggle(self, color):

        if type(color) == str:
            if color == 'B':  # black
                return 'W'
            else:  # white
                return 'B'
        else:
            if color == BLACK:
                return WHITE
            else:
                return BLACK


    def bunch(self, grid, color):  # inefficient algorithm up to now

        bunchlist = [grid]
        sur = self.surrounding_grid(bunchlist)

        while True:
            bunchlen = len(bunchlist)

            for point in sur:
                if self.is_placed(point) == color:
                    if point not in bunchlist:
                        bunchlist.append(point)

            if len(bunchlist) == bunchlen:
                break
            sur = self.surrounding_grid(bunchlist)

        return bunchlist


    def surrounding_grid(self, grid_list):

        sur = []
        if type(grid_list[0]) != tuple:
            grid_list = [grid_list]

        for grid in grid_list:
            U = (grid[0], grid[1] - 1)
            D = (grid[0], grid[1] + 1)
            L = (grid[0] - 1, grid[1])
            R = (grid[0] + 1, grid[1])

            if 0 not in U and U not in sur:
                sur.append(U)
            if 12 not in D and D not in sur:
                sur.append(D)
            if 0 not in L and L not in sur:
                sur.append(L)
            if 12 not in R and R not in sur:
                sur.append(R)

        return sur


def main():

    batoo = placement()

    while True:
        cmd = raw_input("cmd : ")
        if cmd == 'p':
            grid = list(input("grid : "))
            color = raw_input("color : ")
            batoo.place(grid, color)

        elif cmd == 's':
            break

    while True:
        cmd = raw_input("cmd2 : ")
        if cmd == 'p':
            print batoo.history

        elif cmd == 's':
            break

# main()
