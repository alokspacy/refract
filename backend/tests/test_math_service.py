"""Unit tests for math accessibility."""
from app.services.math_service import MathService

def test_fraction_clearspeak():
    svc = MathService()
    expr = svc.to_accessible_math(r"\frac{a}{b}")
    assert "fraction a over b" in expr.spoken_clearspeak
    assert "<math" in expr.mathml

def test_power_and_sqrt():
    svc = MathService()
    expr = svc.to_accessible_math(r"x^2 + \sqrt{y} = 0")
    assert "squared" in expr.spoken_clearspeak
    assert "square root of y" in expr.spoken_clearspeak
    assert "equals 0" in expr.spoken_clearspeak
