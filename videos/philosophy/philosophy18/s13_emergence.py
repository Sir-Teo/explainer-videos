from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Emergence(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Emergence and universality", r"Why do different systems obey the same laws?",
                            lit=(1944, 2002), part=PART)
        with self.voiceover("Chapter twelve. Emergence and universality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ising()
        self.curve()
        self.blocks()
        self.universality()

    def ising(self):
        d = load("rg")
        head = label(r"The Ising model", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"E(s) = -J\sum_{\langle i j\rangle} s_i s_j, \qquad s_i = \pm 1, \qquad "
                     r"P(s) \propto e^{-E(s)/T}", font_size=30, color=THEORY).next_to(head, DOWN, buff=0.3)
        keys = sorted(d, key=lambda k: d[k]["T"])
        imgs = Group()
        for k in keys:
            im = spin_image(d[k]["levels"][1], 3.0)
            imgs.add(im)
        imgs.arrange(RIGHT, buff=0.5).move_to([0, -0.6, 0])
        names = [r"$T = " + f"{d[k]['T']:.2f}" + r"$" for k in keys]
        notes = [r"below $T_c$: \ ordered", r"at $T_c \approx 2.269$: \ critical", r"above $T_c$: \ disordered"]
        caps = VGroup(*[label(n + r": \ " + t, font_size=18, color=GREY_A).next_to(im, DOWN, buff=0.15)
                        for n, t, im in zip(names, notes, imgs)])
        side = label(r"each square a spin, \ up \ (orange) \ or down \ (blue); \ the Reasoner samples by "
                     r"Swendsen--Wang cluster flips", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Some of the deepest emergence in physics happens at phase transitions. <bookmark mark='a'/>The Ising "
            "model is a grid of spins, each up or down. Neighbouring spins prefer to align, and temperature shakes "
            "them. <bookmark mark='b'/>The Reasoner samples the model at three temperatures. At low temperature, "
            "spins align into one great domain: a magnet. <bookmark mark='c'/>At high temperature they are a random "
            "speckle. <bookmark mark='d'/>And at one critical temperature, which Lars Onsager computed exactly in "
            "1944 to be about two point two six nine, there are domains of every size, nested inside one another."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(imgs[0]), FadeIn(caps[0]))
            vo.wait_until("c")
            self.play(FadeIn(imgs[2]), FadeIn(caps[2]))
            vo.wait_until("d")
            self.play(FadeIn(imgs[1]), FadeIn(caps[1]))
        self.clear_scene()

    def curve(self):
        d = load("magnet")
        head = label(r"Onsager's exact answer", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[1.5, 3.1, 0.25], y_range=[0, 1.05, 0.25], x_length=7.4, y_length=4.0,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.0, -0.4, 0])
        ex = series_plot(ax, [m for _, m in d["exact"]], THEORY, xs=[t for t, _ in d["exact"]], width=4)
        dots = VGroup(*[Dot(ax.c2p(t, m), radius=0.06, color=REAL) for t, m in d["sim"]])
        tc = DashedLine(ax.c2p(d["Tc"], 0), ax.c2p(d["Tc"], 1.0), color=GOAL)
        xl = label(r"temperature $T$", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"magnetization $|m|$", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).shift(LEFT * 2.5)
        side = stack([(r"Onsager and Yang \ (1944, \ 1952):", THEORY),
                      (r"$m = \big(1 - \sinh^{-4}(2/T)\big)^{1/8}$", THEORY),
                      (r"simulated, \ $" + f"{d['L']}" + r"\times" + f"{d['L']}" + r"$ spins", REAL),
                      (r"near $T_c$: \ $m \propto (T_c - T)^{\beta}$, \ $\beta = 1/8$", GOAL),
                      (r"above $T_c$ the finite lattice keeps a small residue", GREY_A)], font_size=20,
                     aligned_edge=LEFT, width=5.0).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "The magnetization, the average alignment, measures the order. <bookmark mark='a'/>Onsager, and then "
            "Chen Ning Yang, found it exactly: one minus the inverse fourth power of a hyperbolic sine, raised to "
            "the power one eighth. <bookmark mark='b'/>The Reasoner's simulation of a forty-eight by forty-eight "
            "lattice tracks the exact curve. <bookmark mark='c'/>Near the critical temperature, the order vanishes "
            "as a power law, with exponent beta equal to one eighth. <bookmark mark='d'/>Exponents like this are "
            "the key. They do not depend on the details of the model, and that is what needs explaining."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), Create(ex), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.08), FadeIn(side[2]), FadeIn(side[4]))
            vo.wait_until("c")
            self.play(Create(tc), FadeIn(side[3]))
        self.clear_scene()

    def blocks(self):
        d = load("rg")
        head = label(r"Coarse-graining: \ Kadanoff's block spins", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        keys = sorted(d, key=lambda k: d[k]["T"])
        rows = Group()
        for k in keys:
            ims = Group(*[spin_image(d[k]["levels"][j], 1.45) for j in range(4)]).arrange(RIGHT, buff=0.3)
            rows.add(ims)
        rows.arrange(DOWN, buff=0.35).move_to([-1.4, -0.5, 0])
        rl = VGroup(*[label(r"$T = " + f"{d[k]['T']:.2f}" + r"$", font_size=18, color=GREY_A).next_to(r, LEFT,
                                                                                                 buff=0.25)
                      for k, r in zip(keys, rows)])
        cl = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(rows[0][j], UP, buff=0.12)
                      for j, t in enumerate([r"$243^2$", r"$81^2$", r"$27^2$", r"$9^2$"])])
        corr = VGroup()
        for k, r in zip(keys, rows):
            c = d[k]["corr"]
            corr.add(label(r"$\langle s_i s_j\rangle$: \ " + r" $\to$ ".join(f"{x:.2f}" for x in c), font_size=17,
                           color=OK if d[k]["T"] < 2.2 else (GOAL if d[k]["T"] < 2.3 else BAD)).next_to(r, RIGHT,
                                                                                                          buff=0.3))
        rule = label(r"each $3\times 3$ block becomes one spin, \ by majority vote", font_size=19,
                     color=THEORY).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Leo Kadanoff's idea explains it. <bookmark mark='a'/>Replace each three by three block of spins by a "
            "single spin, chosen by majority vote, and look again. Then do it again. <bookmark mark='b'/>Below the "
            "critical temperature, each coarse-graining makes the picture more ordered: the correlation between "
            "neighbours flows to one. <bookmark mark='c'/>Above it, each step makes the picture more random: the "
            "correlation flows to zero. <bookmark mark='d'/>At the critical temperature, the coarse-grained "
            "picture looks statistically the same as the original, at every scale. The neighbour correlation stays "
            "near point seven. This is a fixed point of the coarse-graining. Kenneth Wilson turned the idea into "
            "the renormalization group, and a Nobel Prize."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(rule))
            vo.wait_until("a")
            for j in range(4):
                self.play(*[FadeIn(r[j]) for r in rows], run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(corr[0]))
            vo.wait_until("c")
            self.play(FadeIn(corr[2]))
            vo.wait_until("d")
            self.play(FadeIn(corr[1]))
        self.clear_scene()

    def universality(self):
        head = label(r"Universality, \ and Batterman's argument", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{system}", r"\text{dimension}", r"\beta"]
        rows = [[MathTex(r"\text{Ising model}", font_size=22), MathTex("2", font_size=22), MathTex(r"1/8", font_size=22)],
                [MathTex(r"\text{layered magnet Rb}_2\text{CoF}_4", font_size=22), MathTex("2", font_size=22),
                 MathTex(r"\approx 0.12", font_size=22)],
                [MathTex(r"\text{Ising model}", font_size=22), MathTex("3", font_size=22),
                 MathTex(r"0.326", font_size=22)],
                [MathTex(r"\text{liquid--gas, \ CO}_2", font_size=22), MathTex("3", font_size=22),
                 MathTex(r"\approx 0.33", font_size=22)],
                [MathTex(r"\text{uniaxial magnet}", font_size=22), MathTex("3", font_size=22),
                 MathTex(r"\approx 0.33", font_size=22)]]
        grid = ValueGrid(hd, rows, col_w=[3.2, 1.4, 1.2], cell_h=0.5, font_size=20).move_to([-3.6, -0.2, 0])
        pairs = [((r"systems with different microphysics share exponents:", THEORY), (r"a universality class", THEORY)),
                 ((r"under coarse-graining all flow to the same fixed point:", OK), (r"the details are irrelevant", OK)),
                 ((r"Batterman \ (2002): \ the explanation \textit{requires} a limit,", REAL),
                  (r"discarding detail, \ not deriving from it", REAL)),
                 ((r"is that emergence, \ or a clever reduction?", GOAL), (r"Butterfield \ (2011): \ both", GOAL))]
        side = VGroup(*[stack([a_, b_], font_size=20, buff=0.1, aligned_edge=LEFT) for a_, b_ in pairs]).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT)
        if side.width > 6.4:
            side.width = 6.4
        side.move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Now the surprise. <bookmark mark='a'/>Systems with completely different microphysics have the same "
            "critical exponents: the two-dimensional Ising model and a layered crystal of rubidium cobalt fluoride; a three-"
            "dimensional magnet, and carbon dioxide at its liquid-gas critical point. They form a universality "
            "class. <bookmark mark='b'/>The renormalization group explains why: under coarse-graining, all of them "
            "flow to the same fixed point, and the microscopic details are irrelevant to where they end up. "
            "<bookmark mark='c'/>Robert Batterman argued that this kind of explanation requires discarding detail, "
            "by taking a limit, rather than deriving the behaviour from the details, and that it is a genuine "
            "case of emergence. <bookmark mark='d'/>Jeremy Butterfield replied that emergence and reduction are "
            "compatible here: the behaviour is novel and robust, and still deducible in the limit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                        lag_ratio=0.2), FadeIn(side[0]))
            for mk, r in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
