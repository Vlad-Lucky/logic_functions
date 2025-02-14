import math
import pygame
from typing import List, Union, Callable
from source_code.block_scheme.blocks.builder_base_block import BuilderBaseBlock
from source_code.block_scheme.connections.builder_base_connection import \
    BuilderBaseConnection
from source_code.constants import BLOCKS_COLOR, BLOCKS_NAME_COLOR, \
    BLOCKS_INDENT_FOR_RESIZING, BLOCKS_WIDTH, BLOCK_MIN_SIZE, \
    BLOCK_TEXT_MAX_SIZE, BLOCK_TEXT_MIN_SIZE, FONT_NAME
from source_code.windows.builder_base_game_window import BuilderBaseGameWindow


class BaseBlock(BuilderBaseBlock):
    def __init__(self, base_game_window: BuilderBaseGameWindow,
                 name: str, rect: pygame.rect.Rect,
                 signal_action: Callable[
                     [List[bool]], List[bool]],
                 inputs: List[BuilderBaseConnection],
                 outputs: List[BuilderBaseConnection],
                 img: Union[str, pygame.Surface] = None):
        super().__init__(base_game_window, name, rect, signal_action,
                         inputs, outputs, img)
        self.update_output_signals()

    def zoom(self, koof: int) -> None:
        new_size_koof = min(max(self.size_koof + koof, 0), int(math.log(BLOCK_TEXT_MAX_SIZE // BLOCK_TEXT_MIN_SIZE, 2)))
        if new_size_koof == self.size_koof + koof:
            self.size_koof += koof
            self.rect.x *= 2 ** koof
            self.rect.y *= 2 ** koof
            self.rect.w *= 2 ** koof
            self.rect.h *= 2 ** koof

    def move(self, x_dif: int, y_dif: int) -> None:
        self.rect = self.rect.move(x_dif, y_dif)

    def is_selected(self) -> bool:
        return self.rect.collidepoint(*pygame.mouse.get_pos())

    def resize(self, w_dif: int, h_dif: int) -> None:
        dif = (w_dif + h_dif) // 2
        if not ((self.rect.w + dif >= BLOCK_MIN_SIZE[0] or dif >= 0) and
                (self.rect.h + dif >= BLOCK_MIN_SIZE[1] or dif >= 0)):
            return
        self.rect.w = max(BLOCK_MIN_SIZE[0], self.rect.w + dif)
        self.rect.h = max(BLOCK_MIN_SIZE[1], self.rect.h + dif)

    def render(self, screen: pygame.Surface) -> None:
        if self.img is None:
            pygame.draw.rect(screen, BLOCKS_COLOR, self.rect,
                             width=BLOCKS_WIDTH)

            font = pygame.font.Font(FONT_NAME, BLOCK_TEXT_MIN_SIZE *
                                    (2 ** self.size_koof))
            widget = font.render(self.name, True, BLOCKS_NAME_COLOR)
            font_rect = widget.get_rect()
            font_rect.center = self.rect.center
            screen.blit(widget, font_rect)
        else:
            img = pygame.transform.smoothscale(self.img, self.rect.size)
            screen.blit(img, self.rect.topleft)

        for connection in self.inputs + self.outputs:
            connection.render(screen)

    def mouse_down(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        for connection in self.inputs + self.outputs:
            connection.mouse_down()

        if self.connection_editing is None and self.is_selected():
            res_ind = BLOCKS_INDENT_FOR_RESIZING
            usl1 = self.rect.top <= mouse_pos[1] <= self.rect.top + res_ind
            usl2 = (self.rect.bottom >= mouse_pos[1] >= self.rect.bottom -
                    res_ind)
            usl3 = self.rect.left <= mouse_pos[0] <= self.rect.left + res_ind
            usl4 = self.rect.right <= mouse_pos[0] >= self.rect.right - res_ind
            if usl1 or usl2 or usl3 or usl4:
                self.is_resizing = True
            else:
                self.is_dragging = True
            self.last_mouse_pos = mouse_pos

    def mouse_motion(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        if self.connection_editing is not None:
            return

        if self.is_dragging:
            # использую замысловатые методы вместо pygame.mouse.get_rel(),
            # потому что pygame.mouse.get_rel() при первом обращении
            # выдаёт всё неправильное
            self.move(mouse_pos[0] - self.last_mouse_pos[0],
                      mouse_pos[1] - self.last_mouse_pos[1])
            self.last_mouse_pos = mouse_pos
        elif self.is_resizing:
            koof = None
            if (mouse_pos[0] - self.last_mouse_pos[0] >=
                    self.rect.w * 2 - self.rect.w or
                    mouse_pos[1] - self.last_mouse_pos[1] >=
                    self.rect.h * 2 - self.rect.h):
                koof = 1
            elif (mouse_pos[0] - self.last_mouse_pos[0] <=
                    self.rect.w // 2 - self.rect.w or
                    mouse_pos[1] - self.last_mouse_pos[1] <=
                    self.rect.h // 2 - self.rect.h):
                koof = -1
            if koof is not None:
                new_size_koof = min(max(self.size_koof + koof, 0),
                                    math.log(BLOCK_TEXT_MAX_SIZE //
                                             BLOCK_TEXT_MIN_SIZE, 2))
                if new_size_koof == self.size_koof + koof:
                    self.size_koof += koof
                    self.rect.w *= 2 ** koof
                    self.rect.h *= 2 ** koof
                    self.last_mouse_pos = mouse_pos

    def mouse_up(self) -> None:
        for connection in self.inputs + self.outputs:
            connection.mouse_up()

        if self.connection_editing is not None:
            return

        self.is_resizing = False
        self.is_dragging = False
        self.last_mouse_pos = None

        self.eliminate_collider_intersection()

    def is_intersected(self) -> bool:
        for collide_rect in self.base_game_window.all_blocks:
            if self.rect is not collide_rect.rect and \
                    self.rect.colliderect(collide_rect.rect):
                return True
        return False

    def eliminate_collider_intersection(self, saving_last_rect: bool = True):
        if self.is_intersected():
            self.rect = self.last_rect.copy()
            self.size_koof = int(math.log(self.rect.w // BLOCK_MIN_SIZE[0], 2))
        if saving_last_rect:
            self.last_rect = self.rect.copy()

    def update_output_signals(self):
        if any(self.inputs) and any(self.outputs):
            signal = self.signal_action([inp.signal for inp in self.inputs])
            for output_id, output_con in enumerate(self.outputs):
                output_con.signal = signal[output_id]

    def delete(self) -> None:
        for connection in self.inputs + self.outputs:
            while len(connection.attached_connections) > 0:
                attached_connection = connection.attached_connections[-1]
                connection.detach(attached_connection)
        del self.base_game_window.all_blocks[
            self.base_game_window.all_blocks.index(self)]

    def copy(self):
        return self.__copy__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self, header: str = 'BaseBlock'):
        ans = f'{header}({self.name},{self.rect}'
        for connection in self.inputs + self.outputs:
            ans += f',{connection}'
        return ans + ')'

    def __copy__(self):
        new_block = BaseBlock(self.base_game_window, self.name, self.rect,
                              [input_.copy() for input_ in self.inputs],
                              [output_.copy() for output_ in self.outputs])
        for connection in new_block.inputs + new_block.outputs:
            connection.parent_block = new_block
        return new_block
