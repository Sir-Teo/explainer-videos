from __future__ import annotations

import html as htmllib
import json

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import (
    CRAWL, Mono, bar_rows, clean_line, label, load, note, page_card, part_card, pipeline_map, source,
)
from videos.frontier.compute import DATA_DIR

SHOWCASE = "http://www.hungrycravings.com/2010/04/savory-custard.html"


def showcase_page() -> tuple[str, str, int]:
    """(raw HTML, extracted text, html bytes) of the showcase page, from the funnel's cache."""
    html = next(json.loads(ln)["html"] for ln in open(DATA_DIR / "funnel_kept_html.jsonl") if SHOWCASE in ln)
    kept = next(json.loads(ln) for ln in open(DATA_DIR / "funnel_kept.jsonl") if SHOWCASE in ln)
    return html, kept["text"], kept["html_bytes"]


def minimap(lines: list[str], content: set[int], cols: int = 6, col_w: int = 90, rows_px: int = 2) -> np.ndarray:
    """An RGBA picture of a source file: one thin bar per line (length = line length), grey for markup,
    teal for the lines that carry the page's text."""
    n = len(lines)
    per = int(np.ceil(n / cols))
    H, W = per * rows_px, cols * (col_w + 10)
    img = np.zeros((H, W, 4), np.uint8)
    grey, teal = (110, 116, 128), tuple(int(c * 255) for c in ManimColor(C.KEPT).to_rgb())
    for i, ln in enumerate(lines):
        c, r = divmod(i, per)
        x0 = c * (col_w + 10) + min(col_w - 1, len(ln) - len(ln.lstrip()) // 2)
        length = min(col_w - (x0 - c * (col_w + 10)), max(1, len(ln.strip()) // 3))
        if not ln.strip():
            continue
        col = teal if i in content else grey
        img[r * rows_px:r * rows_px + rows_px - 1, x0:x0 + length, :3] = col
        img[r * rows_px:r * rows_px + rows_px - 1, x0:x0 + length, 3] = 255
    return img


class RawWeb(VoiceoverScene):
    def construct(self):
        self.opening()
        self.crawl()
        self.one_page()
        self.extraction()

    # ------------------------------------------------------------------
    def opening(self):
        card = part_card(1, r"The data", r"from raw web pages to clean tokens")
        m = pipeline_map(width=13.0, highlight="web").to_edge(DOWN, buff=0.7)
        card.to_edge(UP, buff=1.0)
        with self.voiceover("Part one: the data.") as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(m), run_time=1.2)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crawl(self):
        cols, rows = 400, 250
        assert cols * rows == CRAWL["files"]
        img = np.full((rows, cols, 4), 0, np.uint8)
        img[..., :3] = (70, 76, 88)
        img[..., 3] = 255
        img[:, ::2, :3] = (82, 88, 100)
        grid = ImageMobject(img)
        grid.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        grid.stretch_to_fit_width(8.0).stretch_to_fit_height(5.0).move_to(LEFT * 2.3 + DOWN * 0.4)
        frame = SurroundingRectangle(grid, buff=0.03, color=GREY_B, stroke_width=1.5)
        title = label(r"Common Crawl, " + CRAWL["name"] + r" (" + CRAWL["id"] + r")", font_size=36).to_edge(UP, buff=0.45)
        facts = VGroup(
            label(r"2.17 billion pages", font_size=36, color=C.PAGE),
            label(r"106 TiB compressed", font_size=32, color=GREY_A),
            label(r"100{,}000 files", font_size=32, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(frame, RIGHT, buff=0.6).shift(UP * 1.0)
        one = label(r"each square: one file\\(about 21{,}500 pages)", font_size=24, color=GREY_B).next_to(facts, DOWN, buff=0.5).align_to(facts, LEFT)
        # the files this video downloaded: WET files 0, 12500, ... and (the head of) WARC file 0
        picked = [i * 12_500 for i in range(8)]
        rings = VGroup()
        for idx in picked:
            r, c = divmod(idx, cols)
            pos = grid.get_corner(UL) + RIGHT * (c + 0.5) * 8.0 / cols + DOWN * (r + 0.5) * 5.0 / rows
            rings.add(Circle(radius=0.09, color=C.KEPT, stroke_width=3).move_to(pos))
        ours = label(r"downloaded for this video: 8 files, plus 400 MB of the raw HTML of one", font_size=26,
                     color=C.KEPT).next_to(frame, DOWN, buff=0.25).align_to(frame, LEFT)
        src = source(r"commoncrawl.org, crawl statistics for CC-MAIN-2026-39")

        with self.voiceover(
            "Almost every large language model starts from the same place: Common Crawl, a non-profit that crawls "
            "the web every month or two and gives the result away. <bookmark mark='p'/> Its September 2026 crawl "
            "alone holds 2.17 billion web pages, a hundred and six terabytes compressed, <bookmark mark='f'/> split "
            "into a hundred thousand files. Each square here is one of them. <bookmark mark='o'/> For this video, "
            "we downloaded nine."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("p")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]), FadeIn(src))
            vo.wait_until("f")
            self.play(FadeIn(grid), Create(frame), FadeIn(facts[2]), FadeIn(one), run_time=1.2)
            vo.wait_until("o")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), FadeIn(ours), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def one_page(self):
        raw, text, nbytes = showcase_page()
        lines = raw.splitlines()
        assert 2000 < len(lines) < 2600 and 90_000 < nbytes < 105_000
        paras = [p.strip() for p in text.split("\n") if len(p.strip()) > 25]
        keys = [htmllib.escape(p[:24], quote=False) for p in paras] + [p[:24] for p in paras]
        content = {i for i, ln in enumerate(lines)
                   if any(k in ln for k in keys) and not any(t in ln for t in ("<meta", "og:", "_WidgetManager"))}
        assert content == {435}, content  # the whole post is one long line: line 436 of 2,296
        frac = len(text.encode()) / nbytes
        assert 0.03 < frac < 0.04

        card = page_card(text, SHOWCASE, width=6.4, lines=5, chars=58, font_size=17).to_edge(UP, buff=0.4)
        cap = label(r"one page from the first file: a recipe blog post", font_size=28).next_to(card, DOWN, buff=0.25)
        with self.voiceover(
            "Here's one page from the very first file: a blog post with a recipe for savory custard."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(cap))
        self.play(FadeOut(card), FadeOut(cap))

        head = VGroup(*[Mono(clean_line(ln)[:70], font_size=15, color=GREY_B) for ln in lines[:22] if clean_line(ln)])
        head.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        head.to_corner(UL, buff=0.4)
        mm = ImageMobject(minimap(lines, content))
        mm.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        mm.stretch_to_fit_height(6.6).stretch_to_fit_width(6.2).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.1)
        mmf = SurroundingRectangle(mm, buff=0.05, color=GREY_B, stroke_width=1.5)
        mml = label(rf"all {len(lines):,} lines of its HTML".replace(",", "{,}"), font_size=26, color=GREY_A)
        mml.next_to(mmf, UP, buff=0.1)
        hl = label(r"the recipe: all of it on line 436", font_size=28, color=C.KEPT)
        # content lines sit in the last column of the minimap
        cols = 6
        per = int(np.ceil(len(lines) / cols))
        c, r = divmod(min(content), per)
        y = mm.get_top()[1] - (r / per) * mm.height
        x = mm.get_left()[0] + (c + 0.5) / cols * mm.width
        arrow = Arrow(mmf.get_left() + LEFT * 0.9 + UP * 0.0, [x - 0.55, y - 0.1, 0], buff=0.05, color=C.KEPT, stroke_width=4)
        arrow.put_start_and_end_on([x - 1.9, y - 1.2, 0], [x - 0.55, y - 0.2, 0])
        hl.next_to(arrow.get_start(), DOWN, buff=0.1)
        stat = VGroup(
            label(rf"{nbytes / 1000:.1f} KB of HTML", font_size=30, color=C.PAGE),
            MathTex(r"\downarrow", font_size=36, color=GREY_B),
            label(rf"{len(text.encode()) / 1000:.1f} KB of text: {100 * frac:.1f}\%", font_size=30, color=C.KEPT),
        ).arrange(DOWN, buff=0.15).to_corner(DL, buff=0.6)

        with self.voiceover(
            "This is what the crawler actually stored: more than two thousand lines of HTML. Scripts, style sheets, "
            "menus, links, metadata. <bookmark mark='r'/> And the recipe itself? All of it sits on a single line: "
            "number 436. <bookmark mark='s'/> Ninety-eight kilobytes of HTML, for three kilobytes of text: about "
            "three percent."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h) for h in head], lag_ratio=0.05), run_time=1.5)
            self.play(FadeIn(mm), Create(mmf), FadeIn(mml), run_time=1.2)
            vo.wait_until("r")
            self.play(GrowArrow(arrow), FadeIn(hl))
            vo.wait_until("s")
            self.play(FadeOut(head), FadeIn(stat))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extraction(self):
        f = load("funnel")
        st = f["stats"]
        html_gb = st["url"]["bytes"] / 1e9
        text_mb = st["extract"]["bytes"] / 1e6
        n = st["input"]["docs"]
        assert 10_000 < n < 11_000 and 1.5 < html_gb < 1.8 and 30 < text_mb < 45
        langs = f["languages"]
        total = sum(langs.values())
        top = list(langs.items())[:10]
        en_share = langs["en"] / total
        assert 0.35 < en_share < 0.45

        a = label(rf"{n:,} pages from one raw file: ".replace(",", "{,}") + rf"{html_gb:.2f} GB of HTML $\rightarrow$ "
                  rf"{text_mb:.0f} MB of text", font_size=32).to_edge(UP, buff=0.5)
        b = label(r"text extraction: Trafilatura, as in FineWeb (Common Crawl's own WET text keeps more boilerplate)",
                  font_size=24, color=GREY_A).next_to(a, DOWN, buff=0.2)
        names = {"en": "English", "ru": "Russian", "ja": "Japanese", "es": "Spanish", "zh": "Chinese",
                 "de": "German", "fr": "French", "pt": "Portuguese", "pl": "Polish", "id": "Indonesian",
                 "nl": "Dutch", "it": "Italian"}
        bars = bar_rows([(names.get(code, code), cnt, C.KEPT if code == "en" else C.PAGE, rf"{100 * cnt / total:.0f}\%")
                         for code, cnt in top], 6.0 / top[0][1], font_size=26, bar_h=0.32, buff=0.12)
        bars.next_to(b, DOWN, buff=0.45)
        cap = label(r"language of each page (fastText language ID)", font_size=24, color=GREY_B).next_to(bars, DOWN, buff=0.25)

        with self.voiceover(
            "Across the first ten thousand pages of that file, it's the same story: 1.65 gigabytes of HTML become "
            "thirty-seven megabytes of text. <bookmark mark='t'/> Pulling out the main text is a step of its own. "
            "Common Crawl ships an extracted version, but the FineWeb team found that re-extracting from the raw "
            "HTML, with a library called Trafilatura, leaves out more menus and boilerplate, and trains better "
            "models. <bookmark mark='l'/> And the web is multilingual: in this sample, only four pages in ten are in "
            "English. Frontier models train on many languages; here, like the original FineWeb, we'll keep English."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("t")
            self.play(FadeIn(b))
            vo.wait_until("l")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bars], lag_ratio=0.08), FadeIn(cap),
                      run_time=1.5)
        self.wait(0.5)
        self.clear_scene()
