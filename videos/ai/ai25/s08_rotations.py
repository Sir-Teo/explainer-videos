from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, GNN_C, KIND_COLOR, KIND_NAME, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C,
                                   load, matrix_image, project, take_away, words_num)

PLUS, MINUS = "#F2A07B", "#8FB9EE"


class Rotations(VoiceoverScene):
    def construct(self):
        self.card()
        self.forces()
        self.egnn()
        self.harmonics()
        self.curves()
        self.replay()

    def card(self):
        card = chapter_card(7, r"Networks that turn with the molecule", r"How do you build rotations into a network?",
                            lit=(), part=PART)
        with self.voiceover("Chapter seven. Networks that turn with the molecule."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forces(self):
        d = definition_card(r"E(3)", r"the rigid motions of space: \ rotations $R$, \ reflections, \ translations "
                            r"$t$; \ a point moves as $x \mapsto Rx + t$", width=6.0, font_size=23).move_to([-3.6, 1.9, 0])
        rows = [
            cmath(r"E(Rx + t)", r"=", r"E(x)", font_size=36),
            cmath(r"R^\top \nabla E(Rx + t)", r"=", r"\nabla E(x)", font_size=36),
            cmath(r"\nabla E(Rx + t)", r"=", r"R \, \nabla E(x)", font_size=36),
            cmath(r"F(Rx + t)", r"=", r"R \, F(x)", font_size=36),
        ]
        whys = [why(r"the energy is invariant"), why(r"differentiate in $x$: \ the chain rule"),
                why(r"multiply by $R$: \ $R R^\top = I$"), why(r"forces $F = -\nabla E$ \ turn with the molecule")]
        for r_ in rows:
            r_[0].set_color(STRUCT)
        step = ladder(self, rows, whys, keep=4, top=0.6, x=-0.6, buff=0.45, edge=6.9)
        with self.voiceover(
            "For molecules and materials the symmetry is the group of rigid motions of space, E of three: "
            "rotations, reflections and translations. <bookmark mark='a'/> The energy of a molecule is invariant "
            "under all of them. <bookmark mark='b'/> Differentiate both sides with respect to the positions: the "
            "chain rule brings out the transpose of R. <bookmark mark='c'/> Multiply by R, <bookmark mark='d'/> and "
            "since forces are minus the gradient of the energy, the forces turn with the molecule: they are "
            "equivariant. An invariant model of the energy gives equivariant forces for free, by differentiation, "
            "which is how most machine-learned potentials compute them."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.1))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def egnn(self):
        rows = [
            cmath(r"m_{ij}", r"=", r"\phi_e\big(h_i, h_j, \|x_i - x_j\|^2\big)", font_size=34),
            cmath(r"x_i'", r"=", r"x_i + C \sum_{j} (x_i - x_j)\, \phi_x(m_{ij})", font_size=34),
            cmath(r"h_i'", r"=", r"\phi_h\Big(h_i, \sum_j m_{ij}\Big)", font_size=34),
            cmath(r"(Rx_i + t) + C \sum_j R(x_i - x_j)\, \phi_x(m_{ij})", r"=", r"R x_i' + t", font_size=34),
        ]
        rows[0][2].set_color(STRUCT)
        rows[3][2].set_color(STRUCT)
        whys = [why(r"messages see only distances: \ unchanged by $R$ and $t$"),
                why(r"positions move along the differences"),
                why(r"the features stay invariant"),
                why(r"turn and shift the input: \ differences turn, \ shifts cancel")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.5, edge=6.9)
        hist = VGroup(
            label(r"SchNet (Sch\"utt et al.\ 2017): \ invariant, \ filters of distances", font_size=21, color=GREY_A),
            label(r"EGNN (Satorras, Hoogeboom \& Welling 2021): \ invariant features, \ equivariant positions",
                  font_size=21, color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How do you build that into a network? The simplest answer is the E(n)-equivariant graph network of "
            "Victor Garcia Satorras, Emiel Hoogeboom and Max Welling, in 2021. Each atom has features h and a "
            "position x. <bookmark mark='a'/> The message between two atoms sees their features and the squared "
            "distance between them, nothing else: turning or moving the molecule changes no message. <bookmark "
            "mark='b'/> Each atom then moves along the differences of positions, weighted by learned scalars. "
            "<bookmark mark='c'/> And its features update from the summed messages, so they stay invariant. "
            "<bookmark mark='d'/> Now turn and shift the input. The messages are unchanged, the differences turn by "
            "R, and the shift cancels in every difference, so the new positions are the old ones turned and shifted. "
            "Equivariance, line by line. <bookmark mark='e'/> SchNet, four years earlier, had used distances alone, "
            "for invariant energies."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("e")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonics(self):
        h = load("harmonics")
        D = np.asarray(h["D"], float)
        img = matrix_image(np.abs(D), size=3.6, vmin=0, vmax=1).move_to([-3.4, -0.2, 0])
        n = 9
        cell = 3.6 / n
        x0, y0 = img.get_left()[0], img.get_top()[1]
        boxes = VGroup()
        for a, b, col in ((0, 1, STRUCT), (1, 4, SYM), (4, 9, AUG)):
            boxes.add(Rectangle(width=cell * (b - a), height=cell * (b - a), stroke_color=col, stroke_width=2.5)
                      .move_to([x0 + cell * (a + b) / 2, y0 - cell * (a + b) / 2, 0]))
        il = label(r"$|D|$ for one rotation: \ how it mixes $Y_\ell^m$", font_size=22, color=GREY_A).next_to(img, UP,
                                                                                                         buff=0.2)
        degs = VGroup(label(r"$\ell = 0$: \ $1$ scalar", font_size=22, color=STRUCT),
                      label(r"$\ell = 1$: \ $3$ components, \ a vector", font_size=22, color=SYM),
                      label(r"$\ell = 2$: \ $5$, \ like a quadrupole", font_size=22, color=AUG))
        degs.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([2.4, 1.6, 0])
        off = float(h["off_max"])
        dp = int(np.floor(-np.log10(max(off, 1e-300))))
        facts = VGroup(
            label(rf"outside the blocks: \ at most ${sci(off, 0)}$ \ (rounding)", font_size=22, color=GREY_A),
            label(r"features of degree $\ell$ turn by their own block $D^{(\ell)}(R)$", font_size=22, color=GREY_A),
            label(r"two features multiply into degrees $|\ell_1 - \ell_2|, \dots, \ell_1 + \ell_2$ \ "
                  r"(Clebsch--Gordan)", font_size=22, color=GREY_A),
            label(r"tensor field networks (2018), \ NequIP (2022), \ MACE (2022), \ e3nn", font_size=22,
                  color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.6, -1.2, 0])
        tag = note(r"computed: \ least squares on $20{,}000$ points of the sphere", font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            "EGNN carries two kinds of information: scalars, which don't turn, and positions, which turn like "
            "vectors. Richer models carry more. <bookmark mark='a'/> Any function on the sphere can be written in "
            "spherical harmonics, of degree zero, one, two and up. <bookmark mark='b'/> Here, computed, is what one "
            "rotation does to the nine harmonics of degree up to two: it mixes them only within their degree, in "
            f"blocks of one, three and five; outside the blocks the entries are zero to {dp} decimal places. "
            "<bookmark mark='c'/> So a network can keep features of each degree, turn each with its own block, and "
            "combine two of them into new degrees with the Clebsch–Gordan rules, the same rules that add angular "
            "momenta in quantum mechanics. <bookmark mark='d'/> That is the design of tensor field networks, and "
            "of NequIP and MACE, among today's most accurate learned force fields."
        ) as vo:
            self.play(FadeIn(img), FadeIn(il), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(degs))
            vo.wait_until("b")
            self.play(Create(boxes), FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        nb = load("nbody")
        nd = load("nbody_data")
        sizes = list(nb["sizes"])
        kinds = list(nb["kinds"])
        lx = np.log10(sizes)
        T = nb["table"]
        allv = np.array([[T[k][str(n)] for n in sizes] for k in kinds])
        lo, hi = np.floor(np.log10(allv.min()) * 2) / 2, np.ceil(np.log10(max(allv.max(), nd["mse_constvel"])) * 2) / 2
        g = axes([lx[0], lx[-1]], [lo, hi], x_length=6.0, y_length=3.9, xlabel=r"training systems",
                 ylabel=r"test error \ (mean squared, \ log scale)", xticks=list(lx),
                 yticks=[v for v in np.arange(np.ceil(lo), hi + 0.01, 1.0)],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"10^{{{int(round(v))}}}",
                 center=[-2.3, -0.2, 0])
        cv = np.log10(nd["mse_constvel"])
        cvl = DashedLine(g.ax.c2p(lx[0], cv), g.ax.c2p(lx[-1], cv), color=GREY_C)
        cvt = label(r"keep going in a straight line", font_size=18, color=GREY_C).next_to(cvl, UP, buff=0.05)
        cvt.align_to(cvl, RIGHT)
        objs = {}
        for k in kinds:
            A = np.log10(np.array([T[k][str(n)] for n in sizes]))
            col = KIND_COLOR[k]
            objs[k] = VGroup(band(g.ax, lx, A.min(1), A.max(1), col, 0.2), curve(g.ax, lx, A.mean(1), col, 3.5),
                             VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(lx, A.mean(1))]))
        lg = legend([(KIND_COLOR[k], KIND_NAME[k]) for k in kinds], font_size=20).move_to([4.3, 1.4, 0])
        P = nb["params"]
        par = label(r"weights: \ " + r", \ ".join(rf"{KIND_NAME[k]} ${P[k]:,}$".replace(",", "{,}") for k in kinds),
                    font_size=17, color=GREY_B).to_edge(DOWN, buff=0.25)
        tag = note(rf"computed: \ three seeds \ (band: \ min--max), \ ${nb['steps']:,}$ steps each".replace(",", "{,}"),
                   font_size=20).to_corner(UR, buff=0.2)
        m = {k: float(np.mean(T[k][str(sizes[-1])])) for k in kinds}
        m0 = {k: float(np.mean(T[k][str(sizes[0])])) for k in kinds}
        eg_small, best_other_big = m0["egnn"], min(m["gnn"], m["mlp"], m["mlp_aug"])
        cross = ("With only a hundred, EGNN already beats every other network trained on thirty times as many" if
                 eg_small < best_other_big else
                 f"With a hundred systems its error is {eg_small:.4f}; the best of the others needs the full "
                 f"{sizes[-1]:,} to reach {best_other_big:.4f}")
        ratio = m["mlp"] / m["egnn"]
        ratio_txt = f"{ratio:.0f} times smaller than the MLP's" if ratio >= 2 else "close to the MLP's"
        cvm = float(nd["mse_constvel"])
        mlp_txt = (f"The plain MLP ends at {m['mlp']:.3f}, no better than that guess of {cvm:.3f}" if
                   m["mlp"] >= 0.97 * cvm else f"The plain MLP ends at {m['mlp']:.3f}, below that guess of {cvm:.3f}")
        aug_txt = ("Turned copies help the MLP" if m["mlp_aug"] < 0.97 * m["mlp"] else
                   "Turned copies barely help it at this budget")
        with self.voiceover(
            "Does it pay? Our five-body system again: predict where the particles are at time one, given where "
            "they are and how they move. Four networks, the same three thousand training steps, from a hundred "
            f"training systems up to {sizes[-1]:,}, three seeds each. <bookmark mark='a'/> The dashed line is the "
            "simplest guess, that every particle keeps going in a straight line. <bookmark mark='b'/> "
            f"{mlp_txt}. {aug_txt}: {m['mlp_aug']:.3f}. <bookmark mark='c'/> Message passing on raw "
            f"coordinates: {m['gnn']:.3f}. <bookmark mark='d'/> EGNN: {m['egnn']:.4f}, {ratio_txt}. {cross}."
        ) as vo:
            self.play(FadeIn(g), Create(cvl), FadeIn(cvt), FadeIn(tag), FadeIn(par))
            vo.wait_until("a")
            self.play(Indicate(cvt))
            vo.wait_until("b")
            self.play(FadeIn(objs["mlp"]), FadeIn(objs["mlp_aug"]), FadeIn(lg[2]), FadeIn(lg[3]))
            vo.wait_until("c")
            self.play(FadeIn(objs["gnn"]), FadeIn(lg[1]))
            vo.wait_until("d")
            self.play(FadeIn(objs["egnn"]), FadeIn(lg[0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        nb = load("nbody")
        nd = load("nbody_data")
        snaps = list(nb["snaps"])
        big = nb["sizes"][-1]
        k = 1
        x0 = np.asarray(nd["show_x0"])[k]
        traj = np.asarray(nd["show_traj"])[k]
        q = np.asarray(nd["show_q"])[k]
        fe = [np.asarray(f)[k] for f in nb[f"egnn_{big}_s0"]["frames"]]
        fm = [np.asarray(f)[k] for f in nb[f"mlp_{big}_s0"]["frames"]]
        ang, tilt = 0.4, 0.3
        allp = np.concatenate([traj.reshape(-1, 3), np.concatenate(fe), np.concatenate(fm)])
        c0 = traj.reshape(-1, 3).mean(0)
        P2, _ = project(allp - c0, ang, tilt)
        sc = 2.4 / max(np.abs(P2[: traj.size // 3]).max(), 1e-9)

        def to_scr(X, center):
            P, _ = project(np.asarray(X) - c0, ang, tilt)
            return [np.array([center[0] + sc * p[0], center[1] + sc * p[1], 0]) for p in P]

        panels = []
        for cx, name, col in ((-3.4, KIND_NAME["egnn"], STRUCT), (3.4, KIND_NAME["mlp"], PLAIN)):
            c = np.array([cx, 0.1, 0])
            paths = VGroup(*[VMobject(stroke_color=TRUE_C, stroke_width=2, stroke_opacity=0.6).set_points_smoothly(
                to_scr(traj[:, i], c)) for i in range(traj.shape[1])])
            start = VGroup(*[Dot(p, radius=0.07, color=PLUS if qq > 0 else MINUS) for p, qq in zip(to_scr(x0, c), q)])
            end = VGroup(*[Circle(radius=0.11, stroke_color=TRUE_C, stroke_width=2.5).move_to(p)
                           for p in to_scr(traj[-1], c)])
            frame = Rectangle(width=6.3, height=5.3, stroke_color=GREY_D, stroke_width=1).move_to(c)
            ttl = label(name, font_size=26, color=col).next_to(frame, UP, buff=0.1)
            panels.append(dict(c=c, paths=paths, start=start, end=end, frame=frame, ttl=ttl, col=col))
        steps_l = label(r"step $0$", font_size=22, color=GREY_A).move_to([0, -3.0, 0])
        lg = VGroup(label(r"true paths, \ to $t = 1$", font_size=18, color=TRUE_C),
                    label(r"$\times$ \ predicted end points", font_size=18, color=PRED_C)).arrange(RIGHT, buff=0.5)
        lg.next_to(steps_l, UP, buff=0.12)

        def marks(F, p):
            return VGroup(*[MathTex(r"\times", font_size=34, color=p["col"]).move_to(pt) for pt in to_scr(F, p["c"])])

        cur = [marks(fe[0], panels[0]), marks(fm[0], panels[1])]
        ce = np.asarray(nb[f"egnn_{big}_s0"]["curve"])
        cm = np.asarray(nb[f"mlp_{big}_s0"]["curve"])
        err_e = float(np.sqrt(((fe[-1] - traj[-1]) ** 2).sum(-1).mean()))
        err_m = float(np.sqrt(((fm[-1] - traj[-1]) ** 2).sum(-1).mean()))
        with self.voiceover(
            f"Here is training itself, for the runs on {big:,} systems: one test system the networks never saw, "
            "its five particles, and where they really go by time one, the blue paths. <bookmark mark='a'/> The "
            "crosses are each network's predicted end points, at checkpoints through training. <bookmark mark='b'/> "
            f"EGNN's crosses settle onto the circles; by the end its predicted positions are off by {err_e:.2f} "
            f"on average. The MLP's end {err_m:.2f} away."
        ) as vo:
            for p in panels:
                self.play(FadeIn(p["frame"]), FadeIn(p["ttl"]), Create(p["paths"]), FadeIn(p["start"]),
                          FadeIn(p["end"]), run_time=1.2)
            self.play(FadeIn(steps_l), FadeIn(lg))
            vo.wait_until("a")
            self.play(FadeIn(cur[0]), FadeIn(cur[1]))
            per = max(0.4, vo.until("b") / max(1, len(snaps) - 1))
            for j in range(1, len(snaps)):
                new = [marks(fe[j], panels[0]), marks(fm[j], panels[1])]
                nl = label(rf"step ${snaps[j]:,}$".replace(",", "{,}"), font_size=22, color=GREY_A).move_to(steps_l)
                self.play(ReplacementTransform(cur[0], new[0]), ReplacementTransform(cur[1], new[1]),
                          ReplacementTransform(steps_l, nl), run_time=0.7 * per)
                cur, steps_l = new, nl
                self.wait(0.3 * per)
            vo.wait_until("b")
        self.wait(0.6)
        tk = take_away(r"build the symmetry in, \ and the data goes further: \ nothing is spent learning that turning "
                       r"doesn't matter")
        with self.voiceover(
            "That is the case for equivariance: nothing in the data has to be spent teaching the network that a "
            "turned molecule is the same molecule. Proteins are molecules too, and the rest of this part is about "
            "where these ideas took science, starting with the hardest molecule of all."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
