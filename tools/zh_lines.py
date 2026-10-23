#!/usr/bin/env python
"""Fill a video's narration translation from a table of translated source lines, templates included.

    python tools/zh_lines.py ai27 --todo [Scene ...]   # source lines the table doesn't cover yet
    python tools/zh_lines.py ai27                      # fill narration_zh.json (after translate_narration.py)
    python tools/zh_lines.py ai27 --verify             # will every line of the latest render translate? (exit 1 if not)

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
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir  # noqa: E402
from explainer.zh_templates import IS_TPL, Translator, sources, table  # noqa: E402,F401

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
            if not e.get(lang):  # a line the table doesn't cover keeps a translation made by hand
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


def verify(video: str, lang: str) -> int:
    """Every line of the latest English render must translate, from narration_<lang>.json or the templates, with its
    bookmarks: what a Chinese build needs. Run it before a long build."""
    import os

    os.environ["EXPLAINER_LANG"] = lang
    from explainer import lang as L
    from tools.translate_narration import english_lines, problems

    L.LANG = lang
    bad = latin = 0
    for cls, en in english_lines(video):
        try:
            out = L.translate(en, video_dir(video), cls)
            ps = problems(en, out, lang)
        except KeyError:
            ps = ["no translation"]
        # names kept in Latin script (NVLink, PyTorch) are a style choice, not a failure: a build only breaks on a
        # missing translation or mismatched bookmarks
        latin += any(p_.startswith("Latin words left") for p_ in ps)
        ps = [p_ for p_ in ps if not p_.startswith("Latin words left")]
        if ps:
            bad += 1
            print(f"  {cls}: {'; '.join(ps)}: {' '.join(en.split())[:100]}")
    print(f"{video}: {bad} narration line(s) won't translate ({latin} keep Latin-script names)")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("video")
    ap.add_argument("scenes", nargs="*", help="with --todo: only these scene classes")
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--lang", default="zh")
    args = ap.parse_args()
    if args.todo:
        todo(args.video, args.scenes)
    elif args.verify:
        sys.exit(1 if verify(args.video, args.lang) else 0)
    else:
        sys.exit(1 if fill(args.video, args.lang) else 0)


if __name__ == "__main__":
    main()
