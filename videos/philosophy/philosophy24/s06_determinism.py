from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Determinism(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"What determinism says", r"Does the present fix the future?", lit=(1814, 1986),
                            part=PART)
        with self.voiceover("Chapter five. What determinism says."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.definition()
        self.theories()
        self.chance()

    def definition(self):
        hc = history_card(1986, r"John Earman", r"\textit{A Primer on Determinism}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"W, W' \in \text{Mod}(\mathcal{T}),\;\; W|_{t_0} = W'|_{t_0} \;\Longrightarrow\; W = W'",
                    font_size=34, color=LAW).to_edge(DOWN, buff=0.5)
        axl = Axes(x_range=[0, 6, 1], y_range=[-2, 2, 1], x_length=5.2, y_length=3.0, tips=False,
                   axis_config={"color": GREY_C}).move_to([-3.4, -0.4, 0])
        axr = axl.copy().move_to([3.4, -0.4, 0])
        tl = [label(r"time $\to$", font_size=17, color=GREY_A).next_to(a, DOWN, buff=0.1) for a in (axl, axr)]
        sl = [label(r"state", font_size=17, color=GREY_A).next_to(a.y_axis, UP, buff=0.08) for a in (axl, axr)]
        det = VGroup(*[axl.plot(lambda x, c=c: 0.3 * np.sin(0.9 * x) + c, x_range=[0, 6], color=LAW, stroke_width=3)
                       for c in (-1.35, -0.55, 0.25, 1.05)])
        cut_l = DashedLine(axl.c2p(3, -2), axl.c2p(3, 2), color=GOAL)
        base = lambda x: 0.4 * np.sin(0.8 * x)  # noqa: E731
        ind = VGroup(axr.plot(base, x_range=[0, 3.2], color=BAD, stroke_width=4),
                     axr.plot(lambda x: base(x) + 0.2 * (x - 3.2) ** 2, x_range=[3.2, 6], color=BAD, stroke_width=3),
                     axr.plot(lambda x: base(x) - 0.18 * (x - 3.2) ** 2, x_range=[3.2, 6], color=BAD, stroke_width=3))
        cut_r = DashedLine(axr.c2p(2, -2), axr.c2p(2, 2), color=GOAL)
        cap_l = label(r"deterministic: \ histories never meet", font_size=20, color=LAW).next_to(axl, UP, buff=0.3)
        cap_r = label(r"indeterministic: \ two histories agree, \ then part", font_size=20,
                      color=BAD).next_to(axr, UP, buff=0.3)
        with self.voiceover(
            "Laplace's demon needs determinism, so say exactly what determinism is. John Earman's definition, after "
            "Richard Montague, is about theories. <bookmark mark='a'/>Draw each possible history the theory allows, "
            "its models, as a curve of the world's state against time. <bookmark mark='b'/>A theory is "
            "deterministic if two histories that agree at any one time agree at all times: the curves never meet, "
            "so a slice through any moment picks out one history. <bookmark mark='c'/>A theory is indeterministic "
            "if two of its histories agree completely up to some moment, and then part. "
            "<bookmark mark='d'/>In symbols: if W and W prime are models of the theory and they match at time t "
            "nought, they are the same model. Determinism is then a property you can check, theory by theory."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(axl), Create(axr), *[FadeIn(x) for x in tl + sl])
            vo.wait_until("b")
            self.play(FadeIn(cap_l), LaggedStart(*[Create(c) for c in det], lag_ratio=0.2), Create(cut_l))
            vo.wait_until("c")
            self.play(FadeIn(cap_r), Create(ind[0]), Create(cut_r))
            self.play(Create(ind[1]), Create(ind[2]))
            vo.wait_until("d")
            self.play(Write(f))
        self.clear_scene()

    def theories(self):
        head = label(r"Which theories are deterministic?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = lambda s, c=WHITE: label(s, font_size=19, color=c)  # noqa: E731
        hd = [T(r"theory", CONN), T(r"verdict", CONN), T(r"why", CONN)]
        rows = [[T(r"Newtonian particles", LAW), mark(False), T(r"`space invaders' from infinity; \ Norton's dome "
                                                               r"(chapter 6)")],
                [T(r"Maxwell's fields", LAW), mark(True), T(r"well-posed equations, \ with light-speed limits")],
                [T(r"general relativity", TIME), mark(False), T(r"spacetimes with horizons; \ the hole argument "
                                                              r"(Part 25)")],
                [T(r"quantum: \ Schrödinger evolution", ABS), mark(True), T(r"a linear equation, \ unique "
                                                                         r"solutions")],
                [T(r"quantum: \ with collapse", ABS), mark(False), T(r"measurement outcomes are chancy \ (Part 26)")]]
        grid = ValueGrid(hd, rows, col_w=[3.8, 1.4, 6.8], cell_h=0.62, font_size=20).move_to([0, 0.0, 0])
        note = label(r"surprise: \ determinism is not the default even in classical physics", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Check it, theory by theory, and the answers surprise. <bookmark mark='a'/>Newtonian mechanics of "
            "point particles is not deterministic. Particles can be accelerated to infinity in finite time, as "
            "Zhihong Xia proved for five bodies in 1992; run the film backwards and particles arrive from infinity "
            "without warning, Earman's space invaders. And the next chapter builds an even simpler failure. "
            "<bookmark mark='b'/>Maxwell's equations for the electromagnetic field are deterministic. "
            "<bookmark mark='c'/>General relativity can fail, with spacetimes whose futures are not fixed by any "
            "slice, and Part 25's hole argument. <bookmark mark='d'/>Quantum theory's Schrödinger equation is "
            "deterministic, <bookmark mark='e'/>but if measurement collapses the wave function, outcomes are "
            "chancy, which is Part 26's puzzle. <bookmark mark='f'/>So determinism is not the default, even in "
            "classical physics. It is a substantive claim about a theory, and often false."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.clear_scene()

    def chance(self):
        head = label(r"Chance in a deterministic world?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Lewis", r"no: \ if the past and the laws fix the future, \ every chance is 0 or 1", BAD),
            (r"Loewer \ (2001)", r"yes: \ the Mentaculus's probability over initial states gives real chances, \ "
                                 r"for coins and gases", OK),
            (r"a real coin", r"Diaconis, \ Holmes and Montgomery \ (2007): \ a coin lands the way it started about "
                             r"51\% of the time", CHANCE),
            (r"350\,757 flips", r"Bartoš et al. \ (2023): \ 50.8\% landed on the side they started", CHANCE),
            (r"next", r"where do such chances come from? \ sensitivity, \ chapter 7", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.48, width=9.0, x_text=-3.0, label_size=22, text_size=21)
        with self.voiceover(
            "Can there be chance in a deterministic world? <bookmark mark='a'/>Lewis said no. If the past and the "
            "laws fix the future, the chance of every future event is zero or one. A coin toss in a Newtonian world "
            "has no chance of one half. <bookmark mark='b'/>Barry Loewer said yes. The Mentaculus puts a "
            "probability over the initial states of the universe, and that probability, part of the best system, "
            "gives genuine chances to coin tosses and gas molecules even when the dynamics is deterministic. "
            "<bookmark mark='c'/>And real coins are interesting. Persi Diaconis, Susan Holmes and Richard "
            "Montgomery modelled the physics of a toss in 2007 and predicted a small bias: a coin lands the way it "
            "started about fifty-one per cent of the time. <bookmark mark='d'/>In 2023 František Bartoš and "
            "colleagues flipped coins three hundred and fifty thousand times, and found fifty point eight per cent. "
            "<bookmark mark='e'/>So the chance of heads depends on physics. Where do such chances come from, if the "
            "dynamics is deterministic? Chapter seven answers: from sensitivity."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
