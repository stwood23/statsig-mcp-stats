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


class MetricResult(TypedDict, total=False):
    """Result data for a specific metric in an experiment."""
    
    metric_id: str
    metric_name: str
    metric_type: str
    control_value: float | None
    test_value: float | None
    lift: float | None
    lift_ci_lower: float | None
    lift_ci_upper: float | None
    p_value: float | None
    significance: str | None
    sample_size_control: int | None
    sample_size_test: int | None


class ExperimentResultData(TypedDict, total=False):
    """Comprehensive experiment results data."""
    
    experiment_id: str
    experiment_name: str
    status: str
    start_date: str | None
    end_date: str | None
    sample_size: int | None
    primary_metrics: list[MetricResult]
    secondary_metrics: list[MetricResult] 
    health_metrics: list[MetricResult]
    overall_significance: str | None
    recommendation: str | None


class PulseReportData(TypedDict, total=False):
    """Pulse report data with health and performance indicators."""
    
    experiment_id: str
    report_date: str
    health_score: float | None
    performance_indicators: dict[str, Any]
    alerts: list[dict[str, Any]]
    recommendations: list[str]
    data_quality_score: float | None


class StatisticalAnalysis(TypedDict, total=False):
    """Statistical analysis details for metrics."""
    
    confidence_level: float
    statistical_power: float | None
    effect_size: float | None
    minimum_detectable_effect: float | None
    days_to_significance: int | None
    is_significant: bool
