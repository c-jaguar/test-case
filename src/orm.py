from sqlalchemy.orm import aliased, selectinload
from sqlalchemy import and_, func, select, text
from database import EngineClass
from models import *
from schemas import StorageRelDTO, ItemSumWeightTypeDTO


class ORM:

    @staticmethod
    async def check_connection():
        """Checks connection to DB after changing environment variables. Passes error if connection failed."""
        async with EngineClass.session_factory() as session:
            query = select(text("1"))
            try:
                await session.execute(query)
                return {"message": "DB connection successful"}
            except Exception as e:
                return {"message": f"Error: {e}"}

    @staticmethod
    async def clear_data():
        """Clears all data from DB for debug purposes."""
        async with EngineClass.session_factory() as session:
            await session.execute(text('TRUNCATE {} RESTART IDENTITY;'.format(
                ','.join(table.name for table in reversed(Base.metadata.sorted_tables)))))
            await session.commit()

    @staticmethod
    async def determine_storage(weight):
        """Determines storage for given weight and available storage capacity."""
        async with EngineClass.session_factory() as session:
            s = aliased(StorageOrm)
            query = select(s.id).where(and_(s.capacity < s.max_capacity, weight <= s.max_weight))
            res = await session.execute(query)
            result = res.scalars().first()

            if not result:
                print("No more room in hell")
            return result

    @staticmethod
    async def select_storage_dto():
        """Selects all available storage relations."""
        async with EngineClass.session_factory() as session:
            s = aliased(StorageOrm)
            query = select(s).options(selectinload(s.item))
            res = await session.execute(query)
            res = res.scalars().all()
            result_dto = [StorageRelDTO.model_validate(row, from_attributes=True) for row in res]
        return result_dto

    @staticmethod
    async def select_item_weight_sum():
        """Selects item sum weight by type."""
        async with EngineClass.session_factory() as session:
            i = aliased(ItemOrm)
            query = select(i.type_.label("type"), func.sum(i.weight).label("weight_sum")).group_by(i.type_)
            res = await session.execute(query)
            res = res.all()
            result_dto = [ItemSumWeightTypeDTO.model_validate(row, from_attributes=True) for row in res]
        return result_dto
