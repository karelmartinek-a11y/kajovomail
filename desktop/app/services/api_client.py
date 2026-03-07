from typing import Any, Dict, List, Optional

import httpx

from desktop.app.models import Account, AIResponse, Folder, Message, Offer

class ApiError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details


class ApiClient:
    def __init__(self, base_url: Optional[str] = None):
        if not base_url:
            base_url = "https://mail.hcasc.cz/api/v1"
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(base_url=self.base_url, timeout=15.0)

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            payload = {}
        if response.status_code >= 400:
            raise ApiError(payload.get('message', 'Server error'), payload.get('details'))
        return payload

    def login(self, email: str, password: str) -> Dict[str, Any]:
        response = self.client.post('/session/login', json={'email': email, 'password': password})
        payload = self._handle_response(response)
        csrf = payload.get('csrfToken')
        if csrf:
            self.client.headers['x-csrf-token'] = csrf
        return payload

    def refresh_session(self) -> Dict[str, Any]:
        response = self.client.get('/session/current')
        payload = self._handle_response(response)
        csrf = payload.get('csrfToken')
        if csrf:
            self.client.headers['x-csrf-token'] = csrf
        return payload

    def logout(self) -> None:
        response = self.client.post('/session/logout')
        self._handle_response(response)
        self.client.cookies.clear()

    def accounts(self) -> List[Account]:
        payload = self._handle_response(self.client.get('/accounts'))
        return [Account(**entry) for entry in payload.get('accounts', [])]

    def folders(self, account_id: str) -> List[Folder]:
        payload = self._handle_response(self.client.get(f'/accounts/{account_id}/folders'))
        return [Folder(**entry) for entry in payload.get('folders', [])]

    def messages(self, folder_id: str, limit: int = 50) -> List[Message]:
        payload = self._handle_response(self.client.get(f'/folders/{folder_id}/messages', params={'limit': limit}))
        return [Message(**entry) for entry in payload.get('messages', [])]

    def compose(self, draft: Dict[str, Any]) -> Dict[str, Any]:
        payload = self._handle_response(self.client.post('/drafts/send', json=draft))
        return payload

    def ai_request(self, prompt: str) -> AIResponse:
        payload = self._handle_response(self.client.post('/ai/responses', json={'prompt': prompt}))
        return AIResponse(
            summary=payload.get('summary', ''),
            html_preview=payload.get('htmlPreview', ''),
            policy=payload.get('policy', 'store: false'),
        )

    def get_ai_settings(self) -> Dict[str, Any]:
        return self._handle_response(self.client.get('/settings/ai'))

    def update_ai_settings(
        self, *, openai_api_key: Optional[str] = None, response_style: Optional[str] = None, model: Optional[str] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if openai_api_key is not None:
            payload['openai_api_key'] = openai_api_key
        if response_style is not None:
            payload['response_style'] = response_style
        if model is not None:
            payload['model'] = model
        return self._handle_response(self.client.put('/settings/ai', json=payload))

    def test_openai_key(self, openai_api_key: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if openai_api_key is not None:
            payload['openai_api_key'] = openai_api_key
        return self._handle_response(self.client.post('/settings/ai/test-key', json=payload))

    def list_openai_models(self) -> List[str]:
        payload = self._handle_response(self.client.get('/settings/ai/models'))
        return payload.get('models', [])

    def offers(self) -> List[Offer]:
        payload = self._handle_response(self.client.get('/offers'))
        return [Offer(**entry) for entry in payload.get('offers', [])]

    def cookie_header(self) -> str:
        cookies = self.client.cookies.jar
        return '; '.join(f"{c.name}={c.value}" for c in cookies)
