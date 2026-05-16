from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health Check")
def health_check():
    """
    Verifica que la aplicación se encuentre operativa.
    """
    return {
        "status": "UP",
        "application": "Examen final api developer",
        "version": "1.0.0"
    }