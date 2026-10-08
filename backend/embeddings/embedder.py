import logging
import os
from typing import List, Optional

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

TARGET_DIM = int(os.getenv("EMBEDDING_TARGET_DIM", "384"))

DEFAULT_CANDIDATES = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

MODEL_CANDIDATES = [
    item.strip()
    for item in os.getenv(
        "EMBEDDING_MODEL_CANDIDATES",
        DEFAULT_CANDIDATES
    ).split(",")
    if item.strip()
]

_model: Optional[SentenceTransformer] = None


def _load_embedding_model() -> SentenceTransformer:
    global _model

    if _model is not None:
        return _model

    errors = []

    for model_name in MODEL_CANDIDATES:
        try:
            logger.info(f"Loading embedding model: {model_name}")

            _model = SentenceTransformer(
                model_name,
                device="cpu"
            )

            return _model

        except Exception as exc:
            errors.append(f"{model_name}: {exc}")
            logger.warning(
                f"Embedding model load failed ({model_name}): {exc}"
            )

    raise RuntimeError(
        "No embedding model could be loaded. "
        + " | ".join(errors)
    )


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

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        batch_size=1,
        show_progress_bar=False
    )

    payload = (
        embedding.tolist()
        if hasattr(embedding, "tolist")
        else list(embedding)
    )

    return _fit_to_dimension(payload, TARGET_DIM)