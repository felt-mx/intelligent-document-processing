import httpx
from src.config.config import Config


class Generator:
    def __init__(self, config: Config):
        self.config = config

    async def generate(self, messages, tools=None, tool_choice=None, temperature=0.7):
        payload = {
            "model": self.config.vllm_gen_model_name,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools

        if tool_choice:
            payload["tool_choice"] = tool_choice

        async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
            response = await client.post(
                f"{self.config.vllm_gen_url}/v1/chat/completions",
                json=payload,
            )

            if response.status_code != 200:
                error_body = await response.aread()
                raise Exception(f"VLLM API error: {error_body.decode()}")

            response_json = response.json()

            if isinstance(response_json, dict):
                if "message" in response_json:
                    return response_json["message"]
                elif "choices" in response_json and len(response_json["choices"]) > 0:
                    choice = response_json["choices"][0]
                    if (
                        isinstance(choice, dict)
                        and "message" in choice
                        and isinstance(choice["message"], dict)
                    ):
                        return choice["message"]
                    if "text" in choice:
                        return choice.get("text", "")

            return response.text
