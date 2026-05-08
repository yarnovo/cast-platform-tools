"""cast.follow_user tool 单测。"""

from __future__ import annotations

from cast_platform_tools.follow_user import follow_user
from .conftest import FakeResponse


def test_follow_user_toggles(fake_client) -> None:
    fake_client.responses["/api/follow"] = FakeResponse(200, {"is_following": True})

    result = follow_user(agent_persona_id="u_ag_xxx", user_id="u_alice")

    assert result == {"followee_id": "u_alice", "is_following": True}
    assert len(fake_client.calls) == 1
    assert (
        fake_client.calls[0]["url"]
        == "/api/follow?follower_id=u_ag_xxx&followee_id=u_alice"
    )
