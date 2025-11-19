import os
from typing import Optional
from collections import Counter
from datetime import date
import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd


# ---------- Small numeric helpers ----------

def _safe_year_stats(papers: pd.DataFrame) -> tuple[Optional[int], Optional[int]]:
    if "year" not in papers.columns:
        return None, None
    years = pd.to_numeric(papers["year"], errors="coerce").dropna()
    if len(years) == 0:
        return None, None
    years = years.astype(int)
    return int(years.min()), int(years.max())


def _safe_citation_stats(papers: pd.DataFrame) -> tuple[Optional[float], Optional[float]]:
    if "citationCount" not in papers.columns:
        return None, None
    cits = pd.to_numeric(papers["citationCount"], errors="coerce").dropna()
    if len(cits) == 0:
        return None, None
    return float(cits.median()), float(cits.max())


# ---------- Figure → Base64 helper ----------

def _fig_to_base64(fig) -> str:
    """Convert a Matplotlib figure to a base64-encoded PNG string."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return encoded


# ---------- Plot builders (return base64 strings, not files) ----------

def _make_keyword_image_b64(top_keywords: pd.DataFrame) -> Optional[str]:
    if top_keywords is None or len(top_keywords) == 0:
        return None

    df = top_keywords.copy()
    df = df.sort_values("score", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(df["term"], df["score"])
    ax.set_xlabel("TF-IDF score")
    ax.set_title("Top keywords")
    plt.tight_layout()

    img64 = _fig_to_base64(fig)
    plt.close(fig)
    return img64


def _make_papers_per_year_image_b64(papers: pd.DataFrame) -> Optional[str]:
    if "year" not in papers.columns:
        return None

    years = pd.to_numeric(papers["year"], errors="coerce").dropna()
    if len(years) == 0:
        return None

    years = years.astype(int)
    counts = years.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index, counts.values)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of papers")
    ax.set_title("Papers per year")
    plt.tight_layout()

    img64 = _fig_to_base64(fig)
    plt.close(fig)
    return img64


# ---------- Table helpers ----------

def _get_top_cited(papers: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "citationCount" not in papers.columns:
        return pd.DataFrame()
    df = papers.copy()
    df["citationCount"] = pd.to_numeric(df["citationCount"], errors="coerce")
    return (
        df.dropna(subset=["citationCount"])
        .sort_values("citationCount", ascending=False)
        .head(n)
    )


def _get_most_recent(papers: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if "year" not in papers.columns:
        return pd.DataFrame()
    df = papers.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return (
        df.dropna(subset=["year"])
        .sort_values("year", ascending=False)
        .head(n)
    )


def _compute_recommended_reads(papers: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Combine recency + citations into a single 'meta_score' and pick the top n.
    """
    if "year" not in papers.columns or "citationCount" not in papers.columns:
        return pd.DataFrame()

    df = papers.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["citationCount"] = pd.to_numeric(df["citationCount"], errors="coerce").fillna(0)

    valid = df.dropna(subset=["year"])
    if len(valid) == 0:
        return pd.DataFrame()

    year_min = valid["year"].min()
    year_max = valid["year"].max()
    year_range = year_max - year_min

    if year_range > 0:
        recency = (valid["year"] - year_min) / year_range
    else:
        recency = pd.Series(1.0, index=valid.index)

    cit_max = valid["citationCount"].max()
    if cit_max > 0:
        impact = valid["citationCount"] / cit_max
    else:
        impact = pd.Series(0.0, index=valid.index)

    meta_score = 0.5 * recency + 0.5 * impact
    valid["meta_score"] = meta_score

    return valid.sort_values("meta_score", ascending=False).head(n)


def _extract_top_authors(papers: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """
    Count how often each author appears across all papers.
    Assumes 'authors' column holds list-like of dicts with 'name'.
    """
    if "authors" not in papers.columns:
        return pd.DataFrame(columns=["author", "count"])

    counts = Counter()

    for entry in papers["authors"].dropna():
        try:
            for a in entry:
                name = None
                if isinstance(a, dict):
                    name = a.get("name")
                else:
                    name = str(a)
                if name:
                    counts[name] += 1
        except TypeError:
            continue

    if not counts:
        return pd.DataFrame(columns=["author", "count"])

    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return pd.DataFrame(items, columns=["author", "count"])


def _extract_top_journals(papers: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Count how often each venue/journal appears.
    Guaranteed to return columns: ['venue', 'count'].
    """
    if "venue" not in papers.columns:
        return pd.DataFrame(columns=["venue", "count"])

    venues = (
        papers["venue"]
        .fillna("")
        .astype(str)
        .str.strip()
    )
    venues = venues[venues != ""]
    if len(venues) == 0:
        return pd.DataFrame(columns=["venue", "count"])

    counts = venues.value_counts().head(n)

    return pd.DataFrame({
        "venue": counts.index,
        "count": counts.values,
    })


# ---------- Main report builder (Markdown-only, single file) ----------

def build_report(
    papers: pd.DataFrame,
    outdir: str,
    top_keywords: Optional[pd.DataFrame] = None,
    query: Optional[str] = None,
) -> str:
    """
    Build a 'literature snapshot' report as a single Markdown file.

    Outputs:
      - report.md  (only file written to disk)
        - includes embedded base64 PNGs for plots
        - includes all tables (recommended reads, authors, journals, etc.)
    """
    os.makedirs(outdir, exist_ok=True)

    # Ensure expected columns exist so we never KeyError
    papers = papers.copy()
    if "venue" not in papers.columns:
        papers["venue"] = None
    if "authors" not in papers.columns:
        papers["authors"] = None

    # Stats
    min_year, max_year = _safe_year_stats(papers)
    median_cit, max_cit = _safe_citation_stats(papers)

    # Plots as base64
    keyword_img_b64 = None
    if top_keywords is not None and len(top_keywords) > 0:
        keyword_img_b64 = _make_keyword_image_b64(top_keywords)

    papers_per_year_img_b64 = _make_papers_per_year_image_b64(papers)

    # Derived tables
    top_cited = _get_top_cited(papers, n=10)
    most_recent = _get_most_recent(papers, n=10)
    recommended = _compute_recommended_reads(papers, n=10)
    top_authors = _extract_top_authors(papers, n=15)
    top_journals = _extract_top_journals(papers, n=10)

    # Build Markdown
    md_lines: list[str] = []

    title = "metaScholar Literature Snapshot"
    md_lines.append(f"# {title}\n")

    if query:
        md_lines.append(f"**Query:** `{query}`\n")

    # Overview
    md_lines.append("## Overview\n")
    md_lines.append(f"- **Number of papers:** {len(papers)}")
    if min_year is not None and max_year is not None:
        md_lines.append(f"- **Year range:** {min_year}–{max_year}")
    if median_cit is not None and max_cit is not None:
        md_lines.append(f"- **Citations (median / max):** {median_cit:.1f} / {max_cit:.1f}")
    md_lines.append("")  # blank line

    # Top Keywords
    md_lines.append("## Top Keywords\n")
    if top_keywords is not None and len(top_keywords) > 0:
        md_lines.append("The most prominent terms across titles and abstracts (by TF-IDF score):\n")
        md_lines.append("| Rank | Term | Score |")
        md_lines.append("|------|------|-------|")
        for i, row in top_keywords.iterrows():
            md_lines.append(f"| {i+1} | {row['term']} | {row['score']:.4f} |")
        md_lines.append("")
        if keyword_img_b64 is not None:
            md_lines.append(
                f'<img src="data:image/png;base64,{keyword_img_b64}" alt="Top keywords" />\n'
            )
    else:
        md_lines.append("_No keyword statistics available._\n")

    # Time Trend
    md_lines.append("## Time Trend\n")
    if papers_per_year_img_b64 is not None:
        md_lines.append("Distribution of papers over publication years in this query:\n")
        md_lines.append(
            f'<img src="data:image/png;base64,{papers_per_year_img_b64}" alt="Papers per year" />\n'
        )
    else:
        md_lines.append("_No year information available to plot._\n")

    # Recommended First Reads
    md_lines.append("## Recommended First Reads\n")
    if len(recommended) > 0:
        md_lines.append("Papers ranked by a combined score of recency and citation impact:\n")
        for _, row in recommended.iterrows():
            title_ = str(row.get("title", "")).strip()
            year_ = row.get("year", "NA")
            cits_ = row.get("citationCount", "NA")
            score_ = row.get("meta_score", "NA")
            url_ = row.get("url", "")
            md_lines.append(
                f"- **{title_}** ({year_}) — citations: {cits_}, score: {score_:.3f}"
            )
            if isinstance(url_, str) and url_.strip():
                md_lines.append(f"  - {url_}")
        md_lines.append("")
    else:
        md_lines.append("_Not enough data to compute recommended reads._\n")

    # Top Authors
    md_lines.append("## Top Authors\n")
    if len(top_authors) > 0:
        md_lines.append("Authors appearing most frequently across this query:\n")
        md_lines.append("| Rank | Author | # Papers |")
        md_lines.append("|------|--------|----------|")
        for i, row in top_authors.iterrows():
            md_lines.append(f"| {i+1} | {row['author']} | {row['count']} |")
        md_lines.append("")
    else:
        md_lines.append("_Author information not available or not parseable._\n")

    # Top Journals / Venues
    md_lines.append("## Top Journals / Venues\n")
    if len(top_journals) > 0:
        md_lines.append("Most common journals or venues in this query:\n")
        md_lines.append("| Rank | Journal / Venue | # Papers |")
        md_lines.append("|------|------------------|----------|")
        for i, row in top_journals.iterrows():
            venue = row.get("venue", "Unknown")
            count = row.get("count", 0)
            md_lines.append(f"| {i+1} | {venue} | {count} |")
        md_lines.append("")
    else:
        md_lines.append("_Journal / venue information not available._\n")

    # Most Cited
    md_lines.append("## Most Cited Papers\n")
    if len(top_cited) > 0:
        for _, row in top_cited.iterrows():
            title_ = str(row.get("title", "")).strip()
            year_ = row.get("year", "NA")
            cits_ = row.get("citationCount", "NA")
            url_ = row.get("url", "")
            md_lines.append(f"- **{title_}** ({year_}) — citations: {cits_}")
            if isinstance(url_, str) and url_.strip():
                md_lines.append(f"  - {url_}")
        md_lines.append("")
    else:
        md_lines.append("_Citation data not available._\n")

    # Most Recent
    md_lines.append("## Most Recent Papers\n")
    if len(most_recent) > 0:
        for _, row in most_recent.iterrows():
            title_ = str(row.get("title", "")).strip()
            year_ = row.get("year", "NA")
            cits_ = row.get("citationCount", "NA")
            url_ = row.get("url", "")
            md_lines.append(f"- **{title_}** ({year_}) — citations: {cits_}")
            if isinstance(url_, str) and url_.strip():
                md_lines.append(f"  - {url_}")
        md_lines.append("")
    else:
        md_lines.append("_Year information not available._\n")

    md_lines.append("---")
    md_lines.append("_Generated by metaScholar._\n")

    # Write Markdown file (only output)
    md_path = os.path.join(outdir, "report.md")
    md_text = "\n".join(md_lines)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    return md_path