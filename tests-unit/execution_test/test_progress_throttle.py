"""WebUIProgressHandler must coalesce rapid progress_state sends.

Per-step update calls arrive far faster than a UI renders, so voluntary
sends are time-coalesced while start/finish transitions and preview
images still go out immediately.
"""

import comfy_execution.progress as progress_module
from comfy_execution.progress import (
    BinaryEventTypes,
    NodeProgressState,
    NodeState,
    WebUIProgressHandler,
)


class FakeServer:
    def __init__(self):
        self.sent = []
        self.client_id = None
        self.sockets_metadata = {}

    def send_sync(self, event, data, sid=None):
        self.sent.append((event, data))


class FakeDynPrompt:
    def get_display_node_id(self, node_id):
        return node_id

    def get_parent_node_id(self, node_id):
        return None

    def get_real_node_id(self, node_id):
        return node_id


class FakeRegistry:
    def __init__(self):
        self.dynprompt = FakeDynPrompt()
        self.nodes = {}


class FakeTime:
    def __init__(self):
        self.now = 1000.0

    def monotonic(self):
        return self.now


def _handler(monkeypatch):
    fake_time = FakeTime()
    monkeypatch.setattr(progress_module, "time", fake_time)
    server = FakeServer()
    handler = WebUIProgressHandler(server)
    registry = FakeRegistry()
    handler.set_registry(registry)
    return handler, server, registry, fake_time


def _state(value=0.0, max=10.0, state=NodeState.Running):
    return NodeProgressState(state=state, value=value, max=max)


def _state_sends(server):
    return [entry for entry in server.sent if entry[0] == "progress_state"]


def test_update_handler_throttles_rapid_sends(monkeypatch):
    handler, server, registry, fake_time = _handler(monkeypatch)
    registry.nodes["1"] = _state()

    handler.update_handler("1", 1.0, 10.0, registry.nodes["1"], "pid")
    fake_time.now += 0.01
    handler.update_handler("1", 2.0, 10.0, registry.nodes["1"], "pid")
    fake_time.now += 0.01
    handler.update_handler("1", 3.0, 10.0, registry.nodes["1"], "pid")

    assert len(_state_sends(server)) == 1


def test_update_handler_sends_after_min_interval(monkeypatch):
    handler, server, registry, fake_time = _handler(monkeypatch)
    registry.nodes["1"] = _state()

    handler.update_handler("1", 1.0, 10.0, registry.nodes["1"], "pid")
    fake_time.now += progress_module.PROGRESS_STATE_MIN_INTERVAL
    handler.update_handler("1", 2.0, 10.0, registry.nodes["1"], "pid")

    assert len(_state_sends(server)) == 2


def test_start_and_finish_send_immediately(monkeypatch):
    handler, server, registry, fake_time = _handler(monkeypatch)
    registry.nodes["1"] = _state()

    handler.start_handler("1", registry.nodes["1"], "pid")
    fake_time.now += 0.01
    handler.update_handler("1", 1.0, 10.0, registry.nodes["1"], "pid")
    # mirror ProgressRegistry.finish_progress mutating the entry before notifying
    registry.nodes["1"]["state"] = NodeState.Finished
    registry.nodes["1"]["value"] = 10.0
    handler.finish_handler("1", registry.nodes["1"], "pid")

    sends = _state_sends(server)
    assert len(sends) == 2
    assert sends[-1][1]["nodes"]["1"]["state"] == "finished"


def test_preview_images_are_not_throttled(monkeypatch):
    handler, server, registry, fake_time = _handler(monkeypatch)
    monkeypatch.setattr(
        progress_module.feature_flags, "supports_feature", lambda *args, **kwargs: True
    )
    registry.nodes["1"] = _state()
    image = ("preview.png", object(), None)

    handler.update_handler("1", 1.0, 10.0, registry.nodes["1"], "pid", image)
    fake_time.now += 0.01
    handler.update_handler("1", 2.0, 10.0, registry.nodes["1"], "pid", image)

    assert len(_state_sends(server)) == 1
    previews = [
        entry
        for entry in server.sent
        if entry[0] == BinaryEventTypes.PREVIEW_IMAGE_WITH_METADATA
    ]
    assert len(previews) == 2
