import argparse
import os

from .fetch.semantic_scholar import fetch_papers_for_query, SemanticScholarError
from .text.preprocess import build_corpus_from_df
from .analysis.keywords import compute_top_keywords
from .report.build_report import build_report


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="metascholar",
        description="Generate quick literature snapshot reports using Semantic Scholar."
    )

    parser.add_argument(
        "query",
        type=str,
        help="Search query for Semantic Scholar (e.g. 'exercise depression')."
    )

    parser.add_argument(
        "--n-papers",
        type=int,
        default=100,
        help="Number of papers to fetch (default: 100)."
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="metascholar_output",
        help="Output directory for the report (default: metascholar_output)."
    )

    args = parser.parse_args()
    run_pipeline(args.query, args.n_papers, args.outdir)


def run_pipeline(query: str, n_papers: int, outdir: str) -> None:
    print(f"[metaScholar] Running snapshot for query: {query!r}")
    print(f"[metaScholar] Fetching up to {n_papers} papers...")

    try:
        papers_df = fetch_papers_for_query(query, n_papers)
    except SemanticScholarError as e:
        print("\n[metaScholar] Error:")
        print(f"  {e}\n")
        return

    if papers_df is None or len(papers_df) == 0:
        print("[metaScholar] No papers returned. Try adjusting the query.")
        return

    print(f"[metaScholar] Fetched {len(papers_df)} papers.")

    # 1) Build cleaned corpus
    print("[metaScholar] Building cleaned text corpus from titles and abstracts...")
    corpus = build_corpus_from_df(papers_df)
    non_empty_docs = sum(1 for doc in corpus if doc.strip())
    print(f"[metaScholar] Corpus built with {non_empty_docs} non-empty documents.")

    # 2) Compute top keywords
    print("[metaScholar] Computing top keywords...")
    top_keywords = compute_top_keywords(corpus, top_n=20, max_features=5000)
    print(f"[metaScholar] Found {len(top_keywords)} top keywords.")

    # 3) Ensure output directory exists
    os.makedirs(outdir, exist_ok=True)

    # 4) Build report (now with recommended reads / authors / journals)
    report_path = build_report(
        papers=papers_df,
        outdir=outdir,
        top_keywords=top_keywords,
        query=query,
    )

    print(f"[metaScholar] Report saved to: {report_path}")
    print(f"[metaScholar] Output folder: {os.path.abspath(outdir)}")


if __name__ == "__main__":
    main()