from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Params(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.lsat()

    def card(self):
        card = chapter_card(4, r"Two and three parameters", r"What if items differ in how sharply they sort people?",
                            lit={1968: r"Birnbaum", 1980: r"Lord"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter four. Two and three parameters."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curves(self):
        head = heading(r"Discrimination and guessing")
        eq = MathTex(r"P(\theta) = c_i + (1 - c_i)\,\frac{1}{1 + e^{-a_i(\theta - b_i)}}", font_size=38,
                     color=MODEL).move_to([0, 2.2, 0])
        A = axes([-4, 4], [0, 1], x_length=5.6, y_length=3.0, xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.25, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$", ylabel=r"P(correct)",
                 center=[-3.4, -0.8, 0], font_size=13)
        c1 = icc(A.ax, 0.5, 0.0, SYMP)
        c2 = icc(A.ax, 2.5, 0.0, PERSON)
        c3 = icc(A.ax, 1.5, 0.5, AUTH, c=0.25)
        rows = rows_of([
            (r"discrimination $a$: \ how steeply the curve rises; \ a steep item sorts people sharply near its "
             r"difficulty, \ a flat one barely sorts them", PERSON),
            (r"guessing $c$: \ a floor; \ on a four-option item, \ even the least able get about a quarter right", AUTH),
            (r"Birnbaum's two- and three-parameter models (in Lord and Novick, \ 1968); \ Lord's 1980 book made "
             r"them standard", MODEL),
            (r"the price: \ with unequal slopes, \ the sum score is no longer sufficient, \ and specific objectivity "
             r"is lost", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.6, 0])
        key = VGroup(label(r"$a = 0.5$", font_size=14, color=SYMP), label(r"$a = 2.5$", font_size=14, color=PERSON),
                     label(r"$a = 1.5, \ c = 0.25$", font_size=14, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        tag = published_tag(r"Lord \& Novick (1968); \ Lord (1980)")
        with self.voiceover(
            "Real items aren't all alike. <bookmark mark='a'/> Discrimination, a, is how steeply the curve rises. A "
            "steep item sorts people sharply near its difficulty. A flat one barely sorts them at all. "
            "<bookmark mark='b'/> Guessing, c, is a floor. On a four-option item, even the least able get about a "
            "quarter right. <bookmark mark='c'/> Allan Birnbaum wrote these two- and three-parameter models into Lord "
            "and Novick's 1968 textbook, and Frederic Lord's 1980 book made them standard. <bookmark mark='d'/> The "
            "price: with unequal slopes, the sum score is no longer sufficient, and specific objectivity is lost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c1), Create(c2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c3))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lsat(self):
        d = load("lsat")
        head = heading(r"Five law-school items")
        A = axes([-5, 3], [0, 1], x_length=5.6, y_length=3.2, xticks=[-4, -2, 0, 2], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$", ylabel=r"P(correct)",
                 center=[-3.4, 0.2, 0], font_size=13)
        cols = (GOOD, SYMP, AUTH, PERSON, MODEL)
        rc = VGroup(*[icc(A.ax, d["rasch_a"], b, c, stroke_width=2) for b, c in zip(d["rasch_b"], cols)])
        tc = VGroup(*[DashedVMobject(icc(A.ax, a, b, c, stroke_width=2), num_dashes=30)
                      for a, b, c in zip(d["twopl_a"], d["twopl_b"], cols)])
        key = VGroup(label(r"Rasch (solid)", font_size=14, color=WHITE),
                     label(r"two-parameter (dashed)", font_size=14, color=GREY_A)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"section 6 of the Law School Admission Test: \ five items, \ 1{,}000 people (Bock and Lieberman, \ 1970)",
             WHITE),
            (rf"Rasch (one shared slope, \ {d['rasch_a']:.2f}): \ log-likelihood {d['rasch_ll']:.1f}; \ "
             rf"two-parameter: \ {d['twopl_ll']:.1f}, \ with slopes from {d['twopl_a'].min():.2f} to "
             rf"{d['twopl_a'].max():.2f}", MODEL),
            (rf"likelihood ratio {d['lr']:.2f} on 4 df, \ $p = {d['lr_p']:.2f}$: \ the extra slopes buy nothing here", GOOD),
            (r"the items are easy: \ difficulties from about $-3.6$ to $-0.3$, \ so the test sorts weak candidates, \ "
             r"not strong ones", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.fit\_mml}; \ LSAT data (ltm); \ matches ltm's fit")
        with self.voiceover(
            "Does it matter in practice? <bookmark mark='a'/> Here are five items from the Law School Admission Test, "
            "answered by a thousand people, the data Darrell Bock and Robert Lieberman fitted in 1970. "
            "<bookmark mark='b'/> The Rasch model, with one shared slope, against the two-parameter model, with a "
            "slope for each item. <bookmark mark='c'/> The likelihood ratio is about half a point on four degrees of "
            "freedom. The extra slopes buy nothing here. <bookmark mark='d'/> And look where the curves sit. The items "
            "are easy, so this test sorts weak candidates well, and strong ones hardly at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(rc), Create(tc))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
