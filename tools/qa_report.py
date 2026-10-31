#!/usr/bin/env python
"""Build an offline index of chapter QA evidence: python tools/qa_report.py."""

import html
import hashlib
import importlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.make import all_videos  # noqa: E402
from tools.qa_series import OUT, fingerprint, inputs_current  # noqa: E402


def main():
    review_file = OUT / "review.json"
    review = json.loads(review_file.read_text()) if review_file.exists() else {}
    reviewed = review.get("manual_contact_sheet_review", {})
    proofs = review.get("manual_evidence", {})

    def sheet_reviewed(video, lang, scene, motion=False):
        kind = "motion" if motion else "endpoints"
        proof = proofs.get(f"{video}/{lang}/{scene}/{kind}", {})
        image = OUT / video / lang / (scene + ("_motion" if motion else "")) / ("motion_sheet.png" if motion else "sheet.png")
        return image.exists() and proof.get("sheet_sha256") == hashlib.sha256(image.read_bytes()).hexdigest()
    blocks, checked, total, issues = [], 0, 0, 0
    for video in all_videos("ai"):
        key = fingerprint(video)
        manifest = importlib.import_module(f"videos.ai.{video}.manifest")
        rows = []
        for lang in ("en", "zh"):
            for _, scene, title in manifest.SCENES:
                total += 1
                folder = OUT / video / lang / scene
                path = folder / "result.json"
                result = json.loads(path.read_text()) if path.exists() else {}
                status = result.get("status", "not checked")
                warnings = result.get("warnings", [])
                current = result.get("fingerprint") == key and inputs_current(result)
                if result:
                    checked += 1
                if status != "passed" or warnings or not current:
                    issues += 1
                color = "good" if status == "passed" and not warnings and current else "pending"
                badge = status + ("; earlier source/data" if result and not current else "")
                rel = folder.relative_to(OUT)
                links = []
                if (folder / "sheet.png").exists():
                    links.append(f'<a href="{rel}/sheet.png">contact sheet</a>')
                if (folder / "render.log").exists():
                    links.append(f'<a href="{rel}/render.log">log</a>')
                if path.exists():
                    links.append(f'<a href="{rel}/result.json">details</a>')
                narrated_folder = OUT.parent / "narrated" / video / lang
                narrated_path = narrated_folder / f"{scene}_result.json"
                if narrated_path.exists():
                    narrated = json.loads(narrated_path.read_text())
                    movie_rel = Path(os.path.relpath(ROOT / narrated["movie"], OUT))
                    sheet_rel = Path(os.path.relpath(narrated_folder / f"{scene}_sheet.png", OUT))
                    links.append(f'<a href="{movie_rel}">narrated preview</a>')
                    links.append(f'<a href="{sheet_rel}">narrated frames</a>')
                detail = result.get("error", "")
                if warnings:
                    detail += f" ({len(warnings)} warnings)"
                review_key = video if lang == "en" else f"{video}_zh"
                visual_review = ("contact sheet reviewed" if sheet_reviewed(video, lang, scene) else
                                 "earlier contact sheet reviewed" if scene in reviewed.get(review_key, []) else
                                 "pending visual review")
                motion_folder = folder.with_name(scene + "_motion")
                motion_path = motion_folder / "result.json"
                motion = json.loads(motion_path.read_text()) if motion_path.exists() else {}
                motion_detail = motion.get("status", "not rendered")
                if motion:
                    if motion.get("fingerprint") != key or not inputs_current(motion):
                        motion_detail += "; earlier source/data"
                    if motion.get("warnings"):
                        motion_detail += f'; {len(motion["warnings"])} warnings'
                    motion_detail += "; motion sheet reviewed" if sheet_reviewed(video, lang, scene, True) else "; pending visual review"
                    motion_rel = motion_folder.relative_to(OUT)
                    contact = "motion_sheet.png" if (motion_folder / "motion_sheet.png").exists() else "sheet.png"
                    links.append(f'<a href="{motion_rel}/{contact}">motion frames</a>')
                    links.append(f'<a href="{motion_rel}/result.json">motion details</a>')
                    if motion.get("movie"):
                        movie_rel = (ROOT / motion["movie"]).relative_to(OUT)
                        links.append(f'<a href="{movie_rel}">silent video</a>')
                audio_path = folder / "audio_result.json"
                audio_detail = "not checked"
                if audio_path.exists():
                    audio = json.loads(audio_path.read_text())
                    audio_detail = f'{len(audio["lines"])}/{audio.get("expected_lines", "?")} lines; {len(audio["issues"])} signal/timing issues'
                    leads = sum(len(line.get("asr_review_leads", [])) for line in audio["lines"])
                    if leads:
                        audio_detail += f"; {leads} ASR review leads"
                    audio_input = ROOT / audio.get("input_record", "missing")
                    audio_current = False
                    if audio_input.is_file():
                        raw = audio_input.read_bytes()
                        capture = json.loads(raw)
                        audio_current = (audio.get("input_sha256") == hashlib.sha256(raw).hexdigest()
                                         and capture.get("fingerprint") == key and inputs_current(capture))
                    if not audio_current:
                        audio_detail += "; earlier source capture"
                    audio_detail += "; listening/playback pending"
                    links.append(f'<a href="{rel}/audio_result.json">audio details</a>')
                rows.append(f'<tr><td>{lang}</td><td>{html.escape(scene)}<small>{html.escape(title)}</small></td>'
                            f'<td class="{color}">{html.escape(badge)}<small>{html.escape(detail)}</small></td>'
                            f'<td>{visual_review}</td>'
                            f'<td>{html.escape(motion_detail)}</td>'
                            f'<td>{html.escape(audio_detail)}</td>'
                            f'<td>{" · ".join(links)}</td></tr>')
        blocks.append(f'<details><summary>{html.escape(manifest.TITLE)} — {len(manifest.SCENES)} chapters</summary>'
                      f'<table><thead><tr><th>Language</th><th>Chapter</th><th>Preflight</th><th>Visual review</th>'
                      f'<th>Silent playback</th><th>Narration</th><th>Evidence</th></tr>'
                      f'</thead><tbody>{"".join(rows)}</tbody></table></details>')
    OUT.mkdir(parents=True, exist_ok=True)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AI series QA</title><style>
body{font:16px/1.5 system-ui;margin:40px auto;max-width:1250px;padding:0 20px;background:#0e1117;color:#e6edf3}
h1{font-size:32px}p{max-width:950px;color:#b7c2ce}details{border:1px solid #334155;border-radius:8px;margin:12px 0}
summary{padding:18px;cursor:pointer;font-weight:650}table{border-collapse:collapse;width:100%;font-size:14px}
td,th{text-align:left;padding:12px;border-top:1px solid #334155;vertical-align:top}small{display:block;color:#9baabc}
a{color:#8ecaff}.good{color:#9ad886}.pending{color:#e5ba75}th{color:#9baabc}
</style><h1>AI series QA evidence</h1>'''
    page += (f'<p>{checked} of {total} language/chapter records have been attempted. '
             f'{issues} records are untested or need follow-up. Expand a part for its evidence.</p>'
             '<p>These are silent runtime and animation-endpoint layout checks. Contact sheets require visual review. '
             'Narrated playback and final-resolution masters require separate verification. '
             'Earlier-source records remain visible and are marked explicitly.</p>')
    legacy_path = OUT / "legacy_exports.json"
    if legacy_path.exists():
        exports = json.loads(legacy_path.read_text())
        page += (f'<details><summary>{len(exports)} legacy 4K exports — rebuild required</summary>'
                 '<p>The migration renamed files. Embedded titles and chapter coverage below belong to earlier '
                 'versions; these files do not establish production readiness.</p><table>'
                 '<tr><th>File</th><th>Embedded title</th><th>Chapter markers / current manifest</th></tr>')
        for export in exports:
            page += (f'<tr><td>{html.escape(export["file"])}</td>'
                     f'<td>{html.escape(export["embedded_title"])}</td>'
                     f'<td>{export["embedded_chapters"]} / {export["current_manifest_chapters"]}</td></tr>')
        page += '</table></details>'
    audio_path = OUT / "audio_cache_review.json"
    if audio_path.exists():
        audio = json.loads(audio_path.read_text())
        lines = sum(p["lines"] for p in audio["parts"].values())
        cached = sum(p["cached"] for p in audio["parts"].values())
        page += (f'<p><a href="audio_cache_review.json">Narration cache audit</a>: {cached} of {lines} lines from '
                 f'already rendered chapters have matching audio for {html.escape(audio["voice"])}. '
                 'This checks existing audio files; speech content and narrated synchronization still require review.</p>')
    page += "".join(blocks) + "</html>"
    path = OUT / "index.html"
    path.write_text(page)
    print(path)


if __name__ == "__main__":
    main()
