from backend.app.models.tables import Message


async def seed_message(session, subject, account_id, folder_id, body=""):
    message = Message(subject=subject, account_id=account_id, folder_id=folder_id, body=body)
    session.add(message)
    await session.flush()
    await session.refresh(message)
    return message
