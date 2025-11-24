import warnings

warnings.filterwarnings(
    "ignore",
    message="urllib3 v2 only supports OpenSSL",
    category=Warning,
)
warnings.filterwarnings(
    "ignore",
    module="urllib3",
)

import argparse
import os
import sys
from textwrap import dedent

from .fetch.semantic_scholar import fetch_papers_for_query, SemanticScholarError
from .text.preprocess import build_corpus_from_df
from .analysis.keywords import compute_top_keywords
from .report.build_report import build_report

# Simple ANSI styles for nicer CLI output
RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
DIM = "\033[2m"

def run_pipeline(query: str, n_papers: int, outdir: str) -> None:
    print()
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Query: {query!r}")
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Fetching up to {n_papers} papers...")
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Output folder: {os.path.abspath(outdir)}")
    print()

    try:
        papers_df = fetch_papers_for_query(query, n_papers)
    except SemanticScholarError as e:
        print(f"\n{BOLD}{MAGENTA}[metaScholar]{RESET} Error while contacting Semantic Scholar:")
        print(f"  {e}\n")
        return
    except Exception as e:
        print(f"\n{BOLD}{MAGENTA}[metaScholar]{RESET} Unexpected error:")
        print(f"  {e}\n")
        return

    if papers_df is None or len(papers_df) == 0:
        print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} No papers returned. Try adjusting the query.")
        return

    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Fetched {len(papers_df)} papers.")

    # 1) Build cleaned corpus
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Building cleaned text corpus from titles and abstracts...")
    corpus = build_corpus_from_df(papers_df)
    non_empty_docs = sum(1 for doc in corpus if doc.strip())
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Corpus built with {non_empty_docs} non-empty documents.")

    # 2) Compute top keywords
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Computing top keywords...")
    top_keywords = compute_top_keywords(corpus, top_n=20, max_features=5000)
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Found {len(top_keywords)} top keywords.")

    # 3) Ensure output directory exists
    os.makedirs(outdir, exist_ok=True)

    # 4) Build report (Markdown-only, with embedded plots)
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Building report...")
    report_path = build_report(
        papers=papers_df,
        outdir=outdir,
        top_keywords=top_keywords,
        query=query,
    )

    print()
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} {GREEN}✔ Done! Report saved to: {os.path.abspath(report_path)}{RESET}")
    print()


def _ask_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            value = int(raw)
            if value <= 0:
                print("  Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid integer.")


def _interactive_wizard() -> None:
    print(f"{BOLD}{CYAN}🔬 Welcome to metascholar – literature search and retrieval tool{RESET}\n")

    # Required: query
    query = ""
    while not query:
        query = input(f"{BOLD}{MAGENTA}[metaScholar]{RESET} {BOLD}Search query{RESET} (required, e.g. 'exercise depression'): ").strip()
        if not query:
            print(f"{BOLD}{MAGENTA}[metaScholar]{RESET}   Query cannot be empty.")

    # Optional: number of papers
    n_papers = _ask_int(f"{BOLD}{MAGENTA}[metaScholar]{RESET} {BOLD}Number of papers to fetch{RESET} (default 100)", default=100)

    # Optional: output directory
    default_outdir = "metascholar_output"
    outdir = input(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Output folder name [{default_outdir}]: ").strip()
    if not outdir:
        outdir = default_outdir

    print()
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} {BOLD}Summary{RESET}:")
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET}   • {BOLD}{CYAN}Query{RESET}        : {query!r}")
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET}   • {BOLD}{CYAN}# of papers{RESET}  : {n_papers}")
    print(f"{BOLD}{MAGENTA}[metaScholar]{RESET}   • {BOLD}{CYAN}Output folder{RESET}: {outdir}")
    print()

    confirm = input(f"{BOLD}{MAGENTA}[metaScholar]{RESET} {BOLD}Proceed?{RESET} [y/n]: ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print(f"\n{BOLD}{MAGENTA}[metaScholar]{RESET} Aborted by user.\n")
        return

    run_pipeline(query=query, n_papers=n_papers, outdir=outdir)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="metascholar",
        description="Generate quick literature snapshot reports using Semantic Scholar.",
        add_help=True,
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Search query for Semantic Scholar (e.g. 'exercise depression'). "
             "If omitted, an interactive prompt will be shown.",
    )

    parser.add_argument(
        "--n-papers",
        type=int,
        default=100,
        help="Number of papers to fetch (default: 100).",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default="metascholar_output",
        help="Output directory for the report (default: metascholar_output).",
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without interactive prompts, even if --query is missing.",
    )

    args = parser.parse_args()

    # If no arguments were given at all (just `metascholar`), drop into wizard.
    if len(sys.argv) == 1:
        _interactive_wizard()
        return

    # If query missing and user didn't force non-interactive → wizard
    if not args.query and not args.non_interactive:
        _interactive_wizard()
        return

    # Non-interactive mode (scriptable)
    if not args.query:
        print(f"{BOLD}{MAGENTA}[metaScholar]{RESET} Error: --query is required in non-interactive mode.")
        sys.exit(1)

    run_pipeline(query=args.query, n_papers=args.n_papers, outdir=args.outdir)


if __name__ == "__main__":
    main()