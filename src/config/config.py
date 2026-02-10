from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    def __init__(self):
        self.vllm_api_url = os.getenv("VLLM_API_URL")
        self.vllm_gen_api_port = os.getenv("VLLM_GEN_API_PORT")
        self.vllm_gen_model_name = os.getenv("VLLM_GEN_MODEL_NAME")

    @property
    def vllm_gen_url(self):
        if self.vllm_api_url and self.vllm_gen_api_port:
            return f"http://{self.vllm_api_url}:{self.vllm_gen_api_port}"
        return self.vllm_api_url  # Fallback or None


config = Config()
