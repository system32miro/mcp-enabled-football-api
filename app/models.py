from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class League(BaseModel):
    league_id: int
    name: str
    country: str
    country_id: Optional[int] = None
    icon_url: Optional[str] = None
    cl_spot: Optional[int] = None
    uel_spot: Optional[int] = None
    relegation_spot: Optional[int] = None

class Team(BaseModel):
    team_id: int
    name: str
    founded_year: Optional[float] = None
    stadium_id: Optional[int] = None
    league_id: Optional[int] = None
    coach_id: Optional[int] = None
    cresturl: Optional[str] = None

class Player(BaseModel):
    player_id: int
    team_id: Optional[int] = None
    name: str
    position: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None

class Match(BaseModel):
    match_id: int
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    matchday: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    winner: Optional[str] = None
    utc_date: Optional[date] = None

class Score(BaseModel):
    score_id: int
    match_id: Optional[int] = None
    full_time_home: Optional[int] = None
    full_time_away: Optional[int] = None
    half_time_home: Optional[int] = None
    half_time_away: Optional[int] = None

class Standing(BaseModel):
    standing_id: int
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    position: Optional[int] = None
    team_id: Optional[int] = None
    played_games: Optional[int] = None
    won: Optional[int] = None
    draw: Optional[int] = None
    lost: Optional[int] = None
    points: Optional[int] = None
    goals_for: Optional[int] = None
    goals_against: Optional[int] = None
    goal_difference: Optional[int] = None
    form: Optional[str] = None

class Coach(BaseModel):
    coach_id: int
    name: Optional[str] = None
    team_id: Optional[int] = None
    nationality: Optional[str] = None

class Referee(BaseModel):
    referee_id: int
    name: Optional[str] = None
    nationality: Optional[str] = None

class Stadium(BaseModel):
    stadium_id: int
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[float] = None

class Season(BaseModel):
    season_id: int
    league_id: Optional[int] = None
    year: Optional[str] = None

# Modelos para respostas com paginação
class PaginatedResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    size: int
    total_pages: int 