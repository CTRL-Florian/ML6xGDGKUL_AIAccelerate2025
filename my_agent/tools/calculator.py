import logging
from sympy import sympify

logger = logging.getLogger(__name__)

def calculate(expression: str):
    """
    Performs a mathematical calculation on a given expression.

    Parameters:
        expression (str): A mathematical expression as a string, e.g., "12*(5+3)/2" or "sin(pi/4)".

    Returns:
        float or str: The result of the calculation as a numeric value.
                      Returns the string "Invalid expression" if the input cannot be evaluated.

    Notes:
        - Uses sympy.sympify for safe parsing of the expression.
        - Supports standard arithmetic operations (+, -, *, /, power) and functions like sin, cos, log, etc.
    """
    try:
        result = sympify(expression).evalf()
        return float(result)
    except:
        return "Ongeldige expressie"