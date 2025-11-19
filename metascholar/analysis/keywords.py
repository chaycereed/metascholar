from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def compute_top_keywords(
    corpus: List[str],
    top_n: int = 20,
    max_features: int = 5000,
) -> pd.DataFrame:
    """
    Compute top keywords across the corpus using TF-IDF.

    Returns a DataFrame with columns:
      - term
      - score  (higher = more important across the corpus)
    """
    if not corpus:
        return pd.DataFrame(columns=["term", "score"])

    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(corpus)

    # Sum TF-IDF scores across all documents
    scores = np.asarray(X.sum(axis=0)).ravel()
    terms = np.array(vectorizer.get_feature_names_out())

    order = np.argsort(scores)[::-1]  # descending
    order = order[:top_n]

    top_terms = terms[order]
    top_scores = scores[order]

    df = pd.DataFrame({"term": top_terms, "score": top_scores})
    return df