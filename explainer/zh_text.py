"""On-screen text in Chinese for the Chinese masters of a series.

Every Tex / MathTex / Text string is looked up in the series' table, videos/<series>/<series>_text_zh.json (keyed by
the exact English string; e.g. videos/analysis/analysis_text_zh.json); strings that come out containing Chinese are
typeset with xelatex + xeCJK (Fandol Song), the rest are unchanged. The series is that of the video being rendered
(EXPLAINER_VIDEO, set by tools/build.py and tools/collect_text.py), or of the scene file on manim's command line.
EXPLAINER_COLLECT_TEXT=<file.jsonl> records every string instead, to gather what needs translating.
"""

from __future__ import annotations

import inspect
import json
import os
import re
import sys
from pathlib import Path

from manim import MathTex, Scene, Text

from explainer import lang
from explainer.paths import ANALYSIS_DATA, VIDEOS, video_dir

COLLECT = os.environ.get("EXPLAINER_COLLECT_TEXT", "")
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
_MATH = re.compile(r"\$[^$]*\$|\\\(.*?\\\)")
_CMD = re.compile(r"\\[A-Za-z]+")
_ENV = re.compile(r"\\(?:begin|end)\{\w+\}(?:\{[^{}]*\})?")


def needs_translation(s: str, math_mode: bool) -> bool:
    """True if the string shows English words: in math mode only inside \\text{...}, else outside $...$."""
    if math_mode:
        s = " ".join(re.findall(r"\\text(?:bf|it)?\{([^{}]*)\}", s))
    s = _CMD.sub(" ", _MATH.sub(" ", _ENV.sub(" ", s)))
    return bool(re.search(r"[A-Za-z]{2,}", s))


def table_path() -> Path:
    """videos/<series>/<series>_text_zh.json for the series being rendered (the analysis series by default)."""
    series = ANALYSIS_DATA
    if os.environ.get("EXPLAINER_VIDEO"):
        series = video_dir(os.environ["EXPLAINER_VIDEO"]).parent
    else:
        for a in sys.argv:
            p = Path(a).resolve()
            if a.endswith(".py") and p.parent.parent.parent == VIDEOS:
                series = p.parent.parent
                break
    return series / f"{series.name}_text_zh.json"


def _table() -> dict:
    path = table_path()
    return json.loads(path.read_text()) if path.exists() else {}


def _scene() -> str:
    for fr in inspect.stack()[2:12]:
        obj = fr.frame.f_locals.get("self")
        if isinstance(obj, Scene):
            return type(obj).__name__
    return ""


_TABLE: dict | None = None


# xeCJK drops a space that follows a Chinese character, so "\text{ 时 } d" would set as "时d": make it a control space
_SPACE = re.compile(r"([\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]) +\}")
_TEXT_CMD = re.compile(r"(\\text(?:bf|it|rm)?\{)((?:\\[a-z]+\s*)*)([^{}]*)\}")


def translate(s: str) -> str:
    """The Chinese for an on-screen string: an exact entry in "strings", else each \\text{...} phrase of a formula
    from "phrases" (so animated readouts translate whatever their numbers), then the regex "patterns"."""
    global _TABLE
    if lang.LANG != "zh":
        return s
    if _TABLE is None:
        _TABLE = _table()
    if s in _TABLE.get("strings", {}):
        return _SPACE.sub(r"\1\\ }", _TABLE["strings"][s])
    phrases = _TABLE.get("phrases", {})

    def phrase(m):
        core = m.group(3)
        zh = phrases.get(core.strip())
        if zh is None:
            return m.group(0)
        lead, trail = core[:len(core) - len(core.lstrip())], core[len(core.rstrip()):]
        return f"{m.group(1)}{m.group(2)}{lead}{zh}{trail}}}"

    out = _TEXT_CMD.sub(phrase, s)
    for pat, rep in _TABLE.get("patterns", []):
        out = re.sub(pat, rep, out)
    return _SPACE.sub(r"\1\\ }", out)


def install(base_template) -> None:
    zh_tex = base_template.copy()
    zh_tex.tex_compiler, zh_tex.output_format = "xelatex", ".xdv"
    zh_tex.add_to_preamble(r"\usepackage{xeCJK}\setCJKmainfont{FandolSong-Regular.otf}[BoldFont=FandolSong-Bold.otf]")

    def record(s, kind, math_mode):
        for fr in inspect.stack()[2:8]:  # wrapped_label measures partial lines: keep only its whole text
            if fr.function == "wrapped_label" and s != fr.frame.f_locals.get("text"):
                return
        with open(COLLECT, "a") as f:
            f.write(json.dumps({"s": s, "kind": kind, "scene": _scene(),
                                "needs": needs_translation(s, math_mode)}, ensure_ascii=False) + "\n")

    mathtex_init = MathTex.__init__

    def patched_mathtex(self, *tex_strings, **kw):
        math_mode = kw.get("tex_environment", "align*") != "center" and type(self).__name__ != "Tex"
        if COLLECT:
            for s in tex_strings:
                record(s, type(self).__name__, math_mode)
        if lang.LANG == "zh":
            tex_strings = tuple(translate(s) for s in tex_strings)
            if any(CJK.search(s) for s in tex_strings):
                kw["tex_template"] = zh_tex
        mathtex_init(self, *tex_strings, **kw)

    text_init = Text.__init__

    def patched_text(self, text, *a, **kw):
        if COLLECT:
            record(text, "Text", False)
        if lang.LANG == "zh":
            text = translate(text)
            if CJK.search(text):
                kw["font"] = "Songti SC"
        text_init(self, text, *a, **kw)

    MathTex.__init__, Text.__init__ = patched_mathtex, patched_text
