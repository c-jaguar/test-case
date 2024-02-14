from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from config import Settings


class EngineClass:
    engine = None
    session_factory = None

    @classmethod
    def reload_engine(cls):
        """Changes environment variables and reloads the engine."""
        Settings.reload_settings()
        cls.engine = create_async_engine(
                url=Settings.DATABASE_URL_asyncpg,
                echo=False
            )
        cls.session_factory = async_sessionmaker(cls.engine)


EngineClass.reload_engine()

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 10
    repr_cols = tuple()

    def __repr__(self):
        """Output format for debug purposes."""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
