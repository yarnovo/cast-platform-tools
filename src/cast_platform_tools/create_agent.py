"""cast.create_agent · meta-only · 创建新 agent。"""

from __future__ import annotations

from akong_tools import register_tool

from .client import cast_api


@register_tool("cast.create_agent")
def create_agent(
    *,
    owner_id: str,
    name: str,
    soul: str | None = None,
    playbook: str | None = None,
    tagline: str | None = None,
) -> dict:
    """创建一个新虚拟角色 agent (cast 平台层 meta agent 才有此 tool 权限)。

    Args:
        owner_id: harness 注入 · 真人 owner 的 user_id (从当前 agent.created_by 推)
        name: 新 agent 显示名 · 必填
        soul: 人设详细 markdown · 可选
        playbook: 运营守则 markdown · 可选
        tagline: 一句话介绍 · 可选

    Returns:
        {"agent_id": "ag_xxx", "persona_user_id": "u_ag_xxx"}
    """
    body: dict = {"name": name}
    if soul is not None:
        body["soul"] = soul
    if playbook is not None:
        body["playbook"] = playbook
    if tagline is not None:
        body["tagline"] = tagline
    r = cast_api.post(f"/api/agents?owner_id={owner_id}", json=body)
    r.raise_for_status()
    data = r.json()
    return {
        "agent_id": data.get("id"),
        "persona_user_id": (data.get("persona") or {}).get("id"),
    }
