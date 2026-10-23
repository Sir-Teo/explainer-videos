from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, EBM, HIST, PART, band, curve, digit_sheet, load, rgb_of, to_image)

CD1, CD10, PCD = "#FF6B8B", C.BITS, "#5CD0B3"
NAMES = {"cd1": r"CD-1", "cd10": r"CD-10", "pcd": r"persistent CD"}
COLS = {"cd1": CD1, "cd10": CD10, "pcd": PCD}
SPOKEN = {"cd1": "CD-1", "cd10": "CD-10", "pcd": "persistent CD"}


def filter_sheet(W, rows, cols, size=0.42, gap=0.04) -> ImageMobject:
    """Weight vectors as 14 x 14 pictures: positive warm, negative cool, each scaled to its own range."""
    W = np.asarray(W)
    px = 14
    g = 1
    H, Wd = rows * px + (rows - 1) * g, cols * px + (cols - 1) * g
    img = np.ones((H, Wd, 3)) * rgb_of("#121722")[None, None]
    pos, neg, bg = rgb_of(EBM), rgb_of("#58A6FF"), rgb_of("#0B0F17")
    for k in range(min(len(W), rows * cols)):
        r, c = divmod(k, cols)
        w = W[k].reshape(14, 14)
        t = w / max(np.abs(w).max(), 1e-9)
        a = np.clip(t, 0, 1)[..., None]
        b = np.clip(-t, 0, 1)[..., None]
        img[r * (px + g): r * (px + g) + px, c * (px + g): c * (px + g) + px] = bg * (1 - a - b) + pos * a + neg * b
    return to_image(img, cols * size + (cols - 1) * gap, rows * size + (rows - 1) * gap)


class RBM(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.gradient()
        self.cd()
        self.exact()
        self.learned()

    def card(self):
        card = chapter_card(12, r"Contrastive divergence", r"How do you train a model whose normalizer you can't "
                            r"compute?", lit=(2002,), part=PART)
        with self.voiceover("Chapter twelve. Contrastive divergence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def machine(self):
        r = load("rbm")
        ex = np.asarray(r["binary_examples"])
        sheet = digit_sheet(ex[:8], 2, 4, size=0.5, gap=0.04).move_to([-4.6, 2.3, 0])
        sl = label(r"our digits, \ one bit per pixel", font_size=20, color=DATA).next_to(sheet, DOWN, buff=0.1)
        vis = VGroup(*[Square(0.16, stroke_color=DATA, stroke_width=1, fill_color=DATA, fill_opacity=0.2)
                       for _ in range(49)]).arrange_in_grid(7, 7, buff=0.03).move_to([-4.0, -1.6, 0])
        hid = VGroup(*[Circle(0.13, stroke_color=EBM, stroke_width=1.5, fill_color=EBM, fill_opacity=0.3)
                       for _ in range(16)]).arrange(RIGHT, buff=0.12).move_to([-2.3, 0.2, 0])
        edges = VGroup(*[Line(v.get_center(), h.get_center(), stroke_width=0.5, color=GREY_C).set_opacity(0.35)
                         for i, v in enumerate(vis) for j, h in enumerate(hid) if (i + 3 * j) % 7 == 0])
        vl = label(r"$196$ visible units $v$", font_size=20, color=DATA).next_to(vis, DOWN, buff=0.12)
        hl = label(r"$16$ hidden units $h$", font_size=20, color=EBM).next_to(hid, UP, buff=0.12)
        rows = VGroup(
            cmath(r"E(v, h)", r"=", r"-b^\top v - c^\top h - v^\top W h", font_size=34),
            cmath(r"p(h_j = 1 \mid v)", r"=", r"\sigma\big(c_j + W_{:j}^\top v\big)", font_size=32),
            cmath(r"p(v_i = 1 \mid h)", r"=", r"\sigma\big(b_i + W_{i:}\, h\big)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 1.6, 0])
        rows[0][0].set_color(EBM)
        nb = label(r"no connections within a layer: \ given one layer, \ the other's units are independent",
                   font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.3)
        card = history_card(1986, r"Smolensky: \ the harmonium", r"later renamed the restricted Boltzmann machine",
                            width=4.6, font_size=18).move_to([3.6, -2.2, 0])
        with self.voiceover(
            "The way out was to restrict the machine: two layers, visible and hidden, connected across but not "
            "within; Paul Smolensky's harmonium of 1986, today's restricted Boltzmann machine. <bookmark "
            "mark='a'/> One weight matrix couples the layers. <bookmark mark='b'/> Given one layer, the other's "
            "units are independent, each a sigmoid of its input. <bookmark mark='c'/> Ours: 196 visible units, our "
            "digits in black and white, and sixteen hidden units, for a reason you'll see."
        ) as vo:
            self.play(FadeIn(vis), FadeIn(hid), Create(edges), FadeIn(vl), FadeIn(hl), FadeIn(card))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), Write(rows[2]), FadeIn(nb))
            vo.wait_until("c")
            self.play(FadeIn(sheet), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        rows = [
            cmath(r"\log p(v)", r"=", r"-F(v)", r"-", r"\log Z", font_size=36),
            cmath(r"F(v)", r"=", r"-b^\top v - \sum_j \log\big(1 + e^{\, c_j + W_{:j}^\top v}\big)", font_size=34),
            cmath(r"\frac{\partial \log Z}{\partial \theta}", r"=", r"\mathbb E_{v \sim p}\Big[-\frac{\partial "
                  r"F(v)}{\partial \theta}\Big]", font_size=34),
            cmath(r"\frac{\partial \log p(v)}{\partial W}", r"=", r"\langle v\, h^\top \rangle_{\text{data}}", r"-",
                  r"\langle v\, h^\top \rangle_{\text{model}}", font_size=36),
        ]
        rows[3][2].set_color(DATA)
        rows[3][4].set_color(EBM)
        whys = [why(r"sum out $h$: \ the free energy $F$"), why(r"each hidden unit, \ summed out on its own"),
                why(r"$Z = \sum_v e^{-F(v)}$: \ an expectation under the model"),
                why(r"positive phase \ minus \ negative phase")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.45, edge=6.9)
        hard = label(r"the negative phase needs samples from the model itself", font_size=24, color=EBM)
        hard.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Sum the hidden units out: the log-probability of an image is minus its free energy, minus log Z. "
            "<bookmark mark='a'/> The free energy is a sum of softplus terms. <bookmark mark='b'/> The gradient of "
            "log Z is an average under the model. <bookmark mark='c'/> So the weights' gradient is the Boltzmann "
            "rule: data correlations minus model correlations. <bookmark mark='d'/> The second still needs samples "
            "from the model."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(hard))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cd(self):
        labels_ = [r"v_0", r"h_0", r"v_1", r"h_1", r"\cdots", r"v_k"]
        nodes = VGroup()
        for i, t in enumerate(labels_):
            col = DATA if t.startswith("v") else (EBM if t.startswith("h") else GREY_B)
            nodes.add(VGroup(Circle(0.38, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.12),
                             MathTex(t, font_size=32, color=col)))
        for n_ in nodes:
            n_[1].move_to(n_[0])
        for i, n_ in enumerate(nodes):
            n_.move_to([-5.0 + 1.9 * i, 1.0 + (0.7 if i % 2 else -0.3), 0])
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(nodes, nodes[1:])])
        dl = label(r"a training digit", font_size=20, color=DATA).next_to(nodes[0], DOWN, buff=0.15)
        kl = label(r"after $k$ Gibbs steps", font_size=20, color=DATA).next_to(nodes[-1], DOWN, buff=0.15)
        rule = cmath(r"\Delta W", r"\propto", r"v_0\, p(h \mid v_0)^\top", r"-", r"v_k\, p(h \mid v_k)^\top",
                     font_size=34).move_to([0.0, -1.0, 0])
        rule[2].set_color(DATA)
        rule[4].set_color(EBM)
        h1 = history_card(2002, r"Hinton: \ contrastive divergence", r"start the chain at the data; \ stop after $k$ "
                          r"steps", width=5.0, font_size=18).move_to([-3.4, -2.8, 0])
        h2 = history_card(2008, r"Tieleman: \ persistent CD", r"keep the chains running between updates", width=5.0,
                          font_size=18).move_to([3.0, -2.8, 0])
        with self.voiceover(
            "Geoffrey Hinton's shortcut, in 2002: start the chain at a training digit, <bookmark mark='a'/> run k "
            "steps of Gibbs sampling, a whole layer at a time, <bookmark mark='b'/> and use where it got to. With k "
            "equal to one it's biased, but it learns, and fast: contrastive divergence. <bookmark mark='c'/> "
            "Tijmen Tieleman, in 2008, kept the chains running between updates: persistent CD."
        ) as vo:
            self.play(FadeIn(nodes[0]), FadeIn(dl), FadeIn(h1))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(n_)) for a, n_ in zip(arrs, nodes[1:])],
                                  lag_ratio=0.4), FadeIn(kl), run_time=3.0)
            vo.wait_until("b")
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(h2, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        r = load("rbm")
        curves = {m: np.array([np.asarray(r[f"{m}_s{s}_curve"]) for s in range(3)]) for m in ("cd1", "cd10", "pcd")}
        S = curves["cd1"][0, :, 0]
        lo = float(min(c[:, 1:, 1].min() for c in curves.values()))
        hi = float(max(c[:, :, 1].max() for c in curves.values()))
        lo_t, hi_t = float(np.floor(lo / 10) * 10), float(np.ceil(hi / 10) * 10)
        g = axes([0, S[-1]], [lo_t, hi_t], x_length=6.2, y_length=3.8, xlabel=r"parameter updates",
                 ylabel=r"test log-likelihood, \ nats per digit \ (exact)", xticks=[0, S[-1]],
                 yticks=[lo_t, hi_t], xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[-1.6, -0.5, 0])
        bands, lines = VGroup(), VGroup()
        for m in ("cd1", "cd10", "pcd"):
            Y = curves[m][:, :, 1]
            bands.add(band(g.ax, S, Y.min(0), Y.max(0), COLS[m], 0.25))
            lines.add(curve(g.ax, S, Y.mean(0), COLS[m], 3))
        lg = legend([(COLS[m], NAMES[m]) for m in ("cd1", "cd10", "pcd")], font_size=22).next_to(g, RIGHT, buff=0.4)
        nh = int(r["nh"])
        eq = label(rf"$Z$ summed exactly over all $2^{{{nh}}} = {2 ** nh:,}$ hidden states".replace(",", "{,}"),
                   font_size=22, color=C.BITS).to_edge(UP, buff=0.4)
        fin = {m: float(np.mean([r[f"{m}_s{s}_test_ll"] for s in range(3)])) for m in ("cd1", "cd10", "pcd")}
        order = sorted(fin, key=fin.get, reverse=True)
        first, second, third = (SPOKEN[m] for m in order)
        verdict = (f"Ranked by where they end: {first} at {fin[order[0]]:.1f} nats per digit, then {second} at "
                   f"{fin[order[1]]:.1f}, and {third} at {fin[order[2]]:.1f}.")
        if order[-1] == "cd1":
            why_ = "One step of the chain is the cheapest estimate of the dreams, and the most biased."
        else:
            why_ = "With sixteen hidden units, even one step of the chain is a fair estimate."
        tg = note(r"computed: \ three seeds each, \ the same number of updates; \ bands: \ min to max").to_corner(
            DR, buff=0.2)
        with self.voiceover(
            "Does contrastive divergence maximize the likelihood? Z sums over two to the 196 images, but also over "
            "the hidden states, and sixteen hidden units have only sixty-five thousand. <bookmark mark='a'/> So "
            "here is the exact held-out log-likelihood, three methods, three seeds each, equal updates. <bookmark "
            f"mark='b'/> {verdict} <bookmark mark='c'/> {why_}"
        ) as vo:
            self.play(FadeIn(eq), FadeIn(g), FadeIn(tg))
            vo.wait_until("a")
            for k in range(3):
                self.play(FadeIn(bands[k]), Create(lines[k]), FadeIn(lg[k]), run_time=1.2)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        r = load("rbm")
        Wb = np.asarray(r["big_W"])
        fs = filter_sheet(Wb[:40], 5, 8, size=0.42).move_to([-3.4, 1.0, 0])
        fl = label(r"$40$ of a $100$-unit RBM's filters: \ warm $+$, \ cool $-$", font_size=20, color=EBM)
        fl.next_to(fs, UP, buff=0.12)
        chain = np.asarray(r["big_chain"])  # 5 x 16 x 196
        ks = [0, 1, 10, 100, 1000]
        cols = Group()
        for k, c in zip(ks, chain):
            sh = digit_sheet(c[:4], 4, 1, size=0.42, gap=0.04)
            cols.add(Group(MathTex(rf"k = {k}", font_size=22, color=EBM), sh).arrange(DOWN, buff=0.1))
        cols.arrange(RIGHT, buff=0.25).move_to([3.4, 1.0, 0])
        cl = label(r"Gibbs chains from random pixels", font_size=20, color=EBM).next_to(cols, UP, buff=0.12)
        ex = digit_sheet(np.asarray(r["pcd_s0_exact"])[:8], 1, 8, size=0.4, gap=0.04).move_to([3.4, -1.6, 0])
        exl = label(r"exact samples of a $16$-unit RBM: \ all $2^{16}$ hidden states weighed", font_size=20,
                    color=GREY_A).next_to(ex, UP, buff=0.1)
        dbn = history_card(2006, r"Hinton, Osindero \& Teh: \ deep belief nets", r"RBMs stacked, \ each trained on "
                           r"the one below: \ the start of the deep learning revival (Part 9)", width=5.6,
                           font_size=18).move_to([-3.4, -2.3, 0])
        with self.voiceover(
            "What does it learn? Each hidden unit's weights, as a picture, show what turns it on: forty of a "
            "hundred-unit machine's, positive for ink, negative for paper. <bookmark mark='a'/> To dream, run the "
            "chain from random pixels: one step, ten, a hundred, a thousand. <bookmark mark='b'/> With sixteen "
            "units we can sample the true model exactly, weighing every hidden state. <bookmark mark='c'/> In 2006 "
            "Hinton, Simon Osindero and Yee-Whye Teh stacked RBMs into deep belief nets, and deep learning's revival "
            "began; six years later backpropagation on GPUs made that unnecessary. The ideas stayed: an energy, "
            "and samples drawn by a chain."
        ) as vo:
            self.play(FadeIn(fs), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c_) for c_ in cols], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ex), FadeIn(exl))
            vo.wait_until("c")
            self.play(FadeIn(dbn, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
