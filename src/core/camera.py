import pygame
from src.sprite.drawable import Drawable

class Camera:
    def __init__(self, screen_surface: pygame.Surface):
        self.offset = pygame.Vector2(0.0, 0.0)
        self.screen_surface: pygame.Surface = screen_surface
        self.size: tuple[int, int] = screen_surface.get_size()

    @property
    def rect(self):
        return pygame.Rect(self.offset, self.size)

    def set_center(self, center: pygame.Vector2):
        self.offset = center - pygame.Vector2(self.size) / 2

    def world_to_screen(self, position: pygame.Vector2 | tuple[int, int]):
        return -self.offset + position

    def screen_to_world(self, position: pygame.Vector2 | tuple[int, int]):
        return self.offset + position



def draw_sorted(
        screen: pygame.Surface,
        sprites: list[Drawable],
        camera: Camera|None = None,
        key = lambda sprite: (sprite.layer, sprite.centery)
    ):
    for sprite in sorted(sprites, key=key):
        if camera is not None:
            pos = camera.world_to_screen(sprite.rect.topleft)
        else:
            pos = sprite.rect.topleft

        screen.blit(sprite.image, pos)


class CameraGroup(pygame.sprite.Group):
    def draw(self, camera: Camera):
        draw_sorted(camera.screen_surface, self.sprites(), camera)

class UICameraGROUP(pygame.sprite.Group):
    def draw(self, screen):
        draw_sorted(screen, self.sprites())