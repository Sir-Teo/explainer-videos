from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ADV, ATT, CELLS, CNN, GRUC, HAND, KERNEL, LSTMC, MLPC, PART, RNNC, box_label,
                                   grid_of, img_filter, img_heat, load, seed_band)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []

        def small_axes(xr, yr):
            return Axes(x_range=[*xr, (xr[1] - xr[0]) / 2], y_range=[*yr, (yr[1] - yr[0]) / 2], x_length=TW * 0.9,
                        y_length=TH * 0.85, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})

        h = load("hog")["linear"]
        vals = [h["mnist_pixels"]["mean"], h["mnist_hog"]["mean"]]
        bars = VGroup(*[Rectangle(width=0.7, height=1.7 * v / max(vals), stroke_width=0, fill_color=c,
                                  fill_opacity=0.9) for v, c in zip(vals, [GREY_B, HAND])]).arrange(RIGHT, buff=0.4,
                                                                                                  aligned_edge=DOWN)
        out.append((bars, r"hand-made features", HAND))
        e = load("equivariance")
        pair = Group(img_heat(np.asarray(e["fmap"]), 1.3), img_heat(np.asarray(e["fmap_shift"]), 1.3)).arrange(RIGHT,
                                                                                                         buff=0.15)
        out.append((pair, r"shift, then convolve", KERNEL))
        L = load("lenet")
        w = np.asarray(L["w1"])[-1]
        out.append((grid_of([img_heat(w[f], 0.55) for f in range(6)], cols=3, buff=0.08), r"LeNet's kernels", CNN))
        o = load("orientation")
        out.append((grid_of([img_filter(x, 0.32) for x in np.asarray(o["w1"])], cols=8, buff=0.03),
                    r"edges from photographs", KERNEL))
        a = load("adversarial")
        ax = small_axes((0, 0.3), (0, 1.0))
        out.append((VGroup(ax, seed_band(ax, a["eps"], a["fgsm"]["lenet"], ADV)), r"an invisible change", ADV))
        g = load("rnn_grad")
        ax = small_axes((0, 100), (-12, 12))
        cs = VGroup(*[curve(ax, g["ks"], np.clip(np.asarray(g["tanh_median"])[i], -12, 12), c, 2.5)
                      for i, c in enumerate([C.TRUE_P, C.INTERVAL, C.MODEL_Q, C.SURPRISE])])
        out.append((VGroup(ax, cs), r"gradients fade in time", RNNC))
        m = load("memory")
        T = int(m["T"][-1])
        mb = VGroup(*[Rectangle(width=0.45, height=max(1.7 * float(np.mean([m["runs"][f"{c}-{T}-{s}"]["final"]
                                                                             for s in (0, 1, 2)])), 0.03),
                                stroke_width=0, fill_color=CELLS[c], fill_opacity=0.9)
                      for c in ("rnn", "lstm", "gru", "mingru")]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        out.append((mb, rf"memory over ${T}$ steps", LSTMC))
        s = load("seq2seq")
        al = np.asarray(s["runs"]["1-0"]["show_alpha"])[:len(s["show"]) + 1, :len(s["show"])]
        out.append((img_heat(al, 1.9, sym=False, pos=ATT, height=1.9 * al.shape[0] / al.shape[1]),
                    r"attention aligns", ATT))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Vision began with features designed by hand, and they beat raw pixels. A "
            "convolution shares one small kernel across the image, so it commutes with shifts. Trained end to end, "
            "LeNet grew its own stroke detectors, and our photograph network grew edge detectors and colour cells "
            "like the ones in the visual cortex. Yet an invisible, well-chosen change fools them all, because they "
            "are close to linear. In time, a plain recurrent network's gradient fades, or explodes, as Jacobians "
            "multiply. The LSTM's gated memory line carries it across a hundred steps. And attention lets a "
            "decoder look back at exactly what it needs."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"attention: \ queries, keys and values", [13, 14]),
            (r"linear recurrences, \ scans, \ the fixed-size memory", [15]),
            (r"clipping, \ residual paths, \ optimizers for deep networks", [11]),
            (r"patches and convolutions in vision transformers", [22]),
            (r"equivariance to rotations and permutations", [25]),
            (r"adversarial attacks on language models", [31]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. Bahdanau's attention becomes the whole of the Transformer, in Parts 13 and "
            "14. The linear recurrences and their scans are Part 15's memory. Clipping and the optimizers that "
            "train deep networks are Part 11. Images cut into patches, and convolutions inside the new models, "
            "are Part 22. Equivariance, for rotations, molecules and graphs, is Part 25. And adversarial attacks, "
            "on language models this time, come back in Part 31."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that circular cross-correlation commutes with every shift $T_s$. \ Conversely, show that a "
            r"linear map on $\mathbb{R}^n$ (indices mod $n$) that commutes with all shifts is a cross-correlation.",
            r"Prove $r_L = 1 + \sum_{\ell}(k_\ell - 1)\prod_{i<\ell} s_i$, \ and compute it for AlexNet: \ conv1 "
            r"$11$/$4$, pool $3$/$2$, conv2 $5$/$1$, pool $3$/$2$, conv3--5 $3$/$1$, pool $3$/$2$.",
            r"Derive the cost ratio $1/C' + 1/k^2$ of a depthwise separable convolution. \ For $k = 3$ and "
            r"$C' = 512$, how much cheaper is it? \ Why can the measured speed-up be smaller?",
            r"For a linear score $w \cdot x$, show $\max_{\|\eta\|_\infty \le \varepsilon} w \cdot \eta = "
            r"\varepsilon \|w\|_1$. \ A margin of $3$ between two classes, \ $\|w_y - w_{y'}\|_1 = 300$: \ which "
            r"$\varepsilon$ flips it?",
            r"An LSTM with $i_t = 0$ and $f_t = f$: \ show $c_T = f^{T-k} c_k$, \ find the half-life of the memory, "
            r"\ and say why the forget gate's bias is often started at $1$.",
            r"Show that $(a, b) \circ (a', b') = (a a', a' b + b')$ is associative, \ and that the Hillis--Steele "
            r"scan finds every $h_t$ of $h_t = a_t h_{t-1} + b_t$ in $\lceil \log_2 T \rceil$ rounds.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems, from equivariance to the scan. Pause here and work through them; full "
            "solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        t = load("teaser")
        xs, ys, Z = np.asarray(t["xs"]), np.asarray(t["ys"]), np.asarray(t["Z"])
        head = label(r"Next: \ Part 11, \ Going Downhill", font_size=40).to_edge(UP, buff=0.4)
        img = img_heat(Z[::-1], 9.0, sym=False, pos="#F2D16B", mid="#1B2A6B", height=3.6, smooth=True)
        img.move_to([0, -0.6, 0])

        def P(p):
            x = img.get_left()[0] + img.width * (p[0] - xs[0]) / (xs[-1] - xs[0])
            y = img.get_bottom()[1] + img.height * (p[1] - ys[0]) / (ys[-1] - ys[0])
            return np.array([x, y, 0])

        paths = VGroup()
        for key, col in (("path_gd", GREY_A), ("path_momentum", GRUC), ("path_adam", MLPC)):
            pts = [P(p) for p in np.asarray(t[key]) if xs[0] <= p[0] <= xs[-1] and ys[0] <= p[1] <= ys[-1]]
            paths.add(VMobject(color=col, stroke_width=3).set_points_as_corners(pts))
        leg = legend([(GREY_A, r"gradient descent"), (GRUC, r"momentum"), (MLPC, r"Adam")], font_size=22)
        leg.next_to(img, DOWN, buff=0.3)
        tag = note(r"computed: \ one valley, \ three optimizers").to_corner(DR, buff=0.25)
        steps = VGroup(*[box_label(x, c, font_size=22) for x, c in (
            (r"convergence rates", GREY_B), (r"SGD as noise", GREY_B), (r"momentum, \ Adam, \ AdamW", MLPC),
            (r"Shampoo, \ Muon", CNN), (r"schedules", KERNEL))]).arrange(RIGHT, buff=0.25)
        if steps.width > 13.2:
            steps.width = 13.2
        steps.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Every network in this part was trained by some version of going downhill: plain gradient descent "
            "with momentum, or Adam. Next time, in Part 11, we take the descent itself apart: how fast it "
            "converges and why, what the noise of small batches does, momentum and Adam derived, the newer "
            "optimizers that treat weights as matrices, and the learning-rate schedules of today's models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(tag))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3), FadeIn(leg), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in steps], lag_ratio=0.3),
                      run_time=max(2.0, vo.duration - 5.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"I.~Goodfellow, Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016), \ chapters 9 and 10",
             r"R.~Szeliski, \textit{Computer Vision: Algorithms and Applications}, 2nd ed.\ (2022)",
             r"A.~Zhang, Z.~C.~Lipton, M.~Li \& A.~J.~Smola, \textit{Dive into Deep Learning} (2023)",
             r"A.~Graves, \textit{Supervised Sequence Labelling with Recurrent Neural Networks} (2012)"],
            [r"Hubel \& Wiesel (1959, 1962); \ Fukushima (1980); \ LeCun et al.\ (1989, 1998); \ Waibel et al.\ "
             r"(1989); \ Lowe (2004); \ Dalal \& Triggs (2005)",
             r"Deng et al.\ (2009); \ Russakovsky et al.\ (2015); \ Krizhevsky, Sutskever \& Hinton (2012); \ "
             r"Cire\c{s}an et al.\ (2012); \ Nair \& Hinton (2010); \ Srivastava et al.\ (2014)",
             r"Simonyan \& Zisserman (2014); \ Szegedy et al.\ (2014); \ Ioffe \& Szegedy (2015); \ He et al.\ (2015); "
             r"\ Srivastava, Greff \& Schmidhuber (2015); \ Recht et al.\ (2019)",
             r"Zeiler \& Fergus (2013); \ Simonyan, Vedaldi \& Zisserman (2013); \ Luo et al.\ (2016); \ Olah et al.\ "
             r"(2017); \ Azulay \& Weiss (2019); \ Zhang (2019)",
             r"Szegedy et al.\ (2013); \ Goodfellow, Shlens \& Szegedy (2014); \ Madry et al.\ (2017); \ Wong, Rice "
             r"\& Kolter (2020)",
             r"Sifre (2014); \ Chollet (2016); \ Howard et al.\ (2017); \ Yu \& Koltun (2015); \ van den Oord et al.\ "
             r"(2016); \ Dosovitskiy et al.\ (2020); \ Liu et al.\ (2022); \ Smith et al.\ (2023)",
             r"Jordan (1986); \ Elman (1990); \ Werbos (1990); \ Hochreiter (1991); \ Bengio, Simard \& Frasconi "
             r"(1994); \ Pascanu, Mikolov \& Bengio (2013)",
             r"Hochreiter \& Schmidhuber (1997); \ Gers, Schmidhuber \& Cummins (2000); \ Cho et al.\ (2014); \ "
             r"Chung et al.\ (2014); \ Karpathy, Johnson \& Fei-Fei (2015)",
             r"Sutskever, Vinyals \& Le (2014); \ Bahdanau, Cho \& Bengio (2014); \ Luong et al.\ (2015); \ Wu et "
             r"al.\ (2016); \ Holtzman et al.\ (2019)",
             r"Blelloch (1990); \ Martin \& Cundy (2018); \ Gu \& Dao (2023); \ Beck et al.\ (2024, 2025); \ Feng et "
             r"al.\ (2024)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Goodfellow, Bengio and Courville's book covers both halves of this part, and Szeliski's the vision "
            "that came before. Thanks for watching, and see you in Part 11."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()


_ = (GRUC, RNNC)
