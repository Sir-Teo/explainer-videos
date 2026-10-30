from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import (DATA, PART, SCORE, WALK, ParticleFlow, curve, heat_image, load,
                                   surface_from_grid)
from videos.ai.ai5.compute import density2, rng

ACCEPT, REJECT = "#5BD17A", C.SURPRISE


class MCMC(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.walk()
        self.derive()
        self.langevin()
        self.mixing()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(13, r"Sampling the unsampleable", r"How do you draw from a shape you can only evaluate?",
                            part=PART, lit=(1953,))
        with self.voiceover("Chapter thirteen. Markov chain Monte Carlo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def walk(self):
        d = load("mcmc")
        chain = np.asarray(d["chain"])
        # replay the first steps exactly as compute.py drew them, keeping the proposals too
        g = rng(1953)
        x, steps = np.array([-3.0, 2.0]), []
        for _ in range(16):
            y = x + g.normal(scale=0.7, size=2)
            ok = g.random() < density2(*y) / density2(*x)
            steps.append((x.copy(), y.copy(), bool(ok)))
            x = y if ok else x
        assert np.allclose(x, chain[16])
        ax = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8.0, y_length=6.0, tips=False,
                  axis_config={"stroke_width": 0}).move_to([-2.4, -0.3, 0])
        img = heat_image(density2, (-4, 4), (-3, 3))
        img.stretch_to_fit_width(8.0).stretch_to_fit_height(6.0).move_to(ax)
        frame_ = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        cont = contour_lines(ax, density2, (-4, 4), (-3, 3), [0.1, 0.3, 0.5, 0.7, 0.9], n=(120, 90), stroke_width=1.2)
        cont.set_stroke(opacity=0.55)
        walker = glow_dot(ax.c2p(*steps[0][0]), color=WHITE, radius=0.1)
        trail = VGroup()
        # the rule
        colors = {r"p(\text{new})": ACCEPT, r"p(\text{now})": DATA}
        f = cmath(r"\text{accept with probability}", font_size=30)
        f2 = cmath(r"\min\Big(1,\;", r"\frac{p(\text{new})}{p(\text{now})}", r"\Big)", colors=colors, font_size=42)
        rule = VGroup(f, f2).arrange(DOWN, buff=0.2).move_to([4.6, 2.2, 0])
        steps_t = VGroup(label(r"1. \ propose a small random step", font_size=26),
                         label(r"2. \ uphill: \ always take it", font_size=26, color=ACCEPT),
                         label(r"3. \ downhill: \ only sometimes", font_size=26, color=REJECT))
        steps_t.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rule, DOWN, buff=0.45)
        cancel = label(r"only a ratio: \ the unknown total cancels", font_size=26, color=C.BITS)
        cancel.next_to(steps_t, DOWN, buff=0.45)
        tag = label(r"a density known only up to a constant", font_size=24, color=GREY_A).next_to(img, DOWN, buff=0.15)
        tag.align_to(img, LEFT)  # flush left under the picture, clear of the citation in the corner
        cite_ = cite(r"N.~Metropolis, A.~Rosenbluth, M.~Rosenbluth, A.~Teller \& E.~Teller (1953)", corner=DR)
        hc53 = history_card(1953, r"Metropolis, \ the Rosenbluths, \ the Tellers", r"Los Alamos, \ on the MANIAC: \ "
                            r"sample a shape by a random walk that accepts or rejects each step", width=4.4).move_to([4.6, 0.6, 0])
        with self.voiceover(
            "Often there's no direct way to draw samples: all we can do is evaluate how likely each point is, and "
            "only up to an unknown constant, as with Bayes's rule. <bookmark mark='a'/> Here's a density with two "
            "bumps. In 1953 at Los Alamos, Nicholas Metropolis, Arianna and Marshall Rosenbluth, and Augusta and "
            "Edward Teller, computing on the MANIAC, found a way to sample anything like it: take a random walk. "
            "<bookmark mark='b'/> Propose a small random step. If it goes uphill, take it. <bookmark mark='c'/> If "
            "downhill, take it with probability the ratio of the heights; otherwise stay put."
        ) as vo:
            self.play(FadeIn(img), Create(frame_), Create(cont), FadeIn(tag), run_time=1.5)
            self.play(FadeIn(hc53, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(walker), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeOut(hc53), FadeIn(steps_t[0]), FadeIn(steps_t[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps_t[2]), Write(rule))
            for k, (x0, y0, ok) in enumerate(steps):
                rt = 0.55 if k < 6 else 0.3
                arr = Arrow(ax.c2p(*x0), ax.c2p(*y0), buff=0.08, color=ACCEPT if ok else REJECT, stroke_width=3,
                            max_tip_length_to_length_ratio=0.25)
                self.play(GrowArrow(arr), run_time=rt)
                if ok:
                    trail.add(Line(ax.c2p(*x0), ax.c2p(*y0), color=WALK, stroke_width=2, stroke_opacity=0.6))
                    self.play(walker.animate.move_to(ax.c2p(*y0)), FadeOut(arr), FadeIn(trail[-1]), run_time=rt)
                else:
                    self.play(FadeOut(arr, scale=0.6), Indicate(walker, color=REJECT, scale_factor=1.3), run_time=rt)
        # many steps: the visits pile up like the density
        pts = chain[17::3]
        visits = VGroup(*[Dot(ax.c2p(*p), radius=0.028, color=WHITE, fill_opacity=0.75) for p in pts])
        assert abs(float(d["left"]) - 2 / 3) < 0.05
        # a running count, as the walk goes: the share of the visits drawn so far that are in the left bump
        in_left = np.cumsum(pts[:, 0] < 0) / np.arange(1, len(pts) + 1)
        left = float(in_left[-1])
        assert abs(left - 2 / 3) < 0.05
        share = label(rf"time in the left bump: \ ${100 * left:.0f}\%$ \\ its share of the density: \ $67\%$",
                      font_size=24, color=WHITE)
        share.next_to(cancel, DOWN, buff=0.4).align_to(cancel, LEFT)
        j = ValueTracker(0)
        run_v = DecimalNumber(100 * in_left[0], num_decimal_places=0, unit=r"\%", font_size=30, color=WALK)
        run_l = label(r"time in the left bump, so far:", font_size=24, color=WALK)
        running = VGroup(run_l, run_v).arrange(RIGHT, buff=0.15)
        running.next_to(cancel, DOWN, buff=0.4).align_to(cancel, LEFT)
        keep_in_frame(running)
        with self.voiceover(
            "Only the ratio appears, so the unknown constant cancels. <bookmark mark='a'/> Keep walking: the visits "
            "pile up like the density, because this Markov chain's stationary distribution is the one we wanted. "
            "<bookmark mark='b'/> The left bump holds two thirds of the probability, and the walker spends "
            f"{100 * left:.0f} percent of its time there. This made Bayesian statistics practical in the 1990s, and "
            "physicists still sample molecules this way."
        ) as vo:
            self.play(FadeIn(cancel))
            vo.wait_until("a")
            self.play(FadeIn(running), run_time=0.4)
            run_v.add_updater(lambda m: m.set_value(100 * in_left[min(int(j.get_value()), len(pts) - 1)]))
            self.play(FadeOut(trail), FadeOut(tag),
                      LaggedStart(*[FadeIn(v) for v in visits], lag_ratio=0.0015),
                      MoveAlongPath(walker, VMobject().set_points_as_corners([ax.c2p(*p) for p in chain[17::3]])),
                      j.animate.set_value(len(pts) - 1), run_time=7.0, rate_func=linear)
            run_v.clear_updaters()
            vo.wait_until("b")
            self.play(FadeTransform(running, share))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\pi(x)": DATA, r"\pi(y)": ACCEPT, r"a": C.BITS}
        rows = [
            cmath(r"\pi(x)\, q(y \mid x)\, a(x \to y)", "=", r"\pi(y)\, q(x \mid y)\, a(y \to x)", font_size=34),
            cmath(r"\frac{a(x \to y)}{a(y \to x)}", "=", r"\frac{\pi(y)\, q(x \mid y)}{\pi(x)\, q(y \mid x)}", font_size=34),
            cmath(r"a(x \to y)", "=", r"\min\!\Big(1,\; \frac{\pi(y)\, q(x \mid y)}{\pi(x)\, q(y \mid x)}\Big)", font_size=34),
            cmath(r"a(x \to y)", "=", r"\min\!\Big(1,\; \frac{\pi(y)}{\pi(x)}\Big)", font_size=34),
        ]
        whys = [why(r"detailed balance \ (Chapter 10): \ propose, then accept"),
                why(r"rearrange"),
                why(r"the largest acceptance that keeps it: \ Hastings (1970)"),
                why(r"symmetric proposals: \ Metropolis (1953)")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=0.6, buff=0.45, edge=6.8)
        img = heat_image(density2, (-4, 4), (-3, 3), w=200, h=150)
        img.stretch_to_fit_width(4.0).stretch_to_fit_height(3.0).to_corner(DL, buff=0.35)
        bx = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=4.0, y_length=3.0, tips=False,
                  axis_config={"stroke_width": 0}).move_to(img)
        px, py = bx.c2p(-1.6, -0.6), bx.c2p(1.5, 0.9)
        pic = Group(img, Dot(px, color=DATA, radius=0.08), Dot(py, color=ACCEPT, radius=0.08),
                    MathTex("x", font_size=30, color=DATA).next_to(px, DOWN, buff=0.1),
                    MathTex("y", font_size=30, color=ACCEPT).next_to(py, UP, buff=0.1),
                    CurvedArrow(px + RIGHT * 0.1, py + LEFT * 0.1, angle=-0.6, color=DATA, stroke_width=3, tip_length=0.15),
                    CurvedArrow(py + DOWN * 0.1, px + DOWN * 0.05 + RIGHT * 0.1, angle=-0.6, color=ACCEPT, stroke_width=3,
                                tip_length=0.15),
                    label(r"flows both ways must match", font_size=20, color=GREY_A).next_to(img, UP, buff=0.08))
        with self.voiceover(
            "Why does it work? Chapter ten's detailed balance. A step from x to y is proposed with probability q, "
            "then accepted with probability a. <bookmark mark='a'/> Balance asks that the flows match, <bookmark "
            "mark='b'/> which fixes only the ratio of the acceptances. <bookmark mark='c'/> Make the larger one equal "
            "to one: W. K. Hastings's rule of 1970, for any proposal. <bookmark mark='d'/> With a symmetric proposal "
            "the q's cancel, and it is Metropolis's rule."
        ) as vo:
            self.play(FadeIn(pic))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def langevin(self):
        d = load("langevin")
        frames, grids = np.asarray(d["frames"]), np.asarray(d["grids"])
        gx, gy, target = np.asarray(d["gx"]), np.asarray(d["gy"]), np.asarray(d["target"])
        gt, l1 = np.asarray(d["grid_t"]), np.asarray(d["l1"])
        steps_at = [int(v) for v in d["grid_steps"]]
        left = float(d["flow_left"])
        h = float(d["flow_h"])
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], z_range=[0, 0.32, 0.1], x_length=8.0, y_length=6.0,
                          z_length=2.6, axis_config={"stroke_color": GREY_D, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.3)
        zmax = 0.3
        surfs = [surface_from_grid(axes, gx, gy, np.minimum(G, 0.32), zmax, opacity=0.62) for G in grids]
        wire = surface_from_grid(axes, gx, gy, target, zmax, opacity=0.0)
        wire.set_stroke(color=GREY_A, width=0.6, opacity=0.35)
        floor = Rectangle(width=8.0, height=6.0, stroke_color=GREY_D, stroke_width=1.5, fill_color="#0B0F17",
                          fill_opacity=0.6).move_to(axes.c2p(0, 0, 0))
        flow = ParticleFlow(axes, frames, colors=[WALK] * frames.shape[1], radius=0.028)
        eq = cmath(r"dx", "=", r"\nabla \log p(x)\,dt", "+", r"\sqrt{2}\,dW_t", font_size=36,
                   colors={r"\nabla \log p(x)\,dt": SCORE}).to_corner(UL, buff=0.35)
        ula = cmath(r"x \leftarrow x + h\, \nabla \log p(x) + \sqrt{2h}\,\xi", font_size=28).next_to(eq, DOWN, buff=0.2).align_to(eq, LEFT)
        lab = label(r"the push: \ the score, \ uphill toward likelier places; \\ the kicks: \ Brownian", font_size=20,
                    color=GREY_A).next_to(ula, DOWN, buff=0.15).align_to(eq, LEFT)
        # readouts, one per saved density (fixed-in-frame mobjects must not be rebuilt by number animations)
        reads = []
        for k in range(len(gt)):
            r_ = VGroup(MathTex(rf"t = {gt[k]:.1f}", font_size=30, color=C.BITS),
                        label(rf"distance from $p$ \ ($L^1$): \ ${l1[k]:.2f}$", font_size=22, color=GREY_A))
            r_.arrange(DOWN, aligned_edge=RIGHT, buff=0.12).to_corner(UR, buff=0.4)
            reads.append(r_)
        tl, ll = reads[0], VectorizedPoint()
        key = label(r"surface: \ the particles' density; \ mesh: \ the target $p$", font_size=20, color=GREY_A)
        key.next_to(reads[0], DOWN, buff=0.12).align_to(reads[0], RIGHT)
        hc = cite(r"P.~Langevin (1908); \ G.~Roberts \& R.~Tweedie (1996); \ M.~Welling \& Y.~W.~Teh (2011)", corner=DL)
        fixed = [eq, ula, lab, key, hc] + reads
        for m in fixed:
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-62 * DEGREES, zoom=0.78)
        n_frames = len(frames) - 1
        frame_of = [s / 5 for s in steps_at]  # frames are saved every 5 steps
        good = left > 0.6
        verdict = (f"{100 * left:.0f} percent of the particles are in the left bump, close to its two thirds."
                   if good else f"{100 * left:.0f} percent are in the left bump, short of its two thirds: some are "
                   "still on the wrong side of the valley.")
        with self.voiceover(
            "There is another way to explore, from physics. In 1908 Paul Langevin wrote a particle's motion in a "
            "fluid as a push plus random kicks. <bookmark mark='a'/> Make the push the score, the slope of log p, "
            "uphill toward likelier places, and the kicks Brownian; in small steps it is one line of code. <bookmark "
            "mark='b'/> Fifteen hundred particles start as noise; above them, their density. <bookmark mark='c'/> It "
            f"flows onto the two bumps, and its distance from the target falls from {l1[0]:.2f} to {l1[-1]:.2f}, about "
            f"as low as smoothing allows. {verdict} <bookmark mark='d'/> Its long-run distribution is p itself, as "
            "chapter seventeen proves. With mini-batch scores it sampled neural networks' weights in 2011, and with "
            "learned scores, the first score-based image models."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(hc), Create(axes), FadeIn(floor), FadeIn(flow), FadeIn(surfs[0]), FadeIn(tl),
                      FadeIn(key), Create(wire), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(ula), FadeIn(lab))
            vo.wait_until("b")
            self.begin_ambient_camera_rotation(rate=0.05)
            flow.start()
            vo.wait_until("c")
            cur = surfs[0]
            for k in range(1, len(surfs)):
                self.remove(reads[k - 1])
                self.add(reads[k])
                self.play(flow.t.animate.set_value(frame_of[k]), Transform(cur, surfs[k]), run_time=1.6, rate_func=linear)
            vo.wait_until("d")
        flow.stop()
        self.stop_ambient_camera_rotation()
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def mixing(self):
        d = load("langevin")
        cfg = [str(c) for c in d["configs"]]
        names = {"rwm0.7": r"random-walk Metropolis", "ula0.05": r"Langevin, \ small step", "ula0.3": r"Langevin, \ big step",
                 "mala0.3": r"Langevin $+$ Metropolis \ (MALA)"}
        cols = {"rwm0.7": ACCEPT, "ula0.05": WALK, "ula0.3": REJECT, "mala0.3": C.BITS}
        traces = VGroup()
        for i, c in enumerate(cfg):
            ch = np.asarray(d[f"{c}_chain"])
            ax = Axes(x_range=[0, len(ch), 250], y_range=[-3.5, 3.5, 3.5], x_length=5.4, y_length=1.15, tips=False,
                      axis_config={"stroke_color": GREY_D, "include_ticks": False})
            ln = curve(ax, np.arange(len(ch)), np.clip(ch[:, 0], -3.5, 3.5), color=cols[c], stroke_width=1.6)
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(len(ch), 0), color=GREY_D, stroke_width=1)
            nm = label(names[c], font_size=20, color=cols[c]).next_to(ax, LEFT, buff=0.15)
            traces.add(VGroup(ax, zero, ln, nm))
        traces.arrange(DOWN, buff=0.22, aligned_edge=RIGHT).move_to([-1.6, -0.3, 0])
        tt = label(r"$x$-coordinate over the first $4{,}000$ steps \ (left bump below the dashes)", font_size=20,
                   color=GREY_A).next_to(traces, UP, buff=0.15)

        def stat(c, k):
            v = np.asarray(d[f"{c}_{k}"], float)
            return float(v.mean())

        rows = VGroup(label(r"hops", font_size=20, color=GREY_A), label(r"spread", font_size=20, color=GREY_A))
        rows.arrange(RIGHT, buff=0.55)
        tbl = VGroup()
        for c in cfg:
            tbl.add(VGroup(MathTex(f"{stat(c, 'hops'):.0f}", font_size=26, color=cols[c]),
                           MathTex(f"{stat(c, 'spread'):.2f}", font_size=26, color=cols[c])).arrange(RIGHT, buff=0.6))
        for r, tr in zip(tbl, traces):
            r.move_to([4.6, tr.get_y(), 0])
        rows.next_to(tbl, UP, buff=0.25).set_x(4.6)
        truth = label(r"true spread: \ $0.35$", font_size=20, color=WHITE).next_to(tbl, DOWN, buff=0.2).set_x(4.6)
        tag = note(r"hops between the bumps in $19{,}000$ steps, \ and the spread within the left bump: \ means of five "
                   r"seeds").to_edge(DOWN, buff=0.2)
        h = {c: stat(c, "hops") for c in cfg}
        sp = {c: stat(c, "spread") for c in cfg}
        best_hops = max(cfg, key=lambda c: h[c])
        biased = abs(sp["ula0.3"] - 0.35) > 0.08
        v1 = (f"The big-step Langevin hops between the bumps most, {h['ula0.3']:.0f} times, but its spread is "
              f"{sp['ula0.3']:.2f} where the truth is 0.35: without a correction, a big step blurs the target." if biased
              else f"The big-step Langevin hops {h['ula0.3']:.0f} times and keeps the spread at {sp['ula0.3']:.2f}.")
        v2 = (f"Adding the Metropolis correction removes the bias, {sp['mala0.3']:.2f}, but its proposals across the "
              f"valley are mostly refused: {h['mala0.3']:.0f} hops." if h["mala0.3"] < h["rwm0.7"] else
              f"Adding the Metropolis correction removes the bias, {sp['mala0.3']:.2f}, and hops {h['mala0.3']:.0f} times.")
        with self.voiceover(
            "How well do they mix? Run four samplers for twenty thousand steps each, five times, and follow one "
            f"coordinate. <bookmark mark='a'/> Plain Metropolis crosses between the bumps about {h['rwm0.7']:.0f} "
            f"times, with the right spread. Langevin with small steps crosses only {h['ula0.05']:.0f} times. "
            f"<bookmark mark='b'/> {v1} <bookmark mark='c'/> {v2} Every sampler trades exactness for speed, and "
            "two bumps far apart defeat them all; part twenty-one's way out is to sample a blurred version first."
        ) as vo:
            self.play(FadeIn(tt), LaggedStart(*[FadeIn(t) for t in traces], lag_ratio=0.2), FadeIn(rows), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tbl[0]), FadeIn(tbl[1]))
            vo.wait_until("b")
            self.play(FadeIn(tbl[2]), FadeIn(truth))
            vo.wait_until("c")
            self.play(FadeIn(tbl[3]))
        self.wait(0.3)
        self.clear_scene()
