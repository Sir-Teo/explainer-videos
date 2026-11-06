from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Kac(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The Kac ring", r"How can reversible laws look irreversible?", lit=(1959,),
                            part=PART)
        with self.voiceover("Chapter ten. The Kac ring."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ring()
        self.decay()
        self.reverse()
        self.both_ways()
        self.wall_brick()

    def ring(self):
        d = load("kacsmall")
        N = d["N"]
        hc = history_card(1959, r"Mark Kac", r"\textit{Probability and Related Topics in Physical Sciences}",
                          width=6.8, color=HIST).to_corner(UL, buff=0.3)
        c = np.array([-3.2, -0.6, 0])
        R = 2.2
        ang = [PI / 2 - 2 * PI * i / N for i in range(N)]
        site = [c + R * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
        circle = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(c)
        marks = VGroup()
        for i in d["marked"]:
            a = ang[i] - PI / N
            p_in = c + (R - 0.25) * np.array([np.cos(a), np.sin(a), 0])
            p_out = c + (R + 0.25) * np.array([np.cos(a), np.sin(a), 0])
            marks.add(Line(p_in, p_out, color=BAD, stroke_width=5))

        def balls(state):
            return VGroup(*[Dot(site[i], radius=0.13, color=WHITE if v > 0 else GREY_D,
                                stroke_color=GREY_B, stroke_width=1.5) for i, v in enumerate(state)])

        cur = balls(d["states"][0])
        k = ValueTracker(0)
        count = always_redraw(lambda: label(rf"step {int(k.get_value())}: \ "
                                            rf"{d['whites'][int(k.get_value())]} white of {N}", font_size=22,
                                            color=CHANCE).move_to(c + DOWN * (R + 0.6)))
        rules = stack([(r"36 sites; \ a ball on each, \ white or black", WHITE),
                       (r"6 marked edges, \ fixed", BAD),
                       (r"each tick: \ every ball moves one site clockwise, \ and flips colour if it crosses a mark",
                        LAW),
                       (r"deterministic, \ reversible \ (run it anticlockwise), \ and it returns to the start in "
                        r"$2N$ ticks", ABS)], font_size=20, aligned_edge=LEFT, width=5.0, buff=0.3).move_to(
            [3.9, -0.3, 0])
        with self.voiceover(
            "In 1959 the mathematician Mark Kac built a toy universe that shows the whole puzzle in miniature. "
            "<bookmark mark='a'/>A ring of sites, here thirty-six, with a ball on each, white or black. "
            "<bookmark mark='b'/>Some of the edges between sites carry a mark, and the marks never move. "
            "<bookmark mark='c'/>At each tick of the clock every ball moves one site clockwise, and if it crosses "
            "a marked edge, it changes colour. Start with every ball white, and run it. "
            "<bookmark mark='d'/>The rule is deterministic. It is reversible: move the balls anticlockwise and "
            "every step is undone. And it is recurrent: after twice N ticks every ball has crossed every mark "
            "twice, so everything is back where it started. Every objection of the last chapter applies to this "
            "toy, and yet."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(circle), FadeIn(cur), FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.2), FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]), FadeIn(count))
            for step in range(1, 13):
                nxt = balls(d["states"][step])
                self.play(Transform(cur, nxt), k.animate.set_value(step), run_time=0.45)
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
        count.clear_updaters()
        self.clear_scene()

    def decay(self):
        d = load("kac")
        head = label(r"Two hundred sites", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 450, 50], y_range=[-1, 1, 0.5], x_length=9.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-1.4, -0.5, 0])
        xl = label(r"ticks", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.3).shift(RIGHT * 4.2)
        yl = label(r"$\delta = (\text{white} - \text{black}) / N$", font_size=18, color=GREY_A).next_to(
            ax.y_axis, UP, buff=0.1)
        curve = series_plot(ax, d["delta"], CHANCE, width=2.2)
        theory = series_plot(ax, d["theory"][:120], GOAL, width=3)
        mu = d["mu"]
        f = MathTex(rf"\delta(t) \approx (1 - 2\mu)^t,\quad \mu = {mu:.3f}", font_size=30, color=GOAL).move_to(
            [3.0, 2.55, 0])
        n_ = d["N"]
        dot_n = Dot(ax.c2p(n_, d["delta"][n_]), radius=0.08, color=BAD)
        dot_2n = Dot(ax.c2p(2 * n_, d["delta"][2 * n_]), radius=0.08, color=OK)
        ln = label(rf"$t = N$: \ {d['markers']} marks, \ an odd number: \ all black", font_size=18,
                   color=BAD).next_to(dot_n, DOWN, buff=0.15)
        l2n = label(r"$t = 2N$: \ all white again", font_size=18, color=OK).next_to(dot_2n, LEFT, buff=0.2)
        assert d["returns"] and d["half_way"] == -1.0 and d["markers"] % 2 == 1
        with self.voiceover(
            "Now a ring of two hundred sites, with marks on about one edge in seven, chosen at random. "
            "<bookmark mark='a'/>Measure the colour imbalance: white minus black, over the number of balls. It "
            "starts at one. <bookmark mark='b'/>It decays toward zero, and then wanders near zero, as if the ring "
            "had reached equilibrium. <bookmark mark='c'/>Kac showed that if the marks are uncorrelated with the "
            "colours, his version of Boltzmann's assumption, the imbalance falls like one minus twice the fraction "
            "of marked edges, to the power t: the gold curve. <bookmark mark='d'/>But the ring is recurrent. At "
            "tick two hundred every ball has crossed every mark exactly once. There are twenty-seven marks, an odd "
            "number, so every ball is black: perfect order, in a single tick. <bookmark mark='e'/>At tick four "
            "hundred, every ball is white again. Equilibrium is what the ring does almost all the time, not what it "
            "does forever."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(series_plot(ax, d["delta"][:3], CHANCE, width=2.2)))
            vo.wait_until("b")
            self.play(Create(curve), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(Write(f), Create(theory))
            vo.wait_until("d")
            self.play(FadeIn(dot_n), FadeIn(ln))
            vo.wait_until("e")
            self.play(FadeIn(dot_2n), FadeIn(l2n))
        self.clear_scene()

    def reverse(self):
        d = load("kac")
        head = label(r"Loschmidt's reversal, \ on the ring", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        R = d["reverse_at"]
        ax = Axes(x_range=[0, 2 * R, 20], y_range=[-0.4, 1, 0.2], x_length=7.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-2.4, -0.5, 0])
        fwd = series_plot(ax, d["delta"][:R + 1], CHANCE, width=3)
        back = series_plot(ax, d["reversed"], TIME, xs=list(range(R, 2 * R + 1)), width=3)
        line = DashedLine(ax.c2p(R, -0.4), ax.c2p(R, 1), color=GOAL)
        side = stack([(rf"run {R} ticks forward: \ the imbalance decays", CHANCE),
                      (r"then move every ball anticlockwise", GOAL),
                      (rf"after {R} more ticks: \ every ball white again", TIME),
                      (r"the decay is not built into the rule: \ it depends on the starting state", BAD)],
                     font_size=20, aligned_edge=LEFT, width=4.6).move_to([4.4, -0.4, 0])
        assert d["reverse_returns"]
        with self.voiceover(
            "Loschmidt's objection works on the ring too. <bookmark mark='a'/>Run sixty ticks forward: the "
            "imbalance decays, as before. <bookmark mark='b'/>Now reverse the motion: every ball steps "
            "anticlockwise. <bookmark mark='c'/>The imbalance climbs back, and after sixty more ticks every ball is "
            "white. <bookmark mark='d'/>So the decay is not written into the rule. It depends on the state: on the "
            "colours being uncorrelated with the marks they are about to cross. After sixty forward ticks the "
            "colours are correlated with the marks behind them, and reversing the motion turns those into the marks "
            "ahead."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(fwd), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(back), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def both_ways(self):
        d = load("both")
        head = label(r"A typical present, \ run both ways", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-30, 30, 10], y_range=[0.6, 1.02, 0.1], x_length=8.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-1.8, -0.5, 0])
        xl = label(r"ticks from now", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"entropy (bits per ball)", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        t, e = d["t"], d["entropy"]
        mid = len(t) // 2
        past = series_plot(ax, e[:mid + 1], TIME, xs=t[:mid + 1], width=3.5)
        fut = series_plot(ax, e[mid:], ENT, xs=t[mid:], width=3.5)
        now = Dot(ax.c2p(0, d["now"]), radius=0.09, color=GOAL)
        nl = label(r"now: \ 80\% white", font_size=18, color=GOAL).next_to(now, RIGHT, buff=0.2)
        side = stack([(rf"{d['N']:,} sites; \ a random state with 80\% white; \ nothing special about its past"
                       .replace(",", r"\,"), WHITE),
                      (r"toward the future: \ entropy rises", ENT),
                      (r"toward the past: \ it rises too", TIME),
                      (r"without a special beginning, \ the most probable past has \textit{higher} entropy", BAD)],
                     font_size=20, aligned_edge=LEFT, width=4.2).move_to([4.7, -0.4, 0])
        assert d["past_end"] > d["now"] + 0.2 and d["future_end"] > d["now"] + 0.2
        with self.voiceover(
            "Here is the deepest version of the puzzle. <bookmark mark='a'/>Take a big ring, two thousand sites, "
            "and a state that is eighty per cent white, chosen at random among such states, with nothing special "
            "about how it came to be. Call this moment now. <bookmark mark='b'/>Run the ring forward: entropy "
            "rises. <bookmark mark='c'/>Run it backward: entropy rises too. <bookmark mark='d'/>The typical state "
            "of low entropy is a dip, with higher entropy on both sides. So if all we assume is the time-symmetric "
            "rule and a typical present, then the most probable past is one of higher entropy. David Albert's "
            "example: by this reasoning, a half-melted ice cube in a glass of water was most probably more melted a "
            "minute ago, not less, and assembled itself by a fluctuation. Our memories and records would most "
            "probably be flukes too."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(now), FadeIn(nl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fut), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(past.reverse_points()), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=24, current=24).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(24, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-fourth brick in the Wall, Loschmidt's. <bookmark mark='a'/>The dream was to get the "
            "arrow of time out of the laws. Reversibility and recurrence block it: time-symmetric dynamics, applied "
            "to a typical state, gives entropy rising toward the past as well as the future. "
            "<bookmark mark='b'/>The way through is not in the dynamics at all. It is in the boundary: a special "
            "beginning. The next chapter takes it."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[24], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
