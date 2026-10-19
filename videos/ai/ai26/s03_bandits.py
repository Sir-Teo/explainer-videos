from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, EXPLORE, PART, REWARD, VALUE, axes, curve, legend, load

GREEDY, EPS, UCB, THOMPSON = GREY_B, C.MODEL_Q, C.TRUE_P, C.INTERVAL


class Bandits(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.greedy()
        self.regret()
        self.ucb()
        self.ucb_live()
        self.thompson()

    def card(self):
        card = chapter_card(2, r"Explore or exploit", r"Try the best-looking option, or find out about the others?",
                            lit=(), part=PART)
        with self.voiceover("Chapter two. Explore or exploit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def arms(self, n=5, x0=-5.2, gap=1.5, y=-0.4, height=4.2):
        """Vertical reward scales, one per arm."""
        g = VGroup()
        for k in range(n):
            x = x0 + k * gap
            ax = Line([x, y - height / 2, 0], [x, y + height / 2, 0], color=GREY_D, stroke_width=2)
            lab = label(rf"arm {k + 1}", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
            g.add(VGroup(ax, lab))
        g.y, g.h, g.x0, g.gap = y, height, x0, gap
        return g

    def ry(self, g, v, lo=-2.0, hi=2.5):
        return g.y - g.h / 2 + g.h * (v - lo) / (hi - lo)

    def machines(self):
        d = load("bandit")
        q = np.asarray(d["ucb_q"])
        g = self.arms()
        means = VGroup(*[Line([g.x0 + k * g.gap - 0.35, self.ry(g, v), 0], [g.x0 + k * g.gap + 0.35, self.ry(g, v), 0],
                              color=REWARD, stroke_width=4) for k, v in enumerate(q)])
        curves = VGroup()
        for k, v in enumerate(q):  # each arm pays N(q_k, 1): its density, drawn sideways
            ys = np.linspace(-2.0, 2.5, 60)
            dens = np.exp(-0.5 * (ys - v) ** 2)
            pts = [[g.x0 + k * g.gap + 0.55 * dv, self.ry(g, yy), 0] for yy, dv in zip(ys, dens)]
            curves.add(VMobject(stroke_color=REWARD, stroke_width=2, stroke_opacity=0.6).set_points_smoothly(pts))
        hidden = VGroup(*[label(r"?", font_size=44, color=GREY_B).move_to([g.x0 + k * g.gap, g.y + 0.3, 0])
                          for k in range(len(q))])
        d_b = definition_card(r"$k$-armed bandit", r"$k$ actions, \ each paying a random reward from its own unknown "
                              r"distribution, \ mean $\mu_a$. \ Choose one per step; \ maximize the total.",
                              color=REWARD, width=5.0).to_edge(RIGHT, buff=0.35).shift(UP * 1.2)
        uses = wrapped_label(r"used for: \ clinical trials, \ A/B tests, \ ad placement, \ recommendations", 4.6,
                             font_size=22, color=GREY_A).next_to(d_b, DOWN, buff=0.3).align_to(d_b, LEFT)
        hc = history_card(1933, r"William R. Thompson", r"which of two treatments to give the next patient",
                          width=4.6, color=REWARD).next_to(uses, DOWN, buff=0.35)
        with self.voiceover(
            "Before states and long horizons, take reinforcement learning with every complication removed but one. "
            "<bookmark mark='a'/> You face k slot machines, one-armed bandits. Each pays a random reward from its "
            "own distribution, and you don't know which is best. <bookmark mark='b'/> Pull one arm per step, for "
            "as many steps as you're given, and collect as much as you can. <bookmark mark='c'/> This is the "
            "problem a doctor faces choosing between treatments, and a website choosing which version of a page to "
            "show: Thompson posed it in 1933 about patients. <bookmark mark='d'/> There's one state, so no credit "
            "assignment and no planning. What's left is pure exploration: every pull spent learning about an arm "
            "that might be worse is a pull not spent on the arm that looks best."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(a) for a in g], lag_ratio=0.15), FadeIn(hidden))
            vo.wait_until("a")
            self.play(FadeIn(d_b, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(hidden), LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.15),
                      LaggedStart(*[Create(m) for m in means], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(uses), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(means[1], color=REWARD, scale_factor=1.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def greedy(self):
        d = load("bandit")
        T = len(d["reward_greedy"])
        g = axes([0, T], [0, 1], x_length=6.2, y_length=3.6, xlabel=r"pulls", ylabel=r"how often the best arm is pulled",
                 xticks=[0, 500, 1000], yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.6, -0.2, 0])
        ax = g.ax
        t = np.arange(1, T + 1)
        sm = lambda y: np.convolve(y, np.ones(10) / 10, mode="same")
        cg = curve(ax, t[5:-5], sm(d["optimal_greedy"])[5:-5], GREEDY, 3)
        ce = curve(ax, t[5:-5], sm(d["optimal_eps"])[5:-5], EPS, 3)
        lg = legend([(GREEDY, r"greedy"), (EPS, r"$\varepsilon$-greedy, \ $\varepsilon = 0.1$")]).move_to([3.6, 1.6, 0])
        rule = VGroup(
            label(r"estimate: \ $\hat\mu_a$ = average reward from arm $a$", font_size=24),
            label(r"greedy: \ pull $\arg\max_a \hat\mu_a$", font_size=24, color=GREEDY),
            label(r"$\varepsilon$-greedy: \ the same, \ but a random arm \\ with probability $\varepsilon$",
                  font_size=24, color=EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, -0.9, 0])
        tag = note(r"10 arms, \ means $\sim \mathcal N(0, 1)$, \ $2{,}000$ runs; \ computed").to_corner(DR, buff=0.25)
        og, oe = 100 * d["optimal_greedy"][-100:].mean(), 100 * d["optimal_eps"][-100:].mean()
        with self.voiceover(
            "The obvious strategy: keep an average of the rewards from each arm, and always pull the arm with the "
            "best average. That's the greedy rule. <bookmark mark='a'/> Here it is on the standard testbed from "
            "Sutton and Barto's book: ten arms whose means are themselves random, two thousand runs. Greedy settles "
            f"early on whichever arm happened to pay well at first, and finds the best arm only {og:.0f} percent of "
            "the time. <bookmark mark='b'/> The fix is to explore on purpose. Epsilon-greedy pulls a random arm "
            f"one time in ten: it finds the best arm {oe:.0f} percent of the time. <bookmark mark='c'/> But it "
            "never stops exploring. Even after it knows, it wastes a tenth of its pulls."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rule[0]), FadeIn(tag))
            self.play(FadeIn(rule[1]))
            vo.wait_until("a")
            self.play(Create(cg), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rule[2]))
            self.play(Create(ce), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(rule[2], color=EPS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def regret(self):
        rows = [
            cmath(r"\mathrm{Regret}(T)", r"=", r"T \mu^*", r"- \mathbb E\Big[\sum_{t=1}^T r_t\Big]", font_size=38),
            cmath(r"\mathrm{Regret}(T)", r"=", r"\sum_a \Delta_a\, \mathbb E[N_a(T)]", font_size=38),
        ]
        whys = [why(r"$\mu^*$: the best arm's mean"),
                why(r"$\Delta_a = \mu^* - \mu_a$, \ $N_a$: pulls of arm $a$")]
        for r_ in rows:
            r_[0].set_color(C.SURPRISE)
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.6)
        lin = label(r"$\varepsilon$-greedy: \ $N_a(T) \approx \varepsilon T / k$ \ $\Rightarrow$ \ regret grows like $T$",
                    font_size=28, color=EPS).move_to(DOWN * 1.2)
        goal = label(r"goal: \ regret that grows much slower than $T$", font_size=28, color=REWARD).move_to(DOWN * 2.3)
        with self.voiceover(
            "To compare strategies we need a score. The regret after T pulls is what you would have earned by "
            "always pulling the best arm, minus what you expect to earn. <bookmark mark='a'/> Each pull of a worse "
            "arm a costs its gap, delta a, so the regret is the sum over arms of the gap times the expected number "
            "of pulls of that arm. <bookmark mark='b'/> Epsilon-greedy pulls every arm a fixed fraction of the time "
            "forever, so its regret grows in proportion to T. <bookmark mark='c'/> A good strategy pulls the bad "
            "arms less and less often, so its regret grows much more slowly than T."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(lin))
            vo.wait_until("c")
            self.play(FadeIn(goal))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ucb(self):
        rows = [
            cmath(r"\Pr\big[\, \hat\mu_a", r"\ge", r"\mu_a + \epsilon \,\big]", r"\le", r"e^{-2 n_a \epsilon^2}",
                  font_size=36),
            cmath(r"e^{-2 n_a \epsilon^2}", r"=", r"t^{-4}", font_size=36),
            cmath(r"\epsilon", r"=", r"\sqrt{\frac{2 \ln t}{n_a}}", font_size=36),
            cmath(r"a_t", r"=", r"\arg\max_a \Big[\, \hat\mu_a", r"+", r"\sqrt{\frac{2 \ln t}{n_a}}", r"\,\Big]",
                  font_size=36),
        ]
        rows[3][4].set_color(EXPLORE)
        rows[2][2].set_color(EXPLORE)
        whys = [why(r"Hoeffding, \ rewards in $[0, 1]$, \ $n_a$ pulls"), why(r"make a miss rare"),
                why(r"solve for $\epsilon$"), why(r"pull the arm with the highest \\ plausible mean")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.5, align_index=1, buff=0.42)
        th = theorem_card(r"UCB1", r"each worse arm is pulled at most $\frac{8 \ln T}{\Delta_a^2} + O(1)$ times, \ so "
                          r"$\mathrm{Regret}(T) = O\big(\sum_a \frac{\ln T}{\Delta_a}\big)$", who=r"Auer, Cesa-Bianchi "
                          r"\& Fischer (2002)", width=6.2, color=UCB)
        lb = theorem_card(r"a lower bound", r"any strategy good on every bandit pulls arm $a$ at least "
                          r"$\frac{\ln T}{\mathrm{KL}(\mu_a \,\|\, \mu^*)}$ times: \ $\log T$ regret is the best possible",
                          who=r"Lai \& Robbins (1985)", width=6.2, color=C.KL)
        cards = VGroup(th, lb).arrange(DOWN, buff=0.35).move_to([3.3, -0.3, 0])
        with self.voiceover(
            "A cleverer idea: optimism in the face of uncertainty. Act as if each arm is as good as it plausibly "
            "could be. How good is plausible? <bookmark mark='a'/> Hoeffding's inequality from Part 5: after n "
            "pulls, the chance that an arm's average overestimates its mean by epsilon is at most e to the minus "
            "two n epsilon squared. <bookmark mark='b'/> Choose epsilon so that this chance is tiny, t to the "
            "minus four, <bookmark mark='c'/> and epsilon is the square root of two log t over n. "
            "<bookmark mark='d'/> That's the upper confidence bound algorithm, UCB: pull the arm with the highest "
            "average plus bonus. An arm pulled rarely has a big bonus, so it gets tried; the bonus shrinks as its "
            "pulls pile up, and grows slowly, like log t, for arms left alone, so no arm is abandoned for good. "
            "<bookmark mark='e'/> The payoff is a theorem: each worse arm is pulled only about log T over its gap "
            "squared times, so the regret grows like log T. <bookmark mark='f'/> And Lai and Robbins proved in 1985 "
            "that no strategy can do better than logarithmic regret. UCB is, up to constants, the best possible."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(*[FadeOut(w) for w in whys], VGroup(*rows).animate.scale(0.82).to_edge(LEFT, buff=0.4))
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(lb, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ucb_live(self):
        d = load("bandit")
        est, cnt, ub, act = (np.asarray(d[k]) for k in ("ucb_est", "ucb_cnt", "ucb_bound", "ucb_act"))
        q = np.asarray(d["ucb_q"])
        steps = len(act)
        g = self.arms(x0=-5.6, gap=1.25, y=-0.2, height=4.6)
        t = ValueTracker(0)
        lo, hi = -2.0, 3.5

        def Y(v):
            return g.y - g.h / 2 + g.h * (np.clip(v, lo, hi) - lo) / (hi - lo)

        means = VGroup(*[DashedLine([g.x0 + k * g.gap - 0.35, Y(v), 0], [g.x0 + k * g.gap + 0.35, Y(v), 0],
                                    color=REWARD, stroke_width=2, dash_length=0.06) for k, v in enumerate(q)])

        def bars():
            i = min(int(t.get_value()), steps - 1)
            out = VGroup()
            for k in range(len(q)):
                x = g.x0 + k * g.gap
                if cnt[i, k] == 0:
                    continue
                b = ub[i, k] - est[i, k]
                rect = Rectangle(width=0.36, height=max(Y(est[i, k] + b) - Y(est[i, k] - b), 0.02), stroke_width=0,
                                 fill_color=EXPLORE, fill_opacity=0.28).move_to([x, (Y(est[i, k] + b) + Y(est[i, k] - b)) / 2, 0])
                top = Line([x - 0.22, Y(ub[i, k]), 0], [x + 0.22, Y(ub[i, k]), 0], color=EXPLORE, stroke_width=4)
                dot = Dot([x, Y(est[i, k]), 0], radius=0.07, color=WHITE)
                n = MathTex(str(int(cnt[i, k])), font_size=22, color=GREY_A).move_to([x, g.y - g.h / 2 - 0.65, 0])
                out.add(rect, top, dot, n)
            a = act[i]
            out.add(SurroundingRectangle(VGroup(Dot([g.x0 + a * g.gap, Y(ub[i, a]), 0])), color=AGENT, buff=0.12))
            return out

        live = always_redraw(bars)
        tl = always_redraw(lambda: MathTex(rf"t = {min(int(t.get_value()) + 1, steps)}", font_size=34, color=GREY_A)
                           .move_to([-2.9, 3.2, 0]))
        nl = label(r"pulls", font_size=20, color=GREY_B).move_to([g.x0 - 0.9, g.y - g.h / 2 - 0.65, 0])
        key = VGroup(
            VGroup(Dot(radius=0.07, color=WHITE), label(r"average $\hat\mu_a$", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=EXPLORE, stroke_width=4),
                   label(r"upper bound: \ $\hat\mu_a + \sqrt{2 \ln t / n_a}$", font_size=22, color=EXPLORE))
            .arrange(RIGHT, buff=0.15),
            VGroup(DashedLine(ORIGIN, RIGHT * 0.4, color=REWARD, dash_length=0.06),
                   label(r"true mean (hidden from it)", font_size=22, color=REWARD)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, 1.6, 0])
        best = int(np.argmax(q))
        share = 100 * cnt[-1, best] / cnt[-1].sum()
        with self.voiceover(
            "Watch it work on five arms. The white dot is each arm's average, the bar above it the bonus, and the "
            "arm with the highest top gets pulled, boxed in blue. <bookmark mark='a'/> Early on every arm's bar is "
            "tall, and the pulls go round. <bookmark mark='b'/> As an arm is pulled its bar shrinks, and arms "
            f"whose averages are low drop out of contention. After {steps} pulls, {share:.0f} percent went to the "
            "best arm, and the worst was tried only a handful of times, just enough to be sure."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(a) for a in g], lag_ratio=0.1), FadeIn(means), FadeIn(key), FadeIn(nl))
            self.add(live, tl)
            vo.wait_until("a")
            self.play(t.animate.set_value(30), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(steps - 1), run_time=max(5.0, vo.remaining() - 1.0), rate_func=linear)
        self.wait(0.3)
        live.clear_updaters()
        tl.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def thompson(self):
        d = load("bandit")
        x = np.linspace(-1.2, 1.6, 200)
        posts = [(0.45, 8, GREY_B), (0.55, 30, THOMPSON), (0.2, 3, C.MODEL_Q)]
        g = axes([-1.2, 1.6], [0, 3.5], x_length=5.6, y_length=2.6, xlabel=r"what the arm's mean might be",
                 center=[-3.2, 1.2, 0])
        ax = g.ax
        dens = VGroup()
        for m, n, col in posts:
            s = 1 / math.sqrt(n + 1)
            y = np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
            dens.add(curve(ax, x, y, col, 3, smooth=True))
        draws = [0.38, 0.51, 0.74]
        ticks = VGroup(*[Line(ax.c2p(v, 0), ax.c2p(v, 0.6), color=col, stroke_width=5)
                         for v, (_, _, col) in zip(draws, posts)])
        pick = label(r"the third arm's sample is highest: \ pull it", font_size=22, color=C.MODEL_Q)
        pick.next_to(g, DOWN, buff=0.2)
        rule = label(r"Thompson sampling: \ draw a mean from each arm's posterior, \\ pull the arm whose draw is "
                     r"largest", font_size=24).next_to(pick, DOWN, buff=0.35)
        T = len(d["coin_ucb"])
        lt = np.log10(np.arange(1, T + 1))
        p = d["coin_p"]
        ymax = 200
        r = axes([0, math.log10(T)], [0, ymax], x_length=5.4, y_length=3.6, xlabel=r"pulls (log scale)",
                 ylabel=rf"regret, \ two coins, \ $p = {p[0]}, {p[1]}$", xticks=[1, 2, 3, 4], yticks=[0, 100, 200],
                 log_x=True, center=[3.3, -0.6, 0])
        idx = np.unique(np.round(np.logspace(0, math.log10(T - 1), 120)).astype(int))
        lines = VGroup()
        for m, col in (("eps", EPS), ("ucb", UCB), ("thompson", THOMPSON)):
            y = np.asarray(d[f"coin_{m}"])[idx]
            keep = y <= ymax
            lines.add(curve(r.ax, lt[idx][keep], y[keep], col, 3))
        off = label(rf"$\varepsilon$-greedy: \ ${d['coin_eps'][-1]:.0f}$ by the end", font_size=18, color=EPS)
        off.next_to(r.ax.c2p(lt[idx][np.asarray(d['coin_eps'])[idx] <= ymax][-1], ymax), LEFT, buff=0.1).shift(DOWN * 0.15)
        lg = legend([(EPS, r"$\varepsilon$-greedy"), (UCB, r"UCB"), (THOMPSON, r"Thompson")], font_size=20)
        lg.move_to(r.ax.c2p(0.95, ymax * 0.82))
        tag = note(r"$1{,}000$ runs; \ computed").to_corner(DR, buff=0.2)
        ot = 100 * d["optimal_thompson"][-100:].mean()
        with self.voiceover(
            "There's an older idea, from Thompson himself. Keep a posterior for each arm's mean, Bayes's rule from "
            "Part 5, updated after every pull. <bookmark mark='a'/> Then, at each step, draw one plausible mean "
            "from each posterior and pull the arm whose draw is largest. <bookmark mark='b'/> An arm is pulled "
            "exactly as often as it is likely to be the best: well-known bad arms almost never, uncertain ones "
            "sometimes. <bookmark mark='c'/> On the ten-armed testbed it finds the best arm "
            f"{ot:.0f} percent of the time, the best of the four. And on a pair of coins, <bookmark mark='d'/> "
            "plotted against the log of the number of pulls, epsilon-greedy's regret bends upward and leaves the "
            "chart: it grows like T. UCB and Thompson sampling settle into straight lines here, like log T, and "
            "Thompson's line is the flattest. <bookmark mark='e'/> Remember the upper confidence bound. Ten chapters from now it will be "
            "steering the search inside AlphaGo."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[Create(c_) for c_ in dens], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(t_, DOWN) for t_ in ticks], lag_ratio=0.3))
            self.play(FadeIn(pick), Indicate(ticks[2], color=C.MODEL_Q))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(FadeIn(r), FadeIn(tag))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(lg), run_time=3.0)
            self.play(FadeIn(off))
            vo.wait_until("e")
            self.play(Indicate(lines[1], color=UCB, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()
