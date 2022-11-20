from math import sqrt
from math import floor

def is_prime(number):
    if number > 9223372036854775807:
        return "Liczba nie może być większa niż 9223372036854775807"
    if number < 1:
        return "Liczba nie może być mniejsza niż 1"
    if number == 2:
        return "Liczba 2 jest liczbą pierwszą"
    if number % 2 == 0:
        return {f"Liczba {number} NIE jest liczbą pierwszą"}
    limit = floor(sqrt(number)) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            return {f"Liczba {number} NIE jest liczbą pierwszą"}

    return {f"Liczba {number} jest liczbą pierwszą"}