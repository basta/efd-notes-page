"""Maps each MPV question to the lecture(s) most likely to cover it.

Outputs mpv_routing.json: {"<question_idx>": ["<lecture_file>", ...]}
Empty list means "no relevant lecture in current slides" — the generator will
flag the answer as potentially outdated/out-of-curriculum.
"""

import os
import json
import argparse
from llm_client import make_client, DEFAULT_MODEL


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["lectures"]


def route_question(client, model, question, lectures):
    manifest_str = "\n".join(
        f"- id: {lec['file']}\n  title: {lec['title']}\n  topics: {lec['topics']}"
        for lec in lectures
    )
    system_prompt = (
        "You assign exam questions to lecture slide decks. "
        "Return STRICT JSON only — no prose, no code fences. "
        "Schema: {\"lectures\": [<lecture id>, ...]}. "
        "Choose 1-3 lecture ids whose 'topics' clearly cover the question. "
        "If no lecture clearly covers it, return an empty list. "
        "Do NOT guess — only include a lecture if its topics explicitly mention the concept."
    )
    user_msg = (
        f"Available lectures:\n{manifest_str}\n\n"
        f"Question: {question}\n\n"
        "Return JSON now."
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.0,
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").split("\n", 1)[1].rsplit("\n", 1)[0]
        if raw.startswith("json"):
            raw = raw[4:].lstrip()
    data = json.loads(raw)
    valid_ids = {lec["file"] for lec in lectures}
    return [lid for lid in data.get("lectures", []) if lid in valid_ids]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default="mpv_q.txt")
    parser.add_argument("--manifest", default="mpv_lectures.json")
    parser.add_argument("--output", default="mpv_routing.json")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    client = make_client()

    questions = load_questions(args.questions)
    lectures = load_manifest(args.manifest)
    print(f"Routing {len(questions)} questions across {len(lectures)} lectures...")

    routing = {}
    if os.path.exists(args.output):
        with open(args.output, "r", encoding="utf-8") as f:
            routing = json.load(f)

    for i, q in enumerate(questions, 1):
        key = str(i)
        if key in routing:
            print(f"  [{i:02d}] cached -> {routing[key]}")
            continue
        try:
            matched = route_question(client, args.model, q, lectures)
        except Exception as e:
            print(f"  [{i:02d}] ERROR: {e}")
            matched = []
        routing[key] = matched
        flag = "OUT-OF-SYLLABUS" if not matched else ", ".join(matched)
        print(f"  [{i:02d}] {q[:60]:<60} -> {flag}")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(routing, f, indent=2)

    print(f"Done. Wrote {args.output}.")


if __name__ == "__main__":
    main()
