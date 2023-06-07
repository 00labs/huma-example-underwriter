from huma_signals.adapters.ethereum_wallet import adapter as eth_adapter
from huma_signals.adapters.lending_pools import adapter as lending_pool_adapter

from underwriter import models
from underwriter.domain import rules, underwriter


async def underwrite(
    request: models.UnderwritingRequest,
) -> models.UnderwritingApproval:
    eth_wallet_adapter = eth_adapter.EthereumWalletAdapter()
    eth_wallet_signals = await eth_wallet_adapter.fetch(
        borrower_wallet_address=request.borrower_wallet_address,
    )
    pool_adapter = lending_pool_adapter.LendingPoolAdapter()
    lending_pool_signals = await pool_adapter.fetch(pool_address=request.pool_address)
    signals = models.Signals(
        **{
            **eth_wallet_signals.dict(),
            **lending_pool_signals.dict(),
        }
    )
    return underwriter.EthTransactionsUnderwriter.get_approval(
        signals=signals,
        rules_to_check=rules.TestnetRules()
        if signals.is_testnet
        else rules.MainnetRules(),
    )
