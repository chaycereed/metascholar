from __future__ import annotations

from typing import List, Tuple, Optional

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


def compute_topics(
    corpus: List[str],
    n_topics: int = 5,
    max_features: int = 5000,
    n_top_terms: int = 8,
) -> Tuple[pd.DataFrame, Optional[np.ndarray]]:
    """
    Run a simple NMF-based topic model on the cleaned corpus.

    Returns:
      - topics_df: DataFrame with columns:
          * topic_id
          * top_terms  (string of comma-separated terms)
      - doc_topics: numpy array of length len(corpus),
          containing the dominant topic index for each document
          (or None if topic modeling wasn't possible).
    """
    # Guard: empty or nearly empty corpus
    if not corpus or all((not text or not text.strip()) for text in corpus):
        return pd.DataFrame(columns=["topic_id", "top_terms"]), None

    # Vectorize
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(corpus)

    # Guard: not enough documents/features to meaningfully factorize
    if X.shape[0] < n_topics or X.shape[1] == 0:
        return pd.DataFrame(columns=["topic_id", "top_terms"]), None

    model = NMF(n_components=n_topics, random_state=42)
    W = model.fit_transform(X)        # document-topic matrix
    H = model.components_             # topic-term matrix

    terms = np.array(vectorizer.get_feature_names_out())

    rows = []
    for topic_idx, topic_weights in enumerate(H):
        # Get top terms for this topic
        top_indices = np.argsort(topic_weights)[::-1][:n_top_terms]
        top_terms = terms[top_indices]
        top_terms_str = ", ".join(top_terms)
        rows.append({"topic_id": topic_idx, "top_terms": top_terms_str})

    topics_df = pd.DataFrame(rows)

    # Dominant topic per document
    doc_topics = np.argmax(W, axis=1) if W.size > 0 else None

    return topics_df, doc_topics