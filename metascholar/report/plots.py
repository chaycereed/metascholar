from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


_COLOR = "#4C72B0"
_STYLE = {
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.4,
    "font.size": 10,
}


def _save(fig, outdir: str, filename: str) -> str:
    path = os.path.join(outdir, "figures", filename)
    fig.savefig(path, format="png", bbox_inches="tight", dpi=130)
    plt.close(fig)
    return f"figures/{filename}"


def plot_year_trend(papers: pd.DataFrame, outdir: str) -> str | None:
    if "year" not in papers.columns:
        return None
    years = pd.to_numeric(papers["year"], errors="coerce").dropna().astype(int)
    if len(years) == 0:
        return None

    counts = years.value_counts().sort_index()

    with plt.rc_context(_STYLE):
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.bar(counts.index, counts.values, color=_COLOR, width=0.7, zorder=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Papers")
        ax.set_title("Publications per Year", fontweight="bold", pad=10)
        ax.grid(axis="y", zorder=1)
        ax.grid(axis="x", visible=False)
        fig.tight_layout()

    return _save(fig, outdir, "year_trend.png")


def plot_top_keywords(top_keywords: pd.DataFrame, outdir: str) -> str | None:
    if top_keywords is None or len(top_keywords) == 0:
        return None

    df = top_keywords.head(15).iloc[::-1].reset_index(drop=True)

    with plt.rc_context(_STYLE):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.barh(df["term"], df["score"], color=_COLOR, zorder=2)
        ax.set_xlabel("TF-IDF Score")
        ax.set_title("Top Keywords", fontweight="bold", pad=10)
        ax.grid(axis="x", zorder=1)
        ax.grid(axis="y", visible=False)
        fig.tight_layout()

    return _save(fig, outdir, "top_keywords.png")


def plot_citation_distribution(papers: pd.DataFrame, outdir: str) -> str | None:
    if "citationCount" not in papers.columns:
        return None
    cits = pd.to_numeric(papers["citationCount"], errors="coerce").dropna()
    cits = cits[cits >= 0]
    if len(cits) < 5:
        return None

    with plt.rc_context(_STYLE):
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.hist(cits, bins=30, color=_COLOR, edgecolor="white", linewidth=0.4, zorder=2)
        ax.set_xlabel("Citation Count")
        ax.set_ylabel("Papers")
        ax.set_title("Citation Distribution", fontweight="bold", pad=10)
        ax.grid(axis="y", zorder=1)
        ax.grid(axis="x", visible=False)
        fig.tight_layout()

    return _save(fig, outdir, "citation_distribution.png")
