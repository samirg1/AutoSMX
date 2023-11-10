from random import randrange


def rand_hex(n: int) -> str:
    return f"{randrange(16**n):0{n}x}".upper()