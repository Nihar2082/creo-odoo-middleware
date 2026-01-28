from __future__ import annotations
from dataclasses import dataclass
from matching_logic.core.normalize import normalize_name

@dataclass(frozen=True)
class ModuleConfig:
    module_name: str
    prefix: str

def format_external_id(prefix: str, number: int, revision: str | None = None) -> str:
    base = f"{prefix}_{number:03d}"
    if revision:
        rev = normalize_name(revision)
        return f"{base}_{rev}"
    return base

def resolve_prefix(module_name: str, module_prefix_map: dict[str, str]) -> str:
    key = normalize_name(module_name)
    if key not in module_prefix_map:
        raise ValueError(f"Unknown module '{module_name}'. Add it to MODULE_PREFIX_MAP.")
    return module_prefix_map[key]
