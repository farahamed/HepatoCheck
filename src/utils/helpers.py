"""
Helper Functions
"""

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers."""
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return default
