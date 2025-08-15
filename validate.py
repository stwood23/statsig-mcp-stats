#!/usr/bin/env python3
"""
Validation script for the Statsig MCP server.
Tests that the server can be imported and basic functionality works.
"""

import asyncio
import sys
import traceback


async def test_import():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import statsig_mcp
        print("✅ statsig_mcp package imported successfully")
        
        from statsig_mcp.types import StatsigUserAttributes, ExperimentResultData, MetricResult
        print("✅ types module imported successfully")
        
        from statsig_mcp.console_client import StatsigConsoleClient
        print("✅ console_client module imported successfully")
        
        from statsig_mcp.server import main, server
        print("✅ server module imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False


async def test_client_creation():
    """Test that the Statsig Console client can be created."""
    print("\n🔧 Testing client creation...")
    
    try:
        from statsig_mcp.console_client import StatsigConsoleClient
        
        client = StatsigConsoleClient()
        print("✅ StatsigConsoleClient created successfully")
        
        # Test that initialization fails without API key (expected)
        try:
            await client.initialize()
            print("❌ Expected initialization to fail without API key")
            return False
        except ValueError as e:
            if "STATSIG_CONSOLE_API_KEY" in str(e):
                print("✅ Correctly requires STATSIG_CONSOLE_API_KEY")
                return True
            else:
                print(f"❌ Unexpected error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        traceback.print_exc()
        return False


async def test_server_structure():
    """Test that the server has the expected structure."""
    print("\n🏗️ Testing server structure...")
    
    try:
        from statsig_mcp.server import server

        # Check if server is properly configured
        if hasattr(server, 'list_tools'):
            print("✅ Server has list_tools handler")
        else:
            print("❌ Server missing list_tools handler")
            return False
            
        if hasattr(server, 'call_tool'):
            print("✅ Server has call_tool handler")
        else:
            print("❌ Server missing call_tool handler")
            return False
            
        print("✅ Server structure looks good")
        return True
        
    except Exception as e:
        print(f"❌ Server structure test failed: {e}")
        traceback.print_exc()
        return False


async def main():
    """Run all validation tests."""
    print("🚀 Statsig MCP Server Validation")
    print("=" * 40)
    
    tests = [
        test_import,
        test_client_creation,
        test_server_structure,
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 40)
    print("📊 Validation Results:")
    print(f"✅ Passed: {sum(results)} / {len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)} / {len(results)}")
    
    if all(results):
        print("\n🎉 All validation tests passed!")
        print("\nTo use the server:")
        print("1. Set your STATSIG_CONSOLE_API_KEY environment variable")
        print("   Get it from: https://console.statsig.com → Project Settings → Keys & Environments")
        print("2. Run: python -m statsig_mcp --api-key console-xxx")
        print("3. Or with uv: uv run -m statsig_mcp --api-key console-xxx")
        print("4. Connect using an MCP client or test with MCP Inspector")
        return 0
    else:
        print("\n💥 Some validation tests failed!")
        print("Please check the errors above and fix them.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 