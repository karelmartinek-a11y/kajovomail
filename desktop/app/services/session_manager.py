from __future__ import annotations

import keyring
from typing import Optional

from desktop.app.services.api_client import ApiClient

class SessionManager:
    SERVICE_NAME = 'KajovoMail Desktop'

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.token_key = 'csrf'
        self.user_key = 'user_email'

    def store_csrf(self, token: str) -> None:
        keyring.set_password(self.SERVICE_NAME, self.token_key, token)
        self.api_client.client.headers['x-csrf-token'] = token

    def restore_csrf(self) -> Optional[str]:
        token = keyring.get_password(self.SERVICE_NAME, self.token_key)
        if token:
            self.api_client.client.headers['x-csrf-token'] = token
        return token

    def store_current_user(self, email: str) -> None:
        keyring.set_password(self.SERVICE_NAME, self.user_key, email)

    def current_user(self) -> Optional[str]:
        return keyring.get_password(self.SERVICE_NAME, self.user_key)

    def clear(self) -> None:
        keyring.delete_password(self.SERVICE_NAME, self.token_key)
        keyring.delete_password(self.SERVICE_NAME, self.user_key)
