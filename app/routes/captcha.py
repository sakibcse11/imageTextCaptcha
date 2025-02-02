from fastapi import APIRouter, HTTPException

from app.config import get_pass_key
from app.models import ImageRequest, ImageResponse
from app.services.nopecha_service import solve_image

router = APIRouter()

@router.post("/solve", response_model=ImageResponse)
async def solve_captcha(image_request: ImageRequest):
    if not image_request.key==get_pass_key():
        raise HTTPException(status_code=404, detail="Invalid key.")
    try:
        # Pass the base64 image string to the NopeCHA service
        solution = solve_image(image_request.base64_image)
        return ImageResponse(solution=solution)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
