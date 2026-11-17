#!/usr/bin/env python
"""The narration of a film's chapters as lecture text, for the course sites' lecture notes.

    python tools/lecture_text.py stats12            # print the part's text, chapter by chapter
    python tools/lecture_text.py stats12 --stats    # how many paragraphs, words and computed values

The narration lives in the scene code (``self.voiceover("...")`` and a few helpers that speak a script they are
given), so the notes and the film cannot drift apart.  This reads it with ``ast``, without importing manim or
running the film: a chapter's paragraphs come in the order the film speaks them, following ``construct`` into the
methods it calls.

A number the film computes when it renders (an f-string's ``{value}``) cannot be read from the source. Where the
film keeps its rendered English lines, the number is taken from there: the bilingual films' ``narration_zh.json``, and
``narration_en.json``, which ``--record`` writes from a film's latest render. Otherwise it is kept as a gap, which the
pages show as a small box and explain once.

    python tools/build.py stats12 && python tools/lecture_text.py stats12 --record   # keep the rendered numbers
    EXPLAINER_NARRATION_OUT=/tmp/n ... ; python tools/lecture_text.py stats12 --record /tmp/n   # from a dry run  ``tools/export_script.py`` is the proof-reading
script of a single film, filled in from its latest render.
"""

from __future__ import annotations

import ast
import functools
import html
import re
import runpy
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOOKMARK = re.compile(r"<bookmark[^>]*/>")
GAP_OPEN, GAP_CLOSE = "\x02", "\x03"  # a computed value inside a paragraph: GAP_OPEN expression GAP_CLOSE
NARRATING = {"rows_scene": 3}  # helpers that speak a script passed as this positional argument (also tools/lecture_length.py)
CHAPTER_CARDS = {"card_section": 3, "chapter": 3}  # helpers that open a chapter: (scene, n, title, question)
NUMBER_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
                "sixteen seventeen eighteen nineteen twenty").split()


@dataclass(frozen=True)
class Paragraph:
    text: str  # plain text, gaps marked with GAP_OPEN ... GAP_CLOSE
    kind: str = "p"  # "p", or "q" for the question a chapter card asks

    @property
    def words(self) -> int:
        return len(re.sub(f"{GAP_OPEN}.*?{GAP_CLOSE}", " x ", self.text).split())

    @property
    def gaps(self) -> int:
        return self.text.count(GAP_OPEN)


# ---------------------------------------------------------------------------
# Reading the source
# ---------------------------------------------------------------------------
def _constants(tree: ast.Module) -> dict:
    """Module-level names bound to a string literal (a script kept in a constant)."""
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                continue
            if isinstance(value, str):
                out[node.targets[0].id] = value
    return out


def _script_table(tree: ast.Module) -> list[str]:
    """The English lines of a module-level narration table ``NARRATION = {key: "..." or ("en", "zh")}``."""
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                and "NARRAT" in node.targets[0].id.upper() and isinstance(node.value, ast.Dict)):
            try:
                table = ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                continue
            lines = [v if isinstance(v, str) else v[0] for v in table.values()
                     if isinstance(v, str) or (isinstance(v, (tuple, list)) and v and isinstance(v[0], str))]
            if lines:
                return lines
    return []


def _text(node, consts: dict) -> str | None:
    """The words of a narration argument; a value computed at render time becomes a gap."""
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, str) else None
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                out.append(str(v.value))
            else:
                out.append(GAP_OPEN + ast.unparse(v.value) + GAP_CLOSE)
        return "".join(out)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _text(node.left, consts), _text(node.right, consts)
        if a is None and b is None:
            return None
        gap = lambda n: GAP_OPEN + ast.unparse(n) + GAP_CLOSE  # noqa: E731
        return (a if a is not None else gap(node.left)) + (b if b is not None else gap(node.right))
    if isinstance(node, ast.Name) and node.id in consts:
        return consts[node.id]
    return None


def _call_name(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _spoken(call: ast.Call, consts: dict) -> Paragraph | None:
    """The paragraph a call speaks, if it narrates."""
    name = _call_name(call)
    arg = None
    if name.endswith("voiceover") and isinstance(call.func, ast.Attribute):
        arg = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == "text"), None)
    elif name in NARRATING and len(call.args) > NARRATING[name]:
        arg = call.args[NARRATING[name]]
    elif name in CHAPTER_CARDS:
        q = call.args[CHAPTER_CARDS[name]] if len(call.args) > CHAPTER_CARDS[name] else None
        text = _text(q, consts) if q is not None else None
        return Paragraph(_clean(_tex_plain(text)), "q") if text else None
    elif name.endswith("_section"):
        arg = next((k.value for k in call.keywords if k.arg == "narration"), call.args[3] if len(call.args) > 3 else None)
    if arg is None:
        return None
    text = _clean(_text(arg, consts) or "")
    if len(re.sub(f"{GAP_OPEN}.*?{GAP_CLOSE}", " ", text).split()) < 2:
        return None  # nothing but computed values: nothing to read
    return Paragraph(text)


def _tex_plain(text: str) -> str:
    """A card's question, written for the TeX on screen, as plain words."""
    text = re.sub(r"\\textit\{([^}]*)\}|\\emph\{([^}]*)\}", lambda m: m.group(1) or m.group(2), text)
    text = text.replace("``", '"').replace("''", '"').replace(r"\ ", " ").replace(r"\&", "&").replace("~", " ")
    for tex, sign in ((r"\sharp", "♯"), (r"\flat", "♭"), (r"\natural", "♮"), (r"\times", "×"), (r"\to", "→"),
                      (r"\%", "%"), (r"\$", "$"), ("---", "—"), ("--", "–")):
        text = text.replace(tex, sign)
    text = re.sub(r"(?<!\\)\$", "", text)
    return re.sub(r"\\[a-zA-Z]+\s*", "", text)


def _clean(text: str) -> str:
    return " ".join(BOOKMARK.sub(" ", text).split())


def _ordered(fn: ast.AST) -> list:
    nodes = [n for n in ast.walk(fn) if isinstance(n, (ast.Call, ast.Attribute)) and hasattr(n, "lineno")]
    return sorted(nodes, key=lambda n: (n.lineno, n.col_offset, isinstance(n, ast.Attribute)))


def _methods(tree: ast.Module, cls: str) -> dict:
    """{method name: def} of ``cls`` and of the classes it inherits from in the same module."""
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    out, todo, seen = {}, [cls], set()
    while todo:
        name = todo.pop(0)
        if name in seen or name not in classes:
            continue
        seen.add(name)
        for item in classes[name].body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out.setdefault(item.name, item)
        todo.extend(b.id for b in classes[name].bases if isinstance(b, ast.Name))
    return out


@functools.lru_cache(maxsize=None)
def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text())


def scene_paragraphs(path: Path, cls: str) -> list[Paragraph]:
    """The narration of scene class ``cls`` in ``path``, in the order the film speaks it."""
    tree = _parse(path)
    consts = _constants(tree)
    methods = _methods(tree, cls)
    out, seen, visited = [], set(), set()

    def walk(fn):
        visited.add(fn.name)
        for node in _ordered(fn):
            if isinstance(node, ast.Call):
                if id(node) in seen:
                    continue
                seen.add(id(node))
                p = _spoken(node, consts)
                if p:
                    out.append(p)
            elif (isinstance(node.value, ast.Name) and node.value.id == "self" and node.attr in methods
                  and node.attr not in visited):
                walk(methods[node.attr])

    if "construct" in methods:
        walk(methods["construct"])
    if not out:  # a script kept in a module-level table and looked up by a variable: read the table in order
        out.extend(Paragraph(_clean(t)) for t in _script_table(tree))
    # methods construct reaches only indirectly (a table of callbacks, getattr): in source order, after the rest
    for name, fn in sorted(methods.items(), key=lambda kv: kv[1].lineno):
        if name not in visited:
            walk(fn)
    return out


# ---------------------------------------------------------------------------
# Lecture text
# ---------------------------------------------------------------------------
def _strip_announcement(p: Paragraph, title: str) -> Paragraph | None:
    """Drop the spoken chapter heading ("Chapter three. The Gauss-Markov theorem.") that the page shows as a
    heading anyway."""
    m = re.match(r"^(?:Chapter|Part)\s+([A-Za-z]+(?:[- ][a-z]+)?|\d+)\s*[.:,]\s*", p.text)
    if not m or not (m.group(1).lower() in NUMBER_WORDS or m.group(1).isdigit() or "-" in m.group(1)
                     or m.group(1).lower().split()[0] in NUMBER_WORDS):
        return p
    rest = p.text[m.end():]
    s = re.match(r"^([^.?!]{0,90}[.!?])\s*", rest)
    if s:
        head = set(re.findall(r"[a-z]+", s.group(1).lower())) - {"the", "a", "an", "of", "and", "in", "to"}
        words = set(re.findall(r"[a-z]+", title.lower()))
        if head and (len(head & words) >= max(1, len(head) // 2) or len(s.group(1).split()) <= 3):
            rest = rest[s.end():]
    rest = rest.strip()
    if re.match(r"[a-z]+\b", rest) and not re.match(r"[a-z]+[A-Z]", rest):  # "Chapter seven, compactness, ..."
        rest = rest[0].upper() + rest[1:]
    return Paragraph(rest, p.kind) if rest else None


@functools.lru_cache(maxsize=None)
def rendered_lines(video_dir: Path) -> dict:
    """{scene class: [English line as last rendered]} from the film's ``narration_zh.json``, where the bilingual
    films keep each rendered English line beside its translation, computed numbers filled in."""
    import json  # noqa: PLC0415

    out: dict = {}
    path = video_dir / "narration_en.json"
    if path.exists():
        try:
            for cls, lines in json.loads(path.read_text()).get("lines", {}).items():
                out.setdefault(cls, []).extend(_clean(x) for x in lines if isinstance(x, str))
        except (ValueError, AttributeError):
            pass
    path = video_dir / "narration_zh.json"
    if not path.exists():
        return out
    try:
        lines = json.loads(path.read_text()).get("lines", {})
    except (ValueError, AttributeError):
        return out
    for v in lines.values() if isinstance(lines, dict) else ():
        if isinstance(v, dict) and isinstance(v.get("en"), str):
            out.setdefault(v.get("scene", ""), []).append(_clean(v["en"]))
    return out


def record(video_dir: Path, source: Path | None = None) -> Path | None:
    """Write ``narration_en.json`` beside the film: the rendered English lines of every chapter whose narration has
    computed values, from ``source`` (a folder of ``<Scene>.narration.json`` files, as a dry run with
    ``EXPLAINER_NARRATION_OUT`` writes them) or else from the latest render under ``media/<video>/``."""
    import json  # noqa: PLC0415

    m = runpy.run_path(str(video_dir / "manifest.py"))
    lines: dict = {}
    for module, cls, _ in m["SCENES"]:
        if not any(p.gaps for p in scene_paragraphs(video_dir / f"{module}.py", cls)):
            continue
        if source is not None:
            found = [source / f"{cls}.narration.json"]
        else:
            found = sorted((ROOT / "media" / video_dir.name / "videos" / module).glob(f"*/{cls}.narration.json"),
                           key=lambda f: f.stat().st_mtime)[-1:]
        if found and found[0].exists():
            said = json.loads(found[0].read_text()).get("lines", [])
            lines[cls] = [_clean(x["text"] if isinstance(x, dict) else str(x)) for x in said]
    if not lines:
        return None
    out = video_dir / "narration_en.json"
    out.write_text(json.dumps({"video": video_dir.name, "note": "Rendered English narration of the chapters whose "
                               "numbers are computed at render time, written by tools/lecture_text.py --record; "
                               "the course site fills those numbers in from here.", "lines": lines},
                              ensure_ascii=False, indent=1) + "\n")
    return out


def _fill(p: Paragraph, candidates: list) -> Paragraph:
    """A paragraph with computed gaps, filled from the rendered line whose words match it exactly."""
    parts = re.split(f"{GAP_OPEN}.*?{GAP_CLOSE}", p.text)
    pattern = re.compile("(.+?)".join(re.escape(x) for x in parts), re.S)
    for line in candidates:
        m = pattern.fullmatch(line)
        if m and all(len(g) <= 40 for g in m.groups()):
            return Paragraph(line, p.kind)
    return p


def chapter_text(path: Path, cls: str, title: str = "") -> list[Paragraph]:
    """A chapter's paragraphs for the page: computed values filled in where the film's last render recorded them,
    the spoken heading dropped, very short lines joined to the next."""
    paras = scene_paragraphs(path, cls)
    rendered = rendered_lines(path.parent).get(cls)
    if rendered:
        paras = [_fill(p, rendered) if p.gaps else p for p in paras]
    if paras and paras[0].kind == "p":
        first = _strip_announcement(paras[0], title)
        paras = ([first] if first else []) + paras[1:]
    elif len(paras) > 1 and paras[0].kind == "q":
        second = _strip_announcement(paras[1], title)
        paras = [paras[0]] + ([second] if second else []) + paras[2:]
    out: list[Paragraph] = []
    for p in paras:
        if p.kind == "q" and out and out[-1].kind == "q":
            continue
        continues = re.match(r"[a-z]", p.text) and not re.search(r"[.!?\"')\u201d]$", out[-1].text) if out else False
        if out and out[-1].kind == "p" and p.kind == "p" and (out[-1].words < 14 or continues):
            out[-1] = Paragraph(out[-1].text + " " + p.text)
        elif out and out[-1].kind == "q" and p.kind == "p" and _same(out[-1].text, p.text):
            out[-1] = p  # the card's question, then the narration repeating it: say it once
        else:
            first = p.text.split(" ", 1)[0]
            if p.kind == "p" and first in _SENTENCE_WORDS:  # a line that opens on a lowercase word: start a sentence
                p = Paragraph(p.text[0].upper() + p.text[1:], p.kind)
            out.append(p)
    return out


_SENTENCE_WORDS = set("the a an and but so then this that these those it its we in on at for with from to of as if "
                      "when where while what which how why there here our one two".split())


def _same(question: str, text: str) -> bool:
    q = re.sub(r"\W+", " ", question.lower()).strip()
    return bool(q) and re.sub(r"\W+", " ", text.lower()).strip().startswith(q)


def to_html(p: Paragraph) -> str:
    """One paragraph as HTML; a computed value becomes a small box whose title is the expression."""
    parts = re.split(f"{GAP_OPEN}(.*?){GAP_CLOSE}", p.text)
    out = []
    for i, s in enumerate(parts):
        if i % 2:
            out.append(f'<span class="val" title="Computed when the film renders: {html.escape(s, quote=True)}"></span>')
        else:
            out.append(html.escape(s, quote=False))
    body = "".join(out)
    return f'<p class="lead-q">{body}</p>' if p.kind == "q" else f"<p>{body}</p>"


def film_text(video_dir: Path) -> list[tuple[str, list[Paragraph]]]:
    """[(chapter title, paragraphs)] for a film, in the manifest's order."""
    m = runpy.run_path(str(video_dir / "manifest.py"))
    return [(title, chapter_text(video_dir / f"{module}.py", cls, title)) for module, cls, title in m["SCENES"]]


def main() -> None:
    name = sys.argv[1]
    found = sorted(ROOT.glob(f"videos/*/{name}/manifest.py"))
    if not found:
        sys.exit(f"no video named {name}")
    if "--record" in sys.argv:
        k = sys.argv.index("--record")
        src = Path(sys.argv[k + 1]) if len(sys.argv) > k + 1 and not sys.argv[k + 1].startswith("--") else None
        out = record(found[0].parent, src)
        print(f"wrote {out.relative_to(ROOT)}" if out else "nothing to record: no rendered narration found for the "
              "chapters with computed values")
        return
    chapters = film_text(found[0].parent)
    if "--stats" in sys.argv:
        paras = [p for _, ps in chapters for p in ps]
        print(f"{name}: {len(chapters)} chapters, {len(paras)} paragraphs, {sum(p.words for p in paras)} words, "
              f"{sum(p.gaps for p in paras)} computed values, {sum(1 for _, ps in chapters if not ps)} chapters without text")
        return
    for title, paras in chapters:
        print(f"\n## {title}\n")
        for p in paras:
            text = re.sub(f"{GAP_OPEN}.*?{GAP_CLOSE}", "[#]", p.text)
            print(("> " if p.kind == "q" else "") + text + "\n")


if __name__ == "__main__":
    main()
