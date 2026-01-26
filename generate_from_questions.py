import os
import argparse
import time
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (expecting OPENROUTER_API_KEY)
load_dotenv()


def load_questions(file_path: str) -> List[str]:
    """Loads questions from a text file, one per line."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line]  # Filter empty lines


def generate_answer(
    client: OpenAI,
    model: str,
    question: str,
    index: int,
    context_buffer: List[str],
) -> str:
    """
    Generates an answer for a single question, using previous answers as context.
    """

    context_str = ""
    if context_buffer:
        context_str += "--- PREVIOUSLY WRITTEN SECTIONS (CONTEXT) ---\n"
        context_str += "\n\n".join(context_buffer)
        context_str += "\n--- END PREVIOUS CONTEXT ---\n\n"

    system_prompt = (
        "You are an expert tutor in Control Theory and Network Science. "
        "You are writing a continuous, comprehensive study guide based on a series of questions. "
        "Your task is to write the next section of the guide corresponding to the provided question.\n\n"
        "Follow these rules strictly:\n"
        "1.  **Context**: Use the provided 'PREVIOUSLY WRITTEN SECTIONS' to maintain flow, consistency, and avoid repetition. Connect your new section logically to what came before.\n"
        "2.  **Structure**: You have full control over the structure. Use clear headings (Markdown H2, H3), lists, and bold text to organize the content effectively. "
        f"The current topic is based on Question {index}.\n"
        "3.  **Comprehensive**: Provide a detailed, textbook-quality explanation. Define terms, derive formulas if needed, and give examples.\n"
        "4.  **Math**: Use LaTeX for mathematics. Block equations MUST start and end with `$$` and be on their own lines.\n"
        "5.  **Tone**: tailored for a university-level student preparing for an exam.\n"
    )

    user_message = f"{context_str}Current Question to Answer: {question}\n\nPlease write the section for this question."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling API for question {index}: {e}")
        return f"## Question {index}: {question}\n\n[Error generating answer: {e}]"


def main():
    parser = argparse.ArgumentParser(
        description="Generate a study guide from a list of questions."
    )
    parser.add_argument(
        "--input", default="drs_q.txt", help="Input text file with questions"
    )
    parser.add_argument(
        "--output", default="page/docs/generated_guide.md", help="Output markdown file"
    )
    parser.add_argument(
        "--model",
        default="google/gemini-3-flash-preview",
        help="OpenRouter model ID",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Do not call API, just print prompts"
    )
    parser.add_argument(
        "--tmp-dir",
        default="tmp_questions_guide",
        help="Directory for temporary chunk files",
    )
    parser.add_argument(
        "--context-window",
        type=int,
        default=3,
        help="Number of previous answers to keep in context",
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not found in environment variables.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    print(f"Loading questions from {args.input}...")
    questions = load_questions(args.input)
    print(f"Found {len(questions)} questions.")

    # Create tmp dir
    os.makedirs(args.tmp_dir, exist_ok=True)

    generated_answers = []
    context_buffer = []

    # Sequential Loop
    for i, question in enumerate(questions, 1):
        tmp_file = os.path.join(args.tmp_dir, f"q_{i:04d}.md")

        result = None
        if (
            os.path.exists(tmp_file) and not args.dry_run
        ):  # verify if we can reuse existing file
            # Optimization: If file exists, we generally want to skip.
            # HOWEVER, if we are changing logic to depend on Previous Context,
            # re-using old independent chunks might break the flow.
            # User said "generated md for past questions in the context window".
            # If I re-run, I should probably re-generate to ensure flow, OR I assume
            # the previous run was also sequential.
            # For safety, let's just always read if it exists, but print a warning that context might be stale if it was run differently.
            # Actually, if the file exists, I should probably load it to populate the context buffer for the NEXT question!
            print(f"Found existing file for Question {i}. Loading...")
            with open(tmp_file, "r", encoding="utf-8") as f:
                result = f.read()

        if result is None:
            print(f"Processing Question {i}/{len(questions)}: {question[:50]}...")
            if args.dry_run:
                result = f"## Answer to {i}: {question}\n\n[Context size: {len(context_buffer)} items]\n(Dry Run Content)"
                print(f"-- Dry Run Prompt Context: {len(context_buffer)} prev items --")
            else:
                result = generate_answer(
                    client, args.model, question, i, context_buffer
                )
                # Save to tmp immediately
                with open(tmp_file, "w", encoding="utf-8") as f:
                    f.write(result)

        generated_answers.append(result)

        # Update context buffer
        context_buffer.append(result)
        if len(context_buffer) > args.context_window:
            context_buffer.pop(0)

    print(f"Merging {len(generated_answers)} answers into {args.output}...")
    with open(args.output, "w", encoding="utf-8") as f:
        # Add a title
        f.write("# Study Guide Questions & Answers\n\n")
        f.write("\n\n---\n\n".join(generated_answers))

    print("Done!")


if __name__ == "__main__":
    main()
