# metascholar

A command-line tool that fetches academic papers and generates a literature snapshot report in a single command.

<video src="https://github.com/user-attachments/assets/248bd614-fab3-4f4d-b9db-7d6b48e3343e"
       width="750"
       autoplay
       loop
       muted>
</video>

## Features

- Fetches titles, abstracts, years, authors, citation counts, and venues using the Semantic Scholar API
- Computes top keywords across the literature using TF-IDF
- Ranks recommended first reads by combined recency and citation score
- Identifies top authors and most common journals and venues
- Summarizes most cited and most recent papers
- Generates publication-year trend, top-keyword, and citation-distribution plots saved as PNGs
- Outputs a single `report.md` with inline image links alongside a `figures/` folder

## Installation

Requires Python 3.9 or higher. Install directly from GitHub:

```bash
pip install git+https://github.com/chaycereed/metascholar.git
```

## Usage

### Generate a report

Running `metascholar` with no arguments launches an interactive prompt asking for a search query, number of papers, and output folder name. Confirm the summary to proceed.

```bash
metascholar
```

To skip the prompt and run non-interactively:

```bash
metascholar --query "sleep neurodegenerative disease" --n-papers 100 --outdir sleep_review
```

This produces:

```
sleep_review/
  report.md
  figures/
    year_trend.png
    citation_distribution.png
```

The report includes:

- Overview (paper count, year range, citation statistics)
- Publications-per-year bar chart and citation distribution histogram, side by side
- Recommended first reads with abstracts
- Most cited papers
- Most recent papers
- Top journals and venues table

## Example

See [test/report.md](test/report.md) for a full sample output.

## License

MIT License. See `LICENSE` for details.
