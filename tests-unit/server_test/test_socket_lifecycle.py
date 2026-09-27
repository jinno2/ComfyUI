"""ws session lifecycle: claim, takeover, and release semantics."""

from server import PromptServer


def _bare_server():
    ps = PromptServer.__new__(PromptServer)
    ps.sockets = {}
    ps.sockets_metadata = {}
    return ps


def test_empty_sid_gets_fresh_id_and_default_metadata():
    ps = _bare_server()
    ws = object()
    sid = ps._register_socket(ws, "")
    assert sid
    assert ps.sockets[sid] is ws
    assert ps.sockets_metadata[sid] == {"feature_flags": {}}
    ps._release_socket(ws, sid)
    assert ps.sockets == {} and ps.sockets_metadata == {}


def test_requested_sid_takes_over_old_registration():
    ps = _bare_server()
    old_ws, new_ws = object(), object()
    ps._register_socket(old_ws, "abc")
    sid = ps._register_socket(new_ws, "abc")
    assert sid == "abc"
    assert ps.sockets["abc"] is new_ws


def test_release_keeps_newer_connection_with_same_sid():
    ps = _bare_server()
    old_ws, new_ws = object(), object()
    ps._register_socket(old_ws, "abc")
    ps._register_socket(new_ws, "abc")
    ps._release_socket(old_ws, "abc")
    assert ps.sockets.get("abc") is new_ws
    ps._release_socket(new_ws, "abc")
    assert ps.sockets == {} and ps.sockets_metadata == {}
