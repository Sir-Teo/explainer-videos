from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Error designed in", r"Which designs invite the wrong action?", marr=("how",))
        self.compat()
        self.fitts()
        self.hick()

    def compat(self):
        chips_section(self, r"Compatibility and stereotypes", [
            (r"spatial compatibility", r"the control for the left burner on the left: \ Chapanis's stove experiments "
                                       r"found errors whenever the layout broke the map", SYMP),
            (r"movement stereotypes", r"turn right for more, \ up for on (in some countries down), \ clockwise to "
                                      r"close a tap: \ expectations a design must meet or overcome", MODEL),
            (r"coding", r"shape, \ size, \ colour, \ position, \ texture: \ several codes at once, \ so one failure "
                        r"is caught by another", PERSON),
            (r"consistency", r"the same action in the same place across every system an operator uses", GOOD),
        ], "Some designs invite the wrong action. <bookmark mark='a'/> Spatial compatibility: the control for the left "
           "burner on the left. Chapanis's stove experiments found errors whenever the layout broke the map. "
           "<bookmark mark='b'/> Movement stereotypes: turn right for more, clockwise to close a tap. These are "
           "expectations a design must meet, or pay to overcome. <bookmark mark='c'/> Coding: shape, size, colour, "
           "position and texture, several at once, so that one failure is caught by another. <bookmark mark='d'/> "
           "And consistency: the same action in the same place, across every system an operator uses.")

    def fitts(self):
        d = load("fitts")
        head = heading(r"Fitts's law")
        A = axes([0, 7], [0, 1.4], x_length=5.4, y_length=3.0, xticks=[1, 3, 5, 7], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"difficulty: \ $\log_2(D/W + 1)$ bits",
                 ylabel=r"movement time (s)", center=[-3.3, 0.3, 0], font_size=12)
        dots = scatter(A.ax, d["ID"], d["t"], MODEL, radius=0.035)
        line = Line(A.ax.c2p(0.5, d["a"] + d["b"] * 0.5), A.ax.c2p(6.5, d["a"] + d["b"] * 6.5), color=PERSON,
                    stroke_width=4)
        eq = MathTex(r"MT = a + b\log_2\!\left(\tfrac{D}{W} + 1\right)", font_size=34, color=PERSON).move_to([3.4, 2.0, 0])
        rows = rows_of([
            (r"1954: \ Paul Fitts: \ the time to hit a target grows with the log of distance over width", WHITE),
            (rf"Psyche's 400 simulated movements: \ $b$ = {d['b']:.2f} s per bit, \ $r$ = {d['r']:.2f}", MODEL),
            (r"big, \ near targets for frequent or urgent actions; \ screen edges and corners are infinitely deep", GOOD),
            (r"small, \ far targets for actions that should take deliberate effort", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.5, 0])
        tag = psyche_tag(r"\texttt{work.fitts\_trials}")
        tag2 = published_tag(r"Fitts (1954)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Controls also take time to reach. <bookmark mark='a'/> In 1954 Paul Fitts showed that the time to hit a "
            "target grows with the logarithm of its distance over its width. <bookmark mark='b'/> Here are four "
            "hundred simulated movements, with a slope of about zero point one five seconds per bit. "
            "<bookmark mark='c'/> So frequent or urgent actions get big, near targets. The edges and corners of a "
            "screen are infinitely deep, because the pointer stops there. <bookmark mark='d'/> And actions that should "
            "take deliberate effort get small, far ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dots), Create(line))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def hick(self):
        d = load("hick")
        head = heading(r"Choices take time, \ and mappings add to it")
        A = axes([0, 9], [0, 1.2], x_length=5.4, y_length=3.0, xticks=[1, 2, 4, 6, 8], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"number of alternatives",
                 ylabel=r"reaction time (s)", center=[-3.3, 0.3, 0], font_size=12)
        cc = curve(A.ax, d["n"], d["compatible"], GOOD, stroke_width=4)
        ci = curve(A.ax, d["n"], d["incompatible"], AUTH, stroke_width=4)
        key = VGroup(label(r"compatible mapping", font_size=13, color=GOOD),
                     label(r"incompatible mapping", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"the Hick-Hyman law: \ reaction time grows with the log of the number of equally likely choices", WHITE),
            (r"an incompatible mapping (press left for a light on the right) adds a translation step, \ and the cost "
             r"grows with the choices", AUTH),
            (r"in an emergency, \ every extra bit is time; \ compatible mappings stay fast under stress, \ incompatible "
             r"ones collapse", PERSON),
            (r"Part 1's Donders measured mental stages the same way", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.hick\_rt}, \ illustrative parameters")
        with self.voiceover(
            "Choices take time too. <bookmark mark='a'/> The Hick-Hyman law: reaction time grows with the logarithm of "
            "the number of equally likely choices. <bookmark mark='b'/> An incompatible mapping, such as pressing left "
            "for a light on the right, adds a translation step, and the cost grows with the choices. "
            "<bookmark mark='c'/> In an emergency every extra bit is time. Compatible mappings stay fast under stress, "
            "and incompatible ones collapse. <bookmark mark='d'/> Part 1's Donders measured mental stages the same way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cc))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ci))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
