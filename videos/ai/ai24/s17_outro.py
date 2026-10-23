from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (BARLOW, DIGIT, DINO_C, JEPA, MAE_C, MATRY, NAIVE, PART, POS, ROT, SIMCLR, Hypersphere,
                                   curve, digit, digit_sheet, heat, load, node_box, tile_frame)


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
        p = load("pretext")
        per = np.mean([r["extra"]["rot_acc_by_digit"] for r in p["runs"].values()], 0)
        bars = VGroup(*[Rectangle(width=0.18, height=max(1.6 * v, 0.02), stroke_width=0, fill_color=ROT,
                                  fill_opacity=0.85) for v in per]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        out.append((bars, r"a puzzle's blind spots", ROT))
        r = load("infonce")
        Ns = list(r["Ns"])
        lx = [math.log2(n) for n in Ns]
        ax = Axes(x_range=[0, lx[-1], lx[-1]], y_range=[0, 11, 11], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        g = VGroup(ax, DashedLine(ax.c2p(0, 0), ax.c2p(lx[-1], lx[-1] * math.log(2)), color=GREY_B))
        for I, col in zip(r["mis"], (C.INTERVAL, C.MODEL_Q, C.SURPRISE)):
            g.add(curve(ax, lx, [np.mean([r["est"][f"I{I:g}_N{n}_s{s}"] for s in (0, 1)]) for n in Ns], col, 2.5))
        out.append((g, r"InfoNCE $\le \log N$", C.TRUE_P))
        sp = load("sphere")
        Z = np.asarray(sp["simclr_z"])[-1]
        lab = np.asarray(sp["labels"]).astype(int)
        P = Z / np.linalg.norm(Z, axis=1, keepdims=True)
        sph = VGroup(Circle(radius=0.95, stroke_color=GREY_D, stroke_width=1.5),
                     *[Dot([0.95 * q[0], 0.95 * q[1], 0], radius=0.022, color=DIGIT[c]).set_opacity(
                         0.3 + 0.7 * (q[2] + 1) / 2) for q, c in zip(P, lab)])
        out.append((sph, r"digits on a sphere", SIMCLR))
        c = load("collapse")
        sv_s, sv_n = np.asarray(c["simclr_spectrum"], float), np.asarray(c["naive_spectrum"], float)
        ax2 = Axes(x_range=[0, len(sv_s), len(sv_s)], y_range=[-6, 0, 6], x_length=TW * 0.9, y_length=TH * 0.85,
                   tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        lg = lambda v: np.log10(np.maximum(v / v[0], 1e-6))  # noqa: E731
        k = np.arange(len(sv_s))
        out.append((VGroup(ax2, curve(ax2, k, lg(sv_s), SIMCLR, 2.5), curve(ax2, k, lg(sv_n), NAIVE, 2.5)),
                    r"collapse, \ measured", NAIVE))
        rd = load("redundancy")
        out.append((heat(np.asarray(rd["rec_C"])[-1], 1.8, 1.8, vmax=1.0, pos="#5BD17A", neg="#FF9F45"),
                    r"Barlow's identity", BARLOW))
        d = load("dino")
        Pm = np.asarray(d["dino_Pmean"])[-1][:40]
        db = VGroup(*[Rectangle(width=0.05, height=max(1.6 * v / max(Pm.max(), 1e-9), 0.01), stroke_width=0,
                                fill_color=DINO_C, fill_opacity=0.9) for v in Pm]).arrange(RIGHT, buff=0.015,
                                                                                        aligned_edge=DOWN)
        out.append((db, r"a balanced teacher", DINO_C))
        m = load("mae")
        out.append((digit_sheet(np.stack([np.asarray(m["rec_masked"])[-1][0], np.asarray(m["rec_recon"])[-1][0]]), 1, 2,
                                size=1.2, gap=0.1), r"filling in", MAE_C))
        h = load("halves")
        st = np.asarray(h["rec_steps"])
        ax3 = Axes(x_range=[0, st[-1], st[-1]], y_range=[0, 1, 1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax3, curve(ax3, st, h["align_s0"], C.BITS, 2.5), curve(ax3, st, h["align_s1"], C.BITS, 1.5)),
                    r"two halves converge", C.BITS))
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
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A pretext puzzle teaches what the puzzle needs, blind spots and all. A contrastive "
            "loss is a classifier over candidates, and a bound on information capped at the log of their number. "
            "On the sphere it is two forces, alignment and uniformity, balanced by the temperature. Without "
            "something pushing apart, agreement collapses to a constant, and we can measure it. BYOL and SimSiam "
            "escape by asymmetry, Barlow Twins and VICReg by decorrelating dimensions, DINO by balancing a "
            "teacher between two collapses. Masked models learn by filling in; JEPAs predict meanings instead of "
            "pixels. And networks trained apart, on different halves of the same digits, come to agree."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        TW, TH = 3.7, 1.5
        v = load("views")
        orig = np.asarray(v["orig"])
        pics = []
        d = orig[7].astype(float) / 255.0
        pics.append(Group(digit(d, 1.1, frame=True), MathTex(r"\circlearrowright", font_size=36),
                          digit(np.rot90(d, 1), 1.1, frame=True), MathTex(r"\to", font_size=30),
                          Dot(radius=0.12, color=SIMCLR)).arrange(RIGHT, buff=0.15))
        j = load("jepa")
        T = np.asarray(j["ex_targets"])[1].astype(bool)
        G = int(j["grid"])
        b = Group(digit(orig[4].astype(float) / 255.0, 1.4, frame=True))
        s = 1.4 / G
        for r_ in range(G):
            for c_ in range(G):
                sq = Square(s, stroke_color=GREY_D, stroke_width=1).move_to(
                    b.get_corner(UL) + np.array([s * (c_ + 0.5), -s * (r_ + 0.5), 0]))
                if T[r_, c_]:
                    sq.set_fill(JEPA, opacity=0.55)
                b.add(sq)
        pics.append(b)
        cm = load("compare")
        pics.append(heat(np.asarray(cm["cka"]), 1.4, 1.4, vmax=1.0, signed=False, pos=SIMCLR, gamma=1.0))
        mt = load("matryoshka")
        dims = list(mt["runs"][mt["keys"][0]]["extra"]["prefix_dims"])
        Mk = np.mean([mt["runs"][k]["extra"]["prefix_knn"] for k in mt["keys"]], 0)
        ax = Axes(x_range=[0, len(dims) - 1, len(dims) - 1], y_range=[0, 1, 1], x_length=TW * 0.8, y_length=TH * 0.85,
                  tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        pics.append(VGroup(ax, curve(ax, np.arange(len(dims)), Mk, MATRY, 2.5)))
        dn = load("dino")
        Pm = np.asarray(dn["dino_Pmean"])[-1][:30]
        pics.append(VGroup(*[Rectangle(width=0.07, height=max(1.3 * x / max(Pm.max(), 1e-9), 0.01), stroke_width=0,
                                       fill_color=DINO_C, fill_opacity=0.9) for x in Pm]).arrange(RIGHT, buff=0.02,
                                                                                               aligned_edge=DOWN))
        s5 = load("simclr")
        pool = np.asarray(s5["pool"])
        nn = np.asarray(s5["rec_nn"])[-1][0][:4]
        pics.append(digit_sheet(np.concatenate([pool[s5["queries"][0]][None], pool[nn]]), 1, 5, size=0.6, gap=0.06))
        ideas = [(r"invariance from views; \\ symmetry built in", r"$\to$ \ Part 25", SIMCLR),
                 (r"predicting in representation \\ space: \ world models", r"$\to$ \ Part 29", JEPA),
                 (r"probes and CKA: \\ reading what a network knows", r"$\to$ \ Part 30", SIMCLR),
                 (r"nested features, \\ again in sparse autoencoders", r"$\to$ \ Part 30", MATRY),
                 (r"teachers and students: \\ distillation", r"$\to$ \ Part 27", DINO_C),
                 (r"embeddings and retrieval: \\ memory for agents", r"$\to$ \ Part 29", POS)]
        tiles = Group()
        for pic, (idea, dest, col) in zip(pics, ideas):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 1.3, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            pic.move_to(box.get_top() + DOWN * (0.15 + TH / 2))
            il = label(idea, font_size=20, color=col).move_to(box.get_bottom() + UP * 0.72)
            dl = label(dest, font_size=18, color=GREY_A).move_to(box.get_bottom() + UP * 0.24)
            tiles.add(Group(box, pic, il, dl))
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(DOWN * 0.35)
        head = label(r"Where this comes back", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "All of this comes back. Augmentations teach a network what to ignore; next time, Part 25 builds that "
            "symmetry into the network itself. <bookmark mark='p2'/> Prediction in representation space is the "
            "heart of the world models in Part 29. <bookmark mark='p3'/> Probes and CKA are how Part 30 reads what "
            "a network knows, <bookmark mark='p4'/> and Matryoshka's nested features return there, in sparse "
            "autoencoders. <bookmark mark='p5'/> Teachers and students return in Part 27's distillation; <bookmark "
            "mark='p6'/> and embeddings are the memory that the agents of Part 29 search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tiles[0], shift=UP * 0.1))
            for k_, mk in enumerate(["p2", "p3", "p4", "p5", "p6"], 1):
                vo.wait_until(mk)
                self.play(FadeIn(tiles[k_], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"InfoNCE with $N$ candidates: \ show that the optimal critic is $f^*(x, y) = \log \frac{p(y \mid x)}{p(y)} "
            r"+ c(x)$, \ and that $\log N - \mathcal L_N \le \log N$ for every critic.",
            r"For unit vectors, \ show $z \cdot z^+ = 1 - \tfrac12 \|z - z^+\|^2$, \ and derive the $N \to \infty$ limit "
            r"of the contrastive loss as alignment plus uniformity.",
            r"Show that a constant encoder minimizes the SimSiam loss, \ but gives the NT-Xent loss "
            r"$\log(2N - 1)$, \ its largest value at any fixed configuration of perfect agreement.",
            r"Barlow Twins: \ with batch-standardized outputs, \ show $\mathcal C_{ii} = 1$ exactly when the two views' "
            r"$i$-th outputs are equal for every image, \ and why a constant output is excluded.",
            r"Show that linear CKA is unchanged by $X \mapsto cXQ$ ($Q$ orthogonal, $c > 0$), \ and that when $n \le d$ "
            r"any two full-rank representations are related by an invertible linear map.",
            r"DINO: \ show $H(P_t, P_s) = H(P_t) + \mathrm{KL}(P_t \,\|\, P_s)$, \ and that a teacher whose output does "
            r"not depend on the input lets the student reach $\mathrm{KL} = 0$ without learning anything.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the InfoNCE bound to DINO's two collapses. Pause here and work "
            "through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        v = load("views")
        d = np.asarray(v["orig"])[7].astype(float) / 255.0
        head = label(r"Next: \ Part 25, \ Symmetry and Science", font_size=40).to_edge(UP, buff=0.5)
        imgs = Group(*[digit(np.rot90(d, -k), 1.3, frame=True) for k in range(4)]).arrange(RIGHT, buff=0.5)
        imgs.move_to([0, 1.0, 0])
        inv = VGroup(*[Dot(radius=0.1, color=SIMCLR) for _ in range(4)])
        for dd, im in zip(inv, imgs):
            dd.next_to(im, DOWN, buff=0.6)
        eqv = VGroup(*[Arrow(ORIGIN, 0.6 * np.array([math.cos(math.pi / 2 - k * math.pi / 2),
                                                      math.sin(math.pi / 2 - k * math.pi / 2), 0]), buff=0,
                             color=C.BITS, stroke_width=4) for k in range(4)])
        for a, dd in zip(eqv, inv):
            a.move_to(dd.get_center() + DOWN * 1.1)
        l1 = label(r"invariant: \ the same answer for every turn", font_size=22, color=SIMCLR).next_to(inv, LEFT,
                                                                                                    buff=0.5)
        l2 = label(r"equivariant: \ the answer turns with the input", font_size=22, color=C.BITS).next_to(eqv, LEFT,
                                                                                                       buff=0.5)
        with self.voiceover(
            "Next time: symmetry. Our networks learned to ignore a turn of the page only because we showed them "
            "turned pages. Part 25 builds the symmetry into the network, so that its answer either stays the same "
            "when the input turns, or turns along with it, and follows that idea from graphs to proteins, weather "
            "and mathematics."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(i_) for i_ in imgs], lag_ratio=0.2))
            self.play(FadeIn(inv), FadeIn(l1))
            self.play(LaggedStart(*[GrowArrow(a) for a in eqv], lag_ratio=0.2), FadeIn(l2))
            self.wait(max(0.5, vo.remaining() - 0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: Advanced Topics} (2023), chapter 32",
             r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 14",
             r"R.~Balestriero et al., \textit{A Cookbook of Self-Supervised Learning} (2023)"],
            [r"Barlow (1961); \ Becker \& Hinton (1992); \ Bromley et al.\ (1993); \ Hadsell, Chopra \& LeCun (2006); \ "
             r"Vincent et al.\ (2008); \ Gutmann \& Hyv\"arinen (2010); \ Mikolov et al.\ (2013)",
             r"Doersch, Gupta \& Efros (2015); \ Noroozi \& Favaro (2016); \ Zhang, Isola \& Efros (2016); \ Pathak et "
             r"al.\ (2016); \ Gidaris, Singh \& Komodakis (2018); \ Wu et al.\ (2018); \ van den Oord, Li \& Vinyals "
             r"(2018)",
             r"He et al.\ (2020); \ Chen et al.\ (2020); \ Wang \& Isola (2020); \ Wang \& Liu (2021); \ Grill et al.\ "
             r"(2020); \ Richemond et al.\ (2020); \ Chen \& He (2021); \ Tian, Chen \& Ganguli (2021)",
             r"Zbontar et al.\ (2021); \ Bardes, Ponce \& LeCun (2022); \ Garrido et al.\ (2023); \ Hua et al.\ (2021); "
             r"\ Jing et al.\ (2022); \ Roy \& Vetterli (2007); \ Garrido et al.\ (2023, RankMe); \ Balestriero \& "
             r"LeCun (2025)",
             r"Caron et al.\ (2018, 2020, 2021); \ Oquab et al.\ (2023); \ Sim\'eoni et al.\ (2025); \ Fan et al.\ "
             r"(2025)",
             r"Devlin et al.\ (2019); \ Bao et al.\ (2022); \ He et al.\ (2022); \ LeCun (2022); \ Assran et al.\ "
             r"(2023, 2025); \ Bardes et al.\ (2024); \ Mur-Labadia et al.\ (2026)",
             r"Reimers \& Gurevych (2019); \ Karpukhin et al.\ (2020); \ Gao, Yao \& Chen (2021); \ Muennighoff et al.\ "
             r"(2023); \ Kusupati et al.\ (2022); \ Zhang et al.\ (2025); \ Shanbhogue et al.\ (2026)",
             r"Alain \& Bengio (2016); \ Kornblith et al.\ (2019); \ Huh, Cheung, Wang \& Isola (2024)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "To go deeper, the Cookbook of Self-Supervised Learning, by Randall Balestriero and colleagues, is a "
            "practical guide to everything in this part, and Kevin Murphy's second volume covers the theory. "
            "Thanks for watching, and see you in Part 25."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
