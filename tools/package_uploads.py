#!/usr/bin/env python
"""Verify a series' masters and lay them out for upload in renders/upload/<series name>/ (e.g. analysis-built/).

    python tools/package_uploads.py [--series analysis] [--parts 1 2] [--check-only]
    python tools/package_uploads.py --series ai --parts 1

Per part and language: the master (hard link), .srt, thumbnail.jpg, youtube.txt and bilibili.txt (title,
description with chapters, tags). Text comes from videos/<series>/<series>_upload.json (videos/analysis/
analysis_upload.json for Analysis, Built); the parts are the videos <series>1, <series>2, ...
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from explainer.paths import VIDEOS, video_dir, video_package  # noqa: E402

# set by configure(): the series, its upload text, its kit's folder and file-name prefix
SERIES, DATA, OUT, KIT = "", {}, Path(), ""


def configure(series: str) -> None:
    global SERIES, DATA, OUT, KIT
    SERIES = series
    DATA = json.loads((VIDEOS / series / f"{series}_upload.json").read_text())
    KIT = re.sub(r"[^a-z0-9]+", "-", DATA["series"]["en"]["name"].lower()).strip("-")  # "analysis-built"
    OUT = ROOT / "renders" / "upload" / KIT
REPO_URL = "https://github.com/Sir-Teo/explainer-videos"
BG = (14, 17, 23)  # the videos' background, #0E1117
YELLOW, WHITE, GREY = (247, 209, 84), (240, 240, 240), (150, 156, 166)
FONT_EN = "/opt/homebrew/Cellar/texlive/20260301/share/texmf-dist/fonts/opentype/public/lm/lmroman10-regular.otf"
FONT_ZH = "/System/Library/Fonts/Supplemental/Songti.ttc"
LANG_CODE = {"en": "eng", "zh": "chi"}


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_chapters", "-show_format",
                           "-of", "json", str(path)]))


def loudness(path: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-v", "info", "-i", str(path), "-vn", "-af", "ebur128", "-f", "null",
                          "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def srt_cues(path: Path) -> list[tuple[float, float]]:
    def secs(ts):
        h, m, s = ts.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    return [(secs(a), secs(b)) for a, b in re.findall(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", path.read_text())]


def stamp(t: float, long: bool, pad: bool = False) -> str:
    t = int(t)
    h, m, s = t // 3600, t // 60 % 60, t % 60
    if pad:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{h}:{m:02d}:{s:02d}" if long else f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def verify(video: str, lang: str, mp4: Path, srt: Path) -> dict:
    manifest = importlib.import_module(f"{video_package(video)}.manifest")
    info = probe(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    subs = [s for s in info["streams"] if s["codec_type"] == "subtitle"]
    dur = float(info["format"]["duration"])
    cues = srt_cues(srt)
    q = {
        "width": v["width"], "height": v["height"], "fps": v["r_frame_rate"], "video_codec": v["codec_name"],
        "audio_codec": a["codec_name"], "audio_sample_rate": int(a["sample_rate"]), "audio_channels": a["channels"],
        "audio_kbps": round(int(a.get("bit_rate", 0)) / 1000),
    }
    problems = []
    if (q["width"], q["height"], q["fps"], q["video_codec"]) != (3840, 2160, "60/1", "h264"):
        problems.append(f"video is {q['width']}x{q['height']} {q['fps']} {q['video_codec']}")
    if (q["audio_codec"], q["audio_sample_rate"]) != ("aac", 48000):
        problems.append(f"audio is {q['audio_codec']} {q['audio_sample_rate']} Hz")
    if not subs or subs[0].get("tags", {}).get("language") != LANG_CODE[lang]:
        problems.append("no subtitle track in the narration's language")
    if len(info["chapters"]) != len(manifest.SCENES):
        problems.append(f"{len(info['chapters'])} chapters for {len(manifest.SCENES)} scenes")
    if not cues or cues[-1][1] > dur + 0.5 or any(b < a for a, b in cues):
        problems.append("subtitles run past the video or have negative cues")
    lufs = loudness(mp4)
    if abs(lufs + 16) > 1.0:
        problems.append(f"loudness {lufs} LUFS")
    return {
        "video": video, "lang": lang, "file": str(mp4), "bytes": mp4.stat().st_size, "sha256": sha256(mp4),
        "duration_seconds": round(dur, 3), "quality": q, "loudness_LUFS": lufs, "caption_cues": len(cues),
        "chapters": [(float(c["start_time"]), c["tags"]["title"]) for c in info["chapters"]],
        "title": info["format"].get("tags", {}).get("title", ""), "problems": problems,
    }


# ---------------------------------------------------------------------------
# Thumbnails
# ---------------------------------------------------------------------------
def _segments(lines: list[dict], end: float) -> list[tuple[float, float]]:
    starts = [ln["start"] for ln in lines] + [end]
    return [(0.0, starts[0])] + list(zip(starts[:-1], starts[1:]))


def hero_frame(video: str, t480: float) -> Image.Image:
    """The opening chapter's frame at preview time t480, taken from the 4K English master at the same point of the
    narration (the voices differ, so the time is mapped line by line), as a full 3840x2160 image."""
    pre = ROOT / "media" / video / "videos" / "s01_hook" / "480p30" / "Hook.narration.json"
    k4 = ROOT / "media" / video / "crf16" / "videos" / "s01_hook" / "2160p60"
    a, b = json.loads(pre.read_text()), json.loads((k4 / "Hook.narration.json").read_text())
    sa, sb = _segments(a["lines"], a["duration"]), _segments(b["lines"], b["duration"])
    i = next((k for k, (s, e) in enumerate(sa) if s <= t480 < e), len(sa) - 1)
    f = (t480 - sa[i][0]) / max(sa[i][1] - sa[i][0], 1e-6)
    t4k = sb[i][0] + f * (sb[i][1] - sb[i][0])
    tmp = OUT / ".frames" / f"{video}.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t4k:.3f}", "-i", str(k4 / "Hook.mp4"), "-frames:v", "1", str(tmp)])
    return Image.open(tmp).convert("RGB")


SUP = {"ᵖ": "p", "ˢ": "s", "²": "2", "¹": "1"}  # superscripts the title fonts lack, drawn as raised small letters


def _segments_sup(text: str) -> list[tuple[str, bool]]:
    out: list[tuple[str, bool]] = []
    for ch in text:
        sup = ch in SUP
        ch = SUP.get(ch, ch)
        if out and out[-1][1] == sup:
            out[-1] = (out[-1][0] + ch, sup)
        else:
            out.append((ch, sup))
    return out


def _width(draw, text: str, font, sup_font) -> float:
    return sum(draw.textlength(t, font=sup_font if sup else font) for t, sup in _segments_sup(text))


def _draw_centred(draw, cx: float, y: float, text: str, font, sup_font, size: int, fill) -> None:
    x = cx - _width(draw, text, font, sup_font) / 2
    base = y + font.getmetrics()[0]
    for t, sup in _segments_sup(text):
        f = sup_font if sup else font
        draw.text((x, base - (0.42 * size if sup else 0)), t, font=f, fill=fill, anchor="ls")
        x += draw.textlength(t, font=f)


def _wrap(draw, text: str, font, sup_font, width: int, cjk: bool) -> list[str]:
    """One line if it fits; else the most balanced two lines, breaking after a comma or colon in English, and at
    punctuation or before 与 in Chinese (never inside a word); else greedy lines."""
    w = lambda t: _width(draw, t, font, sup_font)  # noqa: E731
    if w(text) <= width:
        return [text]
    best, best_cost = None, float("inf")
    for i in range(1, len(text)):
        if cjk:
            if text[i - 1] in "、，：；" or (text[i - 1] == "—" and text[i] != "—") or text[i] == "与":
                a, b, bonus = text[:i], text[i:], 0.0
            else:
                continue
        else:
            if text[i] != " ":
                continue
            a, b = text[:i], text[i + 1:]
            bonus = -0.08 * width if a[-1] in ",:;" else 0.0
        m = max(w(a), w(b))
        if m <= width and m + bonus < best_cost:
            best, best_cost = [a, b], m + bonus
    if best:
        return best
    units = list(text) if cjk else text.split(" ")
    lines, cur = [], ""
    for u in units:
        cand = cur + u if cjk or not cur else f"{cur} {u}"
        if w(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = u
    return lines + [cur] if cur else lines


def thumbnail(video: str, lang: str, hero: Image.Image, crop: list[float], dst: Path) -> None:
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    n = int(video.removeprefix(SERIES))
    part = DATA["parts"][video]
    cjk = lang == "zh"
    font_path = FONT_ZH if cjk else FONT_EN
    kicker = f"{DATA['series']['zh']['name']} · 第{n}部分" if cjk else f"{DATA['series']['en']['name']} · Part {n}"
    title = part["short_zh"] if cjk else part["short_en"]
    # the text stays inside the centre 4:3 (x 240..1680), which Bilibili's square-ish crops keep
    kf = ImageFont.truetype(font_path, 58)
    size = 112
    while True:
        tf, sf = ImageFont.truetype(font_path, size), ImageFont.truetype(FONT_EN, int(size * 0.62))
        lines = _wrap(d, title, tf, sf, 1380, cjk)
        if len(lines) <= 2 or size <= 72:
            break
        size -= 8
    y = 64
    d.text((W / 2, y), kicker, font=kf, fill=YELLOW, anchor="mt")
    y += 58 + 34
    for ln in lines:
        _draw_centred(d, W / 2, y, ln, tf, sf, size, WHITE)
        y += int(size * 1.18)
    # the hero picture fills the rest, letterboxed on the videos' own background
    x0, y0, x1, y1 = crop
    hw, hh = hero.size
    pic = hero.crop((int(x0 * hw), int(y0 * hh), int(x1 * hw), int(y1 * hh)))
    box_w, box_h = W - 120, H - (y + 30) - 40
    s = min(box_w / pic.width, box_h / pic.height)
    pic = pic.resize((int(pic.width * s), int(pic.height * s)), Image.LANCZOS)
    img.paste(pic, ((W - pic.width) // 2, y + 30 + (box_h - pic.height) // 2))
    img.save(dst, "JPEG", quality=92, optimize=True)


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
def texts(video: str, lang: str, ver: dict, rev: str) -> dict:
    n = int(video.removeprefix(SERIES))
    part, en, zh = DATA["parts"][video], DATA["series"]["en"], DATA["series"]["zh"]
    long = ver["duration_seconds"] >= 3600
    yt_ch = "\n".join(f"{stamp(t, long)} {title}" for t, title in ver["chapters"])
    bili_ch = "\n".join(f"{stamp(t, True, pad=True)} {title}" for t, title in ver["chapters"])
    src = f"{REPO_URL}/tree/{rev}/{video_dir(video).relative_to(ROOT)}"
    title_en = f"{en['name']}: Part {n}, {part['short_en']}"
    title_zh = ver["title"] if lang == "zh" else f"{zh['name']} · 第{n}部分：{part['short_zh']}"
    if lang == "en":
        yt_title = title_en
        yt_desc = (f"{part['summary_en']}\n\n{en['computed']}\n\nChapters\n{yt_ch}\n\n"
                   f"Source code, narration and every computation:\n{src}\n\n{en['credits']}\n")
        bili_title = f"{zh['name']} 第{n}部分：{part['short_zh']}（英文版）"
        bili_desc = (f"英文配音、英文字幕的原创数学视频；中文配音版另见合集。\n\n{part['summary_zh']}\n\n"
                     f"{part['summary_en']}\n\n章节 / Chapters\n{yt_ch}\n\n源代码：{src}\n\n{zh['credits']}")
    else:
        yt_title = f"{title_zh} | {title_en} (中文)"
        if len(yt_title) > 100:  # a long part name: keep the Chinese whole, shorten the English
            yt_title = f"{title_zh} | {en['name']}, Part {n} (中文)"
        yt_desc = (f"{part['summary_zh']}\n\n{zh['computed']}\n\n{part['summary_en']}\n\n章节 / Chapters\n{yt_ch}\n\n"
                   f"源代码 / Source code:\n{src}\n\n{zh['credits']}\n{en['credits']}\n")
        bili_title = title_zh
        bili_desc = (f"{part['summary_zh']}\n\n{zh['computed']}\n\n章节\n{yt_ch}\n\n源代码：{src}\n\n{zh['credits']}")
    yt_tags = en["tags"] + part["tags_en"] + (["中文", "数学分析"] if lang == "zh" else [])
    bili_tags = (zh["tags"] + part["tags_zh"])[:10]
    return {
        "youtube": {"title": yt_title, "description": yt_desc, "tags": yt_tags, "playlist": en["playlist_title"],
                    "category": "Education", "made_for_kids": False,
                    "language": "English" if lang == "en" else "Chinese (Simplified)",
                    "caption_language": "English" if lang == "en" else "Chinese (Simplified)",
                    "chapters": yt_ch},
        "bilibili": {"title": bili_title, "description": bili_desc, "tags": bili_tags, "collection": zh["playlist_title"],
                     "zone": "知识 → 科学科普", "type": "自制（原创）", "ai_disclosure": "声明：内容含AI合成语音（旁白）",
                     "subtitle_language": "英语" if lang == "en" else "中文（简体）", "chapters": bili_ch},
    }


def check_limits(t: dict) -> list[str]:
    out = []
    if len(t["youtube"]["title"]) > 100:
        out.append(f"YouTube title is {len(t['youtube']['title'])} characters (limit 100)")
    if len(t["youtube"]["description"].encode()) > 5000:
        out.append("YouTube description over 5000 bytes")
    if sum(len(x) + 1 for x in t["youtube"]["tags"]) > 500:
        out.append("YouTube tags over 500 characters")
    if len(t["bilibili"]["title"]) > 80:
        out.append(f"Bilibili title is {len(t['bilibili']['title'])} characters (limit 80)")
    if len(t["bilibili"]["description"]) > 2000:
        out.append(f"Bilibili description is {len(t['bilibili']['description'])} characters (limit 2000)")
    if len(t["bilibili"]["tags"]) > 10 or any(len(x) > 20 for x in t["bilibili"]["tags"]):
        out.append("Bilibili tags: at most 10, each at most 20 characters")
    return out


def write_txt(path: Path, platform: str, t: dict, files: dict) -> None:
    if platform == "youtube":
        y = t["youtube"]
        body = (f"Video file: {files['video']}\nThumbnail: {files['thumbnail']}\n"
                f"Subtitles: {files['srt']}  (language: {y['caption_language']})\n\n"
                f"TITLE\n{y['title']}\n\nDESCRIPTION\n{y['description']}\nTAGS\n{', '.join(y['tags'])}\n\n"
                f"Playlist: {y['playlist']}\nCategory: {y['category']}\nMade for kids: No\n"
                f"Video language: {y['language']}\n")
    else:
        b = t["bilibili"]
        body = (f"视频文件：{files['video']}\n封面：{files['thumbnail']}\n字幕：{files['srt']}（{b['subtitle_language']}）\n\n"
                f"标题\n{b['title']}\n\n简介\n{b['description']}\n\n标签\n{'，'.join(b['tags'])}\n\n"
                f"分区：{b['zone']}\n类型：{b['type']}\n合集：{b['collection']}\n{b['ai_disclosure']}\n\n"
                f"分段章节\n{b['chapters']}\n")
    path.write_text(body)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", default="analysis")
    ap.add_argument("--parts", type=int, nargs="*", help="part numbers (default: every part in the upload text)")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    configure(args.series)
    args.parts = args.parts or sorted(int(v.removeprefix(SERIES)) for v in DATA["parts"])
    rev = run(["git", "-C", str(ROOT), "rev-parse", "HEAD"]).strip()
    OUT.mkdir(parents=True, exist_ok=True)
    man_path = OUT / "manifest.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {"masters": {}}
    for n in args.parts:
        video = f"{SERIES}{n}"
        part = DATA["parts"][video]
        slug = re.sub(r"[^a-z0-9]+", "-", part["short_en"].lower().replace("ᵖ", "p")).strip("-")
        hero = None
        for lang in ("en", "zh"):
            base = ROOT / "renders" / f"{video}_2160p{'' if lang == 'en' else '_zh'}"
            mp4, srt = base.with_suffix(".mp4"), base.with_suffix(".srt")
            if not mp4.exists():
                print(f"  -   {video} {lang}: no master yet")
                continue
            ver = verify(video, lang, mp4, srt)
            t = texts(video, lang, ver, rev)
            problems = ver["problems"] + check_limits(t)
            mins = ver["duration_seconds"] / 60
            print(f"  {'FAIL' if problems else 'ok  '} {video} {lang}: {mins:.1f} min, {ver['bytes'] / 1e6:.0f} MB, "
                  f"{ver['loudness_LUFS']} LUFS, {ver['caption_cues']} cues, {len(ver['chapters'])} chapters"
                  + (f"  -- {'; '.join(problems)}" if problems else ""))
            if args.check_only or problems:
                continue
            folder = OUT / f"{n:02d}-{slug}" / lang
            folder.mkdir(parents=True, exist_ok=True)
            name = f"{KIT}-{n:02d}-{lang}"
            dst = folder / f"{name}.mp4"
            if dst.exists() and not os.path.samefile(dst, mp4):
                dst.unlink()
            if not dst.exists():
                try:
                    os.link(mp4, dst)
                except OSError:
                    import shutil

                    shutil.copy2(mp4, dst)
            srt_dst = folder / f"{name}.{'en' if lang == 'en' else 'zh-Hans'}.srt"
            srt_dst.write_text(srt.read_text())
            if hero is None:
                hero = hero_frame(video, part["thumb"]["t480"])
            thumbnail(video, lang, hero, part["thumb"]["crop"], folder / "thumbnail.jpg")
            files = {"video": dst.name, "srt": srt_dst.name, "thumbnail": "thumbnail.jpg"}
            write_txt(folder / "youtube.txt", "youtube", t, files)
            write_txt(folder / "bilibili.txt", "bilibili", t, files)
            meta = {**{k: v for k, v in ver.items() if k != "problems"}, **t, "files": files, "source_revision": rev}
            (folder / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
            manifest["masters"][f"{video}_{lang}"] = {k: v for k, v in ver.items() if k not in ("problems", "chapters")}
    if not args.check_only:
        manifest["source_revision"] = rev
        man_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
        write_checklist()


def write_checklist() -> None:
    en, zh = DATA["series"]["en"], DATA["series"]["zh"]
    rows = []
    for d in sorted(p for p in OUT.iterdir() if p.is_dir() and not p.name.startswith(".")):
        langs = [lang for lang in ("en", "zh") if (d / lang / "metadata.json").exists()]
        rows.append(f"| {d.name} | {', '.join(langs) or '-'} |")
    (OUT / "UPLOAD.md").write_text(f"""# {en['name']}: upload kit

| part | ready |
|---|---|
{chr(10).join(rows)}

Each `en` / `zh` folder: the video, its `.srt`, `thumbnail.jpg`, and `youtube.txt` / `bilibili.txt` to paste from.

- YouTube: Education, not made for kids; playlist "{en['playlist_title']}": {en['playlist_description']}
- Bilibili: 自制, 知识 / 科学科普; declare the AI-synthesized voice; 合集"{zh['playlist_title']}"：{zh['playlist_description']}
""")


if __name__ == "__main__":
    main()
