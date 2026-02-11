# Intelligent Document Processing (IDP) API

A high-performance FastAPI service designed to extract structured data from unstructured documents (PDFs, Images) using advanced Multimodal Large Language Models (LLMs). This project interfaces with a VLLM-compatible backend to process invoices and return standardized JSON responses.

## 🚀 Features

- **Multimodal Extraction**: Supports various file formats including PDF, JPG, JPEG, PNG, TIFF, and BMP.
- **Structured Output**: extracts detailed invoice fields (Line Items, Tax Details, Totals) into a validated Pydantic model (`src/models/invoice.py`).
- **High Performance**: Built on FastAPI and `uv` for fast execution and dependency management.
- **LLM Powered**: Leverages `vLLM` for efficient inference (configured for Qwen-VL or similar multimodal models).
- **Dockerized**: Ready-to-deploy container setup with Docker and Docker Compose.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **PDF/Image Processing**: `pymupdf`, `pillow`
- **LLM Integration**: Custom generator interacting with VLLM API.

## 📋 Prerequisites

Before running the project, ensure you have the following:

- **Docker** and **Docker Compose** (for containerized execution)
- **Python 3.11+** (for local development)
- A running instance of **vLLM** (or compatible API) serving a multimodal model.

## ⚙️ Configuration

The application requires the following environment variables. You can set them in a `.env` file or in `docker-compose.yml`.

| Variable              | Description                        |
| --------------------- | ---------------------------------- |
| `VLLM_API_URL`        | Checkpoint URL/IP for the VLLM API |
| `VLLM_GEN_API_PORT`   | Port for the generation API        |
| `VLLM_GEN_MODEL_NAME` | Name of the model to use           |

## 🚀 Getting Started

### Option 1: Using Docker (Recommended)

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd intelligent-document-processing
   ```

2. **Configure Environment**:
   Update `docker-compose.yml` with your VLLM API details or create a `.env` file.

3. **Build and Run**:
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:19011`.

### Option 2: Local Development

This project uses `uv` for fast package management.

1. **Install uv**:

   ```bash
   pip install uv
   # or
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Dependencies**:

   ```bash
   uv sync
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the root directory:

   ```env
   VLLM_API_URL=your_vllm_ip
   VLLM_GEN_API_PORT=9010
   VLLM_GEN_MODEL_NAME=your_model_name
   ```

4. **Run the Server**:
   ```bash
   uv run uvicorn src.api.app:idp_app --reload --port 8000
   ```

## 📡 API Usage

### Extract Invoice Data

**Endpoint**: `POST /api/v1/extract`

**Description**: Upload a document file (PDF, Image) to extract invoice details.

**Curl Example**:

```bash
curl -X 'POST' \
  'http://localhost:19011/api/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/invoice.pdf'
```
