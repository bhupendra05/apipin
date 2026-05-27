import pytest
from apipin import apipin, ApiPinError

def test_first_call_pins(tmp_path):
    apipin("test_api", {"name": "Alice", "age": 30}, snapshot_dir=tmp_path, action="raise")
    assert (tmp_path / "test_api.json").exists()

def test_matching_schema_passes(tmp_path):
    apipin("t", {"x": 1}, snapshot_dir=tmp_path)
    apipin("t", {"x": 99}, snapshot_dir=tmp_path, action="raise")  # same shape, different value

def test_drift_raises(tmp_path):
    apipin("drift", {"name": "Alice"}, snapshot_dir=tmp_path)
    with pytest.raises(ApiPinError):
        apipin("drift", {"name": "Bob", "new_field": "surprise"}, snapshot_dir=tmp_path, action="raise")
