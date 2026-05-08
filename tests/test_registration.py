"""验证 import cast_platform_tools 触发 5 个 tool 全注册到 akong_tools 全局 registry。"""

from __future__ import annotations


def test_all_5_tools_registered() -> None:
    # 清空 registry · 然后重新 import 触发注册
    import importlib

    import akong_tools as harness_tools

    harness_tools.clear_registered_tools()

    import cast_platform_tools  # noqa: F401  — import 触发副作用

    # 即使被前一个测试 import 过 · clear 后需要 reload 各子模块 · 重新装饰器执行
    for sub in (
        "cast_platform_tools.post",
        "cast_platform_tools.dm",
        "cast_platform_tools.like_post",
        "cast_platform_tools.follow_user",
        "cast_platform_tools.create_agent",
    ):
        importlib.reload(importlib.import_module(sub))

    registered = set(harness_tools.all_registered_tools().keys())
    expected = {
        "cast.post",
        "cast.send_dm",
        "cast.like_post",
        "cast.follow_user",
        "cast.create_agent",
    }
    assert expected.issubset(registered), (
        f"expected {expected} ⊆ registered · got registered={registered}"
    )
    assert len(expected) == 5
