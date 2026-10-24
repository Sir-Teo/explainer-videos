"""Chinese narration from templates: each part's ``zh_lines.py`` translates its source lines, literal or computed.

The rendered English line is matched against the scene's source (a literal by prefix, an f-string or a sum of
strings and names as a template), and the values it was formatted with are carried into the translation.  Used by
``tools/zh_lines.py`` (to fill ``narration_zh.json`` and list what's missing) and by :mod:`explainer.lang` at render
time, so a line computed from data on another machine, with slightly different numbers, is still translated.
Needs Python 3.12: template keys are source text as ``ast.unparse`` prints it.
"""

from __future__ import annotations

import ast
import importlib.util
import re
from functools import lru_cache

from explainer.paths import video_dir

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
                rx += _NUMBER if numeric(v) else "(.*?)"
                names.append(v)
        out[ast.unparse(n)] = (re.compile("^" + rx + "$", re.S), names)
    return out


# a placeholder formatted as a number ({x:.2f}, {n:,}, {int(k)}, {len(runs)}) matches only a number, so it can't
# swallow the words around it
_NUMBER = r"([-+−]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?:e[-+]?\d+)?%?)"


def numeric(placeholder: str) -> bool:
    spec = placeholder.rsplit(":", 1)[1] if ":" in placeholder and not placeholder.endswith("]") else ""
    return bool(re.search(r"[dfge%n,]$", spec)) or bool(re.match(r"(int|len|round|abs)\(", placeholder))


def ambiguous(video: str) -> list[str]:
    """Templates where two computed values meet with only spaces between them ("{verdict} {hits}"): the matcher can't
    tell where one ends, so it may split them wrongly.  Put a bookmark or words between them."""
    out = []
    for src in templates(video):
        node = ast.parse(src, mode="eval").body
        parts = _parts(node)
        words = lambda k, v: k == "name" and not numeric(v)  # noqa: E731  (numbers can't run into each other's words)
        for (k1, v1), (k2, v2), (k3, v3) in zip(parts, parts[1:], parts[2:]):
            if words(k1, v1) and k2 == "text" and not v2.strip() and words(k3, v3):
                out.append(src)
                break
        else:
            if any(words(*a) and words(*b) for a, b in zip(parts, parts[1:])):
                out.append(src)
    return out


class Translator:
    def __init__(self, video: str):
        t = table(video)
        self.zh, self.phrases = t["ZH"], t["PHRASES"]
        self.title, self.chapters = t["TITLE"], t["CHAPTERS"]
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
        # the longest key first, as for literal lines: two branches that begin alike keep their own translations
        for key, tr in sorted(self.zh.items(), key=lambda kv: -len(kv[0])):
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
                        raise ValueError(f"{key[:60]}...: no value for {left} (the translation's placeholders must "
                                         f"be spelled as in the source: {names})")
                    return out


@lru_cache(maxsize=None)
def translator(video: str) -> Translator | None:
    """The video's template translator, or None if it has no ``zh_lines.py``."""
    return Translator(video) if (video_dir(video) / "zh_lines.py").exists() else None
