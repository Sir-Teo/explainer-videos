from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, PART, era_strip, load, page_dots, page_plane


class Hook(VoiceoverScene):
    def construct(self):
        self.page()
        self.fingerprint()
        self.cloud()
        self.era()
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
        txt = VGroup(*[data_text(l_, font="DejaVu Serif", font_size=26, color=GREY_A) for l_ in lines])
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
            lab = data_text(vocab[j], font="DejaVu Sans Mono", font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.12)
            lab.set_y(base - 0.25)
            groups.add(VGroup(bars, lab))
        head = label(r"A page's fingerprint: \ how often it uses the commonest words", font_size=32).to_edge(UP, buff=0.4)
        legend_ = VGroup(label(r"Austen, on average", font_size=24, color=AUSTEN),
                         label(r"this page", font_size=24, color=WHITE),
                         label(r"Dickens, on average", font_size=24, color=DICKENS)).arrange(RIGHT, buff=0.6)
        legend_.next_to(head, DOWN, buff=0.3)
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
                      LaggedStart(*[FadeIn(g[1]) for g in groups], lag_ratio=0.08), FadeIn(legend_), FadeIn(unit),
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
        n = int(p["n_pages"])
        books = label(rf"${n}$ pages: \ \textit{{Pride and Prejudice}}, \textit{{Emma}} \ vs \ \textit{{A Tale of Two "
                      rf"Cities}}, \textit{{Great Expectations}}, \textit{{A Christmas Carol}}", font_size=22,
                      color=GREY_A).to_edge(UP, buff=0.3)
        key = VGroup(label(r"Austen", font_size=28, color=AUSTEN), label(r"Dickens", font_size=28, color=DICKENS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.6).shift(DOWN * 0.8)
        task = VGroup(*[label(t, font_size=30, color=C.BITS) for t in (r"Draw a line?", r"Bend it?",
                                                                         r"Ask the neighbours?", r"Ask questions?")])
        task.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(key, DOWN, buff=0.6).align_to(key, LEFT)
        if task.get_right()[0] > 6.8:
            task.shift(LEFT * (task.get_right()[0] - 6.8))
        test = np.asarray(p["test"], bool)
        with self.voiceover(
            "Take just two of those numbers, how often a page says 'the' and how often it says 'not', and every "
            f"page becomes a point. <bookmark mark='a'/> {n} pages from five novels. The two authors mostly sit "
            f"apart, but they overlap. We'll train on {int((~test).sum())} of them, and keep {int(test.sum())} "
            "locked away to test on. <bookmark mark='b'/> Telling the authors apart is the oldest job in machine "
            "learning: classification. Draw a line? Bend it? Ask the neighbours? Ask questions? This part tries them all."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(books))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.004), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in task], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from Legendre's least squares to foundation models for tables, evenly spaced."""
        events = [
            (1805, r"Legendre: \\ least squares"),
            (1936, r"Fisher: \\ discriminants"),
            (1958, r"Rosenblatt: \\ the perceptron"),
            (1967, r"Cover, Hart: \\ neighbours"),
            (1984, r"Breiman et al.: \\ CART trees"),
            (1995, r"Cortes, Vapnik: \\ the SVM"),
            (1997, r"Freund, Schapire: \\ AdaBoost"),
            (2001, r"random forests; \\ Viola--Jones faces"),
            (2006, r"the Netflix \\ Prize"),
            (2010, r"Kaggle"),
            (2016, r"XGBoost"),
            (2025, r"TabPFN: \\ a model for tables"),
        ]
        axis, skel, marks = era_strip(events, font_size=18)
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The methods are older than the computers that run them. In 1805 Legendre fitted orbits by least "
            "squares. <bookmark mark='a'/> In 1936 Ronald Fisher found the direction that best separates "
            "species of iris. <bookmark mark='b'/> In 1958 Frank Rosenblatt's perceptron learned a line from examples, "
            "<bookmark mark='c'/> and in 1967 Cover and Hart proved how well simply copying your nearest neighbour "
            "can do. <bookmark mark='d'/> Then trees that ask questions, <bookmark mark='e'/> Vapnik's support "
            "vector machines, <bookmark mark='f'/> boosting, <bookmark mark='g'/> random forests, and Viola and "
            "Jones finding faces in real time. <bookmark mark='h'/> Then the competitions: Netflix's million-dollar "
            "prize, <bookmark mark='i'/> Kaggle, <bookmark mark='j'/> and XGBoost, which won many of them. "
            "<bookmark mark='k'/> And now, transformers trained to read whole tables at once."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghijk"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Classical ML", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"least squares as a projection; \ why it is best (Gauss--Markov); \ ridge and the lasso",
            r"logistic regression and Newton's method; \ naive Bayes; \ honest probabilities",
            r"Fisher's discriminant; \ nearest neighbours and the curse of dimensionality",
            r"kernels and support vector machines, \ with the dual derived",
            r"trees, \ forests and boosting, \ up to XGBoost",
            r"keeping score: \ ROC curves, \ cross-validation, \ and a contest of every method",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 6 of AI, Built, and the start of act two: learning from data. <bookmark mark='a'/> In it: "
            "least squares and why it's the best of its kind, ridge and the lasso; logistic regression, Newton's "
            "method and naive Bayes; Fisher's direction and nearest neighbours; kernels and support vector machines; "
            "trees, forests and boosting; and how to keep score honestly. Every method is written out in a few lines "
            "of numpy, and every number is computed on the pages."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
