import re

file_path = "page/docs/study_guide.md"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
# Pattern for a list item marker at start of line (allowing indentation)
list_pattern = re.compile(r"^\s*([*\-+]|\d+\.)\s+")

for i, line in enumerate(lines):
    # Check if this line is a list item
    is_list_item = list_pattern.match(line)

    if is_list_item:
        # Check previous line
        if i > 0:
            prev_line = lines[i - 1]
            prev_stripped = prev_line.strip()

            # If previous line is not empty and not a list item itself and not a header
            # We should probably insert a newline
            # Note: We need to be careful about nested lists.
            # If the current indentation > previous indentation, it might be a nested list which is fine?
            # But standard checks usually look for blank lines before the *block* of list items.

            prev_is_list_item = list_pattern.match(prev_line)

            # If previous line is text (non-empty, non-list, non-header, non-separator)
            if prev_stripped and not prev_is_list_item:
                # Exclude if it looks like a header (starts with #)
                if not prev_stripped.startswith("#"):
                    # We found a transition from text to list without newline
                    # Only if we aren't already adding one
                    if new_lines and new_lines[-1].strip() != "":
                        new_lines.append("\n")

    new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Processed {len(lines)} lines.")
