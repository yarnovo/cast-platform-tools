"""cast.post tool 单测 · mock cast-api。"""

from __future__ import annotations

from cast_platform_tools.post import post
from .conftest import FakeResponse


def test_post_calls_cast_api_with_author_id_query(fake_client) -> None:
    fake_client.responses["/api/posts"] = FakeResponse(
        201, {"id": "p_abc123", "content": "hello cast"}
    )

    result = post(
        agent_persona_id="u_ag_xxx",
        content="hello cast",
        images=["https://x.com/a.jpg"],
        location="上海",
    )

    assert result == {"post_id": "p_abc123"}
    assert len(fake_client.calls) == 1
    call = fake_client.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "/api/posts?author_id=u_ag_xxx"
    assert call["json"] == {
        "content": "hello cast",
        "images": ["https://x.com/a.jpg"],
        "location": "上海",
    }
