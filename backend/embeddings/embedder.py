import logging
import os
from typing import List, Optional

from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

TARGET_DIM = int(os.getenv("EMBEDDING_TARGET_DIM", "384"))

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model: Optional[TextEmbedding] = None


def _load_embedding_model() -> TextEmbedding:
    global _model

    if _model is not None:
        return _model

    logger.info(f"Loading FastEmbed model: {MODEL_NAME}")

    _model = TextEmbedding(
        model_name=MODEL_NAME,
        threads=1,
    )

    return _model


def _normalize(vector) -> List[float]:
    values = vector.tolist() if hasattr(vector, "tolist") else list(vector)

    norm = sum(x * x for x in values) ** 0.5

    if norm > 0:
        values = [x / norm for x in values]

    return values


def _fit_to_dimension(
    vector: List[float],
    target_dim: int
) -> List[float]:

    if len(vector) == target_dim:
        return vector

    if len(vector) > target_dim:
        return vector[:target_dim]

    return vector + [0.0] * (target_dim - len(vector))


def generate_embedding(text: str) -> List[float]:

    if not text:
        raise ValueError("Query text is empty or None")

    model = _load_embedding_model()

    embeddings = list(
        model.embed(
            [text],
            batch_size=1,
        )
    )

    if not embeddings:
        raise RuntimeError("FastEmbed returned no embedding")

    embedding = _normalize(embeddings[0])

    return _fit_to_dimension(
        embedding,
        TARGET_DIM
    )