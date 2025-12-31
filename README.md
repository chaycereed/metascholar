# metascholar  

Welcome to **metascholar** — a small Python toolkit that generates a **literature snapshot report** from a single command.

`metascholar` helps researchers, students, and PIs quickly understand a topic by automatically fetching papers, extracting key patterns, and producing a clean Markdown report.

---

<video src="https://github.com/user-attachments/assets/248bd614-fab3-4f4d-b9db-7d6b48e3343e"
       width="750"
       autoplay
       loop
       muted>
</video>

---

## What it does

- Fetches **titles, abstracts, years, authors, citations, and venues** using the Semantic Scholar API  
- Builds a **clean text corpus** for lightweight keyword extraction  
- Computes **top keywords** across the literature (TF-IDF based)  
- Generates **time-trend plots** for publication years  
- Produces ranked **recommended first reads** (combined recency × citation score)  
- Identifies **top authors** and **most common journals/venues**  
- Summarizes:  
  - Most cited papers  
  - Most recent papers  
- Outputs **one single Markdown file** (`report.md`) with **embedded base64 images**  
  - No extra folders  
  - No PNGs  
  - Fully portable  

---

## Installation

Install directly from your GitHub repository:

```bash
python3 -m pip install git+https://github.com/chaycereed/metascholar.git
```

After installation:

```bash
metascholar --help
```

---

## Usage

Simply type:

```bash
metascholar
```

You’ll be guided through a small wizard:
```
🔬 Welcome to metascholar – literature search and retrieval tool

[metaScholar] Search query (required, e.g. 'exercise depression'): 
[metaScholar] Number of papers to fetch (default 100) [100]: 
[metaScholar] Output folder name [metascholar_output]: 

[metaScholar] Summary:
[metaScholar]   • Query        : 
[metaScholar]   • # of papers  : 
[metaScholar]   • Output folder: 

[metaScholar] Proceed? [y/n]: 
```


This produces:

```
your_topic/
  report.md
```

The `report.md` includes:

- Top keywords (with embedded plot)  
- Publication year trend (embedded plot)  
- Recommended first reads  
- Top authors  
- Top journals / venues  
- Most cited / most recent papers  

All in **one** human-readable Markdown file.

---

## Example

<details>
<summary>report.md</summary>

# metaScholar Literature Snapshot

**Query:** `sleep neurodegenerative disease`

## Overview

- **Number of papers:** 100
- **Year range:** 2001–2025
- **Citations (median / max):** 20.0 / 983.0

## Top Keywords

| Rank | Term | Score |
|------|------|-------|
| 1 | sleep | 12.3345 |
| 2 | disease | 7.0894 |
| 3 | neurodegenerative | 5.6374 |
| 4 | pd | 4.7811 |
| 5 | ad | 4.3643 |
| 6 | disorder | 4.1193 |
| 7 | disorders | 3.9662 |
| 8 | diseases | 3.9466 |
| 9 | circadian | 3.7010 |
| 10 | rem | 3.3463 |
| 11 | rbd | 3.3190 |
| 12 | behavior | 3.1738 |
| 13 | patients | 3.1519 |
| 14 | brain | 2.7503 |
| 15 | cognitive | 2.7300 |
| 16 | parkinson | 2.6486 |
| 17 | movement | 2.6395 |
| 18 | disturbances | 2.4835 |
| 19 | alzheimer | 2.4129 |
| 20 | review | 2.3648 |

## Top Authors

| Rank | Author | # Papers |
|------|--------|----------|
| 1 | A. Videnovic | 3 |
| 2 | B. Boeve | 3 |
| 3 | S. Naismith | 2 |
| 4 | P. Dušek | 2 |
| 5 | A. Amara | 2 |
| 6 | Rachel K. Rowe | 2 |
| 7 | C. Schenck | 2 |
| 8 | M. Pase | 2 |
| 9 | H. Baumann-Vogel | 2 |
| 10 | E. Werth | 2 |
| 11 | S. Schreiner | 2 |
| 12 | A. Lafontaine | 2 |
| 13 | M. Kaminska | 2 |
| 14 | R. Barker | 2 |
| 15 | Z. Voysey | 2 |

## Top Journals / Venues

| Rank | Journal / Venue | # Papers |
|------|------------------|----------|
| 1 | Frontiers in Neurology | 4 |
| 2 | Journal of Alzheimer's Disease | 4 |
| 3 | PLoS ONE | 4 |
| 4 | Sleep | 4 |
| 5 | Movement Disorders | 4 |
| 6 | Frontiers in Aging Neuroscience | 4 |
| 7 | Nature and Science of Sleep | 3 |
| 8 | Frontiers in Neuroscience | 3 |
| 9 | JAMA Neurology | 2 |
| 10 | Ageing and Neurodegenerative Diseases | 2 |

## Recommended First Reads

- **Sleep and circadian rhythm disruption in psychiatric and neurodegenerative disease** (2010) — citations: 983, score: 0.688
  - https://www.semanticscholar.org/paper/13466cef3c46a4a6d9645995ed68e9252a386840
- **Pathophysiology of REM sleep behaviour disorder and relevance to neurodegenerative disease.** (2007) — citations: 917, score: 0.591
  - https://www.semanticscholar.org/paper/3f1c45db7089ad53c6f3a04ce2d55108791cfe00
- **Role of sleep deprivation in immune-related disease risk and outcomes** (2021) — citations: 336, score: 0.588
  - https://www.semanticscholar.org/paper/ec04a49fce3b310e68890021d9e3695fdbcfcc3f
- **Neurodegenerative disease status and post-mortem pathology in idiopathic rapid-eye-movement sleep behaviour disorder: an observational cohort study** (2013) — citations: 646, score: 0.579
  - https://www.semanticscholar.org/paper/c7158c38c92de8691903e97defaf58decc1bb3bf
- **Quantifying the risk of neurodegenerative disease in idiopathic REM sleep behavior disorder** (2009) — citations: 774, score: 0.560
  - https://www.semanticscholar.org/paper/07e18ceb3fb91c572166943ebf73e82091e737f5
- **Impact of Sleep Disorders and Disturbed Sleep on Brain Health: A Scientific Statement From the American Heart Association** (2024) — citations: 97, score: 0.529
  - https://www.semanticscholar.org/paper/a7fcfc3e47a381fb34f58b5c14300ef5bfbdf2d6
- **Sleep disorders increase the risk of dementia, Alzheimer’s disease, and cognitive decline: a meta-analysis** (2025) — citations: 14, score: 0.507
  - https://www.semanticscholar.org/paper/c7d91310b7162441f00d50558c761ede09ebd41e
- **Sleep disorders cause Parkinson's disease or the reverse is true: Good GABA good night** (2024) — citations: 26, score: 0.492
  - https://www.semanticscholar.org/paper/25fe232bbc15825c3720c730da60aa86b1e9f49c
- **Sleep and Immune System Crosstalk: Implications for Inflammatory Homeostasis and Disease Pathogenesis** (2024) — citations: 18, score: 0.488
  - https://www.semanticscholar.org/paper/6a0713b0bf84c39574ca7216d04e857a9d1ec850
- **Apigenin: a natural molecule at the intersection of sleep and aging** (2024) — citations: 17, score: 0.488
  - https://www.semanticscholar.org/paper/4fcfdf7d5d2c36d587639622c6157e7aa2db54f1

## Most Cited Papers

- **Sleep and circadian rhythm disruption in psychiatric and neurodegenerative disease** (2010) — citations: 983
  - https://www.semanticscholar.org/paper/13466cef3c46a4a6d9645995ed68e9252a386840
- **Pathophysiology of REM sleep behaviour disorder and relevance to neurodegenerative disease.** (2007) — citations: 917
  - https://www.semanticscholar.org/paper/3f1c45db7089ad53c6f3a04ce2d55108791cfe00
- **Quantifying the risk of neurodegenerative disease in idiopathic REM sleep behavior disorder** (2009) — citations: 774
  - https://www.semanticscholar.org/paper/07e18ceb3fb91c572166943ebf73e82091e737f5
- **Neurodegenerative disease status and post-mortem pathology in idiopathic rapid-eye-movement sleep behaviour disorder: an observational cohort study** (2013) — citations: 646
  - https://www.semanticscholar.org/paper/c7158c38c92de8691903e97defaf58decc1bb3bf
- **Association of REM sleep behavior disorder and neurodegenerative disease may reflect an underlying synucleinopathy** (2001) — citations: 565
  - https://www.semanticscholar.org/paper/1602a73ebe522cf18dfeb8ff3d9c60cc290bd1e4
- **Role of sleep deprivation in immune-related disease risk and outcomes** (2021) — citations: 336
  - https://www.semanticscholar.org/paper/ec04a49fce3b310e68890021d9e3695fdbcfcc3f
- **Rapid Eye Movement Sleep Behavior Disorder and Neurodegenerative Disease.** (2015) — citations: 197
  - https://www.semanticscholar.org/paper/8341dd2422cb02a4c0eea9d46cfe4ed1fb991ccb
- **The role of endoplasmic reticulum stress in neurodegenerative disease** (2016) — citations: 194
  - https://www.semanticscholar.org/paper/99aefe68cbbd5d550111ec99e8e1f0990f77a220
- **Sleep disturbance in mental health problems and neurodegenerative disease** (2013) — citations: 161
  - https://www.semanticscholar.org/paper/11e7642d5ed637d06d9cf792f1c73e072f5b7485
- **Prodromal Parkinsonism and Neurodegenerative Risk Stratification in REM Sleep Behavior Disorder** (2017) — citations: 144
  - https://www.semanticscholar.org/paper/ee07485d006b6a612afdab713db22197bebc4e8e

## Most Recent Papers

- **Sleep disorders increase the risk of dementia, Alzheimer’s disease, and cognitive decline: a meta-analysis** (2025) — citations: 14
  - https://www.semanticscholar.org/paper/c7d91310b7162441f00d50558c761ede09ebd41e
- **Acute sleep deprivation in mice generates protein pathology consistent with neurodegenerative diseases** (2024) — citations: 4
  - https://www.semanticscholar.org/paper/a353c8831bbce93e81b2e9255a1ef6dc0b0eaaef
- **Impact of Sleep Disorders and Disturbed Sleep on Brain Health: A Scientific Statement From the American Heart Association** (2024) — citations: 97
  - https://www.semanticscholar.org/paper/a7fcfc3e47a381fb34f58b5c14300ef5bfbdf2d6
- **Sleep, glymphatic system, and Parkinson’s disease** (2024) — citations: 4
  - https://www.semanticscholar.org/paper/1980cfe453718b535b79078d494bc99bf3b07085
- **A Randomized-Controlled Trial Targeting Cognition in Early Alzheimer’s Disease by Improving Sleep with Trazodone (REST)** (2024) — citations: 5
  - https://www.semanticscholar.org/paper/cffb40aa0673be732a5fd03838cbb33cdc12abdd
- **T2 MRI visible perivascular spaces in Parkinson’s disease: clinical significance and association with polysomnography measured sleep** (2024) — citations: 9
  - https://www.semanticscholar.org/paper/2879f65151b1ee91286679d3b682a08c5a81128b
- **Cortical Macro‐ and Microstructural Changes in Parkinson's Disease with Probable Rapid Eye Movement Sleep Behavior Disorder** (2024) — citations: 10
  - https://www.semanticscholar.org/paper/b78a9d46b47c3f5d79305181e770189dfd1aefea
- **The Genetic Landscape of Sleep Disorders in Parkinson’s Disease** (2024) — citations: 14
  - https://www.semanticscholar.org/paper/b476e30de1d265380c409452314246e873bce4bc
- **Sleep and Immune System Crosstalk: Implications for Inflammatory Homeostasis and Disease Pathogenesis** (2024) — citations: 18
  - https://www.semanticscholar.org/paper/6a0713b0bf84c39574ca7216d04e857a9d1ec850
- **Sleep disorders cause Parkinson's disease or the reverse is true: Good GABA good night** (2024) — citations: 26
  - https://www.semanticscholar.org/paper/25fe232bbc15825c3720c730da60aa86b1e9f49c

---
_Generated by metaScholar._
</details>

---

## License

MIT License. See `LICENSE` for details.
