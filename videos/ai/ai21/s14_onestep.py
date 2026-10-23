from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (CD_C, DATA, DMD_C, FM_C, MF_C, NOISE, OT_C, PART, PROG_C, RF2_C, RF_C, SC_C, SCORE,
                                   Panel, load, take_away)


class OneStep(VoiceoverScene):
    def construct(self):
        self.card()
        self.average()
        self.shortcut()
        self.board()

    def card(self):
        card = chapter_card(13, r"One step from scratch", r"Can a model learn to jump, without a teacher?", part=PART)
        with self.voiceover("Chapter thirteen. One step from scratch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def average(self):
        f = load("flow")
        P = np.asarray(f["fm_path"])  # (frames, particles, 2): the learned flow
        n = len(P) - 1
        # the path that bulges most from its chord, among those that keep moving forward along it (a path that
        # doubles back is not a curve) and travel far enough to see
        chord = np.linalg.norm(P[-1] - P[0], axis=-1)
        u_ = (P[-1] - P[0]) / np.maximum(chord, 1e-9)[:, None]
        rel = P - P[0]
        proj = (rel * u_[None]).sum(-1) / np.maximum(chord, 1e-9)
        bulge = np.abs(rel[..., 0] * u_[None, :, 1] - rel[..., 1] * u_[None, :, 0]).max(0) / np.maximum(chord, 1e-9)
        ok = np.where((np.diff(proj, axis=0) > -0.02).all(0) & (chord > 1.2))[0]
        i = int(ok[np.argmax(bulge[ok])]) if len(ok) else int(np.argmax(bulge))
        q = P[:, i]
        lo_, hi_ = q.min(0), q.max(0)
        S = 4.4 / max(float((hi_ - lo_).max()), 1e-9)  # the one path, filling the left of the frame
        O = np.array([-3.7, -0.4, 0]) - S * np.array([*(lo_ + hi_) / 2, 0])
        pts = [O + S * np.array([x, y, 0]) for x, y in q]
        path = VMobject(color=FM_C, stroke_width=3.5).set_points_smoothly(pts)
        a, b = int(0.2 * n), int(0.85 * n)
        zs, zt = Dot(pts[a], radius=0.08, color=NOISE), Dot(pts[b], radius=0.08, color=DATA)
        zsl = MathTex(r"z_s", font_size=30, color=NOISE).next_to(zs, LEFT, buff=0.1)
        ztl = MathTex(r"z_t", font_size=30, color=DATA).next_to(zt, RIGHT, buff=0.1)
        tang = VGroup()
        for k in range(a, b + 1, max(1, (b - a) // 5)):
            d = pts[min(k + 1, n)] - pts[k]
            d = d / max(np.linalg.norm(d), 1e-9) * 0.55
            tang.add(Arrow(pts[k], pts[k] + d, buff=0, color=SCORE, stroke_width=3, max_tip_length_to_length_ratio=0.3))
        avg = Arrow(pts[a], pts[b], buff=0.08, color=MF_C, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        side = np.array([-(pts[b] - pts[a])[1], (pts[b] - pts[a])[0], 0])
        side = side / max(np.linalg.norm(side), 1e-9)
        vl = label(r"$v$: \\ the speedometer, \\ velocity at each moment", font_size=20, color=SCORE).move_to(tang.get_center() + 1.3 * side)
        ul = label(r"$(t - s)\,u$: \\ one jump, \\ at the average velocity", font_size=20, color=MF_C).move_to(avg.get_center() - 1.1 * side)
        keep_in_frame(vl)
        keep_in_frame(ul)
        colors = {r"u": MF_C, r"v": SCORE, r"z_s": NOISE, r"z_t": DATA}
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
                       label(r"one Jacobian-vector product: \ about one extra pass", font_size=18, color=GREY_A),
                       label(r"sg: \ stop-gradient, \ the target is held fixed", font_size=18, color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.06).align_to(e_, LEFT)
        for k in range(1, len(eqs)):
            eqs[k:].shift(DOWN * 0.2)
            notes[k:].shift(DOWN * 0.2)
        head = label(r"MeanFlow: \ learn the average velocity", font_size=26).to_edge(UP, buff=0.35)
        keep_in_frame(VGroup(eqs, notes))
        cite_ = cite(r"Z.~Geng, M.~Deng, X.~Bai, J.~Z.~Kolter \& K.~He, \textit{Mean Flows for One-step Generative Modeling} "
                     r"(2025)", corner=DR, font_size=18)
        with self.voiceover(
            "In 2025 Zhengyang Geng, Kaiming He and colleagues trained a one-step model with no teacher at all. "
            "<bookmark mark='a'/> Here is one point's path under our flow model: it bends. Flow matching learns v, "
            "the velocity at each moment, so it has to take many small steps. <bookmark mark='b'/> MeanFlow learns u "
            "instead: the average velocity between two times s and t, like the average speed over a trip rather "
            "than the speedometer's reading. <bookmark mark='c'/> With it, a single jump from s to t lands on the "
            "path, however much it bends. <bookmark mark='d'/> To get u exactly you would integrate the velocity "
            "along the path: the slow work we wanted to avoid. The trick: write t minus s times u as z t minus z s, "
            "and differentiate in s. Out comes an identity: the average velocity is the velocity now, plus t minus s "
            "times how fast the average changes as the start moves along the path. <bookmark mark='e'/> That "
            "derivative costs one Jacobian-vector product, about one extra run of the network. <bookmark mark='f'/> "
            "So the network is trained to match the right-hand side, held fixed: no integral, and no teacher. On "
            "ImageNet at 256 pixels it reached an FID of 3.43 in one step."
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
    def shortcut(self):
        m = load("fewstep")
        panels = Group()
        lim = np.array([4.0, 3.3])
        for i, (k, col, nm) in enumerate((("meanflow", MF_C, r"MeanFlow"), ("shortcut", SC_C, r"shortcut model"))):
            pn = Panel(4.6, center=[-3.5 + 7.0 * i, 0.4, 0], xlim=(-3.4, 3.4), ylim=(-2.8, 2.4))
            sn = np.clip(np.asarray(m[f"{k}_snaps"]), -lim, lim)
            panels.add(Group(pn, pn.dots(sn[0], col, radius=0.018), label(nm, font_size=24, color=col).next_to(pn, UP, buff=0.1)))
        sc = cmath(r"u(z, s, s + 2d) = \tfrac12\big[\,u(z, s, s + d) + u(z', s + d, s + 2d)\,\big]", font_size=28)
        sc.to_edge(DOWN, buff=0.35)
        scl = label(r"shortcut models: \ one jump of $2d$ must equal two of $d$", font_size=20, color=SC_C).next_to(sc, UP, buff=0.1)
        steps = {k: [int(v) for v in m[f"{k}_snap_steps"]] for k in ("meanflow", "shortcut")}
        cite_ = cite(r"K.~Frans, D.~Hafner, S.~Levine \& P.~Abbeel, \textit{One Step Diffusion via Shortcut Models} (2024)",
                     corner=UR, font_size=18)
        with self.voiceover(
            "Here is ours learning: one jump from the same noise, at checkpoints during training. "
            "<bookmark mark='a'/> A year earlier, Kevin Frans and colleagues' shortcut models got there another way: "
            "the network is told the size of the jump, and trained so that one jump of size two d equals two jumps "
            "of size d, starting from plain flow matching at size zero. <bookmark mark='b'/> Watch both learn to land "
            "on the letters."
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(panels[1]), FadeIn(scl), Write(sc))
            vo.wait_until("b")
            for j in range(1, max(len(steps["meanflow"]), len(steps["shortcut"]))):
                anims = []
                for i, k in enumerate(("meanflow", "shortcut")):
                    sn = np.clip(np.asarray(m[f"{k}_snaps"]), -lim, lim)
                    if j < len(sn):
                        anims += panels[i][0].move(panels[i][1], sn[j])
                self.play(*anims, run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        f, d, m = load("flow"), load("distill"), load("fewstep")
        rows = [("fm", r"flow matching, \ $1$ Euler step", FM_C, np.asarray(f["fm_sw"])[:, 0]),
                ("ot", r"minibatch OT pairs", OT_C, np.asarray(f["ot_sw"])[:, 0]),
                ("rf1", r"reflow once", RF_C, np.asarray(f["rf1_sw"])[:, 0]),
                ("rf2", r"reflow twice", RF2_C, np.asarray(f["rf2_sw"])[:, 0]),
                ("prog", r"progressive distillation", PROG_C, np.asarray(d["prog_sw"])[:, -1]),
                ("cd", r"consistency distillation", CD_C, np.asarray(d["cd_sw"])),
                ("dmd", r"distribution matching (DMD)", DMD_C, np.asarray(d["dmd_sw"])),
                ("mf", r"MeanFlow", MF_C, np.asarray(m["meanflow_sw"])[:, 0]),
                ("sc", r"shortcut model", SC_C, np.asarray(m["shortcut_sw"])[:, 0])]
        teach = {"fm": False, "ot": False, "rf1": True, "rf2": True, "prog": True, "cd": True, "dmd": True, "mf": False,
                 "sc": False}
        # the scale of the one-step models; plain flow matching's single step runs off it, with a break in its bar
        hi = max(float(v.max()) for k, *_, v in rows if k != "fm") * 1.25
        W = 6.0
        x0 = -1.2
        cap = lambda v: min(float(v), 1.04 * hi)  # noqa: E731
        g = VGroup()
        for i, (k, nm, col, v) in enumerate(rows):
            y = 2.3 - 0.56 * i
            name = label(nm, font_size=20, color=col).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            w = W * cap(v.mean()) / hi
            bar = Rectangle(width=max(w, 0.02), height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [x0 + w / 2, y, 0])
            wh = Line([x0 + W * cap(v.min()) / hi, y, 0], [x0 + W * cap(v.max()) / hi, y, 0], color=WHITE, stroke_width=2)
            val = MathTex(f"{v.mean():.3f}", font_size=22, color=col).next_to([x0 + W * cap(v.max()) / hi, y, 0], RIGHT,
                                                                             buff=0.15)
            t_ = label(r"teacher" if teach[k] else r"from scratch", font_size=16, color=GREY_B).next_to(val, RIGHT, buff=0.2)
            if v.mean() > 1.04 * hi:  # a break in the bar: it is off the scale
                bx = x0 + 0.8 * w
                bar = VGroup(bar, Polygon([bx - 0.12, y - 0.25, 0], [bx + 0.02, y + 0.25, 0], [bx + 0.14, y + 0.25, 0],
                                          [bx, y - 0.25, 0], stroke_width=0, fill_color=BACKGROUND, fill_opacity=1))
            g.add(VGroup(name, bar, wh, val, t_))
        fl = float(f["floor"])
        flo = DashedLine([x0 + W * fl / hi, 2.65, 0], [x0 + W * fl / hi, 2.3 - 0.56 * (len(rows) - 1) - 0.3, 0], color=GREY_B,
                         stroke_width=1.5)
        fll = label(r"floor", font_size=16, color=GREY_B).next_to(flo, UP, buff=0.05)
        head = label(rf"one step from noise: \ distance from the data \ (mean; \ whiskers: ${len(rows[0][3])}$ seeds) \\ "
                     rf"each network about ${int(d['steps']):,}$ training steps, \ plus its teacher's where marked".replace(",", "{,}"),
                     font_size=20, color=GREY_A).to_edge(UP, buff=0.2)
        order = sorted(rows, key=lambda r: r[3].mean())
        best, second = order[0], order[1]
        scratch = [r for r in rows if not teach[r[0]] and r[0] != "fm"]
        bs = min(scratch, key=lambda r: r[3].mean())
        spoken = {"fm": "plain flow matching", "ot": "minibatch optimal-transport flow matching", "rf1": "one reflow",
                  "rf2": "two reflows", "prog": "progressive distillation", "cd": "consistency distillation",
                  "dmd": "distribution matching", "mf": "MeanFlow", "sc": "the shortcut model"}
        best_name, bs_name, second_name = spoken[best[0]], spoken[bs[0]], spoken[second[0]]
        sep = best[3].max() < second[3].min()
        if sep:
            sep_note = f"and every one of its seeds beats every seed of the runner-up, {second_name}."
        else:
            sep_note = f"though its seeds overlap with the runner-up's, {second_name}."
        ta = take_away(r"Fifty steps to one: \ straighter paths, \ a student that jumps, \ or a network that learns the jump.")
        with self.voiceover(
            "Here is every one-step model of this part, from the same noise, each network trained for about the same "
            f"number of steps, {len(rows[0][3])} seeds each. <bookmark mark='a'/> The best single step is {best_name}'s, at {best[3].mean():.3f}, "
            + sep_note + " <bookmark mark='b'/> Among the models with no teacher, the best is " + bs_name
            + f", at {bs[3].mean():.3f}. <bookmark mark='c'/> Plain flow matching's single step, at "
            f"{rows[0][3].mean():.3f}, is the blur every method starts from."
        ) as vo:
            self.play(FadeIn(head), Create(flo), FadeIn(fll))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in g], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(g[rows.index(best)], color=WHITE))
            vo.wait_until("b")
            self.play(Indicate(g[rows.index(bs)], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
