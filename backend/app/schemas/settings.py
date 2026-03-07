from pydantic import BaseModel


class AISettingsResponse(BaseModel):
    has_openai_api_key: bool
    openai_api_key_masked: str | None = None
    response_style: str
    model: str | None = None


class AISettingsUpdate(BaseModel):
    openai_api_key: str | None = None
    response_style: str | None = None
    model: str | None = None


class AIKeyTestRequest(BaseModel):
    openai_api_key: str | None = None


class AIKeyTestResponse(BaseModel):
    valid: bool
    message: str
    models: list[str] = []


class AIModelsResponse(BaseModel):
    models: list[str]
