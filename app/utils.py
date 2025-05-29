import math
from typing import Dict, List, Any
from app.database import execute_query

def paginate_query(base_query: str, params: tuple = (), page: int = 1, size: int = 20) -> Dict[str, Any]:
    """Aplica paginação a uma query"""
    # Limitar o tamanho da página
    size = min(size, 100)  # Máximo 100 items por página
    offset = (page - 1) * size
    
    # Query para contar total de registos
    count_query = f"SELECT COUNT(*) as total FROM ({base_query})"
    total_result = execute_query(count_query, params)
    total = total_result[0]['total'] if total_result else 0
    
    # Query com paginação
    paginated_query = f"{base_query} LIMIT {size} OFFSET {offset}"
    data = execute_query(paginated_query, params)
    
    return {
        "data": data,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": math.ceil(total / size) if total > 0 else 0
    }

def build_where_clause(filters: Dict[str, Any]) -> tuple:
    """Constrói uma cláusula WHERE com base nos filtros fornecidos"""
    conditions = []
    params = []
    
    for key, value in filters.items():
        if value is not None:
            conditions.append(f"{key} = ?")
            params.append(value)
    
    where_clause = " AND ".join(conditions) if conditions else ""
    return where_clause, tuple(params)

def search_query(table: str, search_fields: List[str], search_term: str) -> str:
    """Constrói uma query de pesquisa de texto"""
    if not search_term:
        return ""
    
    search_conditions = []
    for field in search_fields:
        search_conditions.append(f"{field} LIKE '%{search_term}%'")
    
    return f"({' OR '.join(search_conditions)})" 