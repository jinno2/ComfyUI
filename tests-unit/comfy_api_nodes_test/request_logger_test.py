import pytest

from comfy_api_nodes.util import request_logger


@pytest.mark.parametrize("header_sides", [
    ("request_headers",),
    ("response_headers",),
    ("request_headers", "response_headers"),
])
def test_log_redacts_sensitive_headers(header_sides, tmp_path, monkeypatch):
    monkeypatch.setattr(request_logger, "get_log_directory", lambda: str(tmp_path))
    headers = {
        "Authorization": "Bearer authorization-secret",
        "x-aPi-KEY": "api-key-secret",
        "cOoKiE": "session=cookie-secret",
        "sEt-CoOkIe": "session=set-cookie-secret; HttpOnly",
        "Content-Type": "application/json",
        "X-Request-ID": "request-123",
    }
    original_headers = headers.copy()

    request_logger.log_request_response(
        operation_id="redaction-test",
        request_method="POST",
        request_url="https://example.invalid/test",
        response_status_code=200,
        **{side: headers for side in header_sides},
    )

    log_files = list(tmp_path.glob("*.log"))
    assert len(log_files) == 1
    content = log_files[0].read_text(encoding="utf-8")
    for name in ("Authorization", "x-aPi-KEY", "cOoKiE", "sEt-CoOkIe"):
        assert original_headers[name] not in content
        assert content.count(f'"{name}": "***"') == len(header_sides)
    assert '"Content-Type": "application/json"' in content
    assert '"X-Request-ID": "request-123"' in content
    assert "REQUEST" in content
    assert "RESPONSE" in content
    assert "Status Code: 200" in content
    assert headers == original_headers


@pytest.mark.parametrize("headers", [None, {}])
def test_log_without_headers(headers, tmp_path, monkeypatch):
    monkeypatch.setattr(request_logger, "get_log_directory", lambda: str(tmp_path))

    request_logger.log_request_response(
        operation_id="no-headers-test",
        request_method="GET",
        request_url="https://example.invalid/test",
        request_headers=headers,
        response_headers=headers,
        response_status_code=204,
    )

    log_files = list(tmp_path.glob("*.log"))
    assert len(log_files) == 1
    content = log_files[0].read_text(encoding="utf-8")
    assert "Method: GET" in content
    assert "Status Code: 204" in content
    assert "Headers:" not in content
