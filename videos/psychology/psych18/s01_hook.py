from __future__ import annotations

import numpy as np

from videos.psychology.psych18.common import *  # noqa: F403


def court():
    """A schematic of the 1999 video: six players, three in white shirts and three in black, passing two balls."""
    floor = RoundedRectangle(width=6.4, height=3.6, corner_radius=0.2, stroke_color=GREY_C, stroke_width=2)
    white = [np.array(p) for p in ([-2.2, 0.9, 0], [-0.4, -1.0, 0], [1.6, 1.0, 0])]
    black = [np.array(p) for p in ([-1.4, -0.9, 0], [0.6, 1.1, 0], [2.3, -0.8, 0])]
    players = VGroup()
    for p in white:
        players.add(VGroup(Circle(0.22, color=WHITE, fill_color=WHITE, fill_opacity=1), Line(DOWN * 0.22, DOWN * 0.7,
                                                                                             color=WHITE)).move_to(p))
    for p in black:
        players.add(VGroup(Circle(0.22, color=GREY_B, fill_color="#20242b", fill_opacity=1),
                           Line(DOWN * 0.22, DOWN * 0.7, color=GREY_B)).move_to(p))
    return floor, players, white, black


class Hook(VoiceoverScene):
    def construct(self):
        self.gorilla()
        self.flicker()
        self.question()
        self.objectives()

    def gorilla(self):
        p = archive.SIMONS_CHABRIS_1999.data
        head = heading(r"Count the passes")
        floor, players, white, black = court()
        g = VGroup(floor, players).move_to([0, 0.9, 0])
        shift = g.get_center() - np.array([0, 0, 0])
        white = [w + shift for w in white]
        black = [b + shift for b in black]
        ball = Dot(white[0], radius=0.09, color=ATT)
        count = label(r"white team's passes: \ 0", font_size=26, color=ATT).next_to(floor, UP, buff=0.15)
        gor = VGroup(RoundedRectangle(width=0.7, height=1.3, corner_radius=0.3, fill_color="#4a505a", fill_opacity=1,
                                      stroke_color=GREY_A, stroke_width=2),
                     Circle(0.25, fill_color="#4a505a", fill_opacity=1, stroke_color=GREY_A, stroke_width=2)
                     .shift(UP * 0.85))
        gor.move_to(floor.get_right() + RIGHT * 0.6 + DOWN * 0.1)
        gl = label(r"a person in a gorilla suit, \ about nine seconds on screen", font_size=20, color=GREY_B)
        rows = rows_of([
            (rf"1999: \ Simons and Chabris; \ {p['observers']} observers counted the passes of one team", WHITE),
            (rf"{pct(p['missed'])} never saw the unexpected visitor: \ the gorilla, \ or in other versions a woman "
             r"with an umbrella", ATT),
            (r"it was not hidden: \ it was in plain view, \ and they were looking at the screen", GREY_A),
        ], 12.4, 27, 0.3).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.SIMONS_CHABRIS_1999.cite)
        with self.voiceover(
            "In 1999 Daniel Simons and Christopher Chabris made a short video. <bookmark mark='a'/> Six students, three "
            "in white shirts and three in black, pass basketballs to one another. The observers' task is to count the "
            "passes made by the white team, silently, and report the number at the end. <bookmark mark='b'/> Partway "
            "through, a person in a gorilla suit walks into the middle of the players, turns to the camera, thumps its "
            "chest and walks off. It is on screen for about nine seconds. <bookmark mark='c'/> Across this and "
            "versions in which a woman with an umbrella walked through instead, "
            f"{pct(p['missed'])} of the {p['observers']} observers never saw the unexpected visitor. Nothing was "
            "hidden, and nobody looked away. They were looking at the screen, at the right place, and they did not see a gorilla. "
            "<bookmark mark='d'/> Seeing, it turns out, is not just a matter of light reaching the eye."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(floor), FadeIn(players), FadeIn(ball), FadeIn(count))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            order = [white[0], white[1], white[2], white[0], white[1], white[2]]
            for k in range(1, 6):
                new = label(rf"white team's passes: \ {k}", font_size=26, color=ATT).move_to(count)
                self.play(ball.animate.move_to(order[k]), Transform(count, new), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(gor), run_time=0.5)
            self.play(gor.animate.move_to(floor.get_center() + DOWN * 0.1), run_time=2.0)
            gl.next_to(floor, DOWN, buff=0.15)
            self.play(FadeIn(gl), Wiggle(gor, scale_value=1.05))
            self.play(gor.animate.move_to(floor.get_left() + LEFT * 0.6), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(rows[1], color=ATT, scale_factor=1.03))
        self.clear_scene()

    def flicker(self):
        p = archive.RENSINK_1997.data
        head = heading(r"Spot the difference, \ with a flicker")
        boxes = VGroup()
        for name, col in ((r"A", WHITE), (r"blank", GREY_C), (r"A$'$", ATT), (r"blank", GREY_C), (r"A", WHITE),
                          (r"blank", GREY_C), (r"A$'$", ATT)):
            b = Rectangle(width=1.35 if name != "blank" else 0.55, height=1.0, stroke_color=col, stroke_width=2,
                          fill_color="#1a1f27" if name == "blank" else "#0b0e13", fill_opacity=1)
            boxes.add(VGroup(b, label(name, font_size=22, color=col).move_to(b)))
        boxes.arrange(RIGHT, buff=0.12).move_to([0, 2.0, 0])
        cap = label(rf"each picture {p['image_ms']} ms, \ each blank {p['blank_ms']} ms, \ round and round",
                    font_size=22, color=GREY_A).next_to(boxes, DOWN, buff=0.2)
        A = axes([0, 12], [0, 3], x_length=8.0, y_length=2.2, xticks=[0, 4, 8, 12], yticks=[],
                 xlabel=r"seconds to see the change", center=[1.4, -1.0, 0], font_size=18)
        ax = A.ax
        bars, labs = VGroup(), VGroup()
        for k, (v, name, col) in enumerate([(p["no_blank_seconds"], r"no blanks", GREY_B),
                                            (p["ci_seconds"], r"blanks: \ a central change", CUE),
                                            (p["mi_seconds"], r"blanks: \ a marginal change", ATT)]):
            y = 2.5 - k
            r = Rectangle(width=ax.c2p(v, 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=col,
                          fill_opacity=0.85)
            r.move_to(ax.c2p(0, y), aligned_edge=LEFT)
            bars.add(r)
            labs.add(VGroup(label(name, font_size=19, color=col).next_to(ax.c2p(0, y), LEFT, buff=0.2),
                            label(rf"{v} s", font_size=20, color=col).next_to(r, RIGHT, buff=0.12)))
        tag = published_tag(archive.RENSINK_1997.cite)
        with self.voiceover(
            "Here is the same blindness without a gorilla. <bookmark mark='a'/> In 1997 Ronald Rensink, Kevin O'Regan "
            "and James Clark showed people a photograph, then a brief grey blank, then the photograph again with one "
            "thing changed, then a blank, round and round, until they spotted the change. <bookmark mark='b'/> With "
            "no blank, the change was found in under a second: the flicker of the change itself grabs the eye. "
            "<bookmark mark='c'/> With the blank, which hides that flicker, a large change to the main object of the "
            f"scene took {p['ci_seconds']} seconds on average. <bookmark mark='d'/> A change to something at the margin, "
            f"an object nobody would mention if asked to describe the picture, took {p['mi_seconds']} seconds; for some "
            "pictures, close to a minute. The change was big, it repeated, and the observers knew it was there. They "
            "only saw it when they happened to attend to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.25), FadeIn(cap), FadeIn(A))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1], LEFT), FadeIn(labs[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2], LEFT), FadeIn(labs[2]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what attention is, \ and what it does")
        rows = rows_of([
            (r"why does so much reach the eye, \ and so little reach us?", WHITE),
            (r"where does the selecting happen: \ early, \ before meaning, \ or late, \ after it?", CUE),
            (r"what does attention do to a neuron, \ and to a decision in progress?", CONTROL),
            (r"and what does that mean for radiologists, \ drivers, \ alarms and screens?", ATT),
        ], 11.8, 31, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "This part is about that missing step. <bookmark mark='a'/> Why does so much reach the eye and the ear, "
            "and so little reach awareness? <bookmark mark='b'/> Where in the stream of processing does the selecting "
            "happen: early, before meaning is extracted, or late, after it? <bookmark mark='c'/> What does attending "
            "to something do to a neuron, and to a decision that is under way? <bookmark mark='d'/> And what does all "
            "this mean for people whose jobs are searching and watching: radiologists, drivers, airport screeners, "
            "and anyone with a phone?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 18", font_size=34, color=GREY_B), label(r"Attention", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the cocktail party and the first box in the head: \ filters, \ attenuation, \ load",
            r"a spotlight that moves without the eyes: \ Posner's cueing, \ inhibition of return",
            r"search: \ pop-out, \ feature integration, \ guided search, \ a saliency map",
            r"seeing without attention: \ change blindness and inattentional blindness",
            r"attention in time, \ conflict and control: \ the blink, \ the bottleneck, \ Stroop",
            r"what attention does to neurons: \ the normalization model, \ derived; \ capacity and vigilance",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 18 of Psychology, Built, and the first part of Act Five, on thinking: attention. "
            "<bookmark mark='a'/> We'll start at a cocktail party, with the first diagram of information flowing "
            "through a mind, and the argument about where it filters. Then a spotlight that moves without the eyes. "
            "Then search: why a red item pops out and a red vertical one doesn't, and the models that explain both, "
            "down to a saliency map you can compute. Then what we fail to see without attention. Then attention in "
            "time, and the conflict between what you read and what you're asked to name. Then what attention does to "
            "a single neuron, derived from one equation, and how much a glance can take in, and for how long we can "
            "keep watching. And at the end, alarms, radiology, roads and screens."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
