import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.block_scheme.connections.output_connection import \
    OutputConnection
from source_code.windows.base_game_window import BaseGameWindow


class NotBlock(BaseBlock):
    def __init__(self, base_game_window: BaseGameWindow,
                 rect: pygame.rect.Rect):
        super().__init__(base_game_window, 'not', rect, [
            InputConnection(base_game_window, self, (50, 100))
        ], [OutputConnection(base_game_window, self, (50, 0))])

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('NotBlock')

    def __copy__(self):
        new_block = NotBlock(self.base_game_window, self.rect)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block
