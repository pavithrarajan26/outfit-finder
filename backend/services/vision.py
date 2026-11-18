
import json
import re
from typing import List

from google import genai
from google.genai import types, errors
from pydantic import ValidationError

import config
from schemas import OutfitItem, VisionPayload


class VisionError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


SYSTEM_PROMPT = """
You are an AI clothing recognition assistant.

Analyze the uploaded image and identify each visible clothing item.

Return ONLY valid JSON in this format:
{
  "items": [
    {
      "category": "shirt",
      "color": "white",
      "style": "casual",
      "description": "A white cotton short sleeve shirt",
      "search_query": "white casual cotton short sleeve shirt",
      "confidence": 0.95
    }
  ]
}

Rules:
- Identify individual clothing items, not the person.
- Include shirts, pants, skirts, dresses, jackets, shoes, and accessories.
- Use clear, simple descriptions.
- Do not guess details that cannot be seen.
- Confidence must be between 0 and 1.
- Return an empty items list if no clothing is visible.
"""


def detect_image_type(image_bytes: bytes) -> str:
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"

    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"

    if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return "image/webp"

    raise VisionError(
        "Unsupported image format. Please upload a JPG, PNG, or WebP image.",
        status_code=400,
    )


def parse_items_json(response_text: str) -> List[OutfitItem]:
    cleaned = response_text.strip()

    # Remove JSON markdown fences if the model includes them.
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned)
        payload = VisionPayload.model_validate(data)

        items = payload.items

        for index, item in enumerate(items):
            item.id = str(index + 1)

        return items

    except (json.JSONDecodeError, ValidationError, AttributeError) as error:
        raise VisionError(
            "Gemini returned an unexpected response. Please try another image.",
            status_code=502,
        ) from error


def mock_items() -> List[OutfitItem]:
    sample_data = {
        "items": [
            {
                "category": "shirt",
                "color": "white",
                "style": "casual",
                "description": "A white casual shirt",
                "search_query": "white casual shirt",
                "confidence": 0.95,
            },
            {
                "category": "pants",
                "color": "blue",
                "style": "casual",
                "description": "Blue denim jeans",
                "search_query": "blue denim jeans",
                "confidence": 0.93,
            },
            {
                "category": "shoes",
                "color": "white",
                "style": "casual",
                "description": "White casual sneakers",
                "search_query": "white casual sneakers",
                "confidence": 0.90,
            },
            {
                "category": "jacket",
                "color": "black",
                "style": "casual",
                "description": "A black casual jacket",
                "search_query": "black casual jacket",
                "confidence": 0.88,
            },
        ]
    }

    return parse_items_json(json.dumps(sample_data))


def analyze_with_gemini(
    image_bytes: bytes,
    media_type: str,
) -> List[OutfitItem]:

    if not config.GEMINI_API_KEY:
        raise VisionError(
            "Gemini API key is missing. Check your backend .env file.",
            status_code=500,
        )

    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=media_type,
        )

        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=[
                SYSTEM_PROMPT,
                "Identify all clothing items in this image.",
                image_part,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=1500,
            ),
        )

        if not response.text:
            raise VisionError(
                "Gemini did not return any results. Please try again.",
                status_code=502,
            )

        return parse_items_json(response.text)

    except VisionError:
        raise

    except errors.APIError as error:
        status = getattr(error, "code", None)

        if status == 503:
            raise VisionError(
                "Gemini is temporarily overloaded. Please wait a minute and try uploading again.",
                status_code=503,
            ) from error

        if status == 429:
            raise VisionError(
                "Gemini API request limit reached. Please wait a little and try again.",
                status_code=429,
            ) from error

        if status in (401, 403):
            raise VisionError(
                "Gemini could not authenticate your API key. Check your backend .env file.",
                status_code=500,
            ) from error

        raise VisionError(
            f"Gemini image analysis failed: {error}",
            status_code=502,
        ) from error

    except Exception as error:
        raise VisionError(
            f"Something went wrong while analyzing the image: {error}",
            status_code=502,
        ) from error


def analyze_image(
    image_bytes: bytes,
    media_type: str,
):
    if config.USE_MOCK_VISION:
        return mock_items(), "mock"

    items = analyze_with_gemini(image_bytes, media_type)
    return items, "gemini"
