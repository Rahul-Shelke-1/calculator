from calculator.operations import add, subtract, multiply, divide, power
import pytest

def test_add():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_subtract():
    assert subtract(5, 2) == 3

def test_multiply():
    assert multiply(2, 4) == 8

def test_multiply_negative_numbers():
    assert multiply(-2, 4) == -8

def test_divide():
    assert divide(10, 2) == 5

def test_divide_decimal():
    assert divide(5, 2) == 2.5

def test_power(): 
    assert power(2, m=2) == 4

def test_power_zero_exponent(): 
    assert power(5, m=0) == 1

def test_power_one_exponent(): 
    assert power(7, m=1) == 7

def test_power_negative_exponent(): 
    assert power(2, m=-2) == 0.25