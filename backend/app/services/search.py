from sqlalchemy import select, or_, and_, not_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Message


def build_search_clause(query: str):
    tokens = query.split()
    clauses = []
    for token in tokens:
        if token.upper() == "AND":
            continue
        if token.upper() == "OR":
            continue
        if token.upper() == "NOT":
            continue
        if token.startswith('"') and token.endswith('"'):
            clauses.append(Message.subject.ilike(f"%{token.strip('\"')}%"))
        else:
            clauses.append(Message.subject.ilike(f"%{token}%"))
    return and_(*clauses) if clauses else None


async def search_messages(session: AsyncSession, account_id: int, query: str, folder_id: int | None = None, page: int = 1, per_page: int = 20):
    clause = build_search_clause(query)
    q = select(Message).where(Message.account_id == account_id)
    if folder_id:
        q = q.where(Message.folder_id == folder_id)
    if clause is not None:
        q = q.where(clause)
    q = q.order_by(Message.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(q)
    return result.scalars().all()
