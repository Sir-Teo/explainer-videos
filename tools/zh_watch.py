#!/usr/bin/env python
"""Chinese for what the watch retrofit added to a part of *Computer Science, Built* (videos/cs/SYLLABUS.md 1.2).

    python tools/zh_watch.py cs30 --need need.json      # what has no Chinese yet: spoken lines and on-screen strings
    python tools/zh_watch.py cs30 --put need.json zh.json   # merge translations, zh.json = {"<id>": "<Chinese>"}

The retrofit's set pieces speak through keywords (``self.ask(..., say=, reveal=)``, ``self.wrong_idea(...,
narration=, right_narration=)``, ``self.checkpoint(..., narration=, answers_narration=)``) and show TeX (the question,
the options, the misconception, the checkpoint's questions and answers). ``--need`` lists every such line, and every
``self.voiceover`` line, that a Chinese build could not translate, plus every on-screen string the series table leaves
in English. ``--put`` writes the spoken ones to ``videos/cs/<part>/zh_watch.json``, which the part's ``zh_lines.py``
folds into its table (literal lines by their text, f-strings as templates; see tools/zh_lines.py), and the on-screen
ones to ``videos/cs/cs_text_zh.json`` through tools/text_zh_add.py.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("EXPLAINER_LANG", "zh")
os.environ.setdefault("EXPLAINER_TTS", "silent")

from explainer.paths import video_dir  # noqa: E402

SPOKEN = {"ask": ("say", "reveal"), "predict": ("narration",), "reveal": ("narration",), "expect": ("narration",),
          "checkpoint": ("narration", "answers_narration"), "wrong_idea": ("narration", "right_narration"),
          "chapter": ("said",)}
SHOWN = {"ask": (0, 1), "predict": (0, 1), "wrong_idea": (0, 1), "checkpoint": (0,)}
LOADER = '''
_watch = Path(__file__).with_name("zh_watch.json")
if _watch.exists():  # the watch retrofit's lines (tools/zh_watch.py)
    ZH.update(json.loads(_watch.read_text()))
'''


def _strings(node):
    """(kind, text) for every string a node holds: literals as they are, f-strings as their source."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield "en", node.value
    elif isinstance(node, ast.JoinedStr):
        yield "tpl", ast.unparse(node)
    elif isinstance(node, ast.IfExp):
        yield from _strings(node.body)
        yield from _strings(node.orelse)
    elif isinstance(node, (ast.List, ast.Tuple)):
        for e in node.elts:
            yield from _strings(e)


def lines(video: str):
    """Every spoken line and on-screen kit string of the part: dicts with scene, kind (en/tpl) and where."""
    for path in sorted(video_dir(video).glob("s[0-9]*_*.py")):
        tree = ast.parse(path.read_text())
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for c in ast.walk(cls):
                if not (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)):
                    continue
                name = c.func.attr
                if name == "voiceover" and c.args:
                    for kind, s in _strings(c.args[0]):
                        yield {"scene": cls.name, "kind": kind, "en": s, "where": "said"}
                for k in c.keywords:
                    if k.arg in SPOKEN.get(name, ()):
                        for kind, s in _strings(k.value):
                            yield {"scene": cls.name, "kind": kind, "en": s, "where": "said"}
                for i in SHOWN.get(name, ()):
                    if i < len(c.args):
                        for kind, s in _strings(c.args[i]):
                            yield {"scene": cls.name, "kind": kind, "en": s, "where": "shown"}


def need(video: str) -> list[dict]:
    from explainer import lang as L
    from explainer import zh_text
    from explainer.zh_templates import source_startswith, table

    L.LANG = "zh"
    os.environ["EXPLAINER_VIDEO"] = video
    keys = list(table(video)["ZH"])
    out, seen = [], set()
    for x in lines(video):
        if (x["where"], x["en"]) in seen:
            continue
        seen.add((x["where"], x["en"]))
        if x["where"] == "said":
            if x["kind"] == "tpl":
                ok = any(source_startswith(x["en"], k) for k in keys)
            else:
                try:
                    L.translate(x["en"], video_dir(video), x["scene"])
                    ok = True
                except KeyError:
                    ok = False
        else:
            if x["kind"] == "tpl":  # a computed on-screen string: the table's number templates cover it, or not
                continue
            t = zh_text.translate(x["en"])
            ok = bool(zh_text.CJK.search(t)) or not zh_text.needs_translation(x["en"], False)
        if not ok:
            out.append({"id": str(len(out)), **x})
    return out


def put(video: str, need_file: Path, zh_file: Path) -> None:
    items = {x["id"]: x for x in json.loads(need_file.read_text())}
    zh = json.loads(zh_file.read_text())
    said, shown = {}, {}
    for i, t in zh.items():
        x = items[i]
        (said if x["where"] == "said" else shown)[x["en"]] = t
    d = video_dir(video)
    if said:
        path = d / "zh_watch.json"
        old = json.loads(path.read_text()) if path.exists() else {}
        old.update(said)
        path.write_text(json.dumps(old, ensure_ascii=False, indent=1) + "\n")
        zl = d / "zh_lines.py"
        if "zh_watch.json" not in zl.read_text():
            zl.write_text(zl.read_text().rstrip("\n") + "\n" + LOADER)
        print(f"{path.relative_to(ROOT)}: {len(said)} spoken line(s)")
    if shown:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"strings": shown, "patterns": []}, f, ensure_ascii=False)
        subprocess.run([sys.executable, str(ROOT / "tools" / "text_zh_add.py"), "cs", f.name], check=True)
        os.unlink(f.name)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--need", type=Path)
    ap.add_argument("--put", nargs=2, type=Path)
    a = ap.parse_args(argv)
    if a.put:
        put(a.video, *a.put)
        return 0
    items = need(a.video)
    if a.need:
        a.need.write_text(json.dumps(items, ensure_ascii=False, indent=0))
    for x in items:
        print(f'{x["id"]}\t{x["where"]}\t{x["scene"]}\t{x["en"]}')
    print(f"{a.video}: {sum(x['where'] == 'said' for x in items)} spoken, "
          f"{sum(x['where'] == 'shown' for x in items)} on screen without Chinese", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
