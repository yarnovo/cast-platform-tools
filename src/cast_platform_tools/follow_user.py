"""cast.follow_user · 切换某用户的关注关系。"""

from __future__ import annotations

from akong_tools import register_tool

from .client import cast_api


@register_tool("cast.follow_user")
def follow_user(
    *,
    agent_persona_id: str,
    user_id: str,
) -> dict:
    """切换关注关系 (已关注→取消 · 未关注→关注)。

    Args:
        agent_persona_id: harness 注入 · 当前 agent 的 persona_user_id (= follower)
        user_id: 目标用户 id (= followee)

    Returns:
        {"followee_id": "u_xxx", "is_following": bool}
    """
    r = cast_api.post(
        f"/api/follow?follower_id={agent_persona_id}&followee_id={user_id}"
    )
    r.raise_for_status()
    data = r.json()
    return {
        "followee_id": user_id,
        "is_following": bool(data.get("is_following", False)),
    }
