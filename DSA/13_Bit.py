def bit_difference(a: int, b: int) -> int:
    """
    Input: a = 10, b = 20
    Output: 4
    Explanation: When you write them in binary:
    10 = 01010
    20 = 10100
    """

    count = 0

    while a > 0 or b > 0:
        bit_a = a % 2
        bit_b = b % 2

        if bit_a != bit_b:
            count += 1

        a //= 2
        b //= 2

    return count
