import pygame
from creepers import CreeperState, Field

from view.units.Entity import EntityDrawer, entity_within_bounds


class CreeperDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], state: CreeperState):
        super().__init__(position, None, state)  # Используем None для image, будет установлено позже
        self.dx = self.dy = 0
        self.state = state

    def update(self, new_position: tuple[float, float], steps, state=None):
        self.state = state
        if state == CreeperState.Born:
            # Для состояния Born просто устанавливаем текущую позицию и сбрасываем цель
            self.cur_x, self.cur_y = new_position
            self.target_x, self.target_y = new_position
            self.steps_left = 0
        else:
            # Для остальных состояний выполняем обычное обновление
            self.target_x, self.target_y = new_position
            self._set_target(steps)

    def draw_step(self, drawer):
        self.update_position()

        screen_x = self.cur_x * drawer.zoom_level + drawer.offset_x
        screen_y = self.cur_y * drawer.zoom_level + drawer.offset_y

        size = int(20 * drawer.zoom_level)

        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Крипер вне видимой области

        # TODO: когда появится  статус BONK, раскомментировать

        # if self.state == CreeperState.BONK:
        #     image = pygame.transform.scale(drawer.images.creeper_image_bonk, (size, size))
        #     drawer.screen.blit(image, (screen_x, screen_y))
        #     # Рисуем Sparkle над крипером
        #     sparkle_frame_index = (pygame.time.get_ticks() // 100) % len(drawer.images.sparkle_frames)
        #     sparkle_image = pygame.transform.scale(drawer.images.sparkle_frames[sparkle_frame_index], (size, size))
        #     drawer.screen.blit(sparkle_image, (screen_x, screen_y - size))  # Анимация над крипером

        if self.state == CreeperState.Walk:
            image = drawer.images.creeper_image_walk
        elif self.state == CreeperState.Born:
            image = drawer.images.creeper_image_born
        elif self.state == CreeperState.Sleep:
            image = drawer.images.creeper_image_sleep
        elif self.state == CreeperState.Hissing:
            image = drawer.images.creeper_image_hiss
        elif self.state == CreeperState.Explodes:
            image = drawer.images.creeper_image_walk  # Замените на нужное изображение
        else:
            return

        scaled_image = pygame.transform.scale(image, (size, size))
        drawer.screen.blit(scaled_image, (screen_x, screen_y))


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
        self.field.run_update_field()

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps, drawer):
        self.field.wait_update_field()
        for drawers, (coord, state) in zip(self.creepers, self._creepers2data(self.field.get_creepers())):
            # if state == CreeperState.BONK: TODO: Раскоментить когда будет BONK
            # drawers.state = CreeperState.BONK TODO: Раскоментить когда будет BONK
            # else:
            drawers.update(coord, steps, state)
        self.field.run_update_field()

    def draw_creepers(self, drawer):
        # Вычисляем границы видимой области

        for creeper in self.creepers:
            if entity_within_bounds(creeper, drawer):
                creeper.draw_step(drawer)
