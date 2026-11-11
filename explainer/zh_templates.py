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


@lru_cache(maxsize=16384)
def _source_body(s: str) -> str:
    match = re.match(r"(f?)(\"\"\"|'''|\"|')", s)
    quote = match[2]
    text = s[match.end():]
    closed = False
    if text.endswith(quote):
        try:
            node = ast.parse(s, mode="eval").body
        except SyntaxError:
            pass
        else:
            if isinstance(node, (ast.Constant, ast.JoinedStr)):
                text = text[:-len(quote)]
                closed = True
    # Preserve a complete key's closing delimiter. It must not become a prefix
    # of a different conditional branch with another sentence appended.
    return match[1] + text.replace("\\'", "'").replace('\\"', '"') + ("\0" if closed else "")


def source_startswith(source: str, prefix: str) -> bool:
    """Match source prefixes independently of ast.unparse's outer quote choice.

    F-string quoting can change when a computed expression uses a string key or
    an English sentence gains an apostrophe. Both spellings describe the same
    template; translation keys are often deliberately incomplete expressions.
    """
    if source.startswith(prefix):
        return True
    if not (IS_TPL(source) and IS_TPL(prefix)):
        return False

    return _source_body(source).startswith(_source_body(prefix))


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
    for f in sorted(video_dir(video).glob("s[0-9][0-9]*_*.py")):
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
    for f in sorted(video_dir(video).glob("s[0-9][0-9]*_*.py")):
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


_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = dict(zip("twenty thirty forty fifty sixty seventy eighty ninety".split(), range(20, 100, 10)))


def spoken_int(v: str) -> int | None:
    """A whole number spelled out in English ('one hundred and ten', 'twenty-three thousand'), or None."""
    if "," in v:
        return None                                       # a list, not one number
    words = v.lower().replace("-", " ").split()
    if not words or any(w not in _ONES and w not in _TENS and w not in ("hundred", "thousand", "million", "billion", "and")
                        for w in words) or words[0] == "and" or words[-1] == "and":
        return None
    if any(w == "and" and words[i - 1] not in ("hundred", "thousand", "million", "billion")
           for i, w in enumerate(words)):
        return None                                       # 'two and three' is a list, not five
    total = part = 0
    for w in words:
        if w in _ONES:
            part += _ONES.index(w)
        elif w in _TENS:
            part += _TENS[w]
        elif w == "hundred":
            part = (part or 1) * 100
        elif w in ("thousand", "million", "billion"):
            total += (part or 1) * {"thousand": 10 ** 3, "million": 10 ** 6, "billion": 10 ** 9}[w]
            part = 0
    return total + part


def spoken_number(v: str) -> str | None:
    """A number spelled out in English, whole ('one hundred and ten') or with spoken decimals ('two point eight
    five'), as digits; None if ``v`` is anything else."""
    whole, _, frac = v.partition(" point ")
    n = spoken_int(whole)
    if n is None:
        return None
    if not frac:
        return str(n)
    digits = frac.split()
    if not digits or any(d not in _ONES[:10] for d in digits):
        return None
    return f"{n}." + "".join(str(_ONES.index(d)) for d in digits)


_ORDINAL = {"first": "one", "second": "two", "third": "three", "fifth": "five", "eighth": "eight", "ninth": "nine",
            "twelfth": "twelve"}
_UNITS = {"milliseconds": "毫秒", "millisecond": "毫秒", "seconds": "秒", "second": "秒", "percent": "%"}


def spoken_ordinal(v: str) -> str | None:
    """An ordinal spelled out in English ('twenty-first', 'hundredth') as digits, or None."""
    m = re.fullmatch(r"(.*?[ -]?)([a-z]+)", v)
    if not m:
        return None
    head, last = m.groups()
    if last in _ORDINAL:
        base = _ORDINAL[last]
    elif last.endswith("ieth"):
        base = last[:-4] + "y"
    elif last.endswith("th"):
        base = last[:-2]
    else:
        return None
    return spoken_number(head + base)


def spoken_quantity(v: str) -> str | None:
    """A spelled-out number with a unit ('nine hundred and seven milliseconds') in Chinese digits and unit."""
    num, _, unit = v.rpartition(" ")
    if unit not in _UNITS:
        return None
    n = spoken_number(num)
    return None if n is None else n + _UNITS[unit]


def spoken_list(v: str) -> str | None:
    """A comma-separated list of spelled-out numbers ('twelve, plus forty, plus six' or 'one, two and three') as
    digits joined the Chinese way (12加40加6, 1、2和3); None if ``v`` is anything else."""
    parts = v.split(", ")
    if len(parts) < 2:
        return None
    out = []
    for i, p in enumerate(parts):
        sep = "、" if i else ""
        for word, zh in (("plus ", "加"), ("and ", "和")):
            if i and p.startswith(word):
                p, sep = p[len(word):], zh
        if i == len(parts) - 1 and " and " in p and spoken_number(p) is None:
            a, _, b = p.rpartition(" and ")
            if spoken_number(a) is None or spoken_number(b) is None:
                return None
            out += [sep, spoken_number(a), "和", spoken_number(b)]
            continue
        n = spoken_number(p)
        if n is None:
            return None
        out += [sep, n]
    return "".join(out)


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
        n = spoken_number(v)
        for alt in (spoken_list, spoken_quantity, spoken_ordinal):
            if n is None:
                n = alt(v)
        if n is not None:
            return n                                  # a number spelled out for the English voice: digits in Chinese
        return v.replace(",", "") if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", v) else v

    def __call__(self, en: str, depth: int = 0) -> str | None:
        hits = [k for k in self.zh if not IS_TPL(k) and en.startswith(k)]
        if hits:
            return self.zh[max(hits, key=len)]
        # the longest key first, as for literal lines: two branches that begin alike keep their own translations
        for key, tr in sorted(self.zh.items(), key=lambda kv: -len(kv[0])):
            if not IS_TPL(key):
                continue
            for src in [s for s in self.tpls if source_startswith(s, key)]:
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
