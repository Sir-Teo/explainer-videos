from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import (CEIL, CI, CLEAN, HACK, JUDGE, LEAK, PART, STRONG, TRUSTED, WEAK, curve, load,
                                   tile_frame)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.problems()
        self.references()
        self.thanks()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,  # noqa: E731
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        m = load("measure")
        r = np.asarray(m["boot_4"])
        h, e = np.histogram(r, bins=24)
        ax = mk([float(e[0]), float(e[-1]), 1], [0, float(h.max()), 1])
        bars = VGroup(*[Rectangle(width=ax.c2p(e[k + 1], 0)[0] - ax.c2p(e[k], 0)[0], height=max(ax.c2p(0, h[k])[1] -
                                                                                          ax.c2p(0, 0)[1], 0.01),
                                  stroke_width=0, fill_color=CI, fill_opacity=0.85)
                        .move_to(ax.c2p((e[k] + e[k + 1]) / 2, h[k] / 2)) for k in range(len(h))])
        out.append((VGroup(ax, bars), r"the bootstrap", CI))
        bd, bu = np.asarray(m["boot_diff"]), np.asarray(m["boot_diff_unpaired"])
        lo, hi = float(bu.min()), float(bu.max())
        bins = np.linspace(lo, hi, 30)
        hp, hu = np.histogram(bd, bins)[0], np.histogram(bu, bins)[0]
        ax = mk([lo, hi, 1], [0, float(max(hp.max(), hu.max())), 1])
        ctr = (bins[:-1] + bins[1:]) / 2
        out.append((VGroup(ax, curve(ax, ctr, hu, GREY_B, 3), curve(ax, ctr, hp, CI, 3),
                           DashedLine(ax.c2p(0, 0), ax.c2p(0, float(hp.max())), color=WHITE, dash_length=0.05)),
                    r"pair the comparison", CI))
        c = load("contamination")
        cl, lk = np.asarray(c["clean"]), np.asarray(c["leaked"])
        ax = mk([0, len(cl), 1], [0, float(cl.max()) * 1.1, 1])
        g = VGroup(ax)
        for k, (a, b) in enumerate(zip(cl, lk)):
            for v, col, dx in ((a, CLEAN, 0.3), (b, LEAK, 0.7)):
                p0, p1 = ax.c2p(k + dx - 0.18, 0), ax.c2p(k + dx + 0.18, v)
                g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                                fill_opacity=0.9).move_to((p0 + p1) / 2))
        out.append((g, r"contamination", LEAK))
        a = load("arena")
        cps, w = np.log10(np.asarray(a["checkpoints"], float)), np.log10(np.asarray(a["width"]))
        ax = mk([float(cps[0]), float(cps[-1]), 1], [float(w.min()) - 0.1, float(w.max()) + 0.1, 1])
        out.append((VGroup(ax, curve(ax, cps, w, JUDGE, 3), *[Dot(ax.c2p(x, y), radius=0.04, color=JUDGE)
                                                              for x, y in zip(cps, w)]), r"arena intervals shrink", JUDGE))
        f = load("forecast")
        rows = [r_ for r_ in f["rows"] if r_["sota"]]
        t = np.array([r_["t"] for r_ in rows])
        y = np.log2([r_["p50"] for r_ in rows])
        ax = mk([float(t.min()) - 0.2, float(t.max()) + 0.2, 1], [float(y.min()) - 0.5, float(y.max()) + 0.5, 1])
        cb = np.asarray(f["coef_back"])
        out.append((VGroup(ax, *[Dot(ax.c2p(a_, b_), radius=0.035, color=C.MODEL_Q) for a_, b_ in zip(t, y)],
                           DashedLine(ax.c2p(0, cb[0]), ax.c2p(float(t.max()), cb[0] + cb[1] * float(t.max())),
                                      color=C.CONTEXT, dash_length=0.06)), r"a forecast, backtested", C.CONTEXT))
        hk = load("hacking")
        eps = np.asarray(hk["eval_eps"])
        ret, fin = np.asarray(hk["proxy_ret"]).mean(0), np.asarray(hk["proxy_fin"]).mean(0)
        ax = mk([0, float(eps[-1]), 1], [0, 1, 1])
        out.append((VGroup(ax, curve(ax, eps, ret / max(ret.max(), 1e-9), HACK, 3), curve(ax, eps, fin, C.REWARD, 3)),
                    r"reward hacking", HACK))
        wd = load("w2s")
        vals = [float(np.mean(wd[k])) for k in ("weak", "w2s", "w2s_conf", "ceiling")]
        ax = mk([0, 4, 1], [0, max(vals) * 1.1, 1])
        g = VGroup(ax)
        for k, (v, col) in enumerate(zip(vals, (WEAK, STRONG, CI, CEIL))):
            p0, p1 = ax.c2p(k + 0.2, 0), ax.c2p(k + 0.8, v)
            g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                            fill_opacity=0.9).move_to((p0 + p1) / 2))
        out.append((g, r"weak-to-strong", STRONG))
        ctl = load("control")
        pts = [(r_["usefulness"], r_["safety"]) for r_ in ctl["rows"]]
        ax = mk([0, 1, 1], [0, 1, 1])
        out.append((VGroup(ax, curve(ax, [p[0] for p in pts], [p[1] for p in pts], TRUSTED, 3)), r"control", TRUSTED))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        wd = load("w2s")
        weak, w2s, ceil = (float(np.mean(wd[k])) for k in ("weak", "w2s", "ceiling"))
        pgr = (w2s - weak) / max(ceil - weak, 1e-9)
        if pgr > 0.2:
            w2s_said = ("A weak supervisor can teach a stronger student more than it knows, but not all the student "
                        "could learn, and some of its mistakes besides.")
        else:
            w2s_said = ("A weak supervisor taught our stronger student little beyond its own mistakes, though at "
                        "larger scale it has recovered about half the gap.")
        with self.voiceover(
            "Let's take stock, one last time. A single score is a sample: bootstrap it, and compare models on the "
            "same items. A score means nothing if the test leaked, and contamination reorders the leaderboard. "
            "Votes become ratings through Bradley and Terry, and their intervals shrink only as fast as the square "
            "root of the votes. Trends forecast, until they bend, so backtest them. An optimizer finds the loophole in "
            "whatever we write down. " + w2s_said + " And control buys safety from a model we can't trust, at a price "
            "in usefulness we can measure."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Two models' per-item scores have equal variance $\sigma^2$ and correlation $\rho$. \ Show that the paired "
            r"standard error of the difference is $\sqrt{2(1-\rho)}$ times one model's. \ What is the factor at "
            r"$\rho = 0.94$?",
            r"Show that at the Bradley--Terry maximum-likelihood estimate, \ each model's expected number of wins, "
            r"$\sum_j n_{ij}\,\sigma(\theta_i - \theta_j)$, \ equals its actual number of wins.",
            r"For the item $P(y = 1 \mid \theta) = \sigma(a(\theta - b))$, \ derive the Fisher information $a^2 p(1-p)$, "
            r"\ and show it is largest at $\theta = b$, \ where it equals $a^2/4$.",
            r"With $r' = r + \gamma\Phi(s') - \Phi(s)$ and $\Phi = 0$ at the end of an episode, \ show that every "
            r"policy's return changes by $-\Phi(s_0)$, \ so the optimal policies are the same.",
            r"In the control game, \ derive $P(\text{red wins}) = \frac{w}{c+w}\big(1 - (1-c-w)^N\big)$. \ With "
            r"$q = 0.48$ and $s = 0.3$, \ what is the blue team's safety as $N \to \infty$?",
            r"After clipping every example's gradient to norm $C$, \ by how much can adding or removing one example "
            r"change the sum of gradients? \ Why does that make Gaussian noise of scale $\sigma C$ the right amount?",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from paired comparisons to the clip in DP-SGD. Pause here and work through "
            "them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"B.~Efron \& R.~Tibshirani, \textit{An Introduction to the Bootstrap} (1993)",
             r"C.~Dwork \& A.~Roth, \textit{The Algorithmic Foundations of Differential Privacy} (2014)",
             r"International AI Safety Report (2026), \ chaired by Y.~Bengio"],
            [r"N.~Wiener, \textit{Science} (1960); \ I.~J.~Good (1965); \ Efron (1979); \ Bradley \& Terry (1952); \ "
             r"Lord (1952), \ Rasch (1960)",
             r"Brown et al.\ (2020); \ Srivastava et al.\ (2022); \ Zhang et al.\ (2024); \ Jain et al.\ (2024); \ White "
             r"et al.\ (2024); \ Miller (2024); \ Sclar et al.\ (2023)",
             r"Zheng et al.\ (2023); \ Chiang et al.\ (2024); \ Singh et al.\ (2025); \ Maia Polo et al.\ (2024); \ Ho et "
             r"al.\ (2025)",
             r"Hoffmann et al.\ (2022); \ Kwa et al.\ (2025); \ Becker et al.\ (2025)",
             r"Krakovna et al.\ (2020); \ Ng, Harada \& Russell (1999); \ METR (2025); \ Baker et al.\ (2025); \ "
             r"MacDiarmid et al.\ (2025)",
             r"Irving, Christiano \& Amodei (2018); \ Khan et al.\ (2024); \ Burns et al.\ (2023)",
             r"Hubinger et al.\ (2024); \ Greenblatt et al.\ (2024); \ Meinke et al.\ (2024); \ Schoen et al.\ (2025); \ "
             r"Korbak et al.\ (2025)",
             r"Greenblatt, Shlegeris, Sachan \& Roger (2023); \ Bhatt et al.\ (2025); \ Sharma et al.\ (2025); \ Nasr, "
             r"Carlini et al.\ (2025)",
             r"Carlini et al.\ (2021, 2023); \ Nasr et al.\ (2023); \ Shokri et al.\ (2017); \ Abadi et al.\ (2016); \ "
             r"Mironov et al.\ (2019)"])
        with self.voiceover(
            "For going further: Efron and Tibshirani on the bootstrap, Dwork and Roth on differential privacy, and "
            "the International AI Safety Report for the state of the field, updated every year."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thanks(self):
        smap = series_map(current=None, done=PART).scale(0.85).move_to(DOWN * 0.1)
        title = label(r"AI, Built", font_size=48).to_edge(UP, buff=0.3)
        data = note(r"Every number in this series was computed on the computer that made it, \ or taken from a cited "
                    r"source; \ illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.55)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "That is the end of AI, Built: thirty-one parts, from a guessing game to the question of trust. Every "
            "model of our own in it was trained on the computer that made it. Thank you for building it with me."
        ):
            self.play(FadeIn(title), FadeIn(smap), FadeIn(data), FadeIn(credit), run_time=2.0)
        self.wait(3.0)
        self.play(FadeOut(Group(*self.mobjects)))
