from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403



def raven(size=0.3) -> VMobject:
    """A dark bird silhouette: body, head and beak."""
    body = Ellipse(width=size * 2.0, height=size * 1.0, stroke_color=GREY_B, stroke_width=1.5, fill_color=RAVEN,
                   fill_opacity=1)
    head = Circle(radius=size * 0.32, stroke_color=GREY_B, stroke_width=1.5, fill_color=RAVEN,
                  fill_opacity=1).move_to(body.get_right() + UP * size * 0.35 + LEFT * size * 0.15)
    beak = Polygon(head.get_right() + UP * size * 0.06, head.get_right() + DOWN * size * 0.08,
                   head.get_right() + RIGHT * size * 0.35, stroke_width=0, fill_color=GREY_B, fill_opacity=1)
    tail = Polygon(body.get_left() + UP * size * 0.15, body.get_left() + DOWN * size * 0.15,
                   body.get_left() + LEFT * size * 0.5 + UP * size * 0.25, stroke_width=0, fill_color=RAVEN,
                   fill_opacity=1)
    return VGroup(tail, body, head, beak)


def shoe(size=0.3) -> VMobject:
    pts = [LEFT * 1.0 + DOWN * 0.4, RIGHT * 1.1 + DOWN * 0.4, RIGHT * 1.1 + UP * 0.0, RIGHT * 0.2 + UP * 0.15,
           LEFT * 0.2 + UP * 0.6, LEFT * 1.0 + UP * 0.6]
    return Polygon(*[p * size for p in pts], stroke_color=GREY_B, stroke_width=1.5, fill_color=WHITE,
                   fill_opacity=0.95)


class Ravens(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The ravens", r"Does a white shoe confirm that all ravens are black?", lit=(1945,),
                            part=PART)
        with self.voiceover("Chapter four. The ravens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradox()
        self.price()
        self.bayes()

    def paradox(self):
        hc = history_card(1945, r"Carl Hempel", r"`Studies in the Logic of Confirmation'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        h = MathTex(r"H:\ \forall x\,(Rx \to Bx)", font_size=38, color=FUT)
        hc2 = MathTex(r"\equiv\ \forall x\,(\lnot Bx \to \lnot Rx)", font_size=38, color=FUT)
        hh = VGroup(h, hc2).arrange(RIGHT, buff=0.3).next_to(hc, DOWN, buff=0.45).set_x(0)
        r1 = VGroup(raven(0.35), label(r"a black raven: \ an instance of $H$", font_size=23, color=OK)).arrange(
            RIGHT, buff=0.4)
        r2 = VGroup(shoe(0.3), label(r"a white shoe: \ an instance of the equivalent", font_size=23,
                                     color=PAST)).arrange(RIGHT, buff=0.4)
        rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(hh, DOWN, buff=0.5).set_x(-0.5)
        foot = stack([(r"so a white shoe confirms that all ravens are black", BAD),
                      (r"indoor ornithology", GREY_A)], font_size=25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1945 Carl Hempel found a paradox at the heart of confirmation. <bookmark mark='a'/>Take the "
            "hypothesis that all ravens are black: for everything, if it is a raven, it is black. "
            "<bookmark mark='b'/>A black raven is an instance of it, and surely confirms it. <bookmark mark='c'/>But "
            "the hypothesis is logically equivalent to its contrapositive: everything that is not black is not a "
            "raven. <bookmark mark='d'/>And a white shoe is an instance of that. <bookmark mark='e'/>So, it seems, a "
            "white shoe confirms that all ravens are black, and you can do ornithology without leaving the house."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(h))
            vo.wait_until("b")
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(Write(hc2))
            vo.wait_until("d")
            self.play(FadeIn(r2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def price(self):
        d = load("ravens")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["R1"], ["R2"], ["R3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.8, font_size=22,
                       center=[0, -0.5, 0], title=r"The Price List: \ the ravens")
        positions = [(("R1",), r"Good \ (1967)", r"a black raven can \textit{dis}confirm: \ it depends on what "
                                                r"else you believe about the world"),
                     (("R2",), r"Scheffler, \ Goodman", r"confirmation is selective: \ not closed under "
                                                       r"equivalence"),
                     (("R3",), r"Hempel; \ the Bayesians", r"the shoe does confirm, \ by a tiny amount: \ "
                                                          r"intuition is misled by background knowledge")]
        with self.voiceover(
            "Hempel's paradox is a Price List. <bookmark mark='a'/>Three principles: Nicod's criterion, that an "
            "instance confirms a generalization; the equivalence condition, that what confirms a claim confirms its "
            "logical equivalents; and the conviction that a white shoe does not confirm anything about ravens. "
            "<bookmark mark='b'/>Together they are inconsistent, and dropping any one restores consistency. "
            "<bookmark mark='c'/>I. J. Good dropped the first. He described a world in which seeing a black raven "
            "should lower your confidence that all ravens are black, because of what else you believe about how many "
            "ravens there are. <bookmark mark='d'/>Israel Scheffler and Nelson Goodman dropped the second: "
            "confirmation, they said, is selective, and does not pass across equivalences. <bookmark mark='e'/>Hempel "
            "himself, and most Bayesians, drop the third. The shoe does confirm, but by an amount so small that "
            "intuition rounds it to zero."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def bayes(self):
        d = load("ravens")["bayes"]
        head = label(r"How tiny? \ The Bayesian accounting", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        setup = stack([(r"$10^8$ objects; \ $10^4$ ravens; \ 90\% of things are not black", WHITE),
                       (r"$H$: \ all ravens are black \ \ vs \ \ $H'$: \ 100 ravens are white", GREY_A)],
                      font_size=22).next_to(head, DOWN, buff=0.3)
        # two jars: the ravens, and the non-black things
        jar_a = RoundedRectangle(width=3.0, height=3.0, corner_radius=0.2, stroke_color=GREY_B, stroke_width=2)
        jar_b = RoundedRectangle(width=3.0, height=3.0, corner_radius=0.2, stroke_color=GREY_B, stroke_width=2)
        jars = VGroup(jar_a, jar_b).arrange(RIGHT, buff=3.2).move_to([0, -0.9, 0])
        dots_a = VGroup(*[Dot(radius=0.07, color=RAVEN if k else WHITE, stroke_width=1, stroke_color=GREY_B)
                          for k in [0] + [1] * 99]).arrange_in_grid(10, 10, buff=0.16).move_to(jar_a)
        dots_b = VGroup(*[Dot(radius=0.03, color=GREY_C) for _ in range(900)]).arrange_in_grid(30, 30,
                                                                                              buff=0.03).move_to(jar_b)
        la = label(r"draw a raven: \ under $H'$, \ 1 in 100 is white", font_size=20, color=OK).next_to(jar_a, DOWN,
                                                                                                       buff=0.2)
        lb = label(r"draw a non-black thing: \ 1 in 900{,}000 a white raven", font_size=20, color=PAST).next_to(
            jar_b, DOWN, buff=0.2)
        ta = label(r"the ravens", font_size=21, color=GREY_A).next_to(jar_a, UP, buff=0.12)
        tb = label(r"the non-black things", font_size=21, color=GREY_A).next_to(jar_b, UP, buff=0.12)
        bf = MathTex(r"\frac{P(E\mid H)}{P(E\mid H')}", font_size=34, color=GOAL).move_to([0, -0.4, 0])
        va = MathTex(r"\text{raven: }" + f"{d['bayes_factor_raven']:.4f}", font_size=30, color=OK).next_to(bf, DOWN, buff=0.3).shift(
            LEFT * 0.0)
        vb = MathTex(r"\text{shoe: }" + f"{d['bayes_factor_shoe']:.7f}", font_size=30, color=PAST).next_to(va, DOWN, buff=0.2)
        ratio = d["rise_raven"] / d["rise_shoe"]
        foot = stack([
            (r"posterior of $H$ rises by " + f"{d['rise_raven']:.4f}" + r" \ for the raven, \ by " +
             f"{d['rise_shoe'] * 1e7:.1f}" + r"$\times 10^{-7}$ for the shoe", WHITE),
            (r"the raven is worth about " + f"{round(ratio, -2):,.0f}".replace(",", "{,}") + r" shoes: \ both "
             r"confirm, \ by wildly different amounts", GOAL),
        ], font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How tiny is tiny? Here is the Bayesian accounting, after Good, Mackie, and Branden Fitelson and James "
            "Hawthorne. <bookmark mark='a'/>Imagine a hundred million objects, ten thousand of them ravens, and "
            "ninety percent of everything not black. Compare H, all ravens are black, with a rival H prime, on which "
            "a hundred ravens are white. <bookmark mark='b'/>Pick a raven at random. Under H prime, one in a hundred "
            "ravens is white, so finding it black is a real test. <bookmark mark='c'/>Pick a non-black thing at "
            "random. Under H prime, only one in nine hundred thousand of them is a white raven, so finding a shoe "
            "is almost no test at all. <bookmark mark='d'/>The Bayes factor, the ratio of the likelihoods, measures "
            "the evidence: one point zero one for the raven; one point zero zero zero zero zero one for the shoe. "
            "<bookmark mark='e'/>Both confirm. The raven is worth about nine thousand shoes. The paradox dissolves "
            "into a difference of degree, if you accept that a white shoe confirms at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(Create(jar_a), FadeIn(ta), LaggedStart(*[FadeIn(x) for x in dots_a], lag_ratio=0.01),
                      run_time=1.5)
            self.play(FadeIn(la), Indicate(dots_a[0], color=WHITE, scale_factor=2.0))
            vo.wait_until("c")
            self.play(Create(jar_b), FadeIn(tb), FadeIn(dots_b), run_time=1.5)
            self.play(FadeIn(lb))
            vo.wait_until("d")
            self.play(FadeIn(bf))
            self.play(FadeIn(va, shift=LEFT * 0.3), FadeIn(vb, shift=RIGHT * 0.3))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
