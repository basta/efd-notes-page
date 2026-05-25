# Course Study Guides

LLM-generated study guides for CTU FEE master's courses, grounded in lecturer slides and structured around exam-style questions.

## Available courses

### [MPV — Computer Vision Methods](mpv/index.md)

44 exam questions covering local features (Harris, SIFT, MSER, FAST), image retrieval (BoW, VLAD, SMK, NetVLAD), deep metric learning, self-supervised learning, RANSAC, tracking (KLT, KCF, TLD, mean-shift), Hough transform, and deep nets for classification and detection. Each section ends with a self-test and answer key.

### [EFD — Estimation, Filtering, and Detection](generated_guide.md)

Bayesian estimation, Kalman filtering, parameter estimation, change detection, Monte Carlo methods, Gaussian process regression.

## How to use a section

Each MPV question page is structured as:

1. **Explanation** — textbook-quality answer grounded in the relevant lecture slides
2. **Self-Test** — 3-4 comprehension questions
3. **Answer Key** — work through the test first, then check yourself

## How it's built

PDFs → `docling` extraction → per-question LLM routing to the relevant lecture(s) → grounded answers via thinking-model LLM → Sonnet subagents append self-tests and answer keys → MkDocs Material site.

See the [README](https://github.com/basta/efd-notes-page/blob/master/README.md) for the full pipeline and how to add a new course.
