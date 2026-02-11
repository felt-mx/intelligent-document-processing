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
        logger.error(f"Generation failed: {type(e).__name__}: {repr(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"LLM Generation failed: {type(e).__name__}: {str(e)}",
        )

    # 3. Parse Response
    try:
        # generator returns a message dict like {"role": "assistant", "content": "..."}
        # extract the content string before parsing as JSON
        if isinstance(response, dict):
            content = response.get("content", "")
        else:
            content = response
        data = json.loads(content)
        return Invoice(**data)
    except Exception as e:
        logger.error(f"Validation failed: {type(e).__name__}: {repr(e)}")
        logger.error(f"Raw LLM response: {response}")
        raise HTTPException(
            status_code=500,
            detail=f"Data validation failed: {type(e).__name__}: {str(e)}",
        )
