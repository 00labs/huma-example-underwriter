import pydantic


class HumaModel(pydantic.BaseModel):
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        allow_population_by_field_name = True


class UnderwritingRequest(HumaModel):
    pool_address: str
    borrower_wallet_address: str


class Token(HumaModel):
    symbol: str
    name: str
    decimal: int


class Terms(HumaModel):
    credit_limit: int
    interval_in_days: int
    apr_in_bps: int
    remaining_periods: int = 1


class Receivable(HumaModel):
    amount: int


class Approval(HumaModel):
    token: Token
    terms: Terms
    receivable: Receivable | None = None


class Rejection(HumaModel):
    reasons: list[str]


class UnderwritingApproval(HumaModel):
    result: Approval | Rejection


class Signals(HumaModel):
    total_transactions: int
    total_sent: int
    total_received: int
    wallet_tenure_in_days: int
    total_income_90days: int
    total_transactions_90days: int

    pool_address: str
    apr: int
    max_credit_amount: int
    token_name: str
    token_symbol: str
    token_decimal: int

    is_testnet: bool
