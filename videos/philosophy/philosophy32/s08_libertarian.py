from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Libertarian(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Libertarianism", r"Can an undetermined choice be up to the chooser?",
                            lit=(1996,), part=PART)
        with self.voiceover("Chapter seven. Libertarianism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.views()
        self.kane()
        self.torn()
        self.rollback()

    def views(self):
        head = label(r"Two libertarian pictures", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"agent causation", r"Reid; \ Chisholm \ (1964): \ the agent, \ not an event in the agent, \ causes "
                                     r"the decision: \ `a prime mover unmoved'", WILL),
                (r"its defenders", r"O'Connor \ (2000), \ Clarke: \ a distinct kind of causation, \ compatible with "
                                   r"physics if the laws leave room", SELF),
                (r"event-causal", r"Kane \ (1996): \ ordinary causation, \ but some decisions are undetermined events "
                                  r"in the brain", CHANCE),
                (r"the shared demand", r"some choice must have been genuinely open, \ and settled by us", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Libertarians hold that freedom requires indeterminism, and that we are free. There are two main "
            "pictures. <bookmark mark='a'/>On agent causation, from Thomas Reid to Roderick Chisholm, the agent "
            "herself, not any event within her, causes her decision. Each of us, Chisholm wrote, is a prime mover "
            "unmoved. <bookmark mark='b'/>Timothy O'Connor and Randolph Clarke defend a version consistent with "
            "physics, provided its laws leave room. <bookmark mark='c'/>Robert Kane's event-causal view needs no new "
            "kind of cause: some decisions are simply undetermined events in the brain. <bookmark mark='d'/>Both "
            "require that some choice was genuinely open until we settled it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kane(self):
        hc = history_card(1996, r"Robert Kane", r"\textit{The Significance of Free Will}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        left = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=SELF, fill_opacity=0.1),
                      label(r"stop to help the victim", font_size=19, color=SELF)).move_to([-2.4, -0.3, 0])
        right = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=WILL, fill_opacity=0.1),
                       label(r"hurry on to the meeting", font_size=19, color=WILL)).move_to([2.4, -0.3, 0])
        her = VGroup(Circle(radius=0.3, color=GREY_A), label(r"her", font_size=16, color=GREY_A)).move_to([0, 1.3, 0])
        aa = Arrow(her.get_bottom(), left.get_top(), buff=0.1, color=SELF)
        ab = Arrow(her.get_bottom(), right.get_top(), buff=0.1, color=WILL)
        rows = stack([(r"a self-forming action: \ two efforts of will, \ each for a reason she has", GREY_A),
                      (r"brain noise makes the outcome undetermined", CHANCE),
                      (r"whichever she chooses, \ she chose it, \ for her reasons, \ and endorses it", GOAL)],
                     font_size=20, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Kane's central case is a businesswoman on her way to an important meeting, who sees an assault in an "
            "alley. <bookmark mark='a'/>She is torn: her moral reasons pull her to stop and help, her ambition to "
            "hurry on. She makes an effort of will in both directions at once. <bookmark mark='b'/>Noise in her "
            "brain makes the outcome undetermined. <bookmark mark='c'/>Whichever way it goes, Kane says, she chose "
            "it, for reasons that were hers, and having chosen she will endorse it. Such self-forming actions, he "
            "argues, are where we become the authors of our characters."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(her))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), GrowArrow(aa), GrowArrow(ab), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Wiggle(her))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def torn(self):
        d = load("torn")
        head = label(r"Where could indeterminism matter? \ A torn decision, \ built", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert d["gamma"] == 0.5 and d["lambda"] == 0.7808 and d["slope"] == d["ln10_over_lambda"] == 2.949
        assert [r["exponent"] for r in rows] == [3, 6, 9, 12, 15, 20, 30]
        assert [r["time"] for r in rows] == [8.63, 17.48, 26.33, 35.17, 44.02, 58.76, 88.26]
        assert all(r["side"] == "right" and r["mirror"] == "left" for r in rows)
        ax1 = Axes(x_range=[-1.6, 1.6, 1], y_range=[-0.3, 0.3, 0.3], x_length=4.6, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B, "include_ticks": False}).move_to([-3.8, 0.9, 0])
        well = ax1.plot(lambda x: -x ** 2 / 2 + x ** 4 / 4, x_range=[-1.55, 1.55], color=SELF, stroke_width=3)
        ball = Dot(ax1.c2p(0, 0) + UP * 0.12, radius=0.12, color=WILL)
        wl = VGroup(label(r"help", font_size=17, color=OK).next_to(ax1.c2p(-1, -0.25), DOWN, buff=0.1),
                    label(r"hurry on", font_size=17, color=BAD).next_to(ax1.c2p(1, -0.25), DOWN, buff=0.1))
        f = MathTex(r"\ddot x = x - x^3 - 0.5\,\dot x", font_size=28, color=SELF).next_to(ax1, DOWN, buff=0.45)
        f2 = MathTex(r"t_{\text{decide}} \approx \frac{\ln(1/\varepsilon)}{\lambda}, \quad \lambda = 0.781",
                     font_size=28, color=GOAL).next_to(f, DOWN, buff=0.3)
        ax2 = Axes(x_range=[0, 30, 5], y_range=[0, 90, 30], x_length=5.0, y_length=3.6, tips=False,
                   axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([3.4, -0.4, 0])
        xl = label(r"offset $\varepsilon = 10^{-k}$: \ $k$", font_size=16, color=GREY_A).next_to(ax2.x_axis, DOWN,
                                                                                               buff=0.4)
        yl = label(r"time to fall to one side", font_size=16, color=GREY_A).next_to(ax2.y_axis, UP, buff=0.12)
        pts = VGroup(*[Dot(ax2.c2p(r["exponent"], r["time"]), radius=0.07, color=CHANCE) for r in rows])
        line = Line(ax2.c2p(rows[0]["exponent"], rows[0]["time"]), ax2.c2p(rows[-1]["exponent"], rows[-1]["time"]),
                    color=CHANCE, stroke_width=2)
        note = label(r"each factor of ten smaller adds the same delay: \ 2.95 time units", font_size=17,
                     color=CHANCE).next_to(ax2, DOWN, buff=0.75)
        intro = label(r"Kane: \ chaos might amplify quantum indeterminacy; \ Balaguer \ (2010): \ torn decisions, "
                      r"\ reasons balanced", font_size=18, color=GREY_A).next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "Where in a brain could indeterminism do this work? Kane suggested that chaotic processes might "
            "amplify quantum indeterminacy, and Mark Balaguer described torn decisions, in 2010, as ones where the "
            "reasons on each side are balanced. <bookmark mark='a'/>The Reasoner models such a decision as a ball "
            "balanced on the hump between two wells: help, or hurry on. It obeys a simple damped equation. "
            "<bookmark mark='b'/>At the top, any offset, however tiny, grows exponentially, so the ball falls to the "
            "side the offset points to. <bookmark mark='c'/>The Reasoner starts it ten to the minus three from the "
            "top, then ten to the minus six, down to ten to the minus thirty, far below any quantum scale in a "
            "neuron. Each factor of ten adds the same delay, and even the smallest decides in finite time. "
            "<bookmark mark='d'/>So a balanced system can let an undetermined microscopic event settle a choice. "
            "Max Tegmark estimated in 2000 that quantum superpositions in neurons decohere within ten to the minus "
            "thirteen seconds, far too fast to be directly involved, but amplified noise needs no superposition, "
            "only chance. The physics can make room. What it cannot do is answer the next objection: if chance "
            "settles the choice, how is that the agent settling it?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(intro))
            vo.wait_until("a")
            self.play(Create(ax1), Create(well), FadeIn(ball), FadeIn(wl), Write(f))
            vo.wait_until("b")
            self.play(ball.animate.move_to(ax1.c2p(1, -0.25) + UP * 0.12), run_time=1.2, rate_func=rate_functions.ease_in_quad)
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.25), Create(line), run_time=2)
            self.play(FadeIn(note))
            vo.wait_until("d")
            self.play(Indicate(pts[-1], color=WHITE))
        self.clear_scene()

    def rollback(self):
        d = load("rollback")
        head = label(r"The rollback argument, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["p"] == 0.7 and d["replays"] == 1000 and d["truths"] == 708
        assert d["running"] == [1.0, 1.0, 1.0, 0.9, 0.85, 0.78, 0.74, 0.74, 0.712, 0.708]
        dots = VGroup()
        for k, v in enumerate(d["first"]):
            dots.add(Dot([-6.2 + 0.31 * k, 2.25, 0], radius=0.09, color=OK if v else BAD))
        dl = label(r"the first 40 replays: \ truth \ (green) \ or lie \ (red)", font_size=18,
                   color=GREY_A).next_to(dots, DOWN, buff=0.15)
        ax = Axes(x_range=[0, 1000, 200], y_range=[0, 1, 0.5], x_length=9.4, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 1}}
                  ).move_to([-1.0, -1.1, 0])
        xl = label(r"replays", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"share telling the truth", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12).shift(
            RIGHT * 1.0)
        curve = VMobject(color=OK, stroke_width=3).set_points_as_corners(
            [ax.c2p(5 * k + 1, v) for k, v in enumerate(d["curve"])])
        line = DashedLine(ax.c2p(0, 0.7), ax.c2p(1000, 0.7), color=GREY_B)
        side = stack([(r"after 1000 replays: \ 708 truths, \ 0.708", OK),
                      (r"near the chance, \ 0.7: \ the frequency is all there is to say", GREY_A),
                      (r"van Inwagen: \ so which way one replay goes is luck", BAD)], font_size=19,
                     aligned_edge=LEFT, width=3.4, buff=0.3).move_to([5.0, -0.9, 0])
        with self.voiceover(
            "Van Inwagen, an incompatibilist himself, pressed the luck objection against such views with a thought "
            "experiment. <bookmark mark='a'/>Alice is undecided between telling the truth and lying, and at an "
            "undetermined moment she tells the truth. Now suppose God rolls the universe back to just before that "
            "moment, and lets it run again, and again, a thousand times. The Reasoner runs the replays, with a "
            "seventy percent chance of the truth each time. <bookmark mark='b'/>Early on the share bounces around. "
            "After ten replays it is ninety percent; after a hundred, seventy four. <bookmark mark='c'/>After a "
            "thousand, seven hundred and eight truths: point seven oh eight. The frequency settles to the chance. "
            "<bookmark mark='d'/>Watching the replays, van Inwagen says, we could only conclude that what happens on "
            "any one of them is a matter of chance. If that is what an undetermined choice looks like, how can it "
            "be up to Alice? Libertarians reply that chance at the level of outcomes is compatible with the choice "
            "being hers at the level of reasons; the debate is far from over."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.05), FadeIn(dl), run_time=3)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(line))
            self.play(Create(curve), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()
