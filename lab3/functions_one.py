def grams_to_ounces(grams: float) -> float:
    return 28.3495231 * grams


def fahrenheit_to_celsius(F: float) -> float:
    return ((5 / 9) * (F - 32))


def solve(numheads: int, numlegs: int) -> dict[str: int]:
    rabbits, chickens = 0, 0
    while (numheads % (numlegs/2) != 0):
        rabbits += 1
        numlegs -= 4
        numheads -= 1
    chickens = numheads
    return {"Rabbits": rabbits, "Chickens": chickens}


def filter_prime(nums: list[int]) -> list[int]:
    primes = []
    for num in nums:
        for i in range(2, num-1):
            if num % i == 0:
                break
        else:
            primes.append(num)
    return primes


def perms_of_string(s: str) -> None:
    for perm in permutations(s):
        print(*perm, sep="")


def reverse_sentence(s: str) -> str:
    return " ".join(s.split()[::-1])


def has_33(nums: list[int]) -> bool:
    i = 0
    while i <= len(nums)-2:
        if nums[i] == nums[i+1]:
            return True
        i += 1
    return False


def spy_game(nums: list[int]) -> bool:
    nums = str(list(filter(lambda x: x in [0, 7], nums)))
    return True if "0, 0, 7" in nums else False


def sphere_volume(radius: float) -> float:
    return (4/3) * radius**3 * 3.14


def get_unique(nums: list[int]) -> list[int]:
    uniques = []
    for num in nums:
        if num not in uniques:
            uniques.append(num)
    return uniques


def is_palindrome(s: str) -> bool:
    for i in range(0, len(s)//2):
        if s[i] != s[-i-1]:
            return False
    return True


def histogram(data: list[int]) -> None:
    for line in data:
        print("*" * line)


def guess_the_number_game():
    name = input("Hello! What is your name?\n")
    print("\nWell, KBTU, I am thinking of a number between 1 and 20.")

    aim = randint(1, 20)
    guesses = 0

    while True:
        user_input = int(input("Take a guess.\n"))
        guesses += 1
        print()
        if user_input < aim:
            print("Your guess is too low.")
        elif user_input > aim:
            print("Your guess is too hight.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break