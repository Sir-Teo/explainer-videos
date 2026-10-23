from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (BYOL_C, DIGIT, NAIVE, PART, SIMCLR, SIMSIAM, TARGET, Hypersphere, arrow, axes,
                                   bars_chart, load, node_box, pct, seed_curves, take_away)


class BYOL(VoiceoverScene):
    def construct(self):
        self.card()
        self.byol()
        self.simsiam()
        self.em()
        self.results()

    def card(self):
        card = chapter_card(7, r"No negatives: \ BYOL and SimSiam", r"How can a network that only pulls together "
                            r"not collapse?", lit=(), part=PART)
        with self.voiceover("Chapter seven. No negatives: BYOL and SimSiam."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def byol(self):
        y1, y2 = 1.2, -1.0
        on = VGroup(node_box(r"encoder", BYOL_C, font_size=22), node_box(r"projector", BYOL_C, font_size=22),
                    node_box(r"predictor", BYOL_C, font_size=22)).arrange(RIGHT, buff=0.6).move_to([-1.8, y1, 0])
        tg = VGroup(node_box(r"encoder", TARGET, font_size=22), node_box(r"projector", TARGET, font_size=22))
        tg.arrange(RIGHT, buff=0.6)
        tg[0].move_to([on[0].get_x(), y2, 0])
        tg[1].move_to([on[1].get_x(), y2, 0])
        x1 = label(r"view 1", font_size=22, color=GREY_A).next_to(on[0], LEFT, buff=0.6)
        x2 = label(r"view 2", font_size=22, color=GREY_A).next_to(tg[0], LEFT, buff=0.6)
        arr = VGroup(arrow(x1.get_right(), on[0].get_left()), arrow(on[0].get_right(), on[1].get_left()),
                     arrow(on[1].get_right(), on[2].get_left()), arrow(x2.get_right(), tg[0].get_left()),
                     arrow(tg[0].get_right(), tg[1].get_left()))
        loss = node_box(r"$\| \bar p - \bar z' \|^2$", C.LOSS, font_size=26).move_to([4.6, 0.1, 0])
        a1 = arrow(on[2].get_right(), loss.get_top() + LEFT * 0.3)
        a2 = arrow(tg[1].get_right(), loss.get_bottom() + LEFT * 0.3, color=TARGET)
        sg = label(r"stop-gradient", font_size=20, color=TARGET).next_to(a2, DOWN, buff=0.1)
        ema = label(r"a slow moving average of the online weights", font_size=20, color=TARGET)
        ema.next_to(tg, DOWN, buff=0.3).align_to(tg, LEFT)
        bar = label(r"$\bar{\ }$: \ unit length", font_size=18, color=GREY_B).next_to(loss, DOWN, buff=0.1)
        nl = label(r"online network", font_size=20, color=BYOL_C).next_to(on, UP, buff=0.2)
        tl = label(r"target network", font_size=20, color=TARGET).next_to(tg, UP, buff=0.2)
        res = label(r"no negatives; \ ResNet-50 on ImageNet: \ $74.3\%$ linear probe", font_size=24, color=BYOL_C)
        res.to_edge(DOWN, buff=0.5)
        src = cite(r"Grill et al.\ (2020): \ BYOL")
        with self.voiceover(
            "In June 2020 a DeepMind team led by Jean-Bastien Grill removed the negatives anyway. <bookmark "
            "mark='a'/> BYOL has two networks. The online network sees one view and, through an extra small "
            "network called the predictor, tries to predict <bookmark mark='b'/> what the target network makes of "
            "the other view. <bookmark mark='c'/> No gradient flows into the target; its weights are a slowly "
            "moving average of the online weights. <bookmark mark='d'/> Nothing pushes images apart, yet it did not "
            "collapse, and it beat SimCLR: 74.3 percent on ImageNet with a ResNet-50."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(x1), FadeIn(on), FadeIn(nl), *[GrowArrow(a) for a in arr[:3]])
            vo.wait_until("b")
            self.play(FadeIn(x2), FadeIn(tg), FadeIn(tl), *[GrowArrow(a) for a in arr[3:]], FadeIn(loss),
                      GrowArrow(a1), GrowArrow(a2), FadeIn(bar))
            vo.wait_until("c")
            self.play(FadeIn(sg), FadeIn(ema))
            vo.wait_until("d")
            self.play(FadeIn(res, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simsiam(self):
        c = load("collapse")
        sp = load("sphere")
        runs, K = c["runs"], c["keys"]
        lab = np.asarray(sp["labels"]).astype(int)
        S_ = runs[K["simsiam"][0]]["steps"][-1]
        top = max(max(runs[k]["zspread"]) for k in K["simsiam"] + K["simsiam_nosg"])
        ax = axes([0, S_], [0, top * 1.15], x_length=5.0, y_length=3.0, xlabel=r"training step",
                  ylabel=r"spread of $z$ \ (std of unit vectors)", xticks=[0, S_], center=[-3.0, -0.6, 0])
        c_sg = seed_curves(ax.ax, runs, K["simsiam"], "zspread", SIMSIAM)
        c_no = seed_curves(ax.ax, runs, K["simsiam_nosg"], "zspread", NAIVE)
        leg = VGroup(label(r"SimSiam", font_size=20, color=SIMSIAM),
                     label(r"the same, \ without the stop-gradient", font_size=20, color=NAIVE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.15)
        h1 = Hypersphere(np.asarray(sp["simsiam_z"])[-1], [DIGIT[c_] for c_ in lab], radius=1.35,
                         center=[2.4, -0.5, 0], dot=0.03)
        h2 = Hypersphere(np.asarray(sp["naive_z"])[-1], [DIGIT[c_] for c_ in lab], radius=1.35,
                         center=[5.4, -0.5, 0], dot=0.03)
        l1 = label(r"SimSiam, \\ three numbers", font_size=20, color=SIMSIAM).next_to(h1, UP, buff=0.2)
        l2 = label(r"pull together only, \\ three numbers", font_size=20, color=NAIVE).next_to(h2, UP, buff=0.2)
        f = MathTex(r"\mathcal L", r"=", r"-\tfrac12\cos\big(p_1, \mathrm{sg}(z_2)\big)", r"-",
                    r"\tfrac12\cos\big(p_2, \mathrm{sg}(z_1)\big)", font_size=34).to_edge(UP, buff=0.5)
        f[2].set_color(SIMSIAM)
        f[4].set_color(SIMSIAM)
        src = cite(r"Chen \& He (2021): \ SimSiam", corner=DR)
        sg_end = float(np.mean([runs[k]["zspread"][-1] for k in K["simsiam"]]))
        no_end = float(np.mean([runs[k]["zspread"][-1] for k in K["simsiam_nosg"]]))
        collapsed = no_end < 0.25 * sg_end
        r_sg = float(np.mean([runs[k]["final"]["rank_z"] for k in K["simsiam"]]))
        r_no = float(np.mean([runs[k]["final"]["rank_z"] for k in K["simsiam_nosg"]]))
        v = (f"With the stop-gradient, the spread holds at {sg_end:.3f}; without it, it falls to {no_end:.3f}, and "
             f"the effective rank to {r_no:.1f}, against {r_sg:.0f}. Remove one line of code and the network "
             "collapses." if collapsed else
             f"With the stop-gradient, the spread ends at {sg_end:.3f}; without it, at {no_end:.3f}.")
        with self.voiceover(
            "Five months later, Xinlei Chen and Kaiming He removed the moving average too. SimSiam is one network, "
            "applied to both views, with a predictor on one side and a stop-gradient on the other: the target "
            "vector is treated as a constant. <bookmark mark='a'/> We trained it, three times with the stop-gradient "
            f"and twice without. <bookmark mark='b'/> {v} <bookmark mark='c'/> On the sphere, with three output "
            "numbers, SimSiam keeps the digits apart without ever pushing on them, while the pull-together network "
            "sits on one point."
        ) as vo:
            self.play(Write(f), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(leg))
            vo.wait_until("b")
            self.play(Create(c_sg), Create(c_no), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(h1), FadeIn(h2), FadeIn(l1), FadeIn(l2))
            self.play(h1.angle.animate.set_value(2.5), h2.angle.animate.set_value(2.5),
                      run_time=max(1.0, vo.remaining()), rate_func=linear)
        h1.freeze()
        h2.freeze()
        self.clear_scene()

    # ------------------------------------------------------------------
    def em(self):
        cols = {r"\eta_x": TARGET, r"\theta": SIMSIAM}
        rows = [
            cmath(r"\mathcal L(\theta, \eta)", r"=", r"\mathbb E_{x, T}\,\big\|F_\theta(T(x)) - \eta_x\big\|^2",
                  font_size=36),
            cmath(r"\theta^{t}", r"\leftarrow", r"\arg\min_\theta\, \mathcal L(\theta, \eta^{t-1})", font_size=36),
            cmath(r"\eta_x^{t}", r"\leftarrow", r"\arg\min_\eta\, \mathcal L(\theta^t, \eta) = \mathbb E_T\big[F_{\theta^t}(T(x))\big]",
                  font_size=36),
            cmath(r"\eta_x^{t}", r"\approx", r"F_{\theta^t}(T'(x))", r",\quad", r"\text{predictor} \approx \mathbb E_T",
                  font_size=36),
        ]
        rows[0][2].set_color(SIMSIAM)
        rows[2][0].set_color(TARGET)
        rows[3][0].set_color(TARGET)
        whys = [why(r"a free target $\eta_x$ for every image"), why(r"targets fixed: \ a gradient step \ (the stop-gradient)"),
                why(r"weights fixed: \ the best target is the average view"),
                why(r"one sampled view stands in; \ the predictor learns the average")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-2.0, buff=0.55, edge=6.9)
        note_ = label(r"a constant is still a minimum: \ the alternation just does not walk there; \\ "
                      r"Tian, Chen \& Ganguli (2021): \ the predictor's dynamics keep the directions alive",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        src = cite(r"Chen \& He (2021)", corner=DR)
        with self.voiceover(
            "Why does one stop-gradient matter so much? Chen and He offered an explanation. Imagine a free target "
            "vector, eta, for every image, and a loss that pulls each view's output toward its image's target. "
            "<bookmark mark='a'/> Minimize it by turns. With the targets fixed, take a gradient step on the "
            "network: that is exactly what the stop-gradient does. <bookmark mark='b'/> With the network fixed, "
            "the best target is the average output over all views of the image. <bookmark mark='c'/> SimSiam uses "
            "one sampled view in place of the average, and the predictor learns to make up the difference. "
            "<bookmark mark='d'/> Collapsing to a constant still minimizes the loss; this way of descending simply "
            "does not lead there. Yuandong Tian, Xinlei Chen and Surya Ganguli worked out the dynamics: the "
            "predictor and the stop-gradient together keep the useful directions from dying."
        ) as vo:
            step(0)
            self.play(FadeIn(src))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(note_, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        c = load("collapse")
        s = load("simclr")
        sm = s["summary"]["0.2"]
        cs = c["summary"]
        names = [r"SimCLR", r"BYOL", r"SimSiam"]
        cols = [SIMCLR, BYOL_C, SIMSIAM]
        lin = [sm["linear"], cs["byol"]["linear"], cs["simsiam"]["linear"]]
        few = [sm["few"], cs["byol"]["few"], cs["simsiam"]["few"]]
        lo = float(np.floor((min(x[1] for x in lin) - 0.01) * 100) / 100)
        ch1 = bars_chart([x[0] for x in lin], cols, names, height=2.8, bar_w=0.8, gap=0.5, vmin=lo, vmax=1.0,
                         spread=[(x[1], x[2]) for x in lin], value_fmt=lambda v: pct(v), font_size=22)
        lo2 = float(np.floor((min(x[1] for x in few) - 0.02) * 50) / 50)
        ch2 = bars_chart([x[0] for x in few], cols, names, height=2.8, bar_w=0.8, gap=0.5, vmin=lo2, vmax=1.0,
                         spread=[(x[1], x[2]) for x in few], value_fmt=lambda v: pct(v), font_size=22)
        ch1.move_to([-3.4, -0.5, 0])
        ch2.move_to([3.4, -0.5, 0])
        t1 = label(rf"linear probe, \% \ (axis from ${pct(lo, 0)}$)", font_size=22, color=GREY_A).next_to(ch1, UP,
                                                                                                       buff=0.35)
        t2 = label(rf"10 labels per digit, \% \ (axis from ${pct(lo2, 0)}$)", font_size=22, color=GREY_A).next_to(
            ch2, UP, buff=0.35)
        tg = tag(r"computed: \ three seeds each; \ whiskers: lowest to highest")
        best = int(np.argmax([x[0] for x in lin]))
        leader = ["SimCLR", "BYOL", "SimSiam"][best]
        diff = max(x[0] for x in lin) - min(x[0] for x in lin)
        line = (f"At our budget the three land within {pct(diff)} points of each other on the linear probe, with "
                f"{leader} ahead." if diff < 0.01 else
                f"At our budget {leader} leads the linear probe, by {pct(diff)} points over the last.")
        tk = take_away(r"asymmetry, \ a predictor and a stop-gradient, \ is enough to escape collapse")
        with self.voiceover(
            f"How do they compare, on the same budget? <bookmark mark='a'/> {line} <bookmark mark='b'/> With ten "
            f"labels per digit: SimCLR {pct(few[0][0])}, BYOL {pct(few[1][0])}, SimSiam {pct(few[2][0])} percent. "
            "<bookmark mark='c'/> And one more twist: some suspected BYOL was secretly contrastive, through batch "
            "normalization, which mixes information across a batch. Its authors replaced it with a normalization "
            "that sees one image at a time, and reached 73.9 percent."
        ) as vo:
            self.play(FadeIn(t1), FadeIn(ch1[0]), FadeIn(ch1.names), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch1.bars], lag_ratio=0.2), FadeIn(ch1.whiskers),
                      FadeIn(ch1.vals))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(ch2[0]), FadeIn(ch2.names),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch2.bars], lag_ratio=0.2), FadeIn(ch2.whiskers),
                      FadeIn(ch2.vals))
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.1), FadeIn(cite(r"Richemond et al.\ (2020)", corner=UR)))
        self.wait(0.3)
        self.clear_scene()
