from __future__ import annotations

import requests
import pandas as pd
from typing import Optional


BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

TIMEOUT = 10
MAX_RETRIES = 3


class SemanticScholarError(Exception):
    """Custom error class for clearer user-friendly messages."""
    pass


def fetch_papers_for_query(query: str, n_papers: int = 100) -> pd.DataFrame:
    """
    Fetch papers from Semantic Scholar with friendly error messages.
    """

    params = {
        "query": query,
        "limit": n_papers,
        # NOTE: added 'venue' for journal / conference name
        "fields": "title,abstract,year,citationCount,authors,url,venue"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(BASE_URL, params=params, timeout=TIMEOUT)

            if resp.status_code == 429:
                raise SemanticScholarError(
                    "Semantic Scholar is currently rate-limiting requests.\n"
                    "Try again in 30–60 seconds, or reduce --n-papers."
                )

            if resp.status_code >= 500:
                raise SemanticScholarError(
                    "Semantic Scholar's servers are currently unavailable (5xx error).\n"
                    "They may be busy or temporarily offline. Please try again later."
                )

            if resp.status_code != 200:
                raise SemanticScholarError(
                    f"Semantic Scholar returned an unexpected status code: {resp.status_code}.\n"
                    "Double-check your query or try again later."
                )

            try:
                data = resp.json()
            except Exception:
                raise SemanticScholarError(
                    "Semantic Scholar returned a response but it could not be parsed.\n"
                    "This may happen during high server load. Try again in a moment."
                )

            papers = data.get("data")
            if papers is None:
                raise SemanticScholarError(
                    "Semantic Scholar returned an unexpected response format.\n"
                    "Try again later or modify your query."
                )

            if len(papers) == 0:
                raise SemanticScholarError(
                    f"No papers found for query: {query!r}.\n"
                    "Try a broader or simpler search term."
                )

            df = pd.json_normalize(papers)

            # Ensure 'venue' always exists
            if "venue" not in df.columns:
                df["venue"] = None

            return df

        except requests.exceptions.Timeout:
            if attempt == MAX_RETRIES:
                raise SemanticScholarError(
                    "The request to Semantic Scholar timed out.\n"
                    "Their servers may be overloaded. Try again shortly."
                )

        except requests.exceptions.ConnectionError:
            if attempt == MAX_RETRIES:
                raise SemanticScholarError(
                    "Could not connect to Semantic Scholar.\n"
                    "Check your internet connection or try again later."
                )

    raise SemanticScholarError(
        "Repeated attempts to reach Semantic Scholar failed.\n"
        "Their service might be experiencing issues. Try again later."
    )