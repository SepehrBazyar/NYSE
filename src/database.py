from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
)


def get_session():
    with Session(engine) as session:
        yield session
