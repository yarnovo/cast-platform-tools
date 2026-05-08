"""测试公共 fixture · mock cast-api HTTP client + registry 清理。"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from cast_platform_tools import client as client_mod


class FakeResponse:
    def __init__(self, status_code: int = 200, json_data: Any = None, text: str = "") -> None:
        self.status_code = status_code
        self._json = json_data if json_data is not None else {}
        self.text = text or ""

    def json(self) -> Any:
        return self._json

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"HTTP {self.status_code}",
                request=httpx.Request("POST", "http://test"),
                response=httpx.Response(self.status_code),
            )


class FakeClient:
    """记录所有调用的 fake httpx.Client。"""

    def __init__(self, responses: dict[str, FakeResponse] | None = None, default: FakeResponse | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self.responses = responses or {}
        self.default = default or FakeResponse(200, {})

    def post(self, url: str, json: Any = None, **kwargs: Any) -> FakeResponse:  # noqa: A002
        self.calls.append({"method": "POST", "url": url, "json": json})
        # 匹配 url path 前缀 (忽略 query string)
        path = url.split("?", 1)[0]
        return self.responses.get(path, self.default)

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"method": "GET", "url": url})
        path = url.split("?", 1)[0]
        return self.responses.get(path, self.default)

    def close(self) -> None:
        pass


@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch) -> FakeClient:
    """替换 cast_platform_tools.client.cast_api 为 FakeClient · 返实例供断言。"""
    fc = FakeClient()
    monkeypatch.setattr(client_mod, "cast_api", fc)
    # 同时替换已被 tool 模块 import 的 cast_api 引用
    from cast_platform_tools import post as post_mod
    from cast_platform_tools import dm as dm_mod
    from cast_platform_tools import like_post as like_mod
    from cast_platform_tools import follow_user as follow_mod
    from cast_platform_tools import create_agent as create_mod

    for mod in (post_mod, dm_mod, like_mod, follow_mod, create_mod):
        monkeypatch.setattr(mod, "cast_api", fc)
    return fc
