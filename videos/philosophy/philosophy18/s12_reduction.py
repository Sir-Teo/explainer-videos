from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Reduction(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Reduction", r"Is chemistry just physics, \ and psychology just chemistry?",
                            lit=(1961, 1967), part=PART)
        with self.voiceover("Chapter eleven. Reduction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.nagel()
        self.gas()
        self.multiple()
        self.peg()

    def nagel(self):
        hc = history_card(1961, r"Ernest Nagel", r"\textit{The Structure of Science}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        top = RoundedRectangle(width=4.2, height=0.8, corner_radius=0.12, color=REAL).move_to([-3.2, 0.8, 0])
        bot = RoundedRectangle(width=4.2, height=0.8, corner_radius=0.12, color=THEORY).move_to([-3.2, -1.6, 0])
        tl = label(r"thermodynamics: \ $T$, \ $p$, \ entropy", font_size=19, color=REAL).move_to(top)
        bl = label(r"statistical mechanics: \ molecules", font_size=19, color=THEORY).move_to(bot)
        arrow = Arrow(bot.get_top(), top.get_bottom(), buff=0.1, color=GOAL, stroke_width=4)
        bridge = MathTex(r"T = \frac{2}{3k}\Big\langle \tfrac12 m v^2 \Big\rangle", font_size=30, color=GOAL).next_to(
            arrow, RIGHT, buff=0.3)
        bl2 = label(r"bridge law", font_size=17, color=GOAL).next_to(bridge, DOWN, buff=0.1)
        side = stack([(r"a theory reduces to another when its laws can be derived from it", WHITE),
                      (r"plus bridge laws linking their vocabularies", GOAL),
                      (r"derivability alone is not enough: \ the bridge laws need justifying", GREY_A),
                      (r"and usually what is derived is an approximation \ (Schaffner, \ 1967)", BAD)],
                     font_size=20, aligned_edge=LEFT, width=5.6).move_to([3.6, -0.4, 0])
        with self.voiceover(
            "What is it for one science to reduce to another? <bookmark mark='a'/>Ernest Nagel's answer: a theory "
            "reduces to another when its laws can be derived from the other's. <bookmark mark='b'/>Since the two "
            "use different vocabularies, the derivation needs bridge laws. The textbook case links temperature in "
            "thermodynamics to the mean kinetic energy of molecules. <bookmark mark='c'/>But a bridge law is itself "
            "an empirical discovery that needs justifying. <bookmark mark='d'/>And what is derived is usually only "
            "an approximation to the old law, as Kenneth Schaffner pointed out: reduction corrects as it explains."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(top), FadeIn(tl), FadeIn(bot), FadeIn(bl))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(bridge), FadeIn(bl2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gas(self):
        d = load("kinetic")
        head = label(r"The bridge law, \ run on simulated molecules", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ymax = max(d["hist"]) * 1.1
        ax = Axes(x_range=[0, 1400, 200], y_range=[0, ymax, ymax / 4], x_length=7.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18},
                  x_axis_config={"include_numbers": True}, y_axis_config={"include_ticks": False}).move_to(
            [-2.4, -0.2, 0])
        bars = bar_hist(ax, d["hist"], d["edges"], THEORY)
        xl = label(r"speed \ (m/s)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        rms = DashedLine(ax.c2p(d["rms"], 0), ax.c2p(d["rms"], ymax * 0.95), color=GOAL)
        rl = label(r"rms " + f"{d['rms']:.0f}" + r" m/s", font_size=17, color=GOAL).next_to(rms, UP, buff=0.05)
        side = stack([(f"{d['n']:,}".replace(",", "{,}") + r" nitrogen molecules, \ velocities drawn at " +
                       f"{d['T']:.0f}" + r" K", WHITE),
                      (r"the Maxwell--Boltzmann distribution of speeds", THEORY),
                      (r"apply the bridge law to the sample: \ $T = " + f"{d['T_recovered']:.1f}" + r"$ K", GOAL),
                      (r"temperature \textit{is} mean kinetic energy, \ in gases", OK),
                      (r"in solids, \ plasmas and spin systems, \ temperature is realized differently", BAD)],
                     font_size=20, aligned_edge=LEFT, width=5.0).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "The Reasoner can run the bridge law in reverse. <bookmark mark='a'/>It draws the velocities of a "
            "hundred thousand nitrogen molecules at three hundred kelvin. <bookmark mark='b'/>Their speeds follow "
            "the Maxwell–Boltzmann distribution, with a root-mean-square speed of about five hundred and eighteen "
            "metres per second. <bookmark mark='c'/>Apply the bridge law to the sample's average kinetic energy, "
            "and out comes the temperature: three hundred and one kelvin, within sampling error. "
            "<bookmark mark='d'/>In a gas, temperature is mean molecular kinetic energy. "
            "<bookmark mark='e'/>But in solids, plasmas and magnetic spin systems, temperature is realized in other "
            "ways. Even this showcase reduction is local."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(side[1]),
                      run_time=2)
            self.play(Create(rms), FadeIn(rl))
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def multiple(self):
        head = label(r"Multiple realizability", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        pain = RoundedRectangle(width=2.0, height=0.7, corner_radius=0.12, color=REAL).move_to([-3.9, 1.0, 0])
        pl = label(r"pain", font_size=20, color=REAL).move_to(pain)
        reals = [r"C-fibres \ (human)", r"octopus ganglia", r"silicon?"]
        rb = VGroup()
        for i, t in enumerate(reals):
            b = RoundedRectangle(width=1.95, height=0.6, corner_radius=0.12, color=THEORY)
            tl_ = label(t, font_size=15, color=THEORY)
            if tl_.width > 1.8:
                tl_.width = 1.8
            rb.add(VGroup(b, tl_.move_to(b)))
        rb.arrange(RIGHT, buff=0.2).move_to([-3.9, -0.8, 0])
        lines = VGroup(*[Line(pain.get_bottom(), r.get_top(), color=GREY_B, stroke_width=2) for r in rb])
        rows = [
            (r"Putnam \ (1967)", r"one mental kind, \ many physical realizers: \ no single bridge law", REAL),
            (r"Fodor \ (1974)", r"`special sciences': \ economics has laws about money, \ which can be shells, \ "
                                r"coins or bits", THEORY),
            (r"the reply", r"local reductions, \ species by species \ (Kim; \ Lewis)", ANTI),
            (r"the payoff", r"autonomy of the higher sciences, \ and Part 17's question of which level causes", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=4.4, x_label=-0.4, x_text=2.5, label_size=19, text_size=19)
        with self.voiceover(
            "Reduction faces a deeper obstacle in the special sciences. <bookmark mark='a'/>Hilary Putnam argued "
            "in 1967 that a mental kind like pain can be realized in very different physical systems: human C-"
            "fibres, the ganglia of an octopus, perhaps silicon. Then there is no single physical kind for a bridge "
            "law to name. <bookmark mark='b'/>Jerry Fodor generalized: economics has laws about money, but money can "
            "be shells, coins, or bits in a database, with nothing physical in common. "
            "<bookmark mark='c'/>Reductionists, including Kim and David Lewis, replied with local reductions: pain-"
            "in-humans to one state, pain-in-octopuses to another. <bookmark mark='d'/>The question left over is "
            "whether higher-level sciences are autonomous, and whether their kinds cause anything, which was Part "
            "seventeen's exclusion problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pain), FadeIn(pl), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(r) for r in rb], lag_ratio=0.2), FadeIn(g[0]))
            for mk, r in zip("bcd", g[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def peg(self):
        head = label(r"Putnam's peg \ (1975)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hole = VGroup(Square(side_length=2.6, color=GREY_B, fill_opacity=0.2),
                      Circle(radius=0.9, color=GREY_B, fill_color=BLACK, fill_opacity=1)).move_to([-5.0, 0.6, 0])
        sq = Square(side_length=1.8, color=REAL, fill_opacity=0.5).move_to([-2.3, 0.6, 0])
        diag = Line(sq.get_corner(DL), sq.get_corner(UR), color=GOAL, stroke_width=3)
        peg = VGroup(sq, diag)
        ann = VGroup(label(r"hole: \ diameter 1", font_size=18, color=GREY_A).next_to(hole, DOWN, buff=0.2),
                     label(r"peg: \ side 1, \ diagonal $\sqrt2 \approx 1.414$", font_size=18,
                           color=REAL).next_to(peg, DOWN, buff=0.2))
        rows = stack([(r"why won't the peg go through? \ because its diagonal exceeds the hole's diameter", OK),
                      (r"a derivation from the position of every particle would also entail it", THEORY),
                      (r"but it would bury the explanation in irrelevant detail", BAD),
                      (r"higher-level explanations can be better, \ not just shorter: \ Chapter 12's universality, "
                       r"\ Part 17's proportionality", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=6.2).move_to([3.4, 0.2, 0])
        with self.voiceover(
            "Putnam gave an example that cuts against the idea that the lowest level always explains best. "
            "<bookmark mark='a'/>A board has a round hole one inch across. A square peg has sides of one inch. Why "
            "won't the peg go through? Because its diagonal, the square root of two inches, exceeds the hole's "
            "diameter. <bookmark mark='b'/>A derivation from the positions of every particle in board and peg "
            "would also entail that it won't go through. <bookmark mark='c'/>But it would bury the explanation in "
            "detail that does not matter: any rigid peg of that shape, made of anything, would fail. "
            "<bookmark mark='d'/>Higher-level explanations can be better, not just shorter, which is the lesson of "
            "universality in chapter twelve and of proportionality in Part 17."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hole), FadeIn(sq), FadeIn(ann[0]))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(ann[1]), FadeIn(rows[0]))
            self.play(peg.animate.move_to(hole.get_center() + RIGHT * 0.3), run_time=1)
            self.play(peg.animate.move_to([-2.3, 0.6, 0]), run_time=0.6)
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
