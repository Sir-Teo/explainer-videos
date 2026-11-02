from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, PART, PUT, Q_C, answer_under, illustration, load,
                                        pause_at)


class FreeLunch(VoiceoverScene):
    def construct(self):
        f = load("free_lunch")
        self.card()
        self.doubling_math()
        self.doubling_run(f)
        self.nflvr()
        self.bubble(f)
        self.predict()

    def card(self):
        c = chapter_card(10, r"Free lunches, doubling, and bubbles", r"Why does continuous time need more than ``no "
                         r"arbitrage''?", lit=(1994,), part=PART)
        with self.voiceover("Chapter ten. Free lunches, doubling, and bubbles."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def doubling_math(self):
        rows = [cmath(r"\theta_t", r"=", r"(T - t)^{-1/2},\qquad X_t = \int_0^t \theta_s\, dW_s", font_size=36,
                      colors={r"\theta_t": ARB}),
                cmath(r"\langle X\rangle_t", r"=", r"\int_0^t \frac{ds}{T - s} = \ln\frac{T}{T - t}\ \longrightarrow\ "
                      r"\infty", font_size=36),
                cmath(r"X_t", r"=", r"\beta_{\langle X\rangle_t}\ \Rightarrow\ X\ \text{hits } +1 \text{ before } T",
                      font_size=36, colors={r"X_t": ARB}),
                cmath(r"P\big(\min X < -k\ \text{before}\ +1\big)", r"=", r"\frac{1}{1 + k}", font_size=36,
                      colors={r"\frac{1}{1 + k}": PUT})]
        whys = [why(r"bet ever harder on a fair game as the deadline nears: the continuous-time doubling strategy", 21),
                why(r"It\^o's isometry: the clock of $X$ runs out to infinity before time $T$", 21),
                why(r"Dambis--Dubins--Schwarz: $X$ is a Brownian motion $\beta$ on that clock, and a Brownian motion "
                    r"given infinite time reaches every level; stop when it reaches $+1$", 21),
                why(r"but on the way: the gambler's-ruin formula of Part 4: half the paths fall below $-1$, one in "
                    r"eleven below $-10$, and the losses are unbounded", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Continuous time allows a trick one period never did. Bet on a fair game harder and "
            "harder as a deadline nears: hold one over the square root of the time left. <bookmark "
            "mark='a'/> The variance of the gains, the log of T over the time left, runs to infinity "
            "before the deadline. <bookmark mark='b'/> By Dambis, Dubins and Schwarz the gains are a "
            "Brownian motion on that clock, so they reach plus one before T for sure. Stop there: a "
            "sure profit from a fair game. <bookmark mark='c'/> The catch: by Part four's gambler's "
            "ruin, the wealth first falls below minus k with probability one over one plus k. Half "
            "the paths go below minus one."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def doubling_run(self, f):
        clock = np.asarray(f["draw_clock"])
        tt = 1 - np.exp(-clock)
        g = axes([0, 1.0], [-6.5, 1.6], x_length=7.0, y_length=5.0, xlabel=r"time, as a fraction of the deadline $T$",
                 ylabel=r"the doubler's gains", xticks=[0, 0.5, 0.9, 1.0], yticks=[-6, -4, -2, -1, 0, 1], font_size=16)
        g.to_edge(LEFT, buff=1.8).shift(DOWN * 0.2)
        ax = g.ax
        win = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=CALL, stroke_width=2)
        k = ValueTracker(0.0)
        draws = [np.asarray(d) for d in f["draw"]]

        def fan():
            v = k.get_value()
            out = VGroup()
            for d in draws:
                n = len(d)
                m = max(2, int(min(v, 1.0) * n))
                pts = [ax.c2p(tt[i], np.clip(d[i], -6.5, 1.6)) for i in range(m)]
                col = CALL if m >= n and d[-1] >= 0.99 else FWD
                out.add(VMobject(stroke_width=1.3, stroke_color=col, stroke_opacity=0.45).set_points_as_corners(pts))
            return out

        FAN = always_redraw(fan)
        mins = np.array([d.min() for d in draws])

        def hist():
            v = min(k.get_value(), 1.0)
            cur = np.array([d[:max(2, int(v * len(d)))].min() for d in draws])
            bins = np.linspace(-6.5, 0, 14)
            h, _ = np.histogram(np.clip(cur, -6.49, 0), bins)
            x0 = ax.get_left()[0] - 0.2
            out = VGroup()
            for i, c in enumerate(h):
                if c == 0:
                    continue
                y0, y1 = ax.c2p(0, bins[i])[1], ax.c2p(0, bins[i + 1])[1]
                wdt = 1.4 * c / len(draws) * 2.5
                out.add(Rectangle(width=wdt, height=y1 - y0 - 0.02, stroke_width=0, fill_color=PUT,
                                  fill_opacity=0.75).move_to([x0 - wdt / 2, (y0 + y1) / 2, 0]))
            return out

        H = always_redraw(hist)
        hl = label(r"worst loss so far", font_size=17, color=PUT).next_to(ax.get_left(), LEFT, buff=0.3).shift(UP * 2.3)
        fr, ex = f["frac"], f["frac_exact"]
        side = VGroup(
            label(rf"{f['n']:,} doublers simulated".replace(",", "{,}"), font_size=22, color=FWD),
            MathTex(rf"\text{{below }} -1:\ {100 * fr['1']:.1f}\%\ \ (\text{{theory }} {100 * ex['1']:.1f}\%)",
                    font_size=26, color=PUT),
            MathTex(rf"\text{{below }} -3:\ {100 * fr['3']:.1f}\%\ \ (\text{{theory }} {100 * ex['3']:.1f}\%)",
                    font_size=26, color=PUT),
            MathTex(rf"\text{{below }} -10:\ {100 * fr['10']:.1f}\%\ \ (\text{{theory }} {100 * ex['10']:.1f}\%)",
                    font_size=26, color=PUT),
            wrapped_label(r"every path that finishes ends at $+1$ (green); none ends below", 3.8, 19, CALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        floor = DashedLine(ax.c2p(0, -1), ax.c2p(1, -1), color=ARB, stroke_width=3)
        fl = label(r"admissible: wealth must stay above $-a$ (here $a = 1$)", font_size=19, color=ARB).next_to(
            ax.c2p(0.02, -1), DOWN, buff=0.1, aligned_edge=LEFT)
        src = illustration(r"simulated: Brownian motion on the clock $\ln T/(T - t)$, bridge-corrected crossings")
        with self.voiceover(
            "A hundred and twenty doublers. <bookmark mark='a'/> One by one they reach plus one and "
            "stop, in green, while the histogram of their worst losses grows a tail that keeps going. "
            f"<bookmark mark='b'/> Over {f['n']:,} simulated doublers, {100 * fr['1']:.1f} percent "
            f"fell below minus one, theory a half; {100 * fr['10']:.1f} percent below minus ten, "
            "theory one in eleven. <bookmark mark='c'/> The fix: admissible strategies, whose wealth "
            "never falls below some minus a. With a floor at minus one, half the doublers are stopped "
            "out."
            " The admissible doubler, stopped at minus one or plus one, wins half the time and loses "
            "half the time: a fair game again."
        ) as vo:
            self.play(FadeIn(g), Create(win), FadeIn(src), FadeIn(hl))
            self.add(FAN, H)
            vo.wait_until("a")
            self.play(k.animate.set_value(1.0), run_time=max(vo.until("b") - 0.2, 4.0), rate_func=linear)
            FAN.clear_updaters()
            H.clear_updaters()
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[:4]], lag_ratio=0.3), FadeIn(side[4]), run_time=2)
            vo.wait_until("c")
            self.play(Create(floor), FadeIn(fl))
        FAN.clear_updaters()
        H.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def nflvr(self):
        d = definition_card(r"No free lunch with vanishing risk (NFLVR)",
                            r"there is no sequence of admissible strategies whose terminal gains converge to a "
                            r"non-negative, non-zero limit while their worst losses shrink to zero",
                            color=Q_C, width=6.6, font_size=22)
        t = theorem_card(r"Delbaen and Schachermayer (1994, 1998)",
                         r"for a locally bounded price process: NFLVR $\iff$ an equivalent local martingale measure "
                         r"exists; in general, an equivalent $\sigma$-martingale measure.", color=Q_C, width=6.4,
                         font_size=22)
        h1 = history_card(1981, r"Kreps", r"``free lunch'': a limit of near-arbitrages, in a weak topology", width=4.2,
                          font_size=18)
        h2 = history_card(1990, r"Dalang, Morton and Willinger", r"discrete time, any probability space: no arbitrage "
                          r"$\iff$ an equivalent martingale measure", width=4.2, font_size=18)
        top = VGroup(d, t).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(UP, buff=0.4)
        bot = VGroup(h1, h2).arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(top, DOWN, buff=0.35)
        with self.voiceover(
            "Admissibility is still not quite enough. Kreps saw in 1981 that limits of "
            "near-arbitrages, free lunches, must go too. <bookmark mark='a'/> In discrete time "
            "Dalang, Morton and Willinger showed in 1990 that plain no arbitrage suffices, on any "
            "probability space. <bookmark mark='b'/> In continuous time Delbaen and Schachermayer "
            "found the condition in 1994: no free lunch with vanishing risk. <bookmark mark='c'/> It "
            "is equivalent to an equivalent local martingale measure, and in full generality, in "
            "1998, a sigma-martingale measure: the theorem's final form."
            " Why vanishing risk? Ruling out trades whose losses shrink to nothing while the gains "
            "stay, not just exact arbitrages, is what keeps the set of attainable payoffs closed, so "
            "chapter four's separating hyperplane still exists in infinite dimensions."
        ) as vo:
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(t, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def bubble(self, f):
        t, P = np.asarray(f["bub_t"]), np.asarray(f["bub_paths"])
        mean = np.asarray(f["bub_mean"])
        g = axes([0, 1.0], [0, 4.0], x_length=7.0, y_length=4.6, xlabel=r"time", ylabel=r"$S_t = 1/|B_t|$",
                 xticks=[0, 0.5, 1.0], yticks=[0, 1, 2, 3, 4], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        fan = VGroup(*[VMobject(stroke_width=1.1, stroke_color=ALT, stroke_opacity=0.35).set_points_as_corners(
            [ax.c2p(a, min(b, 4.0)) for a, b in zip(t, row)]) for row in P])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        mc = curve(ax, t, mean, Q_C, stroke_width=5)
        b = f["bubble"]
        side = VGroup(
            wrapped_label(r"$B$: a Brownian motion in three dimensions, from $(1, 0, 0)$; $1/|x|$ is harmonic there, so "
                          r"$S$ has no drift: a local martingale", 4.6, 20, GREY_A),
            MathTex(r"\mathbb{E}[S_T] = 2\Phi(1/\sqrt{T}) - 1 < 1 = S_0", font_size=30, color=Q_C),
            MathTex(rf"T = 1:\ \text{{simulated }} {b['1.0']['mc']:.4f},\ \text{{exact }} {b['1.0']['exact']:.4f}",
                    font_size=26, color=Q_C),
            MathTex(rf"T = 4:\ \text{{simulated }} {b['4.0']['mc']:.4f},\ \text{{exact }} {b['4.0']['exact']:.4f}",
                    font_size=26, color=Q_C),
            MathTex(r"C - P = \mathbb{E}[S_T] - K \ne S_0 - K", font_size=30, color=ARB),
            wrapped_label(r"a strict local martingale satisfies NFLVR, yet the asset is worth more than its "
                          r"discounted payoff: a bubble, and put--call parity fails (Cox and Hobson 2005)", 4.6, 19, ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "One strange object lives inside it. Let a price be one over the distance of a "
            "three-dimensional Brownian motion from the origin: locally a fair game, no drift. "
            "<bookmark mark='a'/> But the mean sinks, as a few paths spike near the origin: at time "
            f"one, {b['1.0']['exact']:.3f} exactly, {b['1.0']['mc']:.4f} from two million paths. A "
            "strict local martingale. <bookmark mark='b'/> No free lunch, yet the asset trades above "
            "its expected value: a bubble, and parity fails. Cox and Hobson priced such options in "
            "2005."
            f" At time four the mean has sunk to {b['4.0']['exact']:.3f}."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(p_) for p_ in fan], lag_ratio=0.01), run_time=3)
            vo.wait_until("a")
            self.play(Create(mc), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"The doubler never loses at the end and costs nothing to start. Why is it not an arbitrage in "
                        r"the theorem's sense?")
        with self.voiceover(
            "Pause and predict. The doubler costs nothing and never loses at the end. Why is it not "
            "an arbitrage? <bookmark mark='a'/> It is not admissible: it needs unlimited credit on "
            "the way, and with bounded losses it is no longer sure to win."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"it is not admissible: its interim losses are unbounded; with a floor "
                                                r"at $-a$ it is no longer sure to win")))
        self.wait(0.4)
        self.clear_scene()
