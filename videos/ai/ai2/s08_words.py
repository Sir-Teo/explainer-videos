from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import MONO, load
from videos.ai.ai2.compute import DIM


class Words(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.neighbours()
        self.analogy()
        self.word2vec()
        self.w2v_learning()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Word vectors from counting", r"Can a computer learn what words mean by counting?",
                            lit=(1990, 2013), part=2)
        with self.voiceover("Chapter seven. Word vectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def table(self):
        w = load("words")
        assert w["n_words"] == 4353464 and len(w["vocab"]) == 10000
        T = np.asarray(w["top300"])
        v = np.clip(T / np.percentile(T[T > 0], 99), 0, 1) ** 0.6
        dark, lit = np.array(ManimColor("#121826").to_rgb()), np.array(ManimColor(C.CONTEXT).to_rgb())
        rgb = ((v[..., None] * lit + (1 - v[..., None]) * dark) * 255).astype(np.uint8)
        img = ImageMobject(rgb).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.height = 4.6
        img.move_to([-3.3, -0.5, 0])
        vocab = list(w["vocab"])
        ticks = VGroup(data_text(" ".join(vocab[:4]) + " …", font=MONO, font_size=20, color=GREY_A).next_to(img, UP, buff=0.12))
        cap = label(r"the $300$ commonest words, \\ of the $10{,}000$", font_size=24, color=GREY_B).next_to(img, DOWN, buff=0.15)
        P = C.CONTEXT
        pmi = cmath(r"\mathrm{PMI}(w, c)", "=", r"\log \frac{P(w, c)}{P(w)\,P(c)}", colors={r"\mathrm{PMI}(w, c)": P},
                    font_size=46).move_to([3.3, 1.4, 0])
        what = label(r"how much more often $w$ and $c$ meet \\ than if words were scattered at random", font_size=26,
                     color=GREY_A).next_to(pmi, DOWN, buff=0.3)
        keep = label(r"keep the positive part: \ $\max(\mathrm{PMI}, 0)$", font_size=28, color=P).next_to(what, DOWN, buff=0.35)
        counts = label(r"$4.35$ million words; \ pairs within $4$ words of each other", font_size=26, color=GREY_A)
        counts.to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now the same, with words. <bookmark mark='a'/> Take the ten thousand most common words in the thirty "
            "books, and count how often each pair turns up within four words of each other: a table with a hundred "
            "million cells, from four point three five million words of text. <bookmark mark='b'/> Then turn the "
            "counts into surprise, part one's way: how much more often do two words meet than they would by chance? "
            "That's the pointwise mutual information. Keep its positive part."
        ) as vo:
            self.play(FadeIn(counts))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("b")
            self.play(Write(pmi))
            self.play(FadeIn(what))
            self.play(FadeIn(keep))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neighbours(self):
        w = load("words")
        nb = w["neighbours"]
        s = np.asarray(w["s"])
        assert len(s) == 100
        show = ["monday", "three", "dog", "ship"]
        assert [x for x, _ in nb["monday"][:2]] == ["saturday", "tuesday"] and nb["three"][0][0] == "four"
        assert "perezvon" in [x for x, _ in nb["dog"]] and "wolf" in [x for x, _ in nb["dog"]]
        head = label(r"Keep the table's $100$ strongest directions: \ $100$ numbers per word", font_size=32)
        head.to_edge(UP, buff=0.4)
        cols = VGroup()
        for word in show:
            title = data_text(word, font=MONO, font_size=30, color=C.BITS)
            rows = VGroup()
            for x, sim in nb[word][:5]:
                bar = Rectangle(width=1.6 * sim, height=0.22, stroke_width=0, fill_color=C.CONTEXT, fill_opacity=0.85)
                rows.add(VGroup(data_text(x, font=MONO, font_size=22, color=WHITE), bar).arrange(RIGHT, buff=0.12))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            cols.add(VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3))
        cols.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.6)
        if cols.width > 13.2:
            cols.width = 13.2
        perez = label(r"Perezvon: \ a dog in \textit{The Brothers Karamazov}", font_size=26, color=GREY_A)
        perez.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Then keep the table's hundred strongest directions, with the singular value decomposition. "
            "<bookmark mark='a'/> Every word gets a hundred numbers. <bookmark mark='b'/> And words that keep the "
            "same company end up close together. Monday: Saturday, Tuesday, Sunday. Three: four, two, five. Dog: "
            "dogs, sheep, wolf, cat, and Perezvon, which, in The Brothers Karamazov, is a dog. Nobody gave it a "
            "dictionary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[0]) for c in cols], lag_ratio=0.2))
            vo.wait_until("b")
            for c in cols:
                self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in c[1]],
                                      lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(perez))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analogy(self):
        w = load("words")
        an = w["analogies"]
        assert an["france:paris::england"][0] == "london" and an["man:king::woman"][:2] == ["duke", "queen"]
        xy = np.asarray(w["analogy_xy"])
        xy = xy / np.abs(xy).max() * 2.6
        pts = [np.array([x, y, 0]) + DOWN * 0.3 for x, y in xy]
        names = ["france", "paris", "england", "london"]
        cols = [C.TRUE_P, C.BITS, C.TRUE_P, C.BITS]
        dots = VGroup(*[glow_dot(p, color=c, radius=0.09) for p, c in zip(pts, cols)])
        labs = VGroup(*[data_text(n, font=MONO, font_size=28, color=c).next_to(p, UP if k % 2 else DOWN, buff=0.18)
                        for k, (n, p, c) in enumerate(zip(names, pts, cols))])
        step = Arrow(pts[0], pts[1], buff=0.12, color=C.BITS, stroke_width=5)
        again = Arrow(pts[2], pts[2] + (pts[1] - pts[0]), buff=0.12, color=C.BITS, stroke_width=5)
        land = DashedLine(pts[2] + (pts[1] - pts[0]), pts[3], color=GREY_B, stroke_width=2)
        head = label(r"Directions mean something too", font_size=34).to_edge(UP, buff=0.4)
        near = an["france:paris::england"][:5]
        res = VGroup(label(r"the words nearest to where you land:", font_size=24, color=GREY_A),
                     *[data_text(f"{k + 1}. {wd}", font=MONO, font_size=24, color=C.BITS if k == 0 else WHITE)
                       for k, wd in enumerate(near)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.5)
        k2 = label(r"\texttt{man} : \texttt{king} :: \texttt{woman} : \ \texttt{duke}, \ \texttt{queen}, \ \ldots",
                   font_size=28, color=GREY_A).to_corner(DL, buff=0.6)
        tag = label(r"drawn on the plane of the two steps", font_size=22, color=GREY_B).to_corner(UR, buff=0.45)
        with self.voiceover(
            "Directions mean something too. <bookmark mark='a'/> Start at France, and step to Paris. Then take the "
            "same step, starting from England. <bookmark mark='b'/> The nearest word to where you land is London. "
            "Man is to king as woman is to: duke first, then queen. Novels from the nineteenth century had their "
            "own ideas."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(dots[2]), FadeIn(labs[2]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labs[1]), GrowArrow(step))
            self.play(TransformFromCopy(step, again), run_time=1.3)
            vo.wait_until("b")
            self.play(Create(land), FadeIn(dots[3]), FadeIn(labs[3]), FadeIn(res))
            self.play(FadeIn(k2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def word2vec(self):
        sg, w = load("sgns"), load("words")
        common = ["monday", "three", "ship"]
        assert all(sg["overlap"][x] >= 3 for x in common)
        colors = {r"\mathbf{w}": C.TRUE_P, r"\mathbf{c}": C.BITS, r"\mathbf{n}_i": C.PENALTY}
        f = cmath(r"\log \sigma(", r"\mathbf{w}", r"\cdot", r"\mathbf{c}", r")", "+", r"\textstyle\sum_{i=1}^{5}",
                  r"\log \sigma(-", r"\mathbf{w}", r"\cdot", r"\mathbf{n}_i", r")", colors=colors, font_size=42)
        f.to_edge(UP, buff=1.2)
        what = label(r"raise $\mathbf{w}\cdot\mathbf{c}$ for a real neighbour $c$, \ lower it for $5$ random words $n_i$",
                     font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.25)
        head = label(r"word2vec (2013): \ guess the neighbours", font_size=34).to_edge(UP, buff=0.4)
        loss = np.asarray(sg["loss"])
        ax = Axes(x_range=[0, len(loss) - 1, max(1, (len(loss) - 1) // 4)], y_range=[2.0, 4.4, 0.5], x_length=4.2,
                  y_length=2.4, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-4.2, -1.6, 0])
        curve = ax.plot_line_graph(np.arange(len(loss)), np.clip(loss, 2.0, 4.4), add_vertex_dots=False,
                                   line_color=C.LOSS, stroke_width=3)
        al = label(r"training loss", font_size=22, color=C.LOSS).next_to(ax, UP, buff=0.1)
        tabs = VGroup()
        for word in common:
            a = VGroup(*[data_text(x, font=MONO, font_size=20, color=WHITE) for x, _ in w["neighbours"][word][:3]]).arrange(DOWN, buff=0.08)
            b = VGroup(*[data_text(x, font=MONO, font_size=20, color=WHITE) for x, _ in sg["neighbours"][word][:3]]).arrange(DOWN, buff=0.08)
            t = data_text(word, font=MONO, font_size=24, color=C.BITS)
            tabs.add(VGroup(t, VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP)).arrange(DOWN, buff=0.15))
        tabs.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([2.6, -1.5, 0])
        hdr = label(r"counting $+$ SVD \quad\quad word2vec", font_size=22, color=GREY_B).next_to(tabs, UP, buff=0.2)
        lg = label(r"O.~Levy \& Y.~Goldberg (2014): \ word2vec factorizes the same PMI table, shifted",
                   font_size=26, color=C.BITS).to_edge(DOWN, buff=0.35)
        # factorizing: the big table as the product of two thin ones
        nv, nd = len(w["vocab"]), DIM
        big = Square(1.3, stroke_color=C.CONTEXT, stroke_width=2, fill_color=C.CONTEXT, fill_opacity=0.3)
        tall = Rectangle(width=0.16, height=1.3, stroke_color=C.TRUE_P, stroke_width=2, fill_color=C.TRUE_P, fill_opacity=0.4)
        wide = Rectangle(width=1.3, height=0.16, stroke_color=C.BITS, stroke_width=2, fill_color=C.BITS, fill_opacity=0.4)
        shapes = VGroup(big, MathTex(r"\approx", font_size=34), tall, MathTex(r"\times", font_size=30), wide).arrange(RIGHT, buff=0.22)
        dims_ = VGroup(*[MathTex(t, font_size=20, color=GREY_A).next_to(m, DOWN, buff=0.12) for t, m in (
            (rf"{nv:,} \times {nv:,}".replace(",", "{,}"), big), (rf"{nv:,} \times {nd}".replace(",", "{,}"), tall),
            (rf"{nd} \times {nv:,}".replace(",", "{,}"), wide))])
        dims_[1].shift(DOWN * 0.3)
        fac_card = gloss(r"factorizing a table", r"writing a big table as the product\\ of two thin ones", picture=VGroup(
            shapes, dims_), corner=DL, width=4.4, color=C.CONTEXT)
        fac_card.move_to([-4.3, -1.55, 0])
        with self.voiceover(
            "In 2013, Tomas Mikolov and his colleagues at Google trained word vectors another way: with a guessing "
            "game. From each word, guess the words around it. <bookmark mark='a'/> That's word2vec. We trained it on "
            "the same books, for three passes. <bookmark mark='b'/> For common words, its neighbours agree with the "
            "counting method's. <bookmark mark='c'/> And in 2014, Omer Levy and Yoav Goldberg showed why: word2vec is "
            "quietly factorizing the very same table of mutual information, writing that huge table as the product "
            "of two thin ones, a hundred numbers per word. Guessing and counting meet again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(what))
            self.play(Create(ax), FadeIn(al), Create(curve), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(t) for t in tabs], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(lg, shift=UP * 0.1), FadeOut(VGroup(ax, al, curve)), FadeIn(fac_card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def w2v_learning(self):
        """How word2vec learns: the nearest neighbours of four words, at checkpoints through training."""
        sg = load("sgns")
        steps = [int(s_) for s_ in sg["snap_steps"]]
        snaps = sg["snap_neighbours"]
        words = ["monday", "three", "father", "eyes"]
        total = int(sg["steps"])

        def column(k, word):
            return VGroup(*[data_text(x, font=MONO, font_size=20, color=WHITE) for x in snaps[k][word][:5]]).arrange(DOWN, buff=0.1)

        heads = VGroup(*[data_text(w_, font=MONO, font_size=26, color=C.BITS) for w_ in words]).arrange(RIGHT, buff=1.6).move_to([0, 1.8, 0])
        cols = VGroup(*[column(0, w_).next_to(h_, DOWN, buff=0.35) for w_, h_ in zip(words, heads)])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}\ \text{{of}}\ {total:,}".replace(",", "{,}"),
                                            font_size=30, color=C.BITS).to_edge(UP, buff=0.5))
        sub = label(r"each word's $5$ nearest neighbours, \ by the cosine of their vectors", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        days = "monday tuesday wednesday thursday friday saturday sunday january february march april may june july august"
        proper = lambda w_: w_.capitalize() if w_ in days.split() else w_  # noqa: E731
        step_card = gloss(r"training step, \ batch", r"each step looks at a small batch of examples\\ and nudges the "
                          r"vectors once", corner=UR, width=4.4)
        with self.voiceover(
            "Watch word2vec learn. Here are four words and their five nearest neighbours, at checkpoints during "
            "training. Training goes in steps: each step looks at a small batch of examples, and nudges the vectors "
            "once. <bookmark mark='a'/> At the start the vectors are random, and so are the neighbours. "
            f"<bookmark mark='b'/> After only {steps[1]} steps, most words' neighbours are the commonest words in "
            "the books, like 'they', 'is' and 'all': every batch pushes the frequent words, so they move first. "
            f"<bookmark mark='c'/> By step {steps[4]:,}, meaning appears: three sits with "
            f"{', '.join(snaps[4]['three'][:3])}, eyes with {', '.join(snaps[4]['eyes'][:3])}. "
            "<bookmark mark='d'/> By the end, Monday sits with "
            f"{proper(snaps[-1]['monday'][0])}, three with {', '.join(snaps[-1]['three'][:3])}, father with "
            f"{snaps[-1]['father'][0]} and {snaps[-1]['father'][1]}: nothing told it what a day or a number is; only "
            "which words keep company."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(cols), FadeIn(sub))
            self.add(cnt)
            self.play(FadeIn(step_card))
            vo.wait_until("a")
            marks = {1: "b", 2: "c", len(steps) - 1: "d"}  # hold on step 36 while it is described
            for k in range(1, len(steps)):
                if k in marks:
                    vo.wait_until(marks[k])
                if k == 2:
                    self.play(FadeOut(step_card), run_time=0.4)
                new = VGroup(*[column(k, w_).next_to(h_, DOWN, buff=0.35) for w_, h_ in zip(words, heads)])
                self.play(Transform(cols, new), t.animate.set_value(steps[k]), run_time=0.9)
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()
