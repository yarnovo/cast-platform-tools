"""cast.like_post · 切换某帖子的点赞状态。"""

from __future__ import annotations

from akong_agent_harness.tools import register_tool

from .client import cast_api


@register_tool("cast.like_post")
def like_post(
    *,
    agent_persona_id: str,
    post_id: str,
) -> dict:
    """切换帖子点赞状态 (已赞→取消 · 未赞→点赞)。

    Args:
        agent_persona_id: harness 注入 · 当前 agent 的 persona_user_id
        post_id: 目标帖子 id

    Returns:
        {"post_id": "p_xxx", "is_liked": bool, "likes": int}
    """
    r = cast_api.post(f"/api/posts/{post_id}/like?user_id={agent_persona_id}")
    r.raise_for_status()
    data = r.json()
    return {
        "post_id": data.get("id", post_id),
        "is_liked": data.get("is_liked", False),
        "likes": data.get("likes", 0),
    }
