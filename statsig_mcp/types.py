"""
Type definitions for Statsig MCP server.
"""

from typing import Any, Dict, Optional, Union

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


class FeatureGateCheckRequest(TypedDict):
    """Request for checking a feature gate."""
    user_id: str
    gate_name: str
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]]


class DynamicConfigRequest(TypedDict):
    """Request for getting dynamic config."""
    user_id: str
    config_name: str
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]]


class ExperimentRequest(TypedDict):
    """Request for getting experiment."""
    user_id: str
    experiment_name: str
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]]


class LayerRequest(TypedDict):
    """Request for getting layer."""
    user_id: str
    layer_name: str
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]]


class LogEventRequest(TypedDict):
    """Request for logging an event."""
    user_id: str
    event_name: str
    value: Optional[Union[str, int, float]]
    metadata: Optional[Dict[str, Any]]
    user_email: Optional[str]
    user_country: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    app_version: Optional[str]
    locale: Optional[str]
    custom_attributes: Optional[Dict[str, Any]]
    private_attributes: Optional[Dict[str, Any]]


class FeatureGateResult(TypedDict):
    """Result from checking a feature gate."""
    gate_name: str
    value: bool
    rule_id: str
    group_name: Optional[str]


class DynamicConfigResult(TypedDict):
    """Result from getting dynamic config."""
    config_name: str
    value: Dict[str, Any]
    rule_id: str
    group_name: Optional[str]


class ExperimentResult(TypedDict):
    """Result from getting experiment."""
    experiment_name: str
    value: Dict[str, Any]
    rule_id: str
    group_name: Optional[str]


class LayerResult(TypedDict):
    """Result from getting layer."""
    layer_name: str
    value: Dict[str, Any]
    rule_id: str
    allocated_experiment_name: Optional[str]


class EventLogResult(TypedDict):
    """Result from logging an event."""
    success: bool
    message: str 