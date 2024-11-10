from random import randint


def update_config(nums: int, thao: float, radius: float):
    print(nums, thao, radius)
    return nums, thao, radius


def new_states(nums: int):
    return [(randint(10, 700), randint(10, 700)) for _ in range(nums)]
