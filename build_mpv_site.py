"""Builds the MkDocs MPV section: one page per question, grouped by lecture in nav.

Reads:
  mpv_q.txt              — list of questions
  mpv_routing.json       — question_idx -> [lecture_id, ...]
  mpv_lectures.json      — lecture id, title, topics (defines section order)
  tmp_mpv_guide/q_*.md   — per-question generated content
  tmp_mpv_guide/figures/ — referenced PNGs

Writes:
  page/docs/mpv/<slug>.md  — one page per question
  page/docs/figures/       — copied from tmp_mpv_guide/figures/
  page/mkdocs.yml          — rewritten with nav + Material theme features
"""

import os
import re
import json
import shutil
import yaml

DOCS = "page/docs"
MPV_DIR = os.path.join(DOCS, "mpv")
FIGURES_DST = os.path.join(DOCS, "figures")
FIGURES_SRC = "tmp_mpv_guide/figures"
TMP_DIR = "tmp_mpv_guide"
MKDOCS_YML = "page/mkdocs.yml"


def slugify(text: str, max_words: int = 6) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    words = text.split()[:max_words]
    return "-".join(words)


def short_title(question: str, max_words: int = 6) -> str:
    """Short navigation label, e.g. 'Wide-baseline matching'."""
    first = question.split(".")[0].strip()
    if len(first.split()) > max_words:
        first = " ".join(first.split()[:max_words]) + "…"
    return first


def main():
    with open("mpv_q.txt", encoding="utf-8") as f:
        questions = [ln.strip() for ln in f if ln.strip()]
    routing = json.load(open("mpv_routing.json", encoding="utf-8"))
    lectures = json.load(open("mpv_lectures.json", encoding="utf-8"))["lectures"]

    os.makedirs(MPV_DIR, exist_ok=True)
    os.makedirs(FIGURES_DST, exist_ok=True)

    # Group questions by their primary (first-listed) lecture.
    # Empty routing => "out-of-syllabus".
    by_lecture: dict[str, list[tuple[int, str, str]]] = {lec["file"]: [] for lec in lectures}
    by_lecture["__out_of_syllabus__"] = []

    for i, q in enumerate(questions, 1):
        routed = routing.get(str(i), [])
        primary = routed[0] if routed else "__out_of_syllabus__"
        if primary not in by_lecture:
            primary = "__out_of_syllabus__"
        slug = f"q{i:02d}-{slugify(q)}"
        by_lecture[primary].append((i, slug, q))

    # Write per-question pages
    written = 0
    for i, q in enumerate(questions, 1):
        src = os.path.join(TMP_DIR, f"q_{i:04d}.md")
        if not os.path.exists(src):
            print(f"  WARN: missing {src}")
            continue
        slug = f"q{i:02d}-{slugify(q)}"
        dst = os.path.join(MPV_DIR, f"{slug}.md")
        # Bump # paths: file is now one directory deeper, so figures/foo.png
        # references stay valid because we also copy figures into docs/figures
        # but the markdown lives at docs/mpv/<slug>.md, so figures/ is a sibling
        # of mpv/ — need to rewrite to ../figures/...
        with open(src, encoding="utf-8") as f:
            content = f.read()
        content = content.replace("](figures/", "](../figures/")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(content)
        written += 1
    print(f"Wrote {written} per-question pages to {MPV_DIR}/")

    # Copy figures
    if os.path.isdir(FIGURES_SRC):
        copied = 0
        for fname in os.listdir(FIGURES_SRC):
            shutil.copy2(os.path.join(FIGURES_SRC, fname), os.path.join(FIGURES_DST, fname))
            copied += 1
        print(f"Copied {copied} figures -> {FIGURES_DST}/")

    # Write a section landing page
    landing = os.path.join(MPV_DIR, "index.md")
    with open(landing, "w", encoding="utf-8") as f:
        f.write("# MPV Study Guide\n\n")
        f.write(
            "_Generated study guide for the CTU FEE A4M33MPV / B4M33MPV course "
            "(Computer Vision Methods). Each section answers one exam question, "
            "grouped by lecture._\n\n"
        )
        for lec in lectures:
            qs = by_lecture.get(lec["file"], [])
            if not qs:
                continue
            f.write(f"## {lec['title']}\n\n")
            for i, slug, q in qs:
                f.write(f"- [Q{i}. {short_title(q)}]({slug}.md)\n")
            f.write("\n")
        oos = by_lecture["__out_of_syllabus__"]
        if oos:
            f.write("## Beyond 2026 Syllabus\n\n")
            for i, slug, q in oos:
                f.write(f"- [Q{i}. {short_title(q)}]({slug}.md)\n")

    # Build the MkDocs nav structure
    nav = [
        {"Home": "index.md"},
    ]
    if os.path.exists(os.path.join(DOCS, "generated_guide.md")):
        nav.append({"EFD Generated Guide": "generated_guide.md"})

    mpv_section: list = [{"Overview": "mpv/index.md"}]
    for lec in lectures:
        qs = by_lecture.get(lec["file"], [])
        if not qs:
            continue
        section = []
        for i, slug, q in qs:
            section.append({f"Q{i}. {short_title(q)}": f"mpv/{slug}.md"})
        mpv_section.append({lec["title"]: section})
    oos = by_lecture["__out_of_syllabus__"]
    if oos:
        oos_section = []
        for i, slug, q in oos:
            oos_section.append({f"Q{i}. {short_title(q)}": f"mpv/{slug}.md"})
        mpv_section.append({"Beyond 2026 Syllabus": oos_section})
    nav.append({"MPV Guide": mpv_section})

    # Rewrite mkdocs.yml preserving theme & math, adding features + nav
    mkdocs_cfg = {
        "site_name": "Course Study Guides",
        "site_url": "https://basta.github.io/efd-notes-page/",
        "repo_url": "https://github.com/basta/efd-notes-page",
        "theme": {
            "name": "material",
            "palette": {"scheme": "default"},
            "features": [
                "navigation.sections",
                "navigation.indexes",
                "navigation.top",
                "navigation.tracking",
                "toc.follow",
                "content.code.copy",
            ],
        },
        "markdown_extensions": [
            {"pymdownx.arithmatex": {"generic": True}},
            "admonition",
            "pymdownx.details",
        ],
        "extra_javascript": [
            "javascripts/mathjax.js",
            "https://polyfill.io/v3/polyfill.min.js?features=es6",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
        ],
        "nav": nav,
    }
    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.safe_dump(mkdocs_cfg, f, sort_keys=False, allow_unicode=True)
    print(f"Updated {MKDOCS_YML}")

    print("\nDone. Run:  cd page && uv run --project .. mkdocs serve")


if __name__ == "__main__":
    main()
