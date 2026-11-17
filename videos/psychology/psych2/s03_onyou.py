from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.pendulum()
        self.coin()
        self.leak()

    def card(self):
        card = chapter_card(2, r"On you: \ the pendulum and the coin", r"Do you give yourself away too?",
                            lit={1833: r"Chevreul's pendulum", 1852: r"Carpenter: ideo-motor action"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter two. Two experiments, and you are the subject of both."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def pendulum(self):
        stage = demo_stage(width=8.4, height=5.2, center=[-2.6, -0.2, 0])
        c = stage.box.get_center()
        pivot = c + UP * 2.0
        hand = VGroup(RoundedRectangle(width=1.2, height=0.5, corner_radius=0.2, stroke_width=0, fill_color=P.HUMAN,
                                       fill_opacity=0.9).move_to(pivot + UP * 0.28),
                      label(r"your hand, held still", font_size=22, color=GREY_A).move_to(pivot + UP * 0.28 + RIGHT * 2.0))
        thread = Line(pivot, pivot + DOWN * 2.6, color=GREY_A, stroke_width=2)
        bob = Circle(radius=0.2, stroke_color=P.ACCENT, stroke_width=5).move_to(pivot + DOWN * 2.8)
        swing = VGroup(thread, bob)
        cross = VGroup(Line(c + DOWN * 2.05 + LEFT * 2.6, c + DOWN * 2.05 + RIGHT * 2.6, color=GREY_B, stroke_width=3),
                       Line(c + DOWN * 2.3 + LEFT * 0.0, c + DOWN * 1.8, color=GREY_B, stroke_width=3))
        steps = VGroup(*[wrapped_label(t, 4.3, 25, WHITE) for t in (
            r"1. \ Tie a ring or a key to 25 cm of thread.",
            r"2. \ Rest your elbow on the table and hold the thread still over a line drawn on paper.",
            r"3. \ Do not move. \ Just \emph{think} of the ring swinging along the line.",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.5, 0])
        name = VGroup(label(r"ideomotor action", font_size=34, color=P.ACCENT),
                      wrapped_label(r"thinking of a movement starts the movement, below what you can feel", 4.3, 23,
                                    GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        name.next_to(steps, DOWN, buff=0.45).align_to(steps, LEFT)
        with self.voiceover(
            "Hans read movements his questioners didn't know they were making. Do you make them? Here's a test "
            "you can do in a minute. Pause the video if you'd like to set it up. <bookmark mark='a'/> Tie a ring, "
            "or a key, to a piece of thread about as long as your forearm. <bookmark mark='b'/> Rest your elbow "
            "on the table, and hold the thread so that the ring hangs still, just above a line drawn on a piece "
            "of paper. <bookmark mark='c'/> Now don't move your hand. Just think of the ring swinging along the "
            "line. Imagine it going back and forth. <bookmark mark='d'/> For most people, within half a minute, "
            "it does. Think of a circle instead, and it circles. <bookmark mark='e'/> The chemist Michel Chevreul "
            "studied this in 1833, when pendulums were being used to divine metals and answer questions. He found "
            "that when he looked away, the swinging stopped. The pendulum knew only what his eyes told his hand. "
            "<bookmark mark='f'/> The name for it came in 1852: ideomotor action. Thinking of a movement begins "
            "the movement, too faintly to feel. It's what moved the heads of Pfungst's twenty-three subjects, and "
            "it's what moves a ouija board."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(swing), FadeIn(steps[0], shift=LEFT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(hand), FadeIn(cross), FadeIn(steps[1], shift=LEFT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(steps[2], shift=LEFT * 0.15))
            vo.wait_until("d")
            for amp in (0.06, 0.12, 0.2, 0.26, 0.26):
                self.play(Rotate(swing, amp, about_point=pivot), run_time=0.45, rate_func=smooth)
                self.play(Rotate(swing, -2 * amp, about_point=pivot), run_time=0.9, rate_func=smooth)
                self.play(Rotate(swing, amp, about_point=pivot), run_time=0.45, rate_func=smooth)
            vo.wait_until("f")
            self.play(FadeIn(name, shift=UP * 0.15))
            for amp in (0.2, 0.12):
                self.play(Rotate(swing, amp, about_point=pivot), run_time=0.45, rate_func=smooth)
                self.play(Rotate(swing, -2 * amp, about_point=pivot), run_time=0.9, rate_func=smooth)
                self.play(Rotate(swing, amp, about_point=pivot), run_time=0.45, rate_func=smooth)
        self.clear_scene()

    def keys(self, seq, y, color) -> VGroup:
        g = VGroup()
        for k, s in enumerate(seq):
            sq = Square(side_length=0.27, stroke_width=0, fill_color=color if s else "#2A3242", fill_opacity=1)
            g.add(sq.move_to([-5.6 + 0.29 * k, y, 0]))
        return g

    def coin(self):
        d = load("be_random")
        stage = demo_stage(width=12.4, height=3.0, center=[0, 1.55, 0])
        c = stage.box.get_center()
        ask = VGroup(label(r"Be a coin.", font_size=50, color=WHITE),
                     label(r"In your head: \ heads or tails, twenty times, as randomly as you can.", font_size=30,
                           color=GREY_A)).arrange(DOWN, buff=0.25).move_to(c)
        ring = countdown_ring(0.5).move_to(c + RIGHT * 5.2 + DOWN * 0.7)
        person, coin_ = d["person"], d["coin"]
        row_p = self.keys(d["example_person"][:30], -0.8, P.HUMAN)
        row_c = self.keys(d["example_coin"][:30], -1.9, P.SIGNAL)
        lab_p = label(r"a person-like sequence", font_size=24, color=P.HUMAN).next_to(row_p, UP, buff=0.12)
        lab_p.align_to(row_p, LEFT)
        lab_c = label(r"a coin", font_size=24, color=P.SIGNAL).next_to(row_c, UP, buff=0.12).align_to(row_c, LEFT)
        facts = VGroup(
            label(rf"switches {100 * person['alternation']:.0f}\% of the time", font_size=26, color=P.HUMAN),
            label(rf"switches {100 * coin_['alternation']:.0f}\% of the time", font_size=26, color=P.SIGNAL))
        facts[0].next_to(row_p, RIGHT, buff=0.35)
        facts[1].next_to(row_c, RIGHT, buff=0.35)
        runs = label(rf"longest run in {d['n_press']} presses: \ about {person['longest_run']:.1f} for the "
                     rf"switcher, \ {coin_['longest_run']:.0f} for the coin", font_size=28, color=GREY_A)
        runs.to_edge(DOWN, buff=0.75)
        tag = note(r"sequences: a generator that switches 60\% of the time (the usual figure for people), and a "
                   r"fair coin").to_corner(DL, buff=0.3)
        four = label(rf"a run of four or more in 20 tosses of a real coin: \ {100 * d['p_run4_in_20']:.0f} times in "
                     r"100", font_size=30, color=P.SIGNAL).next_to(stage, DOWN, buff=0.5)
        with self.voiceover(
            "The second experiment. Be a coin. <bookmark mark='a'/> In your head, call heads or tails, twenty "
            "times, as randomly as you can. Go."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ask[0]))
            vo.wait_until("a")
            self.play(FadeIn(ask[1]), FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=10.0, rate_func=linear)
        with self.voiceover(
"Now think about what you did. Did you ever call the same side four times in a row? "
            "<bookmark mark='b'/> A real coin, in twenty tosses, usually does. People almost never do, because "
            "four in a row doesn't feel random. "
            "<bookmark mark='c'/> Here's a sequence of the kind people make: it switches sides about six times in "
            "ten. <bookmark mark='d'/> And here's a real coin, which switches half the time, and so it clumps. "
            f"<bookmark mark='e'/> In a hundred tosses a coin's longest run is about {coin_['longest_run']:.0f}. "
            "The switcher's is shorter. This has been found over and over since the nineteen-fifties: asked to be "
            "random, people alternate too much."
        ) as vo:
            self.play(FadeOut(ring), ask[1].animate.set_color(GREY_C))
            vo.wait_until("b")
            self.play(FadeIn(four, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeOut(four), FadeIn(lab_p), FadeIn(tag), LaggedStart(*[FadeIn(k) for k in row_p], lag_ratio=0.05),
                      run_time=3.0)
            self.play(FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(lab_c), LaggedStart(*[FadeIn(k) for k in row_c], lag_ratio=0.05), run_time=3.0)
            self.play(FadeIn(facts[1]))
            vo.wait_until("e")
            self.play(FadeIn(runs, shift=UP * 0.15))
        self.clear_scene()

    def leak(self):
        d = load("be_random")
        person, coin_ = d["person"], d["coin"]
        head = heading(r"A program that watches you can guess you")
        unit = 9.0
        rows = VGroup()
        for name, v, color in ((r"against a coin", coin_["accuracy"], P.SIGNAL),
                               (r"against a 60\% switcher", person["accuracy"], P.HUMAN)):
            bar = Rectangle(width=v * unit, height=0.7, stroke_width=0, fill_color=color, fill_opacity=0.85)
            bar.move_to([-4.2 + v * unit / 2, 0, 0])
            nm = label(name, font_size=28, color=color).next_to(bar, UP, buff=0.1).align_to(bar, LEFT)
            val = label(rf"{100 * v:.0f}\% guessed", font_size=34, color=color).next_to(bar, RIGHT, buff=0.25)
            rows.add(VGroup(bar, nm, val))
        rows.arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.5, 0])
        half_x = rows[0][0].get_left()[0] + 0.5 * unit
        half = DashedLine([half_x, rows.get_top()[1] + 0.2, 0], [half_x, rows.get_bottom()[1] - 0.2, 0], color=GREY_B,
                          stroke_width=2)
        half_lab = label(r"chance", font_size=22, color=GREY_B).next_to(half, DOWN, buff=0.08)
        moral = VGroup(
            label(r"You leak what you know, and you leak what you will do next.", font_size=34, color=P.ACCENT),
            label(r"So in an experiment, nothing is left to a person that a deck of cards can decide.", font_size=32),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.85)
        # the predictor, in outline: your last presses, and its guess at the next
        past = VGroup(*[Square(side_length=0.5, stroke_width=0, fill_color=P.HUMAN if s else "#2A3242",
                               fill_opacity=1) for s in d["example_person"][:10]]).arrange(RIGHT, buff=0.08)
        nxt = VGroup(Square(side_length=0.5, stroke_color=P.PSYCHE, stroke_width=3, fill_color="#101726",
                            fill_opacity=1), label(r"?", font_size=36, color=P.PSYCHE))
        nxt[1].move_to(nxt[0])
        strip = VGroup(past, nxt).arrange(RIGHT, buff=0.2)
        cap = VGroup(label(r"your presses so far", font_size=24, color=GREY_A),
                     label(r"its guess, made before you press", font_size=24, color=P.PSYCHE))
        cap[0].next_to(past, DOWN, buff=0.15)
        cap[1].next_to(nxt, UP, buff=0.2)
        machine = VGroup(strip, cap).move_to([0, 0.3, 0])
        tag = psyche_tag(rf"computed: a context predictor on {d['n_press']} presses of each generator")
        with self.voiceover(
            "And if you're predictable, you can be read. <bookmark mark='a'/> On this part's page of the course "
            "site there's a small program that watches you press two keys at random, and before each press, "
            "guesses it. It does nothing clever. It remembers what you did the last few times you were in the "
            "same situation. <bookmark mark='b'/> Against a real coin it's right half the time, as it must be. "
            f"<bookmark mark='c'/> Against a sequence that only switches a little too often, it gets "
            f"{100 * person['accuracy']:.0f} per cent, and real people have more habits than that for it to find. "
            "Try it, and see your own number. <bookmark mark='d'/> So here are two facts about you, to carry "
            "through the rest of this part. You leak what you know. And you leak what you're about to do. "
            "<bookmark mark='e'/> An experimenter is a person too. So in a well-designed experiment, nothing is "
            "left to a person that a deck of cards can decide."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.1) for k in past], lag_ratio=0.15), FadeIn(cap[0]),
                      run_time=3.0)
            self.play(FadeIn(nxt, scale=1.2), FadeIn(cap[1]))
            vo.wait_until("b")
            self.play(FadeOut(machine))
            self.play(GrowFromEdge(rows[0][0], LEFT), FadeIn(rows[0][1]), FadeIn(rows[0][2]), Create(half),
                      FadeIn(half_lab))
            vo.wait_until("c")
            self.play(GrowFromEdge(rows[1][0], LEFT), FadeIn(rows[1][1]), FadeIn(rows[1][2]))
            vo.wait_until("d")
            self.play(FadeIn(moral[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(moral[1], shift=UP * 0.15))
        self.clear_scene()
