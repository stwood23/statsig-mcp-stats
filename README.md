# Statsig MCP Server

A Model Context Protocol (MCP) server that provides access to Statsig feature flags, dynamic configs, experiments, and event logging through a standard interface.

## Overview

This MCP server enables LLMs to interact with [Statsig](https://statsig.com), a feature management and experimentation platform. It exposes Statsig's core functionality as tools that can be called by MCP clients.

## Features

- **Feature Gates**: Check if feature flags are enabled for users
- **Dynamic Configs**: Retrieve configuration values for different user segments
- **Experiments & Layers**: Get experiment assignments and layer parameters
- **Event Logging**: Track custom events and user interactions
- **User Targeting**: Support for complex user targeting with custom attributes

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd statsig-mcp
```

2. Install dependencies:

```bash
pip install -e .
```

## Configuration

### Required Environment Variables

- `STATSIG_SERVER_SECRET_KEY`: Your Statsig server secret key (get from Statsig console)

### Optional Environment Variables

- `STATSIG_ENVIRONMENT`: Environment tier (e.g., "development", "staging", "production")
- `STATSIG_API_TIMEOUT`: API timeout in milliseconds (default: 3000)
- `STATSIG_DISABLE_LOGGING`: Set to "true" to disable event logging (default: false)

## Usage

### Running the Server

```bash
# Set your Statsig server secret key
export STATSIG_SERVER_SECRET_KEY="secret-your-key-here"

# Optional: Set environment
export STATSIG_ENVIRONMENT="development"

# Run the server
python -m statsig_mcp.server
```

### Available Tools

#### 1. `check_feature_gate`

Check if a feature gate is enabled for a user.

**Parameters:**

- `user_id` (string): User identifier
- `gate_name` (string): Name of the feature gate
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

**Example:**

```json
{
  "user_id": "user123",
  "gate_name": "new_checkout_flow",
  "user_email": "user@example.com",
  "custom_attributes": { "plan": "premium" }
}
```

#### 2. `get_dynamic_config`

Get dynamic configuration values for a user.

**Parameters:**

- `user_id` (string): User identifier
- `config_name` (string): Name of the dynamic config
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

#### 3. `get_experiment`

Get experiment assignment for a user.

**Parameters:**

- `user_id` (string): User identifier
- `experiment_name` (string): Name of the experiment
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

#### 4. `get_layer`

Get layer parameter values for a user.

**Parameters:**

- `user_id` (string): User identifier
- `layer_name` (string): Name of the layer
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

#### 5. `log_event`

Log a custom event.

**Parameters:**

- `user_id` (string): User identifier
- `event_name` (string): Name of the event
- `value` (string|number, optional): Event value
- `metadata` (object, optional): Event metadata
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

### Example MCP Client Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters
server_params = StdioServerParameters(
    command="python",
    args=["-m", "statsig_mcp.server"],
    env={"STATSIG_SERVER_SECRET_KEY": "your-secret-key"}
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Check a feature gate
            result = await session.call_tool(
                "check_feature_gate",
                arguments={
                    "user_id": "user123",
                    "gate_name": "new_feature",
                    "custom_attributes": {"plan": "premium"}
                }
            )
            print(f"Feature gate result: {result}")

            # Get dynamic config
            config = await session.call_tool(
                "get_dynamic_config",
                arguments={
                    "user_id": "user123",
                    "config_name": "ui_config"
                }
            )
            print(f"Config: {config}")

            # Log an event
            await session.call_tool(
                "log_event",
                arguments={
                    "user_id": "user123",
                    "event_name": "button_click",
                    "metadata": {"button": "checkout"}
                }
            )
```

## Development

### Setup Development Environment

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

### Project Structure

```
statsig_mcp/
├── __init__.py
├── server.py          # Main MCP server implementation
├── statsig_client.py  # Statsig client wrapper
└── types.py           # Type definitions
```

## Security Notes

- Never expose your Statsig server secret key in client-side code
- Use environment variables or secure configuration management for API keys
- The server secret key provides full access to your Statsig project

## Troubleshooting

### Common Issues

1. **"Statsig not initialized" error**: Ensure `STATSIG_SERVER_SECRET_KEY` is set
2. **Network timeouts**: Increase `STATSIG_API_TIMEOUT` if needed
3. **Feature gate not found**: Verify the gate name exists in your Statsig console

### Debug Mode

Set `STATSIG_DEBUG=true` to enable verbose logging:

```bash
export STATSIG_DEBUG=true
python -m statsig_mcp.server
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Resources

- [Statsig Documentation](https://docs.statsig.com)
- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [Statsig Python SDK](https://docs.statsig.com/server-core/python-core)
