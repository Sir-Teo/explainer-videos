from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai5.compute import density2
from videos.ai.ai7.common import (AUSTEN, CAUSE, CONSONANT, DICKENS, HIDDEN, MONO, PART, SEEN, TOPIC_COLORS, VOICE1,
                                  VOICE2, VOWEL, ellipse_2sd, heat_grid, load, mix)


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

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        # 1. PCA: the share of variation, direction by direction
        share = np.asarray(load("pca")["share"])[:10]
        out.append((VGroup(*[Rectangle(width=0.2, height=max(12 * s, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                       fill_opacity=0.85).move_to([0.27 * i, 6 * s, 0]) for i, s in enumerate(share)]),
                    r"principal components", C.MODEL_Q))
        # 2. ICA: the two voices recovered
        ica = load("ica")
        t, Y = np.asarray(ica["t"])[:300], np.asarray(ica["Y"])[:, :300]
        ax2 = plane([t[0], t[-1], 1], [-6, 3, 1])
        out.append((VGroup(curve(ax2, t, Y[0] / np.abs(Y[0]).max() + 1.5, VOICE1, 2.5),
                           curve(ax2, t, Y[1] / np.abs(Y[1]).max() - 1.5, VOICE2, 2.5)), r"two voices, unmixed", VOICE1))
        # 3. EM: the two bells on the pages
        g = load("gmm")
        P, R = np.asarray(g["P"]), np.asarray(g["r"])[-1]
        y = np.asarray(g["y"])
        if ((R > 0.5) == y).mean() < 0.5:
            R = 1 - R
        ax3 = plane([P[:, 0].min(), P[:, 0].max(), 1], [P[:, 1].min(), P[:, 1].max(), 1])
        m, cv = np.asarray(g["means"])[-1], np.asarray(g["covs"])[-1]
        em = VGroup(*[Dot(ax3.c2p(*p_), radius=0.02, color=mix(AUSTEN, DICKENS, r_)) for p_, r_ in zip(P, R)])
        em.add(*[ellipse_2sd(ax3, m[k], cv[k], WHITE, stroke_width=2) for k in range(2)])
        out.append((em, r"mixtures and EM", WHITE))
        # 4. topics
        lda = load("lda")
        c3 = np.argsort(-np.asarray(lda["main_share"]))[:3]
        cols = VGroup(*[VGroup(*[data_text(w, font=MONO, font_size=22, color=TOPIC_COLORS[k]) for w in lda["top"][k][:4]])
                        .arrange(DOWN, buff=0.06) for k in c3]).arrange(RIGHT, buff=0.3)
        out.append((cols, r"topic models", TOPIC_COLORS[int(c3[0])]))
        # 5. HMM: the two states' letters
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
        # 6. IBM Model 1's alignment
        A = np.asarray(load("ibm1")["align"])[-1]
        out.append((heat_grid(A, cell=0.3, color=C.BITS), r"alignment by EM", C.BITS))
        # 7. the scoreboard's two new rows
        sb = load("scoreboard")
        rows = [r_ for r_ in sb["rows"] if r_.get("key") in ("best", "kn", "infini")]
        sbars = VGroup()
        for i, r_ in enumerate(rows):
            w = 2.4 * r_["bits"] / 2.5
            sbars.add(VGroup(Rectangle(width=w, height=0.32, stroke_width=0, fill_color=C.COUNTING,
                                       fill_opacity=0.45 + 0.25 * i).move_to([-1.2 + w / 2, 0.5 - 0.5 * i, 0]),
                             MathTex(f"{r_['bits']:.2f}", font_size=24, color=C.COUNTING).move_to([1.6, 0.5 - 0.5 * i, 0])))
        out.append((sbars, r"Kneser--Ney, \ $\infty$-gram", C.COUNTING))
        # 8. belief propagation on a tree
        pos = [[0, 0.8], [-0.8, 0], [0.8, 0], [-1.2, -0.8], [-0.4, -0.8], [0.4, -0.8], [1.2, -0.8]]
        tree = VGroup(*[Line([*pos[a], 0], [*pos[b], 0], color=GREY_C, stroke_width=2) for a, b in load("bp")["edges"]],
                      *[Circle(radius=0.16, color=HIDDEN, stroke_width=2.5, fill_color=BACKGROUND, fill_opacity=1)
                        .move_to([*p_, 0]) for p_ in pos])
        out.append((tree, r"belief propagation", HIDDEN))
        # 9. causes
        c = load("causal")
        cb = VGroup()
        for i, (v, col) in enumerate(((c["naive"], GREY_B), (c["adjusted_sim"], CAUSE), (c["experiment"], SEEN))):
            h_ = abs(v) * 8
            cb.add(Rectangle(width=0.5, height=h_, stroke_width=0, fill_color=col, fill_opacity=0.9)
                   .move_to([-0.8 + 0.8 * i, h_ / 2 if v > 0 else -h_ / 2, 0]))
        cb.add(Line([-1.2, 0, 0], [1.2, 0, 0], color=GREY_C, stroke_width=1.5))
        out.append((cb, r"seeing vs.\ doing", CAUSE))
        # 10. a Gaussian process
        gp = load("gp")
        xsg, mg, sg = np.asarray(gp["xs"]), np.asarray(gp["mean"]), np.asarray(gp["sd"])
        xd, yd = np.asarray(gp["x"]), np.asarray(gp["y"])
        win = xsg <= 60
        xsg, mg, sg = xsg[win], mg[win], sg[win]
        top = max(float((mg + 2 * sg).max()), float(yd[xd <= 60].max()))
        ax5 = plane([0, 60, 10], [0, top, 1])
        bandp = Polygon(*[ax5.c2p(a, b) for a, b in zip(xsg, mg + 2 * sg)],
                        *[ax5.c2p(a, max(b, 0)) for a, b in zip(xsg[::-1], (mg - 2 * sg)[::-1])],
                        stroke_width=0, fill_color=HIDDEN, fill_opacity=0.35)
        pts5 = VGroup(*[Dot(ax5.c2p(a, b), radius=0.025, color=DICKENS) for a, b in zip(xd, yd) if a <= 60])
        out.append((VGroup(bandp, pts5, VMobject(color=WHITE, stroke_width=2.5).set_points_smoothly(
            [ax5.c2p(a, b) for a, b in zip(xsg, mg)])), r"Gaussian processes", HIDDEN))
        # 11. Bayesian optimization
        bo = load("bayesopt")
        grid, truth = np.asarray(bo["grid"]), np.asarray(bo["truth"])
        ax6 = plane([0, 1, 0.5], [float(truth.min()) - 0.005, float(np.percentile(truth, 80)), 0.01])
        keep = truth <= np.percentile(truth, 80)
        bot = VGroup(curve(ax6, grid[keep], truth[keep], GREY_C, 2),
                     *[Dot(ax6.c2p(x_, min(y_, float(np.percentile(truth, 80)))), radius=0.05, color=C.MODEL_Q)
                       for x_, y_ in zip(bo["xs"], bo["ys"])])
        out.append((bot, r"Bayesian optimization", C.BITS))
        # 12. VI on two bumps
        v = load("vi")
        t_ = np.asarray(v["t_qp"])
        ax7 = plane([-4, 4, 1], [-3, 3, 1])
        cont = contour_lines(ax7, density2, (-4, 4), (-3, 3), [0.1, 0.4, 0.7], n=(80, 60), stroke_width=1.4)
        s0, s1, r = math.exp(t_[2]), math.exp(t_[3]), math.tanh(t_[4])
        cq = np.array([[s0 * s0, r * s0 * s1], [r * s0 * s1, s1 * s1]])
        out.append((VGroup(cont, ellipse_2sd(ax7, t_[:2], cq, C.MODEL_Q, stroke_width=3, k=1.5)), r"variational inference",
                    C.MODEL_Q))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=3, cols=4, buff=(0.22, 0.22))
        tiles.scale_to_fit_height(6.5).move_to(DOWN * 0.35)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in twelve pictures", font_size=36).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Let's take stock. <bookmark mark='pca'/> Principal components are the covariance's eigenvectors: the line of greatest spread, "
            "and the line closest to the data, at once; add noise, and they become a probability model. "
            "<bookmark mark='ica'/> Independent components unmixed two voices. <bookmark mark='em'/> With an exact "
            "posterior E step and an M step that never lowers the same bound, EM cannot lower the likelihood. "
            "K-means is its small-variance limit, <bookmark mark='topics'/> and a topic model is a mixture of mixtures. "
            "<bookmark mark='hmm'/> Hidden Markov models found vowels with no labels, "
            "<bookmark mark='alignment'/> and EM's alignments started statistical translation. "
            "<bookmark mark='counting'/> Good–Turing and Kneser–Ney counted "
            "what hadn't been seen, and a suffix array counted contexts of any length. Graphs gave us independence, "
            "<bookmark mark='graphs'/> message passing, and, <bookmark mark='causes'/> with do, cause and effect. "
            "<bookmark mark='gp'/> Gaussian processes put probabilities on whole "
            "functions, chose their own length scale by Occam's razor, <bookmark mark='optimization'/> and chose where to look next. "
            "<bookmark mark='vi'/> And variational "
            "inference turned an impossible posterior into an optimization."
        ) as vo:
            self.play(FadeIn(head), run_time=0.35)
            for cue, tile in zip(("pca", "ica", "em", "topics", "hmm", "alignment", "counting",
                                  "graphs", "causes", "gp", "optimization", "vi"), tiles):
                vo.wait_until(cue)
                self.play(FadeIn(tile, shift=UP * 0.15, scale=0.95), run_time=0.35)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"alignment, \ learned softly: \ attention", [13]),
            (r"hidden state through time: \ state-space models", [15]),
            (r"mixtures, soft assignment: \ mixtures of experts", [16]),
            (r"the forward algorithm: \ CTC", [23]),
            (r"Gaussian processes: \ infinitely wide networks", [12]),
            (r"the ELBO and the reparameterization trick", [20, 21]),
            (r"interventions: \ causal tracing", [30]),
            (r"Kneser--Ney: \ the row to beat", [9]),
        ], font_size=24)
        with self.voiceover(
            "Hidden parts come back everywhere. <bookmark mark='alignment'/> Model 1's alignments return as attention, a soft alignment learned "
            "inside the network, in part thirteen. <bookmark mark='state'/> State-space models, in part fifteen, carry a hidden state through "
            "time, <bookmark mark='experts'/> and mixtures of experts, in part sixteen, are mixtures with a learned way of choosing. "
            "<bookmark mark='forward'/> The forward algorithm trains speech recognizers in part twenty-three. "
            "<bookmark mark='gp'/> An infinitely wide network is a Gaussian "
            "process, in part twelve. <bookmark mark='elbo'/> The ELBO and the reparameterization trick train autoencoders and diffusion "
            "models. <bookmark mark='causes'/> Setting a network's activations by hand is the do operator, in part thirty. "
            "<bookmark mark='counting'/> And Kneser–Ney is "
            "the row the first neural language model has to beat, in part nine."
        ) as vo:
            self.play(FadeIn(card.head), run_time=0.35)
            for cue, row in zip(("alignment", "state", "experts", "forward", "gp", "elbo", "causes", "counting"), card.rows):
                vo.wait_until(cue)
                self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.35)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For centred data with covariance $C$ and a unit vector $\mathbf{u}$, show that the mean squared distance to "
            r"the line through $\mathbf{u}$ is $\mathrm{tr}(C) - \mathbf{u}^{\top} C \mathbf{u}$. \ Deduce that "
            r"Pearson's and Hotelling's lines coincide.",
            r"In probabilistic PCA, show that $x$ has covariance $W W^{\top} + \sigma^2 I$, and check that "
            r"$W = U_k (\Lambda_k - \sigma^2 I)^{1/2}$ makes it agree with the data's covariance on the top $k$ directions.",
            r"Using $\log p(x; \theta) = \mathcal{B}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x; \theta))$, prove that one "
            r"round of EM never lowers the likelihood.",
            r"Derive the forward recursion $\alpha_t(j) = \sum_i \alpha_{t-1}(i) A_{ij} B_j(x_t)$, and count its "
            r"operations for $T$ steps and $S$ states.",
            r"Good--Turing gives each item seen once the count $1^* = 2 N_2 / N_1$. \ What total probability does it give "
            r"all of them together, and where did the rest of their mass go?",
            r"For the graph $Z \to X$, $Z \to Y$, $X \to Y$, derive $P(y \mid \mathrm{do}(x)) = \sum_z P(y \mid x, z) P(z)$ "
            r"by deleting the factor $P(x \mid z)$ from the joint.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems, from Pearson's line to Pearl's do operator. Pause here and work through them; "
            "full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
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
            self.play(Create(lt), FadeIn(names[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(le), FadeIn(names[1]), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"C.~M.~Bishop, \textit{Pattern Recognition and Machine Learning} (2006); \ D.~MacKay, \textit{Information "
            r"Theory, Inference, and Learning Algorithms} (2003)",
            r"C.~E.~Rasmussen \& C.~K.~I.~Williams, \textit{Gaussian Processes for Machine Learning} (2006); \ "
            r"D.~Koller \& N.~Friedman, \textit{Probabilistic Graphical Models} (2009)",
            r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing}, 3rd ed.\ draft; \ J.~Pearl, "
            r"\textit{Causality} (2000)",
        ]
        papers = [
            r"Pearson (1901); \ Hotelling (1933); \ Tipping \& Bishop (1999); \ Comon (1994); \ Bell \& Sejnowski (1995); "
            r"\ Hyv\"arinen (1999)",
            r"Dempster, Laird \& Rubin (1977); \ Lloyd (1957/1982); \ Blei, Ng \& Jordan (2003)",
            r"Viterbi (1967); \ Baum et al.\ (1970); \ Jelinek (1976); \ Cave \& Neuwirth (1980); \ Rabiner (1989)",
            r"Brown et al.\ (1990, 1993); \ Papineni et al.\ (2002); \ Good (1953); \ Church \& Gale (1991); \ "
            r"Kneser \& Ney (1995); \ Chen \& Goodman (1998)",
            r"Manber \& Myers (1990); \ Liu, Min, Zettlemoyer, Choi \& Hajishirzi, \textit{Infini-gram} (2024)",
            r"Pearl (1982, 1988, 1995); \ Charig et al.\ (1986); \ Julious \& Mullee (1994)",
            r"Krige (1951); \ MacKay (1992); \ Mockus (1975); \ Jones, Schonlau \& Welch (1998); \ Snoek, Larochelle \& "
            r"Adams (2012)",
            r"Jordan, Ghahramani, Jaakkola \& Saul (1999); \ Kingma \& Welling (2013); \ Rezende, Mohamed \& Wierstra (2014)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every method is written out in numpy; \ every "
                    r"number on screen is computed and checked.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.height > 5.9:
            card.height = 5.9
        card.to_edge(UP, buff=0.3)
        with self.voiceover(
            "Bishop's Pattern Recognition and Machine Learning covers most of this part; Rasmussen and Williams the "
            "Gaussian processes, and Pearl's Causality the causes. Thanks for watching, and see you in part eight."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
