"""
Type definitions for Statsig MCP server.
"""

from typing import Any, Dict, Optional

from typing_extensions import TypedDict


class StatsigUserAttributes(TypedDict, total=False):
    """User attributes for Statsig user object."""
    user_id: str
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]] 