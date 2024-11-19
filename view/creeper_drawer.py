import pygame
from creepers import CreeperState, Field


class DrawExplosion:
    def __init__(self, position):
        self.position = position
        self.explosion_frame_index = 0
        self.explosion_timer = pygame.time.get_ticks()

    def _update_frame(self, frame_count):
        timer = 100
        if pygame.time.get_ticks() - self.explosion_timer > timer:  # 100 ms between frames
            self.explosion_frame_index += 1
            self.explosion_timer = pygame.time.get_ticks()
        return self.explosion_frame_index > frame_count

    def __call__(self, drawer):
        if not drawer.image.explosion_frames(len(drawer.image.explosion_frames)):
            return False
        drawer.screen.blit(drawer.image.explosion_frames[self.explosion_frame_index], self.position)


class CreeperDrawer:
    def __init__(self, position: tuple[float, float], state: CreeperState):
        self.cur_x, self.cur_y = position
        self.state = state
        self.target_x, self.target_y = position
        self.steps_left = 0

    def update(self, new_position: tuple[float, float], state: CreeperState, steps):
        self.state = state
        if state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
            steps = 0
        elif state == CreeperState.Sleep:
            steps = 0
        self.target_x, self.target_y = new_position
        self._set_target(steps)

    def _set_target(self, steps):
        self.steps_left = steps
        if not steps:
            return
        self.dx = (self.target_x - self.cur_x) / steps
        self.dy = (self.target_y - self.cur_y) / steps

    def update_position(self):
        if self.steps_left > 0:
            self.cur_x += self.dx
            self.cur_y += self.dy
            self.steps_left -= 1
        return self.steps_left > 0

    def draw_step(self, drawer):
        if not self.update_position():
            drawer.register_callback_animation(DrawExplosion((self.target_x, self.target_y)))
            return

        if self.state in {CreeperState.Walk, CreeperState.Explodes}:
            drawer.screen.blit(drawer.images.creeper_image_walk, (self.cur_x, self.cur_y))
        elif self.state == CreeperState.Born:
            drawer.screen.blit(drawer.images.creeper_image_born, (self.cur_x, self.cur_y))
        elif self.state == CreeperState.Sleep:
            drawer.screen.blit(drawer.images.creeper_image_sleep, (self.cur_x, self.cur_y))
        elif self.state == CreeperState.Hissing:
            drawer.screen.blit(drawer.images.creeper_image_hiss, (self.cur_x, self.cur_y))


class CreepersManager:
    def __init__(self, app, position_shift):
        self.field = Field(
            (app.width, app.height),
            creepers_num=app.creeper_count,
            explosion_radius=app.radius_explosion,
            move_radius=app.radius,
            dist_func=app.dist_func,
        )
        self.shift = position_shift
        self.creepers = [CreeperDrawer(coord, state) for coord, state in self._creepers2data(self.field.get_creepers())]

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps):
        self.field.update_field()
        for drawers, (coord, state) in zip(self.creepers, self._creepers2data(self.field.get_creepers())):
            drawers.update(coord, state, steps)

    def draw_creepers(self, drawer):
        for creeper in self.creepers:
            creeper.draw_step(drawer)
