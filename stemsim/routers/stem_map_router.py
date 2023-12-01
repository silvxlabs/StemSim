from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4

from ..core.stem_map import generate_stem_map, StemMap
from ..db import STEM_MAPS


# =============================================================================
# Data Transfer Objects
# =============================================================================
class ListStemMaps(BaseModel):
    stem_maps: list[str]


class GetStem(BaseModel):
    uid: int
    x: float
    y: float
    dbh: float
    cut: bool


class GetStemMap(BaseModel):
    stem_map_id: str | None = None
    stems: list[GetStem]


class CreateStemMap(BaseModel):
    width: int
    height: int
    tph: float
    dbh_mu: float
    dbh_sigma: float


# =============================================================================
# API Endpoints
# =============================================================================
router = APIRouter()


@router.get("/{stem_map_id}")
async def get_stem_map(stem_map_id: str):
    stem_map = stem_map_to_json(STEM_MAPS[stem_map_id])
    return GetStemMap(stem_map_id=stem_map_id, stems=stem_map.stems)


@router.get("")
async def list_stem_maps() -> ListStemMaps:
    return ListStemMaps(stem_maps=list(STEM_MAPS.keys()))


@router.post("")
async def create_stem_map(new_stem_map: CreateStemMap) -> GetStemMap:
    stem_map_id = uuid4().hex
    stem_map = generate_stem_map(
        new_stem_map.width,
        new_stem_map.height,
        new_stem_map.tph,
        new_stem_map.dbh_mu,
        new_stem_map.dbh_sigma,
    )
    STEM_MAPS[stem_map_id] = stem_map
    stem_map = stem_map_to_json(stem_map)
    return GetStemMap(stem_map_id=stem_map_id, stems=stem_map)


# =============================================================================
# Helper Functions
# =============================================================================
def stem_map_to_json(stem_map: StemMap) -> GetStemMap:
    """
    Helper function to convert a StemMap object to a GetStemMap object.

    Parameters
    ----------
    stem_map : StemMap
        The StemMap object to convert.

    Returns
    -------
    GetStemMap
        The converted GetStemMap object.
    """
    return [
        GetStem(
            uid=int(stem[0]),
            x=float(stem[1]),
            y=float(stem[2]),
            dbh=float(stem[3]),
            cut=bool(stem[4]),
        )
        for stem in stem_map._stems
    ]
