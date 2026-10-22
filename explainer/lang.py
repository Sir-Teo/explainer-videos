"""Narration language: English (the source) or a translation looked up by the English text.

``EXPLAINER_LANG=zh`` renders a video with Chinese narration.  Every ``self.voiceover(...)`` line is looked up in
``videos/<video>/narration_zh.json`` by a hash of its English text (bookmarks included), so the scene code stays
the single source of truth and a changed English line fails loudly instead of playing a stale translation.

Bookmarks and subtitles work on *tokens*: whitespace-separated words in English, and in Chinese one token per
character (with any punctuation attached) or per run of Latin letters and digits.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from functools import lru_cache
from pathlib import Path

from explainer.paths import video_dir

LANG = os.environ.get("EXPLAINER_LANG", "en")
# Set to a .jsonl path to record every English line whose translation is missing (and narrate it in English)
# instead of failing: how the lines to translate are gathered.
COLLECT = os.environ.get("EXPLAINER_COLLECT", "")

_CJK = "㐀-䶿一-鿿豈-﫿"
_IS_CJK = re.compile(f"[{_CJK}]")
# Chinese punctuation: closing marks stick to the token before them, opening marks to the token after.
_CLOSE = set("。，、；：？！”’）》」』】…—·%")
_OPEN = set("“‘（《「『【")


def key(en: str) -> str:
    return hashlib.sha1(" ".join(en.split()).encode()).hexdigest()[:12]


def tokens(text: str, lang: str | None = None) -> list[str]:
    """Display tokens.  Chinese tokens keep a leading space when the text had one (between Latin words)."""
    lang = lang or LANG
    if lang == "en":
        return text.split()
    out: list[str] = []
    pending_open = ""
    space = False  # whitespace since the last character
    latin = False  # the last token is a run of Latin letters / digits that the next one may extend
    for ch in text:
        if ch.isspace():
            space, latin = True, False
            continue
        if ch in _OPEN:
            pending_open += ch
            latin = False
        elif ch in _CLOSE:
            if out:
                out[-1] += ch
            else:
                pending_open += ch
            latin = False
        elif _IS_CJK.match(ch):
            out.append(pending_open + ch)
            pending_open, latin = "", False
        elif latin and not space:  # continues a Latin run ("1.414", "L^2")
            out[-1] += ch
        elif not ch.isalnum() and out and not space:  # ASCII punctuation after a character
            out[-1] += ch
        else:  # a new Latin run
            lead = " " if space and out and not _IS_CJK.match(out[-1].rstrip("".join(_CLOSE))[-1:] or "x") else ""
            out.append(lead + pending_open + ch)
            pending_open, latin = "", True
        space = False
    if pending_open and out:
        out[-1] += pending_open
    return out


def join(toks: list[str], lang: str | None = None) -> str:
    lang = lang or LANG
    return " ".join(toks) if lang == "en" else "".join(toks).strip()


def norm(s: str) -> str:
    """Letters, digits and CJK characters only: what alignment compares."""
    return re.sub(f"[^a-z0-9{_CJK}]", "", s.lower())


def clean(text: str, lang: str | None = None) -> str:
    """Collapse whitespace (and, in Chinese, drop the spaces next to CJK characters)."""
    text = " ".join(text.split())
    if (lang or LANG) != "en":
        text = re.sub(f"(?<=[{_CJK}，。、；：？！“”（）《》]) | (?=[{_CJK}，。、；：？！“”（）《》])", "", text)
    return text


SENTENCE_END = {"en": (".", "?", "!", ":", ";"), "zh": ("。", "？", "！", "：", "；", "”")}
CUE_CHARS = {"en": 72, "zh": 24}


@lru_cache(maxsize=None)
def _table(video_dir: str, lang: str) -> dict:
    path = Path(video_dir) / f"narration_{lang}.json"
    if not path.exists():
        return {"lines": {}, "chapters": {}}
    return json.loads(path.read_text())


def translate(text: str, video_dir: Path, scene: str) -> str:
    """The narration line in ``LANG`` for the English ``text`` (with its bookmarks)."""
    if LANG == "en":
        return text
    k = key(text)
    entry = _table(str(video_dir), LANG)["lines"].get(k)
    if entry and entry.get(LANG):
        return entry[LANG]
    # not in the table (a line computed from data that came out differently on this machine): the part's templates
    tr = _templates(video_dir, LANG)
    if tr is not None:
        out = tr(" ".join(text.split()))
        if out is not None and BOOKMARK.findall(out) == BOOKMARK.findall(text):
            return out
    if COLLECT:
        with open(COLLECT, "a") as f:
            f.write(json.dumps({"key": k, "scene": scene, "en": " ".join(text.split())}, ensure_ascii=False) + "\n")
        return text
    raise KeyError(f"{scene}: no {LANG} narration for line {k}: {text[:80]!r}... "
                   f"(add it to {video_dir.name}/narration_{LANG}.json)")


BOOKMARK = re.compile(r"<bookmark\s+mark\s*=\s*['\"]([^'\"]+)['\"]\s*/>")


def _templates(video_dir: Path, lang: str):
    """The part's template translator (``zh_lines.py``, see :mod:`explainer.zh_templates`), if it has one."""
    if lang != "zh" or not (Path(video_dir) / "zh_lines.py").exists():
        return None
    from explainer.zh_templates import translator

    return translator(Path(video_dir).name)


def chapter_title(video: str, cls: str, english: str, lang: str | None = None) -> str:
    lang = lang or LANG
    if lang == "en":
        return english
    root = video_dir(video)
    tr = _templates(root, lang)
    return (_table(str(root), lang).get("chapters", {}).get(cls) or (tr.chapters.get(cls) if tr else None)
            or english)


def video_title(video: str, english: str, lang: str | None = None) -> str:
    lang = lang or LANG
    if lang == "en":
        return english
    root = video_dir(video)
    tr = _templates(root, lang)
    return _table(str(root), lang).get("title") or (tr.title if tr else None) or english
