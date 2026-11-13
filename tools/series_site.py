#!/usr/bin/env python
"""Build the course sites of every series but *Quant, Built* (which has its own table, labs and interactives:
``tools/course_site.py``), and the landing page that lists them all, for GitHub Pages.

    python tools/series_site.py                       # -> _site/{ai,stats,cs,philosophy,psychology,analysis,films}/ and _site/index.html
    python tools/series_site.py --series stats cs     # only these courses (and the landing page)
    python tools/series_site.py --series ai --parts 5 # only these parts' pages (and the course pages)
    python tools/course_site.py                       # the whole site: Quant, Built, then everything here
    python -m http.server -d _site 8000               # look at it

Nothing here is written twice.  Every page is generated from what the series already holds:

* each part's ``manifest.py``: the chapters, in the film's order, with their length from the narration;
* each part's ``README.md``: what the part covers, chapter notes, what is computed, problems with solutions,
  the glossary, sources, and the Chinese edition (QA logs of review passes are left out);
* the series' ``README.md``: the story, the devices, and the table of parts (its acts and each part's row);
* the series' ``SYLLABUS.md``: each part's question, story and prerequisites where the syllabus states them, and
  its chapter-by-chapter plan;
* the series' course table, labs and interactives (``videos/coursekit``, ``videos/<series>/course``,
  ``videos/<series>/labs``): the level, story, objectives by track and key results of each part, which chapters
  each track watches, the lab (run here: its output and figure go on the page) and the interactive.

It needs numpy, scipy, matplotlib and markdown, not manim: no film is imported, only parsed.  ``--skip-labs``
leaves the labs off the pages for a quick structural build.
"""

from __future__ import annotations

import argparse
import functools
import json
import re
import runpy
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import course_site as quant_site  # noqa: E402  (the Markdown and math helpers, the stylesheet, KaTeX)
from videos import coursekit  # noqa: E402
from videos.coursekit import labs  # noqa: E402

esc, md_to_html = quant_site.esc, quant_site.md_to_html
REPO, BLOB, KATEX = quant_site.REPO, quant_site.BLOB, quant_site.KATEX
VIDEOS = ROOT / "videos"
WPM = 140  # the narrator's pace outside Quant, Built (tools/lecture_length.py)


# ---------------------------------------------------------------------------
# The courses
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Course:
    key: str  # the site folder, and (for a series) the folder under videos/
    name: str
    zh: str
    mark: str  # the letter in the top bar
    colors: tuple  # the mark's gradient
    kicker: str
    lede: str
    tagline: str  # one line, for the landing page
    prefix: str = ""  # parts are videos/<key>/<prefix>N; empty: a collection of films (``groups``)
    acts: tuple = ()  # ((label, name, (first, last), blurb), ...); empty: read from the README's table of parts
    groups: tuple = ()  # for a collection: ((series folder, name, blurb), ...)
    story: tuple = ()  # headings of the series README shown on the course page (matched by prefix)
    unit: str = "part"
    note: str = ""  # the footer's first line


COURSES = [
    Course(
        key="ai", prefix="ai", name="AI, Built", zh="人工智能，从零搭建", mark="A", colors=("#58a6ff", "#a78bfa"),
        kicker="A thirty-one-part course on how modern AI works and how it came to be",
        tagline="From Shannon's guessing game to transformers, diffusion, reinforcement learning, agents, and "
                "what we find inside the models.",
        lede="In 1951 Claude Shannon asked people to guess the next letter of an English text, and from their "
             "mistakes estimated how much information English carries. Every modern model plays a version of that "
             "game: language models guess the next token, diffusion models guess the noise, policies guess the "
             "next action. The course asks what you have to know to guess well, derives the mathematics on screen, "
             "trains its own small models, and tells the field's history as it goes.",
        story=("The story",),
        note="Every number on screen is computed by the part, measured on the machine that renders it, or cited. "
             "Schematics are labelled schematic and made-up examples illustrative.",
    ),
    Course(
        key="stats", prefix="stats", name="Statistics, Built", zh="统计学，从零搭建", mark="S",
        colors=("#2dd4bf", "#f7d154"),
        kicker="A sixty-five-part course in statistics, from a first course to a PhD",
        tagline="Five stages, from a histogram to a dissertation, with every method's promise measured on the "
                "Coverage Board.",
        lede="In 1662 John Graunt read half a century of London's Bills of Mortality and worked out things about "
             "the living city that nobody had counted. Statistics is his question made precise: what can we know "
             "about what we cannot see, from what we can, and how often will we be wrong? The course runs through "
             "five stages of a real degree, builds its own statistics library, and tests every promise a method "
             "makes on a simulated world whose truth is known.",
        story=("The story", "The five stages", "The devices that hold it together", "The Spiral", "Course map",
               "The bookshelf"),
        note="Simulated populations are labelled simulated; historical datasets are cited where they are used.",
    ),
    Course(
        key="cs", prefix="cs", name="Computer Science, Built", zh="计算机科学，从零搭建", mark="C",
        colors=("#4ade80", "#58a6ff"),
        kicker="A sixty-one-part course in computer science: a degree, industry practice, and a research tier",
        tagline="A computer built from one gate, then the languages, algorithms, limits, systems and networks "
                "stacked on top of it.",
        lede="Calculus is Latin for a small stone, the kind people once counted with. In 1928 Hilbert asked "
             "whether a mechanical procedure could decide every mathematical question; in 1936 Turing defined the "
             "machine that would have to do it and proved that none can. The machine outlived the question. The "
             "course follows it from paper to planet: it builds a computer, Pebble, from NAND gates, and each part "
             "adds a layer to the tower above it.",
        story=("The story",),
        note="Every number on screen is computed by the part, measured on the machine that renders it, or cited. "
             "Schematics are labelled schematic and made-up examples illustrative.",
    ),
    Course(
        key="philosophy", prefix="philosophy", name="Philosophy, Built", zh="哲学，从零搭建", mark="P",
        colors=("#e879f9", "#f7d154"),
        kicker="A forty-two-part course in philosophy, from the first arguments to aligned machines",
        tagline="Leibniz's 'let us calculate', taken literally: a reasoning machine built part by part, and the "
                "theorems that stop it.",
        lede="In 1685 Leibniz wrote that the way to settle a dispute would be to make reasoning as tangible as "
             "that of the mathematicians, so that we could simply say: let us calculate. The course takes him "
             "literally. Part by part it builds the calculator, a tested library called the Reasoner, and asks "
             "three questions each time: what does calculation make clear, where does it stop, and what is the "
             "price of each way out?",
        acts=(
            ("Prologue", "Calculemus", (1, 1), "What is an argument, and could reasoning be calculation?"),
            ("Act I", "The Machinery of Reason", (2, 5),
             "What follows from what? Propositional, first-order, modal and non-classical logic."),
            ("Act II", "The Limits of Reason", (6, 9),
             "What can't proof, computation or truth reach? Sets, Gödel and Turing, the liar, the philosophy of "
             "mathematics."),
            ("Act III", "Knowledge", (10, 14),
             "What can we know, and how much should we believe? Descartes to Kant, knowledge, common knowledge, "
             "credence, revision."),
            ("Act IV", "Science", (15, 19),
             "How does evidence become theory? Induction, statistics, causation, theories and reality, life."),
            ("Act V", "The World", (20, 26),
             "What is there, and how is it put together? Ontology, identity, possible worlds, God, laws and "
             "chance, space and time, the quantum."),
            ("Act VI", "Mind and Meaning", (27, 32),
             "How do words and minds reach the world? Sense and reference, meaning in use, phenomenology, mind, "
             "consciousness, free will."),
            ("Act VII", "Value", (33, 40),
             "What should we do, together? Choice, games, ethics, population ethics, metaethics, justice, social "
             "choice, beauty."),
            ("Finale", "The Reasoners We Build", (41, 42),
             "What do we want from the reasoners we build? Fair machines, aligned machines."),
        ),
        story=("The story", "Four devices hold it together"),
        note="Positions are attributed to the philosophers who hold them; survey figures are cited. Every worked "
             "model on screen is computed by the Reasoner.",
    ),
    Course(
        key="psychology", prefix="psych", name="Psychology, Built", zh="心理学，从零搭建", mark="Ψ",
        colors=("#fb7185", "#fbbf24"),
        kicker="A sixty-two-part course in psychology, from a first course to the research frontier: in production",
        tagline="Kant said the mind could never be measured. A model subject built part by part, an experiment on "
                "you in every part, and a ledger of what replicated.",
        lede="In 1786 Kant gave three reasons why psychology could never be a science: no mathematics, no "
             "experiment, and an observer who disturbs what is observed. In 1850 Fechner and Helmholtz took the "
             "wager. The course follows the reply. Each part measures a phenomenon, first on you; builds the "
             "mechanism as a model that runs, a faculty of a model subject called Psyche; and enters the finding "
             "in a ledger with what happened when someone ran it again. The plan is sixty-two parts; the parts "
             "listed here are the ones built so far.",
        story=("The story", "The devices that hold it together", "Four ways through it", "The acts"),
        note="Human data are white and the model orange on screen. Simulated participants are labelled simulated; "
             "historical data are cited where they are used; every finding carries its replication status.",
    ),
    Course(
        key="analysis", prefix="analysis", name="Analysis, Built", zh="数学分析，从零搭建", mark="∫",
        colors=("#fb923c", "#f7d154"),
        kicker="A ten-part course in real, complex and functional analysis",
        tagline="From the holes in the rational numbers to the spectral theorem, along the arc of Rudin's three "
                "textbooks.",
        lede="The rational numbers are dense and full of holes. Filling them gives the real line, and with it "
             "limits, continuity, the integral, measure, Hilbert space and, at the end, the spectral theorem. The "
             "course follows the arc of Walter Rudin's three textbooks, with every theorem proved on screen and "
             "every number the narration states computed and asserted.",
        acts=(
            ("Book I", "Principles of Mathematical Analysis", (1, 4),
             "The real numbers, limits, the Riemann-Stieltjes integral, uniform convergence, and calculus in "
             "many dimensions."),
            ("Book II", "Real and Complex Analysis", (5, 7),
             "Measure and the Lebesgue integral, the L^p spaces and Hilbert space, and complex analysis."),
            ("Book III", "Functional Analysis", (8, 10),
             "Banach spaces, distributions and the Fourier transform, Banach algebras and the spectral theorem."),
        ),
        note="Every number the narration states is computed by the part's compute.py and asserted.",
    ),
    Course(
        key="films", name="Single films", zh="单集", mark="F", colors=("#f87171", "#fbbf24"), unit="film",
        kicker="Thirteen lectures that stand on their own",
        tagline="Quantum mechanics, general relativity, Navier-Stokes, the Riemann hypothesis, stochastic "
                "calculus, how language models work and are trained, and how a trading system is built.",
        lede="Before the long courses there were single films, each a complete lecture on one subject: derived on "
             "screen, computed for real, and fact-checked against its sources. Several are the gentler first pass "
             "at material a course later treats in depth.",
        groups=(
            ("physics", "Physics", "Quantum mechanics and general relativity in two parts each, and the "
                                   "Navier-Stokes equations."),
            ("math", "Mathematics", "The Riemann hypothesis and stochastic calculus."),
            ("ml", "Machine learning", "How large language models work, how frontier models are trained, the "
                                       "open-weight architectures, and reinforcement learning for language "
                                       "models."),
            ("markets", "Markets", "A real-time trading system, and earnings against the cost of money."),
        ),
        note="Every number on screen is computed or cited; each film's page lists its fact-check notes and sources.",
    ),
]
BY_KEY = {c.key: c for c in COURSES}


@dataclass(frozen=True)
class Entry:
    """One part of a course (or one film of a collection)."""

    course: str
    n: int  # its number in the course, from 1
    video: str  # the video's name: ai5, quantum
    dir: Path
    title: str
    subtitle: str
    slug: str  # the page: part05, quantum


def _clean(cell: str) -> str:
    """A table cell or heading as plain text."""
    cell = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell)
    return re.sub(r"[*`]", "", cell).strip()


@functools.lru_cache(maxsize=None)
def manifest(path: Path) -> tuple:
    m = runpy.run_path(str(path / "manifest.py"))
    return m["TITLE"], tuple(tuple(s) for s in m["SCENES"])


@functools.lru_cache(maxsize=None)
def entries(key: str) -> tuple:
    c = BY_KEY[key]
    out = []
    if c.prefix:
        n = 1
        while (path := VIDEOS / c.key / f"{c.prefix}{n}").joinpath("manifest.py").exists():
            title = manifest(path)[0]
            m = re.search(r"Part \d+[,:]\s*(.*)$", title)
            out.append(Entry(key, n, path.name, path, m.group(1) if m else title, "", f"part{n:02d}"))
            n += 1
    else:
        for folder, _, _ in c.groups:
            for path in sorted(p.parent for p in (VIDEOS / folder).glob("*/manifest.py")):
                head, _, tail = manifest(path)[0].partition(": ")
                out.append(Entry(key, len(out) + 1, path.name, path, head, tail, path.name))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def series_readme(key: str) -> str:
    path = VIDEOS / key / "README.md"
    return path.read_text() if path.exists() else ""


@functools.lru_cache(maxsize=None)
def parts_table(key: str) -> tuple:
    """The series README's table of parts: (acts, rows).  ``acts`` is [(label, name, (first, last), blurb)] from
    its bold rows; ``rows`` maps a part's number to [(column, cell)] for the columns after the name."""
    text = series_readme(key)
    m = re.search(r"^## The parts\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    acts, rows, header = [], {}, []
    for line in (m.group(1).splitlines() if m else []):
        if not line.startswith("|"):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if not header:
            header = cells
        elif re.fullmatch(r"\d+", cells[0]):
            n = int(cells[0])
            rows[n] = [(h, x) for h, x in zip(header[2:], cells[2:]) if x]
            if acts:
                acts[-1][2][1] = n
                acts[-1][2][0] = acts[-1][2][0] or n
        elif cells[0].startswith("**"):
            label = _clean(cells[0])
            acts.append([label if label == "Finale" else f"Act {label}", _clean(cells[1]) if len(cells) > 1 else "",
                         [0, 0], ""])
    return tuple((a, b, tuple(r), d) for a, b, r, d in acts), rows


def acts(key: str) -> tuple:
    """[(label, name, (first, last), blurb)]: the course's acts, stages or groups, covering every entry."""
    c = BY_KEY[key]
    if c.groups:
        out, start = [], 1
        for folder, name, blurb in c.groups:
            count = sum(1 for e in entries(key) if e.dir.parent.name == folder)
            out.append(("", name, (start, start + count - 1), blurb))
            start += count
        return tuple(out)
    if c.acts:
        return c.acts
    found = parts_table(key)[0]
    if key == "stats":  # the README calls its acts stages
        found = tuple((label.replace("Act", "Stage"), *rest) for label, *rest in found)
    built = len(entries(key))  # a series in production: its README lists every planned part, the site the built ones
    return tuple((label, name, (a, min(b, built)), blurb) for label, name, (a, b), blurb in found if a <= built)


def act_of(e: Entry) -> tuple:
    for act in acts(e.course):
        if act[2][0] <= e.n <= act[2][1]:
            return act
    raise KeyError(f"{e.video} is in no act of {e.course}")


@functools.lru_cache(maxsize=None)
def syllabus_entry(key: str, n: int) -> dict:
    """What SYLLABUS.md says of Part ``n``: its subtitle, prerequisites, question, story, and the chapter plan."""
    path = VIDEOS / key / "SYLLABUS.md"
    out = {"subtitle": "", "prereq": "", "question": "", "story": "", "plan": ""}
    if not path.exists():
        return out
    m = re.search(rf"^(#{{3,4}}) Part {n} · (.*?)$\n(.*?)(?=^#{{1,4}} |\Z)", path.read_text(), re.S | re.M)
    if not m:
        return out
    sub = re.search(r"\)\s*:\s*(.+)$", m.group(2))
    out["subtitle"] = _clean(sub.group(1)) if sub else ""
    body = m.group(3).strip()
    # the head: the italic-labelled lines before the numbered chapters
    cut = re.search(r"^\s*$|^\d+\. ", body, re.M)
    head, rest = (body[:cut.start()], body[cut.start():]) if cut else (body, "")
    if "*Story:*" in head or "*Question:*" in head:
        for field, label in (("prereq", "Prerequisites"), ("question", "Question"), ("story", "Story")):
            f = re.search(rf"\*{label}:\*\s*(.*?)(?=\s*\*(?:Prerequisites|Question|Story):\*|\Z)", head, re.S)
            if f:
                out[field] = " ".join(f.group(1).split())
        out["prereq"] = out["prereq"].rstrip(".")
        out["question"] = out["question"][:1].upper() + out["question"][1:]
        body = rest.strip()
    out["plan"] = body
    return out


# ---------------------------------------------------------------------------
# A part's README
# ---------------------------------------------------------------------------
_QA = re.compile(
    r"\bqa\b|review|verif|validat|versioned|handoff|acceptance|integration|found and fixed|checkpoint|preflight|"
    r"reconciliation|contracts?$|^next$|input policy|cache requirements|audited|corrected numerical|"
    r"qualifications checked|shared caption|scene-source|baseline precision|candidate|bounded checks|provenance", re.I)
_BUILD = re.compile(r"^build|^run\b|^running|^reproduce", re.I)
_CJK = re.compile(r"[一-鿿]")
_KINDS = [  # (kind, title shown, pattern on the README's heading), first match wins
    ("build", "Build it", _BUILD.pattern),
    ("problems", "Problems, with solutions", r"problem|exercise|^solutions"),
    ("chapters", "Chapter notes", r"^chapters?\b|^outline|^scenes|follow the argument"),
    ("back", "Where it comes back", r"comes back|end of the series"),
    ("glossary", "Glossary", r"glossary"),
    ("sources", "Sources", r"source|reference|fact-check|primary|bookshelf|further study"),
    ("computed", "What is computed and built",
     r"comput|result|simulation|data|built|builds|measure|footage|coverage board|what is real|worked examples|"
     r"autodiff|toy comparisons|theorem|examples|numerical"),
    ("visual", "The visual language", r"visual language|color legend|pictures"),
]
_ORDER = ("chapters", "computed", "problems", "back", "glossary", "sources", "notes", "visual")
_ZH_TITLE = {"problems": "习题与解答", "chapters": "各章", "sources": "来源", "glossary": "术语"}


def _intro(text: str, base: Path) -> str:
    """The README's opening, without the paragraphs that are production status."""
    keep = [p for p in re.split(r"\n\s*\n", text.strip())
            if p.strip() and not re.search(r"\bQA\b|docs/qa/|narrated masters|\*\*Status|^Status:", p)]
    return md_to_html("\n\n".join(keep), base) if keep else ""


@functools.lru_cache(maxsize=None)
def split_readme(path: Path) -> dict:
    """A part's README as {"intro": html, "en": [(kind, title, heading, html)], "zh": [...]}.  Sections whose
    headings are QA logs of review passes are left out: they are kept in docs/qa/, not in the course."""
    blocks, cur, fence = [], ["", []], False
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,2}) +(.*)$", line)
        if m:
            blocks.append(cur)
            cur = [m.group(2).strip(), []]
        else:
            cur[1].append(line)
    blocks.append(cur)
    out = {"intro": "", "en": [], "zh": []}
    for i, (heading, body) in enumerate(blocks[1:]):
        text = "\n".join(body).strip()
        if i == 0:  # under the title
            out["intro"] = _intro(text, path.parent)
            continue
        plain = _clean(re.sub(r"\(.*?\)", "", heading))
        if not text or (_QA.search(plain) and not _BUILD.search(plain)):
            continue
        kind, title = "notes", "Notes"
        for k, t, pat in _KINDS:
            if re.search(pat, plain, re.I):
                kind, title = k, t
                break
        zh = bool(_CJK.search(heading)) and not re.search(r"[A-Za-z]{4,}.*/", heading)
        if zh:
            title = next((t for k, t in _ZH_TITLE.items() if k == kind), _clean(heading))
            kind = "problems" if re.search(r"题|解答", heading) else kind
        out["zh" if zh else "en"].append((kind, title, _clean(heading), md_to_html(text, path.parent)))
    return out


def sections(items: list, kinds: tuple) -> str:
    out = []
    for kind in kinds:
        for k, title, heading, body in items:
            if k != kind:
                continue
            plain = len(heading) <= 24 or heading.lower().startswith(title.lower()[:8])  # "Chapters", "Sources"
            orig = "" if plain else f'<span class="orig">{esc(heading)}</span>'
            out.append(f'<details class="notes notes-{kind}"><summary><span class="kind">{esc(title)}</span>'
                       f'{orig}</summary><div class="md">{body}</div></details>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Lengths
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def chapter_minutes(e: Entry) -> tuple:
    """Estimated minutes of each chapter, in the film's order, from the words it narrates."""
    out = []
    for module, cls, _ in manifest(e.dir)[1]:
        path = e.dir / f"{module}.py"
        out.append(quant_site.narration_words(path, cls) / WPM if path.exists() else 0.0)
    return tuple(out)


def fmt_minutes(m: float) -> str:
    return f"{m:.0f} min" if m < 90 else f"{m / 60:.1f} h"


def chapters(e: Entry) -> list:
    """[(label, title, minutes)]: the cold open has no number; numbered chapters keep the film's numbers."""
    out = []
    for i, ((_, _, title), mins) in enumerate(zip(manifest(e.dir)[1], chapter_minutes(e))):
        m = re.match(r"^(\d+)\.\s+(.*)$", title)
        label, name = (m.group(1), m.group(2)) if m else ("Cold open" if i == 0 else "", title)
        out.append((label, name, mins))
    return out


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def inline_md(text: str, base: Path = VIDEOS) -> str:
    """One line of Markdown (a table cell, a syllabus field); ``base`` is the folder its links are relative to."""
    return re.sub(r"^<p>|</p>$", "", md_to_html(text, base).strip())


def shell(c: Course | None, title: str, body: str, description: str, depth: int = 1, widgets: bool = False) -> str:
    up = "../" * depth
    scripts = f'<script defer src="{up}assets/widgets-{c.key}.js"></script>' if (c and widgets) else ""
    if c:
        syllabus = '<a href="syllabus.html">Syllabus</a>' if (VIDEOS / c.key / "SYLLABUS.md").exists() else ""
        source = f"{REPO}/tree/main/videos/{c.key}" if c.prefix else f"{REPO}/tree/main/videos"
        brand = (f'<a class="brand" href="index.html"><span class="mark" style="background:linear-gradient(135deg,'
                 f'{c.colors[0]},{c.colors[1]})">{esc(c.mark)}</span>{esc(c.name)}</a>')
        tracks = '<a href="tracks.html">Tracks</a><a href="labs.html">Labs</a>' if table(c.key) else ""
        nav = (f'<a href="index.html#map">Course map</a>{tracks}{syllabus}<a href="{up}index.html">All courses</a>'
               f'<a href="{source}">GitHub</a>')
        note = c.note
    else:
        brand = '<a class="brand" href="index.html"><span class="mark">E</span>Explainer Videos</a>'
        nav = f'<a href="#courses">Courses</a><a href="#build">Build</a><a href="{REPO}">GitHub</a>'
        note = "Every number on screen is computed or cited. Simulated data is labelled simulated."
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
  {brand}
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p>{esc(note)}</p>
  <p>Built from <a href="{REPO}">the repository</a> by <code>tools/series_site.py</code>: the films and these pages
  come from the same source.</p>
</footer>
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"></script>
<script defer src="{up}assets/course.js"></script>
{scripts}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# The course table, the labs and the interactives (videos/coursekit), where a series has them
# ---------------------------------------------------------------------------
def table(key: str):
    """The series' course table, or None (the films, or a series that has none yet)."""
    return coursekit.course(key) if BY_KEY[key].prefix else None


def entry_of(e: Entry):
    """The part's course entry, or None."""
    t = table(e.course)
    return t.parts.get(e.n) if t else None


def badge(key: str, tier: str) -> str:
    name = "All tracks" if tier == "*" else table(key).tracks[tier][0]
    return f'<span class="tier tier-{tier if tier != "*" else "all"}">{esc(name)}</span>'


def tiered_chapters(e: Entry) -> list:
    """[(label, title, minutes, tier)] for a part with a course entry."""
    return [(label, title, mins, tier) for (label, title, mins), (_, _, _, tier)
            in zip(chapters(e), table(e.course).chapters(e.n))]


def track_minutes(e: Entry) -> dict:
    return {k: sum(m for _, _, m, tier in tiered_chapters(e) if tier in tiers or tier == "*")
            for k, tiers in coursekit.TRACK_TIERS.items()}


def track_buttons(key: str) -> str:
    buttons = ['<button class="on" data-track="">All chapters</button>']
    for k, (name, _) in table(key).tracks.items():
        buttons.append(f'<button data-track="{k}" data-tiers="{coursekit.TRACK_TIERS[k]}">{esc(name)} track</button>')
    return '<div class="track-buttons" role="group" aria-label="Show a track">' + "".join(buttons) + "</div>"


def widget_source(key: str) -> str:
    return "\n".join(f.read_text() for f in sorted((VIDEOS / key / "course" / "site" / "widgets").glob("*.js")))


def widgets_defined(key: str) -> set:
    return set(re.findall(r"\bW\.([A-Za-z0-9_]+) = function", widget_source(key)))


def write_widgets(out: Path, key: str, only: set | None = None) -> None:
    """assets/widgets-<series>.js: the site's canvas library, the series' interactives, then the boot call.
    ``only``: just the files that define these widgets (a check of some parts must not depend on the others), and
    any file that defines none, which is code the interactives share (psychology's ``00_tasks.js``)."""
    core = quant_site.ASSETS / "widgets"
    source = widget_source(key)
    if only is not None:
        files = sorted((VIDEOS / key / "course" / "site" / "widgets").glob("*.js"))
        defined = [(t, set(re.findall(r"\bW\.([A-Za-z0-9_]+) = function", t))) for t in (f.read_text() for f in files)]
        source = "\n".join(t for t, names in defined if not names or names & only)
    (out / "assets" / f"widgets-{key}.js").write_text(
        "\n".join([(core / "00_core.js").read_text(), source, (core / "99_boot.js").read_text()]))


WITH_LABS = True  # --skip-labs: leave the labs off the pages (a quick structural build)


def has_lab(e: Entry) -> bool:
    return WITH_LABS and bool(BY_KEY[e.course].prefix) and labs.path(e.course, e.n).exists()


def lab_block(e: Entry, out: Path, run_labs: bool) -> str:
    key, n = e.course, e.n
    module = labs.load(key, n)
    src = labs.source(key, n)
    folder = out / key / "labs"
    folder.mkdir(parents=True, exist_ok=True)
    cache, png = folder / f"lab{n:02d}.json", folder / f"lab{n:02d}.png"
    if run_labs or not (cache.exists() and png.exists()):
        start = time.time()
        lab = module.run(seed=0)
        labs.save(lab, png)
        cache.write_text(json.dumps({"table": lab.table(), "seconds": round(time.time() - start, 1)}))
    info = json.loads(cache.read_text())
    (folder / f"lab{n:02d}.py").write_text(src)
    t = table(key)
    tasks = "".join(f"<li>{esc(x)}</li>" for x in module.TASKS)
    return f"""
<section id="lab" class="lab">
  <h2>Lab {n} · {esc(module.TITLE)}</h2>
  <p>{esc(module.GOAL)}</p>
  <figure><img src="labs/lab{n:02d}.png" alt="Figure produced by Lab {n}: {esc(module.TITLE)}" loading="lazy">
  <figcaption>Produced by the lab below, seed 0, in {info['seconds']:.1f} s.</figcaption></figure>
  <div class="run"><code>python -m videos.{key}.labs {n}</code>
  <span>needs {esc(t.lab_needs if t else 'numpy, scipy, matplotlib')} · <a href="labs/lab{n:02d}.py" download>download lab{n:02d}.py</a> ·
  <a href="{BLOB}/videos/{key}/labs/lab{n:02d}.py">source on GitHub</a></span></div>
  <pre class="output"><code>{esc(info['table'])}</code></pre>
  <details><summary>The code ({len(src.splitlines())} lines; it asserts its own result)</summary>
  <pre class="code"><code>{esc(src)}</code></pre></details>
  <h3>Now change it</h3>
  <ol class="tasks">{tasks}</ol>
</section>"""


def _breakable(tex: str) -> str:
    r"""Let KaTeX break a result's line after each \qquad or \quad, and between the words of a top-level
    \text{...} (which otherwise never wraps)."""
    tex = re.sub(r"\\(q?quad)(?![A-Za-z])", r"\\\1\\allowbreak ", tex)
    out, depth, i = [], 0, 0
    while i < len(tex):
        if depth == 0 and tex.startswith(r"\text{", i):
            end = tex.find("}", i + 6)
            words = tex[i + 6:end]
            if end > 0 and not re.search(r"[{\\$]", words) and " " in words.strip():
                pieces = re.findall(r"\s*\S+\s*", words)
                out.append(r"\allowbreak ".join(rf"\text{{{w}}}" for w in pieces))
                i = end + 1
                continue
        c = tex[i]
        if c == "\\" and i + 1 < len(tex):  # an escaped brace is not a group
            out.append(tex[i:i + 2])
            i += 2
            continue
        depth += (c == "{") - (c == "}")
        out.append(c)
        i += 1
    return "".join(out)


def course_blocks(e: Entry) -> dict:
    """The pieces of a part's page that come from its course entry (empty strings without one)."""
    p = entry_of(e)
    if not p:
        return {}
    key, t, all_ = e.course, table(e.course), entries(e.course)
    tm = track_minutes(e)
    prereq = ", ".join(f'<a href="{all_[q - 1].slug}.html">Part {q}</a>' for q in p.prereq) or "none"
    objectives = "".join(
        f'<div class="obj obj-{k}"><h3>{badge(key, k)}</h3><ul>' + "".join(f"<li>{esc(o)}</li>" for o in p.objectives[k])
        + "</ul></div>" for k in "UMDI")
    # inline math in display style: unlike a display, it may break after a relation, an operator or a \qquad,
    # so a long result wraps on a phone instead of running off its card
    results = "".join(f'<div class="result"><span class="name">{esc(name)}</span><span class="tex wrap">\\(\\displaystyle '
                      f'{esc(_breakable(tex))}\\)</span></div>' for name, tex in p.results)
    rows = "".join(f'<li data-tier="{tier}"><span class="num">{label}</span><span class="title">{esc(title)}</span>'
                   f'{badge(key, tier)}<span class="mins">{f"{mins:.0f} min" if mins >= 0.5 else ""}</span></li>'
                   for label, title, mins, tier in tiered_chapters(e))
    track_line = " · ".join(f"{t.tracks[k][0]} {fmt_minutes(tm[k])}" for k in "UMDI")
    also = "".join(f'<li><a href="{BLOB}/{path}">{esc(label)}</a></li>' for label, path in p.also)
    return {
        "level": f"{badge(key, p.level)}<span>starts at this level</span>",
        "prereq": f'<span class="dot">prerequisites: {prereq}</span>',
        "story": (f'<blockquote class="question">{esc(p.question)}</blockquote><p class="story">{esc(p.story)}</p>'
                  f'<p class="handoff"><strong>Where it goes next.</strong> {esc(p.handoff)}</p>'
                  + (f'<p class="outside"><strong>What you need.</strong> {esc(p.outside)}</p>' if p.outside else "")),
        "widget": (f'<section id="try" class="try"><h2>Try it</h2><div class="widget" data-widget="{p.widget}">'
                   f'<noscript>This interactive needs JavaScript.</noscript></div></section>'),
        "objectives": (f'<section id="objectives"><h2>What you will be able to do</h2><div class="objectives">{objectives}'
                       f'</div></section><section id="results"><h2>Key results</h2><div class="results">{results}</div></section>'),
        "chapters": (f'<p class="hint">Each chapter has a home level. Choose a track to see what to watch: {track_line}.</p>'
                     f'{track_buttons(key)}<ol class="chapters">{rows}</ol>'),
        "also": f'<h3>Companion material in this repository</h3><ul>{also}</ul>' if also else "",
    }


def tracks_page(c: Course) -> str:
    t = table(c.key)
    out = []
    for key, (name, blurb) in t.tracks.items():
        tiers = coursekit.TRACK_TIERS[key]
        rows, hours = [], 0.0
        for e in entries(c.key):
            if e.n not in t.parts:
                continue
            watch = [x for x in tiered_chapters(e) if x[3] in tiers]
            own = watch if key == "M" else [x for x in watch if x[3] == key]
            if not own:
                continue
            mins = sum(x[2] for x in watch)
            hours += mins / 60
            shown = own if key in "DI" else watch
            names = "; ".join(esc(x[1]) for x in shown[:9]) + (f" and {len(shown) - 9} more" if len(shown) > 9 else "")
            rows.append(f'<tr><td class="n">{e.n}</td><td><a href="{e.slug}.html">{esc(e.title)}</a><span class="goal">'
                        f'{esc(t.parts[e.n].objectives[key][0])}</span></td><td class="ch">{names}</td>'
                        f'<td class="m">{mins:.0f} min</td></tr>')
        out.append(f'<section id="{key}" class="track track-{key}"><h2>{badge(c.key, key)} {esc(name)} track</h2><p>{esc(blurb)}</p>'
                   f'<p>{esc(t.track_intro.get(key, ""))}</p><p class="hint">{len(rows)} parts · about {hours:.0f} hours of film.</p>'
                   f'<div class="table-wrap"><table class="plan"><thead><tr><th>Part</th><th>What you take from it</th>'
                   f'<th>{"Chapters of this track" if key in "DI" else "Chapters to watch"}</th><th>Time</th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table></div></section>')
    body = ('<article class="doc"><h1>Tracks</h1><p class="lede">One course, four ways through it. Each part\'s page '
            'has the same buttons, so you can switch level chapter by chapter.</p>'
            '<p class="jump">' + " · ".join(f'<a href="#{k}">{esc(v[0])}</a>' for k, v in t.tracks.items()) + "</p>"
            + "".join(out) + "</article>")
    return shell(c, f"Tracks · {c.name}", body, f"The four tracks through {c.name}.")


def labs_page(c: Course) -> str:
    t = table(c.key)
    cards = []
    for e in entries(c.key):
        if has_lab(e):
            module = labs.load(c.key, e.n)
            cards.append(f'<a class="lcard" href="{e.slug}.html#lab"><img src="labs/lab{e.n:02d}.png" alt="" loading="lazy">'
                         f'<span class="n">Lab {e.n} · {esc(e.title)}</span><span class="t">{esc(module.TITLE)}</span></a>')
    lib = (f' They are written on <a href="{REPO}/tree/main/{t.library[1]}">{esc(t.library[0])}</a>: {esc(t.library[2])}.'
           if t.library else "")
    body = f"""<article class="doc"><h1>Labs</h1>
<p class="lede">One lab per part. Each is seeded, runs in seconds with nothing to download, checks its own result
against the theory it illustrates, and ends with three things to change.{lib}</p>
<pre class="code"><code>pip install {t.lab_needs.replace(",", "")}
python -m videos.{c.key}.labs --list
python -m videos.{c.key}.labs {cards and entries(c.key)[0].n} --show
python -m pytest -q tests/test_courses.py -k {c.key}</code></pre>
<div class="lgrid">{''.join(cards)}</div></article>"""
    return shell(c, f"Labs · {c.name}", body, f"The runnable labs of {c.name}.")


def part_page(e: Entry, out: Path | None = None, run_labs: bool = True) -> str:
    c = BY_KEY[e.course]
    cb = course_blocks(e)
    all_ = entries(e.course)
    act = act_of(e)
    readme = split_readme(e.dir / "README.md")
    syl = syllabus_entry(e.course, e.n) if c.prefix else {"subtitle": "", "prereq": "", "question": "", "story": "", "plan": ""}
    chs = chapters(e)
    total = sum(m for _, _, m in chs)
    row = parts_table(e.course)[1].get(e.n, []) if c.prefix else []
    rel = e.dir.relative_to(ROOT).as_posix()
    package = rel.replace("/", ".")
    subtitle = e.subtitle or syl["subtitle"]
    meta = [cb.get("level", ""), f'<span class="{"dot" if cb else ""}">{fmt_minutes(total)}</span>' if total >= 1 else "",
            f'<span class="dot">{len(chs)} chapters</span>',
            cb.get("prereq") or (f'<span class="dot">prerequisites: {inline_md(syl["prereq"], e.dir.parent)}</span>'
                                 if syl["prereq"] else "")]
    story = cb.get("story") or (
        (f'<blockquote class="question">{inline_md(syl["question"], e.dir.parent)}</blockquote>' if syl["question"] else "")
        + (f'<p class="story">{inline_md(syl["story"], e.dir.parent)}</p>' if syl["story"] else ""))
    lab = lab_block(e, out, run_labs) if (out and has_lab(e)) else ""
    glance = "".join(f"<dt>{esc(_clean(h))}</dt><dd>{inline_md(x, e.dir.parent)}</dd>" for h, x in row)
    rows = "".join(f'<li><span class="num">{label}</span><span class="title">{esc(title)}</span><span></span>'
                   f'<span class="mins">{f"{mins:.0f} min" if mins >= 0.5 else ""}</span></li>' for label, title, mins in chs)
    plan = (f'<details class="notes"><summary><span class="kind">The syllabus\'s plan for this part</span>'
            f'<span class="orig">from SYLLABUS.md, the plan of record</span></summary>'
            f'<div class="md">{md_to_html(syl["plan"], VIDEOS / e.course)}</div></details>') if syl["plan"] else ""
    notes = sections(readme["en"], _ORDER)
    zh = sections(readme["zh"], ("chapters", "problems", "glossary", "sources", "computed", "back", "notes", "visual", "build"))
    build_notes = sections(readme["en"], ("build",))
    compute = f"python -m {package}.compute        # the {c.unit}'s numbers, into .cache/{e.video}\n" if (e.dir / "compute.py").exists() else ""
    label = f"{act[0]} · {act[1]}" if act[0] else act[1]
    prev_ = (f'<a class="prev" href="{all_[e.n - 2].slug}.html">← {esc(all_[e.n - 2].title)}</a>' if e.n > 1 else "<span></span>")
    next_ = (f'<a class="next" href="{all_[e.n].slug}.html">{esc(all_[e.n].title)} →</a>' if e.n < len(all_)
             else '<a class="next" href="index.html#map">Back to the course map →</a>')
    overview = (f'<details class="notes overview"{"" if story else " open"}><summary><span class="kind">What '
                f'the {c.unit} covers</span><span class="orig">from its README</span></summary>'
                f'<div class="md">{readme["intro"]}</div></details>') if readme["intro"] else ""
    body = f"""
<article class="part" data-part="{e.n}">
<p class="crumb"><a href="index.html#map">{esc(label)}</a><span>{c.unit.capitalize()} {e.n} of {len(all_)}</span></p>
<h1>{esc(e.title)}</h1>
{f'<p class="sub">{esc(subtitle)}</p>' if subtitle else ''}
<p class="meta">{''.join(meta)}</p>
{story}
{f'<dl class="glance">{glance}</dl>' if glance else ''}
{overview}
{cb.get("widget", "")}
{cb.get("objectives", "")}
<section id="chapters"><h2>Chapters</h2>
{cb.get("chapters") or f'<ol class="chapters">{rows}</ol>'}
{plan}
</section>
{lab}
<section id="notes"><h2>Lecture notes, problems and sources</h2>
<p class="hint">From the {c.unit}'s <a href="{BLOB}/{rel}/README.md">README</a>. Try the problems before opening
the solutions.</p>
{notes or '<p>See the README.</p>'}
{cb.get("also", "")}
</section>
{f'<section id="zh" lang="zh"><h2>中文讲义</h2><p class="hint">本讲的中文部分（与英文版对应）。</p>{zh}</section>' if zh else ''}
<section id="build"><h2>Build the film</h2>
<pre class="code"><code>{compute}python tools/build.py {e.video}                  # render and assemble the film
EXPLAINER_TTS=silent python tools/qa_scene.py {e.video} {manifest(e.dir)[1][0][1]}   # one chapter, silent, with a contact sheet</code></pre>
<p class="hint">Scenes: <a href="{REPO}/tree/main/{rel}">{rel}</a>. Setup: <a href="index.html#setup">see the
course page</a>.</p>
{build_notes}
</section>
<nav class="pager">{prev_}{next_}</nav>
</article>"""
    p = entry_of(e)
    description = (p.question if p else syl["question"]) or subtitle or f"{e.title}: a {c.unit} of {c.name}."
    return shell(c, f"{e.title} · {c.name}", body, _clean(description), widgets=bool(p))


def card_line(e: Entry) -> str:
    """The line under a part's name on the course map."""
    c = BY_KEY[e.course]
    if not c.prefix:
        return e.subtitle or " · ".join(title for _, title, _ in chapters(e)[1:-1])
    if entry_of(e):
        return entry_of(e).question
    q = syllabus_entry(e.course, e.n)["question"]
    if q:
        return _clean(q)
    row = parts_table(e.course)[1].get(e.n, [])
    if row or syllabus_entry(e.course, e.n)["subtitle"]:
        return _clean(row[0][1]) if row else syllabus_entry(e.course, e.n)["subtitle"]
    return " · ".join(title for label, title, _ in chapters(e) if label.isdigit())


def readme_section(key: str, prefix: str) -> tuple:
    m = re.search(rf"^## ({re.escape(prefix)}.*?)$\n(.*?)(?=^## |\Z)", series_readme(key), re.S | re.M)
    return (_clean(m.group(1)), md_to_html(m.group(2).strip(), VIDEOS / key)) if m else ("", "")


def totals(key: str) -> dict:
    es = entries(key)
    return {"parts": len(es), "hours": sum(sum(chapter_minutes(e)) for e in es) / 60,
            "chapters": sum(len(manifest(e.dir)[1]) for e in es),
            "problems": sum(1 for e in es if any(k == "problems" for k, *_ in split_readme(e.dir / "README.md")["en"])),
            "zh": sum(1 for e in es if split_readme(e.dir / "README.md")["zh"])}


def index_page(c: Course) -> str:
    t = totals(c.key)
    tb = table(c.key) if c.prefix else None
    n_labs = sum(1 for e in entries(c.key) if has_lab(e))
    cards = []
    for label, name, (a, b), blurb in acts(c.key):
        rows = []
        for e in entries(c.key)[a - 1:b]:
            mins = sum(chapter_minutes(e))
            p, level, foot = entry_of(e), "", ""
            if p:
                tiers = {x[3] for x in tiered_chapters(e)} - {"*"}
                dots = "".join(f'<i class="d d-{k}" title="{esc(tb.tracks[k][0])} chapters"></i>' for k in "UMDI" if k in tiers)
                level = f' data-level="{p.level}"'
                foot = f'{badge(c.key, p.level)}<span class="dots">{dots}</span>'
            rows.append(f'<a class="pcard" href="{e.slug}.html"{level}><span class="n">{e.n}</span><span class="t">{esc(e.title)}</span>'
                        f'<span class="q">{esc(card_line(e))}</span><span class="foot">{foot}<span class="m">'
                        f'{len(manifest(e.dir)[1])} chapters{f" · {mins:.0f} min" if mins >= 1 else ""}</span></span></a>')
        cards.append(f'<section class="act"><h3>{f"<span>{esc(label)}</span>" if label else ""}{esc(name)}</h3>'
                     f'{f"<p>{esc(blurb)}</p>" if blurb else ""}<div class="pgrid">{"".join(rows)}</div></section>')
    story = []
    for i, prefix in enumerate(c.story):
        heading, page = readme_section(c.key, prefix)
        if page:
            story.append(f'<details class="notes"{" open" if i == 0 else ""}><summary><span class="kind">{esc(heading)}'
                         f'</span></summary><div class="md">{page}</div></details>')
    has_syllabus = (VIDEOS / c.key / "SYLLABUS.md").exists()
    first = entries(c.key)[0]
    stats = [f"<span><b>{t['parts']}</b> {c.unit}s</span>", f"<span><b>{t['hours']:.0f}</b> hours of lectures</span>",
             f"<span><b>{t['chapters']}</b> chapters</span>"]
    if t["problems"]:
        stats.append(f"<span><b>{t['problems']}</b> problem sets with solutions</span>")
    if t["zh"]:
        stats.append(f"<span><b>{t['zh']}</b> {c.unit}s with Chinese notes</span>")
    steps = [("Watch", f"Each {c.unit} is a lecture built in code: derivations in full, every number computed or "
                       f"cited. Build it from source, or read what it covers and its chapter list here."),
             ("Read the notes", f"Each {c.unit}'s page carries its README: what is computed and built, chapter "
                                f"notes, the glossary, and where each idea comes back.")]
    if n_labs:
        steps.append(("Run the lab", f"One lab per part{', on ' + tb.library[0] if tb and tb.library else ''}. Seeded, a few "
                                     f"seconds each, nothing to download. Each checks its own result and ends with "
                                     f"three things to change."))
    if t["problems"]:
        steps.append(("Work the problems", "Problem sets with worked solutions, in English and (where the part has "
                                           "them) Chinese. Try them before opening the solutions."))
    steps.append(("Check the sources", "Every page lists the papers, books and data the film was checked against."))
    tracks = ""
    if tb and tb.parts:
        tcards = []
        for k, (name, blurb) in tb.tracks.items():
            watched = [e for e in entries(c.key) if e.n in tb.parts and (k == "M" or any(x[3] == k for x in tiered_chapters(e)))]
            hours = sum(track_minutes(e)[k] for e in watched) / 60
            tcards.append(f'<a class="tcard tcard-{k}" href="tracks.html#{k}"><h3>{esc(name)}</h3><p>{esc(blurb)}</p>'
                          f'<span>{len(watched)} parts · about {hours:.0f} hours</span></a>')
        tracks = (f'<section id="tracks"><h2>Four tracks through the same material</h2><p class="hint">Every chapter has a '
                  f'home level. A track is the set of chapters to watch at that level; on each part\'s page a button '
                  f'shows them.</p><div class="tgrid">{"".join(tcards)}</div></section>')
        stats.insert(3, f"<span><b>{n_labs}</b> runnable labs</span>")
        stats.insert(4, f"<span><b>{len(widgets_defined(c.key) & {p.widget for p in tb.parts.values()})}</b> interactives</span>")
    how = "".join(f"<div><b>{i} · {a}</b><p>{esc(b)}</p></div>" for i, (a, b) in enumerate(steps, 1))
    body = f"""
<section class="hero">
  <p class="kicker">{esc(c.kicker)}</p>
  <h1>{esc(c.name)}</h1>
  <p class="lede">{esc(c.lede)}</p>
  <div class="stats">{''.join(stats)}</div>
</section>
<section id="how"><h2>How to use the course</h2><div class="steps">{how}</div></section>
{tracks}
{f'<section id="story"><h2>The story and the devices</h2>{"".join(story)}</section>' if story else ''}
<section id="map"><h2>The course map</h2>
<p class="hint">Each card opens the {c.unit}'s page: its chapters, notes, problems and sources.</p>
{''.join(cards)}
</section>
<section id="setup"><h2>Setup</h2>
<pre class="code"><code>git clone {REPO}.git
cd explainer-videos
bash tools/setup_linux.sh &amp;&amp; source .venv/bin/activate
{f"python -m {first.dir.relative_to(ROOT).as_posix().replace('/', '.')}.compute   # the first {c.unit}'s numbers" if (first.dir / "compute.py").exists() else ""}
python tools/build.py {first.video}             # the first {c.unit}</code></pre>
<p class="hint">{f'The plan of record is the <a href="syllabus.html">syllabus</a>: the standard every part meets and all {t["parts"]} parts chapter by chapter. ' if has_syllabus else ''}The
sources are in <a href="{REPO}/tree/main/videos/{c.key if c.prefix else ''}">the repository</a>; the other courses
are on the <a href="../index.html">front page</a>.</p></section>
"""
    return shell(c, f"{c.name}: {c.kicker[0].lower()}{c.kicker[1:]}", body, c.tagline)


def syllabus_page(c: Course) -> str:
    source = VIDEOS / c.key / "SYLLABUS.md"
    lede = f"The plan of record of {c.name}: the standard every part meets, the devices, and every part chapter by chapter."
    body = (f'<article class="doc"><h1>Syllabus</h1><p class="lede">{esc(lede)}</p>'
            f'<div class="md long">{md_to_html(source.read_text().split(chr(10), 1)[1], source.parent)}</div></article>')
    return shell(c, f"Syllabus · {c.name}", body, lede)


def landing_page() -> str:
    from videos.quant import course as quant  # the one course with its own builder

    quant_hours = sum(sum(quant_site.chapter_minutes(n)) for n in range(1, quant.N_PARTS + 1)) / 60
    cards = [("quant/index.html", "Q", ("#a78bfa", "#fbbf24"), "Quant, Built", "量化金融，从零搭建",
              "Pricing by replication and investing for premia, from a first random walk to the research frontier, "
              "built around its own quant firm, the House.", quant.N_PARTS, quant_hours,
              f"parts · {quant.N_PARTS} labs and interactives")]
    for c in COURSES:
        t = totals(c.key)
        n_labs = sum(1 for e in entries(c.key) if has_lab(e))
        extra = f" · {n_labs} labs and interactives" if n_labs else ""
        cards.append((f"{c.key}/index.html", c.mark, c.colors, c.name, c.zh, c.tagline, t["parts"], t["hours"], c.unit + "s" + extra))
    grid = "".join(
        f'<a class="ccard" href="{href}"><span class="mark" style="background:linear-gradient(135deg,{a},{b})">{esc(mark)}'
        f'</span><span class="t">{esc(name)}</span><span class="zh" lang="zh">{esc(zh)}</span><span class="q">{esc(line)}'
        f'</span><span class="m">{parts} {unit} · about {hours:.0f} hours</span></a>'
        for href, mark, (a, b), name, zh, line, parts, hours, unit in cards)
    parts = sum(x[6] for x in cards)
    hours = sum(x[7] for x in cards)
    body = f"""
<section class="hero">
  <p class="kicker">Lectures built in code</p>
  <h1>Explainer Videos</h1>
  <p class="lede">Long-form lectures in the manner of 3Blue1Brown, generated from source: every derivation is
  animated in Manim, every number on screen is computed by the film's own code or cited, and the narration is
  synthesized locally. These pages are the course material that goes with them: four tracks through each course,
  a runnable lab and an interactive for every part, chapters, lecture notes, problems with worked solutions, and
  sources, generated from the same repository as the films.</p>
  <div class="stats"><span><b>{len(cards) - 1}</b> courses</span><span><b>{parts}</b> lectures</span>
  <span><b>{hours:.0f}</b> hours</span></div>
</section>
<section id="courses"><h2>The courses</h2><div class="cgrid">{grid}</div></section>
<section id="build"><h2>Build a film</h2>
<pre class="code"><code>git clone {REPO}.git
cd explainer-videos
bash tools/setup_linux.sh &amp;&amp; source .venv/bin/activate
python tools/build.py quantum           # any film, by name</code></pre>
<p class="hint">Videos are addressed by name; each course's page lists its parts and their names.</p></section>
"""
    return shell(None, "Explainer Videos: courses built in code", body,
                 "Course material for the explainer-video series: chapters, lecture notes, problems with solutions "
                 "and sources.", depth=0)


# ---------------------------------------------------------------------------
def build(out: Path, keys: list | None = None, parts: list | None = None, log=print, run_labs: bool = True,
          pages_only: bool = False) -> None:
    """Write the courses in ``keys`` (default: all) and the landing page into ``out``.  ``pages_only``: just the
    pages of ``parts`` and the interactives they use (tools/check_course.py)."""
    start = time.time()
    quant_site.write_assets(out)
    for key in keys or [c.key for c in COURSES]:
        c = BY_KEY[key]
        folder = out / key
        folder.mkdir(parents=True, exist_ok=True)
        for e in entries(key):
            if parts and c.prefix and e.n not in parts:
                continue
            (folder / f"{e.slug}.html").write_text(part_page(e, out, run_labs))
        if pages_only:
            write_widgets(out, key, {table(key).parts[n].widget for n in parts or [] if n in table(key).parts})
            continue
        (folder / "index.html").write_text(index_page(c))
        if (VIDEOS / key / "SYLLABUS.md").exists():
            (folder / "syllabus.html").write_text(syllabus_page(c))
        if table(key):
            write_widgets(out, key)
            for e in entries(key):  # the labs page shows every lab's figure, also of parts not rebuilt now
                if has_lab(e) and not (folder / "labs" / f"lab{e.n:02d}.png").exists():
                    lab_block(e, out, run_labs)
            (folder / "tracks.html").write_text(tracks_page(c))
            (folder / "labs.html").write_text(labs_page(c))
        t = totals(key)
        log(f"{c.name:<24} {t['parts']:>3} {c.unit}s  {t['hours']:5.1f} h  {t['chapters']} chapters", flush=True)
    if not pages_only:
        (out / "index.html").write_text(landing_page())
    log(f"courses: {out}  ({time.time() - start:.0f} s)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "_site"))
    ap.add_argument("--series", nargs="*", choices=[c.key for c in COURSES], help="only these courses")
    ap.add_argument("--parts", nargs="*", type=int, help="only these parts' pages (the films are always all built)")
    ap.add_argument("--no-labs", action="store_true", help="do not rerun labs whose figure and output already exist")
    ap.add_argument("--skip-labs", action="store_true", help="leave the labs off the pages: a quick structural build")
    args = ap.parse_args()
    global WITH_LABS
    WITH_LABS = not args.skip_labs
    build(Path(args.out), args.series, args.parts, run_labs=not args.no_labs)


if __name__ == "__main__":
    main()
