import json
import logging
from fastapi import HTTPException

from src.config.config import config
from src.core.generator import Generator
from src.models.invoice import Invoice
from .prompt_builder import build_prompt

logger = logging.getLogger(__name__)


async def extract_document(
    file_content: bytes, content_type: str = "application/octet-stream"
) -> Invoice:
    # 1. Build Prompt (Multimodal - pass file directly)
    messages = build_prompt(file_content, content_type)

    # 2. Call Generator
    generator = Generator(config)
    try:
        response = await generator.generate(messages, temperature=0)
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"LLM Generation failed: {str(e)}")

    # 3. Parse Response
    try:
        data = json.loads(response)
        return Invoice(**data)
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data validation failed: {str(e)}")
