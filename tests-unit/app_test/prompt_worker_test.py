"""prompt_worker must survive an unhandled executor exception.

A raising PromptExecutor.execute must not kill the worker thread: the item
gets an error status task_done with empty (not stale) outputs, the UI is
told execution ended, the background asset scan is resumed, and the next
queued prompt still runs.
"""

import threading
import time

import main


class FakeExecutor:
    def __init__(self, server, cache_type, cache_args, asset_manager):
        self.calls = []
        self.history_result = {}
        self.status_messages = []
        self.success = True

    def execute(self, prompt, prompt_id, extra_data, outputs_to_execute):
        self.calls.append(prompt_id)
        if prompt_id == "boom":
            # simulate a prior successful prompt: the attribute still holds
            # that run's outputs and must not leak into the crashed entry
            self.history_result = {"outputs": {"stale": True}, "meta": {}}
            raise RuntimeError("executor bug")
        self.history_result = {"outputs": {}, "meta": {}}


class FakeQueue:
    def __init__(self, items):
        self._items = list(items)
        self._prompts = {item_id: item for item, item_id in items}
        self.done = []
        self.resumed = threading.Event()

    def get(self, timeout):
        if self._items:
            return self._items.pop(0)
        self.resumed.wait()
        return None

    def task_done(self, item_id, history_result, status, process_item=None):
        prompt = self._prompts[item_id]
        if process_item is not None:
            prompt = process_item(prompt)
        self.done.append((prompt[1], history_result, status))

    def get_flags(self):
        return {}


class FakeServer:
    def __init__(self):
        self.last_prompt_id = None
        self.client_id = "client1"
        self.sent = []

    def send_sync(self, event, data, sid):
        self.sent.append((event, data, sid))


class FakeAssetManager:
    def __init__(self):
        self.paused = 0
        self.resumed = 0

    def pause_background_scan(self):
        self.paused += 1

    def resume_background_scan(self):
        self.resumed += 1

    def queue_output_scan(self):
        pass


def _item(prompt_id):
    return ((0, prompt_id, {}, {}, [], {}), prompt_id)


def test_prompt_worker_survives_executor_exception(monkeypatch):
    monkeypatch.setattr(main.execution, "PromptExecutor", FakeExecutor)

    queue = FakeQueue([_item("boom"), _item("good")])
    assets = FakeAssetManager()
    server = FakeServer()

    worker = threading.Thread(target=main.prompt_worker, args=(queue, server, assets), daemon=True)
    worker.start()

    deadline = time.monotonic() + 10
    while len(queue.done) < 2 and time.monotonic() < deadline:
        time.sleep(0.01)

    assert [entry[0] for entry in queue.done] == ["boom", "good"]
    assert queue.done[0][1] == {}
    assert queue.done[0][2].status_str == "error"
    assert queue.done[0][2].completed is True
    assert queue.done[1][2].status_str == "success"
    assert assets.paused == 2
    # the crash path must resume the background scan right away; the second
    # pause is released by the periodic gc section on its own cadence
    assert assets.resumed >= 1
    # both the crash and success paths clear the UI executing state
    assert server.sent == [
        ("executing", {"node": None, "prompt_id": "boom"}, "client1"),
        ("executing", {"node": None, "prompt_id": "good"}, "client1"),
    ]

    queue.resumed.set()
    worker.join(timeout=1)
