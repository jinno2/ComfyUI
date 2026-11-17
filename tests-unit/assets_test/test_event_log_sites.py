import asyncio
from unittest.mock import Mock

import pytest

import server


@pytest.fixture(autouse=True)
def autoclean_unit_test_assets():
    yield


@pytest.mark.asyncio
@pytest.mark.parametrize("enabled,hashing_enabled", [(False, False), (True, False), (True, True)])
async def test_assets_enabled_event(monkeypatch, tmp_path, enabled, hashing_enabled):
    monkeypatch.setattr(server.args, "front_end_root", str(tmp_path))
    monkeypatch.setattr(server.args, "enable_asset_hashing", hashing_enabled)
    monkeypatch.setattr(server.PromptServer, "instance", None, raising=False)
    for name in ("UserManager", "ModelFileManager", "CustomNodeManager", "SubgraphManager", "NodeReplaceManager", "InternalRoutes"):
        monkeypatch.setattr(server, name, Mock())
    monkeypatch.setattr(server.execution, "PromptQueue", Mock())
    emit = Mock()
    monkeypatch.setattr(server, "emit", emit)
    asset_manager = Mock(enabled=enabled)

    server.PromptServer(asyncio.get_running_loop(), asset_manager)

    if enabled:
        emit.assert_called_once_with("assets.enabled", hashing_enabled=hashing_enabled)
    else:
        emit.assert_not_called()
