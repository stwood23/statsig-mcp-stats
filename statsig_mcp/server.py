"""
Statsig MCP Server

A Model Context Protocol server that provides access to Statsig feature flags,
dynamic configs, experiments, and event logging.
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .statsig_client import StatsigMCPClient
from .types import (DynamicConfigRequest, ExperimentRequest,
                    FeatureGateCheckRequest, LayerRequest, LogEventRequest)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize Statsig client
    statsig_client = StatsigMCPClient()
    
    try:
        logger.info("Initializing Statsig client...")
        await statsig_client.initialize()
        logger.info("Statsig client initialized successfully")
        
        yield {"statsig_client": statsig_client}
    finally:
        # Clean up on shutdown
        logger.info("Shutting down Statsig client...")
        await statsig_client.shutdown()
        logger.info("Server shutdown complete")


# Create server with lifespan management
server = Server("statsig-mcp", lifespan=server_lifespan)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="check_feature_gate",
            description="Check if a feature gate is enabled for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "gate_name": {
                        "type": "string",
                        "description": "Name of the feature gate to check"
                    },
                    "user_email": {
                        "type": "string",
                        "description": "User email address (optional)"
                    },
                    "user_country": {
                        "type": "string",
                        "description": "User country code (optional)"
                    },
                    "user_ip": {
                        "type": "string",
                        "description": "User IP address (optional)"
                    },
                    "user_agent": {
                        "type": "string",
                        "description": "User agent string (optional)"
                    },
                    "app_version": {
                        "type": "string",
                        "description": "Application version (optional)"
                    },
                    "locale": {
                        "type": "string",
                        "description": "User locale (optional)"
                    },
                    "custom_attributes": {
                        "type": "object",
                        "description": "Custom user attributes (optional)"
                    },
                    "private_attributes": {
                        "type": "object",
                        "description": "Private user attributes (optional)"
                    }
                },
                "required": ["user_id", "gate_name"]
            }
        ),
        types.Tool(
            name="get_dynamic_config",
            description="Get dynamic configuration values for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "config_name": {
                        "type": "string",
                        "description": "Name of the dynamic config"
                    },
                    "user_email": {
                        "type": "string",
                        "description": "User email address (optional)"
                    },
                    "user_country": {
                        "type": "string",
                        "description": "User country code (optional)"
                    },
                    "user_ip": {
                        "type": "string",
                        "description": "User IP address (optional)"
                    },
                    "user_agent": {
                        "type": "string",
                        "description": "User agent string (optional)"
                    },
                    "app_version": {
                        "type": "string",
                        "description": "Application version (optional)"
                    },
                    "locale": {
                        "type": "string",
                        "description": "User locale (optional)"
                    },
                    "custom_attributes": {
                        "type": "object",
                        "description": "Custom user attributes (optional)"
                    },
                    "private_attributes": {
                        "type": "object",
                        "description": "Private user attributes (optional)"
                    }
                },
                "required": ["user_id", "config_name"]
            }
        ),
        types.Tool(
            name="get_experiment",
            description="Get experiment assignment for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "experiment_name": {
                        "type": "string",
                        "description": "Name of the experiment"
                    },
                    "user_email": {
                        "type": "string",
                        "description": "User email address (optional)"
                    },
                    "user_country": {
                        "type": "string",
                        "description": "User country code (optional)"
                    },
                    "user_ip": {
                        "type": "string",
                        "description": "User IP address (optional)"
                    },
                    "user_agent": {
                        "type": "string",
                        "description": "User agent string (optional)"
                    },
                    "app_version": {
                        "type": "string",
                        "description": "Application version (optional)"
                    },
                    "locale": {
                        "type": "string",
                        "description": "User locale (optional)"
                    },
                    "custom_attributes": {
                        "type": "object",
                        "description": "Custom user attributes (optional)"
                    },
                    "private_attributes": {
                        "type": "object",
                        "description": "Private user attributes (optional)"
                    }
                },
                "required": ["user_id", "experiment_name"]
            }
        ),
        types.Tool(
            name="get_layer",
            description="Get layer parameter values for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "layer_name": {
                        "type": "string",
                        "description": "Name of the layer"
                    },
                    "user_email": {
                        "type": "string",
                        "description": "User email address (optional)"
                    },
                    "user_country": {
                        "type": "string",
                        "description": "User country code (optional)"
                    },
                    "user_ip": {
                        "type": "string",
                        "description": "User IP address (optional)"
                    },
                    "user_agent": {
                        "type": "string",
                        "description": "User agent string (optional)"
                    },
                    "app_version": {
                        "type": "string",
                        "description": "Application version (optional)"
                    },
                    "locale": {
                        "type": "string",
                        "description": "User locale (optional)"
                    },
                    "custom_attributes": {
                        "type": "object",
                        "description": "Custom user attributes (optional)"
                    },
                    "private_attributes": {
                        "type": "object",
                        "description": "Private user attributes (optional)"
                    }
                },
                "required": ["user_id", "layer_name"]
            }
        ),
        types.Tool(
            name="log_event",
            description="Log a custom event",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User identifier"
                    },
                    "event_name": {
                        "type": "string",
                        "description": "Name of the event to log"
                    },
                    "value": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "number"}
                        ],
                        "description": "Event value (optional)"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Event metadata (optional)"
                    },
                    "user_email": {
                        "type": "string",
                        "description": "User email address (optional)"
                    },
                    "user_country": {
                        "type": "string",
                        "description": "User country code (optional)"
                    },
                    "user_ip": {
                        "type": "string",
                        "description": "User IP address (optional)"
                    },
                    "user_agent": {
                        "type": "string",
                        "description": "User agent string (optional)"
                    },
                    "app_version": {
                        "type": "string",
                        "description": "Application version (optional)"
                    },
                    "locale": {
                        "type": "string",
                        "description": "User locale (optional)"
                    },
                    "custom_attributes": {
                        "type": "object",
                        "description": "Custom user attributes (optional)"
                    },
                    "private_attributes": {
                        "type": "object",
                        "description": "Private user attributes (optional)"
                    }
                },
                "required": ["user_id", "event_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    # Get the Statsig client from the request context
    ctx = server.request_context
    statsig_client = ctx.lifespan_context["statsig_client"]

    try:
        if name == "check_feature_gate":
            # Build user attributes dict from arguments
            user_attrs = {k: v for k, v in arguments.items() if k != "gate_name"}
            
            result = await statsig_client.check_feature_gate(
                user_attrs, arguments["gate_name"]
            )
            return [
                types.TextContent(
                    type="text", 
                    text=f"Feature gate '{result['gate_name']}' is {'enabled' if result['value'] else 'disabled'} for user {arguments['user_id']}.\n\nDetails:\n- Value: {result['value']}\n- Rule ID: {result['rule_id']}\n- Group Name: {result.get('group_name', 'N/A')}"
                )
            ]

        elif name == "get_dynamic_config":
            # Build user attributes dict from arguments
            user_attrs = {k: v for k, v in arguments.items() if k != "config_name"}
            
            result = await statsig_client.get_dynamic_config(
                user_attrs, arguments["config_name"]
            )
            return [
                types.TextContent(
                    type="text",
                    text=f"Dynamic config '{result['config_name']}' for user {arguments['user_id']}:\n\nConfiguration:\n{result['value']}\n\nMetadata:\n- Rule ID: {result['rule_id']}\n- Group Name: {result.get('group_name', 'N/A')}"
                )
            ]

        elif name == "get_experiment":
            # Build user attributes dict from arguments
            user_attrs = {k: v for k, v in arguments.items() if k != "experiment_name"}
            
            result = await statsig_client.get_experiment(
                user_attrs, arguments["experiment_name"]
            )
            return [
                types.TextContent(
                    type="text",
                    text=f"Experiment '{result['experiment_name']}' assignment for user {arguments['user_id']}:\n\nParameters:\n{result['value']}\n\nMetadata:\n- Rule ID: {result['rule_id']}\n- Group Name: {result.get('group_name', 'N/A')}"
                )
            ]

        elif name == "get_layer":
            # Build user attributes dict from arguments
            user_attrs = {k: v for k, v in arguments.items() if k != "layer_name"}
            
            result = await statsig_client.get_layer(
                user_attrs, arguments["layer_name"]
            )
            return [
                types.TextContent(
                    type="text",
                    text=f"Layer '{result['layer_name']}' values for user {arguments['user_id']}:\n\nParameters:\n{result['value']}\n\nMetadata:\n- Rule ID: {result['rule_id']}\n- Allocated Experiment: {result.get('allocated_experiment_name', 'N/A')}"
                )
            ]

        elif name == "log_event":
            # Build user attributes dict from arguments
            user_attrs = {k: v for k, v in arguments.items() if k not in ("event_name", "value", "metadata")}
            
            result = await statsig_client.log_event(
                user_attrs,
                arguments["event_name"],
                arguments.get("value"),
                arguments.get("metadata")
            )
            return [
                types.TextContent(
                    type="text",
                    text=f"Event logging {'successful' if result['success'] else 'failed'}: {result['message']}"
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error handling tool call {name}: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]


async def run() -> None:
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="statsig-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main() -> None:
    """Main entry point."""
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 