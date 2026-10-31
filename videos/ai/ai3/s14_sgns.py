from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MONO, chapter, dots_on, load

WC, CC, NC = C.TRUE_P, C.BITS, C.PENALTY
SVDC, SGC = C.CONTEXT, C.REWARD


class SGNS(VoiceoverScene):
    def construct(self):
        chapter(self, 13, r"word2vec is counting in disguise", r"What does a guessing game learn?",
                "Chapter thirteen. Word2vec, which turns out to be counting in disguise.", lit=(2013,))
        self.game()
        self.replay()
        self.derive()
        self.exact()
        self.real()
        self.compare()

    # ------------------------------------------------------------------
    def game(self):
        sg = load("sgns")
        K = int(sg["k"])
        colors = {r"\mathbf{w}": WC, r"\mathbf{c}": CC, r"\mathbf{n}_i": NC}
        f = cmath(r"\log \sigma(", r"\mathbf{w}", r"\cdot", r"\mathbf{c}", r")", "+", rf"\textstyle\sum_{{i=1}}^{{{K}}}",
                  r"\log \sigma(-", r"\mathbf{w}", r"\cdot", r"\mathbf{n}_i", r")", colors=colors, font_size=44)
        f.move_to(UP * 0.9)
        what = label(rf"raise $\mathbf{{w}}\cdot\mathbf{{c}}$ for a real neighbour $c$; \ lower it for ${K}$ random "
                     r"words $n_i$", font_size=28, color=GREY_A).next_to(f, DOWN, buff=0.3)
        sig = label(r"$\sigma(x) = 1/(1 + e^{-x})$: \ the logistic function", font_size=24, color=GREY_B)
        sig.next_to(what, DOWN, buff=0.25)
        hist = history_card(2013, r"T.~Mikolov, \ I.~Sutskever, \ K.~Chen, \ G.~Corrado \& J.~Dean, \ Google",
                            r"word2vec: \ skip-gram with negative sampling, \ trained on billions of words in hours",
                            color=HIST, width=6.2).to_edge(DOWN, buff=0.3)
        head = label(r"Guess the neighbours", font_size=38).to_edge(UP, buff=0.4)
        sent = data_text("the old dog barked at the moon", font=MONO, font_size=30, color=GREY_A).next_to(head, DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "In 2013 Tomas Mikolov and colleagues at Google learned word vectors with a guessing game. "
            "<bookmark mark='a'/> Each word gets two vectors, one as the word and one as a neighbour. "
            "<bookmark mark='b'/> Training raises a word's dot product with its real neighbours, through the logistic "
            f"function, and lowers it with {K} random words. <bookmark mark='c'/> That is skip-gram with negative "
            "sampling, the heart of word2vec: cheap enough for billions of words in hours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sent))
            vo.wait_until("a")
            self.play(Write(f), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(what), FadeIn(sig))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        """How word2vec learns: the loss and the nearest neighbours of four words, at checkpoints through training."""
        sg = load("sgns")
        steps = [int(s_) for s_ in sg["snap_steps"]]
        snaps = sg["snap_neighbours"]
        words = ["monday", "three", "father", "eyes"]
        total = int(sg["steps"])
        loss = np.asarray(sg["loss"])
        lx = np.asarray(sg["loss_steps"], float)
        g = axes([0, total, max(1, total // 4)], [float(loss.min()) - 0.2, float(loss.max()) + 0.2, 1],
                 x_length=4.2, y_length=2.2, xlabel=r"step", ylabel=r"loss", center=[-4.5, -2.3, 0], font_size=18)
        ax = g.ax
        lc = curve(ax, lx, loss, C.LOSS, 2.5)
        t = ValueTracker(0)
        live_loss = always_redraw(lambda: lc.copy().pointwise_become_partial(
            lc, 0, float(np.clip(t.get_value() / max(lx[-1], 1), 0, 1))))
        cursor = always_redraw(lambda: Line(ax.c2p(t.get_value(), float(loss.min()) - 0.2),
                                            ax.c2p(t.get_value(), float(loss.max()) + 0.2), color=WHITE, stroke_width=2))

        def column(k, word):
            return VGroup(*[data_text(x, font=MONO, font_size=20, color=WHITE).move_to(DOWN * 0.38 * i)
                            for i, x in enumerate(snaps[k][word][:5])])

        heads = VGroup(*[data_text(w_, font=MONO, font_size=26, color=C.BITS) for w_ in words]).arrange(RIGHT, buff=1.6)
        heads.move_to([0.6, 2.4, 0])
        cols = VGroup(*[column(0, w_).next_to(h_, DOWN, buff=0.35) for w_, h_ in zip(words, heads)])
        # Reuse digit glyphs rather than compiling a new TeX file every frame.
        slot = Integer(total, font_size=30, color=C.BITS).set_opacity(0)
        cnt = VGroup(MathTex(r"\text{step}", font_size=30, color=C.BITS), slot,
                     MathTex(rf"\text{{of}}\ {total:,}".replace(",", "{,}"), font_size=30, color=C.BITS))
        cnt.arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.3)
        count_value = Integer(0, font_size=30, color=C.BITS)
        count_value.add_updater(lambda m: m.set_value(int(t.get_value())).align_to(slot, RIGHT).set_y(slot.get_y()))
        cnt.add(count_value)
        count_value.update()
        sub = label(rf"trained here: \ the novels, \ ${sg['pairs'] / 1e6:.0f}$ million (word, neighbour) pairs, \ "
                    rf"three passes", font_size=22, color=GREY_A).to_corner(DR, buff=0.3)
        days = "monday tuesday wednesday thursday friday saturday sunday"
        proper = lambda w_: w_.capitalize() if w_ in days.split() else w_  # noqa: E731
        mid = min(4, len(steps) - 1)
        with self.voiceover(
            "We trained it on the novels, with the same vocabulary and nominal window as the counting. "
            "Subsampling frequent words changes the actual context sequences. Four words and their "
            "nearest neighbours, with the loss below. <bookmark mark='a'/> At the start, random. <bookmark mark='b'/> "
            f"After {steps[1]} steps, the lists are still mixed; some favour common function words. "
            f"<bookmark mark='c'/> By step {steps[mid]:,}, meaning appears: three sits with "
            f"{', '.join(snaps[mid]['three'][:3])}. <bookmark mark='d'/> By the end, Monday sits with "
            f"{proper(snaps[-1]['monday'][0])}, and father with {snaps[-1]['father'][0]}. Nothing told it what a day or a "
            "relative is."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(cols), FadeIn(sub), FadeIn(g))
            self.add(cnt, cursor, live_loss)
            vo.wait_until("a")
            marks = {1: "b", mid: "c", len(steps) - 1: "d"}
            # Hold each described snapshot until the next narration bookmark.
            # Keep unspoken intermediate checkpoints in the measured data.
            for k in sorted(marks):
                vo.wait_until(marks[k])
                new = VGroup(*[column(k, w_).next_to(h_, DOWN, buff=0.35) for w_, h_ in zip(words, heads)])
                self.play(FadeOut(cols, rate_func=squish_rate_func(smooth, 0.0, 0.45)),
                          FadeIn(new, rate_func=squish_rate_func(smooth, 0.5, 1.0)), t.animate.set_value(steps[k]),
                          run_time=0.9)
                cols = new
        cnt.clear_updaters()
        cursor.clear_updaters()
        live_loss.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\#(w,c)": CC, r"k\,\#(w)\,P_n(c)": NC}
        rows = [
            cmath(r"\ell(x)", "=", r"\#(w,c)", r"\log\sigma(x) + ", r"k\,\#(w)\,P_n(c)", r"\log\sigma(-x)", font_size=32,
                  colors=colors),
            cmath(r"\ell'(x)", "=", r"\#(w,c)", r"\,\sigma(-x) - ", r"k\,\#(w)\,P_n(c)", r"\,\sigma(x) = 0", font_size=32,
                  colors=colors),
            cmath(r"e^{x}", "=", r"\frac{\#(w,c)}{k\,\#(w)\,P_n(c)}", font_size=34),
            cmath(r"\mathbf{w}\cdot\mathbf{c}", "=", r"\log\frac{\#(w,c)}{\#(w)\,P_n(c)} - \log k",
                  font_size=34, colors={r"\mathbf{w}\cdot\mathbf{c}": WC}),
        ]
        whys = [why(r"the log objective, cell by cell: \ the pair seen $\#(w,c)$ times, \\ drawn as a negative "
                    r"$k\,\#(w)\,P_n(c)$ times on average", font_size=22),
                why(r"$\sigma' = \sigma(1 - \sigma)$, \ $1 - \sigma(x) = \sigma(-x)$", font_size=22),
                why(r"$\sigma(x) / \sigma(-x) = e^x$", font_size=22),
                why(r"if $P_n(c)=P(c)$: \ $\mathrm{PMI}(w,c)-\log k$", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=1.3, x=-2.0, buff=0.45, edge=6.9)
        thm = theorem_card(r"Levy \& Goldberg (2014)",
                           r"For observed pairs with free dot products, \ the log objective is maximized at "
                           r"$x=\log\frac{\#(w,c)}{k\,\#(w)P_n(c)}$. \ If $P_n(c)=P(c)$, \ this is "
                           r"$\mathrm{PMI}(w,c)-\log k$.", width=8.0).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Why do guessing and counting agree? In 2014 Omer Levy and Yoav Goldberg showed why. "
            "<bookmark mark='a'/> Collect the log objective for one word and one context: the pair appears as a real neighbour "
            "some number of times, and as a negative about k times the word's count times the context's sampling "
            "probability. <bookmark mark='b'/> Treat their dot product x as free; set the derivative to zero. "
            "<bookmark mark='c'/> The ratio of the two logistic terms is e to the x. <bookmark mark='d'/> Take logs: "
            "this maximizes the log objective. If negatives follow the empirical context distribution, the best dot "
            "product is PMI minus log k. With smoothed negatives, as in our run, use their sampling probability "
            "in the same log-count ratio: a generalized shifted PMI."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        sg = load("sgns")
        ex = sg["lg_exact"]
        dims = [int(d) for d in ex["dims"]]
        V = int(ex["V"])
        allx = np.concatenate([np.asarray(ex["runs"][str(d)]["x"]) for d in dims])
        lo, hi = float(np.percentile(allx, 0.5)), float(np.percentile(allx, 99.5))
        panels = VGroup()
        for d in dims:
            r = ex["runs"][str(d)]
            ax = Axes(x_range=[lo, hi, 2], y_range=[lo, hi, 2], x_length=3.2, y_length=3.2, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False})
            x, y = np.asarray(r["x"]), np.asarray(r["y"])
            pick = np.arange(0, len(x), 3)
            inside = (x[pick] >= lo) & (x[pick] <= hi) & (y[pick] >= lo) & (y[pick] <= hi)
            omitted = int((~inside).sum())
            pick = pick[inside]
            pts = VGroup(*[Dot(ax.c2p(float(x[i]), float(y[i])), radius=0.018, color=SGC, fill_opacity=0.6) for i in pick])
            diag = Line(ax.c2p(lo, lo), ax.c2p(hi, hi), color=WHITE, stroke_width=1.5)
            t = label(rf"$d = {d}$", font_size=28, color=WHITE).next_to(ax, UP, buff=0.1)
            e = label(rf"median error ${r['median_err']:.3f}$ \\ ${omitted}$ sampled points outside the window omitted",
                      font_size=18, color=SGC).next_to(ax, DOWN, buff=0.1)
            panels.add(VGroup(ax, diag, pts, t, e))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.15)
        if panels.width > 12.8:
            panels.scale_to_fit_width(12.8)
        xl = label(r"across: \ generalized shifted PMI; \quad up: \ $\mathbf{w}\cdot\mathbf{c}$, \ trained", font_size=22,
                   color=GREY_A).next_to(panels, DOWN, buff=0.2)
        yl = VectorizedPoint()
        head = label(rf"${V}$ commonest words; \ $3{{,}}000$ Adam steps; \ ${fmt_int(ex['cells'])}$ pairs seen at least $5$ times",
                     font_size=27).to_edge(UP, buff=0.35)
        r0, r1, r2 = (ex["runs"][str(d)] for d in dims)
        with self.voiceover(
            f"Let's check it on the {V} commonest words, after three thousand Adam steps. We measure "
            f"{ex['cells']:,} observed pairs seen at least five times. <bookmark mark='a'/> With {dims[0]} numbers "
            "per vector, all dot products can be free in principle, but finite training is not a convergence "
            f"certificate: the measured median error from generalized shifted PMI is {r0['median_err']:.3f}. "
            f"<bookmark mark='b'/> With {dims[1]}, the points "
            f"spread: {r1['median_err']:.2f}. <bookmark mark='c'/> With {dims[2]}, {r2['median_err']:.2f}. A short "
            "vector holds only a low-rank version of the table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(xl), FadeIn(yl), *[FadeIn(VGroup(p[0], p[1], p[3])) for p in panels])
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(d_) for d_ in panels[k][2]], lag_ratio=0.002), FadeIn(panels[k][4]),
                          run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real(self):
        sg = load("sgns")
        lg = sg["lg"]
        x, y = np.asarray(lg["x"]), np.asarray(lg["y"])
        lo, hi = float(min(np.percentile(x, 0.5), np.percentile(y, 0.5))), float(max(np.percentile(x, 99.5),
                                                                                       np.percentile(y, 99.5)))
        g = axes([lo, hi, 2], [lo, hi, 2], x_length=4.8, y_length=4.8, xlabel=r"generalized shifted PMI, \ counted from the "
                 r"pairs it saw", ylabel=r"$\mathbf{w}\cdot\mathbf{c}$ \ after training", center=[-3.0, -0.4, 0])
        ax = g.ax
        diag = Line(ax.c2p(lo, lo), ax.c2p(hi, hi), color=WHITE, stroke_width=1.5)
        pick = np.arange(0, len(x), 2)
        inside = (x[pick] >= lo) & (x[pick] <= hi) & (y[pick] >= lo) & (y[pick] <= hi)
        omitted = int((~inside).sum())
        pick = pick[inside]
        pts = VGroup(*[Dot(ax.c2p(float(x[i]), float(y[i])), radius=0.02, color=SGC,
                           fill_opacity=0.55) for i in pick])
        stats = VGroup(label(rf"${fmt_int(lg['n'])}$ pairs seen at least ${lg['min_count']}$ times", font_size=26),
                       label(rf"correlation ${lg['r']:.2f}$", font_size=30, color=SGC),
                       label(rf"slope ${lg['slope']:.2f}$", font_size=30, color=SGC)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.25)
        stats.move_to([3.4, 0.6, 0])
        why_ = label(r"$100$ numbers per word for $10{,}000$ words, \\ three passes, \\ and a loss that weighs "
                     r"frequent pairs more", font_size=24, color=GREY_A).next_to(stats, DOWN, buff=0.4).align_to(stats, LEFT)
        head = label(r"The real run: \ $10{,}000$ words, \ $100$ numbers each", font_size=32).to_edge(UP, buff=0.35)
        cap = note(rf"diagnostic cohort: top $2{{,}}000$ words; \ every second stored sample drawn \\ "
                   rf"${omitted}$ points outside the percentile window omitted; \ statistics use the full cohort",
                   font_size=17).to_edge(DOWN, buff=0.15)
        strong = lg["r"] > 0.7
        verdict = ("They agree closely, though the low rank pulls the extremes toward the middle."
                   if strong else "They agree only loosely: a hundred numbers can't hold the whole table, and the "
                   "training stopped early.")
        with self.voiceover(
            "And the real run, ten thousand words with a hundred numbers each? <bookmark mark='a'/> For the "
            f"{int(lg['n']):,} pairs it saw at least {lg['min_count']} times: trained dot product against the shifted "
            f"PMI of its own training pairs. <bookmark mark='b'/> Correlation {lg['r']:.2f}, slope {lg['slope']:.2f}. "
            f"{verdict}"
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in pts], lag_ratio=0.001), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats], lag_ratio=0.3), FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        sg, w = load("sgns"), load("words")
        a1, a2 = w["analogy_test"], sg["analogy_test"]
        p1, p2 = w["purity"], sg["purity"]
        rels = ["gender", "plural", "past", "comparative", "ordinal"]
        names = {"gender": r"man : woman", "plural": r"dog : dogs", "past": r"walk : walked",
                 "comparative": r"old : older", "ordinal": r"three : third", "all": r"all analogies"}
        rows = VGroup()
        for r in rels + ["all"]:
            rows.add(VGroup(label(names[r] + (rf" \ (${a1[r]['n']}$)" if r != "all" else rf" \ (${a1['all']['n']}$)"),
                                  font_size=24, color=GREY_A if r != "all" else WHITE),
                            MathTex(rf"{100 * a1[r]['acc']:.0f}\%", font_size=28, color=SVDC),
                            MathTex(rf"{100 * a2[r]['acc']:.0f}\%", font_size=28, color=SGC)))
        rows.add(VGroup(label(r"category neighbours", font_size=24, color=WHITE),
                        MathTex(rf"{100 * p1['purity']:.0f}\%", font_size=28, color=SVDC),
                        MathTex(rf"{100 * p2['purity']:.0f}\%", font_size=28, color=SGC)))
        hdr = VGroup(label(r"test", font_size=22, color=GREY_B), label(r"counting $+$ SVD", font_size=22, color=SVDC),
                     label(r"word2vec", font_size=22, color=SGC))
        tab = VGroup(hdr, *rows)
        for r in tab:
            r.arrange(RIGHT, buff=0.5)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        regrid(tab, gap=0.6)
        tab.move_to([-2.4, -0.3, 0])
        glove = history_card(2014, r"J.~Pennington, \ R.~Socher \& C.~Manning, \ GloVe",
                             r"fit $\mathbf{w}\cdot\mathbf{c} + b_w + b_c \approx \log \#(w,c)$ \ by weighted least "
                             r"squares: \ the counting, made explicit", color=HIST, width=4.6).move_to([4.4, 0.9, 0])
        nxt = label(r"one vector per word, \\ whatever the sentence: \\ Parts 13--14 make them contextual", font_size=24,
                    color=C.BITS).move_to([4.4, -1.9, 0])
        head = label(r"Counting against guessing, \ on the same books", font_size=34).to_edge(UP, buff=0.3)
        d_an = a2["all"]["acc"] - a1["all"]["acc"]
        if abs(d_an) < 0.03:
            verdict = "On analogies the two methods are about even."
        elif d_an > 0:
            verdict = "On analogies word2vec does better."
        else:
            verdict = "On analogies the counting method does better."
        with self.voiceover(
            "Which is better? <bookmark mark='a'/> On our analogy questions, counting gets "
            f"{100 * a1['all']['acc']:.0f} percent and word2vec {100 * a2['all']['acc']:.0f}. {verdict} On category "
            f"neighbours, {100 * p1['purity']:.0f} against {100 * p2['purity']:.0f}. Levy, Goldberg and Dagan found in "
            "2015 that, tuned with equal care, the two families are close. <bookmark mark='b'/> GloVe, in 2014, fitted "
            "the log counts directly. <bookmark mark='c'/> All of these give one vector per word: bank by a river and "
            "bank with money share one. Parts 13 and 14 make vectors depend on context."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(glove, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
