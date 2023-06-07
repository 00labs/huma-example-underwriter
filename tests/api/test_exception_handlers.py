import fastapi
import pytest
from huma_signals import exceptions as huma_signal_exceptions

from underwriter.api import exception_handlers


def describe_handle_exception() -> None:
    def when_wrapped_func_runs_without_errors() -> None:
        async def it_does_not_throw_error() -> None:
            @exception_handlers.handle_exception
            async def good_func() -> None:
                pass

            await good_func()

    def when_wrapped_func_throws_signal_exception() -> None:
        def with_specific_status_code() -> None:
            async def it_returns_the_status_code() -> None:
                @exception_handlers.handle_exception
                async def pool_setting_not_found_func() -> None:
                    raise huma_signal_exceptions.PoolSettingsNotFoundException(
                        "Not found"
                    )

                with pytest.raises(fastapi.HTTPException) as e:
                    await pool_setting_not_found_func()
                    assert e.value.status_code == 404

        def with_generic_status_code() -> None:
            async def it_returns_the_error_code() -> None:
                @exception_handlers.handle_exception
                async def contract_call_failed_func() -> None:
                    raise huma_signal_exceptions.ContractCallFailedException(
                        "contract call failed"
                    )

                with pytest.raises(fastapi.HTTPException) as e:
                    await contract_call_failed_func()
                    assert e.value.status_code == 500

    def when_wrapped_func_throws_generic_exception() -> None:
        async def it_returns_the_error_code() -> None:
            @exception_handlers.handle_exception
            async def exceptional_func() -> None:
                raise Exception()

            with pytest.raises(fastapi.HTTPException) as e:
                await exceptional_func()
                assert e.value.status_code == 500
