# Team Setup Guide - Enhanced Statsig MCP Server

This guide helps team members set up the enhanced Statsig MCP server with experiment results functionality.

## 🚀 Quick Setup (5 minutes)

### 1. Get Your Statsig Console API Key
- Go to [Statsig Console](https://console.statsig.com)
- Navigate: **Project Settings → Keys & Environments**  
- Create **"Console API Key"** (starts with `console-`)
- Copy the key - you'll need it in step 3

### 2. Set Up Repository Access
**Option A: Fork (Recommended)**
- Go to https://github.com/stwood23/statsig-mcp-stats
- Click "Fork" to create your own copy

**Option B: Direct Access**  
- Use the original repository if you have collaborator access

### 3. Add Your API Key as a Secret
- In your repository: **Settings → Secrets and variables → Codespaces**
- **New repository secret:**
  - Name: `STATSIG_CONSOLE_API_KEY`
  - Value: `console-your-key-here`

### 4. Create GitHub Codespace  
- Click green **"Code"** button → **"Codespaces"** → **"Create codespace"**
- Wait 2-3 minutes for automatic setup
- **🚀 MCP Server starts automatically!** (runs in background)

### 5. Verify Server is Running
Check that the server started automatically:
```bash
# Check if server is running
ps aux | grep statsig_mcp

# View server logs (optional)
tail -f mcp_server.log
```

**Note:** The server now starts automatically when your Codespace launches - no manual startup required!

### 6. Configure Cursor
Update your local `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "statsig-enhanced": {
      "command": "ssh", 
      "args": [
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "YOUR_CODESPACE_URL.github.dev",
        "cd /workspaces/statsig-mcp-stats && python -m statsig_mcp --api-key $STATSIG_CONSOLE_API_KEY"
      ]
    }
  }
}
```

**Replace `YOUR_CODESPACE_URL.github.dev`** with your actual Codespace URL.

### 7. Restart Cursor & Test
- Restart Cursor to load the new configuration
- Test the new experiment results tools!

## 🎯 New Tools Available

- **`get_experiment_results`** - Statistical analysis with confidence intervals
- **`get_experiment_pulse`** - Health metrics and performance indicators
- **`get_metric_details`** - Detailed metric analysis with significance  
- **`export_pulse_report`** - Export reports in JSON/CSV/summary formats

## 🔒 Security Features

- ✅ Your API key is stored securely in GitHub secrets
- ✅ Not visible in repository code or git history
- ✅ Each team member uses their own API key
- ✅ Easy to rotate keys without code changes

## 🆘 Troubleshooting

**Codespace won't start?**
- Check that you added the `STATSIG_CONSOLE_API_KEY` secret correctly

**Cursor can't connect?**  
- Verify your Codespace URL in the MCP configuration
- Make sure the Codespace is running
- Restart Cursor after configuration changes

**API key issues?**
- Ensure you created a "Console API Key" (not regular API key)
- Check the key starts with `console-`
- Verify the key has experiment results permissions

## 💬 Need Help?

Contact the team member who shared this repository for assistance!
