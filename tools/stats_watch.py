#!/usr/bin/env python
"""Bring a part of *Statistics, Built* to the watch standard (videos/stats/SYLLABUS.md 1.2).

    python tools/stats_watch.py stats12                    # the mechanical steps, one part
    python tools/stats_watch.py --series                   # the mechanical steps, all sixty-five parts
    python tools/stats_watch.py stats12 --spec spec.py     # and the part's spec (predictions, checkpoints, ...)

The mechanical steps, for every scene of the part (idempotent):

* the scene class becomes a ``StatsScene`` (``explainer/stats/watch.py``: a narrated moving-camera scene whose plain
  fades get the entrance their content suggests, with the standard's set pieces);
* each chapter's card method (``card = chapter_card(...)``, spoken, faded in and out) becomes ``self.chapter(...)``,
  the animated card, speaking the line it spoke before;
* Parts 58-65's ``card_voiceover`` helper draws the same animated card;
* the exam parts' ``pose_voiceover`` marks its clock, so the score's clicks count it down;
* the hook's ``objectives()`` (the part's name, an objectives card, prerequisites) becomes ``self.title(PART)``:
  the title comes after the cold open, under the series' theme, and the objectives card goes.

A spec (a Python file defining ``SPEC``, a dict keyed by scene class) adds what needs judgement, chapter by chapter:

* ``"ask": (question, options, answer, say, reveal)``: the chapter's prediction, asked right after its card and
  answered (``self.answer()``) when the chapter ends;
* ``"wrong": (wrong, right, narration, right_narration)``: a misconception, stated and refuted before the prediction;
* ``"checkpoint": ([(question, answer), ...], narration, answers_narration)``: a checkpoint after the chapter;
* ``"drop": [sentence, ...]``: spoken sentences removed (hedges an on-screen tag already carries);
* ``"replace": [(old, new), ...]``: exact source replacements in the scene's file.

A spec is applied once (a scene that already asks is skipped).
"""

from __future__ import annotations

import argparse
import ast
import re
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir  # noqa: E402

PAD = "        "


# ---------------------------------------------------------------------------- mechanical
def _base(src: str) -> str:
    """``class X(VoiceoverScene)`` (with or without mixins) -> ``class X(StatsScene)``."""
    def fix(m):
        return m.group(0).replace("VoiceoverScene", "StatsScene")
    return re.sub(r"^class \w+\([^)]*\bVoiceoverScene\b[^)]*\):", fix, src, flags=re.M)


def _cards(src: str) -> str:
    """A card method (``c = chapter_card(...)``; ``with self.voiceover("..."): self.play(FadeIn ...)``;
    ``self.play(FadeOut(c))``) -> ``self.chapter(..., said="...")``."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.args.args and node.args.args[0].arg == "self"
                and len(node.body) == 3):
            continue
        a, w, f = node.body
        if not (isinstance(a, ast.Assign) and isinstance(a.value, ast.Call)
                and getattr(a.value.func, "id", "") == "chapter_card" and isinstance(w, ast.With)
                and isinstance(f, ast.Expr)):
            continue
        var = a.targets[0].id
        if not re.fullmatch(rf"self\.play\(FadeOut\({var}\)\)", ast.get_source_segment(src, f).strip()):
            continue
        said = w.items[0].context_expr
        if not (isinstance(said, ast.Call) and getattr(said.func, "attr", "") == "voiceover" and said.args):
            continue
        call = a.value
        args = [ast.get_source_segment(src, x) for x in call.args]
        kws = [f"{k.arg}={ast.get_source_segment(src, k.value)}" for k in call.keywords]
        kws.append(f"said={ast.get_source_segment(src, said.args[0])}")
        lines = src.split("\n")
        body = PAD + "self.chapter(" + ", ".join(args + kws) + ")"
        new = "\n".join(lines[:node.body[0].lineno - 1] + [body] + lines[node.end_lineno:])
        return _cards(new)
    return src


def _objectives(src: str) -> str:
    """The hook's ``objectives()`` -> ``self.title(PART)``, after the cold open."""
    tree = ast.parse(src)
    cls = next((n for n in tree.body if isinstance(n, ast.ClassDef)), None)
    if cls is None:
        return src
    fn = next((f for f in cls.body if isinstance(f, ast.FunctionDef) and f.name == "objectives"), None)
    if fn is None or "objectives_card" not in (ast.get_source_segment(src, fn) or ""):
        return src
    lines = src.split("\n")
    start = fn.lineno - 1
    while start > 0 and lines[start - 1].strip().startswith("#"):
        start -= 1
    end = fn.end_lineno
    while end < len(lines) and not lines[end].strip() and end + 1 < len(lines) and not lines[end + 1].strip():
        end += 1
    src = "\n".join(lines[:start] + lines[end:])
    src = src.rstrip("\n") + "\n"
    new, n = re.subn(r"^(\s+)self\.objectives\(\)\n", r"\1self.title(PART)\n", src, count=1, flags=re.M)
    if n != 1:
        raise ValueError("the hook's construct does not call self.objectives()")
    return new


CARD_VO = '''def card_voiceover(self, text, k, title, subtitle, lit=()):
    card = chapter_card(k, title, subtitle, lit=lit, part=PART)
    with self.voiceover(text):
        self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
    self.play(FadeOut(card))
'''
CARD_VO_NEW = '''def card_voiceover(self, text, k, title, subtitle, lit=()):
    """The chapter card, animated (``StatsScene.chapter``), speaking ``text``."""
    self.chapter(k, title, subtitle, lit=lit, part=PART, said=text)
'''
POSE = '''    def pose_voiceover(self, text, card, pause: float = 6.0):
        with self.voiceover(text):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.play(card.sweep(pause))'''
POSE_NEW = '''    def pose_voiceover(self, text, card, pause: float = 6.0):
        with self.voiceover(text):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.mark(f"countdown:{int(round(pause))}")  # the score clicks the exam clock down
        self.play(card.sweep(pause))'''


def mechanical(video: str) -> list[str]:
    d = video_dir(video)
    done = []
    common = d / "common.py"
    if common.exists():
        src = common.read_text()
        new = src.replace(CARD_VO, CARD_VO_NEW).replace(POSE, POSE_NEW)
        if new != src:
            ast.parse(new)
            common.write_text(new)
            done.append(common.name)
    for path in sorted(d.glob("s[0-9]*_*.py")):
        src = path.read_text()
        new = _cards(_base(src))
        if path.name.startswith("s01_"):
            new = _objectives(new)
        if new != src:
            ast.parse(new)
            path.write_text(new)
            done.append(path.name)
    return done


# ---------------------------------------------------------------------------- the spec
def lit(s: str) -> str:
    """A string literal for ``s``: raw when it has backslashes (TeX), double-quoted."""
    if "\\" in s and '"' not in s and not s.endswith("\\") and "\n" not in s:
        return 'r"' + s + '"'
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _wrap_str(s: str, indent: int, width: int = 116) -> str:
    """A long (non-raw) narration string as adjacent literals, broken at spaces, so lines stay under ``width``."""
    room = width - indent - 2
    if len(s) <= room or "\\" in s:
        return lit(s)
    words, parts, cur = s.split(" "), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > room:
            parts.append(cur + " ")
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    parts.append(cur)
    return ("\n" + " " * indent).join(lit(p) for p in parts)


def ask_code(q, options, answer, say, reveal) -> str:
    opts = "[" + ", ".join(lit(o) for o in options) + "]"
    return (f"{PAD}self.ask({lit(q)},\n{PAD}         {opts}, {int(answer)},\n"
            f"{PAD}         say={_wrap_str(say, len(PAD) + 13)},\n"
            f"{PAD}         reveal={_wrap_str(reveal, len(PAD) + 16)})")


def wrong_code(wrong, right, narration, right_narration) -> str:
    return (f"{PAD}self.wrong_idea({lit(wrong)},\n{PAD}                {lit(right)},\n"
            f"{PAD}                narration={_wrap_str(narration, len(PAD) + 26)},\n"
            f"{PAD}                right_narration={_wrap_str(right_narration, len(PAD) + 32)})")


def checkpoint_code(items, narration, answers) -> str:
    rows = (",\n" + PAD + "                 ").join(f"({lit(q)}, {lit(a)})" for q, a in items)
    return (f"{PAD}self.checkpoint([{rows}],\n"
            f"{PAD}                narration={_wrap_str(narration, len(PAD) + 26)},\n"
            f"{PAD}                answers_narration={_wrap_str(answers, len(PAD) + 34)})")


def _construct(tree, cls: str):
    node = next((n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls), None)
    if node is None:
        raise KeyError(f"no scene class {cls}")
    fn = next((f for f in node.body if isinstance(f, ast.FunctionDef) and f.name == "construct"), None)
    if fn is None:
        raise KeyError(f"{cls} has no construct")
    return fn


def drop(src: str, sentence: str) -> str:
    """Remove a spoken sentence, which may be split across string literals."""
    words = sentence.split()
    pat = r'\s*(?:"\s*f?r?")?\s*'.join(re.escape(w) for w in words)
    new, n = re.subn(r" ?" + pat, "", src, count=1)
    if n != 1:
        raise KeyError(f"sentence not found: {sentence[:60]!r}")
    return new


def apply_scene(src: str, cls: str, entry: dict) -> str:
    for sentence in entry.get("drop", []):
        src = drop(src, sentence)
    for old, new in entry.get("replace", []):
        if src.count(old) != 1:
            raise KeyError(f"{cls}: {old[:60]!r} occurs {src.count(old)} times")
        src = src.replace(old, new)
    tree = ast.parse(src)
    fn = _construct(tree, cls)
    body_src = "\n".join(src.split("\n")[fn.lineno - 1:fn.end_lineno])
    if "self.ask(" in body_src or "self.wrong_idea(" in body_src:
        return src  # applied before
    head, tail = [], []
    if "wrong" in entry:
        head.append(wrong_code(*entry["wrong"]))
    if "ask" in entry:
        head.append(ask_code(*entry["ask"]))
        tail.append(PAD + "self.answer()")
    if "checkpoint" in entry:
        tail.append(checkpoint_code(*entry["checkpoint"]))
    lines = src.split("\n")
    first = fn.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
        first = fn.body[1]
    card = first  # the chapter card is construct's first call; the prediction comes right after it
    is_card = isinstance(card, ast.Expr) and isinstance(card.value, ast.Call) and \
        getattr(card.value.func, "attr", "") in ("card", "card_", "card_voiceover", "chapter")
    at = card.end_lineno if is_card else card.lineno - 1
    end = fn.end_lineno
    new = lines[:at] + head + lines[at:end] + tail + lines[end:]
    out = "\n".join(new)
    ast.parse(out)
    return out


def apply(video: str, spec: dict) -> list[str]:
    import importlib

    from explainer.paths import video_package

    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    module_of = {cls: mod for mod, cls, _ in manifest.SCENES}
    d = video_dir(video)
    files: dict[str, str] = {}
    for cls, entry in spec.items():
        mod = module_of[cls]
        files[mod] = apply_scene(files.get(mod) or (d / f"{mod}.py").read_text(), cls, entry)
    for mod, src in files.items():
        (d / f"{mod}.py").write_text(src)
    return sorted(files)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video", nargs="?")
    ap.add_argument("--series", action="store_true", help="the mechanical steps for every part")
    ap.add_argument("--spec")
    a = ap.parse_args(argv)
    vids = [f"stats{n}" for n in range(1, 66)] if a.series else [a.video]
    for v in vids:
        done = mechanical(v)
        print(f"{v}: {len(done)} file(s) retrofitted" + (f" ({', '.join(done[:4])}{', ...' if len(done) > 4 else ''})"
                                                       if done else ""))
    if a.spec:
        print("spec:", ", ".join(apply(a.video, runpy.run_path(a.spec)["SPEC"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
