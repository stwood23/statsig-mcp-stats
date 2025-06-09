#!/usr/bin/env python3
"""
Main entry point for the Statsig MCP server.

This module allows the package to be run with `python -m statsig_mcp`.
"""

import asyncio
import sys

from .server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1) 