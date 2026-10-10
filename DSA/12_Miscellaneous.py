from typing import List


def find_plate(n: int) -> str:  # Example: n = 1_000_000
    for letter_count in range(6):  # Try 0, 1, 2, 3, 4, or 5 letters

        digit_count = 5 - letter_count
        # letter_count = 0 → digit_count = 5
        # letter_count = 1 → digit_count = 4
        # letter_count = 2 → digit_count = 3

        numbers_per_suffix = 10**digit_count
        # 5 digits → 10^5 = 100,000
        # 4 digits → 10^4 = 10,000
        # 3 digits → 10^3 = 1,000

        group_size = numbers_per_suffix * (26**letter_count)
        # 5 digits + 0 letters → 100,000 × 1   = 100,000
        # 4 digits + 1 letter  → 10,000 × 26  = 260,000
        # 3 digits + 2 letters → 1,000 × 676  = 676,000

        if n >= group_size:
            # 1,000,000 >= 100,000 → skip 5-digit group
            # 900,000 >= 260,000   → skip 1-letter group
            # 640,000 < 676,000    → answer is in 2-letter group

            n -= group_size
            # After first group:  1,000,000 - 100,000 = 900,000
            # After second group:   900,000 - 260,000 = 640,000

            continue  # Move to the next plate format

        number = n % numbers_per_suffix
        # 640,000 % 1,000 = 0

        letter_value = n // numbers_per_suffix
        # 640,000 // 1,000 = 640

        letters: List[str] = []  # We will build the letters here

        for _ in range(letter_count):  # Run 2 times because letter_count = 2

            remainder = letter_value % 26
            # First iteration:  640 % 26 = 16
            # Second iteration: 24 % 26 = 24

            letter = chr(ord("A") + remainder)
            # 16 → Q because A=0, B=1, ..., Q=16
            # 24 → Y because A=0, B=1, ..., Y=24

            letters.append(letter)
            # First iteration:  letters = ["Q"]
            # Second iteration: letters = ["Q", "Y"]

            letter_value //= 26
            # First iteration:  640 // 26 = 24
            # Second iteration: 24 // 26 = 0

        letters.reverse()
        # ["Q", "Y"] becomes ["Y", "Q"]

        number_part = str(number).zfill(digit_count)
        # number = 0
        # str(number) = "0"
        # digit_count = 3
        # "0".zfill(3) = "000"

        letter_part = "".join(letters)
        # ["Y", "Q"] becomes "YQ"

        return number_part + letter_part
        # "000" + "YQ" = "000YQ"

    raise ValueError("Number is too large")  # n is beyond ZZZZZ


def minimum_water(matrix: List[List[int]], a: int) -> float:  # Example: 4 × 4 matrix, a = 2
    m = len(matrix)
    # Number of rows = 4

    n = len(matrix[0])
    # Number of columns = 4

    col_sums = [0] * n
    # Initially: [0, 0, 0, 0]

    # Add the first `a` rows
    for row in range(a):  # row = 0, 1

        for col in range(n):  # col = 0, 1, 2, 3

            col_sums[col] += matrix[row][col]

            # After adding row 0:
            # [1, 2, 8, 9]

            # After adding row 1:
            # [1+3, 2+4, 8+7, 9+6]
            # [4, 6, 15, 15]

    answer: float = float("inf")
    # answer = infinity

    # Possible top rows: 0, 1, 2
    for top in range(m - a + 1):

        current_sum: int = sum(col_sums[:a])
        # top = 0: 4 + 6   = 10
        # top = 1: 12 + 12 = 24
        # top = 2: 16 + 14 = 30

        answer: float = min(answer, current_sum)
        # top = 0: min(infinity, 10) = 10
        # top = 1: min(10, 24) = 10
        # top = 2: min(10, 30) = 10

        # Move the square toward the right
        for right in range(a, n):  # right = 2, 3

            current_sum -= col_sums[right - a]
            # Remove the column leaving the square

            current_sum += col_sums[right]
            # Add the new column entering the square

            # When top = 0:
            # right = 2: 10 - 4 + 15 = 21
            # right = 3: 21 - 6 + 15 = 30

            # When top = 1:
            # right = 2: 24 - 12 + 8 = 20
            # right = 3: 20 - 12 + 8 = 16

            # When top = 2:
            # right = 2: 30 - 16 + 4 = 18
            # right = 3: 18 - 14 + 6 = 10

            answer: float = min(answer, current_sum)
            # Keep the smallest sum found so far

        if top + a < m:
            # top = 0: 0 + 2 < 4 → update
            # top = 1: 1 + 2 < 4 → update
            # top = 2: 2 + 2 < 4 → do not update

            for col in range(n):

                col_sums[col] -= matrix[top][col]
                # Remove the old top row

                col_sums[col] += matrix[top + a][col]
                # Add the new bottom row

            # After top = 0:
            # Remove [1, 2, 8, 9]
            # Add    [9, 8, 1, 2]
            # col_sums = [12, 12, 8, 8]

            # After top = 1:
            # Remove [3, 4, 7, 6]
            # Add    [7, 6, 3, 4]
            # col_sums = [16, 14, 4, 6]

    return answer
    # Minimum 2 × 2 sum = 10
