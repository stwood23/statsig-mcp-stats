"""
Type definitions for Statsig MCP server.
"""

from typing import Any

from typing_extensions import TypedDict


class StatsigUserAttributes(TypedDict, total=False):
    """User attributes for Statsig user object."""

    user_id: str
    user_email: str | None
    user_country: str | None
    user_ip: str | None
    user_agent: str | None
    app_version: str | None
    locale: str | None
    custom_attributes: dict[str, Any] | None
    private_attributes: dict[str, Any] | None
