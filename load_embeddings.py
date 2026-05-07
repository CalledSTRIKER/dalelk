import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
from logger import logger

load_dotenv()
EMBEDDING_MODEL_NAME = "google/embeddinggemma-300m"

try:
    logger.info("Loading embedding model...")
    embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception as e:
    logger.error(f"Failed to load embedding model '{EMBEDDING_MODEL_NAME}': {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to load embedding model: {e}")

try:
    logger.info("Reading Course index...")
    courses_index = faiss.read_index("indicies/courses_index.index")
except Exception as e:
    logger.error(f"Failed to read course index: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to read course index: {e}")

try:
    logger.info("Reading Certification index...")
    certs_index = faiss.read_index("indicies/certs_index.index")
except Exception as e:
    logger.error(f"Failed to read certification index: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to read certification index: {e}")

try:
    logger.info("Reading Q&A index...")
    qa_idmap = faiss.read_index("indicies/qa_idmap.index")
    qa_index = faiss.read_index("indicies/qa_index.index")
except Exception as e:
    logger.error(f"Failed to read Q&A index: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to read Q&A index: {e}")

logger.info("FAISS indexes ready.")