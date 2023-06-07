import decimal

from underwriter import models
from underwriter.domain import rules

# Only allow 100 USDC credit line
DEFAULT_MAX_CREDIT_AMOUNT = decimal.Decimal(100)


class EthTransactionsUnderwriter:
    @classmethod
    def get_approval(
        cls,
        signals: models.Signals,
        rules_to_check: rules.Rules,
    ) -> models.UnderwritingApproval:
        rejection_reasons = rules_to_check.check(signals)
        if len(rejection_reasons) > 0:
            return models.UnderwritingApproval(
                result=models.Rejection(reasons=rejection_reasons),
            )

        approved_amount = DEFAULT_MAX_CREDIT_AMOUNT * (10**signals.token_decimal)
        return models.UnderwritingApproval(
            result=models.Approval(
                token=models.Token(
                    symbol=signals.token_symbol,
                    name=signals.token_name,
                    decimal=signals.token_decimal,
                ),
                terms=models.Terms(
                    credit_limit=approved_amount,
                    # TODO: change all these setting to use the pool settings.
                    interval_in_days=30,
                    remaining_periods=12,
                    apr_in_bps=signals.apr,
                ),
            ),
        )
