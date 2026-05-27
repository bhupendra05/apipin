# apipin

> **Snapshot third-party API responses. Know when they silently change shape**

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/apipin)](https://pypi.org/project/apipin)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Install

```bash
pip install apipin
```

## The problem

Third-party APIs change their response shape without warning. The `user.email` field that worked for a year disappears in a silent breaking change. You find out when your app crashes in production.

## Usage

```python
import requests
from apipin import apipin

# First call: saves the response schema to .apipin/github_user.json
resp = requests.get("https://api.github.com/users/torvalds").json()
apipin("github_user", resp)

# All subsequent calls: validates the schema matches
resp = requests.get("https://api.github.com/users/torvalds").json()
apipin("github_user", resp)  # silent if schema matches

# When GitHub removes a field:
# UserWarning: apipin: DRIFT in 'github_user':
#   • .blog: key missing in actual response
```

### Raise instead of warn

```python
apipin("payment_api", stripe_response, action="raise")
# Raises ApiPinError on any schema change
```

### In tests

```python
def test_github_api_contract():
    resp = requests.get("https://api.github.com/users/torvalds").json()
    apipin("github_user", resp, action="raise", snapshot_dir="test_fixtures")
```

## Architecture

```
apipin/
├── apipin/
│   ├── __init__.py   # public API
│   └── *.py          # core implementation
└── tests/
    └── test_*.py     # 3 passed — no API key needed
```

## License

MIT © [bhupendra05](https://github.com/bhupendra05)

---

*Part of the [bhupendra05 developer tools collection](https://github.com/bhupendra05)*
