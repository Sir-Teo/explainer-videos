from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Signals(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Conventions from nothing", r"Can meaning emerge without anyone deciding it?",
                            lit=(1969, 2010), part=PART)
        with self.voiceover("Chapter eleven. Conventions from nothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lewis()
        self.learning()
        self.three()
        self.info()
        self.meaning()

    def lewis(self):
        hc = history_card(1969, r"David Lewis", r"\textit{Convention}", width=4.6, color=HIST).to_corner(UL, buff=0.3)
        states = VGroup(*[label(t, font_size=22, color=WORLD) for t in (r"state 1", r"state 2")]).arrange(DOWN, buff=1.2)
        sigs = VGroup(*[label(t, font_size=22, color=WORD) for t in (r"signal A", r"signal B")]).arrange(DOWN, buff=1.2)
        acts = VGroup(*[label(t, font_size=22, color=HEAR) for t in (r"act 1", r"act 2")]).arrange(DOWN, buff=1.2)
        cols = VGroup(states, sigs, acts).arrange(RIGHT, buff=2.4).move_to([0, -0.4, 0])
        tags = VGroup(label(r"sender sees", font_size=18, color=GREY_A).next_to(states, UP, buff=0.3),
                      label(r"sends", font_size=18, color=GREY_A).next_to(sigs, UP, buff=0.3),
                      label(r"receiver does", font_size=18, color=GREY_A).next_to(acts, UP, buff=0.3))
        arr1 = VGroup(Arrow(states[0].get_right(), sigs[0].get_left(), color=USE, buff=0.15),
                      Arrow(states[1].get_right(), sigs[1].get_left(), color=USE, buff=0.15))
        arr2 = VGroup(Arrow(sigs[0].get_right(), acts[0].get_left(), color=HEAR, buff=0.15),
                      Arrow(sigs[1].get_right(), acts[1].get_left(), color=HEAR, buff=0.15))
        foot = label(r"both are rewarded when the act fits the state: \ a signalling system is an equilibrium", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Where do conventions of meaning come from, if not from a prior agreement, which would itself need "
            "language? <bookmark mark='a'/>David Lewis, in 1969, modelled the simplest case as a game. A sender sees "
            "which of two states the world is in, and sends one of two signals. A receiver sees only the signal, and "
            "acts. <bookmark mark='b'/>Both are rewarded when the act fits the state. <bookmark mark='c'/>A signalling "
            "system, a pairing of states with signals and signals with acts, is an equilibrium: neither player can "
            "do better by changing alone. Which pairing is used is arbitrary: a convention."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(cols), FadeIn(tags))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr1], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr2], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def learning(self):
        d = load("sig2")
        head = label(r"Learned by reinforcement", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6000, 1500], y_range=[0.4, 1.0, 0.1], x_length=6.6, y_length=3.8,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-2.6, -0.4, 0])
        xl = label(r"rounds played", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"chance of success", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        curves = VGroup()
        for c, col in zip(d["curves"], (WORD, USE, HEAR, WORLD, RULE_C, TRUTH)):
            xs = [100 * i for i in range(len(c))]
            curves.add(VMobject(stroke_color=col, stroke_width=2.5).set_points_as_corners(
                [ax.c2p(x, max(0.4, y)) for x, y in zip(xs, c)]))
        assert d["runs"] == 200 and d["hist"][-1] == 196 and d["perfect"] == 172
        side = stack([(r"Roth--Erev: \ an urn of balls for each state and each signal; \ a success adds a ball of the "
                       r"colour just used", WHITE),
                      (r"six runs shown; \ all climb toward perfect signalling", WORD),
                      (r"of 200 runs of 6000 rounds: \ 196 end above 90\% success, \ 172 above 99\%", OK),
                      (r"no one chose the convention; \ which signal means which state differs from run to run", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.6, buff=0.28).move_to([4.5, -0.3, 0])
        with self.voiceover(
            "Brian Skyrms showed that such conventions can emerge from the simplest learning. "
            "<bookmark mark='a'/>Give the sender an urn for each state, holding one ball for each signal, and the "
            "receiver an urn for each signal, holding one ball for each act. Each round, draw a ball to choose. When "
            "the act fits the state, add a ball of the colours just used. This is Roth–Erev reinforcement. "
            "<bookmark mark='b'/>The Reasoner plays the game. Here are six runs: the chance of success climbs from a "
            "half toward one. <bookmark mark='c'/>Of two hundred runs of six thousand rounds, a hundred and ninety-six "
            "end above ninety percent success, and a hundred and seventy-two above ninety-nine. "
            "<bookmark mark='d'/>No one chose the convention, and which signal comes to mean which state differs from "
            "run to run. Meaning, of a minimal kind, out of nothing but reward."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def three(self):
        d2, d3 = load("sig2"), load("sig3")
        head = label(r"With three states, \ some runs get stuck", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 200, 50], x_length=7.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True}
                  ).move_to([-2.2, -0.4, 0])
        labels_x = VGroup(*[MathTex(f"{k / 10:.1f}", font_size=16, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                            for k in range(0, 11, 2)])
        xl = label(r"final chance of success", font_size=17, color=GREY_A).next_to(labels_x, DOWN, buff=0.12)
        yl = label(r"runs", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(ax, LEFT)
        bars = VGroup()
        for k, (a, b) in enumerate(zip(d2["hist"], d3["hist"])):
            for val, col, off in ((a, WORD, 0.27), (b, USE, 0.73)):
                if val == 0:
                    continue
                h = ax.c2p(0, val)[1] - ax.c2p(0, 0)[1]
                bars.add(Rectangle(width=0.32 * ax.x_length / 10, height=h, stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to(ax.c2p(k + off, 0) + UP * h / 2))
        assert d3["hist"][6] == 26 and d3["hist"][-1] == 169
        side = stack([(r"blue: \ 2 states; \ orange: \ 3 states", WHITE),
                      (r"3 states: \ 169 of 200 runs end above 90\%", OK),
                      (r"26 of 200 end near $\tfrac23$: \ partial pooling, \ two states sharing one signal", BAD),
                      (r"the learners settle into a suboptimal convention, \ and stay", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=4.4, buff=0.28).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "With more states, learning can fail. <bookmark mark='a'/>Here are the final success rates of all two "
            "hundred runs, for two states in blue and three states in orange. <bookmark mark='b'/>With three states, a "
            "hundred and sixty-nine runs still end above ninety percent. <bookmark mark='c'/>But twenty-six end near "
            "two thirds. In these runs two states have come to share one signal, and the receiver can only guess "
            "between them: a partial pooling equilibrium. <bookmark mark='d'/>The learners have settled into a worse "
            "convention than they could have had, and reinforcement will not get them out. Skyrms's book Signals, of "
            "2010, studies when such traps occur, and what, like forgetting or invention, lets learners escape them."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(labels_x), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(side[0]), run_time=2)
            for mk, r in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def info(self):
        d2, d3 = load("sig2"), load("sig3")
        head = label(r"Information, \ in bits", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d2["max_info"] == 1.0 and abs(d2["info_top"] - 0.975) < 1e-3
        assert abs(d3["max_info"] - 1.585) < 1e-3 and abs(d3["info_top"] - 1.5179) < 1e-3
        assert d3["n_pooled"] == 27 and abs(d3["info_pooled"] - 0.899) < 1e-3
        eq = MathTex(r"I(\text{state};\, \text{signal}) \;=\; \sum_{s,\,\sigma} p(s, \sigma)\, "
                     r"\log_2 \frac{p(s, \sigma)}{p(s)\, p(\sigma)}", font_size=32, color=WORD).move_to([0, 2.2, 0])
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.6, 0.5], x_length=6.6, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}}
                  ).move_to([-2.4, -0.9, 0])
        yl = label(r"bits", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        data = [(r"2 states: \ learned", d2["info_top"], d2["max_info"], WORD),
                (r"3 states: \ learned", d3["info_top"], d3["max_info"], USE),
                (r"3 states: \ pooled", d3["info_pooled"], d3["max_info"], BAD)]
        bars, caps, tags, vals = VGroup(), VGroup(), VGroup(), VGroup()
        for i, (name, v, mx, col) in enumerate(data):
            x = i + 0.5
            h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
            b = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                ax.c2p(x, 0) + UP * h / 2)
            bars.add(b)
            caps.add(DashedLine(ax.c2p(x - 0.32, mx), ax.c2p(x + 0.32, mx), color=GREY_A, stroke_width=2))
            tags.add(label(name, font_size=16, color=col).next_to(ax.c2p(x, 0), DOWN, buff=0.15))
            vals.add(MathTex(f"{v + 1e-9:.2f}", font_size=20, color=WHITE).move_to(b.get_top() + DOWN * 0.22))
        side = stack([(r"dashed: \ the most a signal can carry, \ $\log_2$ of the number of states", GREY_A),
                      (r"2 states: \ 0.98 of 1 bit; \ 3 states: \ 1.52 of 1.58", OK),
                      (r"the 27 pooled runs: \ 0.90 bits; \ two states share a signal", BAD),
                      (r"information is a property of the whole convention, \ not of the signal alone", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=4.6, buff=0.26).move_to([4.5, -0.7, 0])
        with self.voiceover(
            "How much do the learned signals say? <bookmark mark='a'/>Measure it in bits: the mutual information "
            "between the state and the signal, which is how much seeing the signal reduces uncertainty about the "
            "state. <bookmark mark='b'/>A signal can carry at most the logarithm of the number of states: one bit "
            "for two, about one point five eight for three. <bookmark mark='c'/>The successful runs come close: "
            "point nine eight bits of one, and one point five two of one point five eight. "
            "<bookmark mark='d'/>The twenty-seven pooled runs carry about point nine: two states share a signal, and "
            "what would distinguish them is lost. <bookmark mark='e'/>None of this is in a signal taken alone. The "
            "same mark would carry nothing if the sender used it at random. Information, like meaning on Lewis's "
            "view, belongs to the convention."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), FadeIn(tags), Create(caps), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]),
                      FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def meaning(self):
        head = label(r"What signals mean", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Lewis", r"a convention is a regularity everyone conforms to because everyone expects everyone else to",
             HIST),
            (r"Skyrms", r"the information in a signal: \ how much it moves the probabilities of the states", WORD),
            (r"content", r"a signal's content: \ the states it makes more likely, \ and the acts it makes fitting", USE),
            (r"the gap", r"bees and vervet monkeys signal like this; \ do they mean? \ the questions of chapter 13 begin "
                         r"here", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "What do such signals mean? <bookmark mark='a'/>For Lewis, a convention is a regularity that everyone "
            "conforms to because everyone expects everyone else to, and prefers to conform if the others do. "
            "<bookmark mark='b'/>Skyrms measures the information in a signal by how much it shifts the probabilities "
            "of the states. <bookmark mark='c'/>And he gives it a content: the states it makes more likely, and the "
            "acts it makes fitting. <bookmark mark='d'/>Bees and vervet monkeys use signals like these. Whether they "
            "mean anything in the full sense, and what more would be needed, is the question chapter thirteen asks "
            "about machines."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
