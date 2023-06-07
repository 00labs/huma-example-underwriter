from typing import Any, Mapping, MutableMapping

import datadog
import ddtrace
import orjson
import structlog
from ddtrace import opentracer

from underwriter.settings import settings

_DATADOG_HOST = "localhost"


def instrument() -> None:
    if settings.instrumentation_enabled:
        datadog.initialize(
            api_key=settings.datadog_api_key.get_secret_value(),
            statsd_host=_DATADOG_HOST,
            statsd_port=8125,
        )

        tracer = opentracer.Tracer(
            "eaverse",
            config={
                "agent_hostname": _DATADOG_HOST,
                "agent_port": 8126,
            },
        )
        opentracer.set_global_tracer(tracer)

        structlog.configure(
            processors=[
                _inject_tracer,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(serializer=orjson.dumps),
            ],
            logger_factory=structlog.BytesLoggerFactory(),
        )


def _inject_tracer(  # pylint: disable=unused-argument
    logger: Any,
    log_method: str,
    event_dict: MutableMapping[str, Any],
) -> Mapping[str, Any]:
    """
    make structlog inject tracer info into the log
    Copied from https://docs.datadoghq.com/tracing/connect_logs_and_traces/python/.
    """
    # Get correlation ids from current tracer context.
    span = ddtrace.tracer.current_span()
    trace_id, span_id = (span.trace_id, span.span_id) if span else (None, None)

    # Add ids to structlog event dictionary.
    event_dict["dd.trace_id"] = str(trace_id or 0)
    event_dict["dd.span_id"] = str(span_id or 0)

    # Add the env, service, and version configured for the tracer.
    event_dict["dd.env"] = ddtrace.config.env or ""
    event_dict["dd.service"] = ddtrace.config.service or ""
    event_dict["dd.version"] = ddtrace.config.version or ""

    return event_dict
