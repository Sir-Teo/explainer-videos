from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, CHAIN_GRAD, HIST, LEAN_C, MSA_C, PAIR_C, PART, PLAIN, STRUCT, SYM, TRUE_C,
                                   chain3d, field_image, load, node_box, project)
from videos.ai.ai25.physics import rot_axis

PLUS, MINUS = "#F2A07B", "#8FB9EE"


class Hook(VoiceoverScene):
    def construct(self):
        self.nobel()
        self.turn()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def nobel(self):
        f = load("fold")
        X = np.asarray(f["X"])
        chain = chain3d(X, scale=0.17, center=[-3.6, 0.2, 0], angle=0.6, tilt=0.5, gradient=CHAIN_GRAD, width=4)
        tag = note(r"a three-helix bundle, \ built here from helix geometry \ (illustrative)", font_size=20)
        tag.next_to(chain, DOWN, buff=0.3)
        card = history_card(2024, r"The Nobel Prize in Chemistry",
                            r"one half to David Baker, \ for computational protein design; \ the other half jointly "
                            r"to Demis Hassabis and John Jumper, \ for protein structure prediction", width=6.6,
                            color=HIST).move_to([3.2, 1.0, 0])
        phys = label(r"the same week: \ physics, \ to John Hopfield \\ and Geoffrey Hinton \ (Part 20)", font_size=22,
                     color=GREY_B).next_to(card, DOWN, buff=0.45).align_to(card, LEFT)
        cite_ = cite(r"Royal Swedish Academy of Sciences, \ 9 October 2024", corner=DR)
        with self.voiceover(
            "Stockholm, October 2024. <bookmark mark='a'/> The Nobel Prize in Chemistry goes half to David Baker, for "
            "designing proteins on a computer, and half to Demis Hassabis and John Jumper of Google DeepMind, for "
            "AlphaFold, a neural network that predicts the shape a protein folds into. <bookmark mark='b'/> The day "
            "before, the physics prize had gone to John Hopfield and Geoffrey Hinton, for the neural networks of Part "
            "20. <bookmark mark='c'/> For decades, measuring the shape of a single protein could take a laboratory "
            "years. AlphaFold predicts one in minutes, often to within the width of an atom."
        ) as vo:
            self.play(Create(chain.segs, lag_ratio=0.03), FadeIn(chain.dots), run_time=2.5)
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.15), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(phys))
            vo.wait_until("c")
            self.play(Indicate(chain, color=PAIR_C, scale_factor=1.04), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turn(self):
        e = load("equivariance")
        x0 = np.asarray(e["sweep_x0"], float)
        q = np.asarray(e["sweep_q"], float)
        th = np.asarray(e["sweep_theta"], float)
        U = float(e["sweep_true_energy"])
        curves = {k: np.asarray(e[f"sweep_energy_{k}"], float) for k in ("inv", "mlp", "mlp_aug")}
        axis = np.array([0.3, 1.0, 0.2])
        center = np.array([-3.6, 0.0, 0])
        S = 0.85
        t = ValueTracker(0.0)

        def pos(theta):
            R = rot_axis(axis, theta)
            P, depth = project((x0 - x0.mean(0)) @ R.T, 0.0, 0.25)
            return P, depth

        def mol():
            P, depth = pos(t.get_value())
            pts = [center + S * np.array([p[0], p[1], 0]) for p in P]
            g = VGroup()
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    g.add(Line(pts[i], pts[j], color=GREY_D, stroke_width=1.2, stroke_opacity=0.5))
            order = np.argsort(depth)
            for i in order:
                r = 0.16 * (1 + 0.12 * depth[i])
                c = PLUS if q[i] > 0 else MINUS
                d = Circle(radius=r, stroke_width=1.5, stroke_color=WHITE, fill_color=c, fill_opacity=0.95).move_to(pts[i])
                s_ = MathTex("+" if q[i] > 0 else "-", font_size=22, color=BLACK).move_to(pts[i])
                g.add(d, s_)
            return g

        molecule = always_redraw(mol)
        lo = min(U, *[c.min() for c in curves.values()])
        hi = max(U, *[c.max() for c in curves.values()])
        pad = 0.15 * (hi - lo + 1e-3)
        lo_, hi_ = lo - pad, hi + pad
        g = axes([0, 2 * np.pi], [lo_, hi_], x_length=6.0, y_length=3.6, xlabel=r"how far the molecule is turned",
                 ylabel=r"predicted energy", xticks=[0, np.pi, 2 * np.pi], yticks=[],
                 xfmt=lambda v: {0: "0", 1: r"180^\circ", 2: r"360^\circ"}[int(round(v / np.pi))],
                 center=[3.0, -0.3, 0])
        true_line = DashedLine(g.ax.c2p(0, U), g.ax.c2p(2 * np.pi, U), color=TRUE_C, stroke_width=2.5)
        tl = label(r"the true energy \ (it can't change)", font_size=20, color=TRUE_C)
        tl.move_to(g.ax.c2p(np.pi, U) + UP * 0.22)

        def live(kind, col):
            ys = curves[kind]

            def make():
                v = t.get_value()
                k = int(np.searchsorted(th, v, side="right"))
                xs = list(th[:k]) + [v]
                yv = list(ys[:k]) + [float(np.interp(v, th, ys))]
                if len(xs) < 2:
                    return VectorizedPoint(g.ax.c2p(0, ys[0]))
                return VMobject(stroke_color=col, stroke_width=3.5).set_points_as_corners(
                    [g.ax.c2p(a, b) for a, b in zip(xs, yv)])
            return always_redraw(make)

        live_mlp, live_inv, live_aug = live("mlp", PLAIN), live("inv", STRUCT), live("mlp_aug", AUG)
        lg = legend([(PLAIN, r"a plain network (MLP)"), (AUG, r"the MLP, shown turned copies"),
                     (STRUCT, r"a network built on distances")], font_size=20)
        lg.next_to(g, DOWN, buff=0.2).align_to(g.ax, LEFT)
        rng_m = float(curves["mlp"].max() - curves["mlp"].min())
        rng_a = float(curves["mlp_aug"].max() - curves["mlp_aug"].min())
        rng_i = float(curves["inv"].max() - curves["inv"].min())
        inv_err = abs(float(curves["inv"].mean()) - U)
        tag = note(r"computed: \ five charged particles, \ networks trained here on $3{,}000$ of them",
                   font_size=20).to_corner(DL, buff=0.25)
        if rng_i < 1e-6:
            tiny = "less than a millionth of a unit, rounding error"
        elif rng_i < 1e-4:
            tiny = "less than a ten-thousandth of a unit, rounding error"
        else:
            tiny = f"{rng_i:.4f} of a unit, more than rounding error alone"
        with self.voiceover(
            "Here is the idea this part is built on. Five charged particles: a toy molecule. Turn it in space, and "
            "nothing about it changes, so its energy can't change either. <bookmark mark='a'/> We trained networks on "
            "three thousand such molecules to predict that energy, then turned this one, a full circle. <bookmark "
            f"mark='b'/> A plain network has no idea that turning is harmless: its answer swings over {rng_m:.2f} "
            f"units as the molecule turns. <bookmark mark='c'/> Shown turned copies during training, it swings over "
            f"{rng_a:.2f}. <bookmark mark='d'/> And a network built on the distances between the particles cannot see "
            f"the turn at all: its answer changes by {tiny}, and it sits {inv_err:.2f} from the true "
            "energy."
        ) as vo:
            self.add(molecule)
            self.play(FadeIn(g), Create(true_line), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lg[0]))
            self.add(live_mlp)
            self.play(t.animate.set_value(2 * np.pi), run_time=max(2.0, vo.until("b") + 2.0), rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(lg[1]))
            t.set_value(0.0)
            self.add(live_aug)
            self.play(t.animate.set_value(2 * np.pi), run_time=max(2.0, vo.until("d") - 0.3), rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(lg[2]))
            t.set_value(0.0)
            for m_ in (live_mlp, live_aug):
                m_.clear_updaters()
            self.add(live_inv)
            self.play(t.animate.set_value(2 * np.pi), run_time=max(2.0, vo.remaining() - 0.5), rate_func=linear)
        for m_ in (live_inv, molecule):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        f = load("fold")
        w = load("weather")
        X = np.asarray(f["X"])
        q = label(r"What does a network gain \\ by knowing the symmetries of its problem?", font_size=40)
        q.to_edge(UP, buff=0.6)
        TW = 2.6
        tiles = Group()
        pics = [
            chain3d(X, scale=0.085, angle=0.6, tilt=0.5, gradient=CHAIN_GRAD, width=2.5, dots=False),
            field_image(np.asarray(w["show_truth"])[2], size=2.0),
            VGroup(*[Dot([np.cos(a), np.sin(a), 0], radius=0.09, color=c) for a, c in
                     zip(np.linspace(0, 2 * np.pi, 7)[:-1], [MSA_C, SYM, MSA_C, SYM, MSA_C, SYM])],
                   *[Line([np.cos(a), np.sin(a), 0], [np.cos(b), np.sin(b), 0], color=GREY_C, stroke_width=2)
                     for a, b in zip(np.linspace(0, 2 * np.pi, 7)[:-1], np.linspace(0, 2 * np.pi, 7)[1:])]),
            code_block(["theorem t (a b : Nat) :", "  a + b = b + a := by", "  omega"], font_size=18, color=LEAN_C),
        ]
        caps = [r"proteins", r"weather", r"materials", r"mathematics"]
        cols = [PAIR_C, TRUE_C, MSA_C, LEAN_C]
        for pic, cap, col in zip(pics, caps, cols):
            box = RoundedRectangle(width=TW + 0.3, height=TW + 0.7, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TW - 0.2:
                pic.height = TW - 0.2
            pic.move_to(box.get_center() + UP * 0.25)
            c = label(cap, font_size=24, color=col).move_to(box.get_bottom() + UP * 0.3)
            tiles.add(Group(box, pic, c))
        tiles.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.7)
        sch = note(r"each tile: \ data from this part's own computations, \ or illustrative").to_corner(DR, buff=0.2)
        with self.voiceover(
            "That is the question of this part: what does a network gain by knowing the symmetries of its problem, "
            "and what has that done for science? <bookmark mark='a'/> We'll build the answer from groups and "
            "graphs, through networks that turn with the molecule, to the systems that fold proteins, <bookmark "
            "mark='b'/> forecast the weather, <bookmark mark='c'/> search for new materials, <bookmark mark='d'/> and "
            "prove theorems. Every experiment along the way is computed on this machine; every number about the big "
            "systems is quoted from their own papers."
        ) as vo:
            self.play(Write(q), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(Group(t_[0], t_[2])) for t_ in tiles], lag_ratio=0.2), FadeIn(sch))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(tiles[k][1], shift=UP * 0.15), Indicate(tiles[k][2], scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Symmetry and Science", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"symmetry: \ groups, \ invariance and equivariance; \ functions of sets",
            r"graphs: \ message passing, \ the Weisfeiler--Leman limit, \ smoothing, \ attention",
            r"rotations: \ networks that turn with the molecule",
            r"proteins: \ the folding problem, \ AlphaFold 2 and 3, \ protein design",
            r"fields: \ weather on a mesh, \ neural operators; \ materials by the million",
            r"mathematics: \ geometry, \ proofs in Lean, \ discovery by search",
        ], font_size=25)
        with self.voiceover(
            "This is Part 25 of AI, Built, the last part of its fourth act. <bookmark mark='a'/> In this part: "
            "symmetry, and what it means for a function to respect it; <bookmark mark='o2'/> graphs, the networks "
            "that pass messages along them, and the limit of what they can tell apart; <bookmark mark='o3'/> networks "
            "that turn with the molecule; <bookmark mark='o4'/> proteins, from the folding problem to AlphaFold and "
            "protein design; <bookmark mark='o5'/> fields: the weather, and neural operators, and the search for "
            "materials; <bookmark mark='o6'/> and mathematics, from olympiad geometry to proofs a machine can check, "
            "and discovery by search."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            veils = VGroup(*[Rectangle(width=r_.width + 0.3, height=r_.height + 0.14, stroke_width=0,
                                       fill_color=config.background_color, fill_opacity=0.72).move_to(r_)
                             for r_ in obj.rows])
            mark = Triangle(color=C.BITS, fill_opacity=1, stroke_width=0).rotate(-PI / 2).scale(0.1)
            mark.next_to(obj.rows[0], LEFT, buff=0.15)
            self.play(FadeOut(smap), FadeIn(obj), FadeIn(veils[1:]), FadeIn(mark))
            for k, mk in enumerate(["o2", "o3", "o4", "o5", "o6"], 1):
                vo.wait_until(mk)
                self.play(FadeOut(veils[k]), mark.animate.next_to(obj.rows[k], LEFT, buff=0.15), run_time=0.5)
            self.play(FadeOut(mark), run_time=0.4)
        self.wait(0.3)
        self.clear_scene()
