import sys
import os

# Add the project root (creo-odoo-middleware) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import your function
from matching_logic.core.normalize import normalize_name


# Import the function we want to test
from matching_logic.core.normalize import normalize_name

# Test 1: Check that all letters are converted to uppercase
def test_normalize_uppercase():
    # Input: lowercase text
    # Expected output: all uppercase
    assert normalize_name("motor housing") == "MOTOR HOUSING"

# Test 2: Check that leading/trailing spaces are removed
def test_normalize_trim_spaces():
    # Input: text with extra spaces at start and end
    # Expected output: spaces trimmed, text normalized to uppercase
    assert normalize_name("  Motor Housing  ") == "MOTOR HOUSING"

# Test 3: Check that numbers and special characters are preserved correctly
def test_normalize_keeps_numbers():
    # Input: part name with numbers and lowercase letters
    # Expected output: numbers remain, letters converted to uppercase
    assert normalize_name("M3 x 10") == "M3 X 10"
