from fastapi import APIRouter

from api.repositories.scenes import list_scene_ids
from api.schemas import ScenesResponse


router = APIRouter(
    prefix="/scenes",
    tags=["scenes"],
)


@router.get("", response_model=ScenesResponse)
def read_scenes() -> ScenesResponse:
    return ScenesResponse(scenes=list_scene_ids())