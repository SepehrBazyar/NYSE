from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class Subscription(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Deal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag_id: int = Field(foreign_key="tag.id")
    details: str

    tag: Tag | None = Relationship(back_populates=None)
