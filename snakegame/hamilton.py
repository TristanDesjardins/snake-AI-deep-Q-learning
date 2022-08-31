# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 18:09:02 2022

@author: X2029440
"""

import random
import enum

class From(enum.Enum):
    NOWHERE = 1
    NORTH = 2
    EAST = 3
    SOUTH = 4
    WEST = 5

class Hamiltonian:

    def __init__(self, width: int, height: int, start: tuple = (0, 0)):
        self.arcs = {From.NORTH: (0, -1), From.SOUTH: (0, 1), From.EAST: (1, 0), From.WEST: (-1, 0)}
        self.width = width
        self.height = height
        self.start = start
        self.grid = {(i, j): self._zig_zag(i, j) for i in range(width) for j in range(height)}
        self.grid[start] = From.NOWHERE
        self.curr_loop = []

    def generate(self, count: int = 100):
        for i in range(count):
            sp = self._split_grid()
            self._modify_path(sp)
            tu = self._mend_grid(sp)
            self._modify_path(tu)

    def _modify_path(self, spl):
        pt_a, pt_b = spl
        pta, ptb = self.grid[pt_a], self.grid[pt_b]
        orientation = pta
        if orientation in [From.NORTH, From.SOUTH]:
            if pt_a[0] < pt_b[0]:
                pta, ptb = From.EAST, From.WEST
            else:
                pta, ptb = From.WEST, From.EAST
        else:
            if pt_a[1] < pt_b[1]:
                pta, ptb = From.SOUTH, From.NORTH
            else:
                pta, ptb = From.NORTH, From.SOUTH
        self.grid[pt_a] = pta
        self.grid[pt_b] = ptb

    def _move(self, pt) -> [tuple, None]:
        if pt in self.grid and self.grid[pt] != From.NOWHERE:
            (x, y), (dx, dy) = pt, self.arcs[self.grid[pt]]
            if (x + dx, y + dy) in self.grid:
                return x + dx, y + dy
        return None

    def _set_loop(self, start, stop):
        self.curr_loop = []
        point = start
        while point and len(self.curr_loop) <= len(self.grid) and point != stop and self.grid[point] != From.NOWHERE:
            point = self._move(point)
            self.curr_loop.append(point)
        return point == stop

    def _split_grid(self) -> tuple:
        candidates = []
        for pt, dx in self.grid.items():
            x, y = pt
            if dx == From.NORTH:
                cx = (x+1, y - 1)
                if cx in self.grid and self.grid[cx] == From.SOUTH:
                    candidates.append((pt, cx))
            elif dx == From.SOUTH:
                cx = (x+1, y + 1)
                if cx in self.grid and self.grid[cx] == From.NORTH:
                    candidates.append((pt, cx))
            elif dx == From.EAST:
                cx = (x + 1, y + 1)
                if cx in self.grid and self.grid[cx] == From.WEST:
                    candidates.append((pt, cx))
            elif dx == From.WEST:
                cx = (x - 1, y + 1)
                if cx in self.grid and self.grid[cx] == From.EAST:
                    candidates.append((pt, cx))
        if len(candidates) > 0:
            start, end = random.choice(candidates)
            if self._set_loop(start, end):
                return start, end
            elif not self._set_loop(end, start):
                raise Exception('Cannot split. Loop failed.')
            return end, start

    def _mend_grid(self, sp):
        candidates = []
        for pt, dx in self.grid.items():
            (x, y), lx = pt, pt in self.curr_loop
            if dx == From.NORTH:
                cx = (x+1, y - 1)
                rx = cx in self.curr_loop
                if cx in self.grid and self.grid[cx] == From.SOUTH and rx != lx:
                    candidates.append((pt, cx))
            elif dx == From.SOUTH:
                cx = (x+1, y + 1)
                rx = cx in self.curr_loop
                if cx in self.grid and self.grid[cx] == From.NORTH and rx != lx:
                    candidates.append((pt, cx))
            elif dx == From.EAST:
                cx = (x + 1, y + 1)
                rx = cx in self.curr_loop
                if cx in self.grid and self.grid[cx] == From.WEST and rx != lx:
                    candidates.append((pt, cx))
            elif dx == From.WEST:
                cx = (x - 1, y + 1)
                rx = cx in self.curr_loop
                if cx in self.grid and self.grid[cx] == From.EAST and rx != lx:
                    candidates.append((pt, cx))
        a, b = sp
        if (a, b) in candidates:
            candidates.remove((a, b))
        elif (b, a) in candidates:
            candidates.remove((b, a))
        if len(candidates) > 0:
            return random.choice(candidates)
        else:
            return sp

    def _zig_zag(self, x: int, y: int) -> From:
        even = y % 2 == 0
        if (x == 0 and even) or (x == self.width - 1 and not even):
            return From.NORTH
        return From.WEST if even else From.EAST

    def print_path(self):
        result_str = ''
        for y in range(self.height):
            for x in range(self.width):
                if (self.grid[x, y] == From.NORTH) or ((y > 0) and (self.grid[x, y - 1] == From.SOUTH)):
                    result_str = result_str + ' |'
                else:
                    result_str = result_str + '  '
            result_str = result_str + ' \n'
            for x in range(self.width):
                if (self.grid[x, y] == From.WEST) or ((x > 0) and (self.grid[x - 1, y] == From.EAST)):
                    result_str = result_str + '-O'
                else:
                    result_str = result_str + ' O'
            result_str = result_str + ' \n'
        print(result_str)


if __name__ == '__main__':
    h = Hamiltonian(10, 20)
    h.generate(500)
    h.print_path()