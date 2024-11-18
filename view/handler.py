from enum import Enum

# def update_config(nums: int, thao: float, radius: float):
#     print(nums, thao, radius)
#     return nums, thao, radius


# def new_states(nums: int):
#     return [(randint(0, 1920), randint(0, 1080)) for _ in range(nums)]


class Creeper:
    def get_state(self):
        pass

    def get_coord(self):
        pass


class Field:
    def __init__(
        self, size_of_field: tuple, creepers_num: float, explosion_radius: int, move_radius: float, func_type=1
    ):
        print(size_of_field, creepers_num, explosion_radius, move_radius)

    def update_field(self):
        pass

    def get_creepers(self) -> list[Creeper]:
        pass


class CreeperState(Enum):
    Born = "Born"
    Hissing = "Hiss"
    Sleep = "Sleep"
    Walk = "Walk"
    Explodes = "Explosion"
