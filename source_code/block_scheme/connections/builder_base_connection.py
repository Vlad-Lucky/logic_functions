from collections import Iterable
from typing import List

import pygame
from abc import abstractmethod
from source_code.constants import BLOCKS_COLOR, \
    CONNECTION_LOCAL_RADIUS_PERCENTAGE
from source_code.py_base import PyObjectBase
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock


class BuilderBaseConnection(PyObjectBase):
    def __init__(self, base_game_window, parent_block,
                 local_coord_percents):
        self.parent_block = parent_block
        self.local_coord_percents = (0, 0)
        self.local_w = 0
        self.attached_connections = []
        self.is_attached_to_cursor = False

        self.base_game_window = base_game_window
        self.local_coord_percents = local_coord_percents
        self.local_radius_percentage = CONNECTION_LOCAL_RADIUS_PERCENTAGE

        self._signal = False

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        pass
