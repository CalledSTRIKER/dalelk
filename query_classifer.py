import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from logger import logger
import os

model_path = os.path.join(os.path.dirname(__file__), "models", "fine_tuned_marbert")

try:
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
except Exception as e:
    logger.error(f"Failed to load tokenizer from '{model_path}': {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to load tokenizer: {e}")

try:
    logger.info("Loading classifier model...")
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
except Exception as e:
    logger.error(f"Failed to load classifier model from '{model_path}': {type(e).__name__}: {e}")
    raise RuntimeError(f"Failed to load classifier model: {e}")

labels = model.config.id2label

def analyze_query_intent(query: str):
    try:
        inputs = tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )
        with torch.no_grad():
            outputs = model(**inputs)
        pred_id = torch.argmax(outputs.logits, dim=1).item()
        label = labels[pred_id]
        topic, size = label.split("_")
        return topic, size
    except Exception as e:
        logger.error(f"Failed to classify query '{query}': {type(e).__name__}: {e}")
        raise RuntimeError(f"Failed to classify query: {e}")
