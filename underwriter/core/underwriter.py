from decimal import Decimal
from typing import List

from underwriter.core.models import HumaModel, UnderwritingApproval, UnderwritingRequest

DEFAULT_MIN_TRANSACTION_AMOUNT = 0.1


class EthTransactionsUnderwriter(HumaModel):
    @classmethod
    def check_rules(cls, signals: UnderwritingRequest) -> List[str]:
        rejection_reasons = []
        if signals.total_transactions < 1:
            rejection_reasons.append("No transactions in the wallet")
        if signals.total_transactions < 5:
            rejection_reasons.append("Not enough transactions in the wallet")
        if signals.wallet_teneur_in_days < 90:
            rejection_reasons.append("Wallet is too new")
        if signals.total_transactions_90days < 3:
            rejection_reasons.append("Not enough transactions in the last 90 days")
        if signals.total_income_90days < DEFAULT_MIN_TRANSACTION_AMOUNT:
            rejection_reasons.append("Not enough income in the last 90 days")
        return rejection_reasons

    @classmethod
    def get_approval(cls, signals: UnderwritingRequest) -> UnderwritingApproval:
        rejection_reasons = cls.check_rules(signals)
        if len(rejection_reasons) > 0:
            return UnderwritingApproval(
                approved=False,
                rejection_reasons=rejection_reasons,
            )

        # calculate approvable terms
        approvable_amount = min(
            signals.max_credit_amount, Decimal((10**signals.token_decimal) * float(signals.total_income_90days) / 2)
        )
        return UnderwritingApproval(
            token_symbol=signals.token_symbol,
            token_name=signals.token_name,
            token_decimal=signals.token_decimal,
            credit_limit=approvable_amount,
            interval_in_days=30,
            remaining_periods=3,
            apr_in_bps=signals.apr,
            approved=True,
        )
