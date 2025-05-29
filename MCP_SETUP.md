# 🤖 MCP Configuration - Football API

This guide explains how to configure the Football API MCP (Model Context Protocol) server in different IDEs and AI clients.

## 🚀 Quick Start

1. **Run the server**: 
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Verify MCP**:
   ```bash
   curl http://localhost:8000/mcp
   ```

3. **Configure in your IDE** (instructions below)

## 🔧 Configuration by IDE/Client

### Cursor IDE

**Location**: `~/.cursor/mcp.json` (Windows: `C:\Users\{user}\.cursor\mcp.json`)

```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Restart Cursor** after configuration.

### Windsurf IDE

**Location**: `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Claude Desktop

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux**: `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### VS Code (with MCP extensions)

If you're using an MCP extension for VS Code:

```json
{
  "mcp.servers": {
    "football-api-mcp": {
      "url": "http://localhost:8000/mcp",
      "name": "Football Data API",
      "description": "Football data from main European leagues"
    }
  }
}
```

## 🌐 Production Configuration

### Production URL
```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "https://yourdomain.com/mcp"
    }
  }
}
```

### Configuration with Authentication (future)
```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "https://yourdomain.com/mcp",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

## 🛠️ Clients that Don't Support SSE

For clients that don't support Server-Sent Events directly, use `mcp-remote`:

```json
{
  "mcpServers": {
    "football-api-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```

## 🔍 Available Tools

The MCP server automatically exposes these tools:

### 1. `health_check`
Check API status and database connectivity
```
Input: None
Output: Server status and number of available leagues
```

### 2. `get_leagues_api_v1_leagues__get`
List all European leagues
```
Input: None
Output: Array with 5 leagues (Premier League, La Liga, etc.)
```

### 3. `get_teams_api_v1_teams__get`
Search teams with filters
```
Input: search?, league_id?, page?, size?
Output: Paginated list of teams with complete details
```

### 4. `get_team_api_v1_teams__team_id__get`
Get details of a specific team
```
Input: team_id (required)
Output: Complete team details (stadium, coach, etc.)
```

### 5. `get_matches_api_v1_matches__get`
Query matches with advanced filters
```
Input: league_id?, team_id?, matchday?, winner?, page?, size?
Output: Paginated list of matches with results
```

## 📋 Example Questions

After configuration, you can ask questions like:

- "How many teams are in the Premier League?"
- "Show me Manchester City's details"
- "What were Barcelona's latest matches?"
- "What's the current La Liga standings?"
- "Find teams with 'United' in the name"

## 🐛 Troubleshooting

### MCP doesn't appear in IDE
1. Check if configuration file is in the correct location
2. Verify JSON syntax (use online validator)
3. Completely restart the IDE
4. Check if server is running: `curl http://localhost:8000/mcp`

### Connection error
1. Confirm API is running on port 8000
2. Check firewall/antivirus
3. For production, confirm URL and SSL certificate

### Tools don't appear
1. Wait a few seconds after connecting
2. Check server logs for errors
3. Try disconnecting and reconnecting MCP

### Empty responses
1. Check if database `sports_league.sqlite` exists
2. Test endpoints directly: `curl http://localhost:8000/api/v1/health`
3. Check logs for SQL errors

## 📊 Manual Testing

To test if MCP is working:

```bash
# 1. Check server
curl http://localhost:8000/

# 2. Check health check
curl http://localhost:8000/api/v1/health

# 3. Check MCP endpoint
curl http://localhost:8000/mcp

# 4. Test a specific tool
curl "http://localhost:8000/api/v1/teams?search=manchester"
```

## 📱 IDE Usage

After configuration, MCP will appear:
- **Cursor**: In sidebar or chat
- **Claude**: As "Connected Apps" 
- **VS Code**: Through MCP extension

## 🔄 Updates

To update the server:
1. Stop the server (`Ctrl+C`)
2. Do `git pull` (if using repository)
3. Reinstall dependencies if needed: `pip install -r requirements.txt`
4. Restart: `uvicorn app.main:app --reload`

## 🆘 Support

If you have problems:
1. Check server logs
2. Test REST endpoints directly
3. Validate JSON configuration
4. Consult your specific IDE documentation

---

**Note**: This MCP server is read-only and doesn't modify data. All operations are safe for use in any environment. 