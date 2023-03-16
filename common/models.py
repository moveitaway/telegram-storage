from sqlalchemy import Column, Text, DateTime, func, JSON, ForeignKey, BigInteger

from common.settings import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    plan = Column(Text, nullable=False, default="free")
    extra = Column(JSON, default="{}")


FILE_TYPE_INBOX_FOLDER = "inbox"
FILE_TYPE_FOLDER = "folder"
FILE_TYPE_NOTE = "note"
FILE_TYPE_IMAGE = "image"
FILE_TYPE_DOCUMENT = "document"
FILE_TYPE_AUDIO = "audio"
FILE_TYPE_GIF = "gif"
FILE_TYPE_VIDEO = "video"


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    user_id = Column(BigInteger, ForeignKey(f"{User.__tablename__}.id"))
    type = Column(Text, nullable=False, default=FILE_TYPE_NOTE)
    path = Column(Text, nullable=False, index=True)
    name = Column(Text, nullable=False)
    size = Column(BigInteger, nullable=False, default=0)
    location = Column(Text, nullable=True)
