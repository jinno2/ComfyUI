"""ws session lifecycle: claim, takeover, and release semantics."""

import logging
from types import SimpleNamespace

from server import PromptServer


class StubRequest:
    def __init__(self, client_id="", headers=None, remote="10.0.0.1"):
        self.rel_url = SimpleNamespace(query={"clientId": client_id} if client_id else {})
        self.headers = headers or {}
        self.remote = remote


def _bare_server():
    ps = PromptServer.__new__(PromptServer)
    ps.sockets = {}
    ps.sockets_metadata = {}
    return ps


def test_missing_sid_gets_fresh_id_and_source_metadata():
    ps = _bare_server()
    ws = object()
    sid = ps._register_socket(ws, StubRequest(headers={"Origin": "http://127.0.0.1:8188"}))
    assert sid
    assert ps.sockets[sid] is ws
    assert ps.sockets_metadata[sid] == {
        "feature_flags": {},
        "remote": "10.0.0.1",
        "origin": "http://127.0.0.1:8188",
    }
    ps._release_socket(ws, sid)
    assert ps.sockets == {} and ps.sockets_metadata == {}


def test_requested_sid_takes_over_old_registration(caplog):
    caplog.set_level(logging.INFO)
    ps = _bare_server()
    old_ws, new_ws = object(), object()
    ps._register_socket(old_ws, StubRequest(client_id="abc", remote="10.0.0.1"))
    sid = ps._register_socket(new_ws, StubRequest(client_id="abc", remote="10.0.0.2"))
    assert sid == "abc"
    assert ps.sockets["abc"] is new_ws
    assert "10.0.0.1 -> 10.0.0.2" in caplog.text


def test_release_keeps_newer_connection_with_same_sid():
    ps = _bare_server()
    old_ws, new_ws = object(), object()
    ps._register_socket(old_ws, StubRequest(client_id="abc"))
    ps._register_socket(new_ws, StubRequest(client_id="abc"))
    ps._release_socket(old_ws, "abc")
    assert ps.sockets.get("abc") is new_ws
    ps._release_socket(new_ws, "abc")
    assert ps.sockets == {} and ps.sockets_metadata == {}
