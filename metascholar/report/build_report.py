import os
from typing import Optional
import pandas as pd

# ---------- Small numeric helpers ----------

def _safe_year_stats(papers: pd.DataFrame):
    if "year" not in papers.columns:
        return None, None
    years = pd.to_numeric(papers["year"], errors="coerce").dropna()
    if len(years) == 0:
        return None, None
    years = years.astype(int)
    return int(years.min()), int(years.max())


def _safe_citation_stats(papers: pd.DataFrame):
    if "citationCount" not in papers.columns:
        return None, None
    cits = pd.to_numeric(papers["citationCount"], errors="coerce").dropna()
    if len(cits) == 0:
        return None, None
    return float(cits.median()), float(cits.max())


# ---------- Table helpers ----------

def _get_top_cited(papers: pd.DataFrame, n=10):
    if "citationCount" not in papers.columns:
        return pd.DataFrame()
    df = papers.copy()
    df["citationCount"] = pd.to_numeric(df["citationCount"], errors="coerce")
    return (
        df.dropna(subset=["citationCount"])
        .sort_values("citationCount", ascending=False)
        .head(n)
    )


def _get_most_recent(papers: pd.DataFrame, n=10):
    if "year" not in papers.columns:
        return pd.DataFrame()
    df = papers.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return (
        df.dropna(subset=["year"])
        .sort_values("year", ascending=False)
        .head(n)
    )


def _compute_recommended_reads(papers: pd.DataFrame, n=10):
    if "year" not in papers.columns or "citationCount" not in papers.columns:
        return pd.DataFrame()

    df = papers.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["citationCount"] = pd.to_numeric(df["citationCount"], errors="coerce").fillna(0)

    valid = df.dropna(subset=["year"])
    if len(valid) == 0:
        return pd.DataFrame()

    year_min, year_max = valid["year"].min(), valid["year"].max()
    year_range = max(1, year_max - year_min)

    recency = (valid["year"] - year_min) / year_range

    cit_max = max(1, valid["citationCount"].max())
    impact = valid["citationCount"] / cit_max

    valid["meta_score"] = 0.5 * recency + 0.5 * impact

    return valid.sort_values("meta_score", ascending=False).head(n)


def _extract_top_authors(papers: pd.DataFrame, n=15):
    if "authors" not in papers.columns:
        return pd.DataFrame(columns=["author", "count"])

    from collections import Counter
    counts = Counter()

    for entry in papers["authors"].dropna():
        try:
            for a in entry:
                if isinstance(a, dict):
                    name = a.get("name")
                else:
                    name = str(a)
                if name:
                    counts[name] += 1
        except TypeError:
            continue

    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return pd.DataFrame(items, columns=["author", "count"])


def _extract_top_journals(papers: pd.DataFrame, n=10):
    if "venue" not in papers.columns:
        return pd.DataFrame(columns=["venue", "count"])

    venues = papers["venue"].fillna("").astype(str).str.strip()
    venues = venues[venues != ""]
    if len(venues) == 0:
        return pd.DataFrame(columns=["venue", "count"])

    counts = venues.value_counts().head(n)
    return pd.DataFrame({"venue": counts.index, "count": counts.values})


# ---------- Main Report Builder ----------

def build_report(
    papers: pd.DataFrame,
    outdir: str,
    top_keywords: Optional[pd.DataFrame] = None,
    query: Optional[str] = None,
):
    """
    Build a text-only Markdown report (no plots, no ASCII graphics).
    """
    os.makedirs(outdir, exist_ok=True)

    papers = papers.copy()
    if "venue" not in papers.columns:
        papers["venue"] = None
    if "authors" not in papers.columns:
        papers["authors"] = None

    min_year, max_year = _safe_year_stats(papers)
    median_cit, max_cit = _safe_citation_stats(papers)

    top_cited = _get_top_cited(papers)
    most_recent = _get_most_recent(papers)
    recommended = _compute_recommended_reads(papers)
    top_authors = _extract_top_authors(papers)
    top_journals = _extract_top_journals(papers)

    md = []

    md.append("# metaScholar Literature Snapshot\n")

    if query:
        md.append(f"**Query:** `{query}`\n")

    # Overview
    md.append("## Overview\n")
    md.append(f"- **Number of papers:** {len(papers)}")
    if min_year is not None and max_year is not None:
        md.append(f"- **Year range:** {min_year}–{max_year}")
    if median_cit is not None and max_cit is not None:
        md.append(f"- **Citations (median / max):** {median_cit:.1f} / {max_cit:.1f}")
    md.append("")

    # Top Keywords (table only)
    md.append("## Top Keywords\n")
    if top_keywords is not None and len(top_keywords) > 0:
        md.append("| Rank | Term | Score |")
        md.append("|------|------|-------|")
        for i, row in top_keywords.iterrows():
            md.append(f"| {i+1} | {row['term']} | {row['score']:.4f} |")
        md.append("")
    else:
        md.append("_No keyword statistics available._\n")

    # Authors
    md.append("## Top Authors\n")
    if len(top_authors):
        md.append("| Rank | Author | # Papers |")
        md.append("|------|--------|----------|")
        for i, row in top_authors.iterrows():
            md.append(f"| {i+1} | {row['author']} | {row['count']} |")
        md.append("")
    else:
        md.append("_Author information not available._\n")

    # Journals
    md.append("## Top Journals / Venues\n")
    if len(top_journals):
        md.append("| Rank | Journal / Venue | # Papers |")
        md.append("|------|------------------|----------|")
        for i, row in top_journals.iterrows():
            md.append(f"| {i+1} | {row['venue']} | {row['count']} |")
        md.append("")
    else:
        md.append("_Journal / venue information not available._\n")
    
    # Recommended reads
    md.append("## Recommended First Reads\n")
    if len(recommended):
        for _, row in recommended.iterrows():
            title = row.get("title", "")
            year = row.get("year", "NA")
            cits = row.get("citationCount", "NA")
            score = row.get("meta_score", 0)
            url = row.get("url", "")
            md.append(f"- **{title}** ({year}) — citations: {cits}, score: {score:.3f}")
            if isinstance(url, str) and url.strip():
                md.append(f"  - {url}")
        md.append("")
    else:
        md.append("_Not enough data to compute recommended reads._\n")

    # Most Cited
    md.append("## Most Cited Papers\n")
    if len(top_cited):
        for _, row in top_cited.iterrows():
            title = row.get("title", "")
            year = row.get("year", "NA")
            cits = row.get("citationCount", "NA")
            url = row.get("url", "")
            md.append(f"- **{title}** ({year}) — citations: {cits}")
            if isinstance(url, str) and url.strip():
                md.append(f"  - {url}")
        md.append("")
    else:
        md.append("_Citation data not available._\n")

    # Most Recent
    md.append("## Most Recent Papers\n")
    if len(most_recent):
        for _, row in most_recent.iterrows():
            title = row.get("title", "")
            year = row.get("year", "NA")
            cits = row.get("citationCount", "NA")
            url = row.get("url", "")
            md.append(f"- **{title}** ({year}) — citations: {cits}")
            if isinstance(url, str) and url.strip():
                md.append(f"  - {url}")
        md.append("")
    else:
        md.append("_Year information not available._\n")

    md.append("---")
    md.append("_Generated by metaScholar._\n")

    # Write file
    path = os.path.join(outdir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    return path