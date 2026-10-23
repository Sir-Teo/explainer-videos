#!/usr/bin/env python
"""Keep a video's narration translation in step with its English narration.

    python tools/translate_narration.py analysis1 --lang zh            # update the table, then validate it
    python tools/translate_narration.py analysis1 --lang zh --check    # validate only (exit 1 on problems)

The English lines come from the latest render's ``.narration.json`` files (``raw`` keeps each line's bookmarks),
so lines computed from data are included exactly as spoken.  ``videos/<video>/narration_<lang>.json`` maps a hash
of each English line to its translation (see ``explainer/lang.py``); this tool adds new lines with an empty
translation, drops lines the scenes no longer say, adds the chapter titles, and checks every translation:
same bookmarks in the same order, nothing left empty, nothing untranslated.
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402

from explainer import lang as L  # noqa: E402

BOOKMARK = re.compile(r"<bookmark\s+mark\s*=\s*['\"]([^'\"]+)['\"]\s*/>")


def english_lines(video: str) -> list[tuple[str, str]]:
    """[(scene class, English line with bookmarks)] in film order, from the newest render of each scene."""
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    out = []
    for module, cls, _ in manifest.SCENES:
        metas = sorted((ROOT / "media" / video / "videos" / module).glob(f"*/{cls}.narration.json"),
                       key=lambda p: p.stat().st_mtime)
        if not metas:
            sys.exit(f"no render of {cls} yet: build {video} first (any quality)")
        for line in json.loads(metas[-1].read_text())["lines"]:
            if "raw" not in line:
                sys.exit(f"{metas[-1]} predates bookmark recording: re-render {cls}")
            out.append((cls, line["raw"]))
    return out


def problems(en: str, tr: str, lang: str) -> list[str]:
    out = []
    if not tr.strip():
        return ["empty"]
    if BOOKMARK.findall(en) != BOOKMARK.findall(tr):
        out.append(f"bookmarks {BOOKMARK.findall(en)} -> {BOOKMARK.findall(tr)}")
    if lang == "zh":
        plain = BOOKMARK.sub("", tr)
        cjk = len(re.findall(r"[一-鿿]", plain))
        latin = re.findall(r"[A-Za-z]{4,}", plain)
        # a short line that is mostly a name ("第12章。AlphaGo。") is translated; English left as it was is not
        if cjk == 0 or (cjk < 0.5 * len(re.sub(r"\s", "", plain)) and len(latin) > 2):
            out.append("mostly untranslated")
        if latin:
            out.append(f"Latin words left: {sorted(set(latin))[:6]}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--allow-latin", default="", help="comma-separated words allowed to stay in Latin script")
    args = ap.parse_args()
    path = video_dir(args.video) / f"narration_{args.lang}.json"
    table = json.loads(path.read_text()) if path.exists() else {}
    table.setdefault("title", "")
    table.setdefault("chapters", {})
    old = table.get("lines", {})

    if not args.check:
        manifest = importlib.import_module(f"{video_package(args.video)}.manifest")
        lines = {}
        for cls, en in english_lines(args.video):
            k = L.key(en)
            prev = old.get(k, {})
            lines[k] = {"scene": cls, "en": " ".join(en.split()), args.lang: prev.get(args.lang, "")}
        dropped = set(old) - set(lines)
        table["lines"] = lines
        table["title_en"] = manifest.TITLE
        for _, cls, title in manifest.SCENES:
            table["chapters"].setdefault(cls, "")
        table["chapters_en"] = {cls: title for _, cls, title in manifest.SCENES}
        path.write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n")
        print(f"{path.relative_to(ROOT)}: {len(lines)} lines ({len(dropped)} dropped)")

    allowed = {w for w in args.allow_latin.split(",") if w}
    bad = 0
    for k, e in table["lines"].items():
        ps = problems(e["en"], e.get(args.lang, ""), args.lang)
        ps = [p for p in ps if not (p.startswith("Latin words left") and
                                    set(re.findall(r"'([^']+)'", p)) <= allowed)]
        if ps:
            bad += 1
            if not args.check or bad <= 40:
                print(f"  {k} {e['scene']}: {'; '.join(ps)}")
    missing_ch = [c for c, t in table["chapters"].items() if not t]
    if not table.get("title"):
        missing_ch.append("<title>")
    print(f"{bad} line(s) with problems; {len(missing_ch)} untranslated title(s)")
    sys.exit(1 if args.check and (bad or missing_ch) else 0)


if __name__ == "__main__":
    main()
