"""cast-api HTTP client · 单例 httpx.Client · 5s timeout · 3 retry。"""

from __future__ import annotations

import os

import httpx

DEFAULT_BASE_URL = "https://api.cast.agentaily.com"


def _build_client() -> httpx.Client:
    base_url = os.environ.get("CAST_API_BASE_URL", DEFAULT_BASE_URL)
    transport = httpx.HTTPTransport(retries=3)
    return httpx.Client(
        base_url=base_url,
        timeout=5.0,
        transport=transport,
        headers={"User-Agent": "cast-platform-tools/0.1"},
    )


# module-level 单例 · 测试可 monkeypatch
cast_api: httpx.Client = _build_client()


def reset_client() -> None:
    """测试 hook · 重建单例 (例如改 env 后)"""
    global cast_api
    try:
        cast_api.close()
    except Exception:
        pass
    cast_api = _build_client()
