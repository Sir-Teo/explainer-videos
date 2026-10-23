from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.web import BLOCK
from videos.ai.ai18.common import (EDU, F, KEPT, MONO, PAGE, PART, REMOVED, load, node_box, said, spoken_int,
                                   take_away)

LANG = {"en": r"English", "ru": r"Russian", "es": r"Spanish", "de": r"German", "ja": r"Japanese", "fr": r"French",
        "pt": r"Portuguese", "pl": r"Polish", "it": r"Italian", "zh": r"Chinese", "nl": r"Dutch", "id": r"Indonesian"}


class Web(VoiceoverScene):
    def construct(self):
        self.card()
        self.crawl()
        self.extract()
        self.language()

    def card(self):
        card = chapter_card(2, r"From the web to text", r"What is in a crawl of the web, and what survives?",
                            lit=(2008,), part=PART)
        with self.voiceover("Chapter two. From the web to text."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def crawl(self):
        W = load("web")
        hc = history_card(2007, r"Gil Elbaz founds Common Crawl", r"a non-profit that crawls the web and gives the "
                          r"archive away: \ crawls since 2008, \ more than ten petabytes", width=6.2,
                          color=PAGE).to_corner(UL, buff=0.4)
        # 100,000 files in a crawl: a block of tiles, three of them lit
        tiles = VGroup(*[Square(0.11, stroke_width=0, fill_color=PAGE, fill_opacity=0.35) for _ in range(40 * 25)])
        tiles.arrange_in_grid(rows=25, cols=40, buff=0.025).move_to([3.4, 1.0, 0])
        tcap = label(r"one crawl: \ $100{,}000$ files \ (each tile: $100$)", font_size=20, color=GREY_A)
        tcap.next_to(tiles, UP, buff=0.15)
        lit = [tiles[0], tiles[333], tiles[666]]
        kinds = VGroup(node_box(r"WARC: \ the raw responses, \ HTML", PAGE, font_size=22),
                       node_box(r"WET: \ Common Crawl's own text extraction", PAGE, font_size=22))
        kinds.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(hc, DOWN, buff=0.5).align_to(hc, LEFT)
        ours = VGroup(
            label(rf"our sample: \ $3$ WET files of September 2026's crawl, \ $3$ slices of "
                  rf"${W['chunk_bytes'] / 2 ** 20:.0f}$ MiB each", font_size=24, color=WHITE),
            label(rf"${W['n_pages']:,}$ pages, \ ${W['text_bytes'] / 1e6:.1f}$ MB of text, \ "
                  rf"${W['n_langs']}$ languages".replace(",", "{,}"), font_size=28, color=PAGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.9).align_to(hc, LEFT)
        src = cite(r"commoncrawl.org; \ crawl CC-MAIN-2026-39 \ (computed here)", corner=DR, font_size=17)
        with self.voiceover(
            "Almost every open pretraining corpus starts in the same place: Common Crawl, a non-profit founded by Gil "
            "Elbaz in 2007, which has crawled the web since 2008 and gives the archive away, more than ten petabytes. "
            "<bookmark mark='a'/> Each crawl is cut into a hundred thousand files, in two forms that matter here: WARC "
            "files hold the raw responses, HTML and all; WET files hold the text Common Crawl extracted itself. "
            "<bookmark mark='b'/> For this part we took three WET files of the September 2026 crawl, three slices of "
            f"each: {spoken_int(W['n_pages'])} pages, {W['text_bytes'] / 1e6:.0f} megabytes of text, in {W['n_langs']} "
            "languages. Everything in the next four chapters happens to these pages."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tiles, lag_ratio=0.002, run_time=1.5), FadeIn(tcap))
            vo.wait_until("a")
            self.play(FadeIn(kinds[0], shift=UP * 0.1))
            self.play(FadeIn(kinds[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(*[t.animate.set_fill(YELLOW, opacity=1).scale(1.6) for t in lit], FadeIn(src))
            self.play(FadeIn(ours, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extract(self):
        W = load("web")
        ex = W["example"]
        html = code_block([
            "<!DOCTYPE html><html><head>",
            '<script src="analytics.js"></script>',
            '<link rel="stylesheet" ...>',
            "</head><body>",
            '<nav class="menu"> ... </nav>',
            '<div class="page-content"> ... </div>',
            '<footer> ... </footer>',
            "</body></html>",
        ], font_size=17, color=GREY_B)
        hbox = VGroup(SurroundingRectangle(html, buff=0.2, corner_radius=0.1, color=PAGE, stroke_width=1.5), html)
        hl = label(rf"the page's HTML: \ ${ex['html_bytes']:,}$ bytes".replace(",", "{,}"), font_size=22, color=PAGE)
        left = VGroup(hl, hbox).arrange(DOWN, buff=0.15).move_to([-3.6, 1.3, 0])
        tbox = said(ex["text"], chars=40, font_size=16, max_lines=7, box_color=KEPT)
        tl = label(rf"Trafilatura's text: \ ${ex['text_bytes']:,}$ bytes".replace(",", "{,}"), font_size=22, color=KEPT)
        right = VGroup(tl, tbox).arrange(DOWN, buff=0.15).move_to([3.3, 1.3, 0])
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        url = data_text(ex["url"].replace("http://", "").replace("https://", ""), font=MONO, font_size=15, color=GREY_B)
        url.next_to(right, DOWN, buff=0.15)
        sch = note(r"HTML abridged \ (schematic)", font_size=18).next_to(left, DOWN, buff=0.15)
        stats = VGroup(
            label(rf"${W['warc_pages']}$ HTML pages from WARC slices: \ ${W['html_bytes'] / 1e6:.1f}$ MB of HTML $\to$ "
                  rf"${W['extracted_bytes'] / 1e6:.2f}$ MB of text \ (${100 * W['extracted_share']:.1f}\%$)",
                  font_size=24, color=WHITE),
            label(rf"the median page keeps ${100 * W['median_ratio']:.1f}\%$ of its bytes; \ ${W['empty']}$ keep nothing",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.9)
        fw = note(r"FineWeb (2024): \ Trafilatura on WARC trained better models than the WET text", font_size=20)
        fw.next_to(stats, DOWN, buff=0.3)
        with self.voiceover(
            "The first step is extraction: turning HTML into text. A web page is mostly not prose. Scripts, styles, "
            "menus, footers, buttons. <bookmark mark='a'/> Here is one page from our WARC slices. Its HTML is "
            f"{spoken_int(ex['html_bytes'])} bytes. <bookmark mark='b'/> Trafilatura, the extractor FineWeb uses, "
            f"keeps {spoken_int(ex['text_bytes'])} bytes of it: the article, without the menu around it. "
            f"<bookmark mark='c'/> Across all {W['warc_pages']} HTML pages in our slices, {W['html_bytes'] / 1e6:.0f} "
            f"megabytes of HTML became {W['extracted_bytes'] / 1e6:.1f} megabytes of text: about "
            f"{100 * W['extracted_share']:.0f} percent. <bookmark mark='d'/> This step matters more than it sounds. "
            "FineWeb's authors trained small models on the same crawl extracted two ways, and the Trafilatura text "
            "beat Common Crawl's own WET text."
        ) as vo:
            self.play(FadeIn(left), FadeIn(sch))
            vo.wait_until("a")
            self.play(Indicate(hl))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(right), FadeIn(url))
            vo.wait_until("c")
            self.play(FadeIn(stats, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(fw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def language(self):
        W = load("web")
        langs = W["langs"][:10]
        kept = W["n_pages"] - W["blocked"]
        mx = langs[0][1]
        bars = VGroup()
        for i, (code, n) in enumerate(langs):
            col = KEPT if code == "en" else GREY_B
            h = 3.4 * n / mx
            b = Rectangle(width=0.62, height=max(h, 0.03), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-5.6 + 0.88 * i, -1.6, 0], aligned_edge=DOWN)
            nm = label(LANG.get(code, code), font_size=18, color=col).rotate(PI / 4)
            nm.next_to(b, DOWN, buff=0.1).shift(LEFT * 0.15)
            v = label(f"${n:,}$".replace(",", "{,}"), font_size=18, color=col).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, nm, v))
        bl = label(r"pages by language, \ fastText's identifier", font_size=22, color=GREY_A)
        bl.next_to(bars, UP, buff=0.25).align_to(bars, LEFT)
        en = dict(langs)["en"]
        funnel = VGroup(
            label(rf"${W['n_pages']:,}$ pages".replace(",", "{,}"), font_size=26, color=PAGE),
            label(rf"$-\,{W['blocked']}$ \ by a URL blocklist", font_size=22, color=REMOVED),
            label(rf"${en:,}$ in English".replace(",", "{,}"), font_size=26, color=KEPT),
            label(rf"$-\,{W['english_below']}$ \ less sure than $0.65$", font_size=22, color=REMOVED),
            label(rf"$-\,{en - W['english_below'] - W['english']}$ \ shorter than $50$ words", font_size=22,
                  color=REMOVED),
            label(rf"${W['english']:,}$ pages go on".replace(",", "{,}"), font_size=28, color=KEPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 0.0, 0])
        src = cite(r"Joulin et al.\ (2016--17), \ lid.176; \ Penedo et al., FineWeb (2024); \ computed here", corner=DL,
                   font_size=17)
        share = en / kept
        # Before the chart: the two filters, drawn where the bars will grow.
        n_words = len(BLOCK)
        blk = VGroup(
            label(r"1. \ the address alone", font_size=22, color=REMOVED),
            data_text("…/casino-bonus-2026/", font=MONO, font_size=17, color=GREY_B),
            label(rf"contains one of ${n_words}$ listed words \ $\Rightarrow$ \ dropped, unread", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        sample = "where the river bends"
        pieces = [w for w in ("<wh", "whe", "her", "ere", "re>", "<th", "the", "he>", "<ri", "riv", "…")]
        chips = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.36, corner_radius=0.06, stroke_color=GREY_C,
                                                 stroke_width=1, fill_color="#1a2030", fill_opacity=1),
                                data_text(c, font=MONO, font_size=14, color=GREY_A)) for c in pieces])
        chips.arrange(RIGHT, buff=0.06)
        probs = [("English", 0.97), ("Dutch", 0.01), ("German", 0.01)]
        pbars = VGroup()
        for nm, pr in probs:
            r = Rectangle(width=max(2.6 * pr, 0.04), height=0.24, stroke_width=0, fill_color=KEPT if pr > 0.5 else GREY_B,
                          fill_opacity=0.85)
            t = label(nm, font_size=17, color=GREY_A)
            pbars.add(VGroup(t, r).arrange(RIGHT, buff=0.12))
        pbars.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        ftx = VGroup(
            label(r"2. \ fastText's language identifier", font_size=22, color=KEPT),
            data_text(sample, font=MONO, font_size=17, color=GREY_B),
            chips,
            label(r"one vector per character piece, \ averaged, \ one linear layer \ $\to$ \ $176$ "
                  r"probabilities", font_size=19, color=GREY_A),
            pbars,
            note(r"both examples schematic", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        pre = VGroup(blk, ftx).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        pre.scale_to_fit_height(min(pre.height, 4.1)).move_to([-2.4, -0.45, 0])
        with self.voiceover(
            "Next: which language is each page in? <bookmark mark='a'/> Before that, a cheap filter on the address "
            f"alone: a blocklist of adult and gambling sites removes {W['blocked']} pages. <bookmark mark='b'/> Then "
            "a language identifier: fastText's, from Facebook AI Research, a linear model on character pieces that "
            "picks among 176 languages, fast enough to run on billions of pages. <bookmark mark='c'/> Here is what our "
            f"sample holds. English: {spoken_int(en)} pages, about {round(100 * share)} percent; the rest are spread "
            f"over {W['n_langs'] - 1} other languages. <bookmark mark='d'/> "
            "FineWeb keeps a page as English only if the identifier is at least 65 percent sure. That drops "
            f"{W['english_below']} more; and we drop pages under fifty words. <bookmark mark='e'/> "
            f"{spoken_int(W['english'])} English pages go on to the next step. Multilingual models, like Qwen3 with its "
            "119 languages, run such a pipeline for each language."
        ) as vo:
            self.play(FadeIn(bl), FadeIn(funnel[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(blk, shift=UP * 0.1))
            self.play(FadeIn(funnel[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(ftx[:2]))
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.12), run_time=1.5)
            self.play(FadeIn(ftx[3]))
            self.play(LaggedStart(*[GrowFromEdge(b[1], LEFT) for b in pbars], lag_ratio=0.2), FadeIn(pbars),
                      FadeIn(ftx[5]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeOut(pre))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2])) for b in bars],
                                  lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(funnel[2], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(funnel[3], shift=RIGHT * 0.1), FadeIn(funnel[4], shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(funnel[5], shift=RIGHT * 0.1), Indicate(bars[0][0], color=YELLOW))
        self.wait(0.3)
        self.clear_scene()
