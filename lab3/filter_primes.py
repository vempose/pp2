def is_prime(num: int) -> bool:
    for i in range(2, num-1):
        if num % i == 0:
            break
    else:
        return True
    return False

numbers = [1, 2, 84, 12, 451, 5, 7, 6]
prime_numbers = list(filter(lambda x: is_prime(x), numbers))
print(prime_numbers)