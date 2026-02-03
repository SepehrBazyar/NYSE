from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.models import Deal
from src.schemas.deal import CreateDeal, DealOut
from src.services.notification import publish_new_deal

router = APIRouter(prefix="/deals", tags=["deals"])


@router.post("/", response_model=DealOut)
async def create_deal(
    deal_in: CreateDeal,
    session: AsyncSession = Depends(get_session),
):
    db_deal = Deal(**deal_in.model_dump())
    session.add(db_deal)
    await session.commit()
    await session.refresh(db_deal)

    deal_data = {
        "id": db_deal.id,
        "tag_id": db_deal.tag_id,
        "details": db_deal.details,
    }

    await publish_new_deal(deal_data)

    return deal_data
