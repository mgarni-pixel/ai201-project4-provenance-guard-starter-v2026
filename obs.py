"""
Request-level observability — UNIT 9, the capstone extension.

`audit.py` records *decisions*: what the service concluded about a piece of
text. This records *requests*: what happened when someone called the service,
including the calls that never became a decision.

The two are deliberately separate files. The audit log is the evidence trail a
reviewer reads when a writer appeals, and it is graded evidence from units 7
and 8 — appending operational noise to it would spoil both. `requests.jsonl`
is the operational log: one record per HTTP request, whatever the outcome.

What one record holds:

    timestamp     when the request finished, UTC, to the millisecond
    request_id    a short id, also returned in the X-Request-ID header
    method        GET or POST
    route         the matched rule ("/submit"), not the raw path
    status        the HTTP status actually sent
    duration_ms   whole request, measured around the handler
    creator_id    who called, when the body carried one
    content_id    the decision this produced, when it produced one
    outcome       "ok", or the error code the handler returned
    stages        per-stage milliseconds inside the handler
    exception     the exception type, when the handler raised

Every field is present on every record, null when it does not apply, so the
file is one shape and can be read with a single parser.

    import obs
    obs.install(app)                      # once, at startup
    with obs.stage("model"):              # inside a handler
        ...
"""

import json
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

from flask import g, got_request_exception, request

import config

_lock = threading.Lock()

# Bodies are read on the way in, because a handler is free to consume the
# stream and Flask caches only so much. These are the only fields pulled out —
# the submitted text itself is never copied here. It is already in the audit
# trail, and a second copy in an operational log is a second place it leaks
# from.
_BODY_FIELDS = ("creator_id",)


def install(app):
    """Attach the request hooks to a Flask app. Call once."""
    app.before_request(_start)
    app.after_request(_finish)
    app.teardown_request(_teardown)
    # Flask turns an uncaught exception into a 500 and then finalizes that
    # response, so after_request runs and writes the record BEFORE
    # teardown_request is handed the exception. Without this signal the record
    # would say status 500 and outcome "ok", which is the least useful pair of
    # fields a log could carry. The signal fires while the exception is still
    # in hand, so _finish can read it.
    got_request_exception.connect(_remember_exception, app)
    return app


def _remember_exception(sender, exception, **kwargs):
    g._obs_exception = type(exception).__name__


@contextmanager
def stage(name: str):
    """
    Time one stage of a handler.

    Accumulates rather than overwrites, so calling a stage twice in one
    request reports the total — which is what you want when a retry runs the
    same stage again, and is the number a latency breakdown needs.
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        stages = getattr(g, "_obs_stages", None)
        if stages is None:
            # No request context (a unit test calling the function directly),
            # or install() was never called. Timing is not worth an exception.
            return
        stages[name] = round(stages.get(name, 0.0) + elapsed, 2)


def note(**fields):
    """
    Record something the hooks cannot see from outside the handler — the
    content_id a decision produced, or the error code it chose to return.
    """
    extra = getattr(g, "_obs_extra", None)
    if extra is not None:
        extra.update(fields)


def _start():
    g._obs_started = time.perf_counter()
    g._obs_stages = {}
    g._obs_extra = {}
    g._obs_request_id = uuid.uuid4().hex[:12]
    g._obs_exception = None
    payload = request.get_json(silent=True)
    g._obs_body = {f: payload.get(f) for f in _BODY_FIELDS} if isinstance(payload, dict) else {}


def _finish(response):
    # A 404 for an unknown URL never reaches before_request's siblings in the
    # same way; guard so the hook can never be the thing that breaks a reply.
    if getattr(g, "_obs_started", None) is None:
        return response
    response.headers["X-Request-ID"] = g._obs_request_id
    _write(status=response.status_code, exception=getattr(g, "_obs_exception", None))
    return response


def _teardown(exc):
    """
    A handler that raised still leaves a record.

    after_request does not run when the handler raises, so without this the
    only failures in the log would be the ones the handler was polite enough
    to catch — and a failure that shows up as an absence is one you never find.
    """
    if exc is None or getattr(g, "_obs_started", None) is None:
        return
    if getattr(g, "_obs_written", False):
        return
    # Only reached when after_request never ran — the response was not
    # finalized at all, which is what PROPAGATE_EXCEPTIONS does.
    _write(status=500, exception=type(exc).__name__)


def _write(status: int, exception: str | None = None):
    if getattr(g, "_obs_written", False):
        return
    g._obs_written = True

    extra = g._obs_extra
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "request_id": g._obs_request_id,
        "method": request.method,
        # url_rule is None when nothing matched, and the raw path is the only
        # thing left to say where the call went.
        "route": str(request.url_rule) if request.url_rule else request.path,
        "status": status,
        "duration_ms": round((time.perf_counter() - g._obs_started) * 1000, 2),
        "creator_id": g._obs_body.get("creator_id"),
        "content_id": extra.get("content_id"),
        "outcome": extra.get("outcome", "error" if exception else "ok"),
        "stages": g._obs_stages,
        "exception": exception,
    }

    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False)
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_records(limit: int | None = None) -> list[dict]:
    """
    Read the request log back, oldest first.

    A malformed line is skipped rather than raised on, for the same reason
    `audit.read_entries` does it: a log you cannot open because of one bad row
    is worse than a log with a gap.
    """
    if not config.REQUEST_LOG.exists():
        return []

    records = []
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records[-limit:] if limit else records


REQUIRED_FIELDS = ("timestamp", "request_id", "method", "route", "status",
                   "duration_ms", "creator_id", "content_id", "outcome",
                   "stages", "exception")
