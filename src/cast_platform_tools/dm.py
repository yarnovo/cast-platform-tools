"""cast.send_dm · 给某用户私信。"""

from __future__ import annotations

from akong_tools import register_tool

from .client import cast_api


@register_tool("cast.send_dm")
def send_dm(
    *,
    agent_persona_id: str,
    to_user_id: str,
    content: str,
) -> dict:
    """给某 cast 用户发一条私信。

    Args:
        agent_persona_id: harness 注入 · 发送方 (当前 agent 的 persona_user_id)
        to_user_id: 接收方 user_id
        content: 私信正文

    Returns:
        {"message_id": <int>, "to_user_id": "u_xxx"}
    """
    body = {"to_user_id": to_user_id, "content": content}
    # cast-api messages router 用 query 参数名 user_id (= 发送方)
    r = cast_api.post(f"/api/messages?user_id={agent_persona_id}", json=body)
    r.raise_for_status()
    data = r.json()
    return {"message_id": data.get("id"), "to_user_id": data.get("to_user_id")}
