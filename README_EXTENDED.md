# Statsig MCP Server - Experiment Results Extensions

This document describes the extended functionality added to the base Statsig MCP Server to provide comprehensive experiment results and analytics capabilities through Statsig's Console API.

## Overview

The extended Statsig MCP Server builds upon the foundation of feature flag and experiment management by adding powerful results analysis tools. These extensions enable AI assistants to:

- Fetch comprehensive experiment results with statistical analysis
- Access detailed metric data including confidence intervals and significance tests
- Export pulse reports in multiple formats
- Analyze experiment health and performance metrics
- Cache results for improved performance

## New Features

### 🧪 Experiment Results Analysis
- **Get Experiment Results**: Retrieve complete experiment outcomes with all metrics
- **Metric Details**: Access specific metric results with statistical significance data
- **Health Checks**: Monitor experiment health and validity
- **Time-series Data**: Access historical performance data

### 📊 Advanced Analytics
- **Statistical Analysis**: Confidence intervals, p-values, and effect sizes
- **Pulse Reports**: Comprehensive experiment summaries
- **Metric Comparisons**: Side-by-side variant analysis
- **Custom Metrics**: Support for business-specific KPIs

### 🚀 Performance Enhancements
- **Intelligent Caching**: Configurable caching layer for faster response times
- **Rate Limiting**: Built-in protection against API limits
- **Error Recovery**: Robust error handling with automatic retries
- **Batch Operations**: Efficient bulk data retrieval

## Architecture

### Console API Integration
The extensions integrate with Statsig's Console API endpoints:

```
Console API (statsigapi.net/console/v1/*)
├── Experiments
│   ├── /experiments/{id}/results
│   ├── /experiments/{id}/pulse
│   └── /experiments/{id}/metrics
├── Metrics
│   ├── /metrics/{id}/details
│   └── /metrics/{id}/timeseries
└── Reports
    ├── /reports/pulse/{experiment_id}
    └── /reports/export/{format}
```

### Data Flow
```
AI Assistant Request
        ↓
MCP Tool Handler
        ↓
Cache Check (optional)
        ↓
Console API Client
        ↓
Results Formatter
        ↓
Structured Response
```

## Setup

### Prerequisites
- Existing Statsig MCP Server setup (see main README.md)
- Statsig Console API key with results access permissions
- Python 3.10+ environment

### Configuration

1. **Update Environment Variables**
   ```bash
   # Copy the extended environment template
   cp env.example .env
   
   # Edit with your values
   vim .env
   ```

2. **Required Environment Variables**
   ```bash
   # Core API access
   STATSIG_CONSOLE_API_KEY=console-your-key-here
   
   # Results functionality (optional)
   STATSIG_RESULTS_CACHE_TTL=300
   STATSIG_RESULTS_CACHE_ENABLED=true
   STATSIG_API_TIMEOUT_MS=5000
   STATSIG_RETRY_ATTEMPTS=3
   STATSIG_DEBUG_RESULTS=false
   ```

3. **Start Extended Server**
   ```bash
   # With uv (recommended)
   uv run -m statsig_mcp --api-key "console-xxx" --enable-results
   
   # With Python
   python -m statsig_mcp --api-key "console-xxx" --enable-results
   ```

## New MCP Tools

### 1. Get Experiment Results
Retrieves comprehensive experiment results including all metrics and statistical analysis.

**Tool**: `get_experiment_results`

**Parameters**:
- `experiment_id` (required): Experiment identifier
- `include_metrics` (optional): Include detailed metric breakdowns
- `include_health` (optional): Include experiment health checks

**Example Response**:
```json
{
  "experiment_id": "exp_123",
  "status": "decision_made",
  "results": {
    "primary_metrics": [...],
    "secondary_metrics": [...],
    "health_metrics": [...],
    "statistical_significance": true,
    "confidence_interval": "95%"
  }
}
```

### 2. Get Metric Details
Fetches detailed analysis for specific metrics including statistical significance.

**Tool**: `get_metric_details`

**Parameters**:
- `experiment_id` (required): Experiment identifier  
- `metric_name` (required): Name of the metric to analyze
- `variant_comparison` (optional): Specific variant comparison

### 3. Export Pulse Report
Generates comprehensive pulse reports in various formats.

**Tool**: `export_pulse_report`

**Parameters**:
- `experiment_id` (required): Experiment identifier
- `format` (optional): Export format (json, csv, summary)
- `include_charts` (optional): Include visualization data

## Usage Examples

### Basic Results Retrieval
```python
# Using MCP client
response = await mcp_client.call_tool(
    "get_experiment_results",
    {
        "experiment_id": "mobile_checkout_test",
        "include_metrics": True,
        "include_health": True
    }
)
```

### Metric Analysis
```python
# Analyze specific metric
metric_data = await mcp_client.call_tool(
    "get_metric_details", 
    {
        "experiment_id": "mobile_checkout_test",
        "metric_name": "conversion_rate",
        "variant_comparison": "treatment_vs_control"
    }
)
```

### Report Export
```python
# Export comprehensive report
report = await mcp_client.call_tool(
    "export_pulse_report",
    {
        "experiment_id": "mobile_checkout_test", 
        "format": "json",
        "include_charts": True
    }
)
```

## Performance Considerations

### Caching Strategy
- **Default TTL**: 5 minutes for experiment results
- **Cache Keys**: Based on experiment ID and metric parameters
- **Memory Usage**: Configurable cache size limits
- **Invalidation**: Automatic cache refresh on experiment status changes

### Rate Limiting
- **Console API Limits**: Respects Statsig's rate limits
- **Retry Logic**: Exponential backoff for failed requests
- **Circuit Breaker**: Temporary request blocking on sustained failures

## Error Handling

### Common Scenarios
- **Experiment Not Found**: Clear error message with suggestions
- **Insufficient Permissions**: API key permission guidance
- **Rate Limit Exceeded**: Automatic retry with backoff
- **Invalid Metric**: List of available metrics provided

### Debug Mode
Enable debug logging for troubleshooting:
```bash
STATSIG_DEBUG_RESULTS=true uv run -m statsig_mcp --api-key "console-xxx"
```

## Security Considerations

- **API Key Security**: Console API keys provide broad access - store securely
- **Rate Limiting**: Built-in protection against accidental API abuse
- **Data Privacy**: Results data may contain sensitive business metrics
- **Environment Isolation**: Use different API keys for development/production

## Troubleshooting

### Common Issues

1. **"Results not available"**
   - Verify experiment has sufficient data
   - Check experiment status (must be running or completed)
   - Ensure Console API key has results permissions

2. **Cache issues**
   - Clear cache: set `STATSIG_RESULTS_CACHE_ENABLED=false`
   - Check cache TTL settings
   - Verify memory availability

3. **Slow responses**
   - Enable caching: `STATSIG_RESULTS_CACHE_ENABLED=true`
   - Reduce `STATSIG_API_TIMEOUT_MS` if needed
   - Check network connectivity to Statsig

### Support
- Review logs with `STATSIG_DEBUG_RESULTS=true`
- Check main README.md for base functionality issues
- Verify API key permissions in Statsig Console

## Development

### Testing
```bash
# Run extended functionality tests
uv run pytest tests/test_results/ -v

# Test specific functionality
uv run pytest tests/test_results/test_experiment_results.py
```

### Contributing
When extending this functionality:
1. Add comprehensive tests for new features
2. Update this documentation
3. Follow existing code patterns and error handling
4. Consider performance impact and caching needs

---

*This extension maintains full backward compatibility with the base Statsig MCP Server functionality.*
