import traceback
from typing import List

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from underwriter.core.models import UnderwritingApproval, UnderwritingRequest
from underwriter.core.underwriter import EthTransactionsUnderwriter

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/signals")
async def get_signals(request: Request) -> List[str]:
    return UnderwritingRequest.get_field_names(alias=True)


@router.post("/approve/", response_model=UnderwritingApproval)
async def post_approve(approval_request: UnderwritingRequest) -> UnderwritingApproval:
    try:
        result = EthTransactionsUnderwriter.get_approval(approval_request)
        return result
    except Exception as e:
        logger.error(traceback.format_exc())
        return JSONResponse(
            content={
                "statusCode": 500,
                "errorMessage": traceback.format_exception_only(type(e), e),
            }
        )
