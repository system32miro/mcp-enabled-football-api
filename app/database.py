import sqlite3
from typing import Dict, List, Any
import os

DATABASE_PATH = "sports_league.sqlite"

def get_db_connection():
    """Cria uma conexão à base de dados SQLite"""
    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(f"Base de dados não encontrada: {DATABASE_PATH}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    return conn

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Executa uma query e retorna os resultados como lista de dicionários"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def execute_single_query(query: str, params: tuple = ()) -> Dict[str, Any] | None:
    """Executa uma query e retorna um único resultado"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None 