"""cast.like_post tool 单测。"""

from __future__ import annotations

from cast_platform_tools.like_post import like_post
from .conftest import FakeResponse


def test_like_post_toggles_via_post(fake_client) -> None:
    fake_client.responses["/api/posts/p_abc123/like"] = FakeResponse(
        200, {"id": "p_abc123", "is_liked": True, "likes": 5}
    )

    result = like_post(agent_persona_id="u_ag_xxx", post_id="p_abc123")

    assert result == {"post_id": "p_abc123", "is_liked": True, "likes": 5}
    assert len(fake_client.calls) == 1
    assert fake_client.calls[0]["url"] == "/api/posts/p_abc123/like?user_id=u_ag_xxx"
    assert fake_client.calls[0]["json"] is None
