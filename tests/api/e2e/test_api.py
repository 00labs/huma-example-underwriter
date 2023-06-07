import pytest

from tests.fixtures import model_factories
from tests.helpers import address_helpers, api_test_helpers, vcr_helpers
from underwriter import models

_FIXTURE_BASE_PATH = "/api/e2e/api"


def describe_approve() -> None:
    @pytest.fixture
    def goerli_pool_address() -> str:
        return "0xA22D20FB0c9980fb96A9B0B5679C061aeAf5dDE4"

    @pytest.fixture
    def borrower_wallet_address() -> str:
        return "0xc38B0528097B8076048BEdf4330644F068CEC2e6"

    @pytest.fixture
    def underwriting_request(
        goerli_pool_address: str, borrower_wallet_address: str
    ) -> models.UnderwritingRequest:
        return model_factories.UnderwritingRequestFactory.create(
            pool_address=goerli_pool_address,
            borrower_wallet_address=borrower_wallet_address,
        )

    async def it_approves_the_underwriting_request(
        underwriting_request: models.UnderwritingRequest,
    ) -> None:
        with vcr_helpers.use_cassette(
            fixture_file_path=f"{_FIXTURE_BASE_PATH}/approve.yml",
            match_on=["alchemy_url"],
        ):
            resp = await api_test_helpers.post_request(
                "/approve", data=underwriting_request.json()
            )
            assert resp.status_code == 200
            resp_json = resp.json()
            assert len(resp_json["result"]["reasons"]) > 0

    def if_there_is_an_exception_during_signal_fetching() -> None:
        @pytest.fixture
        def goerli_pool_address() -> str:
            return address_helpers.fake_hex_address()

        async def it_returns_the_error(
            underwriting_request: models.UnderwritingRequest,
        ) -> None:
            with vcr_helpers.use_cassette(
                fixture_file_path=f"{_FIXTURE_BASE_PATH}/approve_error.yml"
            ):
                resp = await api_test_helpers.post_request(
                    "/approve", data=underwriting_request.json()
                )
                assert resp.status_code == 404
