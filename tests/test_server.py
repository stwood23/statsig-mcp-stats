"""
Tests for the Statsig MCP server.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from statsig_mcp.statsig_client import StatsigMCPClient


@pytest.fixture
def user_attrs():
    """Sample user attributes for testing."""
    return {
        "user_id": "test_user_123",
        "user_email": "test@example.com",
        "user_country": "US",
        "custom_attributes": {"plan": "premium"}
    }


class TestStatsigMCPClient:
    """Test the Statsig MCP client wrapper."""

    @pytest.mark.asyncio
    async def test_initialization_requires_secret_key(self):
        """Test that initialization requires a secret key."""
        client = StatsigMCPClient()
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="STATSIG_SERVER_SECRET_KEY"):
                await client.initialize()

    @pytest.mark.asyncio
    async def test_not_initialized_error(self):
        """Test that methods raise error when not initialized."""
        with patch.dict(os.environ, {"STATSIG_SERVER_SECRET_KEY": "test-key"}):
            client = StatsigMCPClient()
            user_attrs = {"user_id": "test"}
            
            with pytest.raises(RuntimeError, match="not initialized"):
                await client.check_feature_gate(user_attrs, "test_gate")

    def test_create_statsig_user(self, user_attrs):
        """Test creating a StatsigUser from attributes."""
        client = StatsigMCPClient()
        
        # Mock the StatsigUser class
        with patch('statsig_mcp.statsig_client.StatsigUser') as mock_user:
            client._create_statsig_user(user_attrs)
            
            mock_user.assert_called_once_with(
                user_id="test_user_123",
                email="test@example.com",
                country="US",
                custom={"plan": "premium"}
            )

    @pytest.mark.asyncio
    async def test_client_lifecycle(self):
        """Test client initialization and shutdown."""
        with patch.dict(os.environ, {"STATSIG_SERVER_SECRET_KEY": "test-key"}):
            client = StatsigMCPClient()
            
            # Mock the Statsig SDK
            with patch('statsig_mcp.statsig_client.Statsig') as mock_statsig:
                mock_instance = AsyncMock()
                mock_statsig.return_value = mock_instance
                
                # Test initialization
                await client.initialize()
                assert client._initialized is True
                mock_instance.initialize.assert_called_once()
                
                # Test shutdown
                await client.shutdown()
                assert client._initialized is False
                mock_instance.shutdown.assert_called_once()


class TestStatsigMCPIntegration:
    """Integration tests for the Statsig MCP server."""

    @pytest.mark.asyncio
    async def test_feature_gate_check(self, user_attrs):
        """Test feature gate checking."""
        with patch.dict(os.environ, {"STATSIG_SERVER_SECRET_KEY": "test-key"}):
            client = StatsigMCPClient()
            
            # Mock the Statsig SDK
            with patch('statsig_mcp.statsig_client.Statsig') as mock_statsig:
                mock_instance = AsyncMock()
                mock_statsig.return_value = mock_instance
                
                # Mock feature gate response - make it a regular MagicMock
                mock_gate = MagicMock()
                mock_gate.value = True
                mock_gate.rule_id = "test_rule_123"
                mock_gate.group_name = "test_group"
                # Make get_feature_gate return a regular MagicMock, not a coroutine
                mock_instance.get_feature_gate = MagicMock(return_value=mock_gate)
                
                await client.initialize()
                result = await client.check_feature_gate(user_attrs, "test_gate")
                
                assert result["gate_name"] == "test_gate"
                assert result["value"] is True
                assert result["rule_id"] == "test_rule_123"

    @pytest.mark.asyncio
    async def test_dynamic_config_get(self, user_attrs):
        """Test dynamic config retrieval."""
        with patch.dict(os.environ, {"STATSIG_SERVER_SECRET_KEY": "test-key"}):
            client = StatsigMCPClient()
            
            # Mock the Statsig SDK
            with patch('statsig_mcp.statsig_client.Statsig') as mock_statsig:
                mock_instance = AsyncMock()
                mock_statsig.return_value = mock_instance
                
                # Mock config response - make it a regular MagicMock
                mock_config = MagicMock()
                mock_config.value = {"theme": "dark", "layout": "grid"}
                mock_config.rule_id = "config_rule_456"
                mock_config.group_name = "config_group"
                # Make get_dynamic_config return a regular MagicMock, not a coroutine
                mock_instance.get_dynamic_config = MagicMock(return_value=mock_config)
                
                await client.initialize()
                result = await client.get_dynamic_config(user_attrs, "ui_config")
                
                assert result["config_name"] == "ui_config"
                assert result["value"] == {"theme": "dark", "layout": "grid"}
                assert result["rule_id"] == "config_rule_456"

    @pytest.mark.asyncio
    async def test_event_logging(self, user_attrs):
        """Test event logging."""
        with patch.dict(os.environ, {"STATSIG_SERVER_SECRET_KEY": "test-key"}):
            client = StatsigMCPClient()
            
            # Mock the Statsig SDK
            with patch('statsig_mcp.statsig_client.Statsig') as mock_statsig:
                mock_instance = AsyncMock()
                mock_statsig.return_value = mock_instance
                
                # Make log_event a regular MagicMock, not a coroutine
                mock_instance.log_event = MagicMock()
                
                await client.initialize()
                result = await client.log_event(
                    user_attrs,
                    "test_event",
                    "test_value",
                    {"source": "test"}
                )
                
                assert result["success"] is True
                assert "successfully" in result["message"]
                mock_instance.log_event.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__]) 