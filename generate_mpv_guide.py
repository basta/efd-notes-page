"""Generates a Computer Vision Methods (MPV) study guide from a list of questions,
grounded in the lecture slide text routed per-question.

Per-question flow:
  1. Look up which lecture(s) this question maps to (from mpv_routing.json).
  2. Load the text of those lecture(s) from MPV/markdown/<file>.md.
  3. Prompt the LLM with: previous answers (continuity context) + slide material + question.
  4. If no lecture matched, prompt without grounding and prepend an out-of-syllabus warning.
"""

import os
import json
import shutil
import argparse
from typing import List
from openai import OpenAI
from llm_client import make_client, DEFAULT_MODEL


def load_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_routing(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_slide_text(slides_dir: str, lecture_ids: List[str]) -> str:
    parts = []
    for lid in lecture_ids:
        md_path = os.path.join(slides_dir, f"{lid}.md")
        if not os.path.exists(md_path):
            print(f"  WARN: missing slide file {md_path}")
            continue
        with open(md_path, "r", encoding="utf-8") as f:
            parts.append(f"### Lecture: {lid}\n\n{f.read()}")
    return "\n\n---\n\n".join(parts)


def generate_answer(
    client: OpenAI,
    model: str,
    question: str,
    index: int,
    prev_answers: List[str],
    slide_material: str,
    out_of_syllabus: bool,
) -> str:
    system_prompt = (
        "You are an expert tutor for the CTU FEE A4M33MPV / B4M33MPV course "
        "(Computer Vision Methods). You are writing a continuous, textbook-style "
        "study guide based on a series of exam questions.\n\n"
        "Rules:\n"
        "1. **Ground in slide material when provided.** Match the course's terminology "
        "and framing. If the slides call something 'DCT' rather than 'KCF', use the "
        "course's term but explain the equivalence.\n"
        "2. **Use previous sections for continuity.** Don't repeat definitions already "
        "covered; instead, reference them briefly and build on them.\n"
        "3. **Structure freely.** Use H2 for the question heading, H3/H4 as needed, "
        "lists, bold for key terms.\n"
        "4. **Math in LaTeX.** Block equations on their own lines, surrounded by blank "
        "lines, with `$$ ... $$`. Inline math with `$ ... $`.\n"
        "5. **Lists need a blank line before them.** Markdown rendering quirk.\n"
        "6. **Be exam-ready.** Detailed enough that a student reading only this guide "
        "can answer the question fully. Define terms, derive formulas if useful, give "
        "intuition AND mechanics.\n"
        "7. **Do not invent slide citations.** Don't say 'as shown in slide 12' — you "
        "don't have slide numbers.\n"
    )

    if out_of_syllabus:
        system_prompt += (
            "\n**Out-of-syllabus warning.** This question was NOT found in the 2026 "
            "MPV slides. Start your answer with a blockquote warning: "
            "'> **Note:** This question was not found in the 2026 MPV slides — it may "
            "be from an older syllabus. Answer below is based on general computer "
            "vision knowledge.' Then answer as best you can.\n"
        )

    user_parts = []
    if prev_answers:
        user_parts.append("--- PREVIOUSLY WRITTEN SECTIONS (for continuity, do not rewrite) ---")
        user_parts.append("\n\n".join(prev_answers))
        user_parts.append("--- END PREVIOUS SECTIONS ---")

    if slide_material:
        user_parts.append("\n--- COURSE SLIDE MATERIAL (ground your answer in this) ---")
        user_parts.append(slide_material)
        user_parts.append("--- END SLIDE MATERIAL ---")

    user_parts.append(f"\nQuestion {index}: {question}\n\nWrite the section now.")
    user_msg = "\n".join(user_parts)

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default="mpv_q.txt")
    parser.add_argument("--routing", default="mpv_routing.json")
    parser.add_argument("--slides-dir", default="MPV/markdown")
    parser.add_argument("--output", default="page/docs/mpv_guide.md")
    parser.add_argument("--tmp-dir", default="tmp_mpv_guide")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--context-window", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    client = make_client()

    questions = load_lines(args.questions)
    routing = load_routing(args.routing)
    os.makedirs(args.tmp_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Loaded {len(questions)} questions, routing for {len(routing)} of them.")

    answers = []
    context_buffer = []

    for i, question in enumerate(questions, 1):
        tmp_file = os.path.join(args.tmp_dir, f"q_{i:04d}.md")

        if os.path.exists(tmp_file) and not args.dry_run:
            print(f"  [{i:02d}] cached")
            with open(tmp_file, "r", encoding="utf-8") as f:
                result = f.read()
        else:
            lecture_ids = routing.get(str(i), [])
            out_of_syllabus = not lecture_ids
            slide_material = load_slide_text(args.slides_dir, lecture_ids)
            tag = "OUT-OF-SYLLABUS" if out_of_syllabus else ", ".join(lecture_ids)
            print(f"  [{i:02d}] generating ({tag}): {question[:60]}...")

            if args.dry_run:
                result = (
                    f"## Q{i}: {question}\n\n[dry-run | grounding: {tag} | "
                    f"slide chars: {len(slide_material)} | prev ctx: {len(context_buffer)}]"
                )
            else:
                try:
                    result = generate_answer(
                        client, args.model, question, i,
                        context_buffer, slide_material, out_of_syllabus,
                    )
                except Exception as e:
                    print(f"    ERROR: {e}")
                    result = f"## Q{i}: {question}\n\n[ERROR generating: {e}]"
                with open(tmp_file, "w", encoding="utf-8") as f:
                    f.write(result)

        answers.append(result)
        context_buffer.append(result)
        if len(context_buffer) > args.context_window:
            context_buffer.pop(0)

    print(f"Merging {len(answers)} answers into {args.output}...")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("# MPV Study Guide\n\n")
        f.write(
            "_Generated study guide for the CTU FEE A4M33MPV / B4M33MPV course "
            "(Computer Vision Methods). Each section answers one exam question, "
            "grounded in the relevant lecture slides where available._\n\n"
        )
        f.write("\n\n---\n\n".join(answers))

    figures_src = os.path.join(args.tmp_dir, "figures")
    if os.path.isdir(figures_src):
        figures_dst = os.path.join(os.path.dirname(args.output), "figures")
        os.makedirs(figures_dst, exist_ok=True)
        copied = 0
        for fname in os.listdir(figures_src):
            shutil.copy2(os.path.join(figures_src, fname), os.path.join(figures_dst, fname))
            copied += 1
        print(f"Copied {copied} figures -> {figures_dst}")

    print("Done.")


if __name__ == "__main__":
    main()
