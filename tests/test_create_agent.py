"""cast.create_agent tool 单测 · meta-only。"""

from __future__ import annotations

from cast_platform_tools.create_agent import create_agent
from .conftest import FakeResponse


def test_create_agent_passes_owner_id_query_and_body(fake_client) -> None:
    fake_client.responses["/api/agents"] = FakeResponse(
        201,
        {
            "id": "ag_new123",
            "name": "心理咨询师小阿",
            "persona": {"id": "u_ag_new123", "name": "心理咨询师小阿"},
            "owner_id": "u_owner",
        },
    )

    result = create_agent(
        owner_id="u_owner",
        name="心理咨询师小阿",
        soul="温柔 · 倾听 · 不评判",
        playbook="不接传销 · 24h 内回复私信",
    )

    assert result == {"agent_id": "ag_new123", "persona_user_id": "u_ag_new123"}
    assert len(fake_client.calls) == 1
    call = fake_client.calls[0]
    assert call["url"] == "/api/agents?owner_id=u_owner"
    assert call["json"] == {
        "name": "心理咨询师小阿",
        "soul": "温柔 · 倾听 · 不评判",
        "playbook": "不接传销 · 24h 内回复私信",
    }
