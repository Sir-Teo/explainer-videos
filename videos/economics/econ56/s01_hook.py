from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403


def envelope(width: float = 6.4, height: float = 3.8) -> VGroup:
    """A manila envelope, flap up, addressed to the candidate."""
    body = Rectangle(width=width, height=height, stroke_color="#C8A96A", stroke_width=2.5, fill_color="#3A3222",
                     fill_opacity=1)
    tl, tr = body.get_corner(UL), body.get_corner(UR)
    flap = Polygon(tl, tr, body.get_center() + UP * 0.2, stroke_color="#C8A96A", stroke_width=2.5,
                   fill_color="#4A3F2B", fill_opacity=1)
    addr = VGroup(label(r"Core Examination \ $\cdot$ \ Year 1", font_size=28, color="#F3E2B8"),
                  label(r"Microeconomics, \ Macroeconomics, \ Econometrics", font_size=20, color="#D9C79C"),
                  label(r"do not open before 9 a.m.", font_size=18, color="#E8A0B4")).arrange(DOWN, buff=0.18)
    addr.move_to(body.get_center() + DOWN * 0.75)
    g = VGroup(body, flap, addr)
    g.body, g.flap, g.addr = body, flap, addr
    return g


def clock(time_text: str = r"11:04 p.m.") -> VGroup:
    face = Circle(radius=0.55, stroke_color=GREY_B, stroke_width=2.5)
    hh = Line(ORIGIN, UP * 0.3 + LEFT * 0.05, color=WHITE, stroke_width=3).shift(face.get_center())
    mm = Line(ORIGIN, RIGHT * 0.42 + UP * 0.05, color=WHITE, stroke_width=2).shift(face.get_center())
    t = label(time_text, font_size=20, color=GREY_B).next_to(face, DOWN, buff=0.15)
    return VGroup(face, hh, mm, t)


class Hook(VoiceoverScene):
    def construct(self):
        self.night()
        self.era()
        self.reading()
        self.question()
        self.title()
        self.objectives()

    def night(self):
        env = envelope().move_to(UP * 0.4)
        clk = clock().to_corner(UR, buff=0.6)
        papers = VGroup()
        for name, col, k in ((r"Microeconomics", MICRO, 0), (r"Macroeconomics", MACRO, 1),
                             (r"Econometrics", METRICS, 2)):
            sheet = RoundedRectangle(width=3.6, height=4.6, corner_radius=0.08, stroke_color=col, stroke_width=2,
                                     fill_color=PAPER, fill_opacity=1)
            head = label(name, font_size=24, color=col).next_to(sheet.get_top(), DOWN, buff=0.3)
            lines = VGroup(*[Line(LEFT * 1.4, RIGHT * (1.4 - 0.5 * (j % 3 == 2)), color=GREY_D, stroke_width=2)
                             for j in range(9)]).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.35)
            qs = label(r"four questions \ $\cdot$ \ 100 marks", font_size=17, color=GREY_B).next_to(
                sheet.get_bottom(), UP, buff=0.25)
            papers.add(VGroup(sheet, head, lines, qs))
        papers.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.25)
        tag = note(r"illustrative: \ this exam is made up; \ its problems are the kind every programme sets",
                   font_size=14, color=E.SOURCE).to_corner(DL, buff=0.3)
        with self.voiceover(
            "It is eleven at night, the night before the first-year examinations. On the desk is an envelope that "
            "will not be opened until nine tomorrow morning. <bookmark mark='a'/> Inside are three papers, the core "
            "of every doctoral programme in economics: microeconomics, macroeconomics and econometrics, four "
            "questions each. <bookmark mark='b'/> Every question tonight is one of those, and every one of them "
            "rests on something this series has already built. We will work all twelve the way a grader wants to "
            "see them: the set-up, the condition that pins the answer down, the answer in a box, and a check. And "
            "after each, the mistakes that cost marks, which are rarely the ones students fear."
        ) as vo:
            self.play(FadeIn(env, shift=UP * 0.2), FadeIn(clk), FadeIn(tag))
            vo.wait_until("a")
            self.play(env.flap.animate.stretch(-1, 1, about_point=env.body.get_top()), run_time=0.8)
            self.play(FadeOut(env, shift=DOWN * 0.4), LaggedStart(*[FadeIn(p_, shift=UP * 0.6) for p_ in papers],
                                                                   lag_ratio=0.35), run_time=2.2)
            vo.wait_until("b")
            self.play(*[p_[2].animate.set_color(p_[0].get_stroke_color()).set_opacity(0.6) for p_ in papers],
                      run_time=1.5)
        self.clear_scene()

    def era(self):
        cards = VGroup(
            history_card(1947, r"Paul Samuelson", r"\emph{Foundations of Economic Analysis}: \ economics as "
                         r"maximization and equilibrium, \ worked in mathematics", color=MICRO, width=6.1,
                         font_size=20),
            history_card(1995, r"Mas-Colell, \ Whinston and Green", r"\emph{Microeconomic Theory}: \ the core's "
                         r"micro book for a generation", color=MICRO, width=6.1, font_size=20),
            history_card(2000, r"Ljungqvist and Sargent; \ Hayashi", r"\emph{Recursive Macroeconomic Theory} and "
                         r"\emph{Econometrics}: \ dynamic programming and GMM as the common language", color=MACRO,
                         width=6.1, font_size=20),
            history_card(2008, r"Jordi Gal\'i", r"\emph{Monetary Policy, Inflation, and the Business Cycle}: \ the "
                         r"three-equation model as a core topic", color=MACRO, width=6.1, font_size=20),
        )
        cards.arrange_in_grid(2, 2, buff=(0.4, 0.4)).move_to(DOWN * 0.2)
        head = label(r"where the core came from", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The core has a history. <bookmark mark='a'/> In 1947 Paul Samuelson's Foundations of Economic Analysis "
            "argued that most of economics is either a maximization or an equilibrium, and should be written in "
            "mathematics; the first-year examination still has that shape. <bookmark mark='b'/> In 1995 Andreu "
            "Mas-Colell, Michael Whinston and Jerry Green published the micro book that a generation of first-year "
            "students has carried. <bookmark mark='c'/> In 2000 Lars Ljungqvist and Thomas Sargent made dynamic "
            "programming the language of macro, and Fumio Hayashi made the generalized method of moments the "
            "language of econometrics. <bookmark mark='d'/> And by 2008, with Jordi Galí's book, the "
            "three-equation New Keynesian model had become a core topic. Each of tonight's questions comes from "
            "this canon."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def reading(self):
        chain = flow_chain([(r"who chooses what, \ given what?", MICRO),
                            (r"what pins it down?", MACRO),
                            (r"solve, \ and box the answer", METRICS),
                            (r"check it", GAIN)], direction=RIGHT, box_w=2.8, box_h=1.1, buff=0.5, font_size=21,
                           notes=[r"agents, \ choice variables, \ constraints, \ what is taken as given",
                                  r"a first-order condition, \ a Bellman equation, \ market clearing, \ a moment",
                                  r"every step with its reason in the margin",
                                  r"a special case, \ the units, \ the signs, \ a limit"], note_size=17)
        chain.move_to(DOWN * 0.2)
        head = label(r"how to read a problem", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Before any question, a way of reading one. <bookmark mark='a'/> First: who chooses what, and what do "
            "they take as given? A consumer chooses a bundle, taking prices as given; a central bank chooses "
            "inflation, taking expectations as given or not. <bookmark mark='b'/> Second: what condition pins the "
            "answer down? A first-order condition, a Bellman equation, market clearing, a population moment. "
            "<bookmark mark='c'/> Third: solve it, writing the reason for each step in the margin, and put the "
            "answer in a box, because a grader is looking for it. <bookmark mark='d'/> Fourth: check it. Does it "
            "reduce to something you know in a special case? Are the units right? Do the signs make sense? Half of "
            "all lost marks would have been saved by the fourth step."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=UP * 0.1), FadeIn(chain.notes[k])]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.9)
        rows = VGroup(
            label(r"can you set up each problem without being told the method?", font_size=26, color=MICRO),
            label(r"can you find the condition that pins the answer down?", font_size=26, color=MACRO),
            label(r"can you check your answer before a grader does?", font_size=26, color=METRICS),
            label(r"and do you know which ideas are settled, \ and which are still open?", font_size=26,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "So the question for tonight: can you do it with the book closed? <bookmark mark='a'/> Can you set up "
            "a problem without being told the method? <bookmark mark='b'/> Can you find the condition that pins "
            "the answer down? <bookmark mark='c'/> Can you check your answer before a grader does? <bookmark "
            "mark='d'/> And do you know which of these ideas are settled, and which are still open?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        papers = VGroup(*[RoundedRectangle(width=0.9, height=1.2, corner_radius=0.05, stroke_color=c_,
                                           stroke_width=2.5, fill_color=PAPER, fill_opacity=1)
                          for c_ in (MICRO, MACRO, METRICS)]).arrange(RIGHT, buff=0.25)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 56 \ $\cdot$ \ The Core Exam", font_size=34, color=E.ACCENT)
        VGroup(papers, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-six: the core exam."):
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in papers], lag_ratio=0.3), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act X \ $\cdot$ \ The Graduate Core", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"micro: \ a kinked budget, \ an externality, \ an auction with a reserve, \ a screening menu",
            r"macro: \ a Ramsey transition, \ benefits that run out, \ discretion, \ why $r < \rho$",
            r"econometrics: \ a demand curve, \ GMM, \ staggered timing, \ a long-run restriction",
            r"how answers are marked, \ and what to do when stuck",
            r"where each problem's idea is still open",
        ], color=E.ACCENT, font_size=29, width=13.0)
        with self.voiceover(
            "By the end of this part you will have worked <bookmark mark='a'/> four micro questions: a consumer "
            "with a kinked budget, an economy with an externality, an auction with a reserve price, and a "
            "screening contract; <bookmark mark='b'/> four macro questions: a tax on capital in the Ramsey model, a "
            "job seeker whose benefits run out, a central bank that cannot commit, and why a precautionary "
            "economy's interest rate lies below the rate of time preference; <bookmark mark='c'/> and four "
            "econometrics questions: identifying a demand curve, estimating an Euler equation by GMM, reading "
            "two-way fixed effects when adoption is staggered, and identifying a VAR from the long run. <bookmark "
            "mark='d'/> You will see how such answers are marked and what to do when stuck, <bookmark mark='e'/> "
            "and where each problem's idea is still being argued about."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
