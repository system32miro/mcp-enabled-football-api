# ⚽ Football API + MCP Server

REST API for querying data from the main European football leagues (2023-2024 season) with **MCP (Model Context Protocol) integration** for AI agents.

## 🤖 MCP Functionality

This API includes an **integrated MCP server** that allows AI agents (like Claude, Cursor, etc.) to directly access football data through intelligent semantic tools.

### ✨ MCP Capabilities
- 🔍 **Intelligent search** for teams, players and matches
- 📊 **Automated statistics** queries
- 🏆 **Real-time standings** analysis
- 🎯 **Automatic filters** by league, team, matchday
- 📈 **Complex data** aggregation
- 🤝 **Native integration** with IDEs and AI agents

### 🔗 MCP Endpoint
- **MCP URL**: `http://localhost:8000/mcp`
- **Protocol**: Server-Sent Events (SSE)
- **Tools**: 6 automatic tools generated from API endpoints

## 📊 Available Data

- **5 Main Leagues**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- **96 Teams** with complete information
- **3150 Players** with personal data and positions
- **1752 Matches** with results and statistics
- **Updated standings** for all leagues
- **Stadiums**, **Coaches** and **Referees**

## 🚀 How to Run

### Method 1: Directly with Python
```bash
# Install dependencies (includes fastapi-mcp)
pip install -r requirements.txt

# Configure environment variables (optional)
cp .env.example .env

# Run API with integrated MCP
uvicorn app.main:app --reload

# Access API at: http://localhost:8000
# Access MCP at: http://localhost:8000/mcp
```

### Method 2: With Docker (Development)
```bash
# Build and run
docker-compose up --build

# Access API at: http://localhost:8000
# Access MCP at: http://localhost:8000/mcp
```

### Method 3: Production Deploy
```bash
# Configure variables for production
export ENVIRONMENT=production
export ALLOWED_ORIGINS=https://yourdomain.com
export LOG_LEVEL=WARNING
export ENABLE_DOCS=false

# Deploy with production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🤖 MCP Configuration for IDEs

### Cursor / Windsurf
Add to `~/.cursor/mcp.json` or `~/.windsurf/mcp.json`:

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
Add to Claude configuration file:

```json
{
  "mcpServers": {
    "football-api-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Other MCP Clients
For clients that don't support SSE directly, use `mcp-remote`:

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

## 🛠️ Available MCP Tools

### 1. `health_check`
Check API status and database connectivity

### 2. `get_leagues_api_v1_leagues__get`
Get all available European leagues

### 3. `get_teams_api_v1_teams__get`
Search teams with filters and pagination
- Parameters: `search`, `league_id`, `page`, `size`

### 4. `get_team_api_v1_teams__team_id__get`
Get complete details of a specific team

### 5. `get_matches_api_v1_matches__get`
Query matches with advanced filters
- Parameters: `league_id`, `team_id`, `matchday`, `winner`, `page`, `size`

Each tool includes **complete documentation** and **JSON schemas** to facilitate AI agent understanding.

## 🔧 Production Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_PATH=sports_league.sqlite
LOG_LEVEL=WARNING
API_VERSION=1.0.0
ENABLE_DOCS=false  # Disable in production
MAX_PAGE_SIZE=100
DEFAULT_PAGE_SIZE=20
```

### Deploy Checklist
- [ ] Configure CORS for specific domains
- [ ] Disable documentation in production (`ENABLE_DOCS=false`)
- [ ] Configure appropriate logging (`LOG_LEVEL=WARNING`)
- [ ] Configure SSL/HTTPS
- [ ] Implement reverse proxy (Nginx)
- [ ] Configure database backup
- [ ] Configure monitoring
- [ ] **Test MCP connectivity** in production

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs (development only)
- **ReDoc**: http://localhost:8000/redoc (development only)
- **Health Check**: http://localhost:8000/api/v1/health
- **MCP Server**: http://localhost:8000/mcp

## 🔗 Main Endpoints

### Leagues
- `GET /api/v1/leagues` - List all leagues
- `GET /api/v1/leagues/{id}` - League details
- `GET /api/v1/leagues/{id}/teams` - Teams in a league
- `GET /api/v1/leagues/{id}/standings` - League standings

### Teams
- `GET /api/v1/teams` - List teams (with pagination and search)
- `GET /api/v1/teams/{id}` - Team details
- `GET /api/v1/teams/{id}/players` - Team players
- `GET /api/v1/teams/{id}/matches` - Team matches
- `GET /api/v1/teams/{id}/statistics` - Team statistics

### Matches
- `GET /api/v1/matches` - List matches (with filters and pagination)
- `GET /api/v1/matches/{id}` - Match details
- `GET /api/v1/matches/upcoming` - Upcoming matches

## 🔍 Filters and Search

### Pagination
```
?page=1&size=20
```

### Filter by League
```
?league_id=1
```

### Search by Name
```
?search=manchester
```

### Match Filters
```
?team_id=65&winner=HOME_TEAM&matchday=1
```

## 📖 Usage Examples

### Traditional REST API

```bash
# Get all leagues
curl http://localhost:8000/api/v1/leagues

# Search Manchester teams
curl "http://localhost:8000/api/v1/teams?search=manchester"

# Premier League standings
curl http://localhost:8000/api/v1/leagues/1/standings

# Manchester City matches
curl http://localhost:8000/api/v1/teams/65/matches
```

### Through MCP Agent (Cursor/Claude)

```
"How many teams are in the Premier League?"
"Show me Manchester City's details"
"What's the current La Liga standings?"
"How many goals did Barcelona score this season?"
```

The agent will automatically use MCP tools to answer the questions!

## 🛠️ Technologies

- **FastAPI** - Modern and fast web framework
- **FastAPI-MCP** - Native MCP integration
- **Pydantic** - Data validation
- **SQLite** - Lightweight and portable database
- **Uvicorn** - ASGI server
- **Docker** - Containerization
- **MCP Protocol** - Model Context Protocol for AI agents

## 📁 Project Structure

```
api/
├── app/
│   ├── main.py              # Main application + MCP Server
│   ├── config.py            # Configuration and environment variables
│   ├── logging_config.py    # Logging configuration
│   ├── database.py          # SQLite connection
│   ├── models.py            # Pydantic models
│   ├── utils.py             # Utilities (pagination, filters)
│   └── routers/             # Organized endpoints
│       ├── leagues.py
│       ├── matches.py
│       └── teams.py
├── requirements.txt         # Python dependencies (includes fastapi-mcp)
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Development
├── docker-compose.prod.yml # Production
├── .env.example            # Configuration example
├── README.md               # This file
└── sports_league.sqlite    # Database
```

## 🎯 Features

✅ **Complete REST API** with automatic documentation  
✅ **Integrated MCP server** for AI agents  
✅ **6 MCP tools** automatically generated  
✅ **Complete MCP documentation** with JSON schemas  
✅ **SSE support** for real-time connectivity  
✅ **Pagination** for large datasets  
✅ **Advanced filters** by league, team, matchday  
✅ **Text search** in team names  
✅ **Detailed statistics** for teams  
✅ **Data relationships** (teams ↔ players ↔ matches)  
✅ **Configured CORS** for web access  
✅ **Health checks** for monitoring  
✅ **Docker ready** for easy deployment  
✅ **Structured logging** for production  
✅ **Environment configurations** (dev/prod)  
✅ **Robust error handling**  
✅ **Security** with non-root user  

## 🔒 Security

- API is **read-only** (GET queries only)
- **MCP Server exposed** locally by default
- **Data validation** with Pydantic
- **Consistent error handling**
- **Pagination limits** to prevent overload
- **Restricted CORS** to specific domains in production
- **Audit logs** for all requests
- **Container with non-root user**

## 📊 Monitoring

- **Health check endpoint**: `/api/v1/health`
- **MCP connectivity check** through health check
- **Structured logs** in file and stdout
- **Performance metrics** in logs
- **Configured Docker health checks**
- **MCP usage tracking** in logs

## 🤖 MCP Use Cases

### For Developers
- Quick data search during development
- Statistics analysis without leaving the IDE
- Ad-hoc queries through Cursor chat

### For Sports Analysts
- Automated comparative analyses
- Data-driven report generation
- Pattern identification through AI

### For Journalists
- Quick fact verification
- Statistics gathering for articles
- Contextual queries about teams and players

## 📊 Sample Data

The API contains real data from the 2023-2024 season of the five main European leagues, including:

- **Premier League**: 20 teams, ~380 matches
- **La Liga**: 20 teams, ~380 matches  
- **Serie A**: 20 teams, ~380 matches
- **Bundesliga**: 18 teams, ~306 matches
- **Ligue 1**: 18 teams, ~306 matches

## 🚀 Next Steps

- [ ] Add more MCP tools (advanced statistics)
- [ ] Implement cache for better performance
- [ ] Add historical data from previous seasons
- [ ] Create optional web dashboard
- [ ] Implement webhooks for real-time updates

## 🤝 Contributions

This project demonstrates the perfect integration between FastAPI and MCP. Feel free to fork and improve!

## 📄 License

MIT License - See LICENSE file for details.

---

**Data Source**: [Kaggle - Football Data European Top 5 Leagues](https://www.kaggle.com/datasets/kamrangayibov/football-data-european-top-5-leagues)  
**Powered by**: [FastAPI](https://fastapi.tiangolo.com/) + [FastAPI-MCP](https://fastapi-mcp.tadata.com/) 