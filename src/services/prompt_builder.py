import base64
import io
import logging
from typing import List, Dict, Any
import fitz
from PIL import Image
from .system_prompt import get_system_prompt, get_user_prompt

logger = logging.getLogger(__name__)

PDF_CONTENT_TYPES = {"application/pdf"}


def _upscale_image_if_needed(file_content: bytes, min_width: int = 2480) -> str:
    """Checks image width and upscales using PIL if below threshold."""
    img = Image.open(io.BytesIO(file_content))
    width, height = img.size

    if width < min_width:
        scale = min_width / width
        # Limit scale to 8.0 to prevent massive memory usage
        scale = min(scale, 8.0)

        new_size = (int(width * scale), int(height * scale))
        # Use Resampling.LANCZOS for high-quality upscaling
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Convert back to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        processed_bytes = buffer.getvalue()
    else:
        processed_bytes = file_content

    b64 = base64.b64encode(processed_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def _process_image_page(page, min_width=2000):
    pix_raw = page.get_pixmap()

    scale = 1.0
    if pix_raw.width < min_width:
        scale = min_width / pix_raw.width

        scale = min(scale, 8.0)

    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat)

    png_bytes = pix.tobytes("png")
    b64 = base64.b64encode(png_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def _convert_to_images(file_content: bytes, filetype: str) -> List[str]:
    data_urls = []

    try:
        doc = fitz.open(stream=file_content, filetype=filetype)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_url = _process_image_page(page, min_width=2480)
            data_urls.append(image_url)
        doc.close()
        logger.info(f"Processed {filetype} into {len(data_urls)} image(s)")
    except Exception as e:
        logger.error(f"Failed to process {filetype} with fitz: {e}")
        raise e

    return data_urls


def build_prompt(file_content: bytes, content_type: str) -> List[Dict[str, Any]]:
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt()

    if content_type == "application/pdf":
        try:
            image_urls = _convert_to_images(file_content, "pdf")
        except Exception as e:
            logger.warning(f"Fitz PDF processing failed: {e}")

    elif content_type.startswith("image/"):
        try:
            # Handle images: check size and upscale if needed
            url = _upscale_image_if_needed(file_content, min_width=2480)
            image_urls = [url]
        except Exception as e:
            logger.error(f"Image upscaling failed: {e}")
            # Fallback to raw content if PIL fails
            b64 = base64.b64encode(file_content).decode("utf-8")
            image_urls = [f"data:{content_type};base64,{b64}"]

    user_content: List[Dict[str, Any]] = [{"type": "text", "text": user_prompt}]
    for url in image_urls:
        user_content.append({"type": "image_url", "image_url": {"url": url}})

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
