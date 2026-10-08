from __future__ import annotations

import json

import numpy as np

from explainer import *  # noqa: F403
from explainer.data import crawl
from videos.frontier.common import Mono, Plot, label, load, mono_lines, page_card, source
from videos.frontier.compute import DATA_DIR

PAIR = ("forsale.godaddy.com/forsale/behindthetimes.com", "forsale.godaddy.com/forsale/dcnc.org")


def pair_docs():
    docs = [json.loads(ln) for ln in open(DATA_DIR / "corpus_filtered.jsonl")]
    a = next(d for d in docs if PAIR[0] in d["url"])
    b = next(d for d in docs if PAIR[1] in d["url"])
    return a, b


def hash_color(v: int) -> ManimColor:
    h = (int(v) % 997) / 997.0
    return ManimColor.from_hsv((h, 0.55, 0.9))


class Dedup(VoiceoverScene):
    def construct(self):
        self.d = load("dedup")
        self.a, self.b = pair_docs()
        self.cluster()
        self.jaccard()
        self.minhash()
        self.bands()
        self.results()

    # ------------------------------------------------------------------
    def cluster(self):
        big = self.d["big"][0]
        n = big[-1]
        assert n == 41 and "is for sale" in big[0]["text"]
        cards = VGroup(*[page_card(x["text"], x["url"], width=4.6, lines=4, chars=38, font_size=15, color=C.DUP)
                         for x in big[:-1][:5]])
        for k, c in enumerate(cards):
            c.move_to(LEFT * 3.2 + UP * 1.6 + (RIGHT * 0.55 + DOWN * 0.55) * k)
        head = label(r"The biggest near-duplicate cluster in our 8 files", font_size=34).to_edge(UP, buff=0.35)
        cnt = label(rf"{n} pages:\\``[domain] is for sale''", font_size=34, color=C.DUP).move_to(RIGHT * 3.8 + UP * 0.5)
        why = label(r"copies waste compute,\\and invite memorization", font_size=28, color=GREY_A).next_to(cnt, DOWN, buff=0.6)
        with self.voiceover(
            "The web is full of copies: mirrored sites, templates, boilerplate pages. Training on the same text over "
            "and over wastes compute and encourages memorization. <bookmark mark='c'/> Here's the biggest cluster of "
            "near-duplicates in our eight files: forty-one pages announcing that some domain name is for sale."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.2), FadeIn(cnt), run_time=2.0)
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jaccard(self):
        ta, tb = self.a["text"], self.b["text"]
        A, B = set(crawl.shingles(ta)), set(crawl.shingles(tb))
        J = len(A & B) / len(A | B)
        p = next(q for q in self.d["pairs"] if PAIR[0] in q["urls"][0] and PAIR[1] in q["urls"][1])
        assert abs(J - p["true"]) < 1e-9 and 0.75 < J < 0.8
        words = crawl.simplify(ta).split()[:16]
        line = VGroup(*[Mono(w, font_size=26) for w in words]).arrange(RIGHT, buff=0.18)
        line.to_edge(UP, buff=1.2)
        if line.width > 13:
            line.width = 13
        brackets = VGroup()
        for k in range(4):
            br = Brace(VGroup(*line[k:k + 5]), DOWN, color=C.DUP, buff=0.08 + 0.32 * k)
            brackets.add(br)
        sh = label(r"shingles: every run of 5 consecutive words", font_size=26, color=C.DUP).next_to(brackets, DOWN, buff=0.15)
        ca = Circle(radius=1.45, color=C.KEPT, fill_opacity=0.15).move_to(LEFT * 3.8 + DOWN * 1.6)
        cb = Circle(radius=1.45, color=BLUE_C, fill_opacity=0.15).move_to(LEFT * 1.9 + DOWN * 1.6)
        na = MathTex(str(len(A - B)), font_size=34).move_to(ca.get_center() + LEFT * 0.8)
        nb = MathTex(str(len(B - A)), font_size=34).move_to(cb.get_center() + RIGHT * 0.8)
        nab = MathTex(str(len(A & B)), font_size=40, color=C.DUP).move_to((ca.get_center() + cb.get_center()) / 2)
        la = label(r"page A", font_size=24, color=C.KEPT).next_to(ca, LEFT, buff=0.15)
        lb = label(r"page B", font_size=24, color=BLUE_C).next_to(cb, RIGHT, buff=0.15)
        jf = MathTex(r"J(A,B) = \frac{|A \cap B|}{|A \cup B|}", rf"= \frac{{{len(A & B)}}}{{{len(A | B)}}} = {J:.2f}",
                     font_size=38).move_to(RIGHT * 3.3 + DOWN * 1.6)
        with self.voiceover(
            "To measure how alike two pages are, cut each one into overlapping five-word shingles. "
            "<bookmark mark='j'/> The Jaccard similarity is the number of shingles they share, divided by the number "
            "of distinct shingles in either. For these two pages, it's 0.78."
        ) as vo:
            self.play(FadeIn(line))
            self.play(LaggedStart(*[GrowFromCenter(b) for b in brackets], lag_ratio=0.25), FadeIn(sh), run_time=1.5)
            vo.wait_until("j")
            self.play(FadeIn(ca), FadeIn(cb), FadeIn(la), FadeIn(lb))
            self.play(FadeIn(na), FadeIn(nb), FadeIn(nab), FadeIn(jf[0]))
            self.play(FadeIn(jf[1]))
        self.J = J
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minhash(self):
        seeds = crawl.hash_params()
        sa, sb = crawl.signature(self.a["text"], seeds), crawl.signature(self.b["text"], seeds)
        agree = int((sa == sb).sum())
        assert len(sa) == 112 and abs(agree / 112 - self.J) < 0.05
        self.sa, self.sb = sa, sb
        cell = 0.105

        def row(sig):
            return VGroup(*[Square(cell, stroke_width=0, fill_color=hash_color(v), fill_opacity=0.95) for v in sig]).arrange(RIGHT, buff=0.012)
        ra, rb = row(sa), row(sb)
        rows = VGroup(ra, rb).arrange(DOWN, buff=0.35).move_to(DOWN * 1.6)
        la = label(r"A", font_size=26, color=C.KEPT).next_to(ra, LEFT, buff=0.2)
        lb = label(r"B", font_size=26, color=BLUE_C).next_to(rb, LEFT, buff=0.2)
        marks = VGroup(*[Line(ra[k].get_bottom(), rb[k].get_top(), color=WHITE, stroke_width=1.5)
                         for k in range(112) if sa[k] == sb[k]])
        step1 = VGroup(
            label(r"1. hash every shingle with a random hash function", font_size=28),
            label(r"2. keep only the smallest value", font_size=28),
            MathTex(r"P\big(\min h(A) = \min h(B)\big) = J(A,B)", font_size=36, color=C.DUP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6)
        sig = label(r"3. repeat with 112 hash functions: a fingerprint of 112 numbers", font_size=28).next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        res = label(rf"{agree} of 112 agree: estimate {agree / 112:.2f}\quad (true: {self.J:.2f})", font_size=30, color=C.DUP)
        res.next_to(rows, DOWN, buff=0.35)
        with self.voiceover(
            "But comparing every page with every other is hopeless. Billions of pages means billions of billions of "
            "pairs. MinHash gets around this with a beautiful trick. <bookmark mark='h'/> Run every shingle of a page "
            "through a random hash function, and keep only the smallest value. <bookmark mark='p'/> Two pages get the "
            "same minimum exactly when the smallest-hashed shingle of the two pages combined is one they share, which "
            "happens with probability equal to their Jaccard similarity. <bookmark mark='r'/> Repeat with 112 "
            "different hash functions, and each page gets a short fingerprint. <bookmark mark='a'/> For our two "
            "pages, 86 of the 112 minimums agree: an estimate of 0.77."
        ) as vo:
            vo.wait_until("h")
            self.play(FadeIn(step1[0]), FadeIn(step1[1]))
            vo.wait_until("p")
            self.play(FadeIn(step1[2]))
            vo.wait_until("r")
            self.play(FadeIn(sig), FadeIn(la), FadeIn(lb), LaggedStart(FadeIn(ra, lag_ratio=0.01), FadeIn(rb, lag_ratio=0.01)),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(Create(marks, lag_ratio=0.02), FadeIn(res), run_time=1.5)
        assert agree == 86
        self.rows = (ra, rb, la, lb)
        self.wait(0.3)
        self.clear_scene(*self.rows)

    # ------------------------------------------------------------------
    def bands(self):
        ra, rb, la, lb = self.rows
        sa, sb = self.sa, self.sb
        B, R = crawl.BANDS, crawl.ROWS
        assert (B, R, crawl.N_GRAMS) == (14, 8, 5)
        g = VGroup(ra, rb, la, lb)
        self.play(g.animate.move_to(UP * 2.6), run_time=0.8)
        boxes = VGroup()
        full = []
        for k in range(B):
            sl = slice(k * R, (k + 1) * R)
            match = bool(np.all(sa[sl] == sb[sl]))
            full.append(match)
            bx = SurroundingRectangle(VGroup(*ra[sl], *rb[sl]), buff=0.04, stroke_width=2 if match else 1,
                                      color=C.DUP if match else GREY_D)
            boxes.add(bx)
        assert any(full)
        bl = label(rf"14 bands of 8: a band that matches completely $\Rightarrow$ same bucket $\Rightarrow$ candidate pair",
                   font_size=24, color=C.DUP).next_to(g, DOWN, buff=0.2)
        plot = Plot(x_range=(0, 1), y_range=(0, 1), width=6.4, height=2.9, x_ticks=[0, 0.25, 0.5, 0.75, 1],
                    y_ticks=[0, 0.5, 1], x_label=r"Jaccard similarity $s$", y_label=r"chance of being caught")
        plot.move_to(LEFT * 2.0 + DOWN * 1.35)
        s = np.linspace(0, 1, 200)
        curve = plot.line(s, crawl.p_candidate(s), color=C.DUP, stroke_width=4)
        form = MathTex(r"P(s) = 1 - (1 - s^{8})^{14}", font_size=36, color=C.DUP).move_to(RIGHT * 4.0 + DOWN * 0.6)
        p8, p5 = float(crawl.p_candidate(0.8)), float(crawl.p_candidate(0.5))
        assert 0.91 < p8 < 0.93 and p5 < 0.06
        facts = VGroup(label(rf"$s = 0.8$: caught {100 * p8:.0f}\% of the time", font_size=26),
                       label(rf"$s = 0.5$: {100 * p5:.0f}\%", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        facts.next_to(form, DOWN, buff=0.4)
        src = source(r"FineWeb's MinHash settings: 5-grams, 14 buckets $\times$ 8 hashes (\texttt{datatrove})")
        with self.voiceover(
            "Then, instead of comparing fingerprints, hash them. <bookmark mark='b'/> Cut the 112 numbers into 14 "
            "bands of eight. Pages that match on all eight numbers of any band land in the same bucket, and become "
            "candidates. <bookmark mark='c'/> The chance of that, as a function of similarity, is this S-curve: pages "
            "that are eighty percent alike are caught ninety-two percent of the time; pages that are half alike, "
            "about five percent."
        ) as vo:
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.05), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(plot), FadeIn(src), FadeIn(form))
            self.play(Create(curve), run_time=1.5)
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = self.d
        removed = 1 - d["n_out"] / d["n_in"]
        assert 0.02 < removed < 0.04 and d["n_clusters_multi"] == 114
        kinds = VGroup(
            label(r"``[domain] is for sale'': 41 pages", font_size=28),
            label(r"``Access denied \dots bot activity'': 24 pages", font_size=28),
            label(r"``Why am I seeing this page?'' (default hosting): 7 pages", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        top = label(rf"Our 8 files: {d['n_in']:,} pages $\rightarrow$ {d['n_out']:,} ({100 * removed:.0f}\% removed, {d['n_clusters_multi']} clusters)".replace(",", "{,}"),
                    font_size=32).to_edge(UP, buff=0.6)
        kinds.next_to(top, DOWN, buff=0.4)
        fw = VGroup(
            label(r"\textbf{FineWeb's surprise:} deduplicating across all 96 crawls", font_size=28),
            label(r"removed 90\% of the oldest crawls, and what was left trained \emph{worse} models.", font_size=28),
            label(r"So FineWeb deduplicates each crawl on its own.", font_size=28, color=C.KEPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.8)
        src = source(r"Penedo et al., \emph{The FineWeb Datasets} (2024)")
        with self.voiceover(
            "In our eight files, deduplication removed about three percent of the pages that survived filtering, in "
            "114 clusters: domain-for-sale pages, access-denied pages, default web-hosting pages. "
            "<bookmark mark='f'/> Across a hundred crawls, the same pages turn up again and again, so the stakes are "
            "much higher, and FineWeb found a surprise. Deduplicating across all the crawls threw away ninety percent "
            "of the oldest ones, and what remained trained worse models. So FineWeb deduplicates each crawl "
            "separately."
        ) as vo:
            self.play(FadeIn(top))
            self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.2) for k in kinds], lag_ratio=0.2))
            vo.wait_until("f")
            self.play(FadeIn(fw), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()
