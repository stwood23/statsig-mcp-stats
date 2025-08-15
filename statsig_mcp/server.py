#!/usr/bin/env python3
"""
Statsig MCP Server

A Model Context Protocol server that provides access to Statsig feature flags,
dynamic configurations, experiments, and event logging.
"""

import argparse
import asyncio
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .console_client import StatsigConsoleClient

# Initialize the MCP server
server = Server("statsig-mcp")

# Global client instance
statsig_client: StatsigConsoleClient | None = None


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Statsig MCP Server - Model Context Protocol server for Statsig feature flags"
    )

    # Server configuration
    parser.add_argument(
        "--api-key",
        type=str,
        help="Statsig Console API key (can also use STATSIG_CONSOLE_API_KEY env var)",
    )

    # MCP server options
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    return parser.parse_args()


def get_configuration(args: argparse.Namespace) -> dict[str, Any]:
    """Get configuration from args and environment variables."""
    # API Key - prioritize command line arg, then env var
    api_key = args.api_key or os.getenv("STATSIG_CONSOLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Statsig Console API key is required. "
            "Provide via --api-key argument or STATSIG_CONSOLE_API_KEY environment variable."
        )

    return {"api_key": api_key}


@server.list_tools()
async def list_tools() -> list[dict]:
    """List available tools."""
    return [
        {
            "name": "list_gates",
            "description": "List all feature gates",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of gates to return (optional)",
                    }
                },
                "required": [],
            },
        },
        {
            "name": "get_gate",
            "description": "Get details of a specific feature gate",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "gate_id": {
                        "type": "string",
                        "description": "ID of the feature gate",
                    }
                },
                "required": ["gate_id"],
            },
        },
        {
            "name": "create_gate",
            "description": "Create a new feature gate",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the feature gate",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the feature gate",
                    },
                    "is_enabled": {
                        "type": "boolean",
                        "description": "Whether the gate is enabled (default: false)",
                    },
                },
                "required": ["name"],
            },
        },
        {
            "name": "update_gate",
            "description": "Update an existing feature gate",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "gate_id": {
                        "type": "string",
                        "description": "ID of the feature gate",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the feature gate (optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the feature gate (optional)",
                    },
                    "is_enabled": {
                        "type": "boolean",
                        "description": "Whether the gate is enabled (optional)",
                    },
                },
                "required": ["gate_id"],
            },
        },
        {
            "name": "delete_gate",
            "description": "Delete a feature gate",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "gate_id": {
                        "type": "string",
                        "description": "ID of the feature gate",
                    }
                },
                "required": ["gate_id"],
            },
        },
        {
            "name": "list_experiments",
            "description": "List all experiments",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of experiments to return (optional)",
                    }
                },
                "required": [],
            },
        },
        {
            "name": "get_experiment",
            "description": "Get details of a specific experiment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment",
                    }
                },
                "required": ["experiment_id"],
            },
        },
        {
            "name": "create_experiment",
            "description": "Create a new experiment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the experiment"},
                    "description": {
                        "type": "string",
                        "description": "Description of the experiment",
                    },
                    "hypothesis": {
                        "type": "string",
                        "description": "Experiment hypothesis (optional)",
                    },
                },
                "required": ["name"],
            },
        },
        {
            "name": "update_experiment",
            "description": "Update an existing experiment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the experiment (optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the experiment (optional)",
                    },
                    "hypothesis": {
                        "type": "string",
                        "description": "Experiment hypothesis (optional)",
                    },
                },
                "required": ["experiment_id"],
            },
        },
        {
            "name": "delete_experiment",
            "description": "Delete an experiment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment",
                    }
                },
                "required": ["experiment_id"],
            },
        },
        {
            "name": "list_dynamic_configs",
            "description": "List all dynamic configs",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of configs to return (optional)",
                    }
                },
                "required": [],
            },
        },
        {
            "name": "get_dynamic_config",
            "description": "Get details of a specific dynamic config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "config_id": {
                        "type": "string",
                        "description": "ID of the dynamic config",
                    }
                },
                "required": ["config_id"],
            },
        },
        {
            "name": "create_dynamic_config",
            "description": "Create a new dynamic config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the dynamic config",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the dynamic config",
                    },
                },
                "required": ["name"],
            },
        },
        {
            "name": "update_dynamic_config",
            "description": "Update an existing dynamic config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "config_id": {
                        "type": "string",
                        "description": "ID of the dynamic config",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the dynamic config (optional)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the dynamic config (optional)",
                    },
                },
                "required": ["config_id"],
            },
        },
        {
            "name": "delete_dynamic_config",
            "description": "Delete a dynamic config",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "config_id": {
                        "type": "string",
                        "description": "ID of the dynamic config",
                    }
                },
                "required": ["config_id"],
            },
        },
        {
            "name": "list_segments",
            "description": "List all segments",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of segments to return (optional)",
                    }
                },
                "required": [],
            },
        },
        {
            "name": "get_segment",
            "description": "Get details of a specific segment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "segment_id": {"type": "string", "description": "ID of the segment"}
                },
                "required": ["segment_id"],
            },
        },
        {
            "name": "create_segment",
            "description": "Create a new segment",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the segment"},
                    "description": {
                        "type": "string",
                        "description": "Description of the segment",
                    },
                },
                "required": ["name"],
            },
        },
        {
            "name": "list_metrics",
            "description": "List all metrics",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of metrics to return (optional)",
                    }
                },
                "required": [],
            },
        },
        {
            "name": "get_metric",
            "description": "Get details of a specific metric",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "metric_id": {"type": "string", "description": "ID of the metric"}
                },
                "required": ["metric_id"],
            },
        },
        {
            "name": "list_audit_logs",
            "description": "List audit logs",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of logs to return (default: 20)",
                    },
                    "from_date": {
                        "type": "string",
                        "description": "Start date for logs (YYYY-MM-DD format, optional)",
                    },
                    "to_date": {
                        "type": "string",
                        "description": "End date for logs (YYYY-MM-DD format, optional)",
                    },
                },
                "required": [],
            },
        },
        {
            "name": "list_target_apps",
            "description": "List all target apps",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "get_target_app",
            "description": "Get details of a specific target app",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "app_id": {"type": "string", "description": "ID of the target app"}
                },
                "required": ["app_id"],
            },
        },
        {
            "name": "list_api_keys",
            "description": "List all API keys",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        {
            "name": "query_events",
            "description": "Query event types and details using Console API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "description": "Specific event name to query (optional - if not provided, lists all events)",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of events to return (default: 10)",
                    },
                },
                "required": [],
            },
        },
        {
            "name": "get_user_by_email",
            "description": "Get team member info by email using Console API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address of team member",
                    }
                },
                "required": ["email"],
            },
        },
        {
            "name": "list_team_users",
            "description": "List all team members using Console API",
            "inputSchema": {"type": "object", "properties": {}, "required": []},
        },
        # Experiment Results and Analytics
        {
            "name": "get_experiment_results",
            "description": "Get comprehensive experiment results with statistical analysis",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment to get results for",
                    },
                    "include_metrics": {
                        "type": "boolean",
                        "description": "Include detailed metric breakdowns (optional, default: true)",
                        "default": True,
                    },
                },
                "required": ["experiment_id"],
            },
        },
        {
            "name": "get_experiment_pulse", 
            "description": "Get experiment pulse data with health metrics and performance indicators",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment to get pulse data for",
                    },
                },
                "required": ["experiment_id"],
            },
        },
        {
            "name": "get_metric_details",
            "description": "Get detailed metric analysis including statistical significance",
            "inputSchema": {
                "type": "object", 
                "properties": {
                    "metric_id": {
                        "type": "string",
                        "description": "ID of the metric to analyze",
                    },
                    "experiment_id": {
                        "type": "string",
                        "description": "ID of the experiment containing the metric",
                    },
                },
                "required": ["metric_id", "experiment_id"],
            },
        },
        {
            "name": "export_pulse_report",
            "description": "Export comprehensive pulse report in specified format",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "experiment_id": {
                        "type": "string", 
                        "description": "ID of the experiment to export report for",
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format (json, csv, summary)",
                        "enum": ["json", "csv", "summary"],
                        "default": "json",
                    },
                },
                "required": ["experiment_id"],
            },
        },
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Handle tool calls."""
    global statsig_client

    if not statsig_client:
        return [{"type": "text", "text": "Error: Statsig client not initialized"}]

    try:
        # Gates
        if name == "list_gates":
            limit = arguments.get("limit")
            result = await statsig_client.list_gates(limit)
            return [
                {"type": "text", "text": _format_list_result(result, "Feature Gates")}
            ]

        elif name == "get_gate":
            gate_id = arguments["gate_id"]
            result = await statsig_client.get_gate(gate_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Feature Gate", gate_id),
                }
            ]

        elif name == "create_gate":
            name_val = arguments["name"]
            description = arguments.get("description", "")
            is_enabled = arguments.get("is_enabled", False)
            result = await statsig_client.create_gate(name_val, description, is_enabled)
            return [
                {
                    "type": "text",
                    "text": _format_create_result(result, "Feature Gate", name_val),
                }
            ]

        elif name == "update_gate":
            gate_id = arguments["gate_id"]
            updates = {k: v for k, v in arguments.items() if k != "gate_id"}
            result = await statsig_client.update_gate(gate_id, updates)
            return [
                {
                    "type": "text",
                    "text": _format_update_result(result, "Feature Gate", gate_id),
                }
            ]

        elif name == "delete_gate":
            gate_id = arguments["gate_id"]
            result = await statsig_client.delete_gate(gate_id)
            return [
                {
                    "type": "text",
                    "text": _format_delete_result(result, "Feature Gate", gate_id),
                }
            ]

        # Experiments
        elif name == "list_experiments":
            limit = arguments.get("limit")
            result = await statsig_client.list_experiments(limit)
            return [
                {"type": "text", "text": _format_list_result(result, "Experiments")}
            ]

        elif name == "get_experiment":
            experiment_id = arguments["experiment_id"]
            result = await statsig_client.get_experiment(experiment_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Experiment", experiment_id),
                }
            ]

        elif name == "create_experiment":
            name_val = arguments["name"]
            description = arguments.get("description", "")
            hypothesis = arguments.get("hypothesis")
            result = await statsig_client.create_experiment(
                name_val, description, hypothesis
            )
            return [
                {
                    "type": "text",
                    "text": _format_create_result(result, "Experiment", name_val),
                }
            ]

        elif name == "update_experiment":
            experiment_id = arguments["experiment_id"]
            updates = {k: v for k, v in arguments.items() if k != "experiment_id"}
            result = await statsig_client.update_experiment(experiment_id, updates)
            return [
                {
                    "type": "text",
                    "text": _format_update_result(result, "Experiment", experiment_id),
                }
            ]

        elif name == "delete_experiment":
            experiment_id = arguments["experiment_id"]
            result = await statsig_client.delete_experiment(experiment_id)
            return [
                {
                    "type": "text",
                    "text": _format_delete_result(result, "Experiment", experiment_id),
                }
            ]

        # Dynamic Configs
        elif name == "list_dynamic_configs":
            limit = arguments.get("limit")
            result = await statsig_client.list_dynamic_configs(limit)
            return [
                {"type": "text", "text": _format_list_result(result, "Dynamic Configs")}
            ]

        elif name == "get_dynamic_config":
            config_id = arguments["config_id"]
            result = await statsig_client.get_dynamic_config(config_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Dynamic Config", config_id),
                }
            ]

        elif name == "create_dynamic_config":
            name_val = arguments["name"]
            description = arguments.get("description", "")
            result = await statsig_client.create_dynamic_config(name_val, description)
            return [
                {
                    "type": "text",
                    "text": _format_create_result(result, "Dynamic Config", name_val),
                }
            ]

        elif name == "update_dynamic_config":
            config_id = arguments["config_id"]
            updates = {k: v for k, v in arguments.items() if k != "config_id"}
            result = await statsig_client.update_dynamic_config(config_id, updates)
            return [
                {
                    "type": "text",
                    "text": _format_update_result(result, "Dynamic Config", config_id),
                }
            ]

        elif name == "delete_dynamic_config":
            config_id = arguments["config_id"]
            result = await statsig_client.delete_dynamic_config(config_id)
            return [
                {
                    "type": "text",
                    "text": _format_delete_result(result, "Dynamic Config", config_id),
                }
            ]

        # Segments
        elif name == "list_segments":
            limit = arguments.get("limit")
            result = await statsig_client.list_segments(limit)
            return [{"type": "text", "text": _format_list_result(result, "Segments")}]

        elif name == "get_segment":
            segment_id = arguments["segment_id"]
            result = await statsig_client.get_segment(segment_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Segment", segment_id),
                }
            ]

        elif name == "create_segment":
            name_val = arguments["name"]
            description = arguments.get("description", "")
            result = await statsig_client.create_segment(name_val, description)
            return [
                {
                    "type": "text",
                    "text": _format_create_result(result, "Segment", name_val),
                }
            ]

        # Metrics
        elif name == "list_metrics":
            limit = arguments.get("limit")
            result = await statsig_client.list_metrics(limit)
            return [{"type": "text", "text": _format_list_result(result, "Metrics")}]

        elif name == "get_metric":
            metric_id = arguments["metric_id"]
            result = await statsig_client.get_metric(metric_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Metric", metric_id),
                }
            ]

        # Audit Logs
        elif name == "list_audit_logs":
            limit = arguments.get("limit", 20)
            from_date = arguments.get("from_date")
            to_date = arguments.get("to_date")
            result = await statsig_client.list_audit_logs(limit, from_date, to_date)
            return [{"type": "text", "text": _format_audit_logs_result(result)}]

        # Target Apps
        elif name == "list_target_apps":
            result = await statsig_client.list_target_apps()
            return [
                {"type": "text", "text": _format_list_result(result, "Target Apps")}
            ]

        elif name == "get_target_app":
            app_id = arguments["app_id"]
            result = await statsig_client.get_target_app(app_id)
            return [
                {
                    "type": "text",
                    "text": _format_item_result(result, "Target App", app_id),
                }
            ]

        # API Keys
        elif name == "list_api_keys":
            result = await statsig_client.list_api_keys()
            return [{"type": "text", "text": _format_list_result(result, "API Keys")}]

        # Events (keeping existing functionality)
        elif name == "query_events":
            event_name = arguments.get("event_name")
            limit = arguments.get("limit", 10)
            result = await statsig_client.query_events(event_name, limit)
            return [{"type": "text", "text": _format_events_query_result(result)}]

        # Users (keeping existing functionality)
        elif name == "get_user_by_email":
            email = arguments["email"]
            result = await statsig_client.get_user_by_email(email)
            return [{"type": "text", "text": _format_user_result(result)}]

        elif name == "list_team_users":
            result = await statsig_client.list_team_users()
            return [{"type": "text", "text": _format_team_users_result(result)}]

        # Experiment Results and Analytics
        elif name == "get_experiment_results":
            experiment_id = arguments["experiment_id"]
            include_metrics = arguments.get("include_metrics", True)
            result = await statsig_client.get_experiment_results(experiment_id, include_metrics)
            return [{"type": "text", "text": _format_experiment_results(result)}]

        elif name == "get_experiment_pulse":
            experiment_id = arguments["experiment_id"]
            result = await statsig_client.get_experiment_pulse(experiment_id)
            return [{"type": "text", "text": _format_pulse_data(result)}]

        elif name == "get_metric_details":
            metric_id = arguments["metric_id"]
            experiment_id = arguments["experiment_id"]
            result = await statsig_client.get_metric_details(metric_id, experiment_id)
            return [{"type": "text", "text": _format_metric_details(result)}]

        elif name == "export_pulse_report":
            experiment_id = arguments["experiment_id"]
            format_type = arguments.get("format", "json")
            result = await statsig_client.export_pulse_report(experiment_id, format_type)
            return [{"type": "text", "text": _format_pulse_report(result, format_type)}]

        else:
            return [{"type": "text", "text": f"Unknown tool: {name}"}]

    except Exception as e:
        return [{"type": "text", "text": f"Error calling tool {name}: {str(e)}"}]


def _format_events_query_result(result: dict) -> str:
    """Format events query result for display."""
    error = result.get("error")

    if error:
        return f"❌ Error querying events: {error}"

    # Check if it's a specific event query
    if "event_name" in result:
        event_name = result["event_name"]
        found = result.get("found", False)

        if not found:
            message = result.get("message", f"Event '{event_name}' not found")
            return f"📭 {message}"

        details = result.get("details", {})
        output = [f"📊 Event Details: {event_name}"]

        if details:
            for key, value in details.items():
                output.append(f"   {key}: {value}")

        return "\n".join(output)

    # List of event types
    event_types = result.get("event_types", [])
    total_found = result.get("total_found", 0)
    note = result.get("note", "")

    output = [f"📊 Event Types ({total_found} found)"]

    if note:
        output.append(f"ℹ️  {note}")

    output.append("")

    for event in event_types:
        name = event.get("name", "Unknown")
        description = event.get("description", "No description")
        output.append(f"🔹 {name}")
        output.append(f"   Description: {description}")

    return "\n".join(output)


def _format_user_result(result: dict) -> str:
    """Format user result for display."""
    email = result.get("email", "Unknown")
    found = result.get("found", False)
    error = result.get("error")

    if error:
        return f"❌ Error getting user {email}: {error}"

    if not found:
        message = result.get("message", f"User '{email}' not found")
        return f"👤 {message}"

    user_data = result.get("user_data", {})
    note = result.get("note", "")

    output = [f"👤 Team Member: {email}"]

    if note:
        output.append(f"ℹ️  {note}")

    output.append("")

    if user_data:
        # Show key user information
        for key, value in user_data.items():
            if key not in ["email"]:  # Don't repeat email
                output.append(f"   {key}: {value}")

    return "\n".join(output)


def _format_team_users_result(result: dict) -> str:
    """Format team users result for display."""
    error = result.get("error")

    if error:
        return f"❌ Error listing team users: {error}"

    team_users = result.get("team_users", [])
    total_users = result.get("total_users", 0)
    note = result.get("note", "")

    output = [f"👥 Team Members ({total_users} total)"]

    if note:
        output.append(f"ℹ️  {note}")

    output.append("")

    for user in team_users:
        email = user.get("email", "Unknown")
        name = user.get("name", user.get("firstName", "Unknown"))
        role = user.get("role", "Unknown")

        output.append(f"👤 {name} ({email})")
        output.append(f"   Role: {role}")

    return "\n".join(output)


async def initialize_client(config: dict[str, Any]) -> None:
    """Initialize the Statsig client with configuration."""
    global statsig_client

    # Set environment variables from config for the client
    os.environ["STATSIG_CONSOLE_API_KEY"] = config["api_key"]

    statsig_client = StatsigConsoleClient()
    await statsig_client.initialize()


async def cleanup() -> None:
    """Cleanup resources."""
    global statsig_client
    if statsig_client:
        await statsig_client.shutdown()


async def main() -> None:
    """Main entry point."""
    try:
        # Parse command-line arguments
        args = parse_arguments()

        # Get configuration
        config = get_configuration(args)

        # Initialize Statsig client
        await initialize_client(config)

        # Run the MCP server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await cleanup()


def main_sync() -> None:
    """Synchronous entry point for console scripts."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


# Entry point is handled by __main__.py when running as module


def _format_list_result(result: dict, resource_type: str) -> str:
    """Format list result for display."""
    error = result.get("error")

    if error:
        return f"❌ Error listing {resource_type}: {error}"

    items = result.get("data", result.get("items", []))
    total = result.get("total", len(items))

    output = [f"📋 {resource_type} ({total} found)"]

    if not items:
        output.append("   No items found")
        return "\n".join(output)

    output.append("")
    for item in items:
        name = item.get("name", item.get("id", "Unknown"))
        item_id = item.get("id", item.get("name", "Unknown"))
        description = item.get("description", "No description")
        status = item.get("status", item.get("isEnabled", "Unknown"))

        output.append(f"🔹 {name} (ID: {item_id})")
        if description and description != "No description":
            output.append(f"   Description: {description}")
        if str(status).lower() in ["true", "active", "enabled"]:
            output.append(f"   Status: ✅ {status}")
        elif str(status).lower() in ["false", "inactive", "disabled"]:
            output.append(f"   Status: ❌ {status}")
        else:
            output.append(f"   Status: {status}")
        output.append("")

    return "\n".join(output)


def _format_item_result(result: dict, resource_type: str, item_id: str) -> str:
    """Format single item result for display."""
    error = result.get("error")

    if error:
        return f"❌ Error getting {resource_type} {item_id}: {error}"

    if not result.get("found", True):
        return f"📭 {resource_type} '{item_id}' not found"

    data = result.get("data", result)
    output = [f"📄 {resource_type}: {item_id}"]
    output.append("")

    # Display key fields
    for key, value in data.items():
        if key not in ["id", "data", "found", "error"]:
            formatted_key = key.replace("_", " ").title()
            if isinstance(value, dict | list):
                output.append(f"   {formatted_key}: {str(value)}")
            else:
                output.append(f"   {formatted_key}: {value}")

    return "\n".join(output)


def _format_create_result(result: dict, resource_type: str, name: str) -> str:
    """Format create result for display."""
    success = result.get("success", False)
    error = result.get("error")

    if error:
        return f"❌ Error creating {resource_type} '{name}': {error}"

    if success:
        item_id = result.get("id", result.get("data", {}).get("id", "Unknown"))
        return f"✅ Successfully created {resource_type} '{name}' (ID: {item_id})"
    else:
        message = result.get("message", "Unknown error")
        return f"❌ Failed to create {resource_type} '{name}': {message}"


def _format_update_result(result: dict, resource_type: str, item_id: str) -> str:
    """Format update result for display."""
    success = result.get("success", False)
    error = result.get("error")

    if error:
        return f"❌ Error updating {resource_type} {item_id}: {error}"

    if success:
        return f"✅ Successfully updated {resource_type} {item_id}"
    else:
        message = result.get("message", "Unknown error")
        return f"❌ Failed to update {resource_type} {item_id}: {message}"


def _format_delete_result(result: dict, resource_type: str, item_id: str) -> str:
    """Format delete result for display."""
    success = result.get("success", False)
    error = result.get("error")

    if error:
        return f"❌ Error deleting {resource_type} {item_id}: {error}"

    if success:
        return f"✅ Successfully deleted {resource_type} {item_id}"
    else:
        message = result.get("message", "Unknown error")
        return f"❌ Failed to delete {resource_type} {item_id}: {message}"


def _format_audit_logs_result(result: dict) -> str:
    """Format audit logs result for display."""
    error = result.get("error")

    if error:
        return f"❌ Error listing audit logs: {error}"

    logs = result.get("data", result.get("logs", []))
    total = result.get("total", len(logs))

    output = [f"📜 Audit Logs ({total} found)"]

    if not logs:
        output.append("   No logs found")
        return "\n".join(output)

    output.append("")
    for log in logs:
        timestamp = log.get("timestamp", log.get("createdAt", "Unknown"))
        action = log.get("action", log.get("event", "Unknown"))
        user = log.get("user", log.get("actor", "Unknown"))
        target = log.get("target", log.get("resource", "Unknown"))

        output.append(f"🔸 {timestamp}")
        output.append(f"   Action: {action}")
        output.append(f"   User: {user}")
        output.append(f"   Target: {target}")
        output.append("")

    return "\n".join(output)


def _format_experiment_results(result: dict) -> str:
    """Format experiment results for display."""
    error = result.get("error")
    
    if error:
        return f"❌ Error getting experiment results: {error}"
    
    data = result.get("data", {})
    experiment_id = data.get("experiment_id", "Unknown")
    experiment_name = data.get("experiment_name", "Unknown")
    status = data.get("status", "Unknown")
    
    output = [f"📊 Experiment Results: {experiment_name} ({experiment_id})"]
    output.append(f"   Status: {status}")
    output.append("")
    
    # Primary metrics
    primary_metrics = data.get("primary_metrics", [])
    if primary_metrics:
        output.append("🎯 Primary Metrics:")
        for metric in primary_metrics:
            name = metric.get("metric_name", "Unknown")
            lift = metric.get("lift")
            p_value = metric.get("p_value")
            significance = metric.get("significance", "Unknown")
            
            output.append(f"   • {name}")
            if lift is not None:
                output.append(f"     Lift: {lift:.2%}")
            if p_value is not None:
                output.append(f"     P-value: {p_value:.4f}")
            output.append(f"     Significance: {significance}")
            output.append("")
    
    # Secondary metrics
    secondary_metrics = data.get("secondary_metrics", [])
    if secondary_metrics:
        output.append("📈 Secondary Metrics:")
        for metric in secondary_metrics:
            name = metric.get("metric_name", "Unknown")
            lift = metric.get("lift")
            significance = metric.get("significance", "Unknown")
            
            output.append(f"   • {name}")
            if lift is not None:
                output.append(f"     Lift: {lift:.2%}")
            output.append(f"     Significance: {significance}")
            output.append("")
    
    # Overall recommendation
    recommendation = data.get("recommendation")
    if recommendation:
        output.append(f"💡 Recommendation: {recommendation}")
    
    return "\n".join(output)


def _format_pulse_data(result: dict) -> str:
    """Format pulse data for display."""
    error = result.get("error")
    
    if error:
        return f"❌ Error getting pulse data: {error}"
    
    data = result.get("data", {})
    experiment_id = data.get("experiment_id", "Unknown")
    health_score = data.get("health_score")
    
    output = [f"💓 Experiment Pulse: {experiment_id}"]
    
    if health_score is not None:
        output.append(f"   Health Score: {health_score:.1f}/10")
        
        # Add health indicator
        if health_score >= 8:
            output.append("   Status: 🟢 Healthy")
        elif health_score >= 6:
            output.append("   Status: 🟡 Moderate")
        else:
            output.append("   Status: 🔴 Needs Attention")
    
    output.append("")
    
    # Performance indicators
    indicators = data.get("performance_indicators", {})
    if indicators:
        output.append("📊 Performance Indicators:")
        for key, value in indicators.items():
            output.append(f"   • {key}: {value}")
        output.append("")
    
    # Alerts
    alerts = data.get("alerts", [])
    if alerts:
        output.append("⚠️  Alerts:")
        for alert in alerts:
            alert_type = alert.get("type", "Unknown")
            message = alert.get("message", "No details")
            output.append(f"   • {alert_type}: {message}")
        output.append("")
    
    # Recommendations
    recommendations = data.get("recommendations", [])
    if recommendations:
        output.append("💡 Recommendations:")
        for rec in recommendations:
            output.append(f"   • {rec}")
    
    return "\n".join(output)


def _format_metric_details(result: dict) -> str:
    """Format metric details for display."""
    error = result.get("error")
    
    if error:
        return f"❌ Error getting metric details: {error}"
    
    data = result.get("data", {})
    metric_name = data.get("metric_name", "Unknown")
    metric_type = data.get("metric_type", "Unknown")
    
    output = [f"📈 Metric Details: {metric_name}"]
    output.append(f"   Type: {metric_type}")
    output.append("")
    
    # Values
    control_value = data.get("control_value")
    test_value = data.get("test_value")
    
    if control_value is not None and test_value is not None:
        output.append("📊 Values:")
        output.append(f"   Control: {control_value:,.2f}")
        output.append(f"   Test: {test_value:,.2f}")
        output.append("")
    
    # Statistical analysis
    lift = data.get("lift")
    lift_ci_lower = data.get("lift_ci_lower")
    lift_ci_upper = data.get("lift_ci_upper")
    p_value = data.get("p_value")
    significance = data.get("significance")
    
    output.append("📊 Statistical Analysis:")
    if lift is not None:
        output.append(f"   Lift: {lift:.2%}")
    
    if lift_ci_lower is not None and lift_ci_upper is not None:
        output.append(f"   95% CI: [{lift_ci_lower:.2%}, {lift_ci_upper:.2%}]")
    
    if p_value is not None:
        output.append(f"   P-value: {p_value:.4f}")
    
    if significance:
        output.append(f"   Significance: {significance}")
    
    # Sample sizes
    sample_control = data.get("sample_size_control")
    sample_test = data.get("sample_size_test")
    
    if sample_control is not None or sample_test is not None:
        output.append("")
        output.append("👥 Sample Sizes:")
        if sample_control is not None:
            output.append(f"   Control: {sample_control:,}")
        if sample_test is not None:
            output.append(f"   Test: {sample_test:,}")
    
    return "\n".join(output)


def _format_pulse_report(result: dict, format_type: str) -> str:
    """Format pulse report export for display."""
    error = result.get("error")
    
    if error:
        return f"❌ Error exporting pulse report: {error}"
    
    data = result.get("data", {})
    
    output = [f"📋 Pulse Report Export ({format_type.upper()})"]
    output.append("")
    
    if format_type == "json":
        # For JSON, show a formatted summary
        experiment_id = data.get("experiment_id", "Unknown")
        report_date = data.get("report_date", "Unknown")
        
        output.append(f"Experiment: {experiment_id}")
        output.append(f"Report Date: {report_date}")
        output.append("")
        output.append("📦 Export contains:")
        output.append("   • Complete experiment results")
        output.append("   • Statistical analysis")
        output.append("   • Health metrics")
        output.append("   • Performance indicators")
        
    elif format_type == "csv":
        output.append("📊 CSV Export Ready")
        output.append("   • Metrics data in tabular format")
        output.append("   • Statistical significance")
        output.append("   • Confidence intervals")
        
    elif format_type == "summary":
        output.append("📝 Executive Summary")
        summary = data.get("summary", "No summary available")
        output.append(f"   {summary}")
    
    return "\n".join(output)
