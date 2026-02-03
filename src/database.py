from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
)


def get_db():
    with Session(engine) as session:
        yield session
