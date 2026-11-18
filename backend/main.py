
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import config
from schemas import AnalyzeResponse, ShoppingResponse
from services.vision import VisionError, analyze_image, detect_image_type
from services.shopping import ShoppingError, search_products

app = FastAPI(title="Outfit Finder API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "vision_mode": "mock" if config.USE_MOCK_VISION else "gemini",
        "shopping_mode": "serpapi" if config.SERPAPI_KEY else "unconfigured",
    }


@app.post("/outfits/analyze", response_model=AnalyzeResponse)
def analyze_outfit(file: UploadFile = File(...)):
    image_bytes = file.file.read(config.MAX_IMAGE_BYTES + 1)

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(image_bytes) > config.MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Image is too large. Please upload one under 5 MB.",
        )

    media_type = detect_image_type(image_bytes)

    if media_type is None:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Please upload a JPEG, PNG or WebP image.",
        )

    try:
        items, source = analyze_image(image_bytes, media_type)
    except VisionError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
        )

    return AnalyzeResponse(items=items, source=source)


@app.get("/shopping/search", response_model=ShoppingResponse)
def shopping_search(
    q: str = Query(..., min_length=2, max_length=200),
    limit: int = Query(10, ge=1, le=20),
):
    try:
        return search_products(q, limit)
    except ShoppingError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )
