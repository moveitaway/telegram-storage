from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.models import User


class UsersCrud:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(User).where((User.telegram_id == telegram_id))
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def persist(self, user: User) -> User:
        if user.id is not None:
            return await self._update(user)

        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        return user

    async def _update(self, user: User) -> User:
        query = (
            update(User)
                .where(User.id == user.id)
                .values(telegram_id=user.telegram_id)
                .values(plan=user.plan)
                .values(extra=user.extra)
        )
        await self.session.execute(query)
        await self.session.flush()

        return user
