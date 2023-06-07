import fastapi
import structlog

from underwriter import models
from underwriter.api import exception_handlers
from underwriter.domain import services

logger = structlog.get_logger(__name__)

router = fastapi.APIRouter()


@router.post("/approve")
@exception_handlers.handle_exception
async def approve(request: models.UnderwritingRequest) -> models.UnderwritingApproval:
    return await services.underwrite(request=request)
