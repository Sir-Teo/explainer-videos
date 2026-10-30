from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import (DATA, DRIFT, MODEL, NOISE, PART, SCORE, WALK, curve, follow, hist_shape, load,
                                   normal_pdf, ramp, swarm)

K = 1.3  # the letters' plane, drawn 1.3 times life size (as in the hook)


class FokkerPlanck(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.fokker_planck()
        self.stationary()
        self.reverse()

    def card(self):
        card = chapter_card(17, r"The density's own law", r"What happens to a whole cloud of random paths?", lit=(2015,),
                            part=PART)
        with self.voiceover("Chapter seventeen. The Fokker-Planck equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"p": MODEL}
        rows = [
            cmath(r"d\varphi(X)", "=", r"\big(\varphi' f + \tfrac12 g^2 \varphi''\big)\,dt + \varphi' g\,dW", font_size=32),
            cmath(r"\frac{d}{dt}\,\mathbb{E}[\varphi(X_t)]", "=", r"\mathbb{E}\big[\varphi' f + \tfrac12 g^2 \varphi''\big]",
                  font_size=32),
            cmath(r"\int \varphi\, \frac{\partial p}{\partial t}\, dx", "=",
                  r"\int \big(\varphi' f + \tfrac12 g^2 \varphi''\big)\, p\, dx", font_size=32),
            cmath(r"\int \varphi\, \frac{\partial p}{\partial t}\, dx", "=", r"\int \varphi\, \Big(-\frac{\partial (f p)}"
                  r"{\partial x} + \tfrac12 \frac{\partial^2 (g^2 p)}{\partial x^2}\Big) dx", font_size=32),
            cmath(r"\frac{\partial p}{\partial t}", "=", r"-\frac{\partial (f p)}{\partial x} + \tfrac12 "
                  r"\frac{\partial^2 (g^2 p)}{\partial x^2}", font_size=36,
                  colors={r"-\frac{\partial (f p)}{\partial x} + \tfrac12 \frac{\partial^2 (g^2 p)}{\partial x^2}": MODEL}),
        ]
        whys = [why(r"It\^o's lemma \ (Chapter 15), \ for $dX = f\,dt + g\,dW$"), why(r"the $dW$ term averages to zero"),
                why(r"an average is an integral against $p$"), why(r"integrate by parts, \ once and twice"),
                why(r"true for every $\varphi$")]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-1.6, buff=0.4, edge=6.8)
        cite_ = cite(r"A.~Fokker (1914); \ M.~Planck (1917); \ A.~Kolmogorov (1931)", corner=DR)
        with self.voiceover(
            "Chapter fourteen found the heat equation for a cloud of pure noise. With a push added, here is the "
            "general law, from Ito's lemma. <bookmark mark='a'/> Take any smooth test function phi of a process with "
            "drift f and noise g. <bookmark mark='b'/> Average: the random term has mean zero. <bookmark mark='c'/> "
            "Write the averages as integrals against the density p. <bookmark mark='d'/> Integrate by parts to move "
            "the derivatives from phi onto p. <bookmark mark='e'/> Since this holds for every phi, the integrands "
            "agree: the Fokker-Planck equation, a deterministic law for the density. Adriaan Fokker and Max Planck "
            "wrote it for molecules; Kolmogorov derived it in general in 1931."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stationary(self):
        d = load("langevin")
        rows = [
            cmath(r"f = (\log \pi)' = \frac{\pi'}{\pi},", r"\quad", r"g^2 = 2", font_size=36),
            cmath(r"\frac{\partial p}{\partial t}", "=", r"-\frac{\partial}{\partial x}\Big(\frac{\pi'}{\pi}\, p\Big) + "
                  r"\frac{\partial^2 p}{\partial x^2}", font_size=36),
            cmath(r"p = \pi:", r"\quad", r"-\pi'' + \pi'' = 0", font_size=36, colors={r"-\pi'' + \pi'' = 0": SCORE}),
        ]
        whys = [why(r"Langevin dynamics \ (Chapter 13)"), why(r"Fokker--Planck"), why(r"$\pi$ does not move: \ stationary")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.55, edge=6.8, align_index=None)
        l1 = np.asarray(d["l1"])
        res = label(rf"Chapter 13's particles: \ distance from $p$ falling from ${l1[0]:.2f}$ to ${l1[-1]:.2f}$", font_size=26,
                    color=WALK).to_edge(DOWN, buff=0.3)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.25], x_length=8.0, y_length=1.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -2.0, 0])
        xs = np.linspace(-4, 4, 300)
        pi_ = 0.45 * normal_pdf(xs, -1.5, 0.6) + 0.55 * normal_pdf(xs, 1.3, 0.7)
        pic = VGroup(ax, curve(ax, xs, pi_, color=SCORE, stroke_width=3.5),
                     label(r"$\pi$: \ the drift pushes up its slopes, \ the noise spreads it out: \ they balance", font_size=20,
                           color=GREY_A).next_to(ax, UP, buff=0.05))
        for x0 in np.linspace(-3.6, 3.6, 13):
            sc = float(np.interp(x0, xs[1:-1], np.diff(np.log(pi_))[1:] / (xs[1] - xs[0])))
            L = 0.45 * math.tanh(sc / 3)
            if abs(L) > 0.05:
                b0 = ax.c2p(x0, 0) + DOWN * 0.15
                pic.add(Arrow(b0, b0 + RIGHT * L, buff=0, color=SCORE, stroke_width=3, max_tip_length_to_length_ratio=0.4))
        with self.voiceover(
            "Now the promise from chapter thirteen. Langevin dynamics has drift the score of a target pi, and noise "
            "of variance two. <bookmark mark='a'/> Put that into Fokker-Planck. <bookmark mark='b'/> If the density "
            "is pi, the drift term gives minus pi double prime, the noise term plus pi double prime, and they "
            "cancel: pi never moves. That is why the particles of chapter thirteen settled onto the bumps, and why "
            "Langevin dynamics samples anything whose score we know."
        ) as vo:
            self.play(FadeIn(pic))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fokker_planck(self):
        d = load("diffusion")
        xs, fp, hist = np.asarray(d["xs"]), np.asarray(d["fp"]), np.asarray(d["fp_hist"])
        fp_ts = [float(t) for t in d["fp_ts"]]
        assert max(d["fp_err"]) < 0.01 and max(d["hist_err"]) < 0.08
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.6, 0.2], x_length=10.0, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -1.2, 0])
        edges = np.linspace(-4, 4, 81)
        hs = [hist_shape(ax, edges, np.minimum(h, 0.6), color=DATA, opacity=0.4, stroke_width=0) for h in hist]
        cs = [curve(ax, xs, np.minimum(p, 0.6), color=MODEL, stroke_width=4) for p in fp]
        tv = DecimalNumber(0, num_decimal_places=2, font_size=36, color=C.BITS)
        tl = VGroup(MathTex(r"t =", font_size=36), tv).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.5).shift(DOWN * 1.6)
        colors = {r"p": MODEL, r"f": DRIFT, r"g^2": NOISE}
        fpe = cmath(r"\frac{\partial p}{\partial t}", "=", r"-\frac{\partial}{\partial x}\big(", r"f", r"\,", r"p",
                    r"\big)", "+", r"\tfrac12", r"g^2", r"\frac{\partial^2 p}{\partial x^2}", colors=colors, font_size=42)
        fpe.to_edge(UP, buff=0.45)
        fpn = label(r"the Fokker--Planck equation: \ the density's own law, \ no randomness left", font_size=26,
                    color=GREY_A).next_to(fpe, DOWN, buff=0.25)
        legend = VGroup(label(r"$20{,}000$ random particles", font_size=24, color=DATA),
                        label(r"the equation's solution", font_size=24, color=MODEL))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.5).shift(DOWN * 1.6)
        end = label(r"all that's left: \ a standard bell", font_size=28, color=WHITE).next_to(ax, DOWN, buff=0.3)
        with self.voiceover(
            "Check it on the Ornstein-Uhlenbeck process. <bookmark mark='a'/> Start with data that has two peaks, and "
            "let every point drift toward zero and jiggle. <bookmark mark='b'/> Twenty thousand particles and the "
            f"equation solved on a grid move together: the histograms stay within {max(d['hist_err']):.3f} of the "
            f"solution, and the solution within {max(d['fp_err']):.4f} of the exact answer. <bookmark mark='c'/> Wait "
            "long enough, and every trace of the data is gone: a plain standard bell. That's what a diffusion model "
            "does to its training images."
        ) as vo:
            self.play(Write(fpe), FadeIn(fpn))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(hs[0]), Create(cs[0]), FadeIn(tl), FadeIn(legend))
            vo.wait_until("b")
            h, c = hs[0], cs[0]
            for k in range(1, len(fp_ts) - 1):
                self.play(Transform(h, hs[k]), Transform(c, cs[k]), ChangeDecimalToValue(tv, fp_ts[k]), run_time=1.6)
            vo.wait_until("c")
            self.play(Transform(h, hs[-1]), Transform(c, cs[-1]), ChangeDecimalToValue(tv, fp_ts[-1]), run_time=2.0)
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reverse(self):
        d = load("diffusion")
        xs, dens, scores, alphas = (np.asarray(d[k]) for k in ("xs", "dens", "scores", "alphas"))
        colors = {r"f(x)": DRIFT, r"\nabla \log p_t(x)": SCORE, r"g\,d\bar W_t": NOISE, r"g^2": NOISE}
        rev = cmath(r"dx", "=", r"\big[", r"f(x)", "-", r"g^2", r"\nabla \log p_t(x)", r"\big]\,dt", "+",
                    r"g\,d\bar W_t", colors=colors, font_size=44).to_edge(UP, buff=0.4)
        rn = label(r"time running backwards \ (Anderson, 1982)", font_size=24, color=GREY_A).next_to(rev, DOWN, buff=0.85)
        sb = brace_note(term(rev, r"\nabla \log p_t(x)"), r"the score", color=SCORE, font_size=28)
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.6, 0.2], x_length=10.0, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -1.0, 0])
        k = 2  # alpha = 0.5: halfway to noise
        assert abs(alphas[k] - 0.5) < 1e-9
        dc = curve(ax, xs, dens[k], color=DATA, stroke_width=4)
        arrows = VGroup()
        for x in np.linspace(-3.6, 3.6, 25):
            s = float(np.interp(x, xs, scores[k]))
            L = 0.55 * math.tanh(s / 2.5)
            base = ax.c2p(x, 0) + DOWN * 0.45
            if abs(L) > 0.04:
                arrows.add(Arrow(base, base + RIGHT * L, buff=0, color=SCORE, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.4))
        al = label(r"the score points uphill: \ toward where data is likelier", font_size=26, color=SCORE)
        al.next_to(ax, DOWN, buff=0.6)
        with self.voiceover(
            "Can the film run backwards, from the bell to the data? In 1982 Brian Anderson showed that, reversed in "
            "time, it is another stochastic differential equation, with one extra term: <bookmark mark='a'/> the "
            "score, the slope of the log of the density at that moment, an arrow saying which way the data gets "
            "likelier. <bookmark mark='b'/> It points uphill, toward the data."
        ) as vo:
            self.play(Write(rev), FadeIn(rn), Create(ax), Create(dc))
            vo.wait_until("a")
            self.play(FadeIn(sb))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.04), FadeIn(al), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()
        # the letters again: the score field in the plane, and the reverse flow
        s = load("shape")
        G = np.asarray(s["grid"])
        F = np.asarray(s["field0.5"])
        bwd = np.asarray(s["bwd"])
        field = VGroup()
        mag = np.linalg.norm(F, axis=1) + 1e-9
        ref = np.percentile(mag, 90)
        for p, v, m in zip(G * K, F, mag):
            L = 0.42 * min(1.0, m / ref)
            field.add(Arrow([p[0], p[1], 0], [p[0] + L * v[0] / m, p[1] + L * v[1] / m, 0], buff=0, color=SCORE,
                            stroke_width=2.5, max_tip_length_to_length_ratio=0.35, stroke_opacity=0.7))
        cols = ramp(bwd[-1][:, 0] + 0.35 * bwd[-1][:, 1], DATA, C.BITS)
        dots = swarm(bwd[0] * K, cols)
        # the slide from data into noise: the noised letters and their score, at three noise levels
        fwd, T = np.asarray(s["fwd"]), float(s["T"])

        def arrows_for(F_, opacity=0.9):
            m_ = np.linalg.norm(F_, axis=1) + 1e-9
            r_ = np.percentile(m_, 90)
            return VGroup(*[Arrow([p[0], p[1], 0], [p[0] + 0.42 * min(1.0, mm / r_) * v[0] / mm,
                                                     p[1] + 0.42 * min(1.0, mm / r_) * v[1] / mm, 0], buff=0,
                                  color=SCORE, stroke_width=3, max_tip_length_to_length_ratio=0.35,
                                  stroke_opacity=opacity) for p, v, mm in zip(G * K, F_, m_)])

        levels = (0.1, 0.5, 2.0)
        panels = VGroup()
        for lv in levels:
            k_ = int(round(lv / T * (len(fwd) - 1)))
            assert abs(k_ * T / (len(fwd) - 1) - lv) < 1e-9
            P_ = fwd[k_][(np.abs(fwd[k_][:, 0]) < 3.4) & (np.abs(fwd[k_][:, 1]) < 2.0)]  # those inside the frame
            pts = swarm(P_ * K, [DATA] * len(P_), radius=0.05, opacity=0.8)
            box = Rectangle(width=2 * 3.4 * K, height=2 * 2.0 * K, stroke_color=GREY_D, stroke_width=2)
            panels.add(VGroup(box, pts, arrows_for(np.asarray(s[f"field{lv}"]))))
        panels.scale(0.37).arrange(RIGHT, buff=0.4).move_to(UP * 0.5)
        p_lab = VGroup(*[label(rf"$t = {lv:g}$", font_size=26, color=GREY_A).next_to(pn, DOWN, buff=0.15)
                         for lv, pn in zip(levels, panels)])
        y_s = p_lab.get_bottom()[1] - 0.35
        slide = Arrow([panels.get_left()[0], y_s, 0], [panels.get_right()[0], y_s, 0], buff=0, color=NOISE,
                      stroke_width=3, max_tip_length_to_length_ratio=0.03)
        s_lab = VGroup(label(r"data", font_size=24, color=DATA).next_to(slide, DOWN, buff=0.12).align_to(slide, LEFT),
                       label(r"noise", font_size=24, color=NOISE).next_to(slide, DOWN, buff=0.12).align_to(slide, RIGHT))
        p_head = label(r"the score, \ at every noise level", font_size=30, color=SCORE).next_to(panels, UP, buff=0.4)
        t = ValueTracker(0.0)
        cap = label(r"the score of the noised letters, \ halfway to noise", font_size=26, color=SCORE).to_edge(DOWN, buff=0.3)
        nxt = label(r"Part 21: \ a network learns the score from millions of images", font_size=28, color=C.BITS)
        nxt.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Know the score at every noise level, every point on the slide from data into noise, and you can turn "
            "noise into data. <bookmark mark='a'/> It's the "
            "field of arrows from the start of this part. <bookmark mark='b'/> There, it was computed exactly from "
            "the letters. A diffusion model learns it from millions of images, with a network, and that's part "
            "twenty-one."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(pn) for pn in panels], lag_ratio=0.25), FadeIn(p_lab), FadeIn(p_head),
                      run_time=1.5)
            self.play(GrowArrow(slide), FadeIn(s_lab))
            vo.wait_until("a")
            mid = panels[1][2]
            self.play(FadeOut(VGroup(panels[0], panels[2], panels[1][:2], p_lab, p_head, slide, s_lab)),
                      ReplacementTransform(mid, field), FadeIn(cap), run_time=1.5)
            self.play(FadeIn(dots))
            dots.add_updater(follow(dots, bwd, t, scale=K))
            vo.wait_until("b")
            self.play(t.animate.set_value(len(bwd) - 1), field.animate.set_opacity(0.15), FadeOut(cap), FadeIn(nxt),
                      run_time=5.0, rate_func=lambda a: 1 - (1 - a) ** 2.2)
            dots.clear_updaters()
        self.wait(0.5)
        self.clear_scene()
