from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, MEAS, TEST, TRAIN, bars, chapter, curve, load

BCOL = {4: "#58A6FF", 16: "#5BD17A", 64: "#F7D154", 300: "#FF6B8B"}


class Sharpness(VoiceoverScene):
    def construct(self):
        chapter(self, 15, r"Flat minima and the sharpness debate", r"Do flat valleys generalize better?",
                "Chapter fifteen. Flat minima, and the sharpness debate.")
        self.idea()
        self.measure()
        self.rescale()

    # ------------------------------------------------------------------
    def idea(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 2.4, 1], x_length=8.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-1.4, -0.9, 0])

        def L(x):
            return 1.6 - 1.3 * math.exp(-((x + 1.4) / 0.75) ** 2) - 1.45 * math.exp(-((x - 1.5) / 0.18) ** 2)

        tr = ax.plot(L, x_range=[-3, 3], color=TRAIN, stroke_width=4)
        te = ax.plot(lambda x: L(x - 0.15) + 0.05, x_range=[-3, 3], color=TEST, stroke_width=3)
        fl = label(r"flat", font_size=24, color=MEAS).next_to(ax.c2p(-1.4, 0.3), DOWN, buff=0.15)
        sh = label(r"sharp", font_size=24, color=C.SURPRISE).next_to(ax.c2p(1.5, 0.15), DOWN, buff=0.15)
        g1 = DoubleArrow(ax.c2p(1.5, L(1.5)), ax.c2p(1.5, L(1.35) + 0.05), buff=0, color=C.SURPRISE, stroke_width=2.5,
                         tip_length=0.12)
        key = legend([(TRAIN, r"training loss"), (TEST, r"test loss: \ the same, \ shifted a little")], font_size=20)
        key.to_corner(UR, buff=0.35)
        tag = note(r"schematic").next_to(ax, DOWN, buff=0.1).align_to(ax, RIGHT)
        hist = VGroup(
            history_card(1997, r"S.~Hochreiter \& J.~Schmidhuber", r"\textit{Flat Minima}: \ a flat minimum needs "
                         r"fewer bits to describe", width=4.6, font_size=17, color=HIST),
            history_card(2017, r"N.~S.~Keskar et al.", r"large batches find sharp minima, \ and generalize worse",
                         width=4.6, font_size=17, color=HIST),
        ).arrange(DOWN, buff=0.2).to_corner(UR, buff=0.25).shift(DOWN * 1.2)
        with self.voiceover(
            "An older idea about why networks generalize: the shape of the valley training ends in. "
            "<bookmark mark='a'/> Suppose the test loss is the training loss shifted a little, because the test "
            "data differs a little. At the bottom of a flat valley, the shift costs almost nothing; at the bottom "
            "of a sharp one, it costs a lot. <bookmark mark='b'/> Hochreiter and Schmidhuber argued in 1997 that "
            "flat minima are simpler: their weights can be written down with fewer bits. In 2017 Keskar and "
            "colleagues reported that training with large batches finds sharper minima, and generalizes worse."
        ) as vo:
            self.play(Create(ax), Create(tr), FadeIn(fl), FadeIn(sh), FadeIn(tag), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(te), FadeIn(key[1]), GrowFromCenter(g1))
            vo.wait_until("b")
            self.play(FadeIn(hist[0], shift=LEFT * 0.2))
            self.play(FadeIn(hist[1], shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        s = load("sharp")
        lam, err, B = np.asarray(s["lam"]), np.asarray(s["err"]), np.asarray(s["B"])
        lr = np.asarray(s["lr"])
        rho = float(s["rho"])
        lo, hi = math.floor(math.log10(lam.min()) * 2) / 2, math.ceil(math.log10(lam.max()) * 2) / 2
        e0, e1 = math.floor(err.min() * 100) / 100 - 0.01, math.ceil(err.max() * 100) / 100 + 0.01
        G = axes([lo, hi], [e0, e1], x_length=6.4, y_length=4.4, xticks=[v for v in np.arange(lo, hi + 1e-9, 0.5)],
                 xfmt=lambda v: f"{10 ** v:.2g}", yticks=[round(v, 2) for v in np.linspace(e0, e1, 4)],
                 yfmt=lambda v: rf"{100 * v:.1f}\%", xlabel=r"sharpness: \ the Hessian's top eigenvalue \ (log scale)",
                 ylabel=r"error on new points", center=(-2.6, -0.5, 0))
        ax = G.ax
        dots = VGroup(*[Dot(ax.c2p(math.log10(a), b), radius=0.09 if l_ > 0.05 else 0.055, color=BCOL[int(bb)])
                        for a, b, bb, l_ in zip(lam, err, B, lr)])
        key = VGroup(*[VGroup(Dot(color=c_), label(rf"batch ${b_}$", font_size=20, color=c_)).arrange(RIGHT, buff=0.12)
                       for b_, c_ in BCOL.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        key.add(label(r"large: \ step $0.1$; \ small: \ $0.02$", font_size=18, color=GREY_B))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(G, RIGHT, buff=0.35).align_to(G, UP)
        setup = label(rf"$10 \to 256 \to 2$ networks, \ ${s['n']}$ points labelled by a teacher network; \ each "
                      rf"trained until its training loss is below ${s['target']:g}$", font_size=21, color=GREY_A)
        setup.to_edge(UP, buff=0.3)
        res = label(rf"rank correlation: \ ${rho:+.2f}$", font_size=28, color=WHITE).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        big, small = lam[B == max(BCOL)].mean(), lam[B == min(BCOL)].mean()
        ebig, esmall = err[B == max(BCOL)].mean(), err[B == min(BCOL)].mean()
        flat_better = rho > 0.3
        reached = bool(np.all(np.asarray(s["tr_loss"]) < float(s["target"])))
        fit = ("each trained until its training loss is equally small" if reached else
               "each trained until its training loss is small, or for at most four thousand epochs")
        batches = (f"Large batches do end sharper: on average {big:.1f} against {small:.2f} for batches of four. "
                   if big > small else
                   f"Here large batches end flatter, not sharper: {big:.2f} against {small:.2f} for batches of four. ")
        if flat_better:
            corr = (f"And the sharper networks do worse on new points: a rank correlation of {rho:+.2f}. The "
                    "flat-minima story holds here. ")
        else:
            lean = ("If anything, the sharper ones generalize better here. " if rho < -0.3 else
                    "Sharpness tells us almost nothing here. ")
            corr = ("But the sharper networks are not the worse ones: the rank correlation between sharpness and "
                    f"test error is {rho:+.2f}. {lean}")
        with self.voiceover(
            f"Test it, small. {len(lam)} networks learn from {s['n']} points labelled by a teacher network, with "
            f"four batch sizes, two step sizes and three seeds, {fit}. Sharpness is the largest eigenvalue of the "
            "training loss's Hessian, measured with part four's Hessian-vector products. <bookmark mark='a'/> "
            + batches + "<bookmark mark='b'/> " + corr
            + "Large studies agree on that much: across many settings, sharpness predicts generalization "
            "inconsistently, as Andriushchenko and colleagues found in 2023."
        ) as vo:
            self.play(FadeIn(setup), FadeIn(G), FadeIn(key[:-1]), FadeIn(key[-1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.06), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rescale(self):
        s = load("sharp")
        al, rs = [float(a) for a in s["alphas"]], np.asarray(s["resc"])
        G = axes([-0.5, len(al) - 0.5], [0, math.ceil(math.log10(rs.max()) * 2) / 2], x_length=5.6, y_length=3.6,
                 xticks=list(range(len(al))), xfmt=lambda v: f"{al[int(round(v))]:g}", yticks=[0, 0.5, 1, 1.5],
                 yfmt=lambda v: f"{10 ** v:.2g}", xlabel=r"$a$: \ first layer $\times a$, \ second $\div a$",
                 ylabel=r"top Hessian eigenvalue \ (log scale)", center=(3.3, -0.6, 0))
        ax = G.ax
        bs = bars(ax, np.arange(len(al)), np.log10(rs), 0.6, C.SURPRISE, 0.85)
        vals = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=WHITE).next_to(b_, UP, buff=0.06)
                        for b_, v in zip(bs, rs)])
        rows = [
            cmath(r"\operatorname{ReLU}(a z)", r"=", r"a \operatorname{ReLU}(z)", font_size=34),
            cmath(r"\tfrac1a W_2 \operatorname{ReLU}(a W_1 x)", r"=", r"W_2 \operatorname{ReLU}(W_1 x)", font_size=34),
        ]
        whys = [why(r"for $a > 0$"), why(r"the same function, \ for every $x$")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-3.4, buff=0.6, edge=6.9)
        same = label(rf"largest change in any output: \ ${sci(max(s['same'], 1e-16), 0)}$", font_size=22, color=GREY_A)
        same.next_to(rows[1], DOWN, buff=1.0).align_to(rows[1], LEFT)
        hist = VGroup(
            history_card(2017, r"L.~Dinh, R.~Pascanu, S.~Bengio \& Y.~Bengio", r"\textit{Sharp Minima Can "
                         r"Generalize for Deep Nets}", width=5.6, font_size=17, color=HIST),
            history_card(2021, r"P.~Foret et al., \ SAM", r"train to minimize the worst loss in a small ball \ "
                         r"(sharpness-aware)", width=5.6, font_size=17, color=HIST),
        ).arrange(DOWN, buff=0.15).to_corner(DL, buff=0.25)
        rng_ = rs.max() / rs.min()
        exactly = ("to rounding error on every output" if s["same"] < 1e-4 else
                   f"to within {s['same']:.3f} on every output")
        with self.voiceover(
            "There's a deeper problem, pointed out by Dinh, Pascanu and the Bengios in 2017. <bookmark mark='a'/> A "
            "ReLU passes a positive scale straight through. <bookmark mark='b'/> So multiply the first layer by a, "
            f"divide the second by a, and the network computes exactly the same function, {exactly}. Same "
            "predictions, same test error. "
            f"<bookmark mark='c'/> But its sharpness changes by a factor of {rng_:.0f} across these rescalings. "
            "Sharpness, as measured, depends on how the weights are written down, not only on what the network "
            "does, so it can't be the whole explanation. Scale-invariant versions, and training that seeks flat "
            "regions on purpose, like sharpness-aware minimization, came next; what sharpness has to do with the "
            "step size is part eleven's edge of stability."
        ) as vo:
            self.play(FadeIn(hist[0], shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(G), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bs], lag_ratio=0.2), run_time=1.8)
            self.play(FadeIn(vals))
            self.play(FadeIn(hist[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
