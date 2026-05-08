import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from data_loader import (
    course_texts,
    cert_texts,
    questions,
    ids,
)
from dotenv import load_dotenv
from logger import logger
import os

load_dotenv()

REPO_DIR     = os.path.dirname(os.path.abspath(__file__))

EMBEDDING_MODEL_NAME = "google/embeddinggemma-300m"
os.makedirs("indicies", exist_ok=True)


try:
    logger.info("Loading embedding model...")
    embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception as e:
    logger.error(f"Failed to load embedding model '{EMBEDDING_MODEL_NAME}': {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to load embedding model: {e}")

try:
    logger.info("Encoding Course documents...")
    course_embeddings = embedder.encode(course_texts, show_progress_bar=True).astype("float32")
    courses_index = faiss.IndexFlatL2(course_embeddings.shape[1])
    courses_index.add(course_embeddings)
    faiss.write_index(courses_index, f"{REPO_DIR}/indicies/courses_index.index")
except Exception as e:
    logger.error(f"Failed to encode/index/write course documents: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to encode/index/write course documents: {e}")

try:
    logger.info("Encoding Certification documents...")
    cert_embeddings = embedder.encode(cert_texts, show_progress_bar=True).astype("float32")
    certs_index = faiss.IndexFlatL2(cert_embeddings.shape[1])
    certs_index.add(cert_embeddings)
    faiss.write_index(certs_index, f"{REPO_DIR}/indicies/certs_index.index")
except Exception as e:
    logger.error(f"Failed to encode/index/write certification documents: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to encode/index/write certification documents: {e}")

try:
    logger.info("Encoding Q&A documents...")
    qa_embeddings = embedder.encode(questions, show_progress_bar=True).astype("float32")
    qa_index = faiss.IndexFlatL2(qa_embeddings.shape[1])
    qa_idmap = faiss.IndexIDMap2(qa_index)
    qa_idmap.add_with_ids(qa_embeddings, ids)
    faiss.write_index(qa_index, f"{REPO_DIR}/indicies/qa_index.index")
    faiss.write_index(qa_idmap, f"{REPO_DIR}/indicies/qa_idmap.index")
except Exception as e:
    logger.error(f"Failed to encode/index/write Q&A documents: {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to encode/index/write Q&A documents: {e}")

logger.info("FAISS indexes ready.")