import factory

from underwriter import models


class UnderwritingRequestFactory(factory.Factory):
    class Meta:
        model = models.UnderwritingRequest

    pool_address = ""
    borrower_wallet_address = ""


class SignalsFactory(factory.Factory):
    class Meta:
        model = models.Signals

    total_transactions = 10
    total_sent = 5
    total_received = 5
    wallet_tenure_in_days = 200
    total_income_90days = 10
    total_transactions_90days = 8
    pool_address = "0x0000000000000000000000000000000000000000"
    apr = 0
    max_credit_amount = 0
    token_name = "Test Token"
    token_symbol = "TT"
    token_decimal = 18
    is_testnet = False
