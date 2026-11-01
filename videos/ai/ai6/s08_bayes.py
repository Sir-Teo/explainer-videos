from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, HL, MONO, chapter, load, plot

NB, LR, PLATT = "#4FD1C5", C.MODEL_Q, "#B48EF0"


class NaiveBayes(VoiceoverScene):
    def construct(self):
        chapter(self, 7, r"Naive Bayes: generative or discriminative?", r"Model the author, or model the writing?",
                "Chapter seven. Naive Bayes.")
        self.derive()
        self.learned()
        self.race()
        self.calibrate()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\theta_{D,w}": DICKENS, r"\theta_{A,w}": AUSTEN, r"\beta_w": HL}
        rows = [
            cmath(r"P(D \mid \text{page})", r"\;\propto\;", r"P(D)\prod_w \theta_{D,w}^{\,c_w}", font_size=34,
                  colors=colors),
            cmath(r"\log\frac{P(D \mid \text{page})}{P(A \mid \text{page})}", "=",
                  r"\log\frac{P(D)}{P(A)} + \sum_w c_w \log\frac{\theta_{D,w}}{\theta_{A,w}}", font_size=34, colors=colors),
            cmath(r"\log\frac{P(D \mid \text{page})}{P(A \mid \text{page})}", "=", r"b + \sum_w \beta_w\, c_w",
                  font_size=34, colors=colors),
            cmath(r"\theta_{D,w}", "=", r"\frac{\text{count}_{D,w} + 1}{N_D + 70}", font_size=34, colors=colors),
        ]
        whys = [why(r"Bayes' rule; \\ each word drawn independently"), why(r"take logs, \ divide"),
                why(r"a straight line \\ in the counts!"), why(r"Laplace's $+1$ \ (Part 1)")]
        step = ladder(self, rows, whys, keep=4, top=1.15, x=-0.6, buff=0.32, edge=6.8)
        gen = definition_card(r"generative", r"model how each author writes, $P(\text{page} \mid \text{author})$, "
                              r"then turn it around with Bayes' rule", width=6.4, font_size=22, color=NB)
        dis = definition_card(r"discriminative", r"model $P(\text{author} \mid \text{page})$ directly, as logistic "
                              r"regression does", width=6.4, font_size=22, color=LR)
        cards = VGroup(gen, dis).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Logistic regression models the answer directly. Naive Bayes models the writing. "
            "<bookmark mark='a'/> Pretend each author writes by drawing words independently, Dickens with "
            "probabilities theta D. Bayes' rule turns that around. <bookmark mark='b'/> Take the log of the odds. "
            "<bookmark mark='c'/> It's a weighted sum of the word counts plus a constant: a straight line, the same "
            "family as logistic regression, but with weights read off from counting, not fitted. "
            "<bookmark mark='d'/> Add one to every count, Laplace's rule from Part 1, so no word is impossible. "
            "<bookmark mark='e'/> Two philosophies: generative models how the data is made; discriminative models "
            "only the decision."
        ) as vo:
            self.play(FadeIn(cards, shift=DOWN * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            vo.wait_until("e")
            self.play(Indicate(gen.head, color=NB, scale_factor=1),
                      Indicate(dis.head, color=LR, scale_factor=1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        d = load("nbvslr")
        A, D = d["nb_austen"], d["nb_dickens"]
        top = max(abs(v) for _, v in A + D) * 1.05
        W = 3.6

        def row(w, v, col):
            L = W * abs(v) / top
            bar = Rectangle(width=L, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.85)
            word = data_text(w, font=MONO, font_size=24, color=col)
            val = MathTex(f"{v:+.2f}", font_size=24, color=col)
            return VGroup(bar, word, val)

        left, right = VGroup(), VGroup()
        for k, (w, v) in enumerate(A):
            r = row(w, v, AUSTEN)
            r[0].move_to([-0.3 - r[0].width / 2, 1.3 - 0.55 * k, 0])
            r[1].next_to(r[0], LEFT, buff=0.15)
            r[2].next_to([-0.3, r[0].get_y(), 0], RIGHT, buff=0.12).set_opacity(0)
            left.add(r)
        for k, (w, v) in enumerate(D):
            r = row(w, v, DICKENS)
            r[0].move_to([0.3 + r[0].width / 2, 1.3 - 0.55 * k, 0])
            r[1].next_to(r[0], RIGHT, buff=0.15)
            r[2].set_opacity(0)
            right.add(r)
        axis = Line([0, 1.7, 0], [0, -1.8, 0], color=GREY_B, stroke_width=2)
        head = cmath(r"\beta_w", "=", r"\log\frac{\theta_{D,w}}{\theta_{A,w}}", font_size=40,
                     colors={r"\beta_w": HL}).to_edge(UP, buff=0.3)
        tl = label(r"Austen's words", font_size=26, color=AUSTEN).move_to([-3.0, 2.1, 0])
        tr = label(r"Dickens's words", font_size=26, color=DICKENS).move_to([3.0, 2.1, 0])
        note_ = note(r"weights from counting all the training pages; \ $+1$ means $e$ times more likely in Dickens").to_edge(DOWN, buff=0.3)
        aw = ", ".join(f"'{w}'" for w, _ in A[:3])
        dw = ", ".join(f"'{w}'" for w, _ in D[:3])
        with self.voiceover(
            "Here's what it learned, by counting. Each word's weight is the log of how much more often Dickens "
            f"uses it than Austen. <bookmark mark='a'/> Austen's strongest words: {aw}. <bookmark mark='b'/> Dickens's: "
            f"{dw}. Every occurrence of a word adds its weight to the page's log-odds."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tl), FadeIn(tr), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_[0], RIGHT) for r_ in left], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(r_[1]) for r_ in left], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_[0], LEFT) for r_ in right], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(r_[1]) for r_ in right], lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("nbvslr")
        sizes = [int(m) for m in d["sizes"]]
        lx = np.log10(sizes)
        # Enclose the actual means and both percentile endpoints; never flatten
        # measured uncertainty against a preset display ceiling.
        peak = max(d[key][str(m)][field] for key in ("nb", "lr")
                   for m in sizes for field in ("mean", "lo", "hi"))
        top = math.ceil(1.08 * peak / 0.05) * 0.05
        tick_step = 0.1 if top <= 0.5 else 0.2
        yticks = np.arange(0, top + 1e-9, tick_step).tolist()
        g = plot([lx[0] - 0.05, lx[-1] + 0.05, 1], [0, top, tick_step], x_length=7.4, y_length=4.4,
                 xticks=[math.log10(v) for v in (4, 16, 64, 256)], yticks=yticks,
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-2.3, -0.4, 0],
                 xlabel=r"training pages \ (log scale)", ylabel=r"error on the held-out pages \ (all $70$ word counts)")
        ax = g.ax
        art = {}
        for key, col in (("nb", NB), ("lr", LR)):
            m_ = [d[key][str(m)]["mean"] for m in sizes]
            lo = [d[key][str(m)]["lo"] for m in sizes]
            hi = [d[key][str(m)]["hi"] for m in sizes]
            art[key] = (band(ax, lx, lo, hi, col, opacity=0.18), curve(ax, lx, m_, col, stroke_width=4),
                        VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=col) for a, b in zip(lx, m_)]))
        key_ = VGroup(label(r"naive Bayes", font_size=26, color=NB), label(r"logistic regression", font_size=26, color=LR),
                      note(r"lines: \ average over many random draws; \\ bands: \ $10$th to $90$th percentile"))
        key_.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 1.9, 0])
        cross = d["crossover"]
        nb_end, lr_end = d["nb"][str(sizes[-1])]["mean"], d["lr"][str(sizes[-1])]["mean"]
        better = d["nb_better_at"]
        hist = note(r"A.~Ng \& M.~Jordan, \textit{On Discriminative vs.\ Generative Classifiers} (2002)").to_corner(DR, buff=0.2)
        res = VGroup(
            label(rf"naive Bayes ahead up to ${max(better)}$ pages" if better else r"naive Bayes never ahead",
                  font_size=24, color=NB),
            label(rf"logistic ahead from ${cross}$ pages on" if cross else r"no crossover", font_size=24, color=LR),
            label(rf"all ${sizes[-1]}$: \ ${100 * nb_end:.1f}\%$ \ vs \ ${100 * lr_end:.1f}\%$", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(key_, DOWN, buff=0.45).align_to(key_, LEFT)
        if better and cross:
            say = (f"With a handful of pages, naive Bayes is ahead: up to {max(better)} training pages, its error is "
                   f"lower. <bookmark mark='b'/> From {cross} pages on, logistic regression overtakes it, and keeps "
                   f"improving: with all {sizes[-1]}, {100 * lr_end:.1f} percent wrong against naive Bayes' "
                   f"{100 * nb_end:.1f}. Exactly the crossover Ng and Jordan predicted in 2002: the generative model "
                   "gets to its best quickly, but its best is worse, because its assumption is false.")
        else:
            say = (f"Here the expected crossover doesn't appear cleanly. <bookmark mark='b'/> With all {sizes[-1]} pages, "
                   f"logistic regression is {100 * lr_end:.1f} percent wrong, naive Bayes {100 * nb_end:.1f}.")
        with self.voiceover(
            "Which is better? Ng and Jordan's answer: it depends on how much data you have. Train both on random "
            "sets of pages, from four up to all of them, many times over, and test on the held-out pages. "
            f"<bookmark mark='a'/> {say}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(key_), FadeIn(hist))
            for k_ in ("nb", "lr"):
                b_, c_, d_ = art[k_]
                self.play(FadeIn(b_), Create(c_), FadeIn(d_), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
            if cross:
                self.play(Create(DashedLine(ax.c2p(math.log10(cross), 0), ax.c2p(math.log10(cross), top), color=HL,
                                            stroke_width=2)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def calibrate(self):
        c = load("calibration")
        panels = VGroup()
        specs = [("lr2", r"logistic, \ $2$ rates", LR), ("nb", r"naive Bayes, \ $70$ words", NB),
                 ("nb_platt", r"naive Bayes, \ Platt-scaled", PLATT)]
        for k, (key, title, col) in enumerate(specs):
            g = plot([0, 1, 0.5], [0, 1, 0.5], x_length=3.4, y_length=3.0, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                     center=[-4.4 + 4.4 * k, -0.6, 0], xlabel=r"predicted $P(\text{Dickens})$" if k == 1 else "",
                     ylabel=r"how often Dickens" if k == 0 else "")
            ax = g.ax
            diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
            r = c[key]
            cnt = np.asarray(r["count"])
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.04 + 0.12 * math.sqrt(n_ / cnt.max()), color=col, fill_opacity=0.8)
                           for a, b, n_ in zip(r["conf"], r["frac"], cnt) if n_ > 0])
            t = label(title, font_size=24, color=col).next_to(g, UP, buff=0.12)
            e = label(rf"calibration error ${r['ece']:.3f}$", font_size=22, color=GREY_A).next_to(g, DOWN, buff=0.15)
            if k == 1:
                e.next_to(g, DOWN, buff=0.15)
            panels.add(VGroup(g, diag, pts, t, e))
        head = label(r"Are the probabilities honest? \ Ten folds, \ every page predicted once", font_size=28).to_edge(UP, buff=0.3)
        tag = note(r"dots: \ pages grouped by predicted probability; \ size: \ how many").to_edge(DOWN, buff=0.15)
        ext = c["nb_extreme"]
        e_nb, e_pl, e_lr = c["nb"]["ece"], c["nb_platt"]["ece"], c["lr2"]["ece"]
        fixed = e_pl < e_nb
        end = (f"and the error falls from {e_nb:.3f} to {e_pl:.3f}." if fixed else
               f"though here the error doesn't fall: {e_nb:.3f} to {e_pl:.3f}.")
        with self.voiceover(
            "There's a second difference. When a model says seventy percent, is it right seventy percent of the time? "
            "Group the pages by the probability given, and plot how often they really were Dickens. Honest "
            f"probabilities lie on the diagonal. <bookmark mark='a'/> Logistic regression's are close: average error "
            f"{e_lr:.3f}. <bookmark mark='b'/> Naive Bayes counts every word as independent evidence, so it's wildly "
            f"sure of itself: {100 * ext:.0f} percent of pages get odds beyond a million to one. <bookmark mark='c'/> "
            f"Platt's fix, in 1999, fits a one-variable logistic regression to its scores on training pages, {end}"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(panels[0][:2]), FadeIn(panels[0][3]))
            self.play(FadeIn(panels[0][2]), FadeIn(panels[0][4]))
            vo.wait_until("a")
            self.play(Indicate(panels[0][2], color=WHITE, scale_factor=1))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]))
        self.wait(0.3)
        self.clear_scene()
