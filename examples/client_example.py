#!/usr/bin/env python3
"""
Example MCP client that demonstrates how to use the Statsig MCP server.

This script shows how to:
1. Connect to the Statsig MCP server
2. Check feature gates
3. Get dynamic configs
4. Get experiment assignments
5. Get layer values
6. Log events

Before running this example:
1. Set your STATSIG_SERVER_SECRET_KEY environment variable
2. Make sure the Statsig MCP server is available
"""

import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_example():
    """Run the Statsig MCP client example."""
    
    # Check if the API key is set
    if not os.getenv("STATSIG_SERVER_SECRET_KEY"):
        print("❌ Please set STATSIG_SERVER_SECRET_KEY environment variable")
        return
    
    # Create server parameters for the Statsig MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "statsig_mcp"],
        env={
            "STATSIG_SERVER_SECRET_KEY": os.getenv("STATSIG_SERVER_SECRET_KEY"),
            "STATSIG_ENVIRONMENT": os.getenv("STATSIG_ENVIRONMENT", "development"),
            "STATSIG_DEBUG": "true"  # Enable debug for this example
        }
    )

    print("🚀 Starting Statsig MCP client example...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            print("📡 Initializing MCP session...")
            await session.initialize()
            
            # List available tools
            print("\n🔧 Available tools:")
            tools = await session.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n" + "="*60)
            print("🧪 Running Statsig examples...")
            print("="*60)
            
            # Example user for testing
            example_user = {
                "user_id": "example_user_123",
                "user_email": "user@example.com", 
                "user_country": "US",
                "custom_attributes": {
                    "plan": "premium",
                    "cohort": "2024_q1"
                }
            }
            
            # 1. Check a feature gate
            print("\n1️⃣ Checking feature gate...")
            try:
                gate_result = await session.call_tool(
                    "check_feature_gate",
                    arguments={
                        **example_user,
                        "gate_name": "new_checkout_flow"
                    }
                )
                print("✅ Feature gate result:")
                for content in gate_result:
                    print(f"   {content.text}")
            except Exception as e:
                print(f"❌ Error checking feature gate: {e}")
            
            # 2. Get dynamic config  
            print("\n2️⃣ Getting dynamic config...")
            try:
                config_result = await session.call_tool(
                    "get_dynamic_config",
                    arguments={
                        **example_user,
                        "config_name": "ui_settings"
                    }
                )
                print("✅ Dynamic config result:")
                for content in config_result:
                    print(f"   {content.text}")
            except Exception as e:
                print(f"❌ Error getting dynamic config: {e}")
            
            # 3. Get experiment assignment
            print("\n3️⃣ Getting experiment assignment...")
            try:
                experiment_result = await session.call_tool(
                    "get_experiment",
                    arguments={
                        **example_user,
                        "experiment_name": "homepage_redesign"
                    }
                )
                print("✅ Experiment result:")
                for content in experiment_result:
                    print(f"   {content.text}")
            except Exception as e:
                print(f"❌ Error getting experiment: {e}")
            
            # 4. Get layer values
            print("\n4️⃣ Getting layer values...")
            try:
                layer_result = await session.call_tool(
                    "get_layer", 
                    arguments={
                        **example_user,
                        "layer_name": "personalization_layer"
                    }
                )
                print("✅ Layer result:")
                for content in layer_result:
                    print(f"   {content.text}")
            except Exception as e:
                print(f"❌ Error getting layer: {e}")
            
            # 5. Log an event
            print("\n5️⃣ Logging an event...")
            try:
                event_result = await session.call_tool(
                    "log_event",
                    arguments={
                        **example_user,
                        "event_name": "mcp_example_completed",
                        "value": "success",
                        "metadata": {
                            "source": "python_example",
                            "version": "1.0.0"
                        }
                    }
                )
                print("✅ Event logging result:")
                for content in event_result:
                    print(f"   {content.text}")
            except Exception as e:
                print(f"❌ Error logging event: {e}")
            
            print("\n" + "="*60)
            print("🎉 Statsig MCP example completed!")
            print("="*60)


if __name__ == "__main__":
    asyncio.run(run_example()) 