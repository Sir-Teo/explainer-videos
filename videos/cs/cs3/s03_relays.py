from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import CODE, CTRL, DATA, HEAD, HIST, NO, ONE, PART, WIRE, YES, lamp, light, switch
from videos.cs.cs2.common import truth_table


def ladder(branches, x0=-4.0, x1=1.0, y0=1.2, dy=1.0, length=0.9):
    """Branches in parallel between two vertical rails; each branch is a list of (literal tex) contacts in series.
    Returns the group and, per branch, its switches."""
    g = VGroup()
    sw = []
    ys = [y0 - k * dy for k in range(len(branches))]
    g.add(Line([x0, ys[0], 0], [x0, ys[-1], 0], color=WIRE, stroke_width=3),
          Line([x1, ys[0], 0], [x1, ys[-1], 0], color=WIRE, stroke_width=3))
    for y, br in zip(ys, branches):
        n = len(br)
        xs = np.linspace(x0, x1, n + 2)[1:-1]
        row = []
        prev = np.array([x0, y, 0])
        for x, lit in zip(xs, br):
            s = switch(False, length=length).move_to([x, y, 0])
            t = MathTex(lit, font_size=30, color=DATA).next_to(s, UP, buff=0.12)
            g.add(Line(prev, s.left(), color=WIRE, stroke_width=3), s, t)
            row.append((s, lit))
            prev = s.right()
        g.add(Line(prev, [x1, y, 0], color=WIRE, stroke_width=3))
        sw.append(row)
    g.rails = (x0, x1, ys)
    return g, sw


class Relays(VoiceoverScene):
    def construct(self):
        self.card()
        self.dictionary()
        self.staircase()
        self.simplify()
        self.consensus()

    def card(self):
        card = chapter_card(2, r"Circuits are expressions", r"How does a switching circuit compute?", lit=(1937,),
                            part=PART)
        with self.voiceover("Chapter two. Circuits are expressions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dictionary(self):
        head = label(r"Shannon's dictionary", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup()
        items = [
            (r"switches in series", r"x \cdot y", r"\textsc{and}"),
            (r"switches in parallel", r"x + y", r"\textsc{or}"),
            (r"a contact that opens when energized", r"\bar x", r"\textsc{not}"),
            (r"two contacts on the same relay", r"x, \ x", r"the same variable"),
            (r"a network between two points", r"f(x, y, \dots)", r"an expression"),
        ]
        for a, b, c in items:
            rows.add(VGroup(label(a, font_size=28, color=GREY_A), MathTex(r"\longleftrightarrow", font_size=32,
                                                                           color=GREY_C),
                            MathTex(b, font_size=34, color=DATA), label(c, font_size=26, color=CTRL)))
        for i, r in enumerate(rows):
            r[0].move_to([-1.6, 1.8 - 0.75 * i, 0], aligned_edge=RIGHT)
            r[1].move_to([-0.8, 1.8 - 0.75 * i, 0])
            r[2].move_to([0.0, 1.8 - 0.75 * i, 0], aligned_edge=LEFT)
            r[3].move_to([3.0, 1.8 - 0.75 * i, 0], aligned_edge=LEFT)
        so = label(r"so: \ any circuit can be written as an expression, \ and any expression built as a circuit",
                   font_size=28, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Shannon's thesis is a dictionary between two languages. <bookmark mark='a'/> Switches in series are "
            "multiplication: and. Switches in parallel are addition: or. A contact that opens when its relay is "
            "energized is not. Several contacts worked by the same relay are the same variable, used several times. "
            "<bookmark mark='b'/> And so any network of switches between two points is an expression, which is true "
            "exactly when current can flow. The dictionary works both ways: to analyse a circuit, write its expression; "
            "to design one, write the expression you want, simplify it with the laws, and translate back."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(so))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def staircase(self):
        head = label(r"A light with a switch at each end of the stairs", font_size=36).to_edge(UP, buff=0.35)
        g, sw = ladder([[r"A", r"\bar B"], [r"\bar A", r"B"]], x0=-5.2, x1=-0.6, y0=0.9, dy=1.6, length=1.0)
        x0, x1, ys = g.rails
        lp = lamp(False).move_to([0.6, (ys[0] + ys[1]) / 2, 0])
        g.add(Line([x1, (ys[0] + ys[1]) / 2, 0], lp.get_left(), color=WIRE, stroke_width=3))
        tt = truth_table([r"A", r"B", r"\text{lamp}"], [[a, b, a != b] for a, b in ((False, False), (False, True),
                                                                                      (True, False), (True, True))],
                         font_size=32, col_w=1.15, colors={0: DATA, 1: DATA, 2: HEAD}).move_to(RIGHT * 4.6 + UP * 0.4)
        eq = MathTex(r"A \bar B + \bar A B = A \oplus B", font_size=38, color=YES).next_to(tt, DOWN, buff=0.4)
        note_ = note(r"\textsc{xor}: \ flipping either switch flips the light", font_size=22).next_to(eq, DOWN,
                                                                                                  buff=0.15)
        with self.voiceover(
            "An example every house has. A staircase light, with a switch at the bottom and a switch at the top: "
            "flipping either one changes the light. <bookmark mark='a'/> In Shannon's language, the lamp should be on "
            "when A is up and B is down, or A is down and B is up. Two branches in parallel, each with two contacts in "
            "series; the bars are contacts that close when their switch is down. <bookmark mark='b'/> Try the four "
            "positions. <bookmark mark='c'/> The lamp is A exclusive-or B. The real two-way switch in your wall is this "
            "circuit, folded into one clever contact."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(lp))
            vo.wait_until("a")
            self.play(FadeIn(tt.cells[0][0]), FadeIn(tt.cells[0][1]), FadeIn(tt.cells[0][2]), FadeIn(tt.rule))
            vo.wait_until("b")
            for k, (a, b) in enumerate(((False, False), (False, True), (True, False), (True, True))):
                vals = {r"A": a, r"\bar B": not b, r"\bar A": not a, r"B": b}
                anims = [s.set(vals[lit]) for row in sw for s, lit in row if s.closed != vals[lit]]
                if anims:
                    self.play(*anims, run_time=0.5)
                on = a != b
                self.play(light(lp, on), FadeIn(tt.rows[k]), run_time=0.6)
                self.wait(0.6)
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simplify(self):
        head = label(r"Designing by algebra", font_size=38).to_edge(UP, buff=0.35)
        g, _ = ladder([[r"x", r"y"], [r"x", r"z"], [r"x", r"\bar y", r"\bar z"]], x0=-6.2, x1=-1.6, y0=1.3, dy=1.1,
                      length=0.8)
        cnt1 = label(r"7 contacts", font_size=26, color=NO).next_to(g, DOWN, buff=0.3)
        steps = VGroup(*[MathTex(t, font_size=36, color=c) for t, c in (
            (r"x y + x z + x \bar y \bar z", GREY_A),
            (r"= x\,(y + z + \bar y \bar z)", GREY_A),
            (r"= x\,\big((y + z) + \overline{y + z}\big)", GREY_A),
            (r"= x \cdot 1 = x", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.8 + UP * 0.6)
        whys = VGroup(note(r"distributivity", font_size=20), note(r"De Morgan", font_size=20),
                      note(r"complement", font_size=20))
        for w, s in zip(whys, steps[1:]):
            w.next_to(s, RIGHT, buff=0.3)
        one = switch(True, length=1.0).move_to(RIGHT * 2.4 + DOWN * 2.1)
        ol = MathTex("x", font_size=32, color=DATA).next_to(one, UP, buff=0.12)
        cnt2 = label(r"1 contact", font_size=26, color=YES).next_to(one, RIGHT, buff=0.4)
        hist = note(r"Shannon's thesis did this for real telephone circuits, \ and designed an adder with relays "
                    r"(Part 4)", font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is the payoff. <bookmark mark='a'/> A circuit with three parallel paths: x and y; x and z; x and not y "
            "and not z. Seven contacts. <bookmark mark='b'/> Write its expression and apply the laws. Factor out x. "
            "What is left in the bracket is y or z, or the negation of y or z, by De Morgan. Something or its negation "
            "is always true. <bookmark mark='c'/> So the whole network is just x: one contact does the work of seven. "
            "Shannon did exactly this to real telephone circuits, and in the same thesis designed a relay circuit that "
            "adds binary numbers, which is where Part 4 begins."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(cnt1))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            for s, w in zip(steps[1:], whys):
                self.play(FadeIn(s, shift=DOWN * 0.1), FadeIn(w), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(one), FadeIn(ol), FadeIn(cnt2))
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consensus(self):
        head = label(r"Analysis: \ a contact that does nothing", font_size=38).to_edge(UP, buff=0.35)
        g, _ = ladder([[r"x", r"y"], [r"\bar x", r"z"], [r"y", r"z"]], x0=-6.2, x1=-2.0, y0=1.3, dy=1.1, length=0.8)
        f = MathTex(r"f = x y + \bar x z + y z", font_size=38, color=GREY_A).move_to(RIGHT * 2.6 + UP * 1.6)
        argm = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"if $y = z = 1$: \ either $x = 1$ \ (top path) \ or $x = 0$ \ (middle path)", GREY_A),
            (r"so the bottom path never carries current \ that the others do not", HEAD),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(f, DOWN, buff=0.4)
        thm = MathTex(r"x y + \bar x z + y z = x y + \bar x z", font_size=38, color=YES).next_to(argm, DOWN, buff=0.45)
        tl = note(r"the \textit{consensus} theorem: \ $yz$ is redundant \ (but see chapter 10)", font_size=22).next_to(
            thm, DOWN, buff=0.15)
        with self.voiceover(
            "The dictionary also works for analysis. <bookmark mark='a'/> Here is a circuit with three paths: x and y; "
            "not x and z; y and z. Its expression is x y plus not x z plus y z. <bookmark mark='b'/> Is the bottom path "
            "doing anything? It conducts when y and z are both closed. But then x is either closed, and the top path "
            "conducts anyway, or open, and the middle one does. The bottom path never adds a connection the others "
            "lack. <bookmark mark='c'/> So y z can be removed: this is the consensus theorem, and synthesis tools apply "
            "it constantly. Chapter ten will show a reason you might deliberately keep that useless contact."
        ) as vo:
            self.play(FadeIn(head), Create(g))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(argm, lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Write(thm), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()
