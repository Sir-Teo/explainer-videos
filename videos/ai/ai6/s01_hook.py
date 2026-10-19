from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, load, page_dots, page_plane


class Hook(VoiceoverScene):
    def construct(self):
        self.page()
        self.fingerprint()
        self.cloud()
        self.plan()

    # ------------------------------------------------------------------
    def page(self):
        p = load("pages")
        words = p["example"].split()
        lines, cur = [], []
        for w in words[:48]:
            cur.append(w)
            if len(" ".join(cur)) > 52:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        txt = VGroup(*[Text(l_, font="DejaVu Serif", font_size=26, color=GREY_A) for l_ in lines])
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(UP * 0.5)
        box = SurroundingRectangle(txt, color=GREY_D, buff=0.35, corner_radius=0.12)
        q = VGroup(label(r"Austen", font_size=40, color=AUSTEN), label(r"or", font_size=34, color=GREY_B),
                   label(r"Dickens?", font_size=40, color=DICKENS)).arrange(RIGHT, buff=0.3).next_to(box, DOWN, buff=0.5)
        with self.voiceover(
            "Here's a page from a novel, a thousand words long, with the punctuation stripped away. "
            "<bookmark mark='a'/> Who wrote it: Jane Austen, or Charles Dickens?"
        ) as vo:
            self.play(Create(box), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in txt], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fingerprint(self):
        p = load("pages")
        vocab, X, y = p["vocab"], np.asarray(p["X"]), np.asarray(p["y"])
        ex = int(p["example_i"])
        show = [vocab.index(w) for w in ("the", "and", "to", "of", "not", "her", "she", "be", "very", "said", "out", "up")]
        ma, md = X[y == 0].mean(0), X[y == 1].mean(0)
        top = max(X[ex, show].max(), ma[show].max(), md[show].max()) * 1.1
        W, H = 0.22, 3.4
        base = -1.7
        groups = VGroup()
        for k, j in enumerate(show):
            x0 = -5.6 + k * 0.98
            bars = VGroup(*[Rectangle(width=W, height=max(H * v / top, 0.01), stroke_width=0, fill_color=c,
                                      fill_opacity=o).move_to([x0 + i * (W + 0.02), base + H * v / top / 2, 0])
                            for i, (v, c, o) in enumerate(((ma[j], AUSTEN, 0.85), (X[ex, j], WHITE, 0.95),
                                                           (md[j], DICKENS, 0.85)))])
            lab = Text(vocab[j], font="DejaVu Sans Mono", font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.12)
            lab.set_y(base - 0.25)
            groups.add(VGroup(bars, lab))
        head = label(r"A page's fingerprint: \ how often it uses the commonest words", font_size=32).to_edge(UP, buff=0.4)
        legend = VGroup(label(r"Austen, on average", font_size=24, color=AUSTEN),
                        label(r"this page", font_size=24, color=WHITE),
                        label(r"Dickens, on average", font_size=24, color=DICKENS)).arrange(RIGHT, buff=0.6)
        legend.next_to(head, DOWN, buff=0.3)
        unit = label(r"uses per $1{,}000$ words", font_size=22, color=GREY_B).to_corner(DL, buff=0.35)
        cite_ = cite(r"F.~Mosteller \& D.~Wallace, \textit{Inference and Disputed Authorship: The Federalist} (1964)",
                     corner=DR)
        with self.voiceover(
            "You might look for names or places. But in 1964, Mosteller and Wallace settled who wrote the disputed "
            "Federalist papers by counting small words, like upon, whilst and also. <bookmark mark='a'/> So describe each "
            "page by how often it uses the seventy commonest words. <bookmark mark='b'/> This page says 'the' a lot "
            "and 'not' very little, like Dickens. Austen says 'not', 'very' and 'be' far more often."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in groups], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(g[1]) for g in groups], lag_ratio=0.08), FadeIn(legend), FadeIn(unit),
                      run_time=2.5)
            vo.wait_until("b")
            for k in (0, 4):
                self.play(Indicate(groups[k], color=WHITE, scale_factor=1.12), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        p = load("pages")
        X2, y = np.asarray(p["X2"]), np.asarray(p["y"])
        plane = page_plane(x_length=8.0, y_length=5.0, center=[-1.4, -0.3, 0])
        ax = plane[0]
        dots = page_dots(ax, X2, y, jitter=0.4)
        n = len(y)
        books = label(rf"${n}$ pages: \ \textit{{Pride and Prejudice}}, \textit{{Emma}} \ vs \ \textit{{A Tale of Two "
                      rf"Cities}}, \textit{{Great Expectations}}, \textit{{A Christmas Carol}}", font_size=22,
                      color=GREY_A).to_edge(UP, buff=0.3)
        key = VGroup(label(r"Austen", font_size=28, color=AUSTEN), label(r"Dickens", font_size=28, color=DICKENS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.6).shift(DOWN * 0.8)
        task = VGroup(*[label(t, font_size=30, color=C.BITS) for t in (r"Draw a line?", r"Bend it?",
                                                                         r"Ask the neighbours?")])
        task.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(key, DOWN, buff=0.6).align_to(key, LEFT)
        if task.get_right()[0] > 6.8:
            task.shift(LEFT * (task.get_right()[0] - 6.8))
        with self.voiceover(
            "Take just two of those numbers, how often a page says 'the' and how often it says 'not', and every "
            "page becomes a point. <bookmark mark='a'/> Six hundred and thirty-nine pages from five novels. The two "
            "authors mostly sit apart, but they overlap. <bookmark mark='b'/> Telling them apart is the oldest job in "
            "machine learning: classification. Draw a line? Bend it? Ask the neighbours? This part tries them all."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(books))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.004), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(task))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 6: \ Classical ML", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"lines, distances, margins, trees", font_size=32, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=6, done=5).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "These are the classics: least squares, logistic regression, nearest neighbours, support vector machines, "
            "trees and their forests. Regression is just the old name for fitting a formula to data. "
            "<bookmark mark='a'/> Act two of the series, learning, starts here, and every method is a few lines of "
            "numpy, Python's standard library for arrays of numbers."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
