from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class HumaModel(BaseModel):
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        allow_population_by_field_name = True

        json_encoders = {
            # custom output conversions
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            Decimal: lambda v: str(v) if v else None,
        }


class UnderwritingRequest(HumaModel):
    total_transactions: int = Field(..., alias="wallet_eth_txns.total_transactions")
    total_sent: int = Field(..., alias="wallet_eth_txns.total_sent")
    total_received: int = Field(..., alias="wallet_eth_txns.total_received")
    wallet_teneur_in_days: int = Field(..., alias="wallet_eth_txns.wallet_teneur_in_days")
    total_income_90days: float = Field(..., alias="wallet_eth_txns.total_income_90days")
    total_transactions_90days: int = Field(..., alias="wallet_eth_txns.total_transactions_90days")

    apr: Decimal = Field(..., alias="pool_policy.apr")
    max_credit_amount: Decimal = Field(..., alias="pool_policy.max_credit_amount")
    token_name: str = Field(..., alias="pool_policy.token_name")
    token_symbol: str = Field(..., alias="pool_policy.token_symbol")
    token_decimal: int = Field(..., alias="pool_policy.token_decimal")

    @classmethod
    def from_signals(cls, signals: Dict[str, Any]) -> "UnderwritingRequest":
        return cls(**signals)

    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias).get("properties").keys())


class UnderwritingApproval(HumaModel):
    token_symbol: str = None
    token_name: str = None
    token_decimal: int = None
    credit_limit: Decimal = None
    interval_in_days: int = None
    apr_in_bps: int = None
    receivable_amount: Decimal = None

    approved: bool = False
    rejection_reasons: List[str] = []
    remaining_periods: int = 1

    def to_dict(self):
        if not self.approved:
            return {"status": "declined", "reason": self.rejection_reasons}
        return {
            "tokenSymbol": self.token_symbol,
            "tokenName": self.token_name,
            "tokenDecimal": self.token_decimal,
            "creditLimit": int(self.credit_limit),
            "intervalInDays": self.interval_in_days,
            "aprInBps": self.apr_in_bps,
            "receivableAmount": int(self.receivable_amount),
            "remainingPeriods": self.remaining_periods,
        }
