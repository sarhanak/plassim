from fastapi import APIRouter

router = APIRouter(prefix="/presets", tags=["presets"])

_PRESETS: dict[str, dict] = {}


@router.get("/{client_id}")
def get_presets(client_id: str) -> dict:
    return {"client_id": client_id, "presets": _PRESETS.get(client_id, {})}


@router.post("")
def upsert_preset(body: dict) -> dict:
    client_id = body.get("client_id", "default")
    preset = body.get("preset", {})
    _PRESETS.setdefault(client_id, {}).update(preset)
    return {"status": "ok", "preset_id": list(preset.keys())[-1] if preset else None}

