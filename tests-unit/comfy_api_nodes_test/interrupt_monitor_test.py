"""Shared interruption-race helper and typed HTTP errors in comfy_api_nodes/util."""

import asyncio
from io import BytesIO

import pytest

from comfy_api_nodes.util import _helpers, download_helpers
from comfy_api_nodes.util._helpers import await_with_interrupt_monitor, poll_for_interrupt
from comfy_api_nodes.util.common_exceptions import ApiHttpError, ProcessingInterrupted


def test_request_wins_race_returns_result():
    async def make_request():
        return "ok"

    async def run():
        result = await await_with_interrupt_monitor(make_request)
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]
        assert pending == []
        return result

    assert asyncio.run(run()) == "ok"


def test_interrupt_cancels_request(monkeypatch):
    monkeypatch.setattr(_helpers, "is_processing_interrupted", lambda: True)
    release = asyncio.Event()
    cancelled = asyncio.Event()

    async def make_request():
        try:
            await release.wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    async def run():
        with pytest.raises(ProcessingInterrupted) as exc_info:
            await await_with_interrupt_monitor(make_request, cancelled_message="Upload cancelled")
        assert str(exc_info.value) == "Upload cancelled"

    asyncio.run(run())
    assert cancelled.is_set()


def test_poll_for_interrupt_stops_when_event_set():
    async def run():
        stop_evt = asyncio.Event()
        task = asyncio.create_task(poll_for_interrupt(stop_evt))
        await asyncio.sleep(0.01)
        assert not task.done()
        stop_evt.set()
        await asyncio.wait_for(task, 2)

    asyncio.run(run())


class _FakeResp:
    status = 403
    headers = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        raise ValueError("not json")

    async def text(self):
        return "forbidden"


class _FakeSession:
    def __init__(self, timeout=None):
        pass

    def get(self, url, headers=None, allow_redirects=True):
        return self._request()

    async def _request(self):
        return _FakeResp()

    async def close(self):
        pass


def test_download_terminal_http_raises_api_http_error(monkeypatch):
    monkeypatch.setattr(download_helpers.aiohttp, "ClientSession", _FakeSession)
    monkeypatch.setattr(download_helpers.request_logger, "log_request_response", lambda **kw: None)

    with pytest.raises(ApiHttpError) as exc_info:
        asyncio.run(download_helpers.download_url_to_bytesio("https://example.com/model.bin", BytesIO()))
    assert exc_info.value.status == 403
    assert str(exc_info.value) == "Failed to download (HTTP 403)."
