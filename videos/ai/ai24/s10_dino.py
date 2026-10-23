from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (DINO_C, NAIVE, PART, SIMCLR, STUDENT, TEACHER, arrow, axes, bars_chart, curve,
                                   load, node_box, pct, take_away)

VAR = {"dino": (r"DINO", DINO_C), "nocenter": (r"no centring", "#FF5C5C"), "nosharpen": (r"no sharpening", "#4DABF7")}


class DINO(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.two_collapses()
        self.measure()
        self.bars()
        self.results()

    def card(self):
        card = chapter_card(9, r"Self-distillation: \ DINO", r"A student, a teacher, \ and two ways to collapse",
                            lit=(), part=PART)
        with self.voiceover("Chapter nine. Self-distillation: DINO."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_(self):
        st = VGroup(node_box(r"student", STUDENT, font_size=24), node_box(r"$K$ prototypes", STUDENT, font_size=22),
                    node_box(r"softmax$\,/\,\tau_s$", STUDENT, font_size=22)).arrange(RIGHT, buff=0.55)
        st.move_to([-1.3, 1.3, 0])
        te = VGroup(node_box(r"teacher", TEACHER, font_size=24), node_box(r"$K$ prototypes", TEACHER, font_size=22),
                    node_box(r"centre, \ softmax$\,/\,\tau_t$", TEACHER, font_size=22)).arrange(RIGHT, buff=0.55)
        te.move_to([-1.3, -1.0, 0])
        for a, b in zip(te, st):
            a.set_x(b.get_x())
        x1 = label(r"view 1", font_size=22, color=GREY_A).next_to(st[0], LEFT, buff=0.5)
        x2 = label(r"view 2", font_size=22, color=GREY_A).next_to(te[0], LEFT, buff=0.5)
        arrs = VGroup(arrow(x1.get_right(), st[0].get_left()), arrow(st[0].get_right(), st[1].get_left()),
                      arrow(st[1].get_right(), st[2].get_left()), arrow(x2.get_right(), te[0].get_left()),
                      arrow(te[0].get_right(), te[1].get_left()), arrow(te[1].get_right(), te[2].get_left()))
        loss = node_box(r"$-\sum_k P_t^{(k)} \log P_s^{(k)}$", C.LOSS, font_size=24).move_to([5.0, 0.15, 0])
        l1 = arrow(st[2].get_right(), loss.get_top() + LEFT * 0.4, color=STUDENT)
        l2 = arrow(te[2].get_right(), loss.get_bottom() + LEFT * 0.4, color=TEACHER)
        ema = label(r"teacher $=$ a slow moving average of the student", font_size=20, color=TEACHER).next_to(
            te, DOWN, buff=0.35).align_to(te, LEFT)
        hist = label(r"DeepCluster (2018): \ cluster, \ then learn the clusters; \ SwAV (2020): \ assign views to "
                     r"prototypes", font_size=20, color=GREY_B).to_edge(UP, buff=0.4)
        src = cite(r"Caron et al.\ (2021): \ DINO, \ ``self-distillation with no labels''")
        with self.voiceover(
            "Mathilde Caron and colleagues at Facebook had spent years teaching networks by clustering: group the "
            "images, then learn to predict the groups. <bookmark mark='a'/> In 2021 they turned it into "
            "distillation without labels: DINO. A student network sees one view <bookmark mark='b'/> and outputs a "
            "probability over K prototypes, learned directions in its space. <bookmark mark='c'/> A teacher sees the "
            "other view and does the same, <bookmark mark='d'/> and the student is trained to match the teacher's "
            "probabilities, with a cross-entropy. The teacher is not trained at all: its weights are a moving "
            "average of the student's, as in BYOL."
        ) as vo:
            self.play(FadeIn(hist), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(x1), FadeIn(st[0]), GrowArrow(arrs[0]))
            vo.wait_until("b")
            self.play(FadeIn(st[1:]), GrowArrow(arrs[1]), GrowArrow(arrs[2]))
            vo.wait_until("c")
            self.play(FadeIn(x2), FadeIn(te), *[GrowArrow(a) for a in arrs[3:]])
            vo.wait_until("d")
            self.play(FadeIn(loss), GrowArrow(l1), GrowArrow(l2), FadeIn(ema))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_collapses(self):
        K = 12
        one = np.zeros(K)
        one[3] = 1.0
        uni = np.ones(K) / K

        def bars(p, col, x):
            g = VGroup(*[Rectangle(width=0.16, height=max(2.0 * v, 0.02), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85) for v in p]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)
            return g.move_to([x, 0.6, 0], aligned_edge=DOWN)

        b1, b2 = bars(one, VAR["nocenter"][1], -4.2), bars(uni, VAR["nosharpen"][1], 4.2)
        t1 = label(r"one prototype wins \\ for every image", font_size=22, color=VAR["nocenter"][1]).next_to(b1, DOWN,
                                                                                                         buff=0.25)
        t2 = label(r"every prototype equal \\ for every image", font_size=22, color=VAR["nosharpen"][1]).next_to(
            b2, DOWN, buff=0.25)
        f1 = MathTex(r"P_t", r"=", r"\operatorname{softmax}\!\big(", r"(g_t(x) - c)", r"/\, \tau_t", r"\big)",
                     font_size=38).move_to([0, 1.9, 0])
        f1[3].set_color(VAR["nocenter"][1])
        f1[4].set_color(VAR["nosharpen"][1])
        c1 = label(r"centring: \ $c \leftarrow 0.9\,c + 0.1\,\overline{g_t(x)}$ \\ no prototype can win for everyone "
                   r"\\ (pushes toward the right)", font_size=21, color=VAR["nocenter"][1]).move_to([0, 0.3, 0])
        c2 = label(r"sharpening: \ $\tau_t = 0.04 < \tau_s = 0.1$ \\ the teacher is more confident than the student "
                   r"\\ (pushes toward the left)", font_size=21, color=VAR["nosharpen"][1]).move_to([0, -1.3, 0])
        dec = MathTex(r"H(P_t, P_s)", r"=", r"H(P_t)", r"+", r"\mathrm{KL}(P_t \,\|\, P_s)", font_size=34)
        dec.to_edge(DOWN, buff=0.5)
        dec[2].set_color(TEACHER)
        dl = label(r"collapse: \ $\mathrm{KL} \to 0$, \ with $H(P_t)$ at $0$ or at $\log K$", font_size=21,
                   color=GREY_A).next_to(dec, UP, buff=0.15)
        with self.voiceover(
            "A student copying a teacher that copies the student can collapse in two opposite ways. <bookmark "
            "mark='a'/> One prototype can win for every image: the teacher says the same thing with full "
            "confidence. <bookmark mark='b'/> Or every prototype can be equally likely for every image: the "
            "teacher says nothing at all. <bookmark mark='c'/> DINO's answer is two opposing pressures on the "
            "teacher. Centring subtracts a running average of the teacher's outputs, so no prototype can win for "
            "everyone; on its own it drifts toward the uniform answer. <bookmark mark='d'/> Sharpening gives the "
            "teacher a lower temperature than the student, so its answers are more confident; on its own it "
            "drifts toward the single winner. <bookmark mark='e'/> The loss splits into the teacher's entropy and "
            "the KL between the two; either collapse drives the KL to zero, with the entropy stuck at one end."
        ) as vo:
            self.play(FadeIn(b1))
            vo.wait_until("a")
            self.play(FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(t2))
            vo.wait_until("c")
            self.play(Write(f1), FadeIn(c1))
            vo.wait_until("d")
            self.play(FadeIn(c2))
            vo.wait_until("e")
            self.play(Write(dec), FadeIn(dl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        d = load("dino")
        runs, keys = d["runs"], d["keys"]
        K = int(d["K"])
        S_ = runs[keys["dino"][0]]["steps"][-1]
        logK = math.log(K)

        def logc(k, f):
            r = runs[k]
            xs = [s for s, lg in zip(r["steps"], r["logs"]) if lg]
            ys = [lg[f] for lg in r["logs"] if lg]
            return xs, ys

        a1 = axes([0, S_], [0, 6], x_length=5.4, y_length=3.0, xlabel=r"training step",
                  ylabel=r"teacher entropy $H(P_t)$, \ nats", xticks=[0, S_], yticks=[0, 2, 4, 6], center=[-3.3, -0.4, 0])
        kmax = max(max(logc(k, "KL")[1]) for ks in keys.values() for k in ks)
        a2 = axes([0, S_], [0, max(0.5, kmax * 1.1)], x_length=5.4, y_length=3.0, xlabel=r"training step",
                  ylabel=r"$\mathrm{KL}(P_t \,\|\, P_s)$, \ nats", xticks=[0, S_], center=[3.3, -0.4, 0])
        top = DashedLine(a1.ax.c2p(0, logK), a1.ax.c2p(S_, logK), color=GREY_B, stroke_width=1.5)
        tl = MathTex(rf"\log {K}", font_size=24, color=GREY_B).next_to(top, UP, buff=0.05).align_to(top, LEFT)
        c1, c2 = VGroup(), VGroup()
        for name, ks in keys.items():
            col = VAR[name][1]
            for i, k in enumerate(ks):
                w = 3 if i == 0 else 1.6
                c1.add(curve(a1.ax, *logc(k, "H"), col, w))
                c2.add(curve(a2.ax, *logc(k, "KL"), col, w))
        leg = VGroup(*[label(VAR[n][0], font_size=22, color=VAR[n][1]) for n in keys]).arrange(RIGHT, buff=0.6)
        leg.to_edge(UP, buff=0.5)
        Hn = {n: float(np.mean([logc(k, "H")[1][-1] for k in ks])) for n, ks in keys.items()}
        KLn = {n: float(np.mean([logc(k, "KL")[1][-1] for k in ks])) for n, ks in keys.items()}
        ok = Hn["nocenter"] < 0.3 and Hn["nosharpen"] > logK - 0.2 and 0.3 < Hn["dino"] < logK - 0.2
        v = (f"Without centring, the teacher's entropy falls to {Hn['nocenter']:.2f}: one prototype for everything. "
             f"Without sharpening, it rises to {Hn['nosharpen']:.2f}, the log of {K}: every prototype equal. In both, "
             f"the KL drops to nearly zero and the student has nothing left to learn. With both, the entropy settles "
             f"at {Hn['dino']:.2f} and the KL stays at {KLn['dino']:.2f}: there is still something to learn." if ok else
             f"The teacher's entropy ends at {Hn['nocenter']:.2f} without centring, {Hn['nosharpen']:.2f} without "
             f"sharpening, and {Hn['dino']:.2f} with both.")
        tg = tag(r"computed: \ $K = 256$; \ DINO three seeds, \ each ablation two")
        with self.voiceover(
            "We trained DINO, and DINO with each half of the balance removed. <bookmark mark='a'/> On the left, the "
            "entropy of the teacher's answers; on the right, the KL between teacher and student. <bookmark "
            f"mark='b'/> {v}"
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(leg), Create(top), FadeIn(tl), FadeIn(tg))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bars(self):
        d = load("dino")
        K = int(d["K"])
        steps = np.asarray(d["rec_steps"])
        n = len(steps)
        tr = ValueTracker(0)
        panels = VGroup()
        W, H = 3.8, 2.4
        for j, name in enumerate(("nocenter", "dino", "nosharpen")):
            P = np.asarray(d[f"{name}_Pmean"])
            used = np.asarray(d[f"{name}_used"])
            col = VAR[name][1]
            x0 = -4.6 + j * 4.6
            frame = Rectangle(width=W, height=H, stroke_color=GREY_D, stroke_width=1).move_to([x0, -0.2, 0])

            def make(P=P, col=col, frame=frame):
                i = int(np.clip(round(tr.get_value()), 0, n - 1))
                p = P[i][:64]
                vmax = 0.5
                g = VGroup()
                bw = W / 64
                for k_, v in enumerate(p):
                    h = max(H * min(v / vmax, 1.0), 0.004)
                    g.add(Rectangle(width=bw * 0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                        frame.get_corner(DL) + RIGHT * (bw * (k_ + 0.5)) + UP * h / 2))
                return g

            bars = always_redraw(make)
            nm = label(VAR[name][0], font_size=24, color=col).next_to(frame, UP, buff=0.15)
            us = always_redraw(lambda used=used, frame=frame, col=col: label(
                rf"prototypes in use: \ ${np.exp(0) * used[int(np.clip(round(tr.get_value()), 0, n - 1))]:.1f}$",
                font_size=20, color=col).next_to(frame, DOWN, buff=0.15))
            panels.add(VGroup(frame, bars, nm, us))
        head = label(r"The teacher's average answer over $512$ test digits, \ top $64$ of $256$ prototypes", font_size=26)
        head.to_edge(UP, buff=0.5)
        st = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(tr.get_value()), 0, n - 1))]}$",
                                         font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6))
        u = {nm_: float(np.asarray(d[f"{nm_}_used"])[-1]) for nm_ in ("dino", "nocenter", "nosharpen")}
        with self.voiceover(
            "The same story, as the teacher's average answer over five hundred and twelve test digits, sorted "
            "from the most used prototype down. <bookmark mark='a'/> Without centring, one bar takes everything: "
            f"by the end, {u['nocenter']:.1f} prototypes in use. Without sharpening, the bars flatten, and all "
            f"{u['nosharpen']:.0f} are equally used, by every digit alike. <bookmark mark='b'/> DINO keeps "
            f"{u['dino']:.0f} prototypes in use across the digits, while each digit's own answer stays confident."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panels), FadeIn(st))
            vo.wait_until("a")
            self.play(tr.animate.set_value(n - 1), run_time=max(3.0, vo.until("b")), rate_func=linear)
        for m in panels:
            m[1].clear_updaters()
            m[3].clear_updaters()
        st.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = load("dino")
        s = load("simclr")
        ds, ss = d["summary"]["dino"], s["summary"]["0.2"]
        rows = [(r"SimCLR", SIMCLR, ss), (r"DINO", DINO_C, ds)]
        tab = VGroup()
        hdr = VGroup(label(r"", font_size=22), label(r"linear probe", font_size=22, color=GREY_A),
                     label(r"$k$-NN", font_size=22, color=GREY_A), label(r"10 labels per digit", font_size=22,
                                                                        color=GREY_A))
        tab.add(hdr)
        for n_, c_, sm in rows:
            tab.add(VGroup(label(n_, font_size=28, color=c_), MathTex(pct(sm["linear"][0]) + r"\%", font_size=32),
                           MathTex(pct(sm["knn"][0]) + r"\%", font_size=32),
                           MathTex(pct(sm["few"][0]) + r"\%", font_size=32)))
        xs = [-4.6, -1.6, 1.0, 3.8]
        for i, r_ in enumerate(tab):
            for j, m in enumerate(r_):
                m.move_to([xs[j], 2.2 - 0.75 * i, 0])
        behind = ds["linear"][0] < ss["linear"][0] - 0.005
        v = (f"At our small budget DINO is behind SimCLR: {pct(ds['linear'][0])} percent against "
             f"{pct(ss['linear'][0])} on the linear probe. Self-distillation is known to need long training, and "
             "the DINO paper's own runs were hundreds of epochs; ours is a few." if behind else
             f"At our budget DINO reaches {pct(ds['linear'][0])} percent on the linear probe, against SimCLR's "
             f"{pct(ss['linear'][0])}.")
        lit = label(r"DINO on ImageNet: \ $78.3\%$ by $k$-NN with a small ViT, \ $80.1\%$ linear with ViT-B; \\ and "
                    r"its attention maps outline objects, \ with no labels and no masks", font_size=22,
                    color=GREY_A).move_to([0, -0.9, 0])
        tk = take_away(r"self-distillation avoids collapse by balancing two opposite collapses")
        with self.voiceover(
            f"And the representation? <bookmark mark='a'/> {v} <bookmark mark='b'/> On ImageNet with vision "
            "transformers, DINO was a turning point: 78.3 percent by nearest neighbours with a small model, and the "
            "attention of its last layer traced the outlines of objects, though nobody had ever shown it an outline."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(tab[2], color=DINO_C, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeIn(lit))
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
