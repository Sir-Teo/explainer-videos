from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import (CTRL, DATA, HEAD, HIST, NO, ONE, PART, WIRE, YES, ZERO, Relay, lamp, light, switch,
                                  wire)
from videos.cs.cs2.common import truth_table


def battery(p, h=0.7):
    p = np.asarray(p, float)
    return VGroup(Line(p + LEFT * 0.3 + UP * 0.06, p + RIGHT * 0.3 + UP * 0.06, color=GREY_A, stroke_width=4),
                  Line(p + LEFT * 0.16 + DOWN * 0.08, p + RIGHT * 0.16 + DOWN * 0.08, color=GREY_A, stroke_width=4))


class Hook(VoiceoverScene):
    def construct(self):
        self.thesis()
        self.series()
        self.parallel()
        self.relay()
        self.plan()

    # ------------------------------------------------------------------
    def thesis(self):
        hc = history_card(1937, r"Claude Shannon, \ aged 21, \ MIT", r"master's thesis: \ \textit{A Symbolic Analysis "
                          r"of Relay and Switching Circuits}", width=6.6, font_size=26).move_to(UP * 1.4)
        q = label(r"``possibly the most important, \ and also the most famous, \\ master's thesis of the century''",
                  font_size=30, color=GREY_A).next_to(hc, DOWN, buff=0.7)
        src = note(r"Howard Gardner, \textit{The Mind's New Science} (1985)", font_size=22).next_to(q, DOWN, buff=0.2)
        hc.shift(UP * 0.5)
        preview, sa, sb, lp, ws = self.circuit(False)
        preview.scale(0.6).move_to(LEFT * 2.4 + DOWN * 0.4)
        eq = MathTex(r"A \wedge B", font_size=44, color=YES).move_to(RIGHT * 3.0 + DOWN * 0.4)
        arrow = MathTex(r"\longleftrightarrow", font_size=44, color=HEAD).move_to(RIGHT * 0.7 + DOWN * 0.4)
        q.move_to(DOWN * 2.45)
        src.next_to(q, DOWN, buff=0.18)
        with self.voiceover(
            "In 1937 a twenty-one-year-old student at MIT, Claude Shannon, was looking after a room-sized machine "
            "built of gears, motors and hundreds of telephone relays, Vannevar Bush's differential analyzer. "
            "<bookmark mark='a'/> Designing relay circuits then was an art, done by trial and error. Shannon noticed "
            "that it did not have to be. The algebra George Boole had invented in 1854 to describe the laws of thought "
            "described these circuits exactly. <bookmark mark='b'/> His master's thesis on the idea has been called "
            "possibly the most important master's thesis of the century. It is the reason every computer since has "
            "been designed with algebra."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(preview), FadeIn(eq), FadeIn(arrow))
            vo.wait_until("a")
            self.play(sa.set(True), sb.set(True), light(lp, True), ws.animate.set_stroke(ONE), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(src))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def circuit(self, parallel: bool):
        bat = battery([-5.0, -0.2, 0])
        lp = lamp(False).move_to([1.2, -0.2, 0])
        if parallel:
            sa = switch(False).move_to([-2.0, 0.6, 0])
            sb = switch(False).move_to([-2.0, -1.0, 0])
            ws = VGroup(
                wire(bat.get_top(), [-3.2, 0.6, 0], via="v"),
                Line([-3.2, 0.6, 0], sa.left(), color=WIRE, stroke_width=3),
                Line([-3.2, 0.6, 0], [-3.2, -1.0, 0], color=WIRE, stroke_width=3),
                Line([-3.2, -1.0, 0], sb.left(), color=WIRE, stroke_width=3),
                Line(sa.right(), [-0.8, 0.6, 0], color=WIRE, stroke_width=3),
                Line(sb.right(), [-0.8, -1.0, 0], color=WIRE, stroke_width=3),
                Line([-0.8, 0.6, 0], [-0.8, -1.0, 0], color=WIRE, stroke_width=3),
                Line([-0.8, -0.2, 0], lp.get_left(), color=WIRE, stroke_width=3),
                wire(lp.get_right(), [2.2, -1.8, 0], via="hv"),
                Line([2.2, -1.8, 0], [-5.0, -1.8, 0], color=WIRE, stroke_width=3),
                Line([-5.0, -1.8, 0], bat.get_bottom(), color=WIRE, stroke_width=3),
            )
        else:
            sa = switch(False).move_to([-3.0, 0.8, 0])
            sb = switch(False).move_to([-0.9, 0.8, 0])
            ws = VGroup(
                Line(bat.get_top(), [-5.0, 0.8, 0], color=WIRE, stroke_width=3),
                Line([-5.0, 0.8, 0], sa.left(), color=WIRE, stroke_width=3),
                Line(sa.right(), sb.left(), color=WIRE, stroke_width=3),
                Line(sb.right(), [1.2, 0.8, 0], color=WIRE, stroke_width=3),
                Line([1.2, 0.8, 0], lp.get_top(), color=WIRE, stroke_width=3),
                Line(lp.get_bottom(), [1.2, -1.6, 0], color=WIRE, stroke_width=3),
                Line([1.2, -1.6, 0], [-5.0, -1.6, 0], color=WIRE, stroke_width=3),
                Line([-5.0, -1.6, 0], bat.get_bottom(), color=WIRE, stroke_width=3),
            )
        la = MathTex("A", font_size=36, color=DATA).next_to(sa, UP, buff=0.25)
        lb = MathTex("B", font_size=36, color=DATA).next_to(sb, UP if not parallel else DOWN, buff=0.25)
        return VGroup(ws, bat, sa, sb, lp, la, lb), sa, sb, lp, ws

    def run_table(self, vo, sa, sb, lp, ws, tt, fn, marks):
        state = [False, False]
        for k, (a, b) in enumerate(((False, False), (False, True), (True, False), (True, True))):
            anims = []
            if a != state[0]:
                anims.append(sa.set(a))
            if b != state[1]:
                anims.append(sb.set(b))
            state = [a, b]
            on = fn(a, b)
            if anims:
                self.play(*anims, run_time=0.5)
            self.play(light(lp, on), ws.animate.set_stroke(ONE if on else WIRE), FadeIn(tt.rows[k]), run_time=0.6)
            if marks and k < len(marks):
                vo.wait_until(marks[k])

    def series(self):
        g, sa, sb, lp, ws = self.circuit(False)
        head = label(r"Two switches in series", font_size=38).to_edge(UP, buff=0.35)
        tt = truth_table([r"A", r"B", r"\text{lamp}"], [[a, b, a and b] for a, b in ((False, False), (False, True),
                                                                                       (True, False), (True, True))],
                         font_size=34, col_w=1.2, colors={0: DATA, 1: DATA, 2: HEAD}).move_to(RIGHT * 4.8 + DOWN * 0.1)
        eq = MathTex(r"\text{lamp} = A \wedge B", font_size=40, color=YES).next_to(tt, DOWN, buff=0.45)
        with self.voiceover(
            "Here is his observation, in its simplest form. A battery, a lamp, and two switches, A and B, one after "
            "the other. <bookmark mark='a'/> Current flows, and the lamp lights, only if A is closed and B is closed. "
            "Try all four settings. <bookmark mark='b'/> The table is Boole's and: switches in series compute A and B."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1:]), FadeIn(tt.cells[0][0]), FadeIn(tt.cells[0][1]),
                      FadeIn(tt.cells[0][2]), FadeIn(tt.rule))
            vo.wait_until("a")
            self.run_table(vo, sa, sb, lp, ws, tt, lambda a, b: a and b, None)
            vo.wait_until("b")
            self.play(Write(eq))
        self.wait(0.3)
        self.clear_scene()

    def parallel(self):
        g, sa, sb, lp, ws = self.circuit(True)
        head = label(r"Two switches in parallel", font_size=38).to_edge(UP, buff=0.35)
        tt = truth_table([r"A", r"B", r"\text{lamp}"], [[a, b, a or b] for a, b in ((False, False), (False, True),
                                                                                      (True, False), (True, True))],
                         font_size=34, col_w=1.2, colors={0: DATA, 1: DATA, 2: HEAD}).move_to(RIGHT * 4.8 + DOWN * 0.1)
        eq = MathTex(r"\text{lamp} = A \vee B", font_size=40, color=YES).next_to(tt, DOWN, buff=0.45)
        with self.voiceover(
            "Now put the two switches side by side, so the current has two ways through. <bookmark mark='a'/> The lamp "
            "lights if A is closed, or B is, or both. <bookmark mark='b'/> Switches in parallel compute A or B. And a "
            "switch that opens when you push it, instead of closing, computes not. And with and, or and not, as "
            "chapter five will prove, you can build any truth table at all."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1:]), FadeIn(tt.cells[0][0]), FadeIn(tt.cells[0][1]),
                      FadeIn(tt.cells[0][2]), FadeIn(tt.rule))
            vo.wait_until("a")
            self.run_table(vo, sa, sb, lp, ws, tt, lambda a, b: a or b, None)
            vo.wait_until("b")
            self.play(Write(eq))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relay(self):
        head = label(r"A switch worked by electricity", font_size=38).to_edge(UP, buff=0.35)
        r1 = Relay(scale=1.3).move_to(LEFT * 3.0 + DOWN * 0.2)
        r2 = Relay(scale=1.3).move_to(RIGHT * 1.6 + DOWN * 0.2)
        link = wire(r1.contact.get_center(), r2.coil.get_left() + LEFT * 0.1, color=WIRE)
        l1 = label(r"current in the coil \\ pulls the contact shut", font_size=24, color=GREY_A).next_to(r1, DOWN,
                                                                                                    buff=0.4)
        l2 = label(r"its output drives \\ the next relay's coil", font_size=24, color=GREY_A).next_to(r2, DOWN, buff=0.4)
        key = label(r"so circuits can drive circuits: \ expressions inside expressions", font_size=28,
                    color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There is one more ingredient, and it is what makes a machine possible. <bookmark mark='a'/> In a relay, "
            "the switch is not pushed by a finger. A current through a coil makes a magnet, and the magnet pulls the "
            "contact closed. <bookmark mark='b'/> So the output of one switching circuit can work the switches of the "
            "next. Expressions can be plugged into expressions, without limit. <bookmark mark='c'/> Relays gave way to "
            "vacuum tubes and then to transistors, a billion times faster and a billion times smaller, but the idea in "
            "Shannon's thesis did not change at all. This part builds logic up from that single idea, all the way to "
            "the circuits Pebble will need."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r1), FadeIn(l1))
            vo.wait_until("a")
            self.play(r1.energize(True))
            vo.wait_until("b")
            self.play(Create(link), FadeIn(r2), FadeIn(l2))
            self.play(link.animate.set_stroke(ONE), r2.energize(True))
            vo.wait_until("c")
            self.play(FadeIn(key))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Logic from Switches", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"Boole's algebra, \ and Shannon's switches: \ circuits are expressions",
            r"the transistor as a switch, \ the CMOS inverter, \ NAND and NOR in silicon",
            r"one gate is enough: \ NAND, \ and Post's test for which gate sets are complete",
            r"normal forms, \ the Boolean cube and Karnaugh maps, \ multiplexers and decision diagrams",
            r"how many gates a function needs: \ Shannon's counting argument, \ and what nobody can prove",
            r"delay and glitches, \ the blocks Pebble needs, \ our simulator, \ and reversible gates",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 3 of Computer Science, Built, the first step of act one: building a computer from switches. "
            "<bookmark mark='a'/> In this part: Boole's algebra, and Shannon's switches. The transistor, the CMOS "
            "inverter, and NAND and NOR gates in silicon. A proof that one kind of gate is enough, and Emil Post's test "
            "for exactly which sets of gates are. Normal forms, the Boolean cube and Karnaugh maps, multiplexers and "
            "decision diagrams. How many gates a function needs, which Shannon answered with a counting argument, and "
            "the embarrassing question nobody can answer. Then delay and glitches, the building blocks Pebble needs, the "
            "simulator that will run every circuit in this series, and gates that never forget."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
