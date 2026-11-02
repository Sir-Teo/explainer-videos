from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


def _gauss(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (np.sqrt(2 * np.pi) * s)


class Regimes(VoiceoverScene):
    def construct(self):
        r = load("regimes_em")
        old = load("regimes")
        self.card()
        self.jars(r)
        self.derive(r)
        self.mstep(r)
        self.em(r, old)

    def card(self):
        c = chapter_card(4, r"Hidden regimes", r"Is the market calm, or in a storm?", lit=(1989,), part=PART)
        with self.voiceover("Chapter four. Hidden regimes."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def jars(self, r):
        t, x = np.asarray(r["t"]), np.asarray(r["x"])
        pred, filt = np.asarray(r["pred"]), np.asarray(r["filt"])
        mu, sd = np.asarray(r["mu"]), np.asarray(r["sd"])
        p = ValueTracker(float(filt[30]))
        H, W = 3.0, 1.3
        base = DOWN * 1.6 + LEFT * 5.0

        def jar(k, col, name):
            box = Rectangle(width=W, height=H, stroke_color=GREY_B, stroke_width=3).move_to(base + RIGHT * 1.8 * k + UP * H / 2)
            liq = always_redraw(lambda: Rectangle(width=W - 0.08, height=max(H * (p.get_value() if k else 1 - p.get_value()), 0.001),
                                                  stroke_width=0, fill_color=col, fill_opacity=0.75).align_to(box, DOWN).shift(UP * 0.04)
                                .set_x(box.get_x()))
            val = always_redraw(lambda: MathTex(f"{(p.get_value() if k else 1 - p.get_value()):.2f}", font_size=28, color=col)
                                .next_to(box, UP, buff=0.1))
            return VGroup(box, liq, val, label(name, font_size=22, color=col).next_to(box, DOWN, buff=0.15))

        calm, storm = jar(0, GOOD, r"calm"), jar(1, BAD, r"storm")
        xs = np.linspace(-0.3, 0.3, 200)
        gd = axes([-0.3, 0.3], [0, 11], x_length=5.6, y_length=2.6, xticks=[-0.2, 0, 0.2], yticks=[],
                  xfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0", xlabel=r"this month's excess return",
                  font_size=16).to_corner(UR, buff=0.5)
        dc = curve(gd.ax, xs, _gauss(xs, mu[0], sd[0]), GOOD, stroke_width=3)
        ds = curve(gd.ax, xs, _gauss(xs, mu[1], sd[1]), BAD, stroke_width=3)
        gp = axes([1926, 2021], [0, 1], x_length=6.6, y_length=1.8, xticks=[1930, 1960, 1990, 2020],
                  xfmt=lambda u: f"{int(u)}", yticks=[0, 1], ylabel=r"filtered probability of the storm",
                  font_size=14).to_corner(DR, buff=0.45)
        tr = ValueTracker(30)
        fill = always_redraw(lambda: VMobject(stroke_width=0, fill_color=BAD, fill_opacity=0.6).set_points_as_corners(
            [gp.ax.c2p(t[30], 0)] + [gp.ax.c2p(a, b) for a, b in zip(t[30:int(tr.get_value()) + 1], filt[30:int(tr.get_value()) + 1])]
            + [gp.ax.c2p(t[int(tr.get_value())], 0)]))
        month = always_redraw(lambda: label(rf"{int(t[int(tr.get_value())])}, month {int(round((t[int(tr.get_value())] % 1) * 12 + 0.5))}",
                                            font_size=22, color=GREY_A).next_to(VGroup(calm, storm), UP, buff=0.5))
        src = real_data(r"Kenneth French's monthly market excess return, 1926--2020; Hamilton (1989) fitted by EM",
                        corner=DL)
        with self.voiceover(
            "Volatility is hidden; we only see its effects. One way to model it is a few hidden states. In 1989 James "
            "Hamilton let the economy switch between regimes by a Markov chain, each regime with its own mean and "
            "volatility. Picture two jars of belief: calm and storm. <bookmark mark='a'/> Each "
            "month, two things happen. First, predict: a little liquid leaks between the jars, because regimes can "
            "change. <bookmark mark='b'/> Then the month's return lands, and each jar is rescaled by how likely that "
            "return is under its regime, here the two bell curves, and the total is poured back to one litre. "
            "<bookmark mark='c'/> Watch it through 1929. Every big monthly move tips the belief toward the storm, and "
            "it stays there. <bookmark mark='d'/> Run it over the century, and the red area it draws lights up the "
            "Depression, 1974, 1987, 2008 and 2020."
        ) as vo:
            self.play(FadeIn(calm), FadeIn(storm), FadeIn(gd), Create(dc), Create(ds), FadeIn(gp), FadeIn(src))
            self.add(fill, month)
            vo.wait_until("a")
            for i in range(31, 34):
                self.play(p.animate.set_value(float(pred[i])), tr.animate.set_value(i - 0.5), run_time=0.7)
                dot = Dot(gd.ax.c2p(np.clip(x[i], -0.3, 0.3), 0), radius=0.08, color=WHITE)
                hs = VGroup(DashedLine(gd.ax.c2p(x[i], 0), gd.ax.c2p(x[i], _gauss(x[i], mu[0], sd[0])), color=GOOD),
                            DashedLine(gd.ax.c2p(x[i], 0), gd.ax.c2p(x[i], _gauss(x[i], mu[1], sd[1])), color=BAD))
                self.play(FadeIn(dot, shift=DOWN * 0.3), Create(hs), run_time=0.5)
                self.play(p.animate.set_value(float(filt[i])), tr.animate.set_value(i), run_time=0.7)
                self.play(FadeOut(dot), FadeOut(hs), run_time=0.3)
            vo.wait_until("b")
            for i in range(34, 40):
                self.play(p.animate.set_value(float(pred[i])), tr.animate.set_value(i - 0.5), run_time=0.35)
                self.play(p.animate.set_value(float(filt[i])), tr.animate.set_value(i), run_time=0.35)
            vo.wait_until("c")
            for i in range(40, 60, 2):
                self.play(p.animate.set_value(float(filt[i])), tr.animate.set_value(i), run_time=0.25)
            vo.wait_until("d")
            p.add_updater(lambda m: m.set_value(float(filt[int(tr.get_value())])))
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(1.0) - 0.4, 3), rate_func=linear)
            p.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self, r):
        rows = [
            cmath(r"\xi_{t|t}", r"=", r"\frac{\xi_{t|t-1}\odot\eta_t}{\mathbf{1}'(\xi_{t|t-1}\odot\eta_t)}", font_size=38),
            cmath(r"\xi_{t+1|t}", r"=", r"P'\,\xi_{t|t}", font_size=38),
            cmath(r"\Pr(D = d)", r"=", r"p_{ii}^{\,d-1}(1 - p_{ii})\ \Rightarrow\ \mathbb{E}D = \frac{1}{1 - p_{ii}}", font_size=38),
            cmath(r"\pi_{storm}", r"=", r"\frac{1 - p_{11}}{2 - p_{11} - p_{22}}", font_size=38),
        ]
        whys = [why(r"Bayes: multiply the prior by each regime's density $\eta_{t,j}$ of $r_t$, renormalise"),
                why(r"the Markov prediction: the leak between the jars"),
                why(r"stay $d-1$ months, then leave: a geometric duration"),
                why(r"the long-run share: inflow to the storm equals outflow")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.4, buff=0.5, edge=6.9)
        P = np.asarray(r["P"])
        ex = VGroup(MathTex(rf"p_{{11}} = {P[0, 0]:.3f},\ p_{{22}} = {P[1, 1]:.3f}", font_size=30, color=GREY_A),
                    MathTex(rf"\mathbb{{E}}D_{{calm}} = {1 / (1 - P[0, 0]):.0f}\text{{ months}},\ \ \mathbb{{E}}D_{{storm}} = "
                            rf"{1 / (1 - P[1, 1]):.0f}\text{{ months}},\ \ \pi_{{storm}} = {r['pi_storm']:.2f}",
                            font_size=30, color=VOL)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In symbols. The update is Bayes' rule: multiply the predicted probabilities by each regime's density of "
            "the return, and renormalise. <bookmark mark='a'/> The prediction multiplies by the transition matrix. "
            "<bookmark mark='b'/> A regime that persists with probability p each month lasts a geometric number of "
            "months, with mean one over one minus p. <bookmark mark='c'/> And the long-run share of time in the storm "
            "balances the flows in and out. <bookmark mark='d'/> With the fitted probabilities, a calm spell lasts "
            f"about {1 / (1 - P[0, 0]):.0f} months on average, a storm about {1 / (1 - P[1, 1]):.0f}, and the market "
            f"spends about {100 * r['pi_storm']:.0f} percent of its time in the storm."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    def em(self, r, old):
        path = r["path"]
        its = np.array([p_["it"] for p_ in path], float)
        ll = np.array([p_["loglik"] for p_ in path], float)
        xs = np.linspace(-0.3, 0.3, 160)

        def frame(i):
            k = [0, 1, 2, 3, len(path) - 1][min(i, 4)]
            m, s = path[k]["mu"], path[k]["sd"]
            g = axes([-0.3, 0.3], [0, 11], x_length=4.8, y_length=2.8, xticks=[-0.2, 0, 0.2], yticks=[],
                     xfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0", font_size=15,
                     ylabel=rf"the two regimes after {path[k]['it']} EM iteration" + ("" if path[k]['it'] == 1 else "s"))
            return VGroup(g, curve(g.ax, xs, _gauss(xs, m[0], s[0]), GOOD, stroke_width=3),
                          curve(g.ax, xs, _gauss(xs, m[1], s[1]), BAD, stroke_width=3))

        rp = TrainingReplay(its, ll, frame, checkpoints=[1, 2, 3, 5, 300], ylabel=r"log-likelihood",
                            xlabel=r"EM iteration", color=VOL)
        rp.to_edge(UP, buff=0.5)
        mu, sd, dur = np.asarray(old["mu"]), np.asarray(old["sd"]), np.asarray(old["duration_months"])
        rows = VGroup(
            MathTex(rf"\text{{calm: mean }} {100 * mu[0]:+.0f}\%, \text{{ vol }} {100 * sd[0]:.0f}\%, \text{{ lasts }} "
                    rf"{dur[0]:.0f} \text{{ months}}", font_size=28, color=GOOD),
            MathTex(rf"\text{{storm: mean }} {100 * mu[1]:+.0f}\%, \text{{ vol }} {100 * sd[1]:.0f}\%, \text{{ lasts }} "
                    rf"{dur[1]:.0f} \text{{ months}}", font_size=28, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=1.6).to_edge(LEFT, buff=0.6)
        pc = pause_card(r"A $-8\%$ month arrives in the calm regime. Does the storm jar fill completely?", width=5.6,
                        font_size=21).to_corner(DR, buff=0.3)
        ans = MathTex(rf"{r['prior_storm']:.2f} \;\to\; {r['post_storm_m8']:.2f}", font_size=34, color=BAD)
        ans.next_to(pc, LEFT, buff=0.4)
        answer = ("Yes: one month is enough." if r["post_storm_m8"] > 0.5 else
                  f"No. It rises from {100 * r['prior_storm']:.0f} to {100 * r['post_storm_m8']:.0f} percent: one bad "
                  "month is not yet a storm: the evidence has to accumulate.")
        with self.voiceover(
            f"How are the regimes found? By expectation-maximisation: guess the two regimes, run the filter and a smoother "
            f"to get each month's probabilities, re-estimate each regime's mean and volatility from the months weighted "
            f"by those probabilities, and repeat. Each round can only raise the likelihood. <bookmark mark='a'/> On ninety-four "
            f"years of monthly returns it converges within a handful of iterations: a calm regime with a mean of {100 * mu[0]:+.0f} "
            f"percent a year and {100 * sd[0]:.0f} percent volatility, and a storm with a mean of {100 * mu[1]:.0f} percent "
            f"and {100 * sd[1]:.0f} percent volatility. <bookmark mark='b'/> Pause and predict. A month of minus eight "
            f"percent arrives while the model is sure it is calm. Does the storm jar fill? <bookmark mark='c'/> {answer}"
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=4)
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(FadeIn(pc))
            vo.wait_until("c")
            self.play(Write(ans))
        self.wait(0.3)
        self.clear_scene()

    def mstep(self, r):
        rows = [
            cmath(r"\xi_{t|T}", r"=", r"\xi_{t|t}\odot\Big[P\big(\xi_{t+1|T}\oslash\xi_{t+1|t}\big)\Big]", font_size=34),
            cmath(r"\hat\mu_j", r"=", r"\frac{\sum_t\xi_{t|T,j}\,r_t}{\sum_t\xi_{t|T,j}},\quad "
                  r"\hat\sigma_j^2 = \frac{\sum_t\xi_{t|T,j}(r_t - \hat\mu_j)^2}{\sum_t\xi_{t|T,j}}", font_size=34),
            cmath(r"\hat p_{ij}", r"=", r"\frac{\sum_t\Pr(s_t = i, s_{t+1} = j\mid\mathcal{F}_T)}{\sum_t\xi_{t|T,i}}", font_size=34),
        ]
        whys = [why(r"Kim's smoother: the filter's answer revised with hindsight, run backwards from the last month"),
                why(r"the M-step: each regime's mean and variance, every month weighted by its probability of that regime"),
                why(r"the transitions: expected moves from $i$ to $j$ over expected time spent in $i$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "How the parameters are found. The filter only looks backwards; for estimation we may use hindsight. "
            "Kim's smoother runs from the last month back to the first and revises every month's probabilities with "
            "everything that came after. <bookmark mark='a'/> Then the maximisation step is weighted least squares: "
            "each regime's mean and variance are the averages of the months, weighted by how likely each month was "
            "to belong to that regime. <bookmark mark='b'/> And each transition probability is the expected number of "
            "moves from one regime to the other, over the expected time spent in the first. Expectation, then "
            "maximisation, repeated: Arthur Dempster, Nan Laird and Donald Rubin's algorithm of 1977, which never "
            "lowers the likelihood."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.3)
        self.clear_scene()
