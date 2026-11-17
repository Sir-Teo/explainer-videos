#!/usr/bin/env python
"""Build the course site for *Quant, Built*: one page of course material per part, for GitHub Pages.

    python tools/course_site.py                  # -> _site/ (runs the 43 labs: about a minute), then the
                                                 #    other courses and the landing page (tools/series_site.py)
    python tools/course_site.py --quant-only     # this course alone
    python tools/course_site.py --no-labs        # pages only, reusing lab figures already in _site/
    python tools/course_site.py --parts 10 12    # just these parts' pages (and the index)
    python -m http.server -d _site 8000          # look at it

The site is generated from what the repository already holds, so it cannot drift from the films:

* ``videos/quant/course``: each part's level, prerequisites, story, objectives by track, key results;
* each part's ``manifest.py``: the chapters, in the film's order, with their length from the narration;
* each part's ``README.md``: lecture notes, desk questions, problems with worked solutions, the researcher's
  notes (English, and the Chinese edition below it);
* ``videos/quant/labs``: the lab's code, its output and its figure, produced by running it;
* ``videos/quant/READING.md``: the part's papers.

It needs numpy, scipy, matplotlib, numba and markdown-it-py, not manim: ``.github/workflows/course-site.yml`` builds
and publishes it on every push to main.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))  # lecture_text, beside this file

from markdown_it import MarkdownIt  # noqa: E402  (CommonMark, as GitHub reads the READMEs)

from videos.quant import course, labs  # noqa: E402  (labs first lets the House import without manim)

REPO = "https://github.com/Sir-Teo/explainer-videos"
BLOB = f"{REPO}/blob/main"
QUANT = ROOT / "videos" / "quant"
ASSETS = QUANT / "course" / "site"
WPM = 168  # the quant narrator's measured pace (tools/lecture_length.py)
TIER_NAME = {"U": "Undergraduate", "M": "Master's", "D": "PhD", "I": "Industry", "*": "All tracks"}
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def esc(text: str) -> str:
    return html.escape(text, quote=True)


def tex_inline(text: str) -> str:
    """Escape prose for HTML (the course table's text holds no markup)."""
    return esc(text)


NARRATING = {"rows_scene": 3}  # scene helpers that speak a script passed as this positional argument


def narration_words(path: Path, cls: str) -> int:
    """Words a scene class narrates (the same count as tools/lecture_length.py, without importing the films)."""
    words = 0
    for node in ast.walk(ast.parse(path.read_text())):
        if not (isinstance(node, ast.ClassDef) and node.name == cls):
            continue
        for call in ast.walk(node):
            if not isinstance(call, ast.Call):
                continue
            if isinstance(call.func, ast.Attribute) and (call.func.attr == "voiceover" or call.func.attr.endswith("_voiceover")) and call.args:
                arg = call.args[0]
            elif isinstance(call.func, ast.Name) and call.func.id in NARRATING and len(call.args) > NARRATING[call.func.id]:
                arg = call.args[NARRATING[call.func.id]]       # a part's helper that narrates a script it is given
            else:
                continue
            for sub in ast.walk(arg):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    words += len(re.sub(r"<bookmark[^>]*/>", " ", sub.value).split())
                elif isinstance(sub, ast.FormattedValue):
                    words += 3
        words += _section_words(node)
    return words


def _section_words(node) -> int:
    """Narration a scene passes through its part's section helpers: ``rows_section(self, title, items, narration)``
    and ``chips_section(...)`` take it as an argument, and ``card_section(self, n, title, question)`` speaks
    "Chapter n. Title"."""
    words = 0
    for call in ast.walk(node):
        if not isinstance(call, ast.Call):
            continue
        name = call.func.attr if isinstance(call.func, ast.Attribute) else getattr(call.func, "id", "")
        if not name.endswith("_section"):
            continue
        if name == "card_section":
            title = call.args[2] if len(call.args) > 2 else None
            words += 2 + (len(title.value.split()) if isinstance(title, ast.Constant) and isinstance(title.value, str)
                          else 3)
            continue
        arg = next((k.value for k in call.keywords if k.arg == "narration"), call.args[3] if len(call.args) > 3 else None)
        for sub in ast.walk(arg) if arg is not None else ():
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                words += len(re.sub(r"<bookmark[^>]*/>", " ", sub.value).split())
            elif isinstance(sub, ast.FormattedValue):
                words += 3
    return words


def chapter_minutes(n: int) -> list:
    """Estimated minutes of each chapter of Part ``n``, in the film's order."""
    out = []
    for module, cls, _ in course.manifest(n)[1]:
        out.append(narration_words(QUANT / f"quant{n}" / f"{module}.py", cls) / WPM)
    return out


def fmt_minutes(m: float) -> str:
    return f"{m:.0f} min" if m < 90 else f"{m / 60:.1f} h"


# ---------------------------------------------------------------------------
# Markdown: the READMEs and READING.md
# ---------------------------------------------------------------------------
_MATH = re.compile(r"\$\$(.+?)\$\$|\$((?:[^$\n]|\n(?!\s*\n)){1,400}?)\$", re.S)
_MATHY = re.compile(r"[\\^_{}]")
_TOKEN = re.compile(r"[A-Za-z]{1,3}(?:'|\([A-Za-z0-9,]{1,5}\))?|[A-Za-z]\s?[=<>≤≥]\s?-?[\dA-Za-z./]+")


_PROSE = re.compile(r"[A-Za-z]{3,}[ ,;]+[A-Za-z]{3,}")


def _inline_math(body: str, text: str, end: int) -> bool:
    """Whether ``$body$`` is math, as GitHub reads it: TeX (a backslash, ^, _ or braces) or a short symbol always is;
    otherwise a span is math unless the closing dollar runs into a digit (``$5 and $6``) or the span reads as prose
    or money (``$1.75 million ... $``)."""
    if _MATHY.search(body) or _TOKEN.fullmatch(body.strip()):
        return True
    if end < len(text) and text[end].isalnum():
        return False
    return not (_PROSE.search(body) or re.match(r"\d[\d.,]*\s*(?:[kKmMbB]n?\b|million|billion|thousand)", body)
                or "\n" in body.strip())


def protect_math(text: str) -> tuple[str, list]:
    """Pull ``$...$`` LaTeX out of Markdown (so underscores are not read as emphasis) and leave dollar amounts
    alone (``_inline_math`` decides which is which)."""
    stash = []

    def repl(m):
        display, inline = m.group(1), m.group(2)
        body = display if display is not None else inline
        if display is None and (body[0].isspace() or body[-1].isspace() or not _inline_math(body, m.string, m.end())):
            return m.group(0)
        stash.append((body, display is not None))
        return f"zzMATH{len(stash) - 1}zz"  # plain letters, which Markdown leaves alone

    # scan left to right so that a rejected "$1.75 million ... $" does not swallow the next real span
    out, pos = [], 0
    while True:
        m = _MATH.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        out.append(text[pos:m.start()])
        r = repl(m)
        if r == m.group(0):  # not math: keep the first dollar sign and look again after it
            out.append(text[m.start()])
            pos = m.start() + 1
        else:
            out.append(r)
            pos = m.end()
    return "".join(out), stash


def restore_math(page: str, stash: list) -> str:
    def repl(m):
        body, display = stash[int(m.group(1))]
        body = esc(" ".join(body.split()))
        return f"\\[{body}\\]" if display else f"\\({body}\\)"

    return re.sub(r"zzMATH(\d+)zz", repl, page)


_LINK = re.compile(r'(href|src)="([^"#][^"]*)"')
_MD = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable(["table", "strikethrough"])


def _late_bold(page: str) -> str:
    """``**粗体。**`` next to CJK punctuation is not emphasis under CommonMark's flanking rules (so GitHub shows the
    asterisks too); outside code, set it bold anyway."""
    parts = re.split(r"(<pre\b.*?</pre>|<code>.*?</code>)", page, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"\*\*([^*<>\n]{1,120}?)\*\*", r"<strong>\1</strong>", parts[i])
    return "".join(parts)


def md_to_html(text: str, base: Path) -> str:
    """Markdown to HTML; relative links are pointed at the file on GitHub (``base`` is the source's folder)."""
    text, stash = protect_math(text)
    page = _MD.render(text)

    def link(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", url):
            return m.group(0)
        path, _, frag = url.partition("#")
        target = (base / path).resolve()
        try:
            rel = target.relative_to(ROOT)
        except ValueError:
            return m.group(0)
        kind = "tree" if target.is_dir() else "blob"
        return f'{attr}="{REPO}/{kind}/main/{rel.as_posix()}{"#" + frag if frag else ""}"'

    page = _LINK.sub(link, page)
    page = _late_bold(page)
    page = page.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return restore_math(page, stash)


_SOLUTION = re.compile(r"<p>(?:<em>|<strong>|<i>|<b>)\s*(?:Solution|Answer|Hint and solution|解答|解|答)[^<]{0,20}"
                       r"(?:</em>|</strong>|</i>|</b>)")
_TAG = re.compile(r"<(/?)(li|ol|ul|div|details|blockquote|table|pre)\b[^>]*>|<p><strong>|<h[1-6]\b|<hr\b")


def _wrap(page: str, start: int, end: int, label: str) -> str:
    body = page[start:end]
    body = re.sub(r"^\s*<p><(em|strong|i|b)>\s*(?:Solution|Answer|解答|解|答)[.:：。]?\s*</\1>[.:：]?\s*", "<p>", body)
    body = re.sub(r"^\s*<p>\s*</p>\s*", "", body)
    return page[:start] + f'<details class="sol"><summary>{label}</summary>' + body + "</details>\n" + page[end:]


def _block_end(page: str, start: int) -> int:
    """Where a solution that starts at ``start`` ends: the end of its list item, or the next problem (a paragraph
    opening in bold), a heading or a rule, whichever comes first."""
    depth = 0
    for m in _TAG.finditer(page, start + 3):
        if m.group(2):
            depth += -1 if m.group(1) else 1
            if depth < 0:
                return m.start()
        elif depth == 0:
            return m.start()
    return len(page)


def _items(page: str) -> list:
    """(content start, content end) of every list item that is not inside another list item."""
    out, stack = [], []
    for m in re.finditer(r"<(/?)li\b[^>]*>", page):
        if not m.group(1):
            stack.append(m.end())
        elif stack:
            start = stack.pop()
            if not stack:
                out.append((start, m.start()))
    return out


def fold_solutions(page: str) -> str:
    """Put each worked solution of a problem set behind a "Solution" toggle, so the problems can be tried first.
    The READMEs write problem sets in a few shapes, read in this order:

    * a paragraph that opens with an italic or bold "Solution" (or 解答): it runs to the end of its list item, or
      to the next problem (a paragraph opening in bold);
    * a block of solutions after the problems, under a "Solutions" heading: the whole block is folded;
    * problems as list items, each a statement paragraph followed by the answer: the rest of the item is folded;
    * problems as paragraphs that open with a bold number and an italic question ("**1.** *the question*"), each
      followed by its answer paragraphs;
    * a bold question answered in the same paragraph or list item (the desk questions): the answer is folded.
    """
    # a label run into its problem's paragraph ("... and J1 = 0. *Solution.* ...") starts a paragraph of its own
    page = re.sub(r"(?<=[^>\s])\s*(<(em|strong)>\s*(?:Solution|Answer)[.:]?\s*</\2>)", r"</p>\n<p>\1", page)
    page = re.sub(r"<p>\s*</p>\n?", "", page)
    starts = [m.start() for m in _SOLUTION.finditer(page)]
    if starts:
        for start in reversed(starts):
            label = "解答" if re.match(r"<p><(?:em|strong|i|b)>\s*解", page[start:]) else "Solution"
            page = _wrap(page, start, _block_end(page, start), label)
        return page
    block = re.search(r"<h[3-6][^>]*>\s*(?:Solutions|Answers|Worked solutions|解答)[^<]*</h[3-6]>|"
                      r"<p><strong>\s*(?:Solutions|Answers|解答)[^<]*</strong>\s*</p>", page)
    if block:
        return page[:block.end()] + '<details class="sol"><summary>Solutions</summary>' + page[block.end():] + "</details>\n"
    items = [(a, b) for a, b in _items(page) if _statement_then_more(page[a:b])]
    if items:
        for a, b in reversed(items):
            cut = page.index("</p>", a) + 4
            if page[cut:b].strip():
                page = _wrap(page, cut, b, "Solution")
        return page
    # "**1.** *the question*": a bold number, then the question in italics (or ending in a question mark)
    heads = [m.start() for m in re.finditer(r"<p><strong>[^<]{0,80}</strong>\s*<em>|<p><strong>[^<]{0,200}\?</strong>", page)]
    if len(heads) >= 2 and _depth_zero(page, heads):
        for i in reversed(range(len(heads))):
            cut = page.index("</p>", heads[i]) + 4
            end = heads[i + 1] if i + 1 < len(heads) else _block_end(page, cut - 4)
            if page[cut:end].strip():
                page = _wrap(page, cut, end, "Solution")
        if '<details class="sol">' in page:
            return page
    # "**A question?** Its answer.": a bold question, answered in the same paragraph or list item
    asked = list(re.finditer(r"(?:<li>|<p>)\s*<strong>[^<]{3,240}\?</strong>\s*(?=\S)", page))
    if len(asked) >= 2:
        for m in reversed(asked):
            close = page.index("</li>" if m.group(0).startswith("<li>") else "</p>", m.end())
            answer = page[m.end():close]
            if answer.strip() and not re.search(r"<(li|ul|ol|p)\b", answer):  # a nested block: leave it open
                page = page[:m.end()] + '<details class="sol"><summary>Answer</summary>' + answer + "</details>" + page[close:]
    return page


def _statement_then_more(item: str) -> bool:
    """A list item that opens with a paragraph and has more blocks after it (the answer)."""
    item = item.strip()
    if not item.startswith("<p>") or "</p>" not in item:
        return False
    return bool(re.match(r"\s*<(p|ul|ol|pre|div|table|blockquote)\b", item.split("</p>", 1)[1]))


def _depth_zero(page: str, positions: list) -> bool:
    """Whether every position is outside any list, table or quotation."""
    for pos in positions:
        before = page[:pos]
        for tag in ("li", "table", "blockquote"):
            if before.count(f"<{tag}") > before.count(f"</{tag}>"):
                return False
    return True


# ---------------------------------------------------------------------------
# Lecture notes: a part's chapters as text (tools/lecture_text.py), shared by both builders
# ---------------------------------------------------------------------------
def readme_chapter_table(readme: Path) -> dict:
    """{chapter number: [(column, cell markdown)]} from the README's chapter table (a table whose first column is
    the chapter's number, 0 for the cold open), leaving out the column that repeats the chapter's title."""
    out, header = {}, None
    for line in readme.read_text().splitlines():
        if not line.startswith("|"):
            header = None if not line.strip() else header
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            if not re.fullmatch(r"#|ch\.?|chapter|no\.?|scene", header[0].strip("*` ").lower()):
                header = []
            continue
        if not header or re.fullmatch(r"[-:\s|]+", line.strip("|")) or len(cells) < 3:
            continue
        m = re.fullmatch(r"(\d+)\.?", cells[0].strip("*` "))
        if not m:
            continue
        keep = [(h.strip("*` "), c) for h, c in zip(header[1:], cells[1:])
                if c and c not in ("—", "-", "–") and not re.fullmatch(r"chapter|title|scene|name|chapter title|chapter \(scene\)",
                                                                         h.strip("*` ").lower())]
        if keep:
            out.setdefault(int(m.group(1)), keep)
    return out


def contents_html(rows: list, tier_badge) -> str:
    """The contents list: rows of (label, title, minutes, tier or None, anchor).  ``tier_badge(tier)`` labels a level."""
    items = []
    for label, title, mins, tier, anchor in rows:
        attr = f' data-tier="{tier}"' if tier else ""
        badge_ = tier_badge(tier) if tier else "<span></span>"
        items.append(f'<li{attr}><span class="num">{label}</span><span class="title"><a href="#{anchor}">{esc(title)}</a>'
                     f'</span>{badge_}<span class="mins">{f"{mins:.0f} min" if mins >= 0.5 else ""}</span></li>')
    return f'<ol class="chapters">{"".join(items)}</ol>'


def lecture_html(chapters: list, tier_badge, unit: str = "part", numbers: dict | None = None,
                 base: Path = ROOT) -> str:
    """The lecture text: chapters of (label, title, minutes, tier or None, anchor, paragraphs).  ``numbers`` is the
    README's chapter table ({chapter number: [(column, markdown)]}), shown under the chapter it describes."""
    import lecture_text  # noqa: PLC0415  (tools/, beside this file)

    out, gaps = [], 0
    for i, (label, title, mins, tier, anchor, paras) in enumerate(chapters):
        gaps += sum(p.gaps for p in paras)
        key = 0 if i == 0 and not label.isdigit() else (int(label) if label.isdigit() else None)
        extra = ""
        if numbers and key is not None and key in numbers:
            cells = "; ".join(f"<b>{esc(h)}:</b> {inline_md(c, base)}" for h, c in numbers[key])
            extra = f'<p class="numbers">{cells}</p>'
        attr = f' data-tier="{tier}"' if tier else ""
        num = f'<span class="cn">{label}</span>' if label.isdigit() and not (i == 0 and label == "0") else ""
        head = (f'<h3>{num}{esc(title)}{tier_badge(tier) if tier else ""}'
                f'{f"<span class=mins>{mins:.0f} min</span>" if mins >= 0.5 else ""}</h3>')
        body = "".join(lecture_text.to_html(p) for p in paras) or "<p class=\"hint\">This chapter has no narration to read.</p>"
        out.append(f'<section class="chapter" id="{anchor}"{attr}>{head}{body}{extra}</section>')
    note = (f"The text of each chapter is the film's narration, as it is spoken, so you can read along or revise "
            f"without the film. The pictures are in the film.")
    if gaps:
        note += (' A dashed box <span class="val"></span> stands for a number the film computes when it is rendered '
                 '(hover over it to see what is computed); the README\'s figures for each chapter, where it lists them, '
                 'follow the chapter\'s text.')
    return f'<p class="note-box">{note}</p>' + "".join(out)


def inline_md(text: str, base: Path = ROOT) -> str:
    """One line of Markdown (a table cell) as inline HTML."""
    return re.sub(r"^<p>|</p>\s*$", "", md_to_html(text, base).strip())


_QA = re.compile(r"visual review|polish|validation|视觉审阅|首数据行|first-data-row|construction clarification|"
                 r"sequential|review status|build and qa|local verification|reproduce this review|"
                 r"reproduce the review|verification and rebuilding|build and review|build and verification|"
                 r"reproducibility status|sources and review status|来源与审阅状态|复现及验收|来源与检查|样本边界修正",
                 re.I)
_CJK = re.compile(r"[一-鿿]")
_KINDS = [  # (kind, title shown, pattern on the README's heading)
    ("chapters", "Chapter notes", r"^chapters?\b|^the \w+ chapters|^nineteen chapters|chapters and|各章|章节"),
    ("desk", "Desk questions, with solutions", r"desk|interview|交易台|面试|桌面"),
    ("problems", "Problems, with worked solutions",
     r"problem|exercise|solutions|advanced practice|pause-question|习题|题|解答|进阶|基础|资格"),
    ("research", "For the researcher", r"researcher|research:|research illustration|theorem|theory|写给研究者|研究|定理"),
    ("audit", "Textbook audit", r"textbook|教材|教科书"),
    ("papers", "Papers and sources", r"paper|reading|sources|references|primary|facts checked|阅读|来源|原始资料"),
    ("hands", "Labs, replays and simulations in the film", r"hands-on|labs, replays"),
    ("data", "Data, scope and reproducibility",
     r"data|reproduc|scope|interpretation|boundar|convention|evidence|limits|qualification|establish|"
     r"selected restored|measurement|mechanism|distinction|arithmetic|数据|范围|边界|口径|约定|复现|解释|科学|"
     r"机制|核算|限制|证据|定义|说明|输入"),
    ("build", "Build the film", r"^build|构建"),
]


def split_readme(n: int) -> dict:
    """A part's README as {"en": [(kind, title, heading, html)], "zh": [...], "intro": html}.  Headings that are
    QA logs of earlier review passes are left out (they are kept in docs/qa/, not in the course)."""
    path = QUANT / f"quant{n}" / "README.md"
    text = path.read_text()
    lines = text.splitlines()
    # blocks: (level, heading, body lines)
    blocks, cur = [], (0, "", [])
    fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,2}) +(.*)$", line)
        if m:
            blocks.append(cur)
            cur = (len(m.group(1)), m.group(2).strip(), [])
        else:
            cur[2].append(line)
    blocks.append(cur)
    out = {"en": [], "zh": [], "intro": ""}
    lang, seen_h1 = "en", False
    for level, heading, body in blocks:
        body_text = "\n".join(body).strip()
        if level == 0:
            continue
        mixed = bool(re.search(r"[A-Za-z]{4,}.*/.*[\u4e00-\u9fff]", heading))  # "English / 中文": kept with the English
        zh_heading = bool(_CJK.search(heading)) and not mixed
        if level == 1:
            if seen_h1 and (zh_heading or lang == "zh"):
                lang = "zh"
            if not seen_h1:
                out["intro"] = md_to_html(body_text, path.parent) if body_text else ""
            elif body_text and lang == "zh":
                out["zh"].append(("intro", "导言", heading, md_to_html(body_text, path.parent)))
            seen_h1 = True
            continue
        if zh_heading:
            lang = "zh"
        if _QA.search(heading) or not body_text:
            continue
        sec_lang = "zh" if zh_heading else "en"  # an English heading after the Chinese half is still English
        kind, title = "data", "Notes"
        for k, t, pat in _KINDS:
            if re.search(pat, heading, re.I):
                kind, title = k, t
                break
        out[sec_lang].append((kind, title, heading, md_to_html(body_text, path.parent)))
    return out


def reading_for(n: int) -> str:
    text = (QUANT / "READING.md").read_text()
    m = re.search(rf"^### Part {n} · .*?$\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return md_to_html(m.group(1).strip(), QUANT) if m else ""


# ---------------------------------------------------------------------------
# Page pieces
# ---------------------------------------------------------------------------
def shell(title: str, body: str, depth: int, description: str = "", scripts: str = "") -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description or title)}">
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<link rel="stylesheet" href="{up}assets/course.css">
</head>
<body>
<header class="top">
  <a class="brand" href="{up}quant/index.html"><span class="mark">Q</span>Quant, Built</a>
  <nav>
    <a href="{up}quant/index.html#map">Course map</a>
    <a href="{up}quant/tracks.html">Tracks</a>
    <a href="{up}quant/labs.html">Labs</a>
    <a href="{up}quant/reading.html">Reading</a>
    <a href="{up}index.html">All courses</a>
    <a href="{REPO}/tree/main/videos/quant">GitHub</a>
  </nav>
</header>
<main>
{body}
</main>
<footer>
  <p><em>An education in methods, not investment advice.</em> Firms are described only from the public record;
  allegations are labelled as allegations. Simulated markets are labelled simulated.</p>
  <p>Built from <a href="{REPO}">the repository</a> by <code>tools/course_site.py</code>: the films, the House
  library and these pages come from the same source.</p>
</footer>
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"></script>
<script defer src="{up}assets/course.js"></script>
{scripts}
</body>
</html>
"""


def badge(tier: str) -> str:
    return f'<span class="tier tier-{tier if tier != "*" else "all"}">{TIER_NAME[tier]}</span>'


def part_link(n: int, text: str | None = None) -> str:
    return f'<a href="part{n:02d}.html">{esc(text or f"Part {n}: {course.title(n)}")}</a>'


def lab_block(n: int, out_dir: Path, run_labs: bool) -> str:
    module = labs.load(n)
    src = labs.source(n)
    cache = out_dir / "quant" / "labs" / f"lab{n:02d}.json"
    png = out_dir / "quant" / "labs" / f"lab{n:02d}.png"
    if run_labs or not (cache.exists() and png.exists()):
        start = time.time()
        lab = module.run(seed=0)
        labs.save(lab, png)
        cache.write_text(json.dumps({"table": lab.table(), "seconds": round(time.time() - start, 1)}))
    info = json.loads(cache.read_text())
    (out_dir / "quant" / "labs" / f"lab{n:02d}.py").write_text(src)
    tasks = "".join(f"<li>{esc(t)}</li>" for t in module.TASKS)
    return f"""
<section id="lab" class="lab">
  <h2>Lab {n} · {esc(module.TITLE)}</h2>
  <p>{esc(module.GOAL)}</p>
  <figure><img src="labs/lab{n:02d}.png" alt="Figure produced by Lab {n}: {esc(module.TITLE)}" loading="lazy">
  <figcaption>Produced by the lab below, seed 0, in {info['seconds']:.1f} s. Simulated data.</figcaption></figure>
  <div class="run"><code>python -m videos.quant.labs {n}</code>
  <span>needs numpy, scipy, matplotlib, numba · <a href="labs/lab{n:02d}.py" download>download lab{n:02d}.py</a> ·
  <a href="{BLOB}/videos/quant/labs/lab{n:02d}.py">source on GitHub</a></span></div>
  <pre class="output"><code>{esc(info['table'])}</code></pre>
  <details><summary>The code ({len(src.splitlines())} lines; it asserts its own result)</summary>
  <pre class="code"><code>{esc(src)}</code></pre></details>
  <h3>Now change it</h3>
  <ol class="tasks">{tasks}</ol>
</section>"""


def track_buttons() -> str:
    buttons = ['<button class="on" data-track="">All chapters</button>']
    for key, (name, _) in course.TRACKS.items():
        buttons.append(f'<button data-track="{key}" data-tiers="{course.TRACK_TIERS[key]}">{name} track</button>')
    return '<div class="track-buttons" role="group" aria-label="Show a track">' + "".join(buttons) + "</div>"


def track_minutes(n: int, minutes: list) -> dict:
    out = {}
    for key, tiers in course.TRACK_TIERS.items():
        out[key] = sum(m for (_, _, _, tier), m in zip(course.chapters(n), minutes) if tier in tiers or tier == "*")
    return out


def readme_sections(sections: list, order: tuple, open_first: bool = False) -> str:
    out = []
    by_kind = {}
    for kind, title, heading, body in sections:
        by_kind.setdefault(kind, []).append((title, heading, body))
    first = True
    for kind in order:
        for title, heading, body in by_kind.get(kind, []):
            op = " open" if (open_first and first) else ""
            first = False
            orig = "" if heading.lower().startswith(title.lower()[:14]) else f'<span class="orig">{esc(heading)}</span>'
            out.append(f'<details class="notes notes-{kind}"{op}><summary><span class="kind">{esc(title)}</span>'
                       f'{orig}</summary><div class="md">{body}</div></details>')
    return "".join(out)


def open_sections(sections: list, order: tuple, titled: bool = True) -> str:
    """README sections shown open, as the notes' back matter; problem sets get folded solutions."""
    chosen = [x for kind in order for x in sections if x[0] == kind]
    out = []
    for kind, title, heading, body in chosen:
        orig = "" if heading.lower().startswith(title.lower()[:14]) else f'<p class="orig">{esc(heading)}</p>'
        head = f"<h3>{esc(title)}</h3>" if titled or len(chosen) > 1 else ""
        body = fold_solutions(body) if kind in ("problems", "desk") else body
        out.append(f'<div class="sect sect-{kind}">{head}{orig}<div class="md">{body}</div></div>')
    return "".join(out)


def lecture_chapters(n: int, minutes: list) -> list:
    """[(label, title, minutes, tier, anchor, paragraphs)] of Part ``n``: each chapter with its narration as text."""
    import lecture_text  # noqa: PLC0415

    scenes = course.manifest(n)[1]
    out = []
    for (i, number, title, tier), mins, (module, cls, full) in zip(course.chapters(n), minutes, scenes):
        paras = lecture_text.chapter_text(QUANT / f"quant{n}" / f"{module}.py", cls, full)
        out.append(("" if number is None else str(number), title, mins, tier, f"ch{i}", paras))
    return out


def part_page(n: int, out_dir: Path, run_labs: bool) -> tuple[str, dict]:
    p = course.PARTS[n]
    act = course.act_of(n)
    name = course.title(n)
    minutes = chapter_minutes(n)
    total = sum(minutes)
    tm = track_minutes(n, minutes)
    readme = split_readme(n)
    prereq = ", ".join(part_link(q, f"Part {q}") for q in p.prereq) or "none"
    objectives = "".join(
        f'<div class="obj obj-{k}"><h3>{badge(k)}</h3><ul>' + "".join(f"<li>{tex_inline(o)}</li>" for o in p.objectives[k])
        + "</ul></div>" for k in "UMDI")
    results = "".join(f'<div class="result"><span class="name">{esc(name_)}</span><span class="tex">\\[{esc(tex)}\\]</span></div>'
                      for name_, tex in p.results)
    also = "".join(f'<li><a href="{BLOB}/{path}">{esc(label)}</a></li>' for label, path in p.also)
    track_line = " · ".join(f"{course.TRACKS[k][0]} {fmt_minutes(tm[k])}" for k in "UMDI")
    widget = (f'<section id="try" class="try"><h2>Try it</h2><div class="widget" data-widget="{p.widget}">'
              f'<noscript>This interactive needs JavaScript.</noscript></div></section>') if p.widget else ""
    lecture = lecture_chapters(n, minutes)
    contents = contents_html([x[:5] for x in lecture], badge)
    text = lecture_html(lecture, badge, "part", readme_chapter_table(QUANT / f"quant{n}" / "README.md"), QUANT / f"quant{n}")
    problems = open_sections(readme["en"], ("desk", "problems"), titled=False)
    research = open_sections(readme["en"], ("research",))
    folded = readme_sections(readme["en"], ("hands", "audit", "data", "chapters"))
    zh = fold_solutions(readme_sections(readme["zh"], ("intro", "chapters", "desk", "problems", "research", "audit",
                                                       "papers", "data", "hands", "build")))
    papers = reading_for(n)
    extra_papers = open_sections(readme["en"], ("papers",))
    prev_ = f'<a class="prev" href="part{n - 1:02d}.html">← Part {n - 1}: {esc(course.title(n - 1))}</a>' if n > 1 else "<span></span>"
    next_ = (f'<a class="next" href="part{n + 1:02d}.html">Part {n + 1}: {esc(course.title(n + 1))} →</a>'
             if n < course.N_PARTS else '<a class="next" href="index.html">Back to the course map →</a>')
    jumps = [("#lecture", "Lecture"), ("#results", "Key results"), ("#try", "Try it") if widget else None, ("#lab", "Lab"),
             ("#problems", "Problems") if problems else None, ("#reading", "Reading"), ("#zh", "中文") if zh else None,
             ("#build", "Build the film")]
    jump = " · ".join(f'<a href="{h}">{t}</a>' for h, t in filter(None, jumps))
    body = f"""
<article class="part" data-part="{n}">
<p class="crumb"><a href="index.html#map">Act {act[0]} · {esc(act[1])}</a></p>
<span class="partno">Part {n} of {course.N_PARTS}</span><h1>{esc(name)}</h1>
<p class="meta">{badge(p.level)}<span>starts at this level</span><span class="dot">{fmt_minutes(total)} of film</span>
<span class="dot">{len(minutes)} chapters</span><span class="dot">prerequisites: {prereq}</span></p>
<blockquote class="question">{tex_inline(p.question)}</blockquote>
<p class="story">{tex_inline(p.story)}</p>
<p class="outside"><strong>What you need.</strong> {tex_inline(p.outside)}</p>
<section id="objectives"><h2>What you will be able to do</h2><div class="objectives">{objectives}</div></section>
<section id="chapters"><h2>Contents</h2>
<p class="hint">Each chapter has a home level. Choose a track to see what to read and watch: {track_line}.</p>
{track_buttons()}
{contents}
<p class="hint">Also on this page: {jump}.</p>
</section>
<section id="lecture" class="lecture"><h2>Lecture</h2>
{text}
<p class="handoff"><strong>Where it goes next.</strong> {tex_inline(p.handoff)}</p>
</section>
<section id="results"><h2>Key results</h2><p class="hint">The part's results in one place, for revision.</p>
<div class="results">{results}</div></section>
{widget}
{lab_block(n, out_dir, run_labs)}
{f'<section id="problems"><h2>Problems, with solutions</h2><p class="hint">Try each problem before opening its solution; the last two of each set are at qualifying-exam level.</p>{problems}</section>' if problems else ''}
<section id="reading"><h2>Reading and notes</h2>
<div class="sect"><h3>The part's papers</h3><p class="orig">from READING.md</p><div class="md">{papers}</div></div>
{extra_papers}
{research}
{folded}
{f'<h3>Companion films in this repository</h3><ul>{also}</ul>' if also else ''}
</section>
{f'<section id="zh" lang="zh"><h2>中文讲义</h2><p class="hint">本讲的中文说明、交易台问题与习题解答（与英文版对应）。</p>{zh}</section>' if zh else ''}
<section id="build"><h2>Build the film</h2>
<pre class="code"><code>python -m videos.quant.quant{n}.compute      # the part's numbers, into .cache/quant{n}
python tools/make.py quant{n}                # the narrated film, English and Chinese
EXPLAINER_TTS=silent python tools/qa_scene.py quant{n} Hook   # one chapter, silent, with a contact sheet</code></pre>
<p class="hint">Scenes: <a href="{REPO}/tree/main/videos/quant/quant{n}">videos/quant/quant{n}</a>.
Setup: <a href="index.html#setup">see the course page</a>. Source of these notes: the part's
<a href="{BLOB}/videos/quant/quant{n}/README.md">README</a> and the scenes' narration.</p>
</section>
<nav class="pager">{prev_}{next_}</nav>
</article>"""
    info = {"minutes": total, "track_minutes": tm, "chapters": len(minutes)}
    page = shell(f"Part {n}: {name} · Quant, Built", body, 1, p.question,
                 '<script defer src="../assets/widgets.js"></script>')
    return page, info


# ---------------------------------------------------------------------------
# Course pages
# ---------------------------------------------------------------------------
def index_page(info: dict) -> str:
    total = sum(v["minutes"] for v in info.values())
    cards = []
    for roman, act_name, (a, b), blurb in course.ACTS:
        rows = []
        for n in range(a, b + 1):
            p = course.PARTS[n]
            tiers = {t for _, _, _, t in course.chapters(n)}
            dots = "".join(f'<i class="d d-{t}" title="{TIER_NAME[t]} chapters"></i>' for t in "UMDI" if t in tiers)
            rows.append(f'<a class="pcard" href="part{n:02d}.html" data-level="{p.level}" data-tiers="{"".join(sorted(tiers - {"*"}))}">'
                        f'<span class="n">{n}</span><span class="t">{esc(course.title(n))}</span>'
                        f'<span class="q">{tex_inline(p.question)}</span>'
                        f'<span class="foot">{badge(p.level)}<span class="dots">{dots}</span>'
                        f'<span class="m">{info[n]["minutes"]:.0f} min</span></span></a>')
        label = f"Act {roman}" if roman != "Finale" else "Finale"
        cards.append(f'<section class="act"><h3><span>{label}</span>{esc(act_name)}</h3><p>{esc(blurb)}</p>'
                     f'<div class="pgrid">{"".join(rows)}</div></section>')
    tracks = []
    for key, (name, blurb) in course.TRACKS.items():
        hours = sum(v["track_minutes"][key] for n, v in info.items() if n in course.track_parts(key)) / 60
        tracks.append(f'<a class="tcard tcard-{key}" href="tracks.html#{key}"><h3>{name}</h3><p>{esc(blurb)}</p>'
                      f'<span>{len(course.track_parts(key))} parts · about {hours:.0f} hours</span></a>')
    body = f"""
<section class="hero">
  <p class="kicker">A forty-three-part course in quantitative finance, in film and in code</p>
  <h1>Quant, Built</h1>
  <p class="lede">In 1900 Louis Bachelier wrote that the expectation of the speculator is zero. Pricing says that
  is exactly right, once you discount and change measure. Investing says it is not quite right: someone is paid
  to take the other side. The course is the argument between those two sentences, from a first random walk to
  the research frontier, and it builds its own quant firm along the way.</p>
  <div class="stats"><span><b>{course.N_PARTS}</b> parts</span><span><b>{total / 60:.0f}</b> hours of lectures</span>
  <span><b>{sum(v['chapters'] for v in info.values())}</b> chapters</span><span><b>{course.N_PARTS}</b> runnable labs</span>
  <span><b>4</b> tracks</span></div>
</section>

<section id="map"><h2>Contents</h2>
<p class="hint">Each part opens as lecture notes: the text of every chapter, its key results, an interactive,
a lab, problems with solutions and its reading. The label is the level at which a part can first be followed.</p>
<div class="track-buttons map-filter" role="group" aria-label="Filter the map by track">
<button class="on" data-level="">Everything</button><button data-level="U">Open to undergraduates</button>
<button data-level="M">Master's and up</button></div>
{''.join(cards)}
</section>


<section id="how"><h2>How to use the course</h2>
<div class="steps">
  <div><b>1 · Read or watch</b><p>Each part is a 50-65 minute lecture built in code: derivations in full, models
  trained on screen, every number computed or cited. Its page carries the lecture as text, chapter by chapter, so
  you can follow along with the film or read it on its own.</p></div>
  <div><b>2 · Run the lab</b><p>One lab per part, on the series' own library, the House. Seeded, a few seconds
  each, no data to download. Each ends with three things to change.</p></div>
  <div><b>3 · Work the problems</b><p>Desk questions in the trading-interview tradition and a tiered problem
  set per part, the last two at qualifying-exam level, all with worked solutions.</p></div>
  <div><b>4 · Read on</b><p>Every part lists its textbook sections and papers, and what the literature has not
  settled.</p></div>
</div></section>

<section id="tracks"><h2>Four tracks through the same material</h2>
<p class="hint">Every chapter has a home level. A track is the set of chapters to watch at that level; on each
part's page a button shows them.</p>
<div class="tgrid">{''.join(tracks)}</div></section>

<section id="devices"><h2>What runs through all of it</h2>
<div class="steps">
  <div><b>The House</b><p>The series' own quant firm, built desk by desk: <a href="{REPO}/tree/main/explainer/quant/house">
  about fifty tested modules</a> in numpy and scipy, from Black-Scholes to a limit-order-book simulator. The labs
  call it; so do the films.</p></div>
  <div><b>P and Q</b><p>Every result says which measure it lives under. Prices and implied quantities are Q;
  forecasts, premia and realized quantities are P.</p></div>
  <div><b>The evaluation protocol</b><p>Research uses data to the end of 2020. A strategy is registered before
  a fresh test, with its costs and its count of trials; the course teaches the protocol and how little five
  years can prove.</p></div>
  <div><b>Crisis files and firm files</b><p>Each idea is shown where it broke (1987, 1998, 2008, 2020, 2022) and
  in the hands of the firms whose business it is, from the public record.</p></div>
</div></section>

<section id="picture"><h2>The course in one picture</h2>
<div class="hero-widget widget" data-widget="hero" aria-label="Simulated price paths under two measures"></div></section>

<section id="setup"><h2>Setup</h2>
<div class="cols"><div><h3>Run the labs (two minutes)</h3>
<pre class="code"><code>git clone {REPO}.git
cd explainer-videos
pip install numpy scipy matplotlib numba
python -m videos.quant.labs 10          # Lab 10: delta hedging
python -m videos.quant.labs --all       # all forty-three</code></pre></div>
<div><h3>Build the films</h3>
<pre class="code"><code>bash tools/setup_linux.sh &amp;&amp; source .venv/bin/activate
python -m explainer.quant.data          # public market data, checksummed
python -m videos.quant.quant10.compute  # Part 10's numbers
python tools/make.py quant10            # the narrated film</code></pre></div></div>
<p class="hint">The plan of record is <a href="{BLOB}/videos/quant/SYLLABUS.md">SYLLABUS.md</a>; the textbook
coverage maps and every part's paper list are on the <a href="reading.html">reading page</a>. The films are in
English and Chinese; each part's page carries its Chinese notes.</p></section>
"""
    return shell("Quant, Built: a course in quantitative finance", body, 1,
                 "A forty-three-part course in quantitative finance, from a first random walk to the research "
                 "frontier, with a runnable lab for every part.", '<script defer src="../assets/widgets.js"></script>')


def tracks_page(info: dict) -> str:
    out = []
    for key, (name, blurb) in course.TRACKS.items():
        tiers = course.TRACK_TIERS[key]
        rows, hours = [], 0.0
        for n in course.track_parts(key):
            minutes = chapter_minutes(n)
            watch = [(c, m) for c, m in zip(course.chapters(n), minutes) if c[3] in tiers and c[3] != "*"]
            own = [c for c, _ in watch if c[3] == key] if key != "M" else [c for c, _ in watch]
            if not own:
                continue
            mins = sum(m for _, m in watch)
            hours += mins / 60
            names = "; ".join(esc(c[2]) for c in (own if key in "DI" else [c for c, _ in watch])[:9])
            more = len(watch) - 9 if key not in "DI" and len(watch) > 9 else 0
            goal = tex_inline(course.PARTS[n].objectives[key][0])
            rows.append(f'<tr><td class="n">{n}</td><td>{part_link(n, course.title(n))}<span class="goal">{goal}</span></td>'
                        f'<td class="ch">{names}{f" and {more} more" if more else ""}</td><td class="m">{mins:.0f} min</td></tr>')
        intro = {
            "U": "For a student with calculus, linear algebra and a first probability course. Twenty-eight parts "
                 "open at this level; in each, watch the chapters marked Undergraduate, run the lab, and do the "
                 "first problems of the set. The remaining fifteen parts become accessible after the toolkit "
                 "(Parts 4-8).",
            "M": "The whole course at the level of a master's in financial engineering: every numbered chapter, "
                 "every lab with its three extensions, the desk questions and the first ten problems of each set.",
            "D": "On top of the master's track: each part's research chapter (its central theorem in the "
                 "generality of the literature, proved and then checked by simulation), its frontier chapter, the "
                 "two qualifying-exam problems, and the 'For the researcher' notes with open problems.",
            "I": "For practitioners and interview preparation: the undergraduate core of each part, then how it is "
                 "used (industry chapters), where it failed (crisis files) and the House's rule; the desk questions; "
                 "and the labs, which are the House's production code in miniature.",
        }[key]
        out.append(f'<section id="{key}" class="track track-{key}"><h2>{badge(key)} {name} track</h2><p>{esc(blurb)}</p>'
                   f'<p>{esc(intro)}</p><p class="hint">{len(rows)} parts · about {hours:.0f} hours of film.</p>'
                   f'<div class="table-wrap"><table class="plan"><thead><tr><th>Part</th><th>What you take from it</th>'
                   f'<th>{"Chapters of this track" if key in "DI" else "Chapters to watch"}</th><th>Time</th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table></div></section>')
    body = ('<article class="doc"><h1>Tracks</h1><p class="lede">One course, four ways through it. Each part\'s page '
            'has the same buttons, so you can switch level chapter by chapter.</p>'
            '<p class="jump">' + " · ".join(f'<a href="#{k}">{v[0]}</a>' for k, v in course.TRACKS.items()) + "</p>"
            + "".join(out) + "</article>")
    return shell("Tracks · Quant, Built", body, 1, "Undergraduate, master's, PhD and industry tracks through Quant, Built.")


def labs_page() -> str:
    cards = []
    for n in range(1, course.N_PARTS + 1):
        module = labs.load(n)
        cards.append(f'<a class="lcard" href="part{n:02d}.html#lab"><img src="labs/lab{n:02d}.png" alt="" loading="lazy">'
                     f'<span class="n">Lab {n} · {esc(course.title(n))}</span><span class="t">{esc(module.TITLE)}</span></a>')
    body = f"""<article class="doc"><h1>Labs</h1>
<p class="lede">One lab per part, written on the House library. Each is seeded, runs in seconds on simulated
data, checks its own result against the theory it illustrates, and ends with three things to change.</p>
<pre class="code"><code>pip install numpy scipy matplotlib numba
python -m videos.quant.labs --list
python -m videos.quant.labs 26 --show
python -m pytest -q tests/test_quant_labs.py</code></pre>
<div class="lgrid">{''.join(cards)}</div></article>"""
    return shell("Labs · Quant, Built", body, 1, "Forty-three runnable labs on the House library.")


def doc_page(title: str, source: Path, lede: str) -> str:
    body = (f'<article class="doc"><h1>{esc(title)}</h1><p class="lede">{esc(lede)}</p>'
            f'<div class="md long">{md_to_html(source.read_text().split(chr(10), 1)[1], source.parent)}</div></article>')
    return shell(f"{title} · Quant, Built", body, 1, lede)


def write_assets(out: Path) -> None:
    """The stylesheet, the script and the interactives, shared by every course on the site."""
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for f in ASSETS.iterdir():
        if f.is_file():
            shutil.copy(f, out / "assets" / f.name)
    # the interactives: one file per act in the source, one file on the site
    (out / "assets" / "widgets.js").write_text("\n".join(f.read_text() for f in sorted((ASSETS / "widgets").glob("*.js"))))
    (out / ".nojekyll").write_text("")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "_site"))
    ap.add_argument("--no-labs", action="store_true", help="do not rerun labs whose figure and output already exist")
    ap.add_argument("--parts", nargs="*", type=int, help="only rebuild these parts' pages")
    ap.add_argument("--quant-only", action="store_true",
                    help="skip the other courses and the landing page (tools/series_site.py)")
    args = ap.parse_args()
    out = Path(args.out)
    (out / "quant" / "labs").mkdir(parents=True, exist_ok=True)
    write_assets(out)
    info, start = {}, time.time()
    wanted = set(args.parts or range(1, course.N_PARTS + 1))
    for n in range(1, course.N_PARTS + 1):
        if n in wanted:
            page, info[n] = part_page(n, out, run_labs=not args.no_labs)
            (out / "quant" / f"part{n:02d}.html").write_text(page)
            print(f"part {n:>2}  {info[n]['minutes']:5.1f} min  {info[n]['chapters']} chapters", flush=True)
        else:
            minutes = chapter_minutes(n)
            info[n] = {"minutes": sum(minutes), "track_minutes": track_minutes(n, minutes), "chapters": len(minutes)}
    (out / "quant" / "index.html").write_text(index_page(info))
    (out / "quant" / "tracks.html").write_text(tracks_page(info))
    (out / "quant" / "labs.html").write_text(labs_page())
    (out / "quant" / "reading.html").write_text(doc_page(
        "Reading", QUANT / "READING.md", "The textbooks the course covers and where, the industry and history "
                                         "library, and every part's papers."))
    (out / "quant" / "syllabus.html").write_text(doc_page(
        "Syllabus", QUANT / "SYLLABUS.md", "The plan of record: the standard every part meets, the devices, the "
                                           "model zoo, the data, and all 43 parts chapter by chapter."))
    print(f"site: {out}  ({time.time() - start:.0f} s)")
    if args.quant_only:
        if not (out / "index.html").exists():
            (out / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>Explainer Videos</title>'
                                            '<meta http-equiv="refresh" content="0; url=quant/index.html">'
                                            '<a href="quant/index.html">Quant, Built</a>\n')
        return
    import series_site  # the other courses, and the landing page that lists them all

    series_site.build(out)


if __name__ == "__main__":
    main()
