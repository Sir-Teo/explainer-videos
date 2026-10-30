from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai5.compute import density2
from videos.ai.ai7.common import AUSTEN, CONSONANT, DICKENS, HIDDEN, VOWEL, ellipse_2sd, load, mix


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        # 1. PCA: the share of variation, direction by direction
        share = np.asarray(load("pca")["share"])[:10]
        out.append((VGroup(*[Rectangle(width=0.2, height=max(12 * s, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                       fill_opacity=0.85).move_to([0.27 * i, 6 * s, 0]) for i, s in enumerate(share)]),
                    r"principal components", C.MODEL_Q))
        # 2. EM: the two bells on the pages
        g = load("gmm")
        P, R = np.asarray(g["P"]), np.asarray(g["r"])[-1]
        y = np.asarray(g["y"])
        if ((R > 0.5) == y).mean() < 0.5:
            R = 1 - R
        ax2 = plane([P[:, 0].min(), P[:, 0].max(), 1], [P[:, 1].min(), P[:, 1].max(), 1])
        m, cv = np.asarray(g["means"])[-1], np.asarray(g["covs"])[-1]
        em = VGroup(*[Dot(ax2.c2p(*p_), radius=0.02, color=mix(AUSTEN, DICKENS, r_)) for p_, r_ in zip(P, R)])
        em.add(*[ellipse_2sd(ax2, m[k], cv[k], WHITE, stroke_width=2) for k in range(2)])
        out.append((em, r"mixtures and EM", WHITE))
        # 3. HMM: the two states' letters
        B = np.asarray(load("hmm")["B"])
        alpha = " abcdefghijklmnopqrstuvwxyz"
        hm = VGroup()
        for k, yb in enumerate((0.1, -1.0)):
            for i, ch in enumerate(alpha):
                h_ = max(1.0 * B[k][i] / 0.4, 0.01)
                col = GREY_B if ch == " " else VOWEL if ch in "aeiou" else CONSONANT
                hm.add(Rectangle(width=0.08, height=h_, stroke_width=0, fill_color=col, fill_opacity=0.9)
                       .move_to([-1.35 + i * 0.104, yb + h_ / 2, 0]))
        out.append((hm, r"a hidden Markov model", HIDDEN))
        # 4. a graphical model: a hidden chain
        zs = VGroup(*[Circle(radius=0.2, color=HIDDEN, stroke_width=2.5).move_to([-1.2 + 0.8 * k, 0.45, 0]) for k in range(4)])
        xs_ = VGroup(*[Circle(radius=0.2, color=C.TRUE_P, stroke_width=2.5, fill_color=C.TRUE_P, fill_opacity=0.35)
                       .move_to([-1.2 + 0.8 * k, -0.55, 0]) for k in range(4)])
        ar = VGroup(*[Arrow(zs[k].get_right(), zs[k + 1].get_left(), buff=0.02, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.3) for k in range(3)],
                    *[Arrow(zs[k].get_bottom(), xs_[k].get_top(), buff=0.02, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.3) for k in range(4)])
        out.append((VGroup(zs, xs_, ar), r"models as pictures", HIDDEN))
        # 5. a Gaussian process
        gp = load("gp")
        xsg, mg, sg = np.asarray(gp["xs"]), np.asarray(gp["mean"]), np.asarray(gp["sd"])
        xd, yd = np.asarray(gp["x"]), np.asarray(gp["y"])
        win = xsg <= 60  # the first sixty pages: the fit and its band, with the data
        xsg, mg, sg = xsg[win], mg[win], sg[win]
        top = max(float((mg + 2 * sg).max()), float(yd[xd <= 60].max()))
        ax5 = plane([0, 60, 10], [0, top, 1])
        bandp = Polygon(*[ax5.c2p(a, b) for a, b in zip(xsg, mg + 2 * sg)],
                        *[ax5.c2p(a, max(b, 0)) for a, b in zip(xsg[::-1], (mg - 2 * sg)[::-1])],
                        stroke_width=0, fill_color=HIDDEN, fill_opacity=0.35)
        pts5 = VGroup(*[Dot(ax5.c2p(a, b), radius=0.025, color=DICKENS) for a, b in zip(xd, yd) if a <= 60])
        out.append((VGroup(bandp, pts5, VMobject(color=WHITE, stroke_width=2.5).set_points_smoothly(
            [ax5.c2p(a, b) for a, b in zip(xsg, mg)])), r"Gaussian processes", HIDDEN))
        # 6. VI on two bumps
        v = load("vi")
        t = np.asarray(v["t_qp"])
        ax6 = plane([-4, 4, 1], [-3, 3, 1])
        cont = contour_lines(ax6, density2, (-4, 4), (-3, 3), [0.1, 0.4, 0.7], n=(80, 60), stroke_width=1.4)
        s0, s1, r = math.exp(t[2]), math.exp(t[3]), math.tanh(t[4])
        cq = np.array([[s0 * s0, r * s0 * s1], [r * s0 * s1, s1 * s1]])
        out.append((VGroup(cont, ellipse_2sd(ax6, t[:2], cq, C.MODEL_Q, stroke_width=3, k=1.5)), r"variational inference",
                    C.MODEL_Q))
        # 7. Kneser-Ney against add-alpha
        k = load("kn")
        p1, kn = np.asarray(k["part1_rows"]), np.array([r_["test"] for r_ in k["rows"]])
        ax7 = Axes(x_range=[0, len(kn) - 1, 1], y_range=[1.8, 4.8, 1], x_length=TW, y_length=TH - 0.2, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax7, VMobject(color=GREY_B, stroke_width=3).set_points_as_corners(
            [ax7.c2p(i, v_) for i, v_ in enumerate(p1[:len(kn)])]), VMobject(color=C.COUNTING, stroke_width=3)
            .set_points_as_corners([ax7.c2p(i, v_) for i, v_ in enumerate(kn)])), r"Kneser--Ney smoothing", C.COUNTING))
        # 8. the scoreboard's new row
        sbar = VGroup(Rectangle(width=2.6 * 2.32 / 3, height=0.3, stroke_width=0, fill_color=C.COUNTING, fill_opacity=0.4)
                      .move_to([-1.3 + 1.3 * 2.32 / 3, 0.35, 0]),
                      Rectangle(width=2.6 * k["best_bits"] / 3, height=0.3, stroke_width=0, fill_color=C.COUNTING,
                                fill_opacity=0.95).move_to([-1.3 + 1.3 * k["best_bits"] / 3, -0.25, 0]),
                      MathTex(r"2.32", font_size=24, color=GREY_B).move_to([1.2, 0.35, 0]),
                      MathTex(f"{k['best_bits']:.2f}", font_size=24, color=C.COUNTING).move_to([1.2, -0.25, 0]))
        out.append((sbar, r"a new scoreboard row", C.COUNTING))
        tiles = Group()
        for pic, cap, col in out:
            box, c = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 7, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Principal components are the covariance's eigenvectors, and they found Austen against "
            "Dickens without labels. A mixture of bells, fitted by EM, recovered the authors themselves. A hidden "
            "Markov model discovered vowels. Graphical models draw all of these as pictures that are also formulas. "
            "Gaussian processes put probabilities on whole functions, and variational inference swaps an impossible "
            "posterior for the closest simple one. And Kneser–Ney counting gave the scoreboard its last counting row."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"mixtures, soft assignment: \ mixtures of experts", [16]),
            (r"hidden state through time: \ state-space models", [15]),
            (r"Gaussian processes: \ infinitely wide networks", [12]),
            (r"the ELBO", [21, 22]),
            (r"directions in a cloud of vectors", [30]),
            (r"Kneser--Ney: \ the row to beat", [9]),
        ], font_size=26)
        with self.voiceover(
            "Hidden parts come back everywhere. Mixture-of-experts models, in part sixteen, are mixtures with a "
            "learned way of choosing. State-space models, in part fifteen, carry a hidden state through time. An "
            "infinitely wide network is a Gaussian process, in part twelve. The ELBO trains diffusion models and "
            "autoencoders. Directions in clouds of vectors are how we look inside models, in part thirty. And "
            "Kneser–Ney is the row the first neural language model has to beat, in part nine."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 8, \ Fitting and Generalizing", font_size=40).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 0.5], x_length=8.0, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 0.4)
        cx = np.linspace(0.2, 10, 160)
        train = 0.9 * np.exp(-cx / 1.8) + 0.02
        test = np.where(cx < 4.5, 0.75 * np.exp(-cx / 1.6) + 0.08 * cx ** 2 / 4.5, 0)
        peak = 0.75 * np.exp(-4.5 / 1.6) + 0.08 * 4.5
        test = np.where(cx < 4.5, test, peak * np.exp(-(cx - 4.5) / 1.5) + 0.18 * (1 - np.exp(-(cx - 4.5) / 1.5)))
        lt = VMobject(color=GREY_B, stroke_width=3).set_points_smoothly([ax.c2p(a, b) for a, b in zip(cx, train)])
        le = VMobject(color=C.BITS, stroke_width=4).set_points_smoothly([ax.c2p(a, min(b, 1.05)) for a, b in zip(cx, test)])
        names = VGroup(label(r"training error", font_size=24, color=GREY_B).next_to(ax.c2p(8, 0.05), UP, buff=0.1),
                       label(r"error on new data", font_size=24, color=C.BITS).next_to(ax.c2p(7.5, 0.22), UP, buff=0.1))
        xl = label(r"model size $\longrightarrow$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        tag = label(r"double descent \ (schematic)", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Next time: the deepest question in machine learning. A model fits its training data; why should it work "
            "on anything else? <bookmark mark='a'/> Bias and variance, the bounds of Vapnik and Chervonenkis, "
            "networks that memorize random labels, and the curve that goes down, up, and then down again."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lt), Create(le), FadeIn(names), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"C.~M.~Bishop, \textit{Pattern Recognition and Machine Learning} (2006), chapters 8--10, 12, 13",
            r"C.~E.~Rasmussen \& C.~K.~I.~Williams, \textit{Gaussian Processes for Machine Learning} (2006)",
            r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing}, 3rd ed.\ draft, chapters 3 and A",
        ]
        papers = [
            r"K.~Pearson (1901); \ H.~Hotelling, \textit{Analysis of a Complex of Statistical Variables into Principal "
            r"Components} (1933)",
            r"A.~P.~Dempster, N.~M.~Laird \& D.~B.~Rubin, \textit{Maximum Likelihood from Incomplete Data via the EM "
            r"Algorithm} (1977)",
            r"L.~E.~Baum et al.\ (1970); \ L.~R.~Rabiner, \textit{A Tutorial on Hidden Markov Models} (1989)",
            r"R.~J.~Cave \& L.~P.~Neuwirth, \textit{Hidden Markov Models for English} (1980)",
            r"J.~Pearl, \textit{Probabilistic Reasoning in Intelligent Systems} (1988)",
            r"M.~I.~Jordan et al., \textit{An Introduction to Variational Methods for Graphical Models} (1999)",
            r"R.~Kneser \& H.~Ney (1995); \ S.~F.~Chen \& J.~Goodman, \textit{An Empirical Study of Smoothing "
            r"Techniques for Language Modeling} (1998)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every method is written out in numpy; \ every "
                    r"number on screen is computed and checked.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Bishop's Pattern Recognition and Machine Learning covers this whole part, and Rabiner's tutorial is "
            "still the best introduction to hidden Markov models. Thanks for watching, and see you in part eight."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
