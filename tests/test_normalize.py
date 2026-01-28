from matching_logic.core.normalize import normalize_name

def test_normalize_uppercase():
    assert normalize_name("motor housing") == "MOTOR HOUSING"

def test_normalize_trim():
    assert normalize_name("  motor housing  ") == "MOTOR HOUSING"
