import pytest

from tests.fixtures import model_factories
from underwriter import models
from underwriter.domain import rules, underwriter


class AlwaysPassRule(rules.Rules):
    @classmethod
    def check(cls, signals: models.Signals) -> list[str]:
        return []


class AlwaysRejectRule(rules.Rules):
    @classmethod
    def check(cls, signals: models.Signals) -> list[str]:
        return ["You shall not pass"]


def describe_Underwriter() -> None:
    @pytest.fixture
    def signals() -> models.Signals:
        return model_factories.SignalsFactory.create()

    @pytest.fixture
    def underwriter_() -> underwriter.EthTransactionsUnderwriter:
        return underwriter.EthTransactionsUnderwriter()

    def it_approves_the_request(
        signals: models.Signals,
        underwriter_: underwriter.EthTransactionsUnderwriter,
    ) -> None:
        approval = underwriter_.get_approval(
            signals=signals, rules_to_check=AlwaysPassRule()
        )
        assert isinstance(approval.result, models.Approval)

    def if_one_of_the_rules_fail() -> None:
        def it_rejects_the_request(
            signals: models.Signals,
            underwriter_: underwriter.EthTransactionsUnderwriter,
        ) -> None:
            approval = underwriter_.get_approval(
                signals=signals, rules_to_check=AlwaysRejectRule()
            )
            assert isinstance(approval.result, models.Rejection)
            assert len(approval.result.reasons) > 0
