"""apipin — Snapshot & validate third-party API responses. Know when they drift."""
from .pin import apipin, ApiPinError
__version__ = "0.1.0"
__all__ = ["apipin", "ApiPinError"]
