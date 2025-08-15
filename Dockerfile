FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Expose port for MCP server
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV STATSIG_CONSOLE_API_KEY=""

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import statsig_mcp; print('healthy')" || exit 1

# Run the MCP server
CMD ["python", "-m", "statsig_mcp", "--api-key", "${STATSIG_CONSOLE_API_KEY}"]
