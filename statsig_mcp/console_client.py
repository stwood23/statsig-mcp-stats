"""
Statsig Console API client for MCP server.
"""

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class StatsigConsoleClient:
    """Console API client for Statsig."""

    def __init__(self) -> None:
        """Initialize the Console API client."""
        self._initialized = False
        self._console_api_key: str | None = None
        self._api_version = "20240601"
        self._base_url = "https://statsigapi.net"
        self._client: httpx.AsyncClient | None = None

    async def initialize(self) -> None:
        """Initialize the Console API client."""
        if self._initialized:
            return

        # Get Console API key from environment
        self._console_api_key = os.getenv("STATSIG_CONSOLE_API_KEY")
        if not self._console_api_key:
            raise ValueError("STATSIG_CONSOLE_API_KEY environment variable is required")

        # Create HTTP client with proper headers for Console API
        console_headers = {
            "STATSIG-API-KEY": self._console_api_key,
            "STATSIG-API-VERSION": self._api_version,
            "Content-Type": "application/json",
        }

        self._client = httpx.AsyncClient(
            base_url=self._base_url, headers=console_headers, timeout=30.0
        )

        self._initialized = True
        logger.info("Statsig Console API client initialized successfully")

    # Gates
    async def list_gates(self, limit: int | None = None) -> dict[str, Any]:
        """List all feature gates."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            url = "/console/v1/gates"
            if limit:
                url += f"?limit={limit}"

            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing gates: {e}")
            return {"error": str(e)}

    async def get_gate(self, gate_id: str) -> dict[str, Any]:
        """Get details of a specific feature gate."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(f"/console/v1/gates/{gate_id}")
            if response.status_code == 404:
                return {"found": False, "error": f"Gate '{gate_id}' not found"}

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting gate {gate_id}: {e}")
            return {"error": str(e)}

    async def create_gate(
        self, name: str, description: str = "", is_enabled: bool = False
    ) -> dict[str, Any]:
        """Create a new feature gate."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            data = {"name": name, "description": description, "isEnabled": is_enabled}

            response = await self._client.post("/console/v1/gates", json=data)
            response.raise_for_status()
            result = response.json()
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error creating gate {name}: {e}")
            return {"success": False, "error": str(e)}

    async def update_gate(
        self, gate_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing feature gate."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            # Convert updates to API format
            data = {}
            if "name" in updates:
                data["name"] = updates["name"]
            if "description" in updates:
                data["description"] = updates["description"]
            if "is_enabled" in updates:
                data["isEnabled"] = updates["is_enabled"]

            response = await self._client.patch(
                f"/console/v1/gates/{gate_id}", json=data
            )
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating gate {gate_id}: {e}")
            return {"success": False, "error": str(e)}

    async def delete_gate(self, gate_id: str) -> dict[str, Any]:
        """Delete a feature gate."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.delete(f"/console/v1/gates/{gate_id}")
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting gate {gate_id}: {e}")
            return {"success": False, "error": str(e)}

    # Experiments
    async def list_experiments(self, limit: int | None = None) -> dict[str, Any]:
        """List all experiments."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            url = "/console/v1/experiments"
            if limit:
                url += f"?limit={limit}"

            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing experiments: {e}")
            return {"error": str(e)}

    async def get_experiment(self, experiment_id: str) -> dict[str, Any]:
        """Get details of a specific experiment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(
                f"/console/v1/experiments/{experiment_id}"
            )
            if response.status_code == 404:
                return {
                    "found": False,
                    "error": f"Experiment '{experiment_id}' not found",
                }

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting experiment {experiment_id}: {e}")
            return {"error": str(e)}

    async def create_experiment(
        self, name: str, description: str = "", hypothesis: str | None = None
    ) -> dict[str, Any]:
        """Create a new experiment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            data = {"name": name, "description": description}
            if hypothesis:
                data["hypothesis"] = hypothesis

            response = await self._client.post("/console/v1/experiments", json=data)
            response.raise_for_status()
            result = response.json()
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error creating experiment {name}: {e}")
            return {"success": False, "error": str(e)}

    async def update_experiment(
        self, experiment_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing experiment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.patch(
                f"/console/v1/experiments/{experiment_id}", json=updates
            )
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating experiment {experiment_id}: {e}")
            return {"success": False, "error": str(e)}

    async def delete_experiment(self, experiment_id: str) -> dict[str, Any]:
        """Delete an experiment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.delete(
                f"/console/v1/experiments/{experiment_id}"
            )
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting experiment {experiment_id}: {e}")
            return {"success": False, "error": str(e)}

    # Dynamic Configs
    async def list_dynamic_configs(self, limit: int | None = None) -> dict[str, Any]:
        """List all dynamic configs."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            url = "/console/v1/dynamic_configs"
            if limit:
                url += f"?limit={limit}"

            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing dynamic configs: {e}")
            return {"error": str(e)}

    async def get_dynamic_config(self, config_id: str) -> dict[str, Any]:
        """Get details of a specific dynamic config."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(
                f"/console/v1/dynamic_configs/{config_id}"
            )
            if response.status_code == 404:
                return {
                    "found": False,
                    "error": f"Dynamic config '{config_id}' not found",
                }

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting dynamic config {config_id}: {e}")
            return {"error": str(e)}

    async def create_dynamic_config(
        self, name: str, description: str = ""
    ) -> dict[str, Any]:
        """Create a new dynamic config."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            data = {"name": name, "description": description}

            response = await self._client.post("/console/v1/dynamic_configs", json=data)
            response.raise_for_status()
            result = response.json()
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error creating dynamic config {name}: {e}")
            return {"success": False, "error": str(e)}

    async def update_dynamic_config(
        self, config_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing dynamic config."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.patch(
                f"/console/v1/dynamic_configs/{config_id}", json=updates
            )
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error updating dynamic config {config_id}: {e}")
            return {"success": False, "error": str(e)}

    async def delete_dynamic_config(self, config_id: str) -> dict[str, Any]:
        """Delete a dynamic config."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.delete(
                f"/console/v1/dynamic_configs/{config_id}"
            )
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting dynamic config {config_id}: {e}")
            return {"success": False, "error": str(e)}

    # Segments
    async def list_segments(self, limit: int | None = None) -> dict[str, Any]:
        """List all segments."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            url = "/console/v1/segments"
            if limit:
                url += f"?limit={limit}"

            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing segments: {e}")
            return {"error": str(e)}

    async def get_segment(self, segment_id: str) -> dict[str, Any]:
        """Get details of a specific segment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(f"/console/v1/segments/{segment_id}")
            if response.status_code == 404:
                return {"found": False, "error": f"Segment '{segment_id}' not found"}

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting segment {segment_id}: {e}")
            return {"error": str(e)}

    async def create_segment(self, name: str, description: str = "") -> dict[str, Any]:
        """Create a new segment."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            data = {"name": name, "description": description}

            response = await self._client.post("/console/v1/segments", json=data)
            response.raise_for_status()
            result = response.json()
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error creating segment {name}: {e}")
            return {"success": False, "error": str(e)}

    # Metrics
    async def list_metrics(self, limit: int | None = None) -> dict[str, Any]:
        """List all metrics."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            url = "/console/v1/metrics"
            if limit:
                url += f"?limit={limit}"

            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing metrics: {e}")
            return {"error": str(e)}

    async def get_metric(self, metric_id: str) -> dict[str, Any]:
        """Get details of a specific metric."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(f"/console/v1/metrics/{metric_id}")
            if response.status_code == 404:
                return {"found": False, "error": f"Metric '{metric_id}' not found"}

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting metric {metric_id}: {e}")
            return {"error": str(e)}

    # Audit Logs
    async def list_audit_logs(
        self, limit: int = 20, from_date: str | None = None, to_date: str | None = None
    ) -> dict[str, Any]:
        """List audit logs."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            params = {"limit": limit}
            if from_date:
                params["from"] = from_date
            if to_date:
                params["to"] = to_date

            response = await self._client.get("/console/v1/audit_logs", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing audit logs: {e}")
            return {"error": str(e)}

    # Target Apps
    async def list_target_apps(self) -> dict[str, Any]:
        """List all target apps."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get("/console/v1/target_apps")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing target apps: {e}")
            return {"error": str(e)}

    async def get_target_app(self, app_id: str) -> dict[str, Any]:
        """Get details of a specific target app."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(f"/console/v1/target_apps/{app_id}")
            if response.status_code == 404:
                return {"found": False, "error": f"Target app '{app_id}' not found"}

            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting target app {app_id}: {e}")
            return {"error": str(e)}

    # API Keys
    async def list_api_keys(self) -> dict[str, Any]:
        """List all API keys."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get("/console/v1/keys")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing API keys: {e}")
            return {"error": str(e)}

    # Events (keeping existing functionality)
    async def query_events(
        self, event_name: str | None = None, limit: int = 10
    ) -> dict[str, Any]:
        """Query events using Console API - shows event types, not user-specific events."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            if event_name:
                # Get specific event details
                response = await self._client.get(f"/console/v1/events/{event_name}")
                if response.status_code == 404:
                    return {
                        "event_name": event_name,
                        "found": False,
                        "message": f"Event '{event_name}' not found",
                    }
                response.raise_for_status()
                data = response.json()
                return {"event_name": event_name, "found": True, "details": data}
            else:
                # List all events
                response = await self._client.get("/console/v1/events")
                response.raise_for_status()
                data = response.json()

                events = data.get("data", [])[:limit]

                return {
                    "event_types": events,
                    "total_found": len(events),
                    "note": "This shows event types, not user-specific events. Use Statsig Console for user event history.",
                }

        except Exception as e:
            logger.error(f"Error querying events: {e}")
            return {
                "error": str(e),
                "message": "Failed to query events via Console API",
            }

    # Users (keeping existing functionality)
    async def get_user_by_email(self, email: str) -> dict[str, Any]:
        """Get user by email using Console API."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get(f"/console/v1/users/{email}")

            if response.status_code == 404:
                return {
                    "email": email,
                    "found": False,
                    "message": f"User with email '{email}' not found in Statsig team",
                }

            response.raise_for_status()
            data = response.json()

            return {
                "email": email,
                "found": True,
                "user_data": data,
                "note": "This shows team member info, not end-user data",
            }

        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return {
                "email": email,
                "found": False,
                "error": str(e),
                "message": "Failed to get user via Console API",
            }

    async def list_team_users(self) -> dict[str, Any]:
        """List team users using Console API."""
        if not self._initialized or not self._client:
            raise RuntimeError("Console API client not initialized")

        try:
            response = await self._client.get("/console/v1/users")
            response.raise_for_status()
            data = response.json()

            users = data.get("data", [])

            return {
                "team_users": users,
                "total_users": len(users),
                "note": "These are team members, not end-users",
            }

        except Exception as e:
            logger.error(f"Error listing team users: {e}")
            return {
                "error": str(e),
                "message": "Failed to list team users via Console API",
            }

    # Experiment Results and Analytics
    async def get_experiment_results(self, experiment_id: str, include_metrics: bool = True) -> dict[str, Any]:
        """Get comprehensive experiment results including statistical analysis."""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        
        try:
            url = f"/console/v1/experiments/{experiment_id}/results"
            params = {"include_metrics": "true" if include_metrics else "false"}
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved results for experiment {experiment_id}")
            return {"success": True, "data": data, "error": None}
        except Exception as e:
            logger.error(f"Error getting experiment results for {experiment_id}: {e}")
            return {"success": False, "data": {}, "error": str(e)}

    async def get_experiment_pulse(self, experiment_id: str) -> dict[str, Any]:
        """Get experiment pulse data with health metrics and performance indicators."""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        
        try:
            url = f"/console/v1/experiments/{experiment_id}/pulse"
            response = await self._client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved pulse data for experiment {experiment_id}")
            return {"success": True, "data": data, "error": None}
        except Exception as e:
            logger.error(f"Error getting experiment pulse for {experiment_id}: {e}")
            return {"success": False, "data": {}, "error": str(e)}

    async def get_metric_details(self, metric_id: str, experiment_id: str) -> dict[str, Any]:
        """Get detailed metric analysis including statistical significance."""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        
        try:
            url = f"/console/v1/experiments/{experiment_id}/metrics/{metric_id}"
            response = await self._client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved metric details for {metric_id} in experiment {experiment_id}")
            return {"success": True, "data": data, "error": None}
        except Exception as e:
            logger.error(f"Error getting metric details for {metric_id} in experiment {experiment_id}: {e}")
            return {"success": False, "data": {}, "error": str(e)}

    async def export_pulse_report(self, experiment_id: str, format: str = "json") -> dict[str, Any]:
        """Export comprehensive pulse report in specified format."""
        if not self._initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        
        try:
            url = f"/console/v1/experiments/{experiment_id}/pulse/export"
            params = {"format": format}
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Exported pulse report for experiment {experiment_id} in {format} format")
            return {"success": True, "data": data, "error": None}
        except Exception as e:
            logger.error(f"Error exporting pulse report for {experiment_id}: {e}")
            return {"success": False, "data": {}, "error": str(e)}

    async def shutdown(self) -> None:
        """Shutdown the Console API client."""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._initialized = False
        logger.info("Statsig Console API client shutdown")
