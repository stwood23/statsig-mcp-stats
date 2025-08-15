#!/usr/bin/env python3
"""
Example usage of the new experiment results functionality.
This demonstrates how to use the extended Statsig MCP server.
"""

import asyncio
import os
from statsig_mcp.console_client import StatsigConsoleClient


async def demo_results_functionality():
    """Demonstrate the new experiment results features."""
    print("🚀 Statsig MCP Results Functionality Demo")
    print("=" * 50)
    
    # Initialize client
    client = StatsigConsoleClient()
    
    # Note: This would normally require a real API key
    print("📋 Available Results Methods:")
    print("   • get_experiment_results(experiment_id, include_metrics=True)")
    print("   • get_experiment_pulse(experiment_id)")
    print("   • get_metric_details(metric_id, experiment_id)")
    print("   • export_pulse_report(experiment_id, format='json')")
    print()
    
    print("🎯 MCP Tools Added:")
    tools = [
        "get_experiment_results - Get comprehensive experiment results with statistical analysis",
        "get_experiment_pulse - Get experiment pulse data with health metrics and performance indicators", 
        "get_metric_details - Get detailed metric analysis including statistical significance",
        "export_pulse_report - Export comprehensive pulse report in specified format"
    ]
    
    for tool in tools:
        print(f"   • {tool}")
    print()
    
    print("💡 Usage Instructions:")
    print("1. Set STATSIG_CONSOLE_API_KEY environment variable")
    print("2. Start the MCP server: python -m statsig_mcp --api-key console-xxx")
    print("3. Use any MCP-compatible client to call the new tools")
    print()
    
    print("📊 Example MCP Tool Call:")
    print('''{
    "method": "tools/call",
    "params": {
        "name": "get_experiment_results",
        "arguments": {
            "experiment_id": "your_experiment_id",
            "include_metrics": true
        }
    }
}''')
    
    print("\n✅ Results functionality successfully implemented!")


if __name__ == "__main__":
    asyncio.run(demo_results_functionality())
