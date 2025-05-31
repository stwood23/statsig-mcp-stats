"""
Statsig client wrapper for MCP server.
"""

import logging
import os
from typing import Any, Dict, Optional, Union

try:
    from statsig_python_core import Statsig, StatsigOptions, StatsigUser
    USING_CORE_SDK = True
except ImportError:
    # Fallback to legacy SDK if core is not available
    try:
        from statsig import StatsigOptions, StatsigUser, statsig
        Statsig = statsig
        USING_CORE_SDK = False
    except ImportError:
        raise ImportError(
            "Statsig Python SDK not found. Install with: pip install statsig-python-core or pip install statsig"
        )

from .types import (DynamicConfigResult, EventLogResult, ExperimentResult,
                    FeatureGateResult, LayerResult, StatsigUserAttributes)

logger = logging.getLogger(__name__)


class StatsigMCPClient:
    """Wrapper around Statsig SDK for MCP server."""

    def __init__(self) -> None:
        """Initialize the Statsig client."""
        self._initialized = False
        self._statsig = None

    async def initialize(self) -> None:
        """Initialize the Statsig SDK."""
        if self._initialized:
            return

        # Get configuration from environment variables
        secret_key = os.getenv("STATSIG_SERVER_SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "STATSIG_SERVER_SECRET_KEY environment variable is required"
            )

        environment = os.getenv("STATSIG_ENVIRONMENT", "development")
        timeout_ms = int(os.getenv("STATSIG_API_TIMEOUT", "3000"))
        disable_logging = os.getenv("STATSIG_DISABLE_LOGGING", "false").lower() == "true"
        debug = os.getenv("STATSIG_DEBUG", "false").lower() == "true"

        try:
            if USING_CORE_SDK:
                # Configure Statsig options for core SDK
                options = StatsigOptions()
                options.environment = environment
                options.init_timeout_ms = timeout_ms
                options.disable_all_logging = disable_logging

                if debug:
                    options.output_log_level = "debug"

                # Initialize Statsig core SDK
                self._statsig = Statsig(secret_key, options)
                await self._statsig.initialize()
            else:
                # Configure Statsig options for legacy SDK
                options = StatsigOptions()
                options.tier = environment
                options.init_timeout = timeout_ms // 1000  # Convert to seconds for legacy SDK
                options.local_mode = False
                options.disable_all_logging = disable_logging

                # Initialize legacy Statsig SDK (synchronous)
                self._statsig = Statsig
                self._statsig.initialize(secret_key, options)

            self._initialized = True
            logger.info(f"Statsig {'core' if USING_CORE_SDK else 'legacy'} SDK initialized successfully for environment: {environment}")
        except Exception as e:
            logger.error(f"Failed to initialize Statsig: {e}")
            raise

    def _create_statsig_user(self, user_attrs: Dict[str, Any]) -> StatsigUser:
        """Create a StatsigUser object from user attributes."""
        user_data = {
            "user_id": user_attrs["user_id"],
        }

        # Add optional fields if provided
        if user_attrs.get("user_email"):
            user_data["email"] = user_attrs["user_email"]
        if user_attrs.get("user_country"):
            user_data["country"] = user_attrs["user_country"]
        if user_attrs.get("user_ip"):
            user_data["ip"] = user_attrs["user_ip"]
        if user_attrs.get("user_agent"):
            user_data["user_agent"] = user_attrs["user_agent"]
        if user_attrs.get("app_version"):
            user_data["app_version"] = user_attrs["app_version"]
        if user_attrs.get("locale"):
            user_data["locale"] = user_attrs["locale"]
        if user_attrs.get("custom_attributes"):
            user_data["custom"] = user_attrs["custom_attributes"]
        if user_attrs.get("private_attributes"):
            user_data["private_attributes"] = user_attrs["private_attributes"]

        return StatsigUser(**user_data)

    async def check_feature_gate(
        self, user_attrs: Dict[str, Any], gate_name: str
    ) -> FeatureGateResult:
        """Check if a feature gate is enabled for a user."""
        if not self._initialized:
            raise RuntimeError("Statsig client not initialized")

        user = self._create_statsig_user(user_attrs)
        
        try:
            if USING_CORE_SDK:
                gate = self._statsig.get_feature_gate(user, gate_name)
            else:
                gate = self._statsig.get_feature_gate(user, gate_name)
            
            return FeatureGateResult(
                gate_name=gate_name,
                value=gate.value if hasattr(gate, 'value') else gate.get_value(),
                rule_id=gate.rule_id if hasattr(gate, 'rule_id') else "unknown",
                group_name=getattr(gate, 'group_name', None)
            )
        except Exception as e:
            logger.error(f"Error checking feature gate {gate_name}: {e}")
            # Return default false value for feature gates
            return FeatureGateResult(
                gate_name=gate_name,
                value=False,
                rule_id="error",
                group_name=None
            )

    async def get_dynamic_config(
        self, user_attrs: Dict[str, Any], config_name: str
    ) -> DynamicConfigResult:
        """Get dynamic configuration for a user."""
        if not self._initialized:
            raise RuntimeError("Statsig client not initialized")

        user = self._create_statsig_user(user_attrs)
        
        try:
            if USING_CORE_SDK:
                config = self._statsig.get_dynamic_config(user, config_name)
            else:
                config = self._statsig.get_config(user, config_name)
            
            # Convert config to dictionary
            config_value = {}
            if hasattr(config, 'value'):
                config_value = config.value
            elif hasattr(config, 'get_value'):
                config_value = config.get_value()

            return DynamicConfigResult(
                config_name=config_name,
                value=config_value,
                rule_id=getattr(config, 'rule_id', 'unknown'),
                group_name=getattr(config, 'group_name', None)
            )
        except Exception as e:
            logger.error(f"Error getting dynamic config {config_name}: {e}")
            return DynamicConfigResult(
                config_name=config_name,
                value={},
                rule_id="error",
                group_name=None
            )

    async def get_experiment(
        self, user_attrs: Dict[str, Any], experiment_name: str
    ) -> ExperimentResult:
        """Get experiment assignment for a user."""
        if not self._initialized:
            raise RuntimeError("Statsig client not initialized")

        user = self._create_statsig_user(user_attrs)
        
        try:
            experiment = self._statsig.get_experiment(user, experiment_name)
            
            # Convert experiment to dictionary
            experiment_value = {}
            if hasattr(experiment, 'value'):
                experiment_value = experiment.value
            elif hasattr(experiment, 'get_value'):
                experiment_value = experiment.get_value()

            return ExperimentResult(
                experiment_name=experiment_name,
                value=experiment_value,
                rule_id=getattr(experiment, 'rule_id', 'unknown'),
                group_name=getattr(experiment, 'group_name', None)
            )
        except Exception as e:
            logger.error(f"Error getting experiment {experiment_name}: {e}")
            return ExperimentResult(
                experiment_name=experiment_name,
                value={},
                rule_id="error",
                group_name=None
            )

    async def get_layer(
        self, user_attrs: Dict[str, Any], layer_name: str
    ) -> LayerResult:
        """Get layer parameters for a user."""
        if not self._initialized:
            raise RuntimeError("Statsig client not initialized")

        user = self._create_statsig_user(user_attrs)
        
        try:
            layer = self._statsig.get_layer(user, layer_name)
            
            # Convert layer to dictionary
            layer_value = {}
            if hasattr(layer, 'value'):
                layer_value = layer.value
            elif hasattr(layer, 'get_values'):
                layer_value = layer.get_values()

            return LayerResult(
                layer_name=layer_name,
                value=layer_value,
                rule_id=getattr(layer, 'rule_id', 'unknown'),
                allocated_experiment_name=getattr(layer, 'allocated_experiment_name', None)
            )
        except Exception as e:
            logger.error(f"Error getting layer {layer_name}: {e}")
            return LayerResult(
                layer_name=layer_name,
                value={},
                rule_id="error",
                allocated_experiment_name=None
            )

    async def log_event(
        self,
        user_attrs: Dict[str, Any],
        event_name: str,
        value: Optional[Union[str, int, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EventLogResult:
        """Log a custom event."""
        if not self._initialized:
            raise RuntimeError("Statsig client not initialized")

        user = self._create_statsig_user(user_attrs)
        
        try:
            if USING_CORE_SDK:
                self._statsig.log_event(
                    user=user,
                    event_name=event_name,
                    value=value,
                    metadata=metadata or {}
                )
            else:
                # Legacy SDK uses different API
                from statsig.statsig_event import StatsigEvent
                event = StatsigEvent(user, event_name, value, metadata or {})
                self._statsig.log_event(event)
            
            return EventLogResult(
                success=True,
                message=f"Event '{event_name}' logged successfully"
            )
        except Exception as e:
            logger.error(f"Error logging event {event_name}: {e}")
            return EventLogResult(
                success=False,
                message=f"Failed to log event: {str(e)}"
            )

    async def shutdown(self) -> None:
        """Shutdown the Statsig client."""
        if self._initialized and self._statsig:
            try:
                if USING_CORE_SDK:
                    await self._statsig.shutdown()
                else:
                    self._statsig.shutdown()
                logger.info("Statsig client shutdown successfully")
            except Exception as e:
                logger.error(f"Error shutting down Statsig client: {e}")
            finally:
                self._initialized = False
                self._statsig = None 