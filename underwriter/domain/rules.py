import abc

from underwriter import models

DEFAULT_MIN_TRANSACTION_AMOUNT = 1


class Rules(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def check(cls, signals: models.Signals) -> list[str]:
        raise NotImplementedError


class MainnetRules(Rules):
    @classmethod
    def check(cls, signals: models.Signals) -> list[str]:
        rejection_reasons = []
        if signals.total_transactions < 5:
            rejection_reasons.append("Not enough transactions in the wallet")
        if signals.wallet_tenure_in_days < 183:
            rejection_reasons.append("Wallet is too new")
        return rejection_reasons


class TestnetRules(Rules):
    @classmethod
    def check(cls, signals: models.Signals) -> list[str]:
        rejection_reasons = []
        if signals.total_transactions < 2:
            rejection_reasons.append("Not enough transactions in the wallet")
        if signals.wallet_tenure_in_days < 7:
            rejection_reasons.append("Wallet is too new")
        return rejection_reasons
