from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import (AUSTEN, BAD, DICKENS, GOOD, HIST, HL, chapter, load, page_plane, plot, regions,
                                  sci_tex, X_RANGE, Y_RANGE, author_color)

EXPC = "#B48EF0"
SHOW = [1, 2, 3, 5, 10, 30]


class AdaBoost(VoiceoverScene):
    def construct(self):
        chapter(self, 14, r"AdaBoost and the exponential loss", r"Can many weak rules make a strong one?",
                "Chapter fourteen. Boosting.", lit=(2001,))
        self.reweight()
        self.derive()
        self.curves()
        self.faces()

    # ------------------------------------------------------------------
    def reweight(self):
        a = load("adaboost")
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        tr = np.nonzero(~test)[0]
        plane = page_plane(x_length=6.8, y_length=4.6, center=[-3.0, -0.3, 0])
        ax = plane[0]
        g = np.random.default_rng(0)
        jit = g.uniform(-0.3, 0.3, (len(tr), 2))

        def dots(w):
            w = np.asarray(w)
            sz = np.clip(0.032 * np.sqrt(w * len(w)), 0.02, 0.17)  # area grows with the weight; 0.032 at 1/n
            out = VGroup()
            for k, i in enumerate(tr):
                x, v = X2[i] + jit[k]
                if X_RANGE[0] <= x <= X_RANGE[1] and Y_RANGE[0] <= v <= Y_RANGE[1]:
                    out.add(Dot(ax.c2p(x, v), radius=float(sz[k]), color=author_color(int(y[i])), fill_opacity=0.75,
                                stroke_width=0))
            return out

        n = len(tr)
        d0 = dots(np.full(n, 1.0 / n))
        imgs = {k: regions(ax, (np.asarray(a[f"region{k}"]) + 1) / 2, a["xs"], a["ys"], opacity=0.42) for k in SHOW}
        ds = {k: dots(a[f"w{k}"]) for k in SHOW}
        st = a["stumps_2"]
        rv = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{round }} {SHOW[int(round(rv.get_value()))]}", font_size=34, color=HL)
                            .next_to(ax, UP, buff=0.1).align_to(ax, RIGHT))
        algo = VGroup(label(r"AdaBoost", font_size=30, color=HL),
                      label(r"1. \ fit a stump (one question) \\ \ \ \ \ to the weighted pages", font_size=22, color=GREY_A),
                      label(r"2. \ its weighted error $\varepsilon$; \ its vote \\ \ \ \ \ $\alpha = \tfrac12\log\frac{1 - "
                            r"\varepsilon}{\varepsilon}$", font_size=22, color=GREY_A),
                      label(r"3. \ multiply the weight of every page \\ \ \ \ \ it got wrong by $e^{2\alpha}$", font_size=22,
                            color=GREY_A),
                      label(r"4. \ repeat; \ the committee votes", font_size=22, color=GREY_A))
        algo.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.2, 0.5, 0])
        cite_ = cite(r"Y.~Freund \& R.~Schapire (1997); \ G\"odel Prize, 2003", corner=DR)
        e1 = a["eps_2"][0]
        with self.voiceover(
            "Boosting asks a different question: can many weak rules make a strong one? Freund and Schapire's "
            "AdaBoost, in 1997, said yes. <bookmark mark='a'/> Start with every training page weighted equally, and "
            f"find the best single question, a stump. It gets {100 * e1:.0f} percent of the weight wrong. "
            "<bookmark mark='b'/> Now make the pages it got wrong heavier, and find the best stump for the "
            "reweighted pages. <bookmark mark='c'/> Repeat. The weight piles up on the hard pages, along the border "
            "between the authors, and the committee's vote, each stump weighted by alpha, carves the plane."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(d0), FadeIn(algo[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(cnt), FadeIn(algo[1]), FadeIn(algo[2]))
            self.bring_to_front(d0)
            vo.wait_until("b")
            self.play(Transform(d0, ds[1]), FadeIn(algo[3]))
            vo.wait_until("c")
            cur = imgs[1]
            for i, k in enumerate(SHOW[1:], 1):
                self.play(FadeOut(cur), FadeIn(imgs[k]), Transform(d0, ds[k]), rv.animate.set_value(i), run_time=1.0)
                self.bring_to_front(d0)
                cur = imgs[k]
            self.play(FadeIn(algo[4]))
        cnt.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        a = load("adaboost")
        colors = {r"w_i": HL, r"\alpha": EXPC, r"\varepsilon": BAD}
        rows = [
            cmath(r"L(\alpha)", "=", r"\sum_i e^{-y_i\,(F(\mathbf{x}_i) + \alpha h(\mathbf{x}_i))}", font_size=34,
                  colors=colors),
            cmath(r"L(\alpha)", "=", r"\sum_i w_i\, e^{-\alpha\, y_i h(\mathbf{x}_i)}, \quad w_i = e^{-y_i F(\mathbf{x}_i)}",
                  font_size=34, colors=colors),
            cmath(r"L(\alpha)", r"\;\propto\;", r"(1 - \varepsilon)\, e^{-\alpha} + \varepsilon\, e^{\alpha}", font_size=34,
                  colors=colors),
            cmath(r"\alpha", "=", r"\tfrac12 \log\frac{1 - \varepsilon}{\varepsilon}", font_size=34, colors=colors),
        ]
        whys = [why(r"the exponential loss, \\ one more stump"), why(r"the weights appear!"),
                why(r"right: \ $e^{-\alpha}$; \ wrong: \ $e^{\alpha}$"), why(r"set $dL/d\alpha = 0$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.4, buff=0.42, edge=6.8)
        chk = label(rf"first five rounds: \ the formula against a brute-force search for $\alpha$, \ largest difference "
                    rf"${sci_tex(a['alpha_check'])}$", font_size=22, color=GOOD).to_edge(DOWN, buff=0.9)
        fht = note(r"J.~Friedman, T.~Hastie \& R.~Tibshirani, \textit{Additive Logistic Regression} (2000)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why those weights, and that alpha? Friedman, Hastie and Tibshirani found the answer in 2000. "
            "<bookmark mark='a'/> AdaBoost greedily minimizes the exponential loss: e to the minus the margin. Add one "
            "stump, scaled by alpha. <bookmark mark='b'/> Split the exponential, and the old committee's part is "
            "exactly each page's weight. <bookmark mark='c'/> Pages the stump gets right contribute e to the minus "
            "alpha, pages it gets wrong e to the alpha. <bookmark mark='d'/> Set the derivative to zero, and alpha is "
            "half the log of the odds of being right. <bookmark mark='e'/> Searching for alpha numerically agrees with the "
            "formula to within a few millionths here."
        ) as vo:
            self.play(FadeIn(fht))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=EXPC, scale_factor=1.05))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        a = load("adaboost")
        L, tr, te = (np.asarray(a[k]) for k in ("exp_loss_70", "train_err_70", "test_err_70"))
        n = len(L)
        r = np.arange(1, n + 1)
        lr = np.log10(r)
        floor = -4
        g = plot([0, lr[-1], 1], [floor, 0, 1], x_length=7.4, y_length=4.4, xticks=[0, 1, 2],
                 yticks=[0, -1, -2, -3, -4], xfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)],
                 yfmt=lambda v: {0: "1", -1: "0.1", -2: "0.01", -3: "0.001", -4: r"10^{-4}"}[int(v)],
                 center=[-2.0, -0.4, 0], xlabel=r"rounds \ (all $70$ rates)", ylabel=r"log scale")
        ax = g.ax

        def logc(v, col, sw):
            return curve(ax, lr, np.maximum(np.log10(np.maximum(v, 1e-12)), floor), col, stroke_width=sw)

        cL, cT, cE = logc(L, EXPC, 4), logc(tr, GREY_A, 3), logc(te, HL, 4)
        z0 = int(np.argmax(tr == 0)) + 1 if (tr == 0).any() else None
        key = VGroup(label(r"exponential loss", font_size=22, color=EXPC), label(r"training error", font_size=22, color=GREY_A),
                     label(r"held-out error", font_size=22, color=HL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.move_to([4.0, 1.9, 0]).align_to([2.4, 0, 0], LEFT)
        bound = label(r"training error $\le$ exponential loss, \\ every round: \\ $e^{-m} \ge 1$ when $m \le 0$",
                      font_size=22, color=GREY_A).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        te_z = te[z0 - 1] if z0 else te[-1]
        best = int(np.argmin(te)) + 1
        keeps = z0 is not None and te.min() < te_z - 1e-9
        res = VGroup(label(rf"training error $0$ at round ${z0}$" if z0 else r"training error never $0$", font_size=22,
                           color=GREY_A),
                     label(rf"held-out error then: \ ${100 * te_z:.1f}\%$", font_size=22, color=HL),
                     label(rf"best: \ ${100 * te.min():.1f}\%$, \ round ${best}$", font_size=22, color=HL),
                     label(rf"final: \ ${100 * te[-1]:.1f}\%$, \ round ${n}$", font_size=22, color=HL)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bound, DOWN, buff=0.35).align_to(key, LEFT)
        floor_note = label(r"plot floor: $10^{-4}$ \\ training error $0$ or positive loss \\ below $10^{-4}$ shares this baseline", font_size=20, color=GREY_A)
        floor_note.next_to(res, DOWN, buff=0.28).align_to(key, LEFT)
        if z0 is None:
            say = (f"The training error never reaches zero in these {n} rounds; its final value is "
                   f"{100 * tr[-1]:.1f} percent. The held-out error ends at {100 * te[-1]:.1f} percent, "
                   f"with its lowest observed value {100 * te.min():.1f} percent at round {best}.")
        elif keeps:
            say = (f"The training error hits zero at round {z0}, with held-out error {100 * te_z:.1f} percent. "
                   f"Its lowest observed held-out error is {100 * te.min():.1f} percent at round {best}; the final "
                   f"value after {n} rounds is {100 * te[-1]:.1f} percent. Exponential loss can keep pushing on "
                   "the margins even after every training page is right, a connection Schapire and colleagues "
                   "studied in 1998.")
        else:
            say = (f"The training error hits zero at round {z0}, and the held-out error is {100 * te_z:.1f} percent; "
                   "more rounds don't improve it.")
        with self.voiceover(
            "On all seventy rates, run four hundred rounds. <bookmark mark='a'/> The exponential loss falls steadily. "
            "<bookmark mark='b'/> It's always above the training error, since e to the minus the margin is at least "
            f"one for any mistake. <bookmark mark='c'/> {say}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), FadeIn(floor_note))
            vo.wait_until("a")
            self.play(Create(cL), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cT), FadeIn(bound), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cE), LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def faces(self):
        hist = history_card(2001, r"Paul Viola \& Michael Jones", r"faces found in real time: \ $384 \times 288$ "
                            r"pixels at $15$ frames a second, \ on a $700$ MHz Pentium III", color=HIST, width=6.0)
        hist.to_corner(UL, buff=0.3)
        # a detection window with Haar-like features: light and dark rectangles, a feature = sum(light) - sum(dark)
        win = Square(2.6, stroke_color=GREY_B, stroke_width=2).move_to([-3.6, -1.6, 0])
        f1 = VGroup(Rectangle(width=2.0, height=0.35, stroke_width=0, fill_color=WHITE, fill_opacity=0.55).move_to(win.get_center() + UP * 0.55),
                    Rectangle(width=2.0, height=0.35, stroke_width=0, fill_color=GREY_E, fill_opacity=0.9).move_to(win.get_center() + UP * 0.2))
        f2 = VGroup(Rectangle(width=0.4, height=0.7, stroke_width=0, fill_color=GREY_E, fill_opacity=0.9).move_to(win.get_center() + LEFT * 0.5 + DOWN * 0.3),
                    Rectangle(width=0.4, height=0.7, stroke_width=0, fill_color=WHITE, fill_opacity=0.55).move_to(win.get_center() + DOWN * 0.3),
                    Rectangle(width=0.4, height=0.7, stroke_width=0, fill_color=GREY_E, fill_opacity=0.9).move_to(win.get_center() + RIGHT * 0.5 + DOWN * 0.3))
        fl = label(r"each stump: \ one rectangle feature, \\ light minus dark", font_size=22, color=GREY_A).next_to(win, RIGHT, buff=0.3)
        # the cascade
        stages = VGroup()
        for k, txt in enumerate((r"$2$ features", r"$10$", r"$25$", r"$\cdots$", r"thousands")):
            box = RoundedRectangle(width=1.05, height=0.6, corner_radius=0.1, stroke_color=HL, stroke_width=2)
            stages.add(VGroup(box, label(txt, font_size=20, color=WHITE).move_to(box)))
        for st in stages:
            if st[1].width > 0.95:
                st[1].scale_to_fit_width(0.95)
        stages.arrange(RIGHT, buff=0.28).move_to([2.9, 1.0, 0])
        keep_in_frame(stages)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.05, stroke_width=3,
                                max_tip_length_to_length_ratio=0.3, color=GREY_B) for i in range(len(stages) - 1)])
        rej = VGroup(*[Arrow(st.get_bottom(), st.get_bottom() + DOWN * 0.7, buff=0.05, stroke_width=3, color=BAD,
                             max_tip_length_to_length_ratio=0.3) for st in stages[:3]])
        rl = label(r"not a face: \ stop early", font_size=20, color=BAD).next_to(rej, DOWN, buff=0.1)
        face = label(r"face", font_size=24, color=GOOD).next_to(stages[-1], DOWN, buff=0.3)
        ch = label(r"a cascade of boosted committees", font_size=24, color=HL).next_to(stages, UP, buff=0.25)
        tag = note(r"schematic; \ first stages' sizes from the paper").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Boosting's most famous success came in 2001. Paul Viola and Michael Jones found faces in video in real "
            "time, on an ordinary 700 megahertz PC. <bookmark mark='a'/> Each weak rule was a stump on one rectangle "
            "feature: the brightness of one band minus its neighbour, like the dark eyes under a lighter forehead. "
            "<bookmark mark='b'/> AdaBoost chose the best few among more than a hundred and sixty thousand. "
            "<bookmark mark='c'/> And they chained the committees into a cascade: a tiny one throws out most windows "
            "at once, and only the hard ones reach the big committees. For years afterwards, that's how cameras found faces."
        ) as vo:
            self.play(FadeIn(hist, shift=DOWN * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(win), FadeIn(f1), FadeIn(fl))
            vo.wait_until("b")
            self.play(Transform(f1, f2))
            vo.wait_until("c")
            self.play(FadeIn(ch), LaggedStart(*[FadeIn(s_) for s_ in stages], lag_ratio=0.2), Create(arrows))
            self.play(LaggedStart(*[GrowArrow(r_) for r_ in rej], lag_ratio=0.2), FadeIn(rl), FadeIn(face))
        self.wait(0.3)
        self.clear_scene()
