"""Strip a Claude Code reply down to clean spoken prose.

Removes/replaces things that are painful to hear read aloud literally:
code blocks, inline code, markdown syntax, links, file paths/URLs, tables.
Pure stdlib, no dependencies.
"""
import re


def clean_for_speech(text: str) -> str:
    if not text:
        return ""

    t = text

    # Fenced code blocks -> a short spoken cue, not the contents
    t = re.sub(r"```.*?```", ", code block, ", t, flags=re.DOTALL)

    # Markdown tables: a block of consecutive lines containing '|' with a
    # header-separator row (---|---) -> a short spoken cue
    def _replace_table(block_text: str) -> str:
        lines = block_text.split("\n")
        out_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            is_table_start = (
                "|" in line
                and i + 1 < len(lines)
                and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1] or "")
                and "-" in lines[i + 1]
            )
            if is_table_start:
                j = i
                while j < len(lines) and "|" in lines[j]:
                    j += 1
                out_lines.append(", a table, ")
                i = j
            else:
                out_lines.append(line)
                i += 1
        return "\n".join(out_lines)

    t = _replace_table(t)

    # Markdown links [text](url) -> just the text (must run before the bare
    # URL/path stripping below, or the URL inside the parens gets replaced
    # first and breaks this pattern)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)

    # File paths and URLs -> a short spoken cue instead of reading every
    # slash/backslash/extension character by character
    t = re.sub(r"https?://\S+", " a link ", t)
    t = re.sub(r"(?:[A-Za-z]:\\|/)[\w./\\\-]{4,}", " a file path ", t)

    # Inline code `x` -> x (keep the content, drop the backticks)
    t = re.sub(r"`([^`]+)`", r"\1", t)

    # Headers: strip leading #'s
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.MULTILINE)

    # Bold / italic markers
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"__(.+?)__", r"\1", t)
    t = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", t)

    # Bullet / numbered list markers at line start -> drop the marker only
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*\d+\.\s+", "", t, flags=re.MULTILINE)

    # Blockquote markers
    t = re.sub(r"^\s*>\s?", "", t, flags=re.MULTILINE)

    # Horizontal rules
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.MULTILINE)

    # Collapse whitespace
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{2,}", ". ", t)
    t = re.sub(r"\n", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    t = re.sub(r",\s*,", ",", t)

    return t.strip()


if __name__ == "__main__":
    import sys
    raw = sys.stdin.read()
    print(clean_for_speech(raw))
