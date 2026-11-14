from fastapi import HTTPException, status


def pending(what: str) -> HTTPException:
    """Respuesta temporal mientras el endpoint no está implementado. El frontend usa mock mientras tanto."""
    return HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=f"Pendiente de implementar: {what}")
