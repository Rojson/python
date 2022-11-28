from math import sqrt
from math import floor

def is_prime(number):
    if number > 9223372036854775807:
        return False
    if number < 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    limit = floor(sqrt(number)) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            False

    return True