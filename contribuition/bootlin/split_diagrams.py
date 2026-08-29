#!/usr/bin/env python3
"""Split every text+diagram slide in linux-kernel.md so each diagram gets its own slide."""
import re, sys

PATH = "/home/panicking/work/michael/kernel-slides/kernel/linux-kernel/linux-kernel.md"
src = open(PATH).read()

# Slides are separated by a line that is exactly `---`. Verify no `---` sits inside a code fence.
in_fence = False
for i, ln in enumerate(src.split("\n"), 1):
    s = ln.strip()
    if s.startswith("```"):
        in_fence = not in_fence
    elif in_fence and s == "---":
        print(f"ERROR: `---` inside code fence at line {i}", file=sys.stderr)
        sys.exit(1)

# Split into segments on `---` lines. Even indices = content, odd indices = frontmatter.
segs = re.split(r'(?m)^---\s*\n', src)
# segs[0] is '' (file begins with ---); content slides are segs[2], segs[4], ...
# Their frontmatter is segs[1], segs[3], ...

IMG_DIV = re.compile(
    r'(?P<indent>[ \t]*)<div style="text-align:center;">\s*\n'
    r'\s*<img src="/images/(?P<name>[a-z0-9-]+)\.svg" style="[^"]*" />\s*\n'
    r'\s*</div>'
)

IMG_ONLY = {"kernel-in-system", "system-call", "dev-model", "thread-life"}

def title_of(content):
    m = re.search(r'(?m)^#\s+(.*)$', content)
    return m.group(1).strip() if m else None

def has_body(content):
    # content minus the title and minus any image divs; is anything left?
    c = re.sub(r'(?m)^#\s+.*$', '', content)
    c = IMG_DIV.sub('', c)
    return bool(c.strip())

new_segs = []
i = 0
splits = 0
while i < len(segs):
    # frontmatter (odd) then content (even)
    if i == 0:
        new_segs.append(segs[0])
        i += 1
        continue
    if i % 2 == 1:
        # frontmatter segment
        new_segs.append(segs[i])
        i += 1
        continue
    # even index: content segment
    content = segs[i]
    m = IMG_DIV.search(content)
    if not m or m.group("name") in IMG_ONLY:
        new_segs.append(content)
        i += 1
        continue
    if not has_body(content):
        # only title + image -> already a dedicated diagram slide
        new_segs.append(content)
        i += 1
        continue

    title = title_of(content) or "Diagram"
    name = m.group("name")

    # 1. remove the image div from the text slide
    text_slide = IMG_DIV.sub('', content, count=1)
    # collapse trailing blank lines
    text_slide = text_slide.rstrip() + "\n"

    # 2. build a dedicated diagram slide (larger)
    diagram_slide = (
        f"# {title}\n\n"
        f'<div style="text-align:center;">\n'
        f'  <img src="/images/{name}.svg" '
        f'style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />\n'
        f"</div>\n"
    )
    diagram_fm = "layout: default\nhideInToc: true\n"

    new_segs.append(text_slide)
    new_segs.append(diagram_fm)
    new_segs.append(diagram_slide)
    splits += 1
    i += 1

out = "---\n".join(new_segs)
open(PATH, "w").write(out)
print(f"split {splits} slides; new file written ({len(out.splitlines())} lines)")
