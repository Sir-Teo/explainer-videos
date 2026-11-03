from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data, sci


class Hawkes(VoiceoverScene):
    def construct(self):
        h = load("hawkes")
        hc = load("hawkes_check")
        hr = load("hawkes_replay")
        rs = load("hawkes_rescale")
        self.card()
        self.thinning(hc)
        self.branching(hc)
        self.replay(h, hr)
        self.rescale(h, rs)

    def card(self):
        c = chapter_card(14, r"Hawkes: jumps that cause jumps", r"Do large moves arrive at random, or in families?",
                         part=PART)
        with self.voiceover("Chapter fourteen. Hawkes processes: jumps that cause jumps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def thinning(self, hc):
        tr = hc["trace"]
        tt, bd, lam, acc = (np.asarray(tr[k]) for k in ("t", "bound", "lam", "accepted"))
        card = lab_card(r"Ogata's thinning", [
            "def hawkes_thinning(mu, alpha, beta, T, seed=0):",
            "    rng = np.random.default_rng(seed)",
            "    t, events, excite = 0.0, [], 0.0",
            "    while True:",
            "        lam_bar = mu + excite              # a bound: the intensity only decays",
            "        w = rng.exponential(1 / lam_bar); t_new = t + w",
            "        if t_new > T: break",
            "        excite *= np.exp(-beta * w); t = t_new",
            "        if rng.random() <= (mu + excite) / lam_bar:",
            "            events.append(t); excite += alpha",
            "    return np.array(events)",
        ], source="explainer/quant/house/sim.py", width=7.4, font_size=15).to_corner(UL, buff=0.25)
        T = 40.0
        g = axes([0, T], [0, max(bd.max(), 1) * 1.1], x_length=6.4, y_length=2.3, xlabel=r"time (days)",
                 ylabel=r"intensity $\lambda_t$", xticks=[0, 20, 40], yticks=[0, 1, 2], font_size=15)
        g.to_corner(DR, buff=0.35)
        ax = g.ax
        ev = tt[acc]
        grid = np.linspace(0, T, 800)
        inten = 0.2 + np.array([np.sum(1.4 * np.exp(-2.0 * (x - ev[ev < x]))) for x in grid])
        line = curve(ax, grid, np.minimum(inten, ax.y_range[1]), JUMP, stroke_width=2.5)
        cands = VGroup(*[VGroup(DashedLine(ax.c2p(a, 0), ax.c2p(a, b), stroke_width=1.2, color=GREY_D),
                                Dot(ax.c2p(a, b * np.random.default_rng(i).uniform(0.05, 1) if not ok else l_),
                                    radius=0.05, color=YELLOW if ok else GREY_B))
                         for i, (a, b, l_, ok) in enumerate(zip(tt, bd, lam, acc))])
        eq = MathTex(r"\lambda_t = \mu + \sum_{t_i < t} \alpha\,e^{-\beta(t - t_i)}", font_size=30, color=JUMP)
        eq.next_to(g, UP, buff=0.35)
        outs = [f"hawkes_thinning(0.2, 1.4, 2.0, T=2000), 50 runs",
                f"mean count {hc['mean_count']:.0f} +/- {hc['sd_count']:.0f}   theory mu T/(1 - alpha/beta) = {hc['theory']:.0f}"]
        with self.voiceover(
            "Large moves cluster: one makes another more likely soon after. Alan Hawkes wrote down a process with "
            "that property in 1971: its intensity jumps by alpha after every event and decays back toward a base rate "
            "mu at speed beta. <bookmark mark='a'/> Yosihiko Ogata's thinning, from 1981, simulates it in a dozen "
            "lines. Between events the intensity only decays, so its current value is an upper bound: draw a "
            "candidate from a Poisson clock at that bound. <bookmark mark='b'/> Accept it with probability true "
            "intensity over bound. The yellow dots are accepted and kick the red curve up; the grey ones fall "
            "through. <bookmark mark='c'/> Fifty runs over two thousand days give a mean count of "
            f"{hc['mean_count']:.0f}, against the theory's {hc['theory']:.0f}."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cands], lag_ratio=0.08), Create(line), run_time=5)
            vo.wait_until("c")
            lab_run(self, card, outs, font_size=16)
        self.wait(0.4)
        self.clear_scene()

    def branching(self, hc):
        cl = hc["clusters"]
        t, par = np.asarray(cl["t"]), np.asarray(cl["parent"])
        T = 60.0
        g = axes([0, T], [0, 6.5], x_length=11.6, y_length=2.6, xlabel=r"time", xticks=[0, 30, 60], yticks=[],
                 font_size=15).shift(DOWN * 1.55)
        ax = g.ax
        gen = np.zeros(len(t), int)
        for i in range(len(t)):
            if par[i] >= 0:
                gen[i] = gen[par[i]] + 1
        cols = [DRIFT, ITO, STRAT, JUMP, YELLOW, WHITE, WHITE]
        gstep = 5.6 / max(int(gen.max()), 1)  # every generation fits under the top of the axes, however deep the tree
        dots = VGroup(*[Dot(ax.c2p(a, 0.6 + gstep * gen[i]), radius=0.08, color=cols[min(gen[i], 6)])
                        for i, a in enumerate(t)])
        links = VGroup(*[Line(dots[par[i]].get_center(), dots[i].get_center(), stroke_width=1.6, color=GREY_B)
                         for i in range(len(t)) if par[i] >= 0])
        ticks = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, 0.3), stroke_width=2, color=YELLOW) for a in t])
        rows = [cmath(r"n", r"=", r"\int_0^\infty \alpha e^{-\beta s}\,ds = \alpha / \beta", font_size=30),
                cmath(r"\bar\lambda", r"=", r"\mu + n\bar\lambda \;\Rightarrow\; \bar\lambda = \frac{\mu}{1 - n}", font_size=30,
                      colors={r"\frac{\mu}{1 - n}": JUMP}),
                cmath(r"\mathbb{E}[\text{cluster size}]", r"=", r"1 + n + n^2 + \dots = \frac{1}{1 - n}", font_size=30)]
        whys = [why(r"each event's children: Poisson, with mean the kernel's mass (the branching ratio)", 18),
                why(r"take expectations; stationary only if $n < 1$", 18),
                why(r"generations form a geometric series (Hawkes and Oakes 1974)", 18)]
        step = ladder(self, rows, whys, keep=2, top=3.4, x=-2.2, buff=0.3, edge=6.9)  # two rows clear the tree
        res = label(rf"here $n = 0.7$: {hc['n_clusters']} families, mean size {hc['mean_cluster']:.2f} against "
                    rf"$1/(1 - n) = {hc['cluster_theory']:.2f}$", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The same process can be seen as families. Immigrants arrive at the base rate mu, and every event, "
            "immigrant or not, has children: a Poisson number of them, with mean n equal to alpha over beta, the "
            "total mass of the kernel, called the branching ratio. <bookmark mark='a'/> Redraw the events as a family "
            "tree, generation by generation, each child hanging from its parent. <bookmark mark='b'/> Taking "
            "expectations, the long-run rate satisfies lambda bar equals mu plus n times lambda bar, so it is mu over "
            "one minus n, which exists only if n is below one: above it, the families never die out. A family's mean "
            "size is one plus n plus n squared and so on, one over one minus n, and here the simulated families "
            f"average {hc['mean_cluster']:.2f}, against {hc['cluster_theory']:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.4) for d in dots], lag_ratio=0.05), run_time=2)
            self.play(Create(links), run_time=1.5)
            vo.wait_until("b")
            step(0)
            step(1)
            step(2)
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, h, hr):
        curves = np.asarray(hr["curves"])
        steps = np.arange(curves.shape[1])
        grid = np.asarray(hr["grid"])
        ev = np.asarray(hr["events"])
        T = hr["T"]

        def frame(i):
            a = axes([0, T], [0, 3.4], x_length=5.4, y_length=3.0, xlabel=r"days since 1 January 2018",
                     ylabel=r"fitted intensity, a day", xticks=[0, 500, 1000], yticks=[0, 1, 2, 3], font_size=14)
            p = hr["ck_params"][min(i, len(hr["ck"]) - 1)]
            lam = np.minimum(np.asarray(hr["lams"][min(i, len(hr["ck"]) - 1)]), 3.4)
            tks = VGroup(*[Line(a.ax.c2p(e, 0), a.ax.c2p(e, 0.2), stroke_width=1, color=BM) for e in ev])
            txt = MathTex(rf"\mu = {p[0]:.3f},\ \alpha = {p[1]:.2f},\ \beta = {p[2]:.2f},\ n = {p[1] / p[2]:.2f}",
                          font_size=22, color=JUMP).next_to(a, UP, buff=0.1)
            return VGroup(a, tks, curve(a.ax, grid, lam, JUMP, stroke_width=1.8), txt)
        lo = float(np.percentile(curves, 3))
        rp = TrainingReplay(steps, np.clip(curves, lo, None), frame, checkpoints=list(hr["ck"]),
                            ylabel=r"log-likelihood", xlabel=r"Nelder--Mead iteration", color=JUMP)
        base = DashedLine(rp.ax.c2p(steps[0], max(hr["ll_poisson"], rp.lo)), rp.ax.c2p(steps[-1], max(hr["ll_poisson"], rp.lo)),
                          color=GREY_B, stroke_width=2)
        bl = label(rf"Poisson clock: {hr['ll_poisson']:.0f}", font_size=17, color=GREY_B).next_to(base, UP, buff=0.08)
        bl.align_to(base, RIGHT)
        f = h["fit"]
        res = VGroup(MathTex(rf"n = \alpha/\beta = {f['branching']:.2f}, \quad \text{{half-life }} {h['half_life_hours']:.1f}"
                             r"\text{ hours}", font_size=28, color=JUMP),
                     label(rf"eight random starts end within ${sci(hr['spread'], 0)}$ of each other", font_size=19,
                           color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.25)
        src = real_data(r"events: Bitcoin hours with $|r| > 4\times$ the past month's volatility, 2018--2020", corner=UL)
        with self.voiceover(
            f"Now fit it to the {f['n']} hours since 2018 when Bitcoin moved more than four times its recent "
            "volatility. The log-likelihood is the sum of log intensities at the events minus the integrated "
            "intensity, computed in one pass by Ozaki's recursion. <bookmark mark='a'/> The House maximizes it from "
            "eight random starts: the log-likelihood climbs on the right, the Poisson clock's value dashed, and the "
            "fitted intensity takes shape on the left. <bookmark mark='b'/> All eight starts agree. The branching "
            f"ratio is {f['branching']:.2f}, and the excitement halves in about {h['half_life_hours']:.0f} hours."
        ) as vo:
            self.play(FadeIn(rp), Create(base), FadeIn(bl), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=8)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def rescale(self, h, rs):
        resc = np.asarray(rs["resc"])
        ev = np.asarray(h["events"])
        T = h["T"]
        top = axes([0, T], [0, 1], x_length=6.0, y_length=0.8, xlabel=r"calendar time (days)", xticks=[0, 500, 1000],
                   yticks=[], font_size=14)
        bot = axes([0, resc[-1]], [0, 1], x_length=6.0, y_length=0.8, xlabel=r"compensator time $\Lambda(t)$",
                   xticks=[0, round(resc[-1])], yticks=[], font_size=14)
        VGroup(top, bot).arrange(DOWN, buff=0.9).to_edge(LEFT, buff=0.5).shift(UP * 0.8)
        t1 = VGroup(*[Line(top.ax.c2p(e, 0), top.ax.c2p(e, 1), stroke_width=1.2, color=JUMP) for e in ev])
        t2 = VGroup(*[Line(bot.ax.c2p(e, 0), bot.ax.c2p(e, 1), stroke_width=1.2, color=DRIFT) for e in resc])
        q = np.asarray(rs["qq_x"])
        g = axes([0, 6], [0, 6], x_length=3.6, y_length=3.6, xlabel=r"Exp(1) quantiles", ylabel=r"rescaled gaps",
                 xticks=[0, 3, 6], yticks=[0, 3, 6], font_size=14).to_corner(UR, buff=0.4)
        diag = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(6, 6), color=GREY_B, stroke_width=1.5)
        sel = np.unique(np.linspace(0, len(q) - 1, 80).astype(int))
        qh = VGroup(*[Dot(g.ax.c2p(min(q[i], 6), min(rs["qq_h"][i], 6)), radius=0.035, color=DRIFT) for i in sel])
        qp = VGroup(*[Dot(g.ax.c2p(min(q[i], 6), min(rs["qq_p"][i], 6)), radius=0.035, color=GREY_B) for i in sel])
        side = VGroup(
            label(rf"Kolmogorov--Smirnov: Hawkes $p = {rs['p_hawkes']:.2f}$", font_size=20, color=DRIFT),
            label(rf"Poisson clock $p = {sci(rs['p_poisson'], 0)}$", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        note_ = wrapped_label(r"Hardiman, Bercot and Bouchaud (2013) estimated $n$ near the critical value 1 for E-mini "
                              r"futures mid-price changes, 1998--2011; Filimonov and Sornette (2012) reported a rising "
                              r"$n$; the estimates depend on the kernel and the window. Nearly critical Hawkes processes "
                              r"lead to rough volatility (Jaisson and Rosenbaum 2016): Parts 14 and 36.", 6.4, 18, GREY_A)
        note_.to_corner(DL, buff=0.3)
        n_ = h["fit"]["branching"]
        pc, ans = pause(rf"Branching ratio ${n_:.2f}$. What fraction of large moves were triggered by earlier ones?",
                        rf"{100 * n_:.0f}\%: in a stationary Hawkes process the triggered share equals $n$.", width=4.6,
                        font_size=18)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(side, DOWN, buff=0.25).align_to(g, LEFT)
        keep_in_frame(VGroup(pc, ans), 0.25)
        good = rs["p_hawkes"] > 0.05 and rs["p_poisson"] < 0.01
        verdict = ("The Hawkes gaps lie on the line, p equal to "
                   f"{rs['p_hawkes']:.2f}; the Poisson clock's do not, with a p-value too small to read."
                   if good else f"Here the test is less clear: p equal to {rs['p_hawkes']:.2f} for Hawkes.")
        with self.voiceover(
            "Is the fit any good? Run the clock at the fitted intensity: measure time by the integrated intensity "
            "instead of the calendar. <bookmark mark='a'/> Under a correct model the clustered events slide apart "
            "into an even rain, a unit-rate Poisson process: the point-process cousin of chapter four's "
            "Dambis-Dubins-Schwarz clock. <bookmark mark='b'/> Compare the rescaled gaps with exponential quantiles. "
            f"{verdict} <bookmark mark='c'/> On the record, Hardiman, Bercot and Bouchaud, at Capital Fund Management, "
            "estimated a branching ratio near one for E-mini futures; such nearly critical processes lead to rough "
            "volatility, in Part fourteen. <bookmark mark='d'/> A pause: with branching ratio "
            f"{h['fit']['branching']:.2f}, what fraction of moves were triggered? Exactly that: "
            f"{100 * h['fit']['branching']:.0f} percent."
            " Nearly critical clustering leaves memory in volatility. Next: a process with memory built in."
        ) as vo:
            self.play(FadeIn(top), FadeIn(t1))
            vo.wait_until("a")
            self.play(FadeIn(bot), TransformFromCopy(t1, t2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(g), Create(diag), LaggedStart(*[FadeIn(d) for d in qp], lag_ratio=0.02),
                      LaggedStart(*[FadeIn(d) for d in qh], lag_ratio=0.02), run_time=2.5)
            self.play(FadeIn(side))
            vo.wait_until("c")
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(pc), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
