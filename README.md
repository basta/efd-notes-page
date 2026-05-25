# Course Lecture Notes

LLM-assisted study guides for university courses, grounded in slide PDFs and exam-style questions. Output is an MkDocs Material site.

## Pipeline

For each course:

1. **Slides → text**: Convert lecture PDFs to markdown with `docling`.
2. **Route**: For each exam question, ask a cheap LLM which lecture(s) cover it.
3. **Generate**: For each question, prompt the LLM with the routed lecture text + the previous N answers (continuity), get back a textbook-quality answer.
4. **Self-test**: Spawn one subagent per question to append a comprehension check + answer key (currently driven manually from a Claude Code session — see Subagents below).
5. **Build site**: Split chunks into per-question pages, group by lecture in MkDocs nav, serve via MkDocs Material.

## Current courses

- **MPV** (Computer Vision Methods) — full question-driven, slide-grounded pipeline. See below.
- **EFD** (Estimation, Filtering, and Detection) — legacy single-source pipeline (`generate_study_guide.py` over `page/docs/index.md`).
- **DRS** — legacy question-driven pipeline without slide grounding (`generate_from_questions.py`).

## MPV: regenerating / updating

Files specific to MPV:

| Path | Purpose |
|---|---|
| `mpv_q.txt` | Exam questions, one per line |
| `mpv_lectures.json` | Lecture manifest (file id, title, topics) — drives routing |
| `mpv_routing.json` | Generated: question index → lecture ids |
| `MPV/*.pdf` | Source slides |
| `MPV/markdown/*.md` | docling-extracted slide text |
| `tmp_mpv_guide/q_NNNN.md` | Per-question generated answers (cache) |
| `page/docs/mpv/*.md` | Per-question site pages |

Steps:

```bash
# 1. Convert PDFs (only when slides change)
uv run docling MPV/*.pdf --to md --image-export-mode placeholder --output MPV/markdown/

# 2. Route questions to lectures (only when questions or manifest change)
uv run python route_questions.py

# 3. Generate grounded answers (skips cached chunks)
uv run python generate_mpv_guide.py

# 4. (Optional) Add self-tests + answer keys via Claude Code subagents — see below.

# 5. Build the site
uv run python build_mpv_site.py

# 6. Serve locally
cd page && uv run --project .. mkdocs serve
```

To regenerate a specific question, delete its `tmp_mpv_guide/q_XXXX.md` cache file and re-run step 3.

## Adding a new course

Say you want to add a course `XYZ`:

1. **Drop PDFs** into `XYZ/*.pdf` and convert:

   ```bash
   mkdir -p XYZ/markdown
   uv run docling XYZ/*.pdf --to md --image-export-mode placeholder --output XYZ/markdown/
   ```

2. **Write `xyz_q.txt`** — one exam question per line.

3. **Write `xyz_lectures.json`** — describes each PDF's content for the router:

   ```json
   {
     "lectures": [
       {
         "file": "lecture01_intro",
         "title": "Introduction",
         "topics": "Comma-separated terms the router should match against questions."
       }
     ]
   }
   ```

   `file` must equal the markdown filename without `.md`. `topics` should list every concept name a question might mention — the router only matches on this field.

4. **Route + generate** using the existing scripts' CLI flags (no fork needed for these two):

   ```bash
   uv run python route_questions.py \
     --questions xyz_q.txt \
     --manifest xyz_lectures.json \
     --output xyz_routing.json

   uv run python generate_mpv_guide.py \
     --questions xyz_q.txt \
     --routing xyz_routing.json \
     --slides-dir XYZ/markdown \
     --output page/docs/xyz_guide.md \
     --tmp-dir tmp_xyz_guide
   ```

   To change the tutor persona (currently CTU MPV / Computer Vision), edit the `system_prompt` in `generate_mpv_guide.py:generate_answer`.

5. **Adapt the site builder**: `build_mpv_site.py` has hardcoded paths (`MPV_DIR`, `mpv_q.txt`, etc.) at the top. Copy it to `build_xyz_site.py` and update the constants.

## Subagents (self-test + answer key step)

Self-test sections and answer keys are appended by spawning Claude Code Sonnet subagents — one per question, in parallel batches. There's no standalone script today; you drive this from an interactive Claude Code session by asking it to "spawn a sonnet subagent for each question and append a Self-Test section" (and again for answer keys).

The prompts used are documented inline in the session history. If you want to reproduce: have each subagent `Read tmp_<course>_guide/q_NNNN.md`, append the new section with `Edit`, preserve existing content.

## Scripts reference

| Script | What it does |
|---|---|
| `llm_client.py` | Shared OpenAI-compatible client; reads API key from opencode's `auth.json` |
| `route_questions.py` | LLM-based classifier mapping each question to lecture id(s) |
| `generate_mpv_guide.py` | Main per-question generator with grounding + continuity context |
| `build_mpv_site.py` | Splits chunks into per-question pages, builds MkDocs nav, copies figures |
| `generate_study_guide.py` | Legacy EFD pipeline (H1-chunked rewrite of one big markdown) |
| `generate_from_questions.py` | Legacy DRS pipeline (question-driven, no slide grounding) |
| `fix_lists.py` | Inserts blank lines before markdown lists (renderer quirk) |

## Deployment

The site is deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `master`.

One-time setup in the GitHub repo settings:

1. **Settings → Pages → Build and deployment → Source**: set to `GitHub Actions`.
2. Push to `master`. The workflow builds `page/` with MkDocs and deploys the resulting `page/site/` directory.

Manual trigger: **Actions → Deploy to GitHub Pages → Run workflow**.

The deployed URL is set in `mkdocs.yml` as `site_url`; if you fork or move the repo, update it in `build_mpv_site.py` and re-run the builder.

## Setup

- Python 3.12+, managed with `uv`. Dependencies in `pyproject.toml`.
- LLM provider defaults to **MetaCentrum** (CTU e-infrastructure) via opencode's stored API key. To override, set `METACENTRUM_API_KEY` env var or edit `llm_client.py:DEFAULT_PROVIDER`.
- Default model: `deepseek-v4-pro-thinking` — slow but high-quality. Swap with `--model <id>`.
