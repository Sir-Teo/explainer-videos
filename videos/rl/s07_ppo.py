from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.rl.common import Plot, label, load, mtex, note, pct_fmt, real_tag, schematic_tag, smooth, source
from videos.rl.compute import load_run

EPS = 0.2


def clip_obj(rho, A, eps=EPS):
    return np.minimum(rho * A, np.clip(rho, 1 - eps, 1 + eps) * A)


class PPO(VoiceoverScene):
    def construct(self):
        self.formula()
        self.cases()
        self.windows()
        self.reuse()
        self.rlhf()

    # ------------------------------------------------------------------
    def formula(self):
        f = mtex(r"L^{\text{CLIP}}(\theta)", r"=", r"\mathbb{E}_t\Big[\min\Big(", r"\rho_t", r"A_t", r",\;",
                 r"\operatorname{clip}(\rho_t,\,1-\varepsilon,\,1+\varepsilon)", r"A_t", r"\Big)\Big]", font_size=46)
        f[3].set_color(C.RATIO)
        f[4].set_color(C.ADVANTAGE)
        f[6].set_color(C.RATIO)
        f[7].set_color(C.ADVANTAGE)
        f.move_to(UP * 1.2)
        b1 = Brace(f[3:5], DOWN, color=C.RATIO)
        l1 = label(r"the surrogate", font_size=26, color=C.RATIO).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(f[6:8], DOWN, color=C.RATIO)
        l2 = label(r"\dots with the ratio held to $[0.8,\ 1.2]$", font_size=26, color=C.RATIO).next_to(b2, DOWN, buff=0.08)
        src = source(r"Schulman, Wolski, Dhariwal, Radford \& Klimov, \emph{Proximal Policy Optimization}, 2017 ($\varepsilon = 0.2$)")
        with self.voiceover(
            "Proximal policy optimization keeps the surrogate, but takes away the incentive to move too far. "
            "<bookmark mark='s'/> Take the surrogate term, ratio times advantage, <bookmark mark='c'/> compute a "
            "second copy with the ratio clipped to between zero point eight and one point two, and keep the smaller "
            "of the two."
        ) as vo:
            self.play(Write(f), FadeIn(src), run_time=2)
            vo.wait_until("s")
            self.play(GrowFromCenter(b1), FadeIn(l1))
            vo.wait_until("c")
            self.play(GrowFromCenter(b2), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cases(self):
        def panel(A, title, color):
            p = Plot(x_range=(0, 2), y_range=(-2, 2), width=5.2, height=3.6, x_ticks=[0, 0.8, 1, 1.2, 2],
                     y_ticks=[-1, 0, 1], x_label=r"ratio $\rho = \pi_\theta / \pi_{\text{old}}$")
            xs = np.linspace(0, 2, 400)
            unc = p.line(xs, xs * A, color=GREY_B, stroke_width=2)
            unc.set_stroke(opacity=0.5)
            cl = p.line(xs, clip_obj(xs, A), color=color, stroke_width=5)
            flat = (xs > 1 + EPS) if A > 0 else (xs < 1 - EPS)
            x0, x1 = (1 + EPS, 2) if A > 0 else (0, 1 - EPS)
            shade = Polygon(p.c2p(x0, -2), p.c2p(x1, -2), p.c2p(x1, 2), p.c2p(x0, 2), stroke_width=0,
                            fill_color=GREY_D, fill_opacity=0.35)
            zl = label(r"gradient $= 0$", font_size=22, color=GREY_A).move_to(p.c2p((x0 + x1) / 2, 1.7 if A < 0 else -1.6))
            t = label(title, font_size=28, color=color).next_to(p, UP, buff=0.2)
            g = VGroup(p, shade, unc, cl, zl, t)
            g.plot, g.curve, g.shade, g.zl, g.A = p, cl, shade, zl, A
            return g
        pos = panel(1.0, r"$A > 0$: a good answer", C.REWARD)
        neg = panel(-1.0, r"$A < 0$: a bad answer", C.PENALTY)
        VGroup(pos, neg).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        rho = ValueTracker(0.6)

        def mover(g):
            def f():
                x = rho.get_value()
                y = float(clip_obj(np.array([x]), g.A)[0])
                p = g.plot.c2p(x, y)
                d = Dot(p, radius=0.09, color=YELLOW)
                active = (x <= 1 + EPS) if g.A > 0 else (x >= 1 - EPS)
                direction = RIGHT if g.A > 0 else LEFT
                arr = Arrow(p, p + direction * 0.7, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.3)
                arr.set_opacity(1.0 if active else 0.0)
                return VGroup(d, arr)
            return always_redraw(f)
        m1, m2 = mover(pos), mover(neg)
        cap = label(r"inside the window: push as usual.\ \ Past it: no more push in that direction.", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Look at it as a function of the ratio. <bookmark mark='p'/> For a good answer, the objective rises "
            "with the ratio, so the gradient pushes the token's probability up, <bookmark mark='f'/> until the "
            "ratio passes one point two. Then the objective goes flat, and the gradient is zero: no reward for "
            "pushing further. <bookmark mark='n'/> For a bad answer it's the mirror image: push the probability "
            "down, until it has fallen by twenty percent. <bookmark mark='m'/> Note the minimum: in the direction "
            "that would hurt, there's no clipping. The objective is a pessimistic bound on the surrogate."
        ) as vo:
            self.play(FadeIn(pos.plot), FadeIn(pos[5]), Create(pos[2]), Create(pos.curve))
            vo.wait_until("p")
            self.play(FadeIn(m1))
            vo.wait_until("f")
            self.play(rho.animate.set_value(1.7), run_time=2.5, rate_func=linear)
            self.play(FadeIn(pos.shade), FadeIn(pos.zl))
            vo.wait_until("n")
            self.play(FadeIn(neg.plot), FadeIn(neg[5]), Create(neg[2]), Create(neg.curve), FadeIn(m2))
            self.play(rho.animate.set_value(0.4), run_time=2.5, rate_func=linear)
            self.play(FadeIn(neg.shade), FadeIn(neg.zl))
            vo.wait_until("m")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def windows(self):
        probs = [0.9, 0.5, 0.2, 0.05, 0.01]
        rows = VGroup()
        W = 6.0
        for p in probs:
            name = MathTex(rf"\pi_{{\text{{old}}}} = {p:g}", font_size=30, color=C.OLD_POLICY)
            track = Line(ORIGIN, RIGHT * W, color=GREY_D, stroke_width=6)
            lo, hi = p * (1 - EPS), min(1.0, p * (1 + EPS))
            win = Line(RIGHT * W * lo, RIGHT * W * hi, color=C.RATIO, stroke_width=14)
            dot = Dot(RIGHT * W * p, radius=0.07, color=WHITE)
            rng_ = MathTex(rf"[{lo:.3g},\ {hi:.3g}]", font_size=26, color=C.RATIO)
            g = VGroup(track, win, dot)
            row = VGroup(name, g, rng_)
            name.next_to(g, LEFT, buff=0.4)
            rng_.next_to(g, RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(DOWN * 0.2)
        for row in rows:
            row[1].align_to(rows[0][1], LEFT)
            row[0].next_to(row[1], LEFT, buff=0.4)
            row[2].next_to(row[1], RIGHT, buff=0.4)
        axis_l = VGroup(MathTex("0", font_size=24, color=GREY_B).next_to(rows[-1][1][0].get_start(), DOWN, buff=0.15),
                        MathTex("1", font_size=24, color=GREY_B).next_to(rows[-1][1][0].get_end(), DOWN, buff=0.15))
        head = label(r"How far one round of updates may move each token's probability ($\varepsilon = 0.2$)", font_size=28).to_edge(UP, buff=0.4)
        foot = label(r"a token at 1\% can only rise to 1.2\%: keep this in mind", font_size=28, color=YELLOW).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In probability terms, the clip gives each token a window. A token the old policy chose with "
            "probability zero point nine can move anywhere from zero point seven two up to one. <bookmark mark='r'/> "
            "But the window is relative: a token at one percent can only rise to one point two percent in a round of "
            "updates. That asymmetry between likely and unlikely tokens will come back to haunt us."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), FadeIn(axis_l))
            vo.wait_until("r")
            self.play(Indicate(rows[-1], color=YELLOW), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reuse(self):
        runs = {}
        for name in ("onpolicy", "reuse_noclip", "reuse_clip"):
            runs[name] = [load_run(f"{name}_s{s}") for s in range(3)]

        def curve(rs):
            steps = np.array([e["step"] for e in rs[0]["evals"]], float)
            ys = np.array([[e["pass1"] for e in r["evals"]] for r in rs])
            return steps, ys.mean(0), ys.min(0), ys.max(0)
        S = max(e["step"] for e in runs["onpolicy"][0]["evals"])
        plot = Plot(x_range=(0, S), y_range=(0.65, 1.0), width=7.8, height=4.4, x_ticks=list(range(0, S + 1, 20)),
                    y_ticks=[0.7, 0.8, 0.9, 1.0], y_fmt=pct_fmt, x_label=r"RL steps (each: 256 fresh answers)",
                    y_label=r"accuracy on held-out problems")
        plot.move_to(LEFT * 1.9 + DOWN * 0.4)
        spec = [("onpolicy", r"1 update per batch", C.OLD_POLICY), ("reuse_noclip", r"16 per batch, no clip", C.PENALTY),
                ("reuse_clip", r"16 per batch, clipped", C.REWARD)]
        lines, bands, keys = VGroup(), VGroup(), VGroup()
        for name, txt, col in spec:
            st, m, lo, hi = curve(runs[name])
            lo, hi, m = np.clip(lo, 0.65, 1.0), np.clip(hi, 0.65, 1.0), np.clip(m, 0.65, 1.0)
            bands.add(Polygon(*[plot.c2p(x, y) for x, y in zip(st, lo)], *[plot.c2p(x, y) for x, y in zip(st[::-1], hi[::-1])],
                              stroke_width=0, fill_color=col, fill_opacity=0.18))
            lines.add(plot.line(st, m, color=col, stroke_width=4))
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=24)).arrange(RIGHT, buff=0.15))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(plot, RIGHT, buff=0.25).shift(UP * 0.8)
        head = label(r"Reusing each batch, with and without the clip (3 seeds each)", font_size=30).to_edge(UP, buff=0.35)
        self.reuse_result = runs
        c_on, c_cl, c_nc = curve(runs["onpolicy"]), curve(runs["reuse_clip"]), curve(runs["reuse_noclip"])
        i5 = int(np.searchsorted(c_on[0], 5))
        dip = int(np.argmin(c_nc[2][4:])) + 4  # worst seed of the unclipped runs, after the first steps
        assert c_cl[1][i5] > c_on[1][i5] + 0.1 and c_cl[1][-1] > c_nc[1][-1] and c_nc[2][dip] < c_cl[2][dip], (c_cl, c_nc)
        with self.voiceover(
            "Does it matter? Here's a real test on the pocket model you'll meet properly in a few minutes. "
            f"<bookmark mark='o'/> Teal: one gradient step per batch. After five steps it's at {c_on[1][i5] * 100:.0f} percent. "
            f"<bookmark mark='n'/> Red: sixteen steps per batch, without the clip. Reusing the data is far more "
            f"efficient: {c_nc[1][i5] * 100:.0f} percent after five steps. But it wobbles: around step {int(c_nc[0][dip])}, "
            f"one seed falls back to {c_nc[2][dip] * 100:.0f}. <bookmark mark='c'/> Green: the same sixteen steps, clipped. "
            f"Just as fast, and it climbs steadily, to {c_cl[1][-1] * 100:.1f} percent. In a model this small the "
            "difference is modest; the point of the clip is that you can take many steps on one batch without "
            "worrying about how far they go."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(real_tag()))
            for k, mark in enumerate(["o", "n", "c"]):
                vo.wait_until(mark)
                self.play(FadeIn(bands[k]), Create(lines[k]), FadeIn(keys[k]), run_time=1.5)
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rlhf(self):
        def model(name, sub, color, train):
            box = RoundedRectangle(width=3.0, height=1.5, corner_radius=0.15, stroke_color=color, fill_color=color,
                                   fill_opacity=0.15 if train else 0.05, stroke_width=3 if train else 2)
            t = label(name, font_size=28).move_to(box).shift(UP * 0.2)
            s = label(sub, font_size=20, color=GREY_A).next_to(t, DOWN, buff=0.1)
            tag = label(r"trained" if train else r"frozen", font_size=20, color=color if train else GREY_B)
            tag.next_to(box, DOWN, buff=0.1)
            return VGroup(box, t, s, tag)
        ms = VGroup(model(r"policy $\pi_\theta$", r"writes the answers", C.RL_POLICY, True),
                    model(r"reference $\pi_{\text{ref}}$", r"the starting point", C.REFERENCE, False),
                    model(r"reward model", r"scores answers", C.REWARD, False),
                    model(r"critic $V$", r"estimates values", C.BASELINE, True)).arrange(RIGHT, buff=0.35).move_to(UP * 1.1)
        head = label(r"RLHF with PPO (InstructGPT, 2022): four full-size networks", font_size=32).to_edge(UP, buff=0.35)
        rt = mtex(r"r_t", r"=", r"-\beta \log\frac{\pi_\theta(y_t\mid s_t)}{\pi_{\text{ref}}(y_t \mid s_t)}", r"\;+\;",
                  r"\mathbf{1}[t = T]\; R_{\text{RM}}(x, y)", font_size=38)
        rt[2].set_color(C.KL)
        rt[4].set_color(C.REWARD)
        rt.next_to(ms, DOWN, buff=0.9)
        rl = label(r"a per-token leash to the reference, plus the reward model's score at the end", font_size=26, color=GREY_A)
        rl.next_to(rt, DOWN, buff=0.2)
        src = source(r"Ouyang et al., \emph{Training language models to follow instructions with human feedback}, 2022")
        with self.voiceover(
            "This is the algorithm behind InstructGPT and the original ChatGPT. Count the networks: "
            "<bookmark mark='p'/> the policy being trained, <bookmark mark='r'/> a frozen copy of where it started, "
            "<bookmark mark='m'/> a reward model, and <bookmark mark='c'/> the critic, each as large as the language "
            "model itself. <bookmark mark='t'/> Every token pays a small penalty for drifting from the reference, "
            "and the reward model's score arrives at the end."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark in enumerate(["p", "r", "m", "c"]):
                vo.wait_until(mark)
                self.play(FadeIn(ms[k], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("t")
            self.play(Write(rt), FadeIn(rl))
        with self.voiceover(
            "Two of those four networks exist to turn human judgment into a number. So where does that number "
            "come from?"
        ):
            self.play(Indicate(ms[2], color=C.REWARD))
        self.wait(0.3)
        self.clear_scene()
