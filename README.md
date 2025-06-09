# Statsig MCP Server

Model Context Protocol server for [Statsig](https://statsig.com) feature flags and experimentation platform.

This MCP server enables AI assistants to interact with Statsig's feature management and experimentation platform, allowing them to check feature flags, retrieve dynamic configurations, get experiment assignments, and log custom events.

## Features

- 🚩 **Feature Gate Checking**: Determine if features are enabled for users
- ⚙️ **Dynamic Configuration**: Retrieve configuration values based on user context
- 🧪 **Experiment Assignment**: Get experiment variations for A/B testing
- 📊 **Layer Parameter Access**: Retrieve values from Statsig layers
- 📈 **Event Logging**: Track custom events for analytics

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/GeLi2001/statsig-mcp.git
cd statsig-mcp

# Install dependencies with uv
uv sync

# Install with dev dependencies
uv sync --extra dev
```

### Using pip

```bash
# Install from source
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

### 1. Run the Server

#### With uv (Recommended):

```bash
# Using command-line arguments (MCP best practice)
uv run -m statsig_mcp --api-key "your-secret-key"

# With additional options
uv run -m statsig_mcp \
  --api-key "your-secret-key" \
  --environment "production" \
  --api-timeout 5000 \
  --debug

# Or with environment variables
STATSIG_SERVER_SECRET_KEY="your-key" uv run -m statsig_mcp
```

#### With Python:

```bash
# Using flags (recommended)
python -m statsig_mcp --api-key "your-secret-key"

# Or environment variables
export STATSIG_SERVER_SECRET_KEY="your-secret-key"
python -m statsig_mcp
```

### 2. Configuration Options

The server supports both **command-line arguments** (recommended for MCP) and **environment variables**:

#### Command-Line Arguments (MCP Best Practice)

```bash
uv run -m statsig_mcp --help
```

| Argument            | Type   | Default     | Description                          |
| ------------------- | ------ | ----------- | ------------------------------------ |
| `--api-key`         | string | None        | Statsig server secret key (required) |
| `--environment`     | string | development | Environment tier                     |
| `--api-timeout`     | int    | 3000        | API timeout in milliseconds          |
| `--disable-logging` | flag   | false       | Disable event logging to Statsig     |
| `--debug`           | flag   | false       | Enable debug logging                 |

#### Environment Variables (Fallback)

| Variable                    | Description                    |
| --------------------------- | ------------------------------ |
| `STATSIG_SERVER_SECRET_KEY` | Statsig server secret key      |
| `STATSIG_ENVIRONMENT`       | Environment tier               |
| `STATSIG_API_TIMEOUT`       | API timeout in milliseconds    |
| `STATSIG_DISABLE_LOGGING`   | Disable logging (true/false)   |
| `STATSIG_DEBUG`             | Enable debug mode (true/false) |

### 3. MCP Client Configuration

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "statsig": {
      "command": "uv",
      "args": [
        "run",
        "-m",
        "statsig_mcp",
        "--api-key",
        "your-secret-key",
        "--environment",
        "production"
      ]
    }
  }
}
```

#### Alternative with Environment Variables

```json
{
  "mcpServers": {
    "statsig": {
      "command": "uv",
      "args": ["run", "-m", "statsig_mcp"],
      "env": {
        "STATSIG_SERVER_SECRET_KEY": "your-secret-key",
        "STATSIG_ENVIRONMENT": "production"
      }
    }
  }
}
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

# Create server parameters with flags (recommended)
server_params = StdioServerParameters(
    command="uv",
    args=[
        "run", "-m", "statsig_mcp",
        "--api-key", "your-secret-key",
        "--environment", "production",
        "--debug"
    ]
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

#### Using uv (Recommended):

```bash
# Clone and setup
git clone https://github.com/GeLi2001/statsig-mcp.git
cd statsig-mcp

# Install all dependencies including dev tools
uv sync --extra dev

# Run tests
uv run pytest

# Format code
uv run black .

# Type checking
uv run mypy .

# Linting
uv run ruff check .
```

#### Using pip:

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

### Running Commands

With `uv`, you can run any command in the virtual environment:

```bash
# Run the server with flags
uv run -m statsig_mcp --api-key "test-key" --debug

# Run tests with verbose output
uv run pytest -v

# Run validation script
uv run python validate.py

# Format and lint
uv run black .
uv run ruff check --fix .
```

### Project Structure

```
statsig_mcp/
├── __init__.py
├── __main__.py        # Module entry point
├── server.py          # Main MCP server implementation
├── statsig_client.py  # Statsig client wrapper
└── types.py           # Type definitions

tests/                 # Test suite
├── test_server.py

pyproject.toml         # Project configuration
uv.lock               # Locked dependencies (uv)
.venv/                # Virtual environment (uv managed)
```

## Security Notes

- Never expose your Statsig server secret key in client-side code
- Use command-line arguments or environment variables for API keys
- The server secret key provides full access to your Statsig project
- Consider using separate API keys for different environments

## Requirements

- Python 3.10+
- uv (recommended) or pip for package management

## Troubleshooting

### Common Issues

1. **"Statsig not initialized" error**: Ensure `--api-key` is provided or `STATSIG_SERVER_SECRET_KEY` is set
2. **Network timeouts**: Increase timeout with `--api-timeout 5000`
3. **Feature gate not found**: Verify the gate name exists in your Statsig console
4. **Python version error**: This package requires Python 3.10+ (MCP requirement)

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# With command-line flag (recommended)
uv run -m statsig_mcp --api-key "your-key" --debug

# With environment variable
STATSIG_DEBUG=true uv run -m statsig_mcp --api-key "your-key"
```

### Help

Get help with command-line options:

```bash
uv run -m statsig_mcp --help
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run tests and linting: `uv run pytest && uv run ruff check`
6. Submit a pull request

## Resources

- [Statsig Documentation](https://docs.statsig.com)
- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [Statsig Python SDK](https://docs.statsig.com/server-core/python-core)
- [uv Documentation](https://docs.astral.sh/uv/)
