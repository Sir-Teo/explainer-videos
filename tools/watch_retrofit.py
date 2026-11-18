#!/usr/bin/env python
"""Retrofit a part of *Computer Science, Built* to the watch standard (videos/cs/SYLLABUS.md 1.2).

    python tools/watch_retrofit.py cs8 spec.py      # apply the mechanical steps and the part's spec
    python tools/watch_retrofit.py cs8 --mechanical # only the mechanical steps

The mechanical steps, for every scene of the part:

* the scene class becomes a ``WatchScene`` (a narrated moving-camera scene with the standard's set pieces);
* each chapter's ``card()`` becomes ``self.chapter(...)``, speaking the line it spoke before (so the Chinese
  tables still match);
* the hook's ``plan()`` (title, series map, objectives card) becomes ``self.title(PART)``: the title comes after
  the cold open, and the objectives card goes.

The spec (a Python file defining ``SPEC``) adds what needs judgement:

* ``"ask"``: ``[(module, section, code), ...]`` inserted at the start of a section: a prediction, normally
  ``self.ask(...)``, answered when the section clears, after its own run has shown the result;
* ``"end"``: ``[(module, section, code), ...]`` inserted after the section's last ``clear_scene()`` (checkpoints);
* ``"start"``: ``[(module, section, code), ...]`` inserted at the start, before any ``ask`` (the misconception);
* ``"trim"``: ``[(module, section), ...]`` sections taken out of the film (the notes keep them), to fit 60 minutes;
* ``"drop"``: ``[(module, sentence), ...]`` spoken sentences removed (hedges the screen's tags now carry);
* ``"replace"``: ``[(module, old, new), ...]`` exact source replacements.

Idempotent for the mechanical steps; a spec is applied once.
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


def _base(src: str) -> str:
    src = re.sub(r"class (\w+)\(VoiceoverScene, MovingCameraScene\)", r"class \1(WatchScene)", src)
    return re.sub(r"class (\w+)\(VoiceoverScene\)", r"class \1(WatchScene)", src)


def _card(src: str) -> str:
    """``def card(self): card = chapter_card(...); with self.voiceover("..."): ...`` -> ``self.chapter(...)``."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == "card"):
            continue
        call = next((c for c in ast.walk(node) if isinstance(c, ast.Call) and getattr(c.func, "id", "") ==
                     "chapter_card"), None)
        if call is None:
            continue
        said = next((c for c in ast.walk(node) if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and
                     c.func.attr == "voiceover" and c.args), None)
        args = [ast.get_source_segment(src, a) for a in call.args]
        kws = [f"{k.arg}={ast.get_source_segment(src, k.value)}" for k in call.keywords]
        if said is not None:
            kws.append(f"said={ast.get_source_segment(src, said.args[0])}")
        lines = src.split("\n")
        body = "        self.chapter(" + ", ".join(args + kws) + ")"
        new = "\n".join(lines[:node.body[0].lineno - 1] + [body] + lines[node.end_lineno:])
        return _card(new)  # in case a file has more than one scene
    return src


def _plan(src: str) -> str:
    """The hook's ``plan()`` -> the title, after the cold open."""
    tree = ast.parse(src)
    cls = next((n for n in tree.body if isinstance(n, ast.ClassDef)), None)
    if cls is None:
        return src
    plan = next((f for f in cls.body if isinstance(f, ast.FunctionDef) and f.name == "plan"), None)
    if plan is None or "objectives_card" not in (ast.get_source_segment(src, plan) or ""):
        return src
    lines = src.split("\n")
    start = plan.lineno - 1
    while start > 0 and lines[start - 1].strip().startswith("#"):
        start -= 1  # its comment rule
    lines = lines[:start] + lines[plan.end_lineno:]
    src = "\n".join(lines)
    return src.replace("        self.plan()\n", "        self.title(PART)\n", 1)


def mechanical(video: str) -> list[str]:
    done = []
    for path in sorted(video_dir(video).glob("s[0-9]*_*.py")):
        src = path.read_text()
        new = _base(src)
        new = _card(new)
        if path.name.startswith("s01_"):
            new = _plan(new)
        if new != src:
            ast.parse(new)
            path.write_text(new)
            done.append(path.name)
    return done


def _method(src: str, name: str):
    tree = ast.parse(src)
    for cls in tree.body:
        if isinstance(cls, ast.ClassDef):
            for f in cls.body:
                if isinstance(f, ast.FunctionDef) and f.name == name:
                    return f
    raise KeyError(name)


def _indent(code: str) -> str:
    code = code.strip("\n")
    lines = code.split("\n")
    pad = min(len(ln) - len(ln.lstrip()) for ln in lines if ln.strip())
    return "\n".join(("        " + ln[pad:]) if ln.strip() else "" for ln in lines)


def insert_start(src: str, section: str, code: str) -> str:
    f = _method(src, section)
    first = f.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):  # after a docstring
        first = f.body[1] if len(f.body) > 1 else first
    lines = src.split("\n")
    at = first.lineno - 1
    return "\n".join(lines[:at] + [_indent(code)] + lines[at:])


def insert_end(src: str, section: str, code: str) -> str:
    f = _method(src, section)
    lines = src.split("\n")
    at = f.end_lineno
    return "\n".join(lines[:at] + [_indent(code)] + lines[at:])


def trim(src: str, section: str) -> str:
    f = _method(src, section)
    lines = src.split("\n")
    start = f.lineno - 1
    while start > 0 and lines[start - 1].strip().startswith("#"):
        start -= 1
    src = "\n".join(lines[:start] + lines[f.end_lineno:])
    new, n = re.subn(rf"\n        self\.{section}\(\)\n", "\n", src, count=1)
    if n != 1:
        raise KeyError(f"construct does not call self.{section}()")
    return new


def drop(src: str, sentence: str) -> str:
    """Remove a spoken sentence, which may be split across string literals."""
    words = sentence.split()
    pat = r'\s*(?:"\s*f?")?\s*'.join(re.escape(w) for w in words)
    new, n = re.subn(r" ?" + pat, "", src, count=1)
    if n != 1:
        raise KeyError(f"sentence not found: {sentence[:60]!r}")
    return new


def apply(video: str, spec: dict) -> None:
    d = video_dir(video)
    files: dict[str, str] = {}

    def get(mod):
        if mod not in files:
            files[mod] = (d / f"{mod}.py").read_text()
        return files[mod]

    for mod, sec in spec.get("trim", []):
        files[mod] = trim(get(mod), sec)
    for mod, sent in spec.get("drop", []):
        files[mod] = drop(get(mod), sent)
    for mod, old, new in spec.get("replace", []):
        s = get(mod)
        if s.count(old) != 1:
            raise KeyError(f"{mod}: {old[:60]!r} occurs {s.count(old)} times")
        files[mod] = s.replace(old, new)
    for mod, sec, code in spec.get("ask", []):
        files[mod] = insert_start(get(mod), sec, code)
    for mod, sec, code in spec.get("start", []):
        files[mod] = insert_start(get(mod), sec, code)
    for mod, sec, code in spec.get("end", []):
        files[mod] = insert_end(get(mod), sec, code)
    for mod, src in files.items():
        ast.parse(src)
        (d / f"{mod}.py").write_text(src)
        print(f"  {mod}.py")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--mechanical", action="store_true")
    a = ap.parse_args(argv)
    print("mechanical:", ", ".join(mechanical(a.video)) or "nothing to do")
    if a.spec and not a.mechanical:
        apply(a.video, runpy.run_path(a.spec)["SPEC"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
