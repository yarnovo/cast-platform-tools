"""cast.send_dm tool 单测。"""

from __future__ import annotations

from cast_platform_tools.dm import send_dm
from .conftest import FakeResponse


def test_send_dm_calls_messages_endpoint(fake_client) -> None:
    fake_client.responses["/api/messages"] = FakeResponse(
        201,
        {"id": 42, "from_user_id": "u_ag_xxx", "to_user_id": "u_alice", "content": "hi"},
    )

    result = send_dm(
        agent_persona_id="u_ag_xxx",
        to_user_id="u_alice",
        content="hi",
    )

    assert result == {"message_id": 42, "to_user_id": "u_alice"}
    assert len(fake_client.calls) == 1
    call = fake_client.calls[0]
    assert call["url"] == "/api/messages?user_id=u_ag_xxx"
    assert call["json"] == {"to_user_id": "u_alice", "content": "hi"}
