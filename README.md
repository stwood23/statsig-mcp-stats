# Statsig MCP Server

Model Context Protocol server for [Statsig](https://statsig.com) feature flags and experimentation platform.

This MCP server enables AI assistants to interact with Statsig's Console API for comprehensive feature management and experimentation platform administration.

## Features

- 🚩 **Feature Gate Management**: Create, read, update, and delete feature gates
- ⚙️ **Dynamic Configuration Management**: Full CRUD operations for dynamic configs
- 🧪 **Experiment Management**: Create, read, update, and delete experiments
- 👥 **Segment Management**: Create and manage user segments
- 📊 **Metrics Access**: View and analyze platform metrics
- 📈 **Audit Logs**: Track changes and access audit trail
- 🎯 **Target Apps**: Manage target applications
- 🔑 **API Key Management**: List and manage API keys
- 👤 **Team Management**: List team users and get user details by email
- 📋 **Event Querying**: List available event types in your project

## 🆕 Extended Features

This version includes additional **Experiment Results Analysis** capabilities:
- 📊 **Statistical Analysis**: Get experiment results with confidence intervals, p-values, and significance tests
- 💓 **Pulse Monitoring**: Access experiment health metrics and performance indicators  
- 📈 **Metric Details**: Detailed analysis of individual metrics with statistical significance
- 📋 **Report Export**: Export comprehensive pulse reports in JSON, CSV, or summary formats

**New MCP Tools:** `get_experiment_results`, `get_experiment_pulse`, `get_metric_details`, `export_pulse_report`

👉 **See [README_EXTENDED.md](README_EXTENDED.md) for complete documentation of the results features.**

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

### 1. Get Your Console API Key

1. Go to [Statsig Console](https://console.statsig.com)
2. Navigate to **Project Settings** → **Keys & Environments**
3. Copy your **Console API Key** (not the client or server key)

### 2. Run the Server

#### With uv (Recommended):

```bash
# Using command-line arguments (MCP best practice)
uv run -m statsig_mcp --api-key "console-xxx"

# With additional options
uv run -m statsig_mcp \
  --api-key "console-xxx" \
  --environment "production" \
  --api-timeout 5000 \
  --debug

# Or with environment variables
STATSIG_CONSOLE_API_KEY="console-xxx" uv run -m statsig_mcp
```

#### With Python:

```bash
# Using flags (recommended)
python -m statsig_mcp --api-key "console-xxx"

# Or environment variables
export STATSIG_CONSOLE_API_KEY="console-xxx"
python -m statsig_mcp
```

### 3. Configuration Options

The server supports both **command-line arguments** (recommended for MCP) and **environment variables**:

#### Command-Line Arguments (MCP Best Practice)

```bash
uv run -m statsig_mcp --help
```

| Argument            | Type   | Default     | Description                        |
| ------------------- | ------ | ----------- | ---------------------------------- |
| `--api-key`         | string | None        | Statsig Console API key (required) |
| `--environment`     | string | development | Environment tier                   |
| `--api-timeout`     | int    | 3000        | API timeout in milliseconds        |
| `--disable-logging` | flag   | false       | Disable event logging to Statsig   |
| `--debug`           | flag   | false       | Enable debug logging               |

#### Environment Variables (Fallback)

| Variable                  | Description                    |
| ------------------------- | ------------------------------ |
| `STATSIG_CONSOLE_API_KEY` | Statsig Console API key        |
| `STATSIG_ENVIRONMENT`     | Environment tier               |
| `STATSIG_API_TIMEOUT`     | API timeout in milliseconds    |
| `STATSIG_DISABLE_LOGGING` | Disable logging (true/false)   |
| `STATSIG_DEBUG`           | Enable debug mode (true/false) |

### 4. MCP Client Configuration

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
        "console-xxx",
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
        "STATSIG_CONSOLE_API_KEY": "console-xxx",
        "STATSIG_ENVIRONMENT": "production"
      }
    }
  }
}
```

### 5. Test with MCP Inspector

```bash
# Test your server with the MCP Inspector
npx @modelcontextprotocol/inspector uv --directory . run statsig-mcp --api-key console-xxx
```

## Available Tools

The server provides 27 Console API tools organized by resource type:

### Feature Gates Management

- **`list_gates`**: List all feature gates
- **`get_gate`**: Get details of a specific feature gate
- **`create_gate`**: Create a new feature gate
- **`update_gate`**: Update an existing feature gate
- **`delete_gate`**: Delete a feature gate

### Experiments Management

- **`list_experiments`**: List all experiments
- **`get_experiment`**: Get details of a specific experiment
- **`create_experiment`**: Create a new experiment
- **`update_experiment`**: Update an existing experiment
- **`delete_experiment`**: Delete an experiment

### Dynamic Configs Management

- **`list_dynamic_configs`**: List all dynamic configs
- **`get_dynamic_config`**: Get details of a specific dynamic config
- **`create_dynamic_config`**: Create a new dynamic config
- **`update_dynamic_config`**: Update an existing dynamic config
- **`delete_dynamic_config`**: Delete a dynamic config

### Segments Management

- **`list_segments`**: List all segments
- **`get_segment`**: Get details of a specific segment
- **`create_segment`**: Create a new segment

### Analytics & Monitoring

- **`list_metrics`**: List all metrics
- **`get_metric`**: Get details of a specific metric
- **`list_audit_logs`**: List audit logs with optional date filtering

### Platform Management

- **`list_target_apps`**: List all target apps
- **`get_target_app`**: Get details of a specific target app
- **`list_api_keys`**: List all API keys

### Team & Events

- **`list_team_users`**: List all team members
- **`get_user_by_email`**: Get team member info by email
- **`query_events`**: Query event types and details

### Example Usage

#### Create a Feature Gate

````json
{
  "name": "new_checkout_flow",
  "description": "Enable new checkout flow for users",
  "is_enabled": true
}

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

Log a custom event directly to Statsig.

**Parameters:**

- `user_id` (string): User identifier
- `event_name` (string): Name of the event
- `value` (string|number, optional): Event value
- `metadata` (object, optional): Event metadata
- `user_email` (string, optional): User email
- `user_country` (string, optional): User country code
- `custom_attributes` (object, optional): Custom user attributes

### Project Management

#### 6. `query_events`

List all event types configured in your Statsig project.

**Parameters:** None

**Returns:** List of event names and their configurations.

#### 7. `get_user_by_email`

Get team member information by email address.

**Parameters:**

- `email` (string): Email address of the team member

#### 8. `list_team_users`

List all team members in your Statsig project.

**Parameters:** None

**Returns:** List of team members with their roles and permissions.

## Example MCP Client Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters with flags (recommended)
server_params = StdioServerParameters(
    command="uv",
    args=[
        "run", "-m", "statsig_mcp",
        "--api-key", "console-xxx",
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

            # List available events
            events = await session.call_tool("query_events")
            print(f"Available events: {events}")

            # Get team member info
            user_info = await session.call_tool(
                "get_user_by_email",
                arguments={"email": "teammate@company.com"}
            )
            print(f"Team member: {user_info}")
````

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
uv run -m statsig_mcp --api-key "console-xxx" --debug

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
├── __main__.py           # Module entry point
├── server.py             # Main MCP server implementation
├── console_client.py     # Statsig Console API client
└── types.py              # Type definitions

tests/                    # Test suite
├── test_server.py

examples/                 # Usage examples
├── client_example.py

pyproject.toml            # Project configuration
uv.lock                   # Locked dependencies (uv)
.venv/                    # Virtual environment (uv managed)
```

## Architecture

This MCP server uses a hybrid approach with three Statsig APIs:

1. **Console API** (`https://statsigapi.net/console/v1/*`) - For project management (team users, event types)
2. **HTTP API** (`https://api.statsig.com/v1/*`) - For real-time feature checks (gates, configs, experiments, layers)
3. **Events API** (`https://events.statsigapi.net/v1/*`) - For direct event logging

This approach provides the best balance of functionality and performance, allowing both management operations and real-time feature evaluation.

## Security Notes

- Never expose your Statsig Console API key in client-side code
- Use command-line arguments or environment variables for API keys
- The Console API key provides full access to your Statsig project
- Consider using separate API keys for different environments
- Console API keys are different from client keys and server secret keys

## Requirements

- Python 3.10+
- uv (recommended) or pip for package management

## Troubleshooting

### Common Issues

1. **"API key not found" error**: Ensure `--api-key` is provided or `STATSIG_CONSOLE_API_KEY` is set
2. **Network timeouts**: Increase timeout with `--api-timeout 5000`
3. **Feature gate not found**: Verify the gate name exists in your Statsig console
4. **Python version error**: This package requires Python 3.10+ (MCP requirement)
5. **Wrong API key type**: Make sure you're using a Console API key, not a client or server key

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# With command-line flag (recommended)
uv run -m statsig_mcp --api-key "console-xxx" --debug

# With environment variable
STATSIG_DEBUG=true uv run -m statsig_mcp --api-key "console-xxx"
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
- [Statsig Console API](https://docs.statsig.com/console-api/all-endpoints-generated)
- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [uv Documentation](https://docs.astral.sh/uv/)
