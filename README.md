# ⚽ Football API

API REST para consulta de dados das principais ligas europeias de futebol (época 2023-2024).

## 📊 Dados Disponíveis

- **5 Ligas Principais**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- **96 Equipas** com informações completas
- **3150 Jogadores** com dados pessoais e posições
- **1752 Jogos** com resultados e estatísticas
- **Classificações** atualizadas de todas as ligas
- **Estádios**, **Treinadores** e **Árbitros**

## 🚀 Como Executar

### Método 1: Diretamente com Python
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (opcional)
cp .env.example .env

# Executar a API
uvicorn app.main:app --reload

# Acessar em: http://localhost:8000
```

### Método 2: Com Docker (Desenvolvimento)
```bash
# Construir e executar
docker-compose up --build

# Acessar em: http://localhost:8000
```

### Método 3: Deploy em Produção
```bash
# Configurar variáveis para produção
export ENVIRONMENT=production
export ALLOWED_ORIGINS=https://yourdomain.com
export LOG_LEVEL=WARNING
export ENABLE_DOCS=false

# Deploy com docker-compose de produção
docker-compose -f docker-compose.prod.yml up -d

# Monitorizar logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Configuração para Produção

### Variáveis de Ambiente
Copie `.env.example` para `.env` e configure:

```bash
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DATABASE_PATH=sports_league.sqlite
LOG_LEVEL=WARNING
API_VERSION=1.0.0
ENABLE_DOCS=false  # Desabilitar em produção
MAX_PAGE_SIZE=100
DEFAULT_PAGE_SIZE=20
```

### Checklist de Deploy
- [ ] Configurar CORS para domínios específicos
- [ ] Desabilitar documentação em produção (`ENABLE_DOCS=false`)
- [ ] Configurar logging apropriado (`LOG_LEVEL=WARNING`)
- [ ] Configurar SSL/HTTPS
- [ ] Implementar proxy reverso (Nginx)
- [ ] Configurar backup da base de dados
- [ ] Configurar monitorização

## 📚 Documentação da API

- **Swagger UI**: http://localhost:8000/docs (apenas em desenvolvimento)
- **ReDoc**: http://localhost:8000/redoc (apenas em desenvolvimento)
- **Health Check**: http://localhost:8000/api/v1/health

## 🔗 Endpoints Principais

### Ligas
- `GET /api/v1/leagues` - Listar todas as ligas
- `GET /api/v1/leagues/{id}` - Detalhes de uma liga
- `GET /api/v1/leagues/{id}/teams` - Equipas de uma liga
- `GET /api/v1/leagues/{id}/standings` - Classificação da liga

### Equipas
- `GET /api/v1/teams` - Listar equipas (com paginação e pesquisa)
- `GET /api/v1/teams/{id}` - Detalhes de uma equipa
- `GET /api/v1/teams/{id}/players` - Jogadores da equipa
- `GET /api/v1/teams/{id}/matches` - Jogos da equipa
- `GET /api/v1/teams/{id}/statistics` - Estatísticas da equipa

### Jogos
- `GET /api/v1/matches` - Listar jogos (com filtros e paginação)
- `GET /api/v1/matches/{id}` - Detalhes de um jogo
- `GET /api/v1/matches/upcoming` - Próximos jogos

## 🔍 Filtros e Pesquisa

### Paginação
```
?page=1&size=20
```

### Filtros por Liga
```
?league_id=1
```

### Pesquisa por Nome
```
?search=manchester
```

### Filtros de Jogos
```
?team_id=65&winner=HOME_TEAM&matchday=1
```

## 📖 Exemplos de Uso

### Obter todas as ligas
```bash
curl http://localhost:8000/api/v1/leagues
```

### Pesquisar equipas do Manchester
```bash
curl "http://localhost:8000/api/v1/teams?search=manchester"
```

### Classificação da Premier League
```bash
curl http://localhost:8000/api/v1/leagues/1/standings
```

### Jogos do Manchester City
```bash
curl http://localhost:8000/api/v1/teams/65/matches
```

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **SQLite** - Base de dados leve e portável
- **Uvicorn** - Servidor ASGI
- **Docker** - Containerização

## 📁 Estrutura do Projeto

```
api/
├── app/
│   ├── main.py              # Aplicação principal
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── logging_config.py    # Configuração de logging
│   ├── database.py          # Conexão SQLite
│   ├── models.py            # Modelos Pydantic
│   ├── utils.py             # Utilitários (paginação, filtros)
│   └── routers/             # Endpoints organizados
│       ├── leagues.py
│       ├── matches.py
│       └── teams.py
├── requirements.txt         # Dependências Python
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Desenvolvimento
├── docker-compose.prod.yml # Produção
├── .env.example            # Exemplo de configuração
├── README.md               # Este ficheiro
└── sports_league.sqlite    # Base de dados
```

## 🎯 Funcionalidades

✅ **API REST completa** com documentação automática  
✅ **Paginação** para grandes conjuntos de dados  
✅ **Filtros avançados** por liga, equipa, jornada  
✅ **Pesquisa de texto** em nomes de equipas  
✅ **Estatísticas detalhadas** de equipas  
✅ **Relações entre dados** (equipas ↔ jogadores ↔ jogos)  
✅ **CORS configurado** para acesso web  
✅ **Health checks** para monitorização  
✅ **Docker ready** para deployment fácil  
✅ **Logging estruturado** para produção  
✅ **Configurações por ambiente** (dev/prod)  
✅ **Tratamento de erros** robusto  
✅ **Segurança** com usuário não-root  

## 🔒 Segurança

- API é **read-only** (apenas consultas GET)
- **Validação de dados** com Pydantic
- **Tratamento de erros** consistente
- **Limites de paginação** para prevenir sobrecarga
- **CORS restrito** a domínios específicos em produção
- **Logs de auditoria** para todas as requests
- **Contentor com usuário não-root**

## 📊 Monitorização

- **Health check endpoint**: `/api/v1/health`
- **Logs estruturados** em ficheiro e stdout
- **Métricas de performance** nos logs
- **Docker health checks** configurados

## 📊 Dados de Exemplo

A API contém dados reais da época 2023-2024 das cinco principais ligas europeias, incluindo:

- **Premier League**: 20 equipas, ~380 jogos
- **La Liga**: 20 equipas, ~380 jogos  
- **Serie A**: 20 equipas, ~380 jogos
- **Bundesliga**: 18 equipas, ~306 jogos
- **Ligue 1**: 18 equipas, ~306 jogos

## 🤝 Contribuições

Este é um projeto simples para demonstração. Sinta-se à vontade para fazer fork e melhorar!

## 📄 Licença

MIT License - Consulte o ficheiro LICENSE para detalhes.

---

**Fonte dos dados**: [Kaggle - Football Data European Top 5 Leagues](https://www.kaggle.com/datasets/kamrangayibov/football-data-european-top-5-leagues) 