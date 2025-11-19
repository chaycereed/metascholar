from __future__ import annotations

from typing import List, Iterable
import re

import pandas as pd


# A small, hand-rolled English stopword list.
# We can expand this later, but this is good enough to start.
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else",
    "of", "in", "on", "at", "to", "for", "from", "by", "with",
    "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those",
    "it", "its", "as", "such",
    "we", "you", "they", "he", "she", "i",
    "our", "their", "his", "her",
    "can", "could", "may", "might", "should", "would",
    "have", "has", "had", "do", "does", "did",
    "not", "no", "yes",
    "using", "used", "use",
    "results", "conclusion", "conclusions",
    "study", "studies", "paper", "article",
}


def simple_clean(text: str) -> str:
    """
    Very basic text cleaning:
    - lowercasing
    - removing non-alphanumeric characters
    - collapsing whitespace
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    # keep letters, numbers, whitespace
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(tokens: Iterable[str]) -> List[str]:
    """
    Remove common stopwords from a list of tokens.
    """
    return [t for t in tokens if t and t not in _STOPWORDS]


def clean_and_tokenize(text: str) -> List[str]:
    """
    Clean a text string and split into non-stopword tokens.
    """
    cleaned = simple_clean(text)
    tokens = cleaned.split()
    return remove_stopwords(tokens)


def build_corpus_from_df(
    papers: pd.DataFrame,
    title_col: str = "title",
    abstract_col: str = "abstract",
    join_char: str = " ",
) -> List[str]:
    """
    Build a cleaned text corpus from a DataFrame of papers.

    For each row:
      1. Combine title + abstract into one string
      2. Clean and tokenize
      3. Join tokens back into a cleaned string

    Returns a list of cleaned documents (one per paper),
    and also adds a 'clean_text' column to the DataFrame in-place.
    """
    corpus: List[str] = []

    titles = papers.get(title_col, pd.Series([""] * len(papers)))
    abstracts = papers.get(abstract_col, pd.Series([""] * len(papers)))

    clean_texts: List[str] = []

    for t, a in zip(titles.fillna(""), abstracts.fillna("")):
        combined = f"{t}. {a}".strip()
        tokens = clean_and_tokenize(combined)
        clean_doc = join_char.join(tokens)
        clean_texts.append(clean_doc)
        corpus.append(clean_doc)

    papers["clean_text"] = clean_texts
    return corpus