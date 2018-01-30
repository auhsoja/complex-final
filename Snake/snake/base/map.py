#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0212

"""Definition of class Map."""

import random
from snake.base.pos import Pos
from snake.base.point import PointType, Point


class Map:
    """2D game map."""

    def __init__(self, num_rows, num_cols):
        """Initialize a Map object."""
        if not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("\'num_rows\' and \'num_cols\' must be integers")
        if num_rows < 5 or num_cols < 5:
            raise ValueError("\'num_rows\' and \'num_cols\' must >= 5")
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__capacity = (num_rows - 2) * (num_cols - 2)
        self.__content = [[Point() for _ in range(num_cols)] for _ in range(num_rows)]
        self.reset()

    def reset(self):
        self.__food = None
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                if i == 0 or i == self.__num_rows - 1 or \
                   j == 0 or j == self.__num_cols - 1:
                    self.__content[i][j].type = PointType.WALL
                else:
                    self.__content[i][j].type = PointType.EMPTY

    def copy(self):
        m_copy = Map(self.__num_rows, self.__num_cols)
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                m_copy.__content[i][j].type = self.__content[i][j].type
        return m_copy

    def point(self, pos):
        """Return a point on the map.

        DO NOT directly modify the point type to PointType.FOOD and vice versa.
        Use {add|rm}_food() methods instead.

        Args:
            pos (base.pos.Pos): The position of the point to be fetched

        Returns:
            snake.point.Point: The point at the given position.

        """
        return self.__content[pos.x][pos.y]

    def is_inside(self, pos):
        return pos.x > 0 and pos.x < self.num_rows - 1 \
               and pos.y > 0 and pos.y < self.num_cols - 1

    def is_empty(self, pos):
        return self.is_inside(pos) and self.point(pos).type == PointType.EMPTY

    def is_safe(self, pos):
        return self.is_inside(pos) and (self.point(pos).type == PointType.EMPTY or \
                                        self.point(pos).type == PointType.FOOD)

    def is_full(self):
        """Check if the map is filled with the snake's bodies."""
        for i in range(1, self.num_rows - 1):
            for j in range(1, self.num_cols - 1):
                t = self.__content[i][j].type
                if t.value < PointType.HEAD_L.value:
                    return False
        return True

    def has_food(self):
        return self.__food is not None

    def rm_food(self):
        if self.has_food():
            self.point(self.__food).type = PointType.EMPTY
            self.__food = None

    def create_food(self, pos):
        self.point(pos).type = PointType.FOOD
        self.__food = pos
        return self.__food

    def create_rand_food(self):
        empty_pos = []
        for i in range(1, self.__num_rows - 1):
            for j in range(1, self.__num_cols - 1):
                t = self.__content[i][j].type
                if t == PointType.EMPTY:
                    empty_pos.append(Pos(i, j))
                elif t == PointType.FOOD:
                    return None  # Stop if food exists
        if empty_pos:
            return self.create_food(random.choice(empty_pos))
        else:
            return None

    @property
    def num_rows(self):
        return self.__num_rows

    @property
    def num_cols(self):
        return self.__num_cols

    @property
    def capacity(self):
        return self.__capacity

    @property
    def food(self):
        return self.__food
