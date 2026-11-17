from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

LIGHT = "#5AA9FF"


def mouse(center, frozen=False, color=GREY_A):
    c = np.asarray(center, float)
    body = Ellipse(width=0.9, height=0.5, color=color, stroke_width=3, fill_color="#1A2130", fill_opacity=1).move_to(c)
    head = Circle(radius=0.2, color=color, stroke_width=3, fill_color="#1A2130", fill_opacity=1).move_to(
        c + RIGHT * 0.52 + UP * 0.08)
    ear = Circle(radius=0.09, color=color, stroke_width=3).move_to(c + RIGHT * 0.5 + UP * 0.3)
    tail = ArcBetweenPoints(c + LEFT * 0.45, c + LEFT * 0.95 + UP * 0.25, angle=-PI / 3, color=color, stroke_width=3)
    g = VGroup(tail, body, head, ear)
    if frozen:
        g.add(*[Line(c + np.array([dx, 0.5, 0]), c + np.array([dx * 1.5, 0.78, 0]), color=THRESH, stroke_width=3)
                for dx in (-0.25, 0.0, 0.25)])
    return g


def box(center, name, color=GREY_B, w=3.9, h=2.4):
    c = np.asarray(center, float)
    r = RoundedRectangle(width=w, height=h, corner_radius=0.15, color=color, stroke_width=3, fill_color="#0E131C",
                         fill_opacity=1).move_to(c)
    return VGroup(r, label(name, font_size=26, color=color).next_to(r, UP, buff=0.1))


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.engram()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ where is a memory?", r"Can a memory be found, and switched on?",
                            lit=(), part=PART, scale=("neuron", "circuit", "mind"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter fourteen. Frontier: where is a memory?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def engram(self):
        head = heading(r"2012: \ a memory, switched on with light")
        xs = [-4.6, 0.0, 4.6]
        y = 1.05
        b1, b2, b3 = box([xs[0], y, 0], r"day 1: \ box A", BAD), box([xs[1], y, 0], r"later: \ box B", GREY_B), \
            box([xs[2], y, 0], r"box B", LIGHT)
        m1, m2, m3 = (mouse([x, y - 0.35, 0], frozen=fz).scale(1.4, about_point=[x, y - 0.35, 0])
                      for x, fz in zip(xs, (False, False, True)))
        shock = VGroup(*[Line([xs[0] - 1.5 + 0.5 * k, y - 1.05, 0], [xs[0] - 1.3 + 0.5 * k, y - 0.9, 0], color=BAD,
                              stroke_width=4) for k in range(7)])
        g = np.random.default_rng(12)

        def cells(cx, lit, light=False):
            grp = VGroup()
            for k in range(14):
                p = np.array([cx - 1.55 + 0.24 * k, y + 0.75 + 0.14 * (k % 2), 0])
                on = k in lit
                grp.add(Dot(p, radius=0.085, color=(LIGHT if light else THRESH) if on else GREY_D))
            return grp

        tagged = sorted(g.choice(14, 4, replace=False).tolist())
        c1, c2, c3 = cells(xs[0], tagged), cells(xs[1], []), cells(xs[2], tagged, light=True)
        fibre = VGroup(Line([xs[2] + 0.95, y + 2.0, 0], [xs[2] + 0.35, y + 1.0, 0], color=LIGHT, stroke_width=5),
                       label(r"blue light", font_size=22, color=LIGHT).move_to([xs[2] + 1.75, y + 1.75, 0]))
        caps = VGroup(
            wrapped_label(r"a mild shock. \ The cells active during learning are made to carry a "
                          r"light-sensitive channel", 4.2, 26, WHITE),
            wrapped_label(r"a different box: \ the mouse explores, unafraid", 4.2, 26, WHITE),
            wrapped_label(r"light on the tagged cells: \ the mouse freezes", 4.2, 26, LIGHT),
        )
        for cap, x in zip(caps, xs):
            cap.move_to([x, y - 1.4, 0], aligned_edge=UP)
        controls = wrapped_label(r"controls: \ no freezing if there was no shock, \ if the tagged cells carry no "
                                 r"channel, \ or if the cells were tagged in a harmless box", 13.0, 26, GREY_A)
        controls.move_to([0, -2.3, 0])
        end = wrapped_label(r"Activating those cells is enough to bring the memory back, as behaviour.", 13.0, 29,
                            P.ACCENT).move_to([0, -3.15, 0])
        # Hebb's idea, drawn: a set of cells bound together
        g2 = np.random.default_rng(49)
        pts = [np.array([-2.6 + 1.05 * (k % 6) + 0.25 * g2.standard_normal(), 1.3 - 1.2 * (k // 6)
                         + 0.25 * g2.standard_normal(), 0]) for k in range(18)]
        chosen = [1, 4, 8, 11, 15]
        net = VGroup(*[Line(pts[a], pts[b], color=RULE, stroke_width=4) for i, a in enumerate(chosen)
                       for b in chosen[i + 1:]],
                     *[Dot(q, radius=0.14, color=THRESH if k in chosen else GREY_D) for k, q in enumerate(pts)])
        net_l = wrapped_label(r"Hebb's idea: \ a memory is a set of cells bound together by strengthened "
                              r"synapses. \ Could anyone find such a set?", 9.0, 30, WHITE).move_to([0, -1.9, 0])
        idea = VGroup(net, net_l)
        src = published_tag(archive.LIU_2012.cite)
        tag = note(r"schematic: no data from the paper").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Hebb's idea was that a memory is a set of cells bound together by strengthened synapses. For "
            "decades nobody could find such a set. The next part tells the story of the man who spent thirty "
            "years looking. Then, in 2012, a laboratory at MIT did something Hebb couldn't have imagined. "
            "<bookmark mark='a'/> Xu Liu, Steve Ramirez and their colleagues put a mouse in a box and gave "
            "it a mild shock to the feet. The mouse learns to fear that box. And with a genetic trick, the "
            "cells of the hippocampus that were active during that learning, and only those, were made to "
            "carry a channel that opens when blue light falls on it. <bookmark mark='b'/> Later, the mouse "
            "is put in a quite different box. It has no reason to be afraid there, and it explores. "
            "<bookmark mark='c'/> Then light is sent down an optical fibre onto the tagged cells. And the "
            "mouse freezes, which is what a frightened mouse does. <bookmark mark='d'/> The controls are "
            "what make it convincing. No freezing if the mouse was never shocked. None if the tagged cells "
            "carry no channel. None if the cells were tagged in a harmless box. <bookmark mark='e'/> So "
            "switching on the cells that were active during an experience is enough to bring something of "
            "that experience back, at least as behaviour. A year later the same group used the method to "
            "attach a fear to a place where nothing bad had ever happened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(idea))
            vo.wait_until("a")
            self.play(FadeOut(idea), run_time=0.6)
            self.play(FadeIn(b1), FadeIn(m1), FadeIn(shock))
            self.play(FadeIn(c1, lag_ratio=0.1), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(m2), FadeIn(c2), FadeIn(caps[1]))
            self.play(m2.animate.shift(LEFT * 0.6), run_time=1.2)
            self.play(m2.animate.shift(RIGHT * 1.0), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(b3), FadeIn(m3), FadeIn(c3), FadeIn(fibre), FadeIn(caps[2]))
            vo.wait_until("d")
            self.play(FadeIn(controls))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"What nobody knows yet")
        qs = [
            (r"Is the memory in the synapses, or in the cells?", r"Tagging finds the cells. \ Whether the strengthened "
             r"synapses between them are the memory, or only the way in, is argued.", EXC),
            (r"Is spike timing the rule in a living brain?", r"In a dish, yes. \ In an animal, firing rates, the "
             r"position of a synapse on its dendrite and the modulators all change the answer.", RULE),
            (r"How does a synapse deep in a network know it should change?", r"Hebb's rule sees only its two cells. "
             r"\ Artificial networks solve this with a signal no synapse could have: \ Part 58.", MODEL),
        ]
        rows = VGroup()
        for i, (q, a, col) in enumerate(qs, 1):
            rows.add(VGroup(label(rf"{i}. \ {q}", font_size=34, color=col), wrapped_label(a, 12.6, 28, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12))
        star = VGroup(label(r"$\star$ \ a problem to take away", font_size=30, color=P.ACCENT),
                      wrapped_label(r"Design the experiment that would tell ``the memory is the pattern of "
                                    r"strengthened synapses'' from ``the memory is which cells were chosen''. \ "
                                    r"What must be blocked, what switched on, and what would each answer look "
                                    r"like?", 12.6, 28, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        col = VGroup(*rows, star).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, -0.3, 0])
        with self.voiceover(
            "That experiment answers one question and opens three. <bookmark mark='a'/> First. Is the memory "
            "in the synapses, or in the cells? The method finds the cells. Whether the strengthened synapses "
            "between them are the memory itself, or only the usual way of getting to it, is being argued "
            "right now. <bookmark mark='b'/> Second. Is spike timing really the rule in a living brain? In a "
            "dish, yes. In an animal, how fast the cells are firing, where on the dendrite the synapse sits, "
            "and which modulators are present all change the answer. <bookmark mark='c'/> Third, and "
            "deepest. Hebb's rule knows about two cells. But suppose an animal makes a mistake, and the "
            "synapse that ought to change is many steps away from the place where the mistake shows. How "
            "does it know? Artificial networks solve that with a signal no real synapse could receive in "
            "the same way. Whether brains have an equivalent is one of the central open problems, and "
            "Part 58 takes it up. <bookmark mark='d'/> And a problem for you. Design the experiment that "
            "would tell those first two possibilities apart. What would you block, what would you switch "
            "on, and what would each answer look like?"
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(star, shift=UP * 0.1))
        self.clear_scene()
