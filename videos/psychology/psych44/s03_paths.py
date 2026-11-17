from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node


class Paths(VoiceoverScene):
    def construct(self):
        self.card()
        self.tracing()
        self.matrix()

    def card(self):
        card = chapter_card(2, r"Wright's paths", r"How do arrows make correlations?", lit={1921: r"Wright"},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter two. Wright's paths."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def tracing(self):
        head = heading(r"The tracing rule")
        A, B, C, D = node("A", SYMP), node("B", PERSON), node("C", MODEL), node("D", GOOD)
        A.move_to([-5.2, 1.2, 0])
        B.move_to([-3.2, 1.2, 0])
        C.move_to([-5.2, -0.8, 0])
        D.move_to([-3.2, -0.8, 0])
        arrs = VGroup(arrow(A, B, text=r"$a$"), arrow(A, C, text=r"$b$"), arrow(B, D, text=r"$c$"),
                      arrow(C, D, text=r"$d$"))
        rows = rows_of([
            (r"standardized variables, \ arrows as direct effects, \ no loops", WHITE),
            (r"Wright's rule: \ a correlation is the sum, \ over every path that links two variables, \ of the product "
             r"of the coefficients along it", MODEL),
            (r"a path may go backward along arrows, \ then forward, \ but never forward then backward, \ and through "
             r"no variable twice", PERSON),
            (r"here: \ $r_{AD} = ac + bd$, \ and $r_{BC} = ab$, \ through their common cause A", GOOD),
        ], 6.4, 20, 0.4).move_to([3.0, -0.1, 0])
        eq = MathTex(r"r_{BC} = a\,b", font_size=36, color=GOOD).move_to([-4.2, -2.4, 0])
        with self.voiceover(
            "Wright's rule turns arrows into correlations. <bookmark mark='a'/> Take standardized variables, arrows "
            "for direct effects, and no loops. <bookmark mark='b'/> A correlation is the sum, over every path that "
            "links two variables, of the product of the coefficients along it. <bookmark mark='c'/> A path may go "
            "backward along the arrows and then forward, but never forward then backward, and through no variable "
            "twice. <bookmark mark='d'/> Here, the correlation of A and D is a c plus b d. And B and C correlate a "
            "times b, though neither causes the other, through their common cause A."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(A, B, C, D)), FadeIn(arrs))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(eq))
        self.clear_scene()

    def matrix(self):
        head = heading(r"In matrix form")
        eqs = VGroup(
            MathTex(r"\mathbf{x} = B\,\mathbf{x} + \boldsymbol{\zeta}", font_size=40, color=WHITE),
            MathTex(r"\Sigma = (I - B)^{-1}\,\Psi\,(I - B)^{-\top}", font_size=40, color=MODEL),
        ).arrange(DOWN, buff=0.5).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"$B$ holds the arrows (direct effects), \ $\Psi$ the covariances of what the arrows leave unexplained", WHITE),
            (r"expanding $(I - B)^{-1} = I + B + B^2 + \dots$ \ sums the paths of length 0, \ 1, \ 2 and so on: \ "
             r"Wright's rule, \ in one line", MODEL),
            (r"\texttt{sem.path\_implied} computes it for any recursive model; \ the tests check it against the "
             r"tracing rule", YOU),
        ], 12.4, 22, 0.4).move_to([0, -1.5, 0])
        with self.voiceover(
            "In matrix form, Wright's rule is one line. <bookmark mark='a'/> Each variable equals the arrows into it "
            "plus a disturbance. B holds the arrows, and psi holds the covariances of what the arrows leave "
            "unexplained. <bookmark mark='b'/> The implied covariance is the inverse of I minus B, times psi, times "
            "its transpose. Expand the inverse as I plus B plus B squared and so on, and each power sums the paths of "
            "one length. That's Wright's rule. <bookmark mark='c'/> Psyche computes it for any model without loops, "
            "and the tests check it against the tracing rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
