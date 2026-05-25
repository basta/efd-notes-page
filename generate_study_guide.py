import os
import re
import argparse
import concurrent.futures
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (expecting OPENROUTER_API_KEY)
load_dotenv()


def load_markdown(file_path: str) -> str:
    """Loads the content of a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_by_h1(content: str) -> List[str]:
    """Splits markdown content by H1 headers, keeping the headers."""
    # Split by lines ensuring we capture the header
    lines = content.split("\n")
    chunks = []
    current_chunk = []

    for line in lines:
        if line.startswith("# ") and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
        current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    # Filter out empty chunks
    return [c for c in chunks if c.strip()]


def generate_study_guide_chunk(
    client: OpenAI,
    model: str,
    target_chunk: str,
    prev_context: List[str],
    next_context: List[str],
) -> str:
    """
    Rewrites a single chunk using the LLM, with context.
    """

    context_str = ""
    if prev_context:
        context_str += "--- PREVIOUS CONTEXT (DO NOT REWRITE) ---\n"
        context_str += "\n\n".join(prev_context)
        context_str += "\n--- END PREVIOUS CONTEXT ---\n\n"

    context_str += "--- CURRENT SECTION TO REWRITE ---\n"
    context_str += target_chunk
    context_str += "\n--- END CURRENT SECTION ---\n\n"

    if next_context:
        context_str += "--- NEXT CONTEXT (DO NOT REWRITE) ---\n"
        context_str += "\n\n".join(next_context)
        context_str += "\n--- END NEXT CONTEXT ---\n"

    system_prompt = (
        "You are an expert tutor in Control Theory and Estimation. "
        "Your task is to rewrite the provided markdown section into a high-quality study guide or textbook format. "
        "Follow these rules strictly:\n"
        "1.  **Keep the H1 Header**: The output must start with the same H1 header as the input (if present).\n"
        "2.  **Preserve Links**: You MUST preserve all image links `![]()` and HTML spans `<span ...>` exactly as they index content.\n"
        "3.  **Explain Clearly**: Expand on bullet points, explain formulas, and make the text flow logically like a book.\n"
        "4.  **Use Context**: Use the provided previous/next context to ensure continuity, but ONLY output the rewritten content for the 'CURRENT SECTION'.\n"
        "5.  **Latex**: Preserve and fix any latex formatting issues if found. IMPORTANT: Block equations start and end with `$$` and MUST be on their own lines, surrounded by blank lines.\n"
        "6.  **Lists**: You MUST provide a blank line before starting any list (bulleted or numbered) to ensure proper rendering.\n"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context_str},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling API: {e}")
        return target_chunk  # Fallback to original


def process_chunk_task(
    client: OpenAI,
    model: str,
    chunk: str,
    prev_context: List[str],
    next_context: List[str],
    index: int,
    tmp_dir: str,
    dry_run: bool,
) -> str:
    """Task to process a single chunk and save to tmp."""
    tmp_file = os.path.join(tmp_dir, f"chunk_{index:04d}.md")

    if os.path.exists(tmp_file):
        print(f"Skipping section {index + 1} (already exists in tmp)")
        with open(tmp_file, "r", encoding="utf-8") as f:
            return f.read()

    print(f"Processing section {index + 1}...")

    if dry_run:
        result = chunk + " (DRY RUN PROCESSED)"
        print(f"--- DRY RUN: Section {index + 1} ---")
    else:
        result = generate_study_guide_chunk(
            client, model, chunk, prev_context, next_context
        )

    # Save to tmp file
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(result)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate a study guide from markdown notes."
    )
    parser.add_argument(
        "--input", default="page/docs/efd-slides.md", help="Input markdown file"
    )
    parser.add_argument(
        "--output", default="page/docs/study_guide.md", help="Output markdown file"
    )
    parser.add_argument(
        "--model", default="google/gemini-3-flash-preview", help="OpenRouter model ID"
    )
    parser.add_argument(
        "--context-window", type=int, default=3, help="Number of sections for context"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Do not call API, just print prompts"
    )
    parser.add_argument(
        "--separator",
        default="\n\n<!-- SECTION DELIMITER -->\n\n",
        help="Separator between sections",
    )
    parser.add_argument(
        "--tmp-dir",
        default="tmp_study_guide",
        help="Directory for temporary chunk files",
    )
    parser.add_argument(
        "--workers", type=int, default=5, help="Number of parallel workers"
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found in environment variables.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    print(f"Loading {args.input}...")
    content = load_markdown(args.input)
    chunks = split_by_h1(content)
    print(f"Found {len(chunks)} sections.")

    # Create tmp dir
    os.makedirs(args.tmp_dir, exist_ok=True)
    print(f"Using temp directory: {args.tmp_dir}")

    # Prepare tasks

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures_map = {}

        for i, chunk in enumerate(chunks):
            # Get context
            start_prev = max(0, i - args.context_window)
            prev_context = chunks[start_prev:i]

            end_next = min(len(chunks), i + 1 + args.context_window)
            next_context = chunks[i + 1 : end_next]

            future = executor.submit(
                process_chunk_task,
                client,
                args.model,
                chunk,
                prev_context,
                next_context,
                i,
                args.tmp_dir,
                args.dry_run,
            )
            futures_map[future] = i

        print(f"Submitted {len(chunks)} tasks with {args.workers} workers.")

        # Wait for all to complete
        results_list = [None] * len(chunks)
        for future in concurrent.futures.as_completed(futures_map):
            idx = futures_map[future]
            try:
                res = future.result()
                results_list[idx] = res
                print(f"Completed section {idx + 1}/{len(chunks)}")
            except Exception as e:
                print(f"Task for section {idx + 1} generated an exception: {e}")
                results_list[idx] = chunks[idx]  # Fallback

    print(f"Merging {len(results_list)} chunks into {args.output}...")
    with open(args.output, "w", encoding="utf-8") as f:
        # Filter out any Nones if something went catastrophic (though fallback above handles it)
        valid_chunks = [c for c in results_list if c is not None]
        f.write(args.separator.join(valid_chunks))

    print("Done!")


if __name__ == "__main__":
    main()
