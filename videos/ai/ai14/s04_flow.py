from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, FM_C, NOISE, RF_C, cloud, curve, load, move_cloud


class Flow(VoiceoverScene):
    def construct(self):
        self.card()
        self.straight()
        self.paths()
        self.reflow()
        self.average()
        self.onestep()

    def card(self):
        card = chapter_card(3, r"Flow matching", r"Why not go in a straight line?", part=14)
        with self.voiceover("Chapter three. Flow matching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def straight(self):
        g = np.random.default_rng(5)
        f = load("flow")
        data = np.asarray(f["fm100"])[:12]
        noise = g.normal(size=(12, 2))
        S = 0.85
        pairs = VGroup()
        for z, x in zip(noise, data):
            a, b = np.array([z[0] * S - 3.0, z[1] * S - 0.4, 0]), np.array([x[0] * S + 0.2, x[1] * S - 0.4, 0])
            pairs.add(VGroup(Dot(a, radius=0.05, color=NOISE), Dot(b, radius=0.05, color=DATA),
                             DashedLine(a, b, color=GREY_B, stroke_width=1.5, dash_length=0.06)))
        colors = {r"x_0": NOISE, r"x_1": DATA, r"v_\theta": FM_C}
        f1 = cmath(r"x_t", "=", r"(1-t)\,", r"x_0", "+", r"t\,", r"x_1", colors=colors, font_size=38)
        f2 = cmath(r"\mathcal{L}", "=", r"\big\|", r"v_\theta", r"(x_t, t)", "-", r"(", r"x_1", "-", r"x_0", r")", r"\big\|^2",
                   colors=colors, font_size=38)
        f3 = cmath(r"x", r"\;\leftarrow\;", r"x", "+", r"v_\theta", r"(x, t)\,\Delta t", colors=colors, font_size=38)
        fs = VGroup(f1, f2, f3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.2, 0.6, 0])
        l1 = label(r"pair a noise point with a data point", font_size=20, color=GREY_A).next_to(f1, DOWN, buff=0.08).align_to(f1, LEFT)
        l2 = label(r"learn the velocity of the straight line", font_size=20, color=GREY_A).next_to(f2, DOWN, buff=0.08).align_to(f2, LEFT)
        l3 = label(r"to sample: \ follow the learned velocity", font_size=20, color=FM_C).next_to(f3, DOWN, buff=0.08).align_to(f3, LEFT)
        cite_ = cite(r"Y.~Lipman et al., \textit{Flow Matching} (2023); \ X.~Liu et al., \textit{Rectified Flow} (2023)", corner=DR)
        with self.voiceover(
            "Flow matching asks for the simplest path there is. Pair a random noise point with a random data point "
            "and join them with a straight line. <bookmark mark='a'/> Train a network to output the velocity along "
            "that line: just the data point minus the noise point. <bookmark mark='b'/> To sample, start from noise "
            "and follow the learned velocity, a few steps at a time. It's the same idea as diffusion, with simpler "
            "bookkeeping, and it's what Stable Diffusion 3 and Flux are trained with."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), Write(f1), FadeIn(l1), FadeIn(cite_), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("b")
            self.play(Write(f3), FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        f = load("flow")
        P = np.asarray(f["fm_path"])
        S, sh = 0.75, np.array([-1.6, -0.5])
        n = 120
        trails = VGroup(*[VMobject(stroke_width=1.4, stroke_color=FM_C, stroke_opacity=0.7).set_points_smoothly(
            [[p[i, 0] * S + sh[0], p[i, 1] * S + sh[1], 0] for p in P[::5]]) for i in range(0, n, 3)])
        d = cloud(P[0][:n], NOISE, radius=0.03, scale=S, shift=sh)
        st = float(f["straight_fm"])
        note_ = label(r"each training line is straight, \\ but the learned paths bend: \\ "
                      r"a noise point could belong \\ to many data points", font_size=24, color=GREY_A).move_to([4.6, 0.8, 0])
        sl = label(rf"straightness: \ ${st:.3f}$ \\ ($1$ = a straight line)", font_size=24, color=FM_C).next_to(note_, DOWN, buff=0.4)
        with self.voiceover(
            "Here are the learned paths. <bookmark mark='a'/> Each training line was straight, but the paths bend. "
            "A noise point was paired with a different random data point every time, so the network learns the "
            "average direction, and averages of straight lines curve. <bookmark mark='b'/> Curved paths still need "
            "many steps."
        ) as vo:
            self.play(FadeIn(d))
            vo.wait_until("a")
            self.play(*move_cloud(d, P[-1][:n], S, sh), Create(trails), run_time=3.0)
            self.play(d.animate.set_color(DATA), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reflow(self):
        f = load("flow")
        ks = [int(k) for k in f["steps"]]
        fm = np.array([float(f[f"sw_fm{k}"]) for k in ks])
        rf = np.array([float(f[f"sw_rf{k}"]) for k in ks])
        lx = np.log10(ks)
        hi = max(fm.max(), rf.max()) * 1.1
        ystep = next(v for v in (0.05, 0.1, 0.2, 0.25, 0.5, 1.0) if v >= hi / 5)  # round tick values
        ax = Axes(x_range=[-0.1, 2.1, 0.5], y_range=[0, hi, ystep], x_length=6.4, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.0, -0.8, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(math.log10(k), 0), DOWN, buff=0.1) for k in ks])
        xn = label(r"sampling steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"distance from the real data", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(-0.1, v), LEFT, buff=0.08)
                      for v in np.arange(ystep, hi + 1e-9, ystep)])
        cf = VGroup(curve(ax, lx, fm, FM_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=FM_C) for a, b in zip(lx, fm)])
        cr = VGroup(curve(ax, lx, rf, RF_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=RF_C) for a, b in zip(lx, rf)])
        k1 = label(r"flow matching", font_size=24, color=FM_C).move_to([3.0, 2.4, 0])
        k2 = label(r"after reflow", font_size=24, color=RF_C).next_to(k1, DOWN, buff=0.2).align_to(k1, LEFT)
        S = 0.42
        one = VGroup(cloud(np.asarray(f["fm1"])[:400], FM_C, radius=0.018, scale=S),
                     cloud(np.asarray(f["rf1"])[:400], RF_C, radius=0.018, scale=S)).arrange(DOWN, buff=0.5).move_to([4.2, -1.0, 0])
        ol = VGroup(label(r"$1$ step", font_size=20, color=FM_C).next_to(one[0], LEFT, buff=0.15),
                    label(r"$1$ step", font_size=20, color=RF_C).next_to(one[1], LEFT, buff=0.15))
        s1, s2 = float(f["straight_fm"]), float(f["straight_rf"])
        with self.voiceover(
            "The fix is called reflow. Run the trained model to pair each noise point with the sample it actually "
            "leads to, and train a second model on those pairs. <bookmark mark='a'/> Now the pairs agree with each "
            f"other, and the paths straighten: from {s1:.3f} to {s2:.3f}. <bookmark mark='b'/> On a straight path, "
            "one big step lands where a hundred small ones would. Distilled this way, image models now make a "
            "picture in one to four steps."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(cf[0]), FadeIn(cf[1:]), FadeIn(k1))
            vo.wait_until("a")
            self.play(Create(cr[0]), FadeIn(cr[1:]), FadeIn(k2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(one), FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def average(self):
        f = load("flow")
        P = np.asarray(f["fm_path"])  # (steps + 1, particles, 2): the learned flow, 100 small steps
        n = len(P) - 1
        L = np.linalg.norm(np.diff(P, axis=0), axis=-1).sum(0)
        chord = np.linalg.norm(P[-1] - P[0], axis=-1)
        st = chord / np.maximum(L, 1e-9)
        cand = [i for i in np.argsort(st) if 2.0 < L[i] < 4.5]
        i = int(cand[0]) if cand else int(np.argmin(st))
        S, O = 1.1, np.array([-3.6, -0.7, 0])
        pts = [O + S * np.array([x, y, 0]) for x, y in P[:, i]]
        path = VMobject(color=FM_C, stroke_width=3.5).set_points_smoothly(pts[::2] + [pts[-1]])
        a, b = int(0.2 * n), int(0.85 * n)
        zs, zt = Dot(pts[a], radius=0.08, color=NOISE), Dot(pts[b], radius=0.08, color=DATA)
        zsl = MathTex(r"z_s", font_size=30, color=NOISE).next_to(zs, LEFT, buff=0.1)
        ztl = MathTex(r"z_t", font_size=30, color=DATA).next_to(zt, RIGHT, buff=0.1)
        tang = VGroup()
        for k in range(a, b + 1, max(1, (b - a) // 5)):
            d = pts[min(k + 1, n)] - pts[k]
            d = d / max(np.linalg.norm(d), 1e-9) * 0.55
            tang.add(Arrow(pts[k], pts[k] + d, buff=0, color=SCORE, stroke_width=3, max_tip_length_to_length_ratio=0.3))
        avg = Arrow(pts[a], pts[b], buff=0.08, color=C.SURPRISE, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        vl = label(r"$v$: \\ the velocity \\ at each moment", font_size=20, color=SCORE).next_to(tang, UP, buff=0.2)
        ul = label(r"$(t - s)\,u$: \\ one jump", font_size=20, color=C.SURPRISE).next_to(avg.get_center(), DOWN, buff=0.35)
        keep_in_frame(vl)
        colors = {r"u": C.SURPRISE, r"v": SCORE, r"z_s": NOISE, r"z_t": DATA}
        eqs = VGroup(
            cmath(r"u", r"(z_s, s, t) = \frac{1}{t - s}\int_s^t", r"v", r"(z_\tau, \tau)\, d\tau", colors=colors, font_size=32),
            cmath(r"z_t", r"=", r"z_s", r"+ (t - s)\,", r"u", r"(z_s, s, t)", colors=colors, font_size=32),
            cmath(r"u", r"=", r"v", r"+ (t - s)\, \frac{d}{ds}", r"u", colors=colors, font_size=32),
            cmath(r"\frac{d}{ds}", r"u", r"=", r"v", r"\cdot \nabla_z", r"u", r"+ \partial_s", r"u", colors=colors, font_size=32),
            cmath(r"\mathcal{L} = \big\|\,", r"u", r"_\theta - \operatorname{sg}\big(", r"v", r"+ (t - s)\tfrac{d}{ds}", r"u",
                  r"_\theta\big)\big\|^2", colors=colors, font_size=32),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([3.3, 0.15, 0])
        notes = VGroup(label(r"the average velocity from $s$ to $t$", font_size=18, color=GREY_A),
                       label(r"so one jump does it", font_size=18, color=GREY_A),
                       label(r"differentiate $(t-s)\,u = z_t - z_s$ in $s$", font_size=18, color=GREY_A),
                       label(r"one Jacobian-vector product", font_size=18, color=GREY_A),
                       label(r"sg: \ the target is held fixed", font_size=18, color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.06).align_to(e_, LEFT)
        for k in range(1, len(eqs)):
            eqs[k:].shift(DOWN * 0.2)
            notes[k:].shift(DOWN * 0.2)
        head = label(r"MeanFlow: \ learn the average velocity", font_size=26).to_edge(UP, buff=0.35)
        keep_in_frame(VGroup(eqs, notes))
        cite_ = cite(r"Z.~Geng et al., \textit{Mean Flows for One-step Generative Modeling} (2025)", corner=DR)
        with self.voiceover(
            "Reflow needs a second model and a second round of training. In 2025, MeanFlow found a more direct "
            "route. <bookmark mark='a'/> Here is one point's path under our flow model: it bends. Flow matching "
            "learns v, the velocity at each moment, so it has to take many small steps. <bookmark mark='b'/> "
            "MeanFlow learns u instead: the average velocity between two times s and t. <bookmark mark='c'/> With "
            "it, a single jump from s to t lands on the path, however much it bends. <bookmark mark='d'/> But we "
            "can't compute that integral to train on. The trick: write t minus s times u as z t minus z s, and "
            "differentiate in s. Out comes an identity: the average velocity is the velocity now, plus t minus s "
            "times how fast u changes along the path. <bookmark mark='e'/> And that rate of change costs one "
            "Jacobian-vector product, a single forward pass. <bookmark mark='f'/> So the network is trained to "
            "match the right-hand side, held fixed, with no integral and no teacher model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(path), run_time=2.0)
            self.play(FadeIn(zs), FadeIn(zsl), FadeIn(zt), FadeIn(ztl), LaggedStart(*[GrowArrow(t_) for t_ in tang], lag_ratio=0.15),
                      FadeIn(vl))
            vo.wait_until("b")
            self.play(Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(GrowArrow(avg), FadeIn(ul), Write(eqs[1]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(eqs[2]), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(Write(eqs[3]), FadeIn(notes[3]))
            vo.wait_until("f")
            self.play(Write(eqs[4]), FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def onestep(self):
        f, m = load("flow"), load("fewstep")
        S = 0.36
        sets = [("fm", r"flow matching", FM_C, np.asarray(f["fm1"]), float(f["sw_fm1"])),
                ("rf", r"after reflow", RF_C, np.asarray(f["rf1"]), float(f["sw_rf1"])),
                ("meanflow", r"MeanFlow", C.SURPRISE, np.asarray(m["meanflow1"]), float(m["sw_meanflow1"])),
                ("shortcut", r"shortcut model", C.TRUE_P, np.asarray(m["shortcut1"]), float(m["sw_shortcut1"]))]
        panels = VGroup()
        for i, (k, name, col, X, d) in enumerate(sets):
            cx = -5.1 + i * 3.4
            c_ = cloud(X[:400], col, radius=0.016, scale=S, shift=[cx, 0.2, 0])
            box = RoundedRectangle(width=3.1, height=2.6, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5).move_to([cx, 0.2, 0])
            t_ = label(name, font_size=22, color=col).next_to(box, UP, buff=0.12)
            d_ = MathTex(rf"{d:.3f}", font_size=28, color=col).next_to(box, DOWN, buff=0.15)
            panels.add(VGroup(box, c_, t_, d_))
        head = label(r"one step from noise", font_size=30).to_corner(UL, buff=0.4)  # the citation takes the right
        dl = label(r"distance from the real data \ (noise itself: \ $" + f"{float(f['sw_noise']):.2f}" + r"$)", font_size=20,
                   color=GREY_A).next_to(panels, DOWN, buff=0.5)
        sc = cmath(r"u(z, s, s + 2d) = \tfrac12\big[\,u(z, s, s + d) + u(z', s + d, s + 2d)\,\big]", font_size=28)
        sc.to_edge(DOWN, buff=0.35)
        scl = label(r"shortcut models: \ one jump of $2d$ must equal two of $d$", font_size=20, color=C.TRUE_P).next_to(sc, UP, buff=0.1)
        best = min(sets, key=lambda s_: s_[4])
        mf1, mf2 = float(m["sw_meanflow1"]), float(m["sw_meanflow2"])
        cite_ = cite(r"K.~Frans et al., \textit{One Step Diffusion via Shortcut Models} (2024)", corner=UR)
        with self.voiceover(
            "Here are all four after a single step from the same noise. <bookmark mark='a'/> Plain flow matching "
            "lands everything near the middle: one step along the starting velocity is a blur. Reflow does much "
            "better. <bookmark mark='b'/> MeanFlow, one jump, "
            + (f"is the closest of all, at {mf1:.3f}. " if best[0] == "meanflow" else f"reaches {mf1:.3f}; two jumps, {mf2:.3f}. ")
            + "<bookmark mark='c'/> Shortcut models, from 2024, get there another way: they're told the size of "
            "the jump, and trained so that one jump of size two d equals two jumps of size d. "
            + (f"Here the best single step is the {best[1].replace('after reflow', 'reflowed model')}'s. " if best[0] != "meanflow" else "")
            + "Few-step samplers like these are why image models can now draw in one to four steps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            self.play(FadeIn(panels[0]), FadeIn(panels[1]))
            vo.wait_until("a")
            self.play(Indicate(panels[0][3]), Indicate(panels[1][3]))
            vo.wait_until("b")
            self.play(FadeIn(panels[2]), FadeIn(dl))
            vo.wait_until("c")
            self.play(FadeIn(panels[3]), FadeIn(scl), Write(sc))
        self.wait(0.3)
        self.clear_scene()
