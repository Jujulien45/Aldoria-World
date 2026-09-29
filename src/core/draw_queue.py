from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.camera import Camera
import pygame
from dataclasses import dataclass, field


@dataclass
class DrawCommand:
    image: pygame.Surface
    position: pygame.Vector2
    layer: int = 0
    world_space: bool = True  # False for UI/HUD, drawn in screen coords

class DrawQueue:
    def __init__(self):
        self._commands: list[DrawCommand] = []

    def schedule(self, image: pygame.Surface, position: pygame.Vector2, layer=0, world_space=True):
        self._commands.append(DrawCommand(image, position, layer, world_space))

    def flush(self, camera : Camera):
        self._commands.sort(key=lambda c: (c.layer, c.position.y))
        for cmd in self._commands:
            if cmd.world_space:
                pos = camera.world_to_screen(cmd.position)
            else:
                pos = cmd.position

            camera.screen_surface.blit(cmd.image, pos)
        self._commands.clear()