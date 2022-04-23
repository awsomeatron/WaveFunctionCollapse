import json
import glob
import math
import random

import pygame


class WaveFunction:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.types = self.load_types()
        self.tiles = [[list(self.types.keys()) for _ in range(self.height)] for _ in range(self.width)]

    def observe(self) -> tuple[int, int]:
        lowest_entropy = math.inf
        lowest = []
        for x in range(self.width):
            for y in range(self.height):
                entropy = len(self.tiles[x][y])
                if lowest_entropy > entropy > 1:
                    lowest.clear()
                    lowest_entropy = entropy
                if entropy == lowest_entropy and entropy > 1:
                    lowest.append((x, y))
        if not lowest:
            return -1, -1
        return random.choice(lowest)

    def collapse(self):
        x, y = self.observe()
        if x != -1 and y != -1:
            self.tiles[x][y] = [random.choice(self.tiles[x][y])]
            self.propagate(x, y)

    def propagate(self, x: int, y: int):
        if x > 0:
            self.tiles[x-1][y] = [type_ for type_ in self.tiles[x-1][y]
                                  if self.tiles[x][y][0] in self.types[type_]["neighbours"]]
        if x + 1 < self.width:
            self.tiles[x+1][y] = [type_ for type_ in self.tiles[x+1][y]
                                  if self.tiles[x][y][0] in self.types[type_]["neighbours"]]
        if y > 0:
            self.tiles[x][y-1] = [type_ for type_ in self.tiles[x][y-1]
                                  if self.tiles[x][y][0] in self.types[type_]["neighbours"]]
        if y + 1 < self.height:
            self.tiles[x][y+1] = [type_ for type_ in self.tiles[x][y+1]
                                  if self.tiles[x][y][0] in self.types[type_]["neighbours"]]

    def fill(self, type_: str):
        with open(f"rules/{type_}.json") as file:
            self.types[type_] = json.load(file)
        self.types[type_]['texture'] = pygame.image.load(f"assets/{self.types[type_]['texture']}")
        for x in range(self.width):
            for y in range(self.height):
                if not self.tiles[x][y]:
                    self.tiles[x][y] = [type_]

    @property
    def has_collapsed(self) -> bool:
        return not [None for x in range(self.width) for y in range(self.height) if len(self.tiles[x][y]) > 1]

    def load_types(self) -> dict[str, dict]:
        rules = {}
        for filename in glob.iglob("rules/[!rock]*"):
            with open(filename) as file:
                rules[filename[6:-5]] = json.load(file)
            rules[filename[6:-5]]['texture'] = pygame.image.load(f"assets/{rules[filename[6:-5]]['texture']}")
        return rules

    def draw(self, screen: pygame.Surface):
        width = screen.get_width()/self.width
        height = screen.get_height()/self.height
        for x in range(self.width):
            for y in range(self.height):
                if len(self.tiles[x][y]) == 1:
                    screen.blit(pygame.transform.scale(self.types[self.tiles[x][y][0]]["texture"], (width, height)),
                                pygame.Rect(x*width, y*height, width, height))
