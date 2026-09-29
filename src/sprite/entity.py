from __future__ import annotations
from typing import TYPE_CHECKING
from src.sprite.drawable import Drawable
import math

if TYPE_CHECKING:
    from src.sprite.static_body import StaticBody

import pygame


class Entity(pygame.sprite.Sprite, Drawable):
    def __init__(
            self,
            midbottom: pygame.Vector2 | tuple[float, float],
            collider_size: tuple[int, int],
            hitbox_size: tuple[int, int] |None = None,
            mass: float = 1,
            collide_tiles: bool = True
        ):
        super().__init__()
        self.mass = mass
        self.collide_tiles = collide_tiles


        self.collider = pygame.FRect((0, 0), collider_size)
        self.collider.midbottom = midbottom

        if hitbox_size is not None:
            self.hitbox = pygame.FRect((0, 0), hitbox_size)
        else:
            self.hitbox = pygame.FRect((0, 0), collider_size)
        self.hitbox.midbottom = midbottom


        self.velocity = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self._force = pygame.Vector2(0.0, 0.0)
        self.moving = False
        self.layer = 0

    @property
    def centery(self):
        return self.rect.centery

    def apply_force(self, force: pygame.Vector2):
        self._force += force

    def solve_collision(self, delta_time: float, static_bodies: list[StaticBody]):
        # x check
        x_movement: float = self.velocity.x * delta_time

        x_projected_rect: pygame.FRect = self.collider.copy()
        x_projected_rect.x += self.velocity.x * delta_time


        # y check
        y_movement: float = self.velocity.y * delta_time

        y_projected_rect: pygame.FRect = self.collider.copy()
        y_projected_rect.y += self.velocity.y * delta_time


        for static_body in static_bodies:
            collider = static_body.collider
            if x_projected_rect.colliderect(collider):
                # positive dir
                if self.velocity.x > 0:
                    x_contact_distance: float = collider.left - self.collider.right
                    x_movement = min(x_movement, x_contact_distance, key=abs)

                elif self.velocity.x < 0:
                    x_contact_distance: float = collider.right - self.collider.left
                    x_movement = min(x_movement, x_contact_distance, key=abs)


            if y_projected_rect.colliderect(collider):
                # positive dir
                if self.velocity.y > 0:
                    y_contact_distance: float = collider.top - self.collider.bottom
                    y_movement = min(y_movement, y_contact_distance, key=abs)

                elif self.velocity.y < 0:
                    y_contact_distance: float = collider.bottom - self.collider.top
                    y_movement = min(y_movement, y_contact_distance, key=abs)


        return x_movement, y_movement


    def update(self, delta_time: float, collision_tiles: list[StaticBody]):
        self.velocity += self._force

        # This looks weird I know, but it's actually the right way to do it
        self.velocity += self.acceleration * 0.5 * delta_time
        if self.collide_tiles:
            x_movement, y_movement = self.solve_collision(delta_time, collision_tiles)
            self.velocity.x = x_movement
            self.velocity.y = y_movement

        self.collider.midbottom += self.velocity * delta_time

        self.moving = (math.isclose(self.velocity.x, 0.0, abs_tol=1e-07) and
                       math.isclose(self.velocity.y, 0.0, abs_tol=1e-07))

        self.velocity += self.acceleration * 0.5 * delta_time
        self._force.x = 0
        self._force.y = 0