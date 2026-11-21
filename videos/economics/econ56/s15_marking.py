from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

SCHEME = [
    (r"the objective and the four constraints", 3),
    (r"which constraints bind, \ with a reason", 3),
    (r"the reduced problem and its first-order conditions", 3),
    (r"$q_H = 2$, \ $q_L = 0.5$, \ the transfers", 3),
    (r"the slack constraints checked; \ one sentence of meaning", 2),
]


class Marking(VoiceoverScene):
    def construct(self):
        card(self, 13, r"How the exam is marked, \ and what to do when stuck", r"What earns marks, and what "
             r"does a good answer look like?", "Chapter thirteen. How the exam is marked, and what to do when "
             "stuck.", scale=("person",), horizon=("a day",))
        self.scheme()
        self.two_answers()
        self.stuck()
        self.eye()

    def scheme(self):
        rows = VGroup()
        for text, m in SCHEME:
            t = label(text, font_size=22, color=WHITE)
            mk = label(rf"{m}", font_size=24, color=EST)
            rows.add(VGroup(t, mk))
        rows.arrange(DOWN, buff=0.32)
        for r_ in rows:
            r_[0].align_to(np.array([-5.0, 0, 0]), LEFT)
            r_[1].move_to([4.6, r_[0].get_center()[1], 0])
        total = VGroup(label(r"total", font_size=22, color=GREY_A).align_to(np.array([-5.0, 0, 0]), LEFT),
                       label(r"14", font_size=24, color=EST).move_to([4.6, 0, 0]))
        total.next_to(rows, DOWN, buff=0.45)
        total[0].align_to(np.array([-5.0, 0, 0]), LEFT)
        total[1].set_x(4.6)
        rule = Line([-5.2, 0, 0], [5.0, 0, 0], color=GREY_C, stroke_width=1.5).next_to(total, UP, buff=0.2)
        head = label(r"a mark scheme: \ Question 4(a), \ screening with two types", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        sub = label(r"marks", font_size=20, color=EST).move_to([4.6, rows.get_top()[1] + 0.45, 0])
        tag = note(r"illustrative: \ a typical scheme, \ not any department's", font_size=14,
                   color=E.SOURCE).to_corner(DL, buff=0.3)
        g = VGroup(rows, total, rule, sub)
        g.move_to(DOWN * 0.2)
        with self.voiceover(
            "How is an answer marked? Graders work from a scheme like this one, for part a of question four, "
            "fourteen marks. <bookmark mark='a'/> Three for writing the objective and all four constraints. "
            "<bookmark mark='b'/> Three for saying which bind, and why. <bookmark mark='c'/> Three for the "
            "reduced problem and its first-order conditions. <bookmark mark='d'/> Three for the numbers. "
            "<bookmark mark='e'/> And two for checking the slack constraints and saying, in a sentence, what the "
            "answer means. <bookmark mark='f'/> Notice how few of the fourteen are for the final numbers: most "
            "marks are for the steps that produce them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(Create(rule), FadeIn(total), Indicate(rows[3], color=EST, scale_factor=1.0))
        self.clear_scene()

    def two_answers(self):
        def sheet(title, lines, score, color):
            body = VGroup(*[wrapped_label(t, 5.0, 19, WHITE) for t in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.18)
            head = label(title, font_size=22, color=color)
            sc = label(score, font_size=34, color=color)
            inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            box = RoundedRectangle(width=5.8, height=4.6, corner_radius=0.12, stroke_color=color, stroke_width=2,
                                   fill_color=PAPER, fill_opacity=0.96)
            inner.move_to(box).align_to(box, UP).shift(DOWN * 0.3)
            sc.next_to(box, DOWN, buff=0.25)
            return VGroup(box, inner, sc)

        a = sheet(r"answer A", [r"$q_H = 2$, \ $q_L = 0.5$.", r"$t_L = 0.5$, \ $t_H = 3.5$.",
                                r"(no working shown)"], r"3 of 14", ERR)
        b = sheet(r"answer B", [r"maximize expected profit s.t. IR and IC for both types.",
                                r"IR$_L$ and IC$_H$ bind: \ the high type can always mimic.",
                                r"substitute: \ $\Pi(q_L, q_H)$; \ FOCs give $q_H = 2$ and",
                                r"$\tfrac23(1 - q_L) = \tfrac16$, \ so $q_L = 0.75$",
                                r"(a slip: \ the right side should be $\tfrac13$)",
                                r"no distortion at the top; \ the low type's quality is cut to reduce the rent."],
                  r"12 of 14", GAIN)
        VGroup(a, b).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.1)
        with self.voiceover(
            "Two answers to the same part. <bookmark mark='a'/> Answer A has every number right and no working. "
            "It earns three marks, the ones for the numbers, and a grader cannot tell it from a copied answer. "
            "<bookmark mark='b'/> Answer B sets the problem up, says which constraints bind and why, makes one "
            "arithmetic slip, carries it through correctly, and says what the result means. It earns twelve. "
            "<bookmark mark='c'/> Method marks are the rule almost everywhere: an error carried forward is "
            "penalized once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(b, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Indicate(b[2], color=GAIN))
        self.clear_scene()

    def stuck(self):
        cards = point_cards([
            (r"write it down anyway", r"the objective, \ the constraints, \ the Bellman equation: \ they carry "
             r"marks on their own", MICRO),
            (r"solve a special case", r"two types before a continuum, \ no noise before noise, \ $n = 2$ before $n$",
             MACRO),
            (r"check units, \ signs, \ limits", r"does the answer have the right units? \ the right sign? \ the "
             r"right limit as a parameter goes to 0?", METRICS),
            (r"state what you would need", r"`if the instrument is excluded, \ then \dots': \ an assumption named "
             r"is half an argument", GAIN),
            (r"budget the time", r"a 25-mark question gets a quarter of the time; \ move on, \ and come back", EST),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.2)
        head = label(r"what to do when stuck", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "What to do when stuck. <bookmark mark='a'/> Write down what you can: the objective, the constraints, "
            "the Bellman equation. They carry marks on their own, and writing them often unsticks you. <bookmark "
            "mark='b'/> Solve a special case: two types before a continuum, no noise before noise, two bidders "
            "before n. Every question tonight did that. <bookmark mark='c'/> Check the units, the signs and the "
            "limits. <bookmark mark='d'/> If you cannot prove something, state the assumption you would need: an "
            "assumption named is half an argument. <bookmark mark='e'/> And budget the time: a question worth a "
            "quarter of the marks gets a quarter of the time. Move on, and come back."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcde", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def eye(self):
        rows = VGroup(
            label(r"the condition that pins the answer down, \ labelled", font_size=24, color=MICRO),
            label(r"every step with its reason in the margin", font_size=24, color=MACRO),
            label(r"the answer in a box", font_size=24, color=GAIN),
            label(r"one sentence: \ what it means, \ and when it would fail", font_size=24, color=METRICS),
            label(r"a figure with its axes labelled, \ where a figure helps", font_size=24, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.1)
        head = label(r"what a grader looks for", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What does a grader look for, scanning a page in a minute? <bookmark mark='a'/> The condition that "
            "pins the answer down, labelled. <bookmark mark='b'/> Steps with reasons. <bookmark mark='c'/> The "
            "answer, boxed. <bookmark mark='d'/> One sentence on what it means and when it would fail. <bookmark "
            "mark='e'/> And a figure where one helps, with its axes labelled. Every solution in this part was "
            "written that way, on purpose."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
