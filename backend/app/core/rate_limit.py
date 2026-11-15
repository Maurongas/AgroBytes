"""Límite de peticiones por IP, en memoria (ventana deslizante de 60 s). Dueño: Backend.

Protege la cuota de NASA POWER y SoilGrids: cada POST /analyses puede disparar consultas a los dos.
Es por proceso: con varios workers el límite real es N × el configurado (suficiente para el MVP).
"""

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from app.core.config import settings

WINDOW_S = 60.0
_hits: dict[str, deque[float]] = defaultdict(deque)


def reset() -> None:
    _hits.clear()


def limit_analyses(request: Request) -> None:
    """Dependencia de FastAPI: 429 si la IP pasó RATE_LIMIT_ANALYSES_PER_MIN en el último minuto (0 = sin límite)."""
    max_hits = settings.RATE_LIMIT_ANALYSES_PER_MIN
    if max_hits <= 0:
        return
    ip = request.client.host if request.client else "desconocida"
    now = time.monotonic()
    hits = _hits[ip]
    while hits and now - hits[0] >= WINDOW_S:
        hits.popleft()
    if len(hits) >= max_hits:
        retry = max(1, round(WINDOW_S - (now - hits[0])))
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                            detail=f"Demasiados análisis seguidos. Intenta de nuevo en {retry} s.",
                            headers={"Retry-After": str(retry)})
    hits.append(now)
    if len(_hits) > 10_000:  # no crecer sin límite con muchas IPs distintas
        for key in [k for k, v in _hits.items() if not v or now - v[-1] >= WINDOW_S]:
            del _hits[key]
