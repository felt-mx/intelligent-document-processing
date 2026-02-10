import base64
from typing import List, Dict, Any
from services.system_prompt import get_system_prompt, get_user_prompt


def build_prompt(file_content: bytes, content_type: str) -> List[Dict[str, Any]]:
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt()

    base64_content = base64.b64encode(file_content).decode("utf-8")
    data_url = f"data:{content_type};base64,{base64_content}"

    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        },
    ]
