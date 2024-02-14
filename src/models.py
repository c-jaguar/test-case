from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]


class StorageOrm(Base):
    __tablename__ = "storage"

    id: Mapped[intpk]
    capacity: Mapped[int]
    max_capacity: Mapped[int]
    max_weight: Mapped[float]

    item: Mapped[list["ItemOrm"]] = relationship(back_populates="storage")


class ItemOrm(Base):
    __tablename__ = "item"

    id: Mapped[intpk]
    type_: Mapped[str_256]
    name: Mapped[str_256]
    weight: Mapped[float]
    storage_id: Mapped[int] = mapped_column(ForeignKey("storage.id"))

    storage: Mapped[StorageOrm] = relationship(back_populates="item")


class SlaveOrm(Base):
    __tablename__ = "slave"

    id: Mapped[intpk]
    name: Mapped[str_256]
