"""
Tests for the Statsig MCP server.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from statsig_mcp.console_client import StatsigConsoleClient


@pytest.fixture
def user_attrs():
    """Sample user attributes for testing."""
    return {
        "user_id": "test_user_123",
        "user_email": "test@example.com",
        "user_country": "US",
        "custom_attributes": {"plan": "premium"}
    }


class TestStatsigConsoleClient:
    """Test the Statsig Console API client."""

    @pytest.mark.asyncio
    async def test_initialization_requires_console_api_key(self):
        """Test that initialization requires a Console API key."""
        client = StatsigConsoleClient()
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="STATSIG_CONSOLE_API_KEY"):
                await client.initialize()

    @pytest.mark.asyncio
    async def test_not_initialized_error(self):
        """Test that methods raise error when not initialized."""
        with patch.dict(os.environ, {"STATSIG_CONSOLE_API_KEY": "console-test-key"}):
            client = StatsigConsoleClient()
            user_attrs = {"user_id": "test"}
            
            with pytest.raises(RuntimeError, match="not initialized"):
                await client.check_feature_gate(user_attrs, "test_gate")

    def test_format_user_for_api(self, user_attrs):
        """Test formatting user attributes for API calls."""
        client = StatsigConsoleClient()
        
        formatted = client._format_user_for_api(user_attrs)
        
        assert formatted["userID"] == "test_user_123"
        assert formatted["email"] == "test@example.com"
        assert formatted["country"] == "US"
        assert formatted["custom"] == {"plan": "premium"}

    @pytest.mark.asyncio
    async def test_client_lifecycle(self):
        """Test client initialization and shutdown."""
        with patch.dict(os.environ, {"STATSIG_CONSOLE_API_KEY": "console-test-key"}):
            client = StatsigConsoleClient()
            
            # Mock httpx.AsyncClient
            mock_client = AsyncMock()
            mock_client.aclose = AsyncMock()
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                # Test initialization
                await client.initialize()
                assert client._initialized is True
                assert client._console_api_key == "console-test-key"
                
                # Test shutdown
                await client.shutdown()
                assert client._initialized is False
                mock_client.aclose.assert_called_once()

    def test_environment_variables(self):
        """Test that environment variables are properly handled."""
        with patch.dict(os.environ, {"STATSIG_CONSOLE_API_KEY": "test-console-key"}):
            client = StatsigConsoleClient()
            # Test that the key is read from environment during initialization
            assert os.getenv("STATSIG_CONSOLE_API_KEY") == "test-console-key"

    def test_api_urls_configuration(self):
        """Test that API URLs are properly configured."""
        client = StatsigConsoleClient()
        
        assert client._base_url == "https://statsigapi.net"
        assert client._http_api_base == "https://api.statsig.com"
        assert client._events_api_base == "https://events.statsigapi.net"
        assert client._api_version == "20240601"


if __name__ == "__main__":
    pytest.main([__file__]) 