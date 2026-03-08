from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Account:
    id: str
    provider: str
    provider_type: str
    email: str
    display_name: Optional[str] = None
    capability_flags: List[str] = ()

@dataclass
class Folder:
    id: str
    name: str
    account_id: str
    is_system: bool = False
    parent_id: Optional[str] = None

@dataclass
class Message:
    id: str
    subject: str
    sender: str
    folder_id: str
    snippet: Optional[str] = None
    body: Optional[str] = None
    created_at: Optional[str] = None
    flags: List[str] = ()

@dataclass
class Offer:
    thread_id: str
    title: str
    state: str
    message_id: Optional[str]

@dataclass
class AIResponse:
    summary: str
    html_preview: str
    policy: str
