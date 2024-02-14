"""empty message

Revision ID: 3344c69520a4
Revises: 62772a794564
Create Date: 2024-02-14 15:04:14.729002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from src.models import *
import csv

# revision identifiers, used by Alembic.
revision: str = '3344c69520a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def determine_storage(weight):
    session = sa.orm.Session(bind=op.get_bind())
    s = sa.orm.aliased(StorageOrm)
    query = sa.select(s.id).where(sa.and_(s.capacity < s.max_capacity, weight <= s.max_weight))
    res = session.execute(query)
    result = res.scalars().first()
    if not result:
        print("No more room in hell")
    return result


def parse_csv():
    with open("data.csv", newline='', encoding='utf-8-sig') as f:
        session = sa.orm.Session(bind=op.get_bind())
        entities = list()
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if not row[0]:
                break
            elif row[0] == "Storage max weight":
                continue
            entities.append(StorageOrm(capacity=0,
                                       max_capacity=10,
                                       max_weight=float(row[0].replace(",", "."))
                                       )
                            )
        session.add_all(entities)
        session.commit()

        session = sa.orm.Session(bind=op.get_bind())
        entities = list()
        next(reader)
        for row in reader:
            if not row[0]:
                break
            elif row[0] == "Items" or row[0] == "Type":
                continue
            weight = float(row[2].replace(",", "."))
            storage_id = determine_storage(weight)
            if storage_id:
                entities.append(ItemOrm(type_=row[0], name=row[1], weight=weight, storage_id=storage_id))
                addtostorage = session.get(StorageOrm, storage_id)
                addtostorage.capacity += 1

        next(reader)
        for row in reader:
            if row[0] == "Workers":
                continue
            entities.append(SlaveOrm(name=row[0]))
        session.add_all(entities)
        session.commit()


def upgrade() -> None:
    op.create_table('storage',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('storage_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('capacity', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('max_capacity', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('max_weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='storage_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('item',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('type_', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
                    sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
                    sa.Column('storage_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['storage_id'], ['storage.id'], name='item_storage_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='item_pkey')
                    )
    op.create_table('slave',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='slave_pkey')
                    )

    parse_csv()


def downgrade() -> None:
    pass
