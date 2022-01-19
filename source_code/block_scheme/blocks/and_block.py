import pygame
from source_code.block_scheme.blocks.base_block import BaseBlock
from source_code.block_scheme.connections.input_connection import \
    InputConnection
from source_code.block_scheme.connections.output_connection import \
    OutputConnection
from source_code.constants import BASE_BLOCK_IMAGES_PATH
from source_code.windows.builder_base_game_window import BuilderBaseGameWindow


class AndBlock(BaseBlock):
    def __init__(self, base_game_window: BuilderBaseGameWindow,
                 rect: pygame.rect.Rect):
        img_path = f'{BASE_BLOCK_IMAGES_PATH}/and.png'
        super().__init__(
            base_game_window, 'and', rect,
            lambda inputs: [inputs[0] and inputs[1]], [
                InputConnection(base_game_window, self, (100 // 3, 100)),
                InputConnection(base_game_window, self, (100 // 3 * 2, 100))
            ], [OutputConnection(base_game_window, self, (50, 0))],
            img=img_path)

    def __str__(self):
        return self.__repr__()

    def __repr__(self, *args):
        return super().__repr__('AndBlock')

    def __copy__(self):
        new_block = AndBlock(self.base_game_window, self.rect)
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block
