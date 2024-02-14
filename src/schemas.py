from pydantic import BaseModel


class StorageAddDTO(BaseModel):
    capacity: int
    max_capacity: int
    max_weight: float


class StorageDTO(StorageAddDTO):
    id: int


class ItemAddDTO(BaseModel):
    type_: str
    weight: float
    name: str
    storage_id: int


class ItemDTO(ItemAddDTO):
    id: int


class SlaveAddDTO(BaseModel):
    name: str


class SlaveDTO(SlaveAddDTO):
    id: int


class StorageRelDTO(StorageDTO):
    item: list["ItemDTO"]


class ItemRelDTO(ItemDTO):
    storage: "StorageDTO"


class ItemSumWeightTypeDTO(BaseModel):
    type: str
    weight_sum: float
