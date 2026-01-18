import os

# Yollar
# src/config.py -> trendyol/src/config.py
# BASE_DIR trendyol klasörünü göstermeli
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)

DOCS_DIR = os.path.join(BASE_DIR, "docs")
DB_DIR = os.path.join(BASE_DIR, "database")

# Modeller (Ollama)
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "RefinedNeuro/RN_TR_R2:latest"

# RAG Parametreleri
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 5
COLLECTION_NAME = "medical_kb"
