from __future__ import annotations

import numpy as np
from scipy.stats import binom

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load

N_MAJ = 21


def majority_paths(k=6, seed=1):
    """P(at least 11 heads in 21 fair tosses | the first n): a martingale that ends at 0 or 1."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(k):
        h = rng.random(N_MAJ) < 0.5
        heads = np.concatenate([[0], np.cumsum(h)])
        n = np.arange(N_MAJ + 1)
        need = 11 - heads
        p = binom.sf(need - 1, N_MAJ - n, 0.5)
        p = np.where(need <= 0, 1.0, np.where(need > N_MAJ - n, 0.0, p))
        out.append(p)
    return np.array(out)


class Martingales(VoiceoverScene):
    def construct(self):
        m = load("martingales")
        self.card()
        self.definition()
        self.examples()
        self.majority()
        self.convex(m)

    def card(self):
        c = chapter_card(3, r"Martingales: Ville's fair games", r"What does it mean for a game to be fair?",
                         part=PART)
        with self.voiceover("Chapter three. Martingales: Ville's fair games."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        d = definition_card(r"Martingale", r"A process $M_0, M_1, \dots$ that is known at each time ($M_n$ depends only "
                            r"on $\mathcal{F}_n$), has a finite mean, and whose best forecast of tomorrow is today: "
                            r"$\mathbb{E}[M_{n+1} \mid \mathcal{F}_n] = M_n$.", width=8.6, color=MART, font_size=25)
        h = history_card(1939, r"Jean Ville, \textit{\'Etude critique de la notion de collectif}",
                         r"named fair games after the ``martingale'', the gamblers' doubling system; Joseph Doob built "
                         r"the theory (1940; \textit{Stochastic Processes}, 1953)", width=8.6)
        ex = VGroup(
            label(r"examples", font_size=24, color=GREY_A),
            MathTex(r"\text{a gambler's wealth in a fair game}", font_size=28),
            MathTex(r"S_n^2 - n \quad \text{for a walk of } \pm 1 \text{ steps}", font_size=28),
            MathTex(r"\mathbb{E}[X \mid \mathcal{F}_n] \quad \text{for any } X\text{: Doob's martingale}", font_size=28,
                    color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(d, h, ex).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "A martingale is a process whose best forecast of tomorrow is today. It is known at each time, it has a "
            "finite mean, and its conditional expectation one step ahead equals its current value. It is the "
            "mathematical form of a fair game. <bookmark mark='a'/> The name comes from Jean Ville's thesis of 1939, "
            "which borrowed it from the most famous betting system, the martingale, in which you double your stake "
            "after every loss. Joseph Doob read Ville and built the theory. <bookmark mark='b'/> Examples: a "
            "gambler's wealth in a fair game. The square of a random walk minus the number of steps. And, from the "
            "previous chapter, the conditional expectation of anything, as information arrives: Doob's martingale."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def examples(self):
        rows = [cmath(r"\mathbb{E}[M_{n+1} \mid \mathcal{F}_n]", r"=", r"M_n \quad (\le:\ \text{super}, \ \ge:\ \text{sub})",
                      font_size=38, colors={r"M_n \quad (\le:\ \text{super}, \ \ge:\ \text{sub})": MART}),
                cmath(r"\mathbb{E}[S_{n+1}^2 \mid \mathcal{F}_n]", r"=",
                      r"S_n^2 + 2S_n\,\mathbb{E}\xi + \mathbb{E}\xi^2 = S_n^2 + 1", font_size=38),
                cmath(r"\mathbb{E}\big[e^{\theta S_{n+1}} \mid \mathcal{F}_n\big]", r"=",
                      r"e^{\theta S_n}\cosh\theta \;\Rightarrow\; Z_n = e^{\theta S_n}(\cosh\theta)^{-n}", font_size=38),
                cmath(r"\mathbb{E}\big[\mathbb{E}[X \mid \mathcal{F}_{n+1}] \mid \mathcal{F}_n\big]", r"=",
                      r"\mathbb{E}[X \mid \mathcal{F}_n]", font_size=38, colors={r"\mathbb{E}[X \mid \mathcal{F}_n]": MART}),
                cmath(r"\mathbb{E}[\varphi(M_{n+1}) \mid \mathcal{F}_n]", r"\ge",
                      r"\varphi\big(\mathbb{E}[M_{n+1} \mid \mathcal{F}_n]\big) = \varphi(M_n)", font_size=38)]
        whys = [why(r"a martingale: adapted, integrable, tomorrow's forecast is today; a supermartingale drifts down "
                    r"(a casino's customer), a submartingale up"),
                why(r"$\xi = \pm 1$ fair, independent of the past; so $S_n^2 - n$ is a martingale"),
                why(r"the moment generating function of $\pm 1$ is $\cosh\theta$: the exponential martingale"),
                why(r"the tower property: Doob's martingale of forecasts"),
                why(r"Jensen: a convex function of a martingale is a submartingale")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.8, buff=0.55, edge=6.9)
        with self.voiceover(
            "Fair, unfavourable and favourable games have names. If tomorrow's forecast is at most today, a "
            "supermartingale: the gambler's wealth at a casino. If at least, a submartingale. "
            "<bookmark mark='a'/> Three examples, each proved in a line. For a fair walk, expand the square of the "
            "next position: the cross term averages to zero and the new step squared is one, so the walk squared "
            "minus the number of steps is a martingale. <bookmark mark='b'/> The exponential of theta times the walk "
            "grows on average by the hyperbolic cosine of theta per step, the moment generating function of a plus "
            "or minus one step; dividing by it gives the exponential martingale, which chapter five uses to time the "
            "walk. <bookmark mark='c'/> The forecast of anything, refined as information arrives, is a martingale "
            "by the tower property. <bookmark mark='d'/> And Jensen's inequality turns a convex function of a "
            "martingale into a submartingale."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def majority(self):
        P = majority_paths()
        g = axes([0, N_MAJ], [0, 1], x_length=8.0, y_length=4.4, xlabel=r"tosses seen", ylabel=r"chance that heads "
                 r"wins a best-of-21", xticks=[0, 7, 14, 21], yticks=[0, 0.5, 1], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = color_gradient([MART, QC.SPOT], len(P))
        n = np.arange(N_MAJ + 1)
        others = VGroup(*[curve(ax, n, p, c, stroke_width=2.5).set_stroke(opacity=0.55) for p, c in zip(P[1:], cols[1:])])
        main = P[0]
        tk = ValueTracker(0.0)
        live = tracing(ax, n, main, tk, MART, stroke_width=4)

        def fan():
            k = int(np.clip(np.floor(tk.get_value() + 1e-6), 0, N_MAJ - 1))
            now = main[k]
            # the two possible next values: the forecast after one more head or one more tail
            seen = majority_heads(k)
            up_v = win_prob(seen + 1, k + 1)
            dn_v = win_prob(seen, k + 1)
            x0, x1 = ax.c2p(k, now), ax.c2p(k + 1, 0)[0]
            g_ = VGroup(DashedLine(x0, [x1, ax.c2p(0, up_v)[1], 0], color=GREY_B, stroke_width=1.5),
                        DashedLine(x0, [x1, ax.c2p(0, dn_v)[1], 0], color=GREY_B, stroke_width=1.5),
                        Dot([x1, ax.c2p(0, up_v)[1], 0], radius=0.07, color=QC.GAIN),
                        Dot([x1, ax.c2p(0, dn_v)[1], 0], radius=0.07, color=LOSS),
                        Line([x1 - 0.12, ax.c2p(0, (up_v + dn_v) / 2)[1], 0], [x1 + 0.12, ax.c2p(0, (up_v + dn_v) / 2)[1], 0],
                             color=QC.IDEA, stroke_width=4),
                        Dot(x0, radius=0.08, color=MART))
            return g_

        def majority_heads(k):
            return int(round(_heads0[k]))

        _heads0 = majority_heads_path()
        fan_m = always_redraw(fan)
        side = VGroup(
            label(r"a live forecast is a martingale:", font_size=22, color=GREY_A),
            label(r"it starts at its mean, 50\%,", font_size=22, color=GREY_A),
            label(r"moves only on news,", font_size=22, color=GREY_A),
            label(r"and ends at 0 or 1", font_size=22, color=GREY_A),
            label(r"the fan: tomorrow's two values; gold tick: their mean $=$ today", font_size=19, color=QC.IDEA),
            wrapped_label(r"a betting market's price, or an option's risk-neutral probability of finishing in the "
                          r"money, behaves the same way (Part 9)", 4.4, 20, MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Here is a Doob martingale you can watch. Two players toss a fair coin twenty-one times, and heads wins "
            "if it comes up eleven times or more. After each toss, compute the chance that heads wins, given the "
            "tosses so far. <bookmark mark='a'/> Each line is one match. Every forecast starts at fifty percent, "
            "jumps with each toss, more sharply as the end approaches, and finishes at zero or one. Yet on average "
            "it never moves: today's forecast is the average of tomorrow's. <bookmark mark='b'/> A betting market's "
            "price behaves like this, and so, under the right measure, does an option's probability of finishing in "
            "the money."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:4]))
            vo.wait_until("a")
            self.add(live, fan_m)
            self.play(FadeIn(side[4]))
            self.play(tk.animate.set_value(N_MAJ - 1.0), run_time=7, rate_func=linear)
            fan_m.clear_updaters()
            self.play(FadeOut(fan_m), tk.animate.set_value(float(N_MAJ)), run_time=0.5)
            live.clear_updaters()
            self.play(LaggedStart(*[Create(p) for p in others], lag_ratio=0.3, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def convex(self, m):
        n = np.asarray(m["n"])
        call, sim = np.asarray(m["call"]), np.asarray(m["call_sim"])
        absm = np.asarray(m["abs"])
        g = axes([0, 50], [0, 6], x_length=7.2, y_length=4.2, xlabel=r"steps $n$ of a fair $\pm1$ walk from 0",
                 ylabel=r"expected value", xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 2, 4, 6],
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        l_call = tracing(ax, n, call, tk, QC.OPTION, stroke_width=3.5)
        l_abs = tracing(ax, n, absm, tk, P_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=WHITE) for a, b in zip(n[::2], sim[::2])])
        leg = legend([(QC.OPTION, r"$\mathbb{E}(S_n - 2)^+$, a call struck at 2"), (P_C, r"$\mathbb{E}|S_n|$"),
                      (WHITE, r"20{,}000 simulated walks")], font_size=19)
        side = VGroup(
            leg,
            MathTex(rf"\mathbb{{E}}(S_{{50}} - 2)^+ = {call[-1]:.2f}", font_size=30, color=QC.OPTION),
            MathTex(rf"\mathbb{{E}}|S_{{50}}| = {absm[-1]:.2f} \approx \sqrt{{2 \cdot 50/\pi}} = {np.sqrt(100 / np.pi):.2f}",
                    font_size=28, color=P_C),
            wrapped_label(r"a forward is a martingale under the pricing measure, so a call on it is a submartingale: "
                          r"longer-dated calls are worth more (calendar spreads $\ge 0$, Part 12)", 4.6, 20, GREY_A),
            wrapped_label(r"Markov $\ne$ martingale: Markov is about memory, martingale about the mean; a biased walk is "
                          r"Markov but not a martingale", 4.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        pred = desk_question(r"Is $|S_n|$ a martingale?", r"No: $|x|$ is convex, so it is a submartingale; its mean "
                             r"grows like $\sqrt{2n/\pi}$.", width=4.2, font_size=20)
        with self.voiceover(
            "That last fact has a price. A call on the walk struck at two pays a convex function, so its value can "
            f"only rise with time. <bookmark mark='a'/> Watch it grow to {call[-1]:.2f} after fifty steps, simulated "
            "walks landing on the exact curve: in Part nine, longer-dated calls are worth more for this reason. "
            "<bookmark mark='b'/> Is the absolute value of the walk a martingale? No, a submartingale; its mean grows "
            f"like the square root of two n over pi, {absm[-1]:.2f} at fifty. <bookmark mark='c'/> And Markov is not "
            "martingale: Markov is about memory, martingale about the mean."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.add(l_call, l_abs)
            vo.wait_until("a")
            self.play(tk.animate.set_value(50.0), run_time=5, rate_func=linear)
            l_call.clear_updaters()
            l_abs.clear_updaters()
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(pred.move_to(ax.c2p(13, 5.0))))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()


def win_prob(heads, seen):
    """P(heads reaches 11 of 21 | ``heads`` heads in the first ``seen`` tosses)."""
    need = 11 - heads
    left = N_MAJ - seen
    if need <= 0:
        return 1.0
    if need > left:
        return 0.0
    return float(binom.sf(need - 1, left, 0.5))


def majority_heads_path(seed=1):
    """The heads count after each toss of the first match drawn by majority_paths (same seed, same draws)."""
    rng = np.random.default_rng(seed)
    h = rng.random(N_MAJ) < 0.5
    return np.concatenate([[0], np.cumsum(h)])
