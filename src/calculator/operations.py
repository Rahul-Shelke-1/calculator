def add(a: int | float, b: int | float) -> int | float:
    """
    Sum two numbers together.

    Parameters
    ----------
    a : int | float
        The first number to add.
    b : int | float
        The second number to add.

    Returns
    -------
    int | float
        The arithmetic sum of `a` and `b`.
    """
    return a + b


def subtract(a: int | float, b: int | float) -> int | float:
    """
    Subtract one number from another.

    Parameters
    ----------
    a : int | float
        The number to be subtracted from (minuend).
    b : int | float
        The number to subtract (subtrahend).

    Returns
    -------
    int | float
        The difference between `a` and `b`.
    """
    return a - b


def multiply(a: int | float, b: int | float) -> int | float:
    """
    Multiply two numbers together.

    Parameters
    ----------
    a : int | float
        The first number to multiply.
    b : int | float
        The second number to multiply.

    Returns
    -------
    int | float
        The product of `a` and `b`.
    """
    return a * b


def divide(a: int | float, b: int | float) -> float:
    """
    Divide one number by another.

    Parameters
    ----------
    a : int | float
        The dividend.
    b : int | float
        The divisor.

    Returns
    -------
    float
        The quotient resulting from the division.

    Raises
    ------
    ValueError
        If `b` is equal to zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a: int | float, m: int | float) -> int | float:
    """
    Raise a number to a given power.

    Parameters
    ----------
    a : int | float
        The base number.
    m : int | float
        The exponent.

    Returns
    -------
    int | float
        The result of `a` raised to the power of `m`.
    """
    return a**m
