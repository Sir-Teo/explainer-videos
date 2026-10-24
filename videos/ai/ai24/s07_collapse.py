from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (NEG as NEGC, POS as POSC, BARLOW, BYOL_C, DIGIT, DINO_C, Hypersphere, NAIVE, PART, SIMCLR, SIMSIAM, axes,
                                   curve, load, node_box, pct, seed_curves, tag, take_away, take_away_in)


class Collapse(VoiceoverScene):
    def construct(self):
        self.card()
        self.predict()
        self.measure()
        self.spectra()
        self.starved()
        self.margin()
        self.routes()

    def card(self):
        card = chapter_card(6, r"Collapse", r"Why not just pull the two views together?", lit=(), part=PART)
        with self.voiceover("Chapter six. Collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def predict(self):
        sp = load("sphere")
        Z = np.asarray(sp["naive_z"])
        lab = np.asarray(sp["labels"]).astype(int)
        steps = np.asarray(sp["rec_steps"])
        n = len(steps)
        pc = pause_card(r"Train a network only to give the two views of each digit the same vector: \ no negatives, "
                        r"\ nothing else. \ What does it learn?", width=9.0, font_size=28)
        f = MathTex(r"\mathcal L", r"=", r"-\cos\big(z, z'\big)", font_size=44).move_to([3.6, 1.6, 0])
        f[2].set_color(NAIVE)
        hs = Hypersphere(Z, [DIGIT[c] for c in lab], radius=2.6, center=[-3.0, -0.4, 0], dot=0.045)
        hs.angle.set_value(0.3)
        sp_ = load("sphere")
        st = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(hs.t.get_value()), 0, n - 1))]}$",
                                         font_size=22, color=GREY_A).move_to([-3.0, 3.1, 0]))
        lossl = label(r"the loss reaches its minimum, $-1$, \\ and stays there", font_size=24, color=NAIVE)
        lossl.next_to(f, DOWN, buff=0.5)
        same = label(r"every digit, \ the same point", font_size=28, color=NAIVE).next_to(lossl, DOWN, buff=0.6)
        tg = tag(r"computed: \ the naive siamese net, \ three output numbers")
        U = Z / np.linalg.norm(Z, axis=2, keepdims=True)
        r0, r1 = float(np.linalg.norm(U[0].mean(0))), float(np.linalg.norm(U[-1].mean(0)))
        if r0 > 0.99 and r1 > 0.99:
            how = ("Like the contrastive network, it starts with every digit bunched in one spot; <bookmark "
                   "mark='b'/> unlike it, it never leaves.")
        else:
            how = "It minimizes it <bookmark mark='b'/> by sending every digit to the same point."
        with self.voiceover(
            "Before going further, a question. Suppose the only rule is: give the two views of each digit the same "
            "vector. No negatives, nothing pushing apart. What does the network learn? Pause and think. <bookmark "
            "mark='a'/> Here is what ours did. The loss is minus the cosine between the two views' vectors. "
            f"{how} The two views agree perfectly, the loss sits at its minimum, and the vector says nothing at all "
            "about the input. This is collapse."
        ) as vo:
            self.play(FadeIn(pc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(pc), FadeIn(hs), FadeIn(st), Write(f), FadeIn(tg))
            vo.wait_until("b")
            self.play(hs.t.animate.set_value(n - 1), hs.angle.animate.set_value(2.8), run_time=4.0,
                      rate_func=lambda u: u ** 0.5)
            self.play(FadeIn(lossl), FadeIn(same))
            self.play(hs.angle.animate.set_value(4.0), run_time=max(0.5, vo.remaining()), rate_func=linear)
        hs.freeze()
        st.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        c = load("collapse")
        s = load("simclr")
        runs_c, kn = c["runs"], c["keys"]["naive"]
        runs_s, ks = s["runs"], s["keys"]["0.2"]
        d = definition_card(r"effective rank",
                            cmath(r"\operatorname{erank}(Z) = \exp\Big(-\sum_k p_k \log p_k\Big), \quad "
                                  r"p_k = \frac{\sigma_k}{\sum_j \sigma_j}", font_size=30),
                            width=6.4, font_size=22)
        dn = label(r"$\sigma_k$: \ singular values of the vectors of $2{,}000$ test digits; \\ $1$ when every vector "
                   r"points the same way, \\ up to $d$ when they fill all $d$ dimensions", font_size=20, color=GREY_A)
        VGroup(d, dn).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.4, 0.5, 0])
        src = cite(r"Roy \& Vetterli (2007); \ RankMe: \ Garrido et al.\ (2023)")
        S_ = runs_s[ks[0]]["steps"][-1]
        top = 20 * math.ceil(max(max(runs_s[k]["zrank"]) for k in ks) / 20 + 0.25)
        ax = axes([0, S_], [0, top], x_length=4.8, y_length=3.0, xlabel=r"training step",
                  ylabel=r"effective rank of $z$", xticks=[0, S_], yticks=list(range(0, top + 1, 20)),
                  center=[3.6, 0.5, 0])
        c1 = seed_curves(ax.ax, runs_s, ks, "zrank", SIMCLR)
        c2 = seed_curves(ax.ax, runs_c, kn, "zrank", NAIVE)
        leg = VGroup(label(r"SimCLR", font_size=20, color=SIMCLR), label(r"pull together only", font_size=20,
                                                                         color=NAIVE)).arrange(RIGHT, buff=0.5)
        leg.next_to(ax, DOWN, buff=0.15)
        r_n = float(np.mean([runs_c[k]["final"]["rank_z"] for k in kn]))
        r_s = float(np.mean([runs_s[k]["final"]["rank_z"] for k in ks]))
        dim = 128
        times = (1 / np.sqrt(dim)) / float(np.mean([runs_c[k]["zspread"][-1] for k in kn]))
        if r_n < 1.5:
            tail = f"The pull-together-only network falls to {r_n:.1f}: one direction."
        else:
            tail = (f"The pull-together-only network falls to {r_n:.1f}, and even that is mostly noise: its vectors "
                    f"are spread {times:.0f} times less than points scattered evenly over the sphere.")
        with self.voiceover(
            "To see collapse in a network with many output numbers, we need a measure. The effective rank takes "
            "the singular values of a set of vectors, turns them into proportions, and asks how many directions "
            "carry the weight: one, if every vector points the same way, up to the dimension, if they fill the "
            "space. <bookmark mark='a'/> SimCLR keeps its vectors spread over about "
            f"{r_s:.0f} of its {dim} dimensions. <bookmark mark='b'/> {tail}"
        ) as vo:
            self.play(FadeIn(d), FadeIn(dn), FadeIn(src), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(leg), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectra(self):
        c = load("collapse")
        sv_s = np.asarray(c["simclr_spectrum"], float)
        sv_n = np.asarray(c["naive_spectrum"], float)
        k = np.arange(1, len(sv_s) + 1)
        lg = lambda v: np.log10(np.maximum(v / v[0], 1e-6))  # noqa: E731
        ax = axes([0, len(k)], [-6, 0], x_length=8.0, y_length=4.2, xlabel=r"direction $k$, \ largest first",
                  ylabel=r"$\sigma_k / \sigma_1$", xticks=[1, 32, 64, 96, 128], yticks=[-6, -4, -2, 0],
                  yfmt=lambda v: f"10^{{{int(v)}}}", center=[-1.0, -0.3, 0])
        cs = curve(ax.ax, k, lg(sv_s), SIMCLR, 3)
        cn = curve(ax.ax, k, lg(sv_n), NAIVE, 3)
        cliff = int(np.argmax(lg(sv_s) < -3)) + 1 if np.any(lg(sv_s) < -3) else len(sv_s)
        ls = label(r"SimCLR: \ a slow decline, \\ then a cliff" if cliff < len(sv_s) else r"SimCLR: \ a slow decline",
                   font_size=22, color=SIMCLR).move_to([4.8, 1.2, 0])
        ln = label(r"pull together only: \\ one direction, \ then noise", font_size=22, color=NAIVE)
        ln.move_to([4.8, -1.4, 0])
        kinds = VGroup(label(r"complete collapse: \ one point", font_size=22, color=NAIVE),
                       label(r"dimensional collapse: \ a few directions", font_size=22, color=SIMCLR))
        kinds.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        src = cite(r"Hua et al.\ (2021); \ Jing, Vincent, LeCun \& Tian (2022)", corner=UR)
        drop = (f"SimCLR declines slowly and then drops off a cliff: after about {cliff} directions, the rest are a "
                "thousand times weaker than the first." if cliff < len(sv_s) else
                "SimCLR declines slowly, and its weakest directions end far below its strongest.")
        with self.voiceover(
            "The whole spectrum shows more. These are the singular values of the two networks' vectors, largest "
            "first, on a log scale. <bookmark mark='a'/> The collapsed network has one direction and then "
            f"only noise. <bookmark mark='b'/> {drop} Even contrastive learning leaves part of the space unused. This "
            "is called dimensional collapse, the milder cousin of complete collapse; Li Jing, Yann LeCun and "
            "colleagues traced it to strong augmentations and to the way the layers' weights evolve together."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(cn), FadeIn(ln))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(ls), run_time=1.6)
            self.play(FadeIn(kinds))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def starved(self):
        c = load("collapse")
        b = load("baselines")
        runs, kn = c["runs"], c["keys"]["naive"]
        S_ = runs[kn[0]]["steps"][-1]
        ax = axes([0, S_], [0.4, 1.0], x_length=6.0, y_length=3.4, xlabel=r"training step",
                  ylabel=r"$k$-NN accuracy of $h$ (quick test)", xticks=[0, S_], yticks=[0.4, 0.6, 0.8, 1.0],
                  center=[-2.2, -0.2, 0])
        cn = seed_curves(ax.ax, runs, kn, "knn", NAIVE)
        k0 = float(np.mean([runs[k]["knn"][0] for k in kn]))
        k1 = float(np.mean([runs[k]["knn"][-1] for k in kn]))
        base = DashedLine(ax.ax.c2p(0, k0), ax.ax.c2p(S_, k0), color=GREY_B, stroke_width=1.5)
        bl = label(r"untrained", font_size=20, color=GREY_B).next_to(base, UP, buff=0.08).align_to(base, RIGHT)
        fl_ = float(np.mean([runs[k]["final"]["linear"] for k in kn]))
        un = float(np.mean([r["linear"] for r in b["random_cnn"]]))
        worse = k1 < k0 - 0.02
        exp_ = label(r"once the head's output is constant, \\ the gradient is zero: \\ the encoder below "
                     r"learns nothing more", font_size=22, color=GREY_A).move_to([4.2, 0.6, 0])
        if worse and fl_ < un + 0.005:
            v = (f"Its nearest-neighbour accuracy falls from {pct(k0, 0)} percent, where the random network started, "
                 f"to {pct(k1, 0)}. Its linear probe ends at {pct(fl_)} percent; an untrained network scores "
                 f"{pct(un)}. Training bought nothing.")
        else:
            v = (f"Its nearest-neighbour accuracy goes from {pct(k0, 0)} to {pct(k1, 0)} percent, and its linear "
                 f"probe ends at {pct(fl_)}, against {pct(un)} for an untrained network.")
        with self.voiceover(
            "Collapse is not harmless to the network underneath. The collapsed vector is the output of a small "
            "head; below it, the encoder's representation h is what we would keep. <bookmark mark='a'/> "
            f"{v} <bookmark mark='b'/> Once the head's output is the same for everything, the loss is at its "
            "minimum and its gradient vanishes: the encoder is left wherever the first steps of collapse dropped "
            "it."
        ) as vo:
            self.play(FadeIn(ax), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(cn), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(exp_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def margin(self):
        f = MathTex(r"\mathcal L", r"=", r"y\, d^2", r"+", r"(1 - y)\, \max(0,\, m - d)^2", font_size=40)
        f.move_to([0, 2.2, 0])
        f[2].set_color(POSC)
        f[4].set_color(NEGC)
        dl = label(r"$d$: \ distance between two outputs; \ $y = 1$ for a similar pair, \ $0$ for a dissimilar one",
                   font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.3)
        ax = axes([0, 3], [0, 4.5], x_length=5.0, y_length=2.6, xlabel=r"distance $d$", ylabel=r"loss",
                  center=[0, -1.3, 0])
        ds = np.linspace(0, 3, 120)
        c1 = curve(ax.ax, ds, ds ** 2 / 2, POSC, 3)
        c2 = curve(ax.ax, ds, np.maximum(0, 2.0 - ds) ** 2, NEGC, 3)
        l1 = label(r"similar: \ pull together", font_size=20, color=POSC).next_to(ax.ax.c2p(2.6, 3.4), LEFT, buff=0.1)
        l2 = label(r"dissimilar: \ push to the margin $m$", font_size=20, color=NEGC).next_to(ax.ax.c2p(0.3, 3.9),
                                                                                             RIGHT, buff=0.1)
        src = cite(r"Hadsell, Chopra \& LeCun (2006); \ Chopra, Hadsell \& LeCun (2005)")
        with self.voiceover(
            "This trap is old. In 2005 and 2006 Raia Hadsell, Sumit Chopra and Yann LeCun trained siamese networks "
            "with a loss that already had both halves. <bookmark mark='a'/> For a similar pair, the squared distance "
            "between their outputs: pull together. <bookmark mark='b'/> For a dissimilar pair, a penalty only if they "
            "come closer than a margin: push apart, but no further than needed. Without the second half, nothing "
            "would stop the network from mapping everything to one point."
        ) as vo:
            self.play(Write(f), FadeIn(dl), FadeIn(src), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(l1), Indicate(f[2], color=POSC))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2), Indicate(f[4], color=NEGC))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def routes(self):
        head = label(r"Four ways to stop collapse", font_size=36).to_edge(UP, buff=0.5)
        boxes = VGroup(
            node_box(r"negatives: \ push the others away \\ SimCLR, \ MoCo \ (chapters 4--5)", SIMCLR, font_size=26),
            node_box(r"asymmetry: \ a predictor and a stop-gradient \\ BYOL, \ SimSiam \ (chapter 7)", SIMSIAM,
                     font_size=26),
            node_box(r"decorrelation: \ spread every dimension \\ Barlow Twins, \ VICReg \ (chapter 8)", BARLOW,
                     font_size=26),
            node_box(r"centring and sharpening a teacher \\ DINO \ (chapter 9)", DINO_C, font_size=26),
        ).arrange_in_grid(2, 2, buff=(0.6, 0.9)).move_to(DOWN * 0.1)
        tk = take_away(r"agreement alone is solved by a constant: \ something must keep the vectors apart")
        with self.voiceover(
            "Every method from here on is a way out of this trap. <bookmark mark='a'/> The contrastive methods push "
            "other images away. <bookmark mark='b'/> BYOL and SimSiam break the symmetry between the two branches. "
            "<bookmark mark='c'/> Barlow Twins and VICReg demand that every dimension stays spread and "
            "uncorrelated. <bookmark mark='d'/> And DINO balances a teacher between two opposite collapses."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[i], shift=UP * 0.15))
            self.play(*take_away_in(self, tk))
        self.wait(0.3)
        self.clear_scene()
