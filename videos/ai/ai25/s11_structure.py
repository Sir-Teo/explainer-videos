from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (CHAIN_GRAD, HIST, MIRROR_C, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C,
                                   chain3d, load, node_box, take_away, words_num)


def frame_glyph(center, angle, color=SYM, s=0.55):
    """A residue as a rigid body: a small triangle (N, C-alpha, C) with its two in-plane axes."""
    c = np.asarray(center, float)
    R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    pts = [c + R @ np.array(p) * s for p in ([-0.8, -0.45, 0], [0, 0, 0], [0.8, -0.45, 0])]
    tri = Polygon(*pts, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.15)
    ex = Arrow(c, c + R @ np.array([1, 0, 0]) * s * 1.2, buff=0, color=PAIR_C, stroke_width=3,
               max_tip_length_to_length_ratio=0.25)
    ey = Arrow(c, c + R @ np.array([0, 1, 0]) * s * 1.2, buff=0, color=STRUCT, stroke_width=3,
               max_tip_length_to_length_ratio=0.25)
    return VGroup(tri, ex, ey, Dot(c, radius=0.05, color=WHITE))


class Structure(VoiceoverScene):
    def construct(self):
        self.card()
        self.frames()
        self.fape()
        self.mirror()
        self.recycling()
        self.database()

    def card(self):
        card = chapter_card(10, r"AlphaFold 2: \ frames, FAPE and recycling", r"How do you build a structure that "
                            r"knows left from right?", lit=(), part=PART)
        with self.voiceover("Chapter ten. AlphaFold 2: frames, FAPE and recycling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def frames(self):
        rng = np.random.default_rng(4)
        gas = VGroup(*[frame_glyph([x, y, 0], a) for x, y, a in
                       zip(rng.uniform(-6.0, -1.5, 7), rng.uniform(-2.2, 1.6, 7), rng.uniform(0, 2 * np.pi, 7))])
        gl = label(r"a `residue gas': \ every residue a rigid body, \ $T_i = (R_i, t_i)$", font_size=22, color=SYM)
        gl.to_edge(UP, buff=0.4).shift(LEFT * 2.6)
        rows = [
            cmath(r"a_{ij}", r"\ni", r"-\big\| T_i \vec q_i - T_j \vec k_j \big\|^2", font_size=32),
            cmath(r"\big\| T\, T_i \vec q_i - T\, T_j \vec k_j \big\|", r"=", r"\big\| T_i \vec q_i - T_j \vec k_j "
                  r"\big\|", font_size=32),
            cmath(r"T_i", r"\leftarrow", r"T_i \circ \Delta T_i", font_size=32),
        ]
        whys = [why(r"points placed in each residue's own frame"), why(r"a rigid motion $T$ keeps distances"),
                why(r"each frame moves by an update \ read in its own frame")]
        step = ladder(self, rows, whys, keep=3, top=1.0, x=2.8, buff=0.55, edge=6.9)
        ipa = label(r"invariant point attention: \ $8$ layers, \ shared weights", font_size=24, color=STRUCT)
        ipa.move_to([2.6, 2.6, 0])
        with self.voiceover(
            "The structure module treats each residue as a rigid body: a little triangle of three backbone atoms, "
            "with its own frame, a rotation and a position. <bookmark mark='a'/> It starts with all the frames "
            "piled at the origin, a residue gas, and moves them. <bookmark mark='b'/> Its attention, invariant point "
            "attention, places learned points in each residue's own frame and scores pairs of residues by how close "
            "those points come in space. <bookmark mark='c'/> A rigid motion of the whole protein moves every point "
            "the same way, so these distances, and the attention, don't change. <bookmark mark='d'/> Each layer then "
            "nudges every frame by an update expressed in that frame's own coordinates, so the updates turn with the "
            "protein: equivariance, again, built in."
        ) as vo:
            self.play(FadeIn(gl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_, scale=0.6) for g_ in gas], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ipa))
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fape(self):
        rows = [
            cmath(r"x_{ij}", r"=", r"T_i^{-1} \circ x_j", font_size=34),
            cmath(r"\mathrm{FAPE}", r"=", r"\frac{1}{Z}\, \mathrm{mean}_{i,j} \min\big(d_{\mathrm{clamp}},\ \| x_{ij} - "
                  r"x_{ij}^{\mathrm{true}} \|\big)", font_size=34),
            cmath(r"(T\,T_i)^{-1} \circ (T\,x_j)", r"=", r"T_i^{-1} \circ x_j", font_size=34),
        ]
        rows[1][0].set_color(PAIR_C)
        whys = [why(r"atom $j$ seen from residue $i$'s frame"),
                why(r"every atom, from every frame; \ $d_{\mathrm{clamp}} = Z = 10$\,\AA"),
                why(r"a rigid motion of the whole: \ cancels")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=0.55, edge=6.9)
        note1 = label(r"but the frames are built right-handed: \ a mirror image is not a rigid motion", font_size=24,
                      color=MIRROR_C).to_edge(DOWN, buff=0.9)
        cite_ = cite(r"Jumper et al., \textit{Nature} (2021), \ supplementary information", corner=DR)
        head = label(r"the loss: \ frame-aligned point error", font_size=32, color=PAIR_C).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What should the network be trained to minimize? AlphaFold 2's answer is the frame-aligned point error, "
            "FAPE. <bookmark mark='a'/> Stand in residue i's frame and look at atom j: that gives its position as "
            "residue i sees it. <bookmark mark='b'/> Do this for every atom, from every frame, in the prediction and "
            "in the true structure, and average the differences, each capped at ten ångströms so that a few wild "
            "atoms don't dominate. <bookmark mark='c'/> Move the whole structure rigidly, and the motion cancels: "
            "FAPE doesn't care where the protein sits or how it is turned. <bookmark mark='d'/> But the frames are "
            "built from three atoms by a right-hand rule. A mirror image is not a rigid motion, so FAPE sees it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(cite_))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(note1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mirror(self):
        f = load("fold")
        X = np.asarray(f["X"])
        M = X * np.array([1, 1, -1])
        left = chain3d(X, scale=0.11, center=[-4.5, 0.9, 0], angle=0.6, tilt=0.5, gradient=CHAIN_GRAD, width=3,
                       dots=False)
        right = chain3d(M, scale=0.11, center=[-1.6, 0.9, 0], angle=0.6, tilt=0.5, color=MIRROR_C, width=3,
                        dots=False)
        mline = DashedLine([-3.05, 2.6, 0], [-3.05, -0.8, 0], color=GREY_C)
        ll = VGroup(label(r"the fold", font_size=22, color=TRUE_C).next_to(left, DOWN, buff=0.15),
                    label(r"its mirror image", font_size=22, color=MIRROR_C).next_to(right, DOWN, buff=0.15))
        hdr = [r"", r"distance RMSD", r"RMSD", r"FAPE"]
        xs = [-1.2, 1.6, 3.6, 5.4]
        y0 = -1.7

        def row(name, vals, col, y):
            g = VGroup(label(name, font_size=22, color=col).move_to([xs[0] - 2.3, y, 0]))
            for v, x in zip(vals, xs[1:]):
                g.add(MathTex(v, font_size=28, color=col).move_to([x, y, 0]))
            return g

        head = VGroup(*[label(h, font_size=21, color=GREY_A).move_to([x, y0, 0]) for h, x in zip(hdr, xs) if h])
        runs = f["runs"]
        good = [r for r in runs if r["rmsd"] < r["rmsd_mirror"]]
        bad = [r for r in runs if r["rmsd"] >= r["rmsd_mirror"]]
        r1 = row(r"mirror image", [f"{f['drmsd_mirror']:.2f}", f"{f['rmsd_mirror']:.1f}", f"{f['fape_mirror']:.2f}"],
                 MIRROR_C, y0 - 0.55)
        r2 = row(r"every atom moved $1$\,\AA", [f"{f['drmsd_noisy']:.2f}", f"{f['rmsd_noisy']:.1f}",
                                                 f"{f['fape_noisy']:.2f}"], PRED_C, y0 - 1.1)
        gf = np.mean([r["fape"] for r in good]) if good else float("nan")
        bf = np.mean([r["fape"] for r in bad]) if bad else float("nan")
        side = VGroup(label(r"chapter 8's twelve folds by descent:", font_size=22, color=GREY_A))
        if good:
            side.add(label(rf"on the fold: \ FAPE ${gf:.2f}$", font_size=24, color=TRUE_C))
        if bad:
            side.add(label(rf"on the mirror: \ FAPE ${bf:.2f}$", font_size=24, color=MIRROR_C))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 1.2, 0])
        tag = note(r"computed", font_size=20).to_corner(DR, buff=0.2)
        fm, dm = f["fape_mirror"], f["drmsd_mirror"]
        with self.voiceover(
            "Here is the difference, measured on our bundle and its reflection. <bookmark mark='a'/> Every distance "
            f"is the same, so the error in distances is {dm:.2f}. <bookmark mark='b'/> Yet FAPE is {fm:.2f}, worse than "
            f"moving every atom a whole ångström at random, which costs {f['fape_noisy']:.2f}. <bookmark mark='c'/> "
            "And chapter eight's folds by gradient descent, which distances alone couldn't sort, separate cleanly: "
            f"those on the true fold score {gf:.2f}, those on the mirror image {bf:.2f}."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), Create(mline), FadeIn(ll), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(r1[:2]))
            vo.wait_until("b")
            self.play(FadeIn(r1[2:]), FadeIn(r2))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recycling(self):
        p = load("pair")
        by = np.array([[p[f"recycle_s{s}"]["by_cycle"][c]["hidden"] for c in range(6)] for s in (0, 1, 2)])
        one = float(np.mean([p[f"triangle_s{s}"]["hidden"] for s in (0, 1, 2)]))
        cyc = np.arange(1, 7)
        lo_, hi_ = float(np.floor(min(by.min(), one) * 2) / 2 - 0.5), float(np.ceil(max(by.max(), one) * 2) / 2 + 0.5)
        g = axes([1, 6], [lo_, hi_], x_length=5.4, y_length=3.6, xlabel=r"passes through the network",
                 ylabel=r"error on unseen pairs (\AA)", xticks=list(cyc), yticks=[lo_, hi_],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", center=[-3.0, -0.3, 0])
        bd = band(g.ax, cyc, by.min(0), by.max(0), PAIR_C, 0.22)
        cv = curve(g.ax, cyc, by.mean(0), PAIR_C, 3.5)
        dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=PAIR_C) for a, b in zip(cyc, by.mean(0))])
        ref = DashedLine(g.ax.c2p(1, one), g.ax.c2p(6, one), color=STRUCT)
        rl = label(r"triangle model trained without recycling", font_size=18, color=STRUCT).next_to(ref, UP, buff=0.06)
        rl.align_to(g.ax, RIGHT)
        train = VGroup(
            label(r"in training: \ a random number of passes, \ $1$ to $4$", font_size=22),
            label(r"gradients through the last pass only", font_size=22),
            label(r"AlphaFold 2: \ $3$ extra passes by default", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 0.9, 0])
        m = by.mean(0)
        best = int(np.argmin(m)) + 1
        gain = m[0] - m.min()
        verdict = (f"A second pass cuts the error from {m[0]:.2f} to {m[1]:.2f} ångströms; the best is at {best} "
                   f"passes, {m.min():.2f}" if m.min() < 0.95 * m[0] else
                   f"In our toy the extra passes change little: from {m[0]:.2f} to {m.min():.2f} ångströms at best")
        vs = ("and with four passes it beats the same network trained without recycling" if m[3] < one else
              f"though even with four passes it doesn't beat the same network trained without recycling, {one:.2f}: "
              "our toy feeds back only its guesses about pairs, with no structure in the loop, while in AlphaFold 2 "
              "recycling did help")
        tag = note(r"computed: \ chapter 9's task, \ three seeds \ (band: \ min--max)", font_size=20)
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "The last trick is recycling: run the whole network again, feeding in its own previous output, so that a "
            "first rough structure can sharpen the reading of the alignment. <bookmark mark='a'/> In training, the "
            "number of passes is random, and the gradient flows only through the last, so every extra pass costs "
            f"no more memory. <bookmark mark='b'/> We added it to chapter nine's triangle model. {verdict}, {vs}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(train))
            vo.wait_until("b")
            self.play(FadeIn(bd), Create(cv), FadeIn(dots), Create(ref), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def database(self):
        items = VGroup(
            history_card(2021, r"July: \ code, paper, \ and a database", r"AlphaFold 2 open-sourced; \ RoseTTAFold "
                         r"(Baek et al.) the same month; \ predicted structures for the human proteome", width=4.4,
                         color=HIST),
            history_card(2022, r"over $200$ million structures", r"nearly every known protein sequence: \ "
                         r"$214{,}684{,}311$ entries \ (EMBL-EBI)", width=4.4, color=HIST),
            history_card(2024, r"the Nobel Prize", r"Hassabis and Jumper, \ with Baker; \ AlphaFold 2 used by "
                         r"millions of researchers", width=4.4, color=HIST),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.9)
        conf = label(r"every prediction comes with its confidence, \ pLDDT: \ where to trust it, \ residue by residue",
                     font_size=24, color=STRUCT).next_to(items, DOWN, buff=0.5)
        lim = label(r"limits: \ one static shape; \ disordered regions; \ complexes, \ DNA, \ drugs bound \ "
                    r"$\to$ \ AlphaFold 3", font_size=24, color=PLAIN).next_to(conf, DOWN, buff=0.35)
        with self.voiceover(
            "In July 2021 DeepMind published AlphaFold 2 with its code; the same month David Baker's group "
            "published RoseTTAFold, a three-track network built on the same insights. <bookmark mark='a'/> With "
            "EMBL's European Bioinformatics Institute, DeepMind released predicted structures, first for the human "
            "proteome and twenty other organisms, then in 2022 for more than two hundred million proteins, nearly "
            "every sequence known. <bookmark mark='b'/> Every prediction carries the network's own confidence, "
            "residue by residue, called pLDDT. <bookmark mark='c'/> Two years later came the Nobel Prize. <bookmark "
            "mark='d'/> But AlphaFold 2 predicts one static shape per chain, and says little about how proteins move, "
            "bind DNA, or hold a drug. That was the next step."
        ) as vo:
            self.play(FadeIn(items[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(items[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(conf))
            vo.wait_until("c")
            self.play(FadeIn(items[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lim))
        self.wait(0.6)
        tk = take_away(r"frames for residues, \ a loss that knows left from right, \ and a network run more than once")
        with self.voiceover(
            "So: residues as rigid frames, moved by attention that can't see how the protein is turned; a loss that "
            "ignores rigid motions but not reflections; and a network that reads its own answer and tries again."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
