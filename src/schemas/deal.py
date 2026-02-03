from pydantic import BaseModel


class CreateDeal(BaseModel):
    tag_id: int
    details: str


class DealOut(BaseModel):
    id: int
    tag_id: int
    details: str
