import numpy as np
from load_embeddings import (
    embedder,
    courses_index,
    certs_index,
    qa_idmap,
)
from data_loader import (
    course_facts_list,
    cert_facts_list,
    questions_and_answers,
)
from logger import logger

def smart_retrieve(query: str, topic: str, size: str):
    if topic == "course":
        index = courses_index
        data_list = course_facts_list
    elif topic == "certification":
        index = certs_index
        data_list = cert_facts_list
    else:
        index = qa_idmap
        data_list = questions_and_answers

    if size == "large":
        top_k = 60
    else:
        top_k = 15

    try:
        query_embedding = embedder.encode([query]).astype("float32")
        D, I = index.search(query_embedding, top_k)
        retrieved_facts = [data_list[i] for i in I[0] if i < len(data_list)]
        return retrieved_facts, topic
    except Exception as e:
        logger.error(f"Retrieval error (topic={topic}, size={size}): {type(e).__name__}: {e}")
        return [], topic
