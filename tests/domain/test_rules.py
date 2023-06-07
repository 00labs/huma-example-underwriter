import pytest

from tests.fixtures import model_factories
from underwriter import models
from underwriter.domain import rules


def describe_MainnetRules() -> None:
    @pytest.fixture
    def signals() -> models.Signals:
        return model_factories.SignalsFactory.create()

    def it_returns_no_rejection_reasons(signals: models.Signals) -> None:
        assert rules.MainnetRules.check(signals) == []

    def when_the_signals_do_not_satisfy_all_rules() -> None:
        @pytest.mark.parametrize(
            "total_transactions, wallet_tenure_in_days, num_rejection_reasons",
            [
                (4, 183, 1),
                (5, 182, 1),
                (4, 182, 2),
            ],
        )
        def it_returns_rejection_reasons(
            total_transactions: int,
            wallet_tenure_in_days: int,
            total_transactions_90days: int,
            total_income_90days: int,
            num_rejection_reasons: int,
        ) -> None:
            signals = model_factories.SignalsFactory.create(
                total_transactions=total_transactions,
                wallet_tenure_in_days=wallet_tenure_in_days,
                total_transactions_90days=total_transactions_90days,
                total_income_90days=total_income_90days,
            )
            assert len(rules.MainnetRules.check(signals)) == num_rejection_reasons


def describe_TestnetRules() -> None:
    @pytest.fixture
    def signals() -> models.Signals:
        return model_factories.SignalsFactory.create()

    def it_returns_no_rejection_reasons(signals: models.Signals) -> None:
        assert rules.TestnetRules.check(signals) == []

    def when_the_signals_do_not_satisfy_all_rules() -> None:
        @pytest.mark.parametrize(
            "total_transactions, wallet_tenure_in_days, num_rejection_reasons",
            [
                (1, 7, 1),
                (2, 6, 1),
                (1, 6, 2),
            ],
        )
        def it_returns_rejection_reasons(
            total_transactions: int,
            wallet_tenure_in_days: int,
            total_income_90days: int,
            num_rejection_reasons: int,
        ) -> None:
            signals = model_factories.SignalsFactory.create(
                total_transactions=total_transactions,
                wallet_tenure_in_days=wallet_tenure_in_days,
                total_income_90days=total_income_90days,
            )
            assert len(rules.TestnetRules.check(signals)) == num_rejection_reasons
