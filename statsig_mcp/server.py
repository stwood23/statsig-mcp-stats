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
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .statsig_client import StatsigMCPClient
from .types import (DynamicConfigResult, EventLogResult, ExperimentResult,
                    FeatureGateResult, LayerResult)

# Initialize the MCP server
server = Server("statsig-mcp")

# Global client instance
statsig_client: Optional[StatsigMCPClient] = None


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Statsig MCP Server - Model Context Protocol server for Statsig feature flags"
    )
    
    # Server configuration
    parser.add_argument(
        "--api-key", 
        type=str,
        help="Statsig server secret key (can also use STATSIG_SERVER_SECRET_KEY env var)"
    )
    
    parser.add_argument(
        "--environment",
        type=str,
        default="development",
        help="Statsig environment tier (default: development)"
    )
    
    parser.add_argument(
        "--api-timeout",
        type=int,
        default=3000,
        help="API timeout in milliseconds (default: 3000)"
    )
    
    parser.add_argument(
        "--disable-logging",
        action="store_true",
        help="Disable event logging to Statsig"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    # MCP server options
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser.parse_args()


def get_configuration(args: argparse.Namespace) -> Dict[str, Any]:
    """Get configuration from args and environment variables."""
    config = {}
    
    # API Key - prioritize command line arg, then env var
    api_key = args.api_key or os.getenv("STATSIG_SERVER_SECRET_KEY")
    if not api_key:
        raise ValueError(
            "Statsig server secret key is required. "
            "Provide via --api-key argument or STATSIG_SERVER_SECRET_KEY environment variable."
        )
    config["api_key"] = api_key
    
    # Other configuration with fallbacks to environment variables
    config["environment"] = args.environment or os.getenv("STATSIG_ENVIRONMENT", "development")
    config["api_timeout"] = args.api_timeout or int(os.getenv("STATSIG_API_TIMEOUT", "3000"))
    config["disable_logging"] = args.disable_logging or os.getenv("STATSIG_DISABLE_LOGGING", "false").lower() == "true"
    config["debug"] = args.debug or os.getenv("STATSIG_DEBUG", "false").lower() == "true"
    
    return config


@server.list_tools()
async def list_tools() -> list[dict]:
    """List available tools."""
    return [
        {
            "name": "check_feature_gate",
            "description": "Check if a feature gate is enabled for a user",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string", 
                        "description": "User identifier"
                    },
                    "gate_name": {
                        "type": "string", 
                        "description": "Name of the feature gate"
                    },
                    "user_email": {
                        "type": "string", 
                        "description": "User email (optional)"
                    },
                    "user_country": {
                        "type": "string", 
                        "description": "User country code (optional)"
                    },
                    "custom_attributes": {
                        "type": "object", 
                        "description": "Custom user attributes (optional)"
                    }
                },
                "required": ["user_id", "gate_name"]
            }
        },
        {
            "name": "get_dynamic_config",
            "description": "Get dynamic configuration for a user",
            "inputSchema": {
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
                        "description": "User email (optional)"
                    },
                    "user_country": {
                        "type": "string", 
                        "description": "User country code (optional)"
                    },
                    "custom_attributes": {
                        "type": "object", 
                        "description": "Custom user attributes (optional)"
                    }
                },
                "required": ["user_id", "config_name"]
            }
        },
        {
            "name": "get_experiment",
            "description": "Get experiment assignment for a user",
            "inputSchema": {
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
                        "description": "User email (optional)"
                    },
                    "user_country": {
                        "type": "string", 
                        "description": "User country code (optional)"
                    },
                    "custom_attributes": {
                        "type": "object", 
                        "description": "Custom user attributes (optional)"
                    }
                },
                "required": ["user_id", "experiment_name"]
            }
        },
        {
            "name": "get_layer",
            "description": "Get layer parameters for a user",
            "inputSchema": {
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
                        "description": "User email (optional)"
                    },
                    "user_country": {
                        "type": "string", 
                        "description": "User country code (optional)"
                    },
                    "custom_attributes": {
                        "type": "object", 
                        "description": "Custom user attributes (optional)"
                    }
                },
                "required": ["user_id", "layer_name"]
            }
        },
        {
            "name": "log_event",
            "description": "Log a custom event",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string", 
                        "description": "User identifier"
                    },
                    "event_name": {
                        "type": "string", 
                        "description": "Name of the event"
                    },
                    "value": {
                        "type": ["string", "number"], 
                        "description": "Event value (optional)"
                    },
                    "metadata": {
                        "type": "object", 
                        "description": "Event metadata (optional)"
                    },
                    "user_email": {
                        "type": "string", 
                        "description": "User email (optional)"
                    },
                    "user_country": {
                        "type": "string", 
                        "description": "User country code (optional)"
                    },
                    "custom_attributes": {
                        "type": "object", 
                        "description": "Custom user attributes (optional)"
                    }
                },
                "required": ["user_id", "event_name"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Handle tool calls."""
    global statsig_client
    
    if not statsig_client:
        return [{"type": "text", "text": "Error: Statsig client not initialized"}]
    
    try:
        if name == "check_feature_gate":
            user_attrs = _extract_user_attributes(arguments)
            gate_name = arguments["gate_name"]
            
            result = await statsig_client.check_feature_gate(user_attrs, gate_name)
            return [{"type": "text", "text": _format_feature_gate_result(result)}]
            
        elif name == "get_dynamic_config":
            user_attrs = _extract_user_attributes(arguments)
            config_name = arguments["config_name"]
            
            result = await statsig_client.get_dynamic_config(user_attrs, config_name)
            return [{"type": "text", "text": _format_dynamic_config_result(result)}]
            
        elif name == "get_experiment":
            user_attrs = _extract_user_attributes(arguments)
            experiment_name = arguments["experiment_name"]
            
            result = await statsig_client.get_experiment(user_attrs, experiment_name)
            return [{"type": "text", "text": _format_experiment_result(result)}]
            
        elif name == "get_layer":
            user_attrs = _extract_user_attributes(arguments)
            layer_name = arguments["layer_name"]
            
            result = await statsig_client.get_layer(user_attrs, layer_name)
            return [{"type": "text", "text": _format_layer_result(result)}]
            
        elif name == "log_event":
            user_attrs = _extract_user_attributes(arguments)
            event_name = arguments["event_name"]
            value = arguments.get("value")
            metadata = arguments.get("metadata")
            
            result = await statsig_client.log_event(user_attrs, event_name, value, metadata)
            return [{"type": "text", "text": _format_event_log_result(result)}]
            
        else:
            return [{"type": "text", "text": f"Unknown tool: {name}"}]
            
    except Exception as e:
        return [{"type": "text", "text": f"Error calling tool {name}: {str(e)}"}]


def _extract_user_attributes(arguments: dict) -> Dict[str, Any]:
    """Extract user attributes from tool arguments."""
    user_attrs = {"user_id": arguments["user_id"]}
    
    if "user_email" in arguments:
        user_attrs["user_email"] = arguments["user_email"]
    if "user_country" in arguments:
        user_attrs["user_country"] = arguments["user_country"]
    if "custom_attributes" in arguments:
        user_attrs["custom_attributes"] = arguments["custom_attributes"]
        
    return user_attrs


def _format_feature_gate_result(result: FeatureGateResult) -> str:
    """Format feature gate result for display."""
    return (
        f"Feature Gate: {result['gate_name']}\n"
        f"Enabled: {result['value']}\n"
        f"Rule ID: {result['rule_id']}\n"
        f"Group: {result.get('group_name', 'N/A')}"
    )


def _format_dynamic_config_result(result: DynamicConfigResult) -> str:
    """Format dynamic config result for display."""
    return (
        f"Dynamic Config: {result['config_name']}\n"
        f"Value: {result['value']}\n"
        f"Rule ID: {result['rule_id']}\n"
        f"Group: {result.get('group_name', 'N/A')}"
    )


def _format_experiment_result(result: ExperimentResult) -> str:
    """Format experiment result for display."""
    return (
        f"Experiment: {result['experiment_name']}\n"
        f"Value: {result['value']}\n"
        f"Rule ID: {result['rule_id']}\n"
        f"Group: {result.get('group_name', 'N/A')}"
    )


def _format_layer_result(result: LayerResult) -> str:
    """Format layer result for display."""
    return (
        f"Layer: {result['layer_name']}\n"
        f"Value: {result['value']}\n"
        f"Rule ID: {result['rule_id']}\n"
        f"Allocated Experiment: {result.get('allocated_experiment_name', 'N/A')}"
    )


def _format_event_log_result(result: EventLogResult) -> str:
    """Format event log result for display."""
    status = "✅ Success" if result['success'] else "❌ Failed"
    return f"{status}: {result['message']}"


async def initialize_client(config: Dict[str, Any]) -> None:
    """Initialize the Statsig client with configuration."""
    global statsig_client
    
    # Set environment variables from config for the client
    os.environ["STATSIG_SERVER_SECRET_KEY"] = config["api_key"]
    os.environ["STATSIG_ENVIRONMENT"] = config["environment"]
    os.environ["STATSIG_API_TIMEOUT"] = str(config["api_timeout"])
    os.environ["STATSIG_DISABLE_LOGGING"] = str(config["disable_logging"]).lower()
    os.environ["STATSIG_DEBUG"] = str(config["debug"]).lower()
    
    statsig_client = StatsigMCPClient()
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
            await server.run(read_stream, write_stream, server.create_initialization_options())
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main()) 