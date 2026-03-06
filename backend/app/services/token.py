from fastapi import Header, HTTPException, Security
from typing import Optional


def get_request_correlation_id(x_correlation_id: Optional[str] = Header(None)) -> str:
    if not x_correlation_id:
        raise HTTPException(status_code=400, detail="Missing X-Correlation-ID")
    return x_correlation_id
