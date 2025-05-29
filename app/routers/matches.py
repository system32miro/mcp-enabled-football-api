from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from app.models import Match, PaginatedResponse
from app.database import execute_query, execute_single_query
from app.utils import paginate_query, build_where_clause

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/")
async def get_matches(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Itens por página"),
    league_id: Optional[int] = Query(None, description="Filtrar por liga"),
    team_id: Optional[int] = Query(None, description="Filtrar por equipa"),
    matchday: Optional[int] = Query(None, description="Filtrar por jornada"),
    winner: Optional[str] = Query(None, description="Filtrar por vencedor (HOME_TEAM, AWAY_TEAM, DRAW)")
):
    """Obter jogos com filtros e paginação"""
    
    # Construir filtros
    filters = {}
    if league_id:
        filters["m.league_id"] = league_id
    if matchday:
        filters["m.matchday"] = matchday
    if winner:
        filters["m.winner"] = winner
    
    # Query base com joins para obter nomes das equipas
    base_query = """
        SELECT 
            m.*,
            ht.name as home_team_name,
            at.name as away_team_name,
            s.full_time_home,
            s.full_time_away,
            s.half_time_home,
            s.half_time_away
        FROM matches m
        LEFT JOIN teams ht ON m.home_team_id = ht.team_id
        LEFT JOIN teams at ON m.away_team_id = at.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
    """
    
    # Adicionar filtros WHERE
    where_clause, params = build_where_clause(filters)
    
    # Filtro especial para team_id (equipa pode ser casa ou fora)
    if team_id:
        if where_clause:
            where_clause += " AND "
        where_clause += "(m.home_team_id = ? OR m.away_team_id = ?)"
        params = params + (team_id, team_id)
    
    if where_clause:
        base_query += f" WHERE {where_clause}"
    
    base_query += " ORDER BY m.utc_date DESC, m.match_id"
    
    return paginate_query(base_query, params, page, size)

@router.get("/{match_id}")
async def get_match(match_id: int):
    """Obter detalhes de um jogo específico"""
    query = """
        SELECT 
            m.*,
            ht.name as home_team_name,
            ht.cresturl as home_team_crest,
            at.name as away_team_name,
            at.cresturl as away_team_crest,
            l.name as league_name,
            l.country as league_country,
            s.full_time_home,
            s.full_time_away,
            s.half_time_home,
            s.half_time_away
        FROM matches m
        LEFT JOIN teams ht ON m.home_team_id = ht.team_id
        LEFT JOIN teams at ON m.away_team_id = at.team_id
        LEFT JOIN leagues l ON m.league_id = l.league_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        WHERE m.match_id = ?
    """
    
    match = execute_single_query(query, (match_id,))
    
    if not match:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return match

@router.get("/upcoming/")
async def get_upcoming_matches(
    days: int = Query(7, ge=1, le=30, description="Próximos X dias"),
    league_id: Optional[int] = Query(None, description="Filtrar por liga")
):
    """Obter próximos jogos (simulação - todos os jogos são de 2023-2024)"""
    
    # Como todos os dados são históricos, vamos retornar os últimos jogos
    # ordenados por data como se fossem próximos
    base_query = """
        SELECT 
            m.*,
            ht.name as home_team_name,
            at.name as away_team_name,
            l.name as league_name
        FROM matches m
        LEFT JOIN teams ht ON m.home_team_id = ht.team_id
        LEFT JOIN teams at ON m.away_team_id = at.team_id
        LEFT JOIN leagues l ON m.league_id = l.league_id
    """
    
    filters = {}
    if league_id:
        filters["m.league_id"] = league_id
    
    where_clause, params = build_where_clause(filters)
    if where_clause:
        base_query += f" WHERE {where_clause}"
    
    base_query += " ORDER BY m.utc_date DESC LIMIT ?"
    params = params + (days * 3,)  # Multiplicar por 3 para ter mais jogos
    
    matches = execute_query(base_query, params)
    return matches 