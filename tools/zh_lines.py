#!/usr/bin/env python
"""Fill a video's narration translation from a table of translated source lines, templates included.

    python tools/zh_lines.py ai27 --todo [Scene ...]   # source lines the table doesn't cover yet
    python tools/zh_lines.py ai27                      # fill narration_zh.json (after translate_narration.py)

`videos/<series>/<video>/zh_lines.py` holds the table:

    TITLE = "AI，从零构建：第27部分，后训练与对齐"
    CHAPTERS = {"Hook": "开场", ...}
    ZH = {
        "Chapter two. Supervised fine-tuning.": "第2章。监督微调。",           # a literal line, by its prefix
        'f"Accuracy climbs over the {S} steps': "在{S}步微调中，准确率……",       # a template, by its source prefix
    }
    PHRASES = {"sea": "大海"}                                                   # spliced-in English values

A literal key is a prefix of the English line. A template key is a prefix of the line's source expression as
`ast.unparse` prints it (`--todo` prints exactly that): an f-string, either branch of a conditional, or a sum of
strings and names (`"..." + verdict`). The rendered English line is matched against the template, and each
placeholder's value is carried into the translation's `{placeholder}` of the same text: through PHRASES, or, when the
value is itself a sentence (a spliced `verdict`), translated by the same table, recursively; numbers lose their
thousands commas. So a line computed from data is translated once and stays translated when the data changes.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir  # noqa: E402

IS_TPL = lambda k: k.startswith(('f"', "f'", '"', "'"))  # noqa: E731


def table(video: str) -> dict:
    path = video_dir(video) / "zh_lines.py"
    if not path.exists():
        return {"ZH": {}, "PHRASES": {}, "TITLE": "", "CHAPTERS": {}}
    spec = importlib.util.spec_from_file_location(f"{video}_zh_lines", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {k: getattr(m, k, d) for k, d in (("ZH", {}), ("PHRASES", {}), ("TITLE", ""), ("CHAPTERS", {}))}


def _parts(node):
    """A template expression as literal text and placeholder names."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _parts(node.left) + _parts(node.right)
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [("text", node.value)]
    if isinstance(node, ast.JoinedStr):
        return [("text", p.value) if isinstance(p, ast.Constant) else ("name", ast.unparse(ast.JoinedStr([p]))[3:-2])
                for p in node.values]
    return [("name", node.id if isinstance(node, ast.Name) else ast.unparse(node))]


def _voiceover_args(tree):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "voiceover"
                and node.args):
            yield node.args[0]


def _branches(node):
    return [node.body, node.orelse] if isinstance(node, ast.IfExp) else [node]


def sources(video: str) -> list[dict]:
    """Every narrated source line in film order: literals, templates, and sentences spliced into templates."""
    out = []
    for f in sorted(video_dir(video).glob("s[0-9][0-9]_*.py")):
        tree = ast.parse(f.read_text())
        for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
            for fn in [n for n in ast.walk(cls) if isinstance(n, ast.FunctionDef)]:
                assigned = {}
                for n in ast.walk(fn):
                    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                        for b in _branches(n.value):
                            if isinstance(b, ast.JoinedStr) or (isinstance(b, ast.Constant) and isinstance(b.value, str)):
                                assigned.setdefault(n.targets[0].id, []).append(b)
                for a in _voiceover_args(fn):
                    for b in _branches(a):
                        if isinstance(b, ast.Name):  # a sentence assigned above: listed below as spliced
                            continue
                        out.append({"scene": cls.name, "en" if isinstance(b, ast.Constant) else "tpl":
                                    b.value if isinstance(b, ast.Constant) else ast.unparse(b)})
                    names = {n.id for n in ast.walk(a) if isinstance(n, ast.Name)}
                    for nm in sorted(names & set(assigned)):
                        for b in assigned[nm]:
                            if len(ast.unparse(b)) > 40:
                                out.append({"scene": cls.name, "sub": nm, "en" if isinstance(b, ast.Constant) else
                                            "tpl": b.value if isinstance(b, ast.Constant) else ast.unparse(b)})
    return out


def templates(video: str) -> dict:
    """{source text: (regex, [placeholder names])} for every f-string and voiceover template of the video."""
    nodes = []
    for f in sorted(video_dir(video).glob("s[0-9][0-9]_*.py")):
        tree = ast.parse(f.read_text())
        nodes += [n for n in ast.walk(tree) if isinstance(n, ast.JoinedStr)]
        for a in _voiceover_args(tree):
            nodes += _branches(a)
    out = {}
    for n in nodes:
        if not isinstance(n, (ast.JoinedStr, ast.BinOp)):
            continue
        rx, names = "", []
        for kind, v in _parts(n):
            if kind == "text":
                rx += r"\s*".join(re.escape(w) for w in v.split(" "))
            else:
                rx += "(.*?)"
                names.append(v)
        out[ast.unparse(n)] = (re.compile("^" + rx + "$", re.S), names)
    return out


class Translator:
    def __init__(self, video: str):
        t = table(video)
        self.zh, self.phrases = t["ZH"], t["PHRASES"]
        self.tpls = templates(video)

    def value(self, v: str, depth: int) -> str:
        if v in self.phrases:
            return self.phrases[v]
        if depth < 3 and len(v) > 25 and " " in v:
            z = self(v, depth + 1)
            if z is not None:
                return z
        return v.replace(",", "") if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", v) else v

    def __call__(self, en: str, depth: int = 0) -> str | None:
        hits = [k for k in self.zh if not IS_TPL(k) and en.startswith(k)]
        if hits:
            return self.zh[max(hits, key=len)]
        for key, tr in self.zh.items():
            if not IS_TPL(key):
                continue
            for src in [s for s in self.tpls if s.startswith(key)]:
                rx, names = self.tpls[src]
                m = rx.match(en)
                if m:
                    vals = {n: self.value(v, depth) for n, v in zip(names, m.groups())}
                    out = re.sub(r"\{([^{}]+)\}", lambda mm: vals.get(mm.group(1), mm.group(0)), tr)
                    left = re.findall(r"\{[^{}]+\}", out)
                    if left:
                        sys.exit(f"{key[:60]}...: no value for {left} (the translation's placeholders must be "
                                 f"spelled as in the source: {names})")
                    return out



def todo(video: str, scenes: list[str]) -> int:
    zh = table(video)["ZH"]
    src = sources(video)
    used, left = set(), []
    for x in src:
        s = x.get("en") or x["tpl"]
        hits = [k for k in zh if s.startswith(k)]
        if len(hits) > 1 and not all(h in hits[0] or hits[0] in h for h in hits):
            print("AMBIGUOUS:", [h[:50] for h in hits])
        used.update(hits)
        if not hits:
            left.append(x)
    unused = [k for k in zh if k not in used]
    if unused:
        print("table keys that match no source line:", [k[:60] for k in unused])
    print(f"{len(src) - len(left)} of {len(src)} source lines covered")
    for x in left:
        if scenes and x["scene"] not in scenes:
            continue
        kind = f"spliced into {x['sub']}" if "sub" in x else ("template" if "tpl" in x else "line")
        print(f"\n## {x['scene']} ({kind})\n{x.get('en') or x['tpl']}")
    return len(left)


def fill(video: str, lang: str) -> int:
    t = table(video)
    tr = Translator(video)
    path = video_dir(video) / f"narration_{lang}.json"
    if not path.exists():
        sys.exit(f"no {path.name}: run tools/translate_narration.py {video} --lang {lang} first")
    nar = json.loads(path.read_text())
    filled = missing = 0
    for e in nar["lines"].values():
        out = tr(e["en"])
        if out is None:
            missing += 1
            print("MISSING", e["scene"], e["en"][:100])
            continue
        if e.get(lang) != out:
            e[lang], filled = out, filled + 1
    if t["TITLE"]:
        nar["title"] = t["TITLE"]
    for cls, title in t["CHAPTERS"].items():
        if cls in nar.get("chapters", {}):
            nar["chapters"][cls] = title
    path.write_text(json.dumps(nar, ensure_ascii=False, indent=1) + "\n")
    print(f"{path.relative_to(ROOT)}: {filled} line(s) updated, {missing} missing")
    return missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("video")
    ap.add_argument("scenes", nargs="*", help="with --todo: only these scene classes")
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--lang", default="zh")
    args = ap.parse_args()
    if args.todo:
        todo(args.video, args.scenes)
    else:
        sys.exit(1 if fill(args.video, args.lang) else 0)


if __name__ == "__main__":
    main()
