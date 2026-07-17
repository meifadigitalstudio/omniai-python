import secrets

def generate_otp(length: int = 6) -> str:
    minimum = 10 ** (length - 1)
    maximum = (10 ** length) - 1

    return str(
        secrets.randbelow(maximum - minimum + 1) + minimum
    )