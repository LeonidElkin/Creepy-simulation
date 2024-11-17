from random import randint


def update_config(nums: int, thao: float, radius: float):
    print(nums, thao, radius)
    return nums, thao, radius


def new_states(nums: int):
    return [(randint(0, 1920), randint(0, 1080)) for _ in range(nums)]
