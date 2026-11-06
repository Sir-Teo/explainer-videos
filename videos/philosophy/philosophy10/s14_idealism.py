from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Idealism(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Things in themselves", r"What is the world like apart from us?", lit=(1781,),
                            part=PART)
        with self.voiceover("Chapter thirteen. Things in themselves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.price()
        self.faith()
        self.readings()

    def price(self):
        head = label(r"Transcendental idealism", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        def col(title, tcol, lines):
            g = VGroup(label(title, font_size=28, color=tcol))
            for t, c in lines:
                g.add(label(t, font_size=23, color=c))
            for m in g:
                if m.width > 6.2:
                    m.width = 6.2
            return g.arrange(DOWN, buff=0.16)
        left = col(r"appearances", KANT, [(r"things as they are given to us:", GREY_A),
                                          (r"in space and time, \ under the categories", GREY_A),
                                          (r"here we have necessary knowledge:", OK),
                                          (r"geometry, \ arithmetic, \ causation", OK)])
        right = col(r"things in themselves", GREY_B, [(r"things as they are", GREY_A),
                                                      (r"apart from how they appear", GREY_A),
                                                      (r"here we know nothing at all:", BAD),
                                                      (r"not even whether they are in space", BAD)])
        cols = VGroup(left, right).arrange(RIGHT, buff=1.2).move_to([0, 1.0, 0])
        eye = VGroup(Circle(radius=0.32, color=KANT, stroke_width=2.5),
                     Dot(radius=0.12, color=KANT)).move_to([left.get_x(), -0.9, 0])
        lens = Rectangle(width=0.9, height=0.9, color=GREY_B, stroke_width=2).next_to(eye, RIGHT, buff=0.35)
        lens_l = label(r"space, \ time, \ categories", font_size=18, color=GREY_B).next_to(lens, DOWN, buff=0.12)
        thing = Square(side_length=0.8, color=GREY_D, fill_color=GREY_D, fill_opacity=0.3).move_to(
            [right.get_x(), -0.9, 0])
        qmark = label(r"?", font_size=34, color=GREY_B).move_to(thing)
        rays = VGroup(*[DashedLine(thing.get_left() + UP * dy, lens.get_right() + UP * dy * 0.6, color=GREY_D,
                                   stroke_width=1.5) for dy in (-0.25, 0, 0.25)])
        rays2 = VGroup(*[Line(lens.get_left() + UP * dy * 0.6, eye.get_right() + UP * dy * 0.3, color=KANT,
                              stroke_width=2) for dy in (-0.25, 0, 0.25)])
        pic = VGroup(eye, lens, lens_l, thing, qmark, rays, rays2)
        foot = VGroup(label(r"the price of necessary knowledge: \ it is knowledge of appearances only", font_size=26,
                            color=GOAL),
                      label(r"empirically real, \ transcendentally ideal", font_size=24, color=KANT)).arrange(
            DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Kant's solution has a price, and he paid it openly. <bookmark mark='a'/>We know a priori what we "
            "ourselves contribute to experience. So our necessary knowledge, of geometry, arithmetic and causation, "
            "holds of things as they appear to us: in space and time, and under the categories. "
            "<bookmark mark='b'/>Of things as they are in themselves, apart from how they appear, we know nothing at "
            "all, not even whether they are in space or time. <bookmark mark='c'/>Necessary knowledge is knowledge of "
            "appearances only. Space and time, Kant said, are empirically real, since everything we meet is in them, "
            "and transcendentally ideal, since they belong to the form of our experience, not to things in "
            "themselves."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            self.play(FadeIn(eye), FadeIn(lens), FadeIn(lens_l), Create(rays2))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(thing), FadeIn(qmark), Create(rays))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def faith(self):
        q = quote_card(r"Thus I had to deny knowledge in order to make room for faith.", r"Immanuel Kant",
                       r"\textit{Critique of Pure Reason}, \ B xxx", width=8.8, font_size=30).move_to([0, 1.8, 0])
        rows = VGroup(
            label(r"God, \ freedom, \ immortality: \ beyond any possible experience", font_size=24),
            label(r"so they can be neither proved nor disproved \ (the antinomies, \ the failed proofs of God)",
                  font_size=22, color=GREY_A),
            label(r"freedom, \ impossible in nature, \ is possible for things in themselves", font_size=24,
                  color=KANT),
            label(r"and morality requires it: \ the \textit{Critique of Practical Reason} \ (1788; \ Part 35)",
                  font_size=22, color=OK)).arrange(DOWN, buff=0.3).move_to([0, -1.2, 0])
        with self.voiceover(
            "Kant saw an advantage in the price. <bookmark mark='a'/>Thus I had to deny knowledge, he wrote, in order "
            "to make room for faith. <bookmark mark='b'/>God, freedom and the immortal soul lie beyond any possible "
            "experience. So they can be neither proved nor disproved: the antinomies, and Kant's refutations of the "
            "traditional proofs of God, show reason failing in both directions. <bookmark mark='c'/>Freedom is "
            "impossible within nature, where every event has a cause, but it is not impossible for things in "
            "themselves. <bookmark mark='d'/>And morality, Kant argued in his second Critique, requires that we think "
            "of ourselves as free. Part 35 takes up his ethics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def readings(self):
        head = label(r"Two readings", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        def col(title, tcol, lines):
            g = VGroup(label(title, font_size=28, color=tcol))
            for t, c, fs in lines:
                g.add(label(t, font_size=fs, color=c))
            for m in g:
                if m.width > 6.2:
                    m.width = 6.2
            return g.arrange(DOWN, buff=0.16)
        two = VGroup(
            col(r"two worlds", GREY_B, [(r"appearances and things in themselves", WHITE, 23),
                                        (r"are two sets of objects", WHITE, 23),
                                        (r"the table I see is a mental representation,", GREY_A, 21),
                                        (r"caused by an unknowable thing", GREY_A, 21),
                                        (r"Strawson, \textit{The Bounds of Sense} (1966): \ incoherent", BAD, 21)]),
            col(r"two aspects", KANT, [(r"one set of objects,", WHITE, 23),
                                       (r"considered in two ways", WHITE, 23),
                                       (r"the table as it appears to us,", GREY_A, 21),
                                       (r"and the same table considered apart from that", GREY_A, 21),
                                       (r"Allison, \textit{Kant's Transcendental Idealism} (1983)", OK, 21)])
        ).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = VGroup(label(r"a third: \ Langton, \textit{Kantian Humility} (1998)", font_size=24, color=GOAL),
                      label(r"we know things' relations and powers, \ never their intrinsic natures", font_size=23,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Scholars still argue about what Kant meant. <bookmark mark='a'/>On the two-world reading, appearances "
            "and things in themselves are two different sets of objects: the table I see is a representation in my "
            "mind, caused by an unknowable thing beyond it. Peter Strawson, in 1966, found this incoherent: we could "
            "not even say that unknowable things cause anything. <bookmark mark='b'/>On the two-aspect reading, "
            "defended by Henry Allison, there is one set of objects, considered in two ways: the table as it appears "
            "to us, and the same table considered apart from the conditions of our experience. <bookmark mark='c'/>"
            "Rae Langton proposed a third: we know things only by their relations and powers, never their intrinsic "
            "natures. Kantian humility."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(two[0]))
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
