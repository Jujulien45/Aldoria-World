import pygame
from typing import Protocol

class Drawable(Protocol):
    rect: pygame.Rect
    centery: float
    image: pygame.Surface
    layer: int