import pygame
from src.sprite.drawable import Drawable


class StaticBody(pygame.sprite.Sprite, Drawable):
    def __init__(
            self,
            midbottom: pygame.Vector2 | tuple[float, float],
            collider_size: tuple[int, int],
        ):
        super().__init__()

        self.collider = pygame.FRect((0, 0), collider_size)
        self.collider.midbottom = midbottom
        self.layer = 0

    @property
    def centery(self) -> float:
        return self.collider.centery
