from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from api.repositories.scenes import list_scene_ids, read_scene_json
from api.schemas import ScenesResponse, MetricsResponse

router = APIRouter(
    prefix="/scenes",
    tags=["scenes"],
)


@router.get("", response_model=ScenesResponse)
def read_scenes() -> ScenesResponse:
    return ScenesResponse(scenes=list_scene_ids())


@router.get("/{scene_id}/metrics", response_model=MetricsResponse)
def read_scene_metrics(scene_id: str) -> MetricsResponse:
    try:
        data = read_scene_json(scene_id, "metrics.json")
        return MetricsResponse.model_validate(data)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Scene metrics not found")

    except (ValidationError, ValueError):
        raise HTTPException(status_code=500, detail="Scene metrics is invalid")
