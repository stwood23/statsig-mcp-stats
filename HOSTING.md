# Hosting the Enhanced Statsig MCP Server

This guide covers various ways to host your enhanced Statsig MCP server without running it locally.

## 🚀 Option 1: GitHub Codespaces (Easiest)

**Best for:** Quick setup, development, and testing

### Steps:
1. **Push your repo to GitHub** (already done ✅)
2. **Go to your GitHub repo** → Click "Code" → "Codespaces" → "Create codespace"
3. **Set environment variable:**
   ```bash
   export STATSIG_CONSOLE_API_KEY=console-your-key-here
   ```
4. **Start the server:**
   ```bash
   python -m statsig_mcp --api-key $STATSIG_CONSOLE_API_KEY
   ```

### Update Cursor MCP config:
```json
{
  "mcpServers": {
    "statsig-codespace": {
      "command": "ssh",
      "args": [
        "your-codespace-url",
        "python -m statsig_mcp --api-key console-xxx"
      ]
    }
  }
}
```

---

## 🐳 Option 2: Docker Container (Most Flexible)

**Best for:** Local Docker, cloud deployment, team sharing

### Local Docker:
```bash
# Build the container
docker build -t statsig-mcp .

# Run with your API key
docker run -p 8000:8000 -e STATSIG_CONSOLE_API_KEY=console-xxx statsig-mcp
```

### Docker Compose:
```bash
# Set your API key
echo "STATSIG_CONSOLE_API_KEY=console-xxx" > .env

# Start the service
docker-compose up -d
```

### Deploy to cloud:
- **DigitalOcean App Platform**
- **AWS ECS/Fargate** 
- **Google Cloud Run**
- **Azure Container Instances**

---

## ☁️ Option 3: Railway (1-Click Deploy)

**Best for:** Zero-config cloud hosting

### Steps:
1. **Connect your GitHub repo to Railway**
2. **Set environment variable:** `STATSIG_CONSOLE_API_KEY=console-xxx`
3. **Deploy automatically** from your repo

### Update Cursor MCP config:
```json
{
  "mcpServers": {
    "statsig-railway": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://your-app.railway.app",
        "--header",
        "authorization:Bearer your-token"
      ]
    }
  }
}
```

---

## 🌍 Option 4: Render (Free Tier Available)

**Best for:** Free hosting with automatic deploys

### Steps:
1. **Connect GitHub repo to Render**
2. **Choose "Web Service"**
3. **Build Command:** `pip install -e .`
4. **Start Command:** `python -m statsig_mcp --api-key $STATSIG_CONSOLE_API_KEY`
5. **Add environment variable:** `STATSIG_CONSOLE_API_KEY`

---

## 🏢 Option 5: Team Server (Self-Hosted)

**Best for:** Enterprise/team deployment

### Ubuntu/Debian Server:
```bash
# Install Python and dependencies
sudo apt update && sudo apt install python3 python3-pip git

# Clone your repo
git clone https://github.com/stwood23/statsig-mcp-stats.git
cd statsig-mcp-stats

# Install dependencies
pip3 install -e .

# Create systemd service
sudo tee /etc/systemd/system/statsig-mcp.service << EOF
[Unit]
Description=Statsig MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/statsig-mcp-stats
Environment=STATSIG_CONSOLE_API_KEY=console-xxx
ExecStart=/usr/bin/python3 -m statsig_mcp --api-key console-xxx
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start the service
sudo systemctl enable statsig-mcp
sudo systemctl start statsig-mcp
```

---

## 📊 Comparison

| Option | Cost | Setup Time | Scalability | Best For |
|--------|------|------------|-------------|----------|
| **Codespaces** | Free tier | 2 minutes | Low | Development/Testing |
| **Docker Local** | Free | 5 minutes | Medium | Local team |
| **Railway** | $5+/month | 3 minutes | High | Production |
| **Render** | Free tier | 5 minutes | Medium | Small projects |
| **Self-hosted** | Server cost | 15 minutes | High | Enterprise |

---

## 🔧 Cursor Configuration for Remote Servers

For any hosted solution, update your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "statsig-remote": {
      "command": "npx",
      "args": [
        "mcp-remote", 
        "https://your-hosted-server.com",
        "--header",
        "authorization:Bearer your-auth-token"
      ]
    }
  }
}
```

---

## 🎯 Recommended Approach

1. **For testing:** Use GitHub Codespaces
2. **For production:** Use Railway or Render
3. **For enterprise:** Self-hosted with Docker

All options will give you the same enhanced functionality with the 4 new experiment results tools!
