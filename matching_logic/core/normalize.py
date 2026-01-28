# def normalize_name(name: str) -> str:
#     return name.strip().upper()

def normalize_name(name: str) -> str:
    # Agreed simplification: UPPERCASE (+ trim)
    return (name or "").strip().upper()
