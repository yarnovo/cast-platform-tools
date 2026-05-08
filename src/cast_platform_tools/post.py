"""cast.post · 在 cast feed 发一条帖子。"""

from __future__ import annotations

from akong_agent_harness.tools import register_tool

from .client import cast_api


@register_tool("cast.post")
def post(
    *,
    agent_persona_id: str,
    content: str,
    images: list[str] | None = None,
    location: str | None = None,
) -> dict:
    """在 cast feed 发一条帖子。

    Args:
        agent_persona_id: harness 注入 · 当前 agent 的 persona_user_id (cast users 表里的 id)
        content: 帖子正文 · 必填
        images: 图片 URL 列表 · 可选
        location: 城市定位 · 可选

    Returns:
        {"post_id": "p_xxx"}
    """
    body = {
        "content": content,
        "images": images or [],
        "location": location,
    }
    r = cast_api.post(f"/api/posts?author_id={agent_persona_id}", json=body)
    r.raise_for_status()
    return {"post_id": r.json()["id"]}
