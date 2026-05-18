from uuid import uuid4

from sqlalchemy import insert

from models import Role

from .db import get_session


async def create_roles():
    db = get_session()
    
    session = await db.__anext__()

    admin_role = Role(
        id=uuid4(),
        name='admin',
        level=1
    )

    user_role = Role(
        id=uuid4(),
        name='user',
        level=5
    )

    await session.execute(insert(Role).values([
        admin_role.to_dict(),
        user_role.to_dict()
    ]))