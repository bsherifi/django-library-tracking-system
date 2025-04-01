import random

rand_list = [random.randint(1, 100) for _ in range(10)]


# Using list comprehension
list_comprehension_below_10 = [num for num in rand_list if num < 10]


# Using filters
def below_ten(num):
    return num < 10

list_comprehension_below_10 = list(filter(below_ten, rand_list))
