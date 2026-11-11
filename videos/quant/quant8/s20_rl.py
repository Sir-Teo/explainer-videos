from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import predict, ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


def heat(P, lo=0.0, hi=2.4, size=0.13):
    """A policy map over (time across, log wealth up)."""
    P = np.asarray(P)
    cells = VGroup()
    ny, nx = P.shape
    for i in range(ny):
        for j in range(nx):
            val = float(np.clip((P[i, j] - lo) / (hi - lo), 0, 1))
            cells.add(Square(size, stroke_width=0, fill_opacity=0.95,
                             fill_color=interpolate_color(ManimColor(UNDER), ManimColor(KELLY), val)).move_to(
                [j * size, i * size, 0]))
    return cells


class RL(VoiceoverScene):
    def construct(self):
        p = load("ppo")
        ps = load("ppo_seeds")
        pc = load("ppo_costs")
        self.card()
        self.derive()
        self.lab(p, ps)
        self.replay(p, ps)
        self.costs(pc)

    def card(self):
        c = chapter_card(16, r"Reinforcement learning on Merton's problem", r"Can a learner that never sees the "
                         r"formula find it?", part=PART)
        with self.voiceover("Chapter sixteen. Reinforcement learning on Merton's problem."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"s_n = (t_n, \log W_n)", r",\ ", r"a_n = \pi_n,\quad r_n = \log\max\{10^{-6},\,1 + r\Delta + "
                      r"\pi_n(R_n - r\Delta)\}", font_size=30),
                cmath(r"\nabla_\vartheta J", r"=", r"\mathbb{E}_\pi\big[\sum_n\nabla_\vartheta \log p_\vartheta(a_n \mid s_n)\,"
                      r"A_n^\pi\big]", font_size=32),
                cmath(r"\hat A_n", r"=", r"r_n + V(s_{n+1}) - V(s_n)", font_size=32, colors={r"\hat A_n": ALT}),
                cmath(r"L^{\mathrm{clip}}", r"=", r"\mathbb{E}\,\min\big(\rho\,\hat A,\ \mathrm{clip}(\rho, 1 \pm "
                      r"\epsilon)\,\hat A\big),\quad \rho = \frac{p_\vartheta(a \mid s)}{p_{\mathrm{old}}(a \mid s)}",
                      font_size=30, colors={r"L^{\mathrm{clip}}": KELLY})]
        whys = [why(r"Merton as a Markov decision process: the state, the action (a fraction), the reward (log growth: "
                    r"$\gamma = 1$)", font_size=21),
                why(r"finite-horizon policy gradient under differentiation/integrability conditions: sum action scores times true advantages",
                    font_size=21),
                why(r"one-step TD advantage: lower-horizon noise, but a learned critic can introduce bias", font_size=21),
                why(r"PPO (Schulman et al.\ 2017): clips a surrogate objective; no hard bound on updates, ratios or KL divergence", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.4, buff=0.75, edge=6.9)
        with self.voiceover(
            """The learner receives the simulated market and reward, without Merton's analytic optimum. State: time and log wealth. Action: a fraction. Reward: log gross wealth, floored at one millionth before taking the log. <bookmark mark='a'/> With suitable differentiation and integrability, the true finite-horizon policy gradient sums action scores times true advantages across the episode. <bookmark mark='b'/> We estimate advantage using a one-step TD error from a learned critic; this estimate can be biased. <bookmark mark='c'/> PPO clips its surrogate objective. It does not enforce a hard bound on each policy update or KL divergence."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, p, ps):
        card = lab_card(r"PPO's core", [
            "for n in range(steps):                     # roll out a batch",
            "    a = Normal(pol(s), explore).sample()   # a fraction",
            "    gross = 1 + r*dt + a*(R - r*dt)        # the market moves",
            "    rew = log(max(gross, 1e-6)); lw += rew",
            "delta = Rw + v_next - v                    # one-step TD advantage",
            "adv = (delta - delta.mean()) / delta.std()",
            "for _ in range(epochs):",
            "    ratio = exp(Normal(pol(st), explore).log_prob(at) - lp_old)",
            "    l_pol = -mean(minimum(ratio*adv, clamp(ratio, 1-clip, 1+clip)*adv))",
            "    l_val = mean((val(st) - ret)**2) * 100",
            "    (l_pol + l_val).backward(); opt.step()",
        ], source="explainer/quant/house/control.py: ppo_merton", width=9.0, font_size=17).to_edge(UP, buff=0.3)
        fin = ps["finals"]
        outs = [f"seed {i}: mean fraction {100 * f:.0f}%   continuous-growth proxy gap {100 * sh:.3f}%/yr"
                for i, (f, sh) in enumerate(zip(fin, ps["shortfall"]))]
        outs.append(f"finite-quadrature benchmark: {100 * ps['discrete']:.0f}%   closed form (continuous): "
                    f"{100 * ps['merton']:.0f}%")
        with self.voiceover(
            f"""Lab five: a thousand and twenty-four ten-year episodes per iteration, three hundred iterations. Actions are unbounded Gaussian fractions; gross wealth is floored at one millionth. That is a numerical simulator, not an admissibility theorem for leveraged GBM. <bookmark mark='a'/> Five seeds finish with mean fractions from {100 * min(fin):.0f} to {100 * max(fin):.0f} percent. The finite-quadrature benchmark is {100 * ps['discrete']:.0f} percent. The displayed gap, at most {100 * max(ps['shortfall']):.2f} percent a year, compares continuous-growth formulas at mean fractions. It does not measure the full learned policy's quarterly performance."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, p, ps):
        runs = np.asarray(ps["runs"])
        steps = np.arange(runs.shape[1])
        ck = list(ps["checkpoints"])
        snaps = p["snapshots"]
        keys = list(snaps.keys())

        def frame(i):
            P = np.asarray(snaps[keys[i]])
            cells = heat(P)
            return VGroup(cells,
                          label(r"time $\to$", font_size=16, color=GREY_B).next_to(cells, DOWN, buff=0.1),
                          label(r"log wealth $\to$", font_size=16, color=GREY_B).rotate(PI / 2).next_to(cells, LEFT,
                                                                                                       buff=0.1),
                          MathTex(rf"\text{{mean }}{100 * P.mean():.0f}\%,\ \text{{range }}{100 * P.min():.0f}"
                                  rf"\text{{--}}{100 * P.max():.0f}\%", font_size=24, color=ALT).next_to(cells, UP,
                                                                                                        buff=0.15))

        rp = TrainingReplay(steps, runs, frame, ck, ylabel=r"average fraction in stocks (5 seeds)",
                            xlabel=r"PPO iteration", color=ALT)
        tgt = DashedLine(rp.ax.c2p(0, ps["discrete"]), rp.ax.c2p(steps[-1], ps["discrete"]), color=KELLY,
                         stroke_width=2.5)
        tl = MathTex(rf"\text{{quadrature reference }}{100 * ps['discrete']:.0f}\%", font_size=24, color=KELLY).next_to(
            tgt, UP, buff=0.08).set_y(2.9).align_to(tgt, RIGHT)
        src = illustration(r"300 iterations $\times$ 1{,}024 ten-year quarterly episodes, 5 seeds, one CPU thread each")
        with self.voiceover(
            "Here is the training, scrubbed checkpoint by checkpoint. On the right, the average fraction the policy chooses, "
            "for five seeds, the band showing their spread, against the finite-quadrature reference. On the left, the policy itself, over time "
            "and wealth, at the same checkpoint. <bookmark mark='a'/> It starts near fifty percent. It climbs, "
            "overshoots on some seeds, and wanders around the reference, in this fixed training protocol. The map flattens: by the end the fraction barely depends on "
            "time or wealth, which is what Merton's theorem says, though the learner never heard of it."
        ) as vo:
            self.play(FadeIn(rp), Create(tgt), FadeIn(tl), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(6.0) - 0.5, 6.0))
        self.wait(0.4)
        self.clear_scene()

    def costs(self, pc):
        gp = np.asarray(pc["grid_p"])
        fin = np.asarray(pc["finals"])
        lo, hi = pc["lo"], pc["hi"]
        g = axes([0.5, 3.0], [0.5, 3.0], x_length=4.8, y_length=4.8, xlabel=r"fraction held before trading",
                 ylabel=r"fraction after trading", xticks=[1, 2, 3], yticks=[1, 2, 3],
                 xfmt=lambda u: f"{100 * u:.0f}\\%", yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        diag = DashedLine(ax.c2p(0.5, 0.5), ax.c2p(3, 3), color=GREY_C, stroke_width=1.5)
        dp = VGroup(Line(ax.c2p(0.5, lo), ax.c2p(lo, lo), color=VALUE, stroke_width=4),
                    Line(ax.c2p(lo, lo), ax.c2p(hi, hi), color=VALUE, stroke_width=4),
                    Line(ax.c2p(hi, hi), ax.c2p(3.0, hi), color=VALUE, stroke_width=4))
        band = Polygon(ax.c2p(lo, 0.5), ax.c2p(hi, 0.5), ax.c2p(hi, 3.0), ax.c2p(lo, 3.0), stroke_width=0,
                       fill_color=VALUE, fill_opacity=0.12)
        learned = VGroup(*[curve(ax, gp, f_, ALT, stroke_width=2.5).set_stroke(opacity=0.8)
                           for f_ in fin])
        leg = legend([(VALUE, r"dynamic programming: the band"), (ALT, r"PPO, 5 seeds (mid-horizon)"),
                      (GREY_C, r"do nothing")], font_size=17).next_to(g, UP, buff=0.18).align_to(g, LEFT)
        pg, pt = np.asarray(pc["ppo_growth"]), np.asarray(pc["ppo_turnover"])
        head = VGroup(*[label(t_, font_size=19, color=GREY_B) for t_ in (r"rule", r"net growth", r"turnover")])
        rows_ = [(r"band (DP)", pc["band"], VALUE), (r"rebalance to Merton", pc["merton"], KELLY),
                 (r"never trade", pc["hold"], GREY_B)]
        cells = [head] + [VGroup(label(n_, font_size=20, color=c_), MathTex(f"{100 * d_['growth']:.2f}\\%", font_size=24),
                                 MathTex(f"{100 * d_['turnover']:.0f}\\%", font_size=24)) for n_, d_, c_ in rows_]
        cells.append(VGroup(label(r"PPO (5 seeds)", font_size=20, color=ALT),
                            MathTex(rf"{100 * pg.min():.2f}\text{{--}}{100 * pg.max():.2f}\%", font_size=24),
                            MathTex(rf"{100 * pt.min():.0f}\text{{--}}{100 * pt.max():.0f}\%", font_size=24)))
        tab = VGroup(*[x for r_ in cells for x in r_]).arrange_in_grid(rows=len(cells), cols=3, buff=(0.45, 0.18),
                                                                    col_alignments="lrr")
        tab.to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        se = pc["band"]["se"]
        q = predict(r"With a 1\% cost on every trade, will the agent learn to do nothing inside a band?", width=3.6,
                       font_size=19).next_to(tab, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)  # wider than the table
        edges = [e for e in pc["edges"] if e[0] is not None]
        close = len(edges) >= 3 and all(abs(e[0] - lo) < 0.15 and abs(e[1] - hi) < 0.15 for e in edges)
        beats = bool(np.median(pg) > pc["merton"]["growth"])
        src = illustration(r"log utility, 1\% cost, quarterly; target clipped to $[0,4]$, gross/cost factors floored at $10^{-6}$; paired 200{,}000-market evaluation")
        with self.voiceover(
            "Now add trading costs: a one percent cost on every trade. The dynamic program says: a band from "
            f"{100 * lo:.0f} to {100 * hi:.0f} percent, do nothing inside, trade to the edge outside. Pause and predict: "
            "will the learner find it? <bookmark mark='a'/> Five learned policies, against the band."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(band), Create(dp), FadeIn(leg), FadeIn(src), FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in learned], lag_ratio=0.2, run_time=2.5))
        with self.voiceover(
            "They do: each seed leaves the position alone over a range close to the band, and its net growth, "
            f"{100 * np.median(pg):.2f} percent a year at the median, beats rebalancing to Merton, "
            f"{100 * pc['merton']['growth']:.2f}. Next: who sizes bets for a living."
            if close and beats else
            "Not quite: the learners trade part of the way toward the middle, leaving only a narrow strip alone, not the "
            f"band. Their net growth is {100 * np.median(pg):.2f} percent a year at the median, against "
            f"{100 * pc['merton']['growth']:.2f} for rebalancing to Merton every quarter and "
            f"{100 * pc['band']['growth']:.2f} for the band. The band's edge over the learners is "
            f"{100 * (pc['band']['growth'] - np.median(pg)):.2f} percent a year, and each episode is a decade of an "
            "eighteen percent market: these five seeds and this training budget did not recover the dynamic-programming policy. Next: who sizes bets for a living."
        ) as vo:
            self.play(FadeOut(q), LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in cells], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()
