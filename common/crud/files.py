from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models import File, User, FILE_TYPE_INBOX_FOLDER


class FilesCrud:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_inbox_folder(self, user: User) -> File:
        query = select(File).where((File.user_id == user.id) & (File.type == FILE_TYPE_INBOX_FOLDER))
        result = await self.session.execute(query)
        file = result.scalars().one_or_none()
        if not file:
            return await self.persist(File(user_id=user.id, type=FILE_TYPE_INBOX_FOLDER, path=f"{user.id}", name="Inbox"))
        return file

    async def persist(self, file: File) -> File:
        if file.id is not None:
            return await self._update(file)

        self.session.add(file)
        await self.session.flush()
        await self.session.commit()
        return file

    async def _update(self, file: File) -> File:
        query = (
            update(File)
                .where(File.id == file.id)
                .values(type=file.type)
                .values(path=file.path)
                .values(name=file.name)
                .values(size=file.size)
                .values(location=file.location)
        )
        await self.session.execute(query)
        await self.session.flush()

        return file
