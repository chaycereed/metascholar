# metascholar  

Welcome to **metascholar** — a small Python toolkit that generates a **literature snapshot report** from a single command.

`metascholar` helps researchers, students, and PIs quickly understand a topic by automatically fetching papers, extracting key patterns, and producing a clean Markdown report.

--

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

### **1. Run interactively (recommended)**

Simply type:

```bash
metascholar
```

You’ll be guided through a small wizard:

- Query (e.g., “exercise depression”)  
- Number of papers to fetch  
- Output folder name  
- Confirmation before running  

This produces:

```
your_topic/
  report.md
```

The report includes:

- Top keywords (with embedded plot)  
- Publication year trend (embedded plot)  
- Recommended first reads  
- Top authors  
- Top journals / venues  
- Most cited / most recent papers  

All in **one** human-readable Markdown file.

---

### **2. Non-interactive mode**

You can also run directly from the command line:

```bash
metascholar --query "exercise depression" --n-papers 150 --outdir reports/exercise_depression
```

This is ideal for scripts, cron jobs, or automated workflows.

---

### **3. Run via Python module**

```bash
python3 -m metascholar.cli "exercise depression"
```

---

## Example Output

A typical `report.md` includes:

- Clean sections  
- Tables for top keywords, authors, venues  
- Embedded figures (keyword plot, time trend)  
- A focused list of “first reads” with links  
- A compact snapshot view of the field

Works in:

- VS Code  
- GitHub  
- Notion  
- Obsidian  
- Markdown previews  

---

## License

MIT License. See `LICENSE` for details.
