from typing import List, Tuple
from enum import Enum
import pygame
from dataclasses import dataclass
from random import randint
from copy import deepcopy

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 800

NUM_ROWS = 10
NUM_COLS = 10

BORDER_WIDTH = 1

class Color(Enum):
    NULL = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 0, 255)
    CYAN = (0, 255, 255)

    # BORDERS
    YELLOW = (255, 255, 0)
    GRAY = (50, 50, 50)

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    @classmethod
    def get_color(cls, i: int):
        return cls.list()[i]

class IlegalMove(Exception):
    pass


class State:
    IDLE = 1
    SELECTED = 2

class GameEngine:

    def __init__(self, screen, height: int, width: int, rows: int, cols: int):
        self.screen = screen
        self.height = height
        self.width = width
        self.rows = rows
        self.cols = cols

        self.h_spacing = int(self.height / self.rows)
        self.v_spacing = int(self.width / self.cols)

        self.matrix: List[List[bool]] = []
        for i in range(self.rows):
            self.matrix.append([])
            for j in range(self.cols):
                self.matrix[i].append(False)

        self.paint()
        self.run = False

    def _find(self, click: Tuple[int,int]) -> Tuple[int,int]:
        return (int(click[0] / self.h_spacing), int(click[1] / self.v_spacing))

    def _get_block_screen_coordinates(self, position: Tuple[int, int]) -> Tuple[int,int]:
        return (self.h_spacing * position[0], self.v_spacing * position[1])

    def _toggle_index(self, position: Tuple[int, int]):
        self.matrix[position[0]][position[1]] ^= True

    def paint(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = Color.GREEN if self.matrix[i][j] else Color.NULL
                coordinates = self._get_block_screen_coordinates((i,j))

                # Paint block
                pygame.draw.rect(self.screen, color.value, (coordinates[0], coordinates[1], self.h_spacing, self.v_spacing))
                # Draw border
                pygame.draw.rect(self.screen, Color.GRAY.value, (coordinates[0], coordinates[1], self.h_spacing, self.v_spacing), BORDER_WIDTH)

    def paint_block(self, position: Tuple[int, int]):
        color = Color.GREEN if self.matrix[position[0]][position[1]] else Color.NULL
        coordinates = self._get_block_screen_coordinates(position)
        # Paint block
        pygame.draw.rect(self.screen, color.value, (coordinates[0], coordinates[1], self.h_spacing, self.v_spacing))
        # Draw border
        pygame.draw.rect(self.screen, Color.GRAY.value, (coordinates[0], coordinates[1], self.h_spacing, self.v_spacing), BORDER_WIDTH)

    def paint_border(self):
        # Draw border
        color = Color.WHITE if self.run else Color.NULL
        pygame.draw.rect(self.screen, color.value, (0, 0, self.width, self.height), BORDER_WIDTH)


    def handle(self, click: Tuple[int,int]):
        print(f"Click {click}")

        position = self._find(click=click)
        self._toggle_index(position=position)
        self.paint_block(position=position)


    def toggle_run(self):
        self.run ^= True

    def _get_of_false(self, position: Tuple[int,int]):
        i,j = position
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return False
        return self.matrix[i][j]

    def _get_neighbors(self, position: Tuple[int,int]) -> int:
        i, j = position
        return sum(
            [
                self._get_of_false((i - 1, j - 1)),
                self._get_of_false((i - 1, j)),
                self._get_of_false((i - 1, j + 1)),
                self._get_of_false((i, j - 1)),
                self._get_of_false((i, j + 1)),
                self._get_of_false((i + 1, j - 1)),
                self._get_of_false((i + 1, j)),
                self._get_of_false((i + 1, j + 1)),
            ]
        )

    def execute(self):
        if not self.run:
            return
        print(f"Running")
        changes: List[Tuple[int,int]] = []
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self._get_neighbors((i,j))
                status = self.matrix[i][j]
                change = False

                if neighbors < 2:
                    change = status
                elif neighbors > 3:
                    change = status
                elif neighbors in [2,3] and status:
                    change = False
                elif neighbors == 3 and not status:
                    change = True

                if change:
                    changes.append((i,j))

        # Now lets apply all the changes
        for position in changes:
            self._toggle_index(position=position)
            self.paint_block(position=position)








