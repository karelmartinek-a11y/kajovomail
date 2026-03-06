import json
from pathlib import Path


def test_openapi_documented():
    payload = json.loads(Path("docs/openapi.json").read_text())
    assert "/api/v1/health/live" in payload["paths"]
    assert "/api/v1/auth/login" in payload["paths"]
