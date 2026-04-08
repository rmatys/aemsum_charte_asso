#!/usr/bin/env python3
"""
Renumber Article headings in the charter sequentially and update all internal
cross-references. References wrapped in ** (e.g. **article 59**) are external
law references and are left unchanged.

Usage: python renumber_articles.py [file.md]
Defaults to README.md.
"""
import re, sys

FILE = sys.argv[1] if len(sys.argv) > 1 else "README.md"

with open(FILE, encoding="utf-8") as f:
    lines = f.readlines()

# Pass 1 – build old→new mapping from heading order
old_to_new: dict[int, int] = {}
counter = 0
for line in lines:
    m = re.match(r"^Article (\d+)\s*:", line)
    if m:
        counter += 1
        old = int(m.group(1))
        if old not in old_to_new:          # first occurrence wins
            old_to_new[old] = counter

# Pass 2 – rewrite headings with new sequential numbers
counter = 0
new_lines = []
for line in lines:
    m = re.match(r"^(Article )(\d+)(\s*:)", line)
    if m:
        counter += 1
        line = m.group(1) + str(counter) + m.group(3) + line[m.end():]
    new_lines.append(line)

content = "".join(new_lines)

# Pass 3 – update lowercase body references, preserving bold segments
def _sub(x):
    return "article " + str(old_to_new.get(int(x.group(1)), int(x.group(1))))

def update_references(text: str) -> str:
    parts = []
    last = 0
    for bold in re.finditer(r"\*\*[^*]+\*\*", text):
        segment = re.sub(r"\barticle (\d+)\b", _sub, text[last:bold.start()])
        parts.append(segment)
        parts.append(bold.group(0))   # bold kept verbatim
        last = bold.end()
    parts.append(re.sub(r"\barticle (\d+)\b", _sub, text[last:]))
    return "".join(parts)

content = update_references(content)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

changed = {k: v for k, v in old_to_new.items() if k != v}
print(f"Done: {counter} articles renumbered in '{FILE}'.")
if changed:
    print(f"Renumbered: {changed}")
else:
    print("All article numbers were already correct.")
