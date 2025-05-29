from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import League, PaginatedResponse
from app.database import execute_query, execute_single_query
from app.utils import paginate_query

router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.get("/", response_model=List[League])
async def get_leagues():
    """Obter todas as ligas"""
    query = "SELECT * FROM leagues ORDER BY name"
    leagues = execute_query(query)
    return leagues

@router.get("/{league_id}", response_model=League)
async def get_league(league_id: int):
    """Obter uma liga específica pelo ID"""
    query = "SELECT * FROM leagues WHERE league_id = ?"
    league = execute_single_query(query, (league_id,))
    
    if not league:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    
    return league

@router.get("/{league_id}/teams")
async def get_league_teams(league_id: int):
    """Obter todas as equipas de uma liga"""
    # Verificar se a liga existe
    league = execute_single_query("SELECT * FROM leagues WHERE league_id = ?", (league_id,))
    if not league:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    
    query = """
        SELECT t.*, s.name as stadium_name, c.name as coach_name
        FROM teams t
        LEFT JOIN stadiums s ON t.stadium_id = s.stadium_id
        LEFT JOIN coaches c ON t.coach_id = c.coach_id
        WHERE t.league_id = ?
        ORDER BY t.name
    """
    teams = execute_query(query, (league_id,))
    return teams

@router.get("/{league_id}/standings")
async def get_league_standings(league_id: int):
    """Obter a classificação de uma liga"""
    # Verificar se a liga existe
    league = execute_single_query("SELECT * FROM leagues WHERE league_id = ?", (league_id,))
    if not league:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    
    query = """
        SELECT 
            s.*,
            t.name as team_name,
            t.cresturl as team_crest
        FROM standings s
        JOIN teams t ON s.team_id = t.team_id
        WHERE s.league_id = ?
        ORDER BY s.position
    """
    standings = execute_query(query, (league_id,))
    return {
        "league": league,
        "standings": standings
    } 