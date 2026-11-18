import pytest
from pydantic import ValidationError

from services.vision import detect_image_type, mock_items, parse_items_json

VALID_REPLY = """{
  "items": [
    {
      "category": "top",
      "color": "black",
      "style": "cropped tee",
      "description": "Black cropped t-shirt.",
      "search_query": "black cropped t-shirt women",
      "confidence": 0.9
    }
  ]
}"""


def test_parse_valid_json_assigns_ids():
    items = parse_items_json(VALID_REPLY)
    assert len(items) == 1
    assert items[0].id == "item-1"
    assert items[0].category == "top"


def test_parse_handles_code_fences():
    items = parse_items_json(f"```json\n{VALID_REPLY}\n```")
    assert len(items) == 1


def test_parse_empty_items_is_ok():
    assert parse_items_json('{"items": []}') == []


def test_parse_rejects_text_without_json():
    with pytest.raises(ValueError):
        parse_items_json("Sorry, I can't help with that.")


def test_parse_rejects_bad_confidence():
    bad = VALID_REPLY.replace("0.9", "5")
    with pytest.raises(ValidationError):
        parse_items_json(bad)


def test_detect_image_types():
    assert detect_image_type(b"\xff\xd8\xff\xe0" + b"0" * 20) == "image/jpeg"
    assert detect_image_type(b"\x89PNG\r\n\x1a\n" + b"0" * 20) == "image/png"
    assert detect_image_type(b"RIFF1234WEBP" + b"0" * 20) == "image/webp"
    assert detect_image_type(b"not an image") is None


def test_mock_items_have_unique_ids():
    ids = [item.id for item in mock_items()]
    assert len(ids) == len(set(ids))