from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import Team, PaginatedResponse
from app.database import execute_query, execute_single_query
from app.utils import paginate_query, build_where_clause

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/")
async def get_teams(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Itens por página"),
    league_id: Optional[int] = Query(None, description="Filtrar por liga"),
    search: Optional[str] = Query(None, description="Pesquisar por nome da equipa")
):
    """Obter equipas com filtros, pesquisa e paginação"""
    
    base_query = """
        SELECT 
            t.*,
            l.name as league_name,
            l.country as league_country,
            s.name as stadium_name,
            s.capacity as stadium_capacity,
            c.name as coach_name,
            c.nationality as coach_nationality
        FROM teams t
        LEFT JOIN leagues l ON t.league_id = l.league_id
        LEFT JOIN stadiums s ON t.stadium_id = s.stadium_id
        LEFT JOIN coaches c ON t.coach_id = c.coach_id
    """
    
    conditions = []
    params = []
    
    # Filtro por liga
    if league_id:
        conditions.append("t.league_id = ?")
        params.append(league_id)
    
    # Pesquisa por nome
    if search:
        conditions.append("t.name LIKE ?")
        params.append(f"%{search}%")
    
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    base_query += " ORDER BY t.name"
    
    return paginate_query(base_query, tuple(params), page, size)

@router.get("/{team_id}")
async def get_team(team_id: int):
    """Obter detalhes de uma equipa específica"""
    query = """
        SELECT 
            t.*,
            l.name as league_name,
            l.country as league_country,
            s.name as stadium_name,
            s.location as stadium_location,
            s.capacity as stadium_capacity,
            c.name as coach_name,
            c.nationality as coach_nationality
        FROM teams t
        LEFT JOIN leagues l ON t.league_id = l.league_id
        LEFT JOIN stadiums s ON t.stadium_id = s.stadium_id
        LEFT JOIN coaches c ON t.coach_id = c.coach_id
        WHERE t.team_id = ?
    """
    
    team = execute_single_query(query, (team_id,))
    
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    
    return team

@router.get("/{team_id}/players")
async def get_team_players(
    team_id: int,
    position: Optional[str] = Query(None, description="Filtrar por posição")
):
    """Obter jogadores de uma equipa"""
    
    # Verificar se a equipa existe
    team = execute_single_query("SELECT * FROM teams WHERE team_id = ?", (team_id,))
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    
    query = "SELECT * FROM players WHERE team_id = ?"
    params = [team_id]
    
    if position:
        query += " AND position = ?"
        params.append(position)
    
    query += " ORDER BY name"
    
    players = execute_query(query, tuple(params))
    return {
        "team": team,
        "players": players,
        "total_players": len(players)
    }

@router.get("/{team_id}/matches")
async def get_team_matches(
    team_id: int,
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Itens por página"),
    home_only: Optional[bool] = Query(None, description="Apenas jogos em casa"),
    away_only: Optional[bool] = Query(None, description="Apenas jogos fora")
):
    """Obter jogos de uma equipa"""
    
    # Verificar se a equipa existe
    team = execute_single_query("SELECT * FROM teams WHERE team_id = ?", (team_id,))
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    
    base_query = """
        SELECT 
            m.*,
            ht.name as home_team_name,
            at.name as away_team_name,
            s.full_time_home,
            s.full_time_away,
            l.name as league_name
        FROM matches m
        LEFT JOIN teams ht ON m.home_team_id = ht.team_id
        LEFT JOIN teams at ON m.away_team_id = at.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        LEFT JOIN leagues l ON m.league_id = l.league_id
        WHERE 
    """
    
    if home_only:
        base_query += "m.home_team_id = ?"
        params = (team_id,)
    elif away_only:
        base_query += "m.away_team_id = ?"
        params = (team_id,)
    else:
        base_query += "(m.home_team_id = ? OR m.away_team_id = ?)"
        params = (team_id, team_id)
    
    base_query += " ORDER BY m.utc_date DESC"
    
    return paginate_query(base_query, params, page, size)

@router.get("/{team_id}/statistics")
async def get_team_statistics(team_id: int):
    """Obter estatísticas de uma equipa"""
    
    # Verificar se a equipa existe
    team = execute_single_query("SELECT * FROM teams WHERE team_id = ?", (team_id,))
    if not team:
        raise HTTPException(status_code=404, detail="Equipa não encontrada")
    
    # Estatísticas dos jogos
    stats_query = """
        SELECT 
            COUNT(*) as total_matches,
            SUM(CASE WHEN winner = 'HOME_TEAM' AND home_team_id = ? THEN 1
                     WHEN winner = 'AWAY_TEAM' AND away_team_id = ? THEN 1
                     ELSE 0 END) as wins,
            SUM(CASE WHEN winner = 'DRAW' THEN 1 ELSE 0 END) as draws,
            SUM(CASE WHEN winner = 'HOME_TEAM' AND away_team_id = ? THEN 1
                     WHEN winner = 'AWAY_TEAM' AND home_team_id = ? THEN 1
                     ELSE 0 END) as losses
        FROM matches 
        WHERE home_team_id = ? OR away_team_id = ?
    """
    
    stats = execute_single_query(stats_query, (team_id, team_id, team_id, team_id, team_id, team_id))
    
    # Estatísticas de golos
    goals_query = """
        SELECT 
            SUM(CASE WHEN m.home_team_id = ? THEN s.full_time_home ELSE s.full_time_away END) as goals_for,
            SUM(CASE WHEN m.home_team_id = ? THEN s.full_time_away ELSE s.full_time_home END) as goals_against
        FROM matches m
        JOIN scores s ON m.match_id = s.match_id
        WHERE m.home_team_id = ? OR m.away_team_id = ?
    """
    
    goals = execute_single_query(goals_query, (team_id, team_id, team_id, team_id))
    
    # Posição na tabela
    position_query = """
        SELECT position, points, played_games
        FROM standings 
        WHERE team_id = ?
    """
    
    position = execute_single_query(position_query, (team_id,))
    
    return {
        "team": team,
        "statistics": {
            **stats,
            **goals,
            "goal_difference": (goals.get("goals_for", 0) or 0) - (goals.get("goals_against", 0) or 0),
            "current_position": position.get("position") if position else None,
            "points": position.get("points") if position else None
        }
    } 