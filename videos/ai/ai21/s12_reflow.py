from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (DATA, FM_C, HIST, NOISE, OT_C, PART, RF2_C, RF_C, Panel, bars_chart, legend, load,
                                   log_axes, logcurve, take_away)

KC = {"fm": FM_C, "ot": OT_C, "rf1": RF_C, "rf2": RF2_C}
KN = {"fm": r"flow matching", "ot": r"minibatch OT pairs", "rf1": r"reflow once", "rf2": r"reflow twice"}
KS = {"fm": "plain flow matching", "ot": "minibatch optimal-transport pairing", "rf1": "one reflow", "rf2": "two reflows"}


class Reflow(VoiceoverScene):
    def construct(self):
        self.card()
        self.replay()
        self.rectify()
        self.measure()
        self.practice()

    def card(self):
        card = chapter_card(11, r"Rectified flow and reflow", r"Can a flow be taught to go straight?", part=PART)
        with self.voiceover("Chapter eleven. Rectified flow and reflow."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def replay(self):
        f = load("flow")
        checks = [int(c) for c in f["checks"]]
        snaps = np.asarray(f["fm_snaps"])
        L = np.asarray(f["fm_curve"])
        pn = Panel(5.8, center=[-3.4, -0.3, 0])
        pts = pn.dots(snaps[0], FM_C, radius=0.022)
        top = float(np.percentile(L[:, 1], 99)) * 1.05
        L = np.stack([L[:, 0], np.minimum(L[:, 1], top)], 1)  # the first few losses run off the top: drawn at it
        g = axes([0, checks[-1]], [0, top], x_length=4.6, y_length=2.6, xlabel=r"training step",
                 ylabel=r"the loss: \ $\| v_\theta - (x_1 - z) \|^2$", xticks=[0, checks[-1]], yticks=[0, round(top, 1)],
                 center=[3.6, 0.6, 0])
        tk = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(tk.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=FM_C).next_to(pn, UP, buff=0.12))
        dot = always_redraw(lambda: Dot(g.ax.c2p(tk.get_value(), float(np.interp(tk.get_value(), L[:, 0], L[:, 1]))),
                                        radius=0.07, color=FM_C))
        P = np.asarray(f["fm_path"])
        trails = pn.paths(P[:, ::3], FM_C, stroke_width=1.2, opacity=0.6, smooth=True)
        st = np.asarray(f["fm_straight"])
        floor_ = float(np.min(L[:, 1]))
        tag = label(r"$600$ points from the same noise, \\ $100$ Euler steps, \ at each checkpoint", font_size=18,
                    color=GREY_A).next_to(g, DOWN, buff=0.4)
        with self.voiceover(
            "Here is a flow-matching network learning our letters, from the same noise at each checkpoint. "
            "<bookmark mark='a'/> The loss falls fast and then stalls, well above zero. <bookmark mark='b'/> It can't "
            f"reach zero: random pairs give every point many velocities, and the network can only learn their "
            f"average. <bookmark mark='c'/> And its paths bend: straightness {st[0]:.2f}, in {len(st)} seeds from "
            f"{st.min():.2f} to {st.max():.2f}."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(pts), FadeIn(g), FadeIn(tag))
            self.add(cnt, dot)
            vo.wait_until("a")
            for k in range(1, len(checks)):
                seg = [g.ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                anims = [tk.animate.set_value(checks[k]), *pn.move(pts, snaps[k])]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=FM_C, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=0.9)
            vo.wait_until("b")
            vo.wait_until("c")
            self.play(Create(trails), run_time=2.0)
        for m in (cnt, dot):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rectify(self):
        f = load("flow")
        panels = VGroup()
        for i, k in enumerate(("fm", "rf1", "rf2")):
            pn = Panel(4.2, center=[-4.6 + 4.6 * i, 0.9, 0])
            P = np.asarray(f[f"{k}_path"])
            panels.add(VGroup(pn, pn.paths(P[:, ::3], KC[k], stroke_width=1.2, opacity=0.7, smooth=True),
                              label(KN[k], font_size=22, color=KC[k]).next_to(pn, UP, buff=0.1),
                              label(rf"straightness ${float(np.mean(f[f'{k}_straight'])):.3f}$", font_size=20,
                                    color=KC[k]).next_to(pn, DOWN, buff=0.08)))
        d = theorem_card(r"rectified flow", VGroup(
            label(r"pair each noise point $z$ with the end of its own flow, $T(z)$, \ and train a new flow on the pairs",
                  font_size=22),
            label(r"the new pairing costs no more, \ for every convex cost; \ repeat, \ and the paths straighten",
                  font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15), who=r"Liu, Gong \& Liu (2023)",
            width=9.0).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Xingchao Liu, Chengyue Gong and Qiang Liu called the fix reflow. <bookmark mark='a'/> Run the trained "
            "flow, and pair each noise point with where the flow actually takes it. Those pairs no longer cross one "
            "another, so train a second flow on them: the averaging that bent the paths has nothing left to average. "
            "<bookmark mark='b'/> They proved the new pairing never costs more to transport, for any convex cost, "
            "and that repeating it straightens the paths. <bookmark mark='c'/> On our letters, once, and twice."
        ) as vo:
            self.play(FadeIn(panels[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(panels[1][0], panels[1][2])), Create(panels[1][1]), FadeIn(panels[1][3]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(panels[2][0], panels[2][2])), Create(panels[2][1]), FadeIn(panels[2][3]), run_time=1.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        f = load("flow")
        kinds = ["fm", "ot", "rf1", "rf2"]
        steps = [int(s) for s in f["steps"]]
        SW = {k: np.asarray(f[f"{k}_sw"]) for k in kinds}  # seed, steps
        fl, noise = float(f["floor"]), float(f["sw_noise"])
        vals = np.concatenate([SW[k].ravel() for k in kinds] + [[fl]])
        lo, hi = math.floor(math.log10(vals.min()) * 2) / 2, math.ceil(math.log10(vals.max()) * 2) / 2
        g = log_axes([0, 2], [lo, hi], x_length=6.0, y_length=3.6, xlabel=r"Euler steps",
                     ylabel=r"distance from the data \ (log scale)", xticks=steps,
                     yticks=[v for v in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0) if lo <= math.log10(v) <= hi],
                     center=[-3.2, -0.3, 0])
        lx = np.log10(steps)
        lines = VGroup()
        for k in kinds:
            lines.add(VGroup(band(g.ax, lx, np.log10(SW[k].min(0)), np.log10(SW[k].max(0)), KC[k], 0.2),
                             logcurve(g.ax, steps, SW[k].mean(0), KC[k], 3, radius=0.045)))
        flo = DashedLine(g.ax.c2p(0, math.log10(fl)), g.ax.c2p(2, math.log10(fl)), color=GREY_B, stroke_width=1.5)
        fll = label(r"a fresh sample \\ of the data", font_size=15, color=GREY_B).next_to(flo, RIGHT, buff=0.1)
        lg = legend([(KC[k], KN[k]) for k in kinds], font_size=19).move_to([4.4, 2.4, 0])
        stv = {k: np.asarray(f[f"{k}_straight"]) for k in kinds}
        ch = bars_chart([stv[k].mean() for k in kinds], [KC[k] for k in kinds], [r"FM", r"OT", r"reflow", r"reflow$^2$"],
                        height=1.8, bar_w=0.6, gap=0.4, vmax=1.0, spread=[(stv[k].min(), stv[k].max()) for k in kinds],
                        digits=3, font_size=18).move_to([4.4, -1.5, 0])
        chl = label(rf"straightness \ (${len(stv['fm'])}$ seeds)", font_size=20, color=GREY_A).next_to(ch, UP, buff=0.3)
        one = {k: SW[k][:, 0] for k in kinds}
        best1 = min(kinds, key=lambda k: one[k].mean())
        fm1 = one["fm"].mean()
        sep = one[best1].max() < min(one[k].min() for k in kinds if k != best1)
        ot_vs = ("Pairing each batch optimally, as Alexander Tong and colleagues and Aram-Alexandre Pooladian and "
                 "colleagues proposed in 2023, gets most of the way with a single training run: "
                 f"{one['ot'].mean():.3f} in one step." if one["ot"].mean() < 0.5 * fm1 else
                 f"Pairing each batch optimally, the 2023 proposal of Tong and of Pooladian and colleagues, reaches "
                 f"{one['ot'].mean():.3f} in one step.")
        sep_note = ("every seed of it ahead of every seed of the others." if sep else "though the seeds overlap.")
        r1, r100 = float(one["rf1"].mean()), float(SW["rf1"][:, -1].mean())
        rf_note = ("After one reflow, one step is nearly as good as a hundred; " if r1 < 1.5 * r100 else
                   f"After one reflow, one step lands {r1:.3f} from the data, against {r100:.3f} with a hundred; ")
        with self.voiceover(
            "Measured, at the same budget for every model, three seeds each: the distance from the data after a "
            "given number of Euler steps. <bookmark mark='a'/> Plain flow matching needs many steps: in one step its "
            f"samples land {fm1:.3f} from the data, against {noise:.2f} for the noise itself. <bookmark mark='b'/> "
            + rf_note + f"the best single step is {KS[best1]}'s, at "
            f"{one[best1].mean():.3f}, " + sep_note + " <bookmark mark='c'/> " + ot_vs + " <bookmark mark='d'/> Straightness says why: one Euler step is "
            "exact on a straight path."
        ) as vo:
            self.play(FadeIn(g), Create(flo), FadeIn(fll), FadeIn(lg))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(ch), FadeIn(chl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        f = load("flow")
        cards = VGroup(
            history_card(2023, r"Liu et al.: \ InstaFlow", r"reflow plus distillation: \ Stable Diffusion in one step",
                         color=HIST, width=4.3, font_size=21),
            history_card(2024, r"Esser et al.: \ Stable Diffusion 3", r"a rectified-flow transformer, \ trained with "
                         r"straight lines", color=HIST, width=4.3, font_size=21),
            history_card(2024, r"Black Forest Labs: \ FLUX.1", r"a $12$-billion-parameter rectified-flow transformer",
                         color=HIST, width=4.3, font_size=21)).arrange(RIGHT, buff=0.22).to_edge(UP, buff=0.4)
        if cards.width > 13.4:
            cards.width = 13.4
        S = Group()
        for i, k in enumerate(("fm", "ot", "rf1", "rf2")):
            pn = Panel(3.2, center=[-5.025 + 3.35 * i, -1.25, 0])
            S.add(Group(pn, pn.scatter(np.asarray(f[f"{k}1"]), KC[k], radius_px=1.4, res=260),
                        label(KN[k], font_size=19, color=KC[k]).next_to(pn, UP, buff=0.08)))
        sl = label(r"one step from the same noise", font_size=20, color=GREY_A).next_to(S, DOWN, buff=0.12)
        with self.voiceover(
            "Here is what one step looks like on our letters, from each of the four. <bookmark mark='a'/> In "
            "practice: InstaFlow, in 2023, combined reflow with distillation to make Stable Diffusion draw in one "
            "step. <bookmark mark='b'/> Stable Diffusion 3 and FLUX one, in 2024, were trained as rectified flows, "
            "straight lines between noise and data, with the architecture that is Part 22's story."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in S], lag_ratio=0.25), FadeIn(sl), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1:], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
