import itertools
from unittest.mock import Mock
from urllib.error import HTTPError

import pytest

from scripts import generate_one


@pytest.fixture
def polling(monkeypatch):
    clock = Mock()
    clock.monotonic.side_effect = itertools.count()
    get = Mock()
    monkeypatch.setattr(generate_one, "time", clock)
    monkeypatch.setattr(generate_one, "http_get_json", get)
    return get, clock.sleep


@pytest.mark.parametrize("outputs", [{}, {"9": {"images": [{"filename": "partial.png"}]}}])
@pytest.mark.parametrize("completed", [False, True])
def test_failed_prompt_stops_before_accepting_outputs(polling, outputs, completed):
    get, sleep = polling
    get.return_value = {"job": {"status": {"status_str": "error", "completed": completed}, "outputs": outputs}}

    with pytest.raises(RuntimeError, match="prompt job failed"):
        generate_one.wait_for_completion("job", timeout=6)

    get.assert_called_once()
    sleep.assert_not_called()


def test_history_with_null_status_and_outputs_still_returns(polling):
    get, sleep = polling
    entry = {"status": None, "outputs": {"9": {"images": [{"filename": "result.png"}]}}}
    get.return_value = {"job": entry}

    assert generate_one.wait_for_completion("job", timeout=6) is entry
    sleep.assert_not_called()


@pytest.mark.parametrize("outputs", [{}, {"9": {"images": [{"filename": "result.png"}]}}])
def test_completed_prompt_returns_history(polling, outputs):
    get, sleep = polling
    entry = {"status": {"status_str": "success", "completed": True}, "outputs": outputs}
    get.return_value = {"job": entry}

    assert generate_one.wait_for_completion("job", timeout=6) is entry
    sleep.assert_not_called()


def test_pending_history_and_404_keep_polling(polling):
    get, sleep = polling
    entry = {"outputs": {"9": {"images": [{"filename": "result.png"}]}}}
    get.side_effect = [{}, HTTPError("history", 404, "Not Found", {}, None), {"job": entry}]

    assert generate_one.wait_for_completion("job", timeout=10) is entry
    assert get.call_count == 3
    assert sleep.call_count == 2


def test_other_http_errors_propagate(polling):
    get, sleep = polling
    failure = HTTPError("history", 500, "Server Error", {}, None)
    get.side_effect = failure

    with pytest.raises(HTTPError) as caught:
        generate_one.wait_for_completion("job", timeout=6)

    assert caught.value is failure
    sleep.assert_not_called()


def test_pending_prompt_times_out(polling):
    get, sleep = polling
    get.return_value = {}

    with pytest.raises(TimeoutError, match="prompt job did not finish within 6s"):
        generate_one.wait_for_completion("job", timeout=6)

    assert get.call_count > 0
    assert sleep.call_count == get.call_count
