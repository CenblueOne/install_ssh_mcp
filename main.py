#!/usr/bin/env python3
"""Entry point untuk Hermes MCP SSH Server."""
from ssh_mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
