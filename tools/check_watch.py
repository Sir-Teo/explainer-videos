#!/usr/bin/env python
"""Does a part meet the watch standard (videos/cs/SYLLABUS.md, section 1.2)?  Read from the scene source, before
anything is rendered.

    python tools/check_watch.py cs7                # one part: each check, and each chapter's numbers
    python tools/check_watch.py --series cs        # one line per part (exit 1 if any fails)

The checks:

* **cold open**: the first scene's first narration is not "This is Part ...", it shows no chapter card,
  objectives card or series map before the first line, and it calls ``self.title(...)`` after it;
* **no objectives card** anywhere (the cold open's question is the objective);
* **predictions**: every numbered chapter calls ``self.predict(...)`` at least once;
* **checkpoints**: at least one ``self.checkpoint(...)`` per 15 estimated minutes, and at least two;
* **a misconception**: at least one ``self.wrong_idea(...)``;
* **motion**: moving animations (transforms, ``.animate``, trackers, updaters, camera moves, live instruments)
  per ``FadeIn``, at least :data:`MOTION_FLOOR` over the part;
* **narration**: sentences average at most :data:`SENTENCE_MAX` words, and at most :data:`HEDGE_MAX` spoken
  hedges (caveats belong on a ``tag(...)`` or in the notes).

It reads source only; ``tools/lecture_length.py`` gives the running time and ``tools/contact_sheet.py`` the look.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import video_dir, video_package  # noqa: E402

MOTION_FLOOR = 0.25
SENTENCE_MAX = 22.0
HEDGE_MAX = 6
WPM = 140

MOTION_CALLS = {"Transform", "ReplacementTransform", "TransformFromCopy", "TransformMatchingTex",
                "TransformMatchingShapes", "ClockwiseTransform", "CounterclockwiseTransform", "MoveToTarget",
                "MoveAlongPath", "Rotate", "Rotating", "Homotopy", "ApplyMatrix", "ApplyPointwiseFunction",
                "ValueTracker", "always_redraw", "frame_to", "frame_home", "morph", "Wiggle", "CyclicReplace",
                "Swap", "GrowArrow", "GrowFromEdge", "GrowFromPoint", "GrowFromCenter", "SpinInFromNothing"}
MOTION_METHODS = {"add_updater", "zoom", "home", "advance", "cycle", "become", "move_camera", "rewrite"}
NARRATED = {"predict", "reveal", "checkpoint", "wrong_idea", "ask", "chapter"}  # kit calls that speak
HEDGES = [r"\bnot an? (measured|physical|recording|proof|guarantee|certification|silicon)\b", r"\bassumed\b",
          r"\billustrative\b", r"\bthis does not (mean|prove|test)\b", r"\bnot an absolute\b",
          r"\bdoes not (prove|establish|certify|isolate|guarantee|imply)\b", r"\bnot (necessarily|automatically)\b",
          r"\bunder (these|stated|our) assumptions\b", r"\bkeep (measurements|in mind)\b", r"\bto be clear\b",
          r"\bin (this|our|that) (model|simulation)\b", r"\bteaching (budget|model)\b", r"\bwe have not\b",
          r"\bnot literally\b", r"\bnot (every|all) \w+ (designs|predictors|processors|machines|systems)\b",
          r"\bonly an? (sketch|model|illustration)\b"]


def _strings(node) -> str:
    """The narration a call speaks: its string constants, with ``{...}`` placeholders as one word."""
    out = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.append(sub.value)
        elif isinstance(sub, ast.FormattedValue):
            out.append(" N ")
    return re.sub(r"<bookmark[^>]*/>", " ", "".join(out))


def _name(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _in_construct(cls_node, call) -> bool:
    """Is ``call`` written in the scene's ``construct`` (which only lists the sections, in order)?"""
    for f in cls_node.body:
        if isinstance(f, ast.FunctionDef) and f.name == "construct":
            return f.lineno <= call.lineno <= f.end_lineno
    return False


def chapter_stats(path: Path, cls: str) -> dict:
    tree = ast.parse(path.read_text())
    node = next((n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls), None)
    st = {"fade": 0, "motion": 0, "predict": 0, "checkpoint": 0, "wrong_idea": 0, "title": 0, "objectives": 0,
          "narration": [], "first": None, "before_first": set()}
    if node is None:
        return st
    calls = sorted((c for c in ast.walk(node) if isinstance(c, ast.Call)), key=lambda c: (c.lineno, c.col_offset))
    for c in calls:
        n = _name(c)
        if n == "FadeIn":
            st["fade"] += 1
        if n in MOTION_CALLS or (isinstance(c.func, ast.Attribute) and n in MOTION_METHODS):
            st["motion"] += 1
        if n in ("predict", "checkpoint", "wrong_idea", "title", "ask") and isinstance(c.func, ast.Attribute):
            st["predict" if n == "ask" else n] += 1
        if n == "objectives_card":
            st["objectives"] += 1
        spoken = None
        if n == "voiceover" and c.args:
            spoken = c.args[0]
        elif n in NARRATED:
            spoken = next((k.value for k in c.keywords if k.arg in ("narration", "say", "said")), None)
            extra = [k.value for k in c.keywords if k.arg in ("right_narration", "answers_narration", "reveal")]
            for e in extra:
                st["narration"].append(_strings(e))
        if spoken is not None:
            text = _strings(spoken)
            if st["first"] is None:
                st["first"] = text
            st["narration"].append(text)
        elif st["first"] is None and n in ("chapter_card", "objectives_card", "series_map") and \
                not _in_construct(node, c):
            st["before_first"].add(n)
    # .animate attribute accesses
    st["motion"] += sum(1 for a in ast.walk(node) if isinstance(a, ast.Attribute) and a.attr == "animate")
    return st


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.?!])\s+", " ".join(text.split())) if len(s.split()) > 1]


def check(video: str) -> dict:
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    rows, problems = [], []
    tot = {"fade": 0, "motion": 0, "checkpoint": 0, "wrong_idea": 0}
    words, sents, hedges = 0, [], []
    first = None
    for k, (module, cls, chapter) in enumerate(manifest.SCENES):
        src = video_dir(video) / f"{module}.py"
        if not src.exists():
            rows.append((chapter, None))
            continue
        st = chapter_stats(src, cls)
        if k == 0:
            first = st
        for key in tot:
            tot[key] += st[key]
        text = " ".join(st["narration"])
        words += len(text.split())
        sents += sentences(text)
        for h in HEDGES:
            hedges += [(chapter, m.group(0)) for m in re.finditer(h, text, re.I)]
        numbered = bool(re.match(r"\s*\d+\.", chapter))
        if numbered and st["predict"] == 0:
            problems.append(f"no prediction in '{chapter}'")
        if st["objectives"]:
            problems.append(f"an objectives card in '{chapter}' (the cold open's question replaces it)")
        rows.append((chapter, st))
    minutes = words / WPM
    if first is not None:
        if first["first"] and re.match(r"\s*(this is part|welcome|in this part|today)", first["first"], re.I):
            problems.append("the cold open starts on the part, not the phenomenon: " + first["first"][:60])
        if first["before_first"]:
            problems.append("before the first line the cold open shows " + ", ".join(sorted(first["before_first"])))
        if not first["title"]:
            problems.append("the first scene never calls self.title(...) after its cold open")
    need = max(2, int(minutes // 15))
    if tot["checkpoint"] < need:
        problems.append(f"{tot['checkpoint']} checkpoint(s); {need} needed for ~{minutes:.0f} min")
    if tot["wrong_idea"] < 1:
        problems.append("no misconception (self.wrong_idea)")
    ratio = tot["motion"] / max(1, tot["fade"])
    if ratio < MOTION_FLOOR:
        problems.append(f"motion ratio {ratio:.2f} < {MOTION_FLOOR}")
    mean = sum(len(s.split()) for s in sents) / max(1, len(sents))
    if mean > SENTENCE_MAX:
        problems.append(f"sentences average {mean:.1f} words (> {SENTENCE_MAX:.0f})")
    if len(hedges) > HEDGE_MAX:
        problems.append(f"{len(hedges)} spoken hedges (> {HEDGE_MAX}): " +
                        "; ".join(f"{h} ({c[:24]})" for c, h in hedges[:8]))
    return {"video": video, "rows": rows, "problems": problems, "ratio": ratio, "minutes": minutes,
            "sentence": mean, "hedges": len(hedges), **tot}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--series")
    args = ap.parse_args(argv)
    vids = list(args.videos)
    if args.series:
        from explainer.paths import VIDEOS

        base = VIDEOS / args.series
        vids += sorted((p.name for p in base.iterdir() if (p / "manifest.py").exists()),
                       key=lambda s: int(re.sub(r"\D", "", s) or 0))
    bad = 0
    for v in vids:
        r = check(v)
        ok = not r["problems"]
        bad += not ok
        if len(vids) == 1:
            print(f"{v}: ~{r['minutes']:.0f} min of narration, motion {r['ratio']:.2f}, sentences {r['sentence']:.1f}"
                  f" words, {r['hedges']} hedges, {r['checkpoint']} checkpoints, {r['wrong_idea']} misconception(s)")
            for chapter, st in r["rows"]:
                if st is None:
                    print(f"  {chapter:52s} (not written yet)")
                    continue
                m = st["motion"] / max(1, st["fade"])
                print(f"  {chapter[:52]:52s} motion {m:4.2f}  predict {st['predict']}  checkpoint {st['checkpoint']}")
            print("PASS" if ok else "FAIL:\n  " + "\n  ".join(r["problems"]))
        else:
            print(f"{v:8s} {'pass' if ok else 'FAIL'}  motion {r['ratio']:.2f}  sent {r['sentence']:4.1f}  hedges "
                  f"{r['hedges']:3d}  checkpoints {r['checkpoint']}  ({len(r['problems'])} problem(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
