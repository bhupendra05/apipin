from __future__ import annotations
import json, warnings
from pathlib import Path
from typing import Any

class ApiPinError(Exception):
    pass

_SNAPSHOT_DIR = Path(".apipin")

def _schema_of(data: Any, depth=0) -> Any:
    if isinstance(data, dict):
        return {k: _schema_of(v, depth+1) for k, v in data.items()} if depth < 4 else "object"
    if isinstance(data, list):
        return [_schema_of(data[0], depth+1)] if data else []
    return type(data).__name__

def _diff_schema(expected: Any, actual: Any, path: str = "") -> list[str]:
    diffs = []
    if type(expected) != type(actual):
        diffs.append(f"{path}: expected {type(expected).__name__}, got {type(actual).__name__}")
        return diffs
    if isinstance(expected, dict):
        for k in expected:
            if k not in actual:
                diffs.append(f"{path}.{k}: key missing in actual response")
            else:
                diffs.extend(_diff_schema(expected[k], actual[k], f"{path}.{k}"))
        # Also check for NEW keys in actual not in expected
        for k in actual:
            if k not in expected:
                diffs.append(f"{path}.{k}: new unexpected key in actual response")
    return diffs

def apipin(name: str, data: dict | list, action: str = "warn", snapshot_dir=None) -> dict | list:
    """
    Pin an API response schema. On first call, saves the shape.
    On subsequent calls, validates the response matches the pinned shape.

    ::

        import requests
        from apipin import apipin

        resp = requests.get("https://api.github.com/users/torvalds").json()
        apipin("github_user", resp)   # pins schema on first call
                                       # warns/raises on future calls if shape drifts
    """
    sdir = Path(snapshot_dir or _SNAPSHOT_DIR)
    sdir.mkdir(exist_ok=True)
    snap_file = sdir / f"{name}.json"
    actual_schema = _schema_of(data)
    if not snap_file.exists():
        snap_file.write_text(json.dumps(actual_schema, indent=2))
        print(f"apipin: pinned '{name}' schema ({snap_file})")
        return data
    expected_schema = json.loads(snap_file.read_text())
    diffs = _diff_schema(expected_schema, actual_schema)
    if diffs:
        msg = f"apipin: DRIFT in '{name}':\n" + "\n".join(f"  • {d}" for d in diffs)
        if action == "raise":
            raise ApiPinError(msg)
        elif action == "log":
            import logging; logging.getLogger("apipin").warning(msg)
        else:
            warnings.warn(msg)
    return data
