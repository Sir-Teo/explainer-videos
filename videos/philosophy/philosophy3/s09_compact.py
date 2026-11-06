from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Compact(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Compactness and the infinite", r"Can first-order logic say `finite'?", lit=(1934,),
                            part=PART)
        with self.voiceover("Chapter eight. Compactness and the infinite."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.statement()
        self.ladder()
        self.finite()
        self.nonstandard()
        self.robinson()

    def statement(self):
        thm = theorem_card(r"Compactness", r"a set of sentences has a model \ if and only if \ every finite part of "
                           r"it has a model", who=r"Gödel 1930 (countable case); Mal'tsev 1936", width=8.6,
                           font_size=26).move_to([0, 1.5, 0])
        pf = VGroup(label(r"why: \ if the whole set had no model, it would be inconsistent (completeness);",
                          font_size=24, color=GREY_A),
                    label(r"the proof of the contradiction is finite, \ so it uses only finitely many sentences;",
                          font_size=24, color=GREY_A),
                    label(r"those few already have no model.", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -0.8, 0])
        with self.voiceover(
            "The first consequence of completeness sounds harmless. <bookmark mark='a'/>A set of sentences, even an "
            "infinite set, has a model if and only if every finite part of it has a model. "
            "<bookmark mark='b'/>The proof is one line. If the whole set had no model, completeness says a "
            "contradiction could be proved from it. A proof is finite, so it uses only finitely many of the "
            "sentences, and those few already have no model. <bookmark mark='c'/>This is the compactness theorem, "
            "and it is the most-used tool in model theory. It is also where first-order logic starts to look strange."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pf], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(Indicate(thm, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def ladder(self):
        d = load("compact")
        lam = VGroup(
            MathTex(r"\lambda_2 \;=\; \exists x_1\, \exists x_2\ (x_1 \neq x_2)", font_size=32),
            MathTex(r"\lambda_3 \;=\; \exists x_1\, \exists x_2\, \exists x_3\ (x_1 \neq x_2 \land x_1 \neq x_3 \land "
                    r"x_2 \neq x_3)", font_size=32),
            label(r"$\lambda_n$: \ `there are at least $n$ things'", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.4)
        hd = [label(r"size", font_size=22, color=P.CLAIM)] + [MathTex(str(k), font_size=26, color=OBJ)
                                                              for k in d["sizes"]]
        rows = [[MathTex(rf"\lambda_{{{n + 1}}}", font_size=26)] + list(r) for n, r in enumerate(d["grid"])]
        grid = ValueGrid(hd, rows, col_w=[1.2] + [0.8] * len(d["sizes"]), font_size=24).move_to([-2.4, -1.2, 0])
        right = VGroup(label(r"each finite set of them: \ a finite model", font_size=24, color=OK),
                       label(r"all of them together: \ only infinite models", font_size=24, color=BAD),
                       label(r"so `infinitely many' takes infinitely many sentences", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(grid, RIGHT, buff=0.8)
        with self.voiceover(
            "First, counting again. <bookmark mark='a'/>For each number n there is a sentence lambda n that says "
            "there are at least n things. <bookmark mark='b'/>The Reasoner checked the first five on structures of "
            "sizes one to six: lambda n is true exactly in the structures with at least n objects. "
            "<bookmark mark='c'/>Any finite collection of these sentences has a finite model: just take enough "
            "objects. <bookmark mark='d'/>All of them together say 'there are infinitely many things', and have "
            "only infinite models. One sentence cannot say it, but infinitely many can."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(lam[0]), Write(lam[1]), FadeIn(lam[2]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            self.play(LaggedStart(*[FadeIn(grid.row(r)) for r in range(len(rows))], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(right[0]))
            vo.wait_until("d")
            self.play(FadeIn(right[1]), FadeIn(right[2]))
        self.clear_scene()

    def finite(self):
        head = label(r"Theorem: \ no set of first-order sentences is true in exactly the finite structures",
                     font_size=28, color=CONN).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"suppose $\Phi$ were: \ true in every finite structure, false in every infinite one",
                  font_size=26),
            MathTex(r"\Phi \ \cup\ \{\lambda_2, \lambda_3, \lambda_4, \dots\}", font_size=40, color=GOAL),
            label(r"every finite part has a model: \ a finite structure big enough for its largest $\lambda_n$",
                  font_size=24, color=OK),
            label(r"so, by compactness, the whole set has a model: \ infinite, \ yet a model of $\Phi$",
                  font_size=24, color=BAD),
            label(r"contradiction: \ `finite' cannot be said", font_size=28, color=BAD)).arrange(DOWN, buff=0.35)
        steps.next_to(head, DOWN, buff=0.5)
        also = label(r"nor `connected', \ `well-ordered', \ `the natural numbers and nothing else'", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now the strange part. <bookmark mark='a'/>Suppose some sentences, call them Phi, were true in exactly "
            "the finite structures. <bookmark mark='b'/>Add to Phi every lambda n. <bookmark mark='c'/>Each finite "
            "part of this set has a model: a finite structure big enough for the largest lambda in it. "
            "<bookmark mark='d'/>So by compactness the whole set has a model. That model satisfies every lambda, so "
            "it is infinite, and it satisfies Phi, which was supposed to be true only in finite structures. "
            "<bookmark mark='e'/>Contradiction. First-order logic can say 'at least a million', but it cannot say "
            "'finitely many'. <bookmark mark='f'/>By the same trick it cannot say that a graph is connected, that an "
            "order has no infinite descending chains, or that the numbers are just zero, one, two, and so on."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=UP * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(also))
        self.clear_scene()

    def nonstandard(self):
        hc = history_card(1934, r"Thoralf Skolem", r"a model of arithmetic with numbers beyond all the natural numbers",
                          width=6.2, color=HIST).to_corner(UL, buff=0.35)
        th = VGroup(MathTex(r"\mathrm{Th}(\mathbb{N})", r"\ \cup\ ", r"\{\, c > 0,\ c > 1,\ c > 2,\ \dots \,\}",
                            font_size=38)).next_to(hc, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        th[0][2].set_color(GOAL)
        tl = label(r"every truth of arithmetic, \ plus a new constant $c$ bigger than each numeral", font_size=22,
                   color=GREY_A).next_to(th, DOWN, buff=0.12).align_to(th, LEFT)
        fin = label(r"each finite part: \ true in $\mathbb{N}$, with $c$ a big enough number", font_size=24,
                    color=OK).next_to(tl, DOWN, buff=0.25).align_to(th, LEFT)
        y = -1.4
        line = Line([-6.6, y, 0], [6.6, y, 0], color=GREY_C, stroke_width=2)
        std = VGroup(*[VGroup(Dot([-6.2 + 0.55 * i, y, 0], radius=0.06, color=OBJ),
                              MathTex(str(i), font_size=24, color=OBJ).move_to([-6.2 + 0.55 * i, y - 0.32, 0]))
                       for i in range(6)])
        dots = MathTex(r"\cdots", font_size=36, color=OBJ).move_to([-2.5, y + 0.05, 0])
        gal = VGroup()
        for cx, nm, js in ((0.4, "c", range(-2, 3)), (4.5, "2c", range(-1, 2))):
            g = VGroup()
            for j in js:
                x = cx + 0.72 * j
                lab = nm if j == 0 else (rf"{nm}{j:+d}")
                g.add(VGroup(Dot([x, y, 0], radius=0.06, color=GOAL),
                             MathTex(lab, font_size=20, color=GOAL).move_to([x, y - 0.32, 0])))
            half = 0.72 * (len(js) - 1) / 2 + 0.45
            g.add(MathTex(r"\cdots", font_size=30, color=GOAL).move_to([cx - half, y + 0.05, 0]),
                  MathTex(r"\cdots", font_size=30, color=GOAL).move_to([cx + half, y + 0.05, 0]))
            gal.add(g)
        sl = label(r"the standard numbers", font_size=22, color=OBJ).move_to([-4.8, y + 0.55, 0])
        nl = label(r"nonstandard numbers: \ each one inside a copy of the integers", font_size=22,
                   color=GOAL).move_to([2.4, y + 0.55, 0])
        order = label(r"a countable nonstandard model is ordered like \ $\mathbb{N}$ \ followed by \ "
                      r"$\mathbb{Q}$ copies of $\mathbb{Z}$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The most famous application is to arithmetic. <bookmark mark='a'/>Take every sentence that is true of "
            "the natural numbers, and add a new name c, with the sentences: c is greater than zero, c is greater "
            "than one, c is greater than two, and so on forever. <bookmark mark='b'/>Any finite part of this set is "
            "true in the ordinary numbers: just let c be a number bigger than the finitely many numerals mentioned. "
            "<bookmark mark='c'/>So by compactness the whole set has a model. It satisfies every truth of "
            "arithmetic, and yet it contains c, a number bigger than zero, one, two, and every other standard "
            "number. <bookmark mark='d'/>Since it obeys the laws of arithmetic, c has a predecessor and a successor, "
            "and c plus c is bigger still. Each nonstandard number lives in its own copy of the integers, infinitely "
            "far out. <bookmark mark='e'/>Thoralf Skolem built such a model directly in 1934. Every countable "
            "nonstandard model is ordered in the same way: the natural numbers, then densely many copies of the "
            "integers, arranged like the rationals. No first-order theory can rule them out."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(th), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(fin))
            self.play(Create(line), LaggedStart(*[FadeIn(s) for s in std], lag_ratio=0.15), FadeIn(dots),
                      FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(gal[0][2], scale=1.5), FadeIn(nl))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*[gal[0][i] for i in (0, 1, 3, 4, 5, 6)])))
            self.play(FadeIn(gal[1]))
            vo.wait_until("e")
            self.play(FadeIn(order))
        self.clear_scene()

    def robinson(self):
        hc = history_card(1961, r"Abraham Robinson", r"nonstandard analysis: \ infinitesimals made rigorous",
                          width=6.0, color=HIST).to_corner(UL, buff=0.4)
        eps = VGroup(MathTex(r"\varepsilon = \frac{1}{c}", font_size=48, color=GOAL),
                     label(r"positive, \ yet smaller than $1, \frac12, \frac13, \dots$", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.2).move_to([3.0, 1.2, 0])
        der = MathTex(r"f'(x) \;=\; \mathrm{st}\!\left(\frac{f(x + \varepsilon) - f(x)}{\varepsilon}\right)",
                      font_size=40).move_to([0, -0.6, 0])
        ex = MathTex(r"\frac{(x+\varepsilon)^2 - x^2}{\varepsilon} = 2x + \varepsilon \ \ \xrightarrow{\ \mathrm{st}\ }"
                     r"\ \ 2x", font_size=36, color=OK).next_to(der, DOWN, buff=0.4)
        lb = label(r"Leibniz's infinitesimals (Part 1), \ banished by Berkeley's `ghosts of departed quantities' "
                   r"(1734), \ return", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Compactness also rescued an old idea. <bookmark mark='a'/>In 1961 Abraham Robinson applied the same "
            "construction to the real numbers. If c is infinitely large, then epsilon, one over c, is positive and "
            "yet smaller than every ordinary fraction: an infinitesimal. <bookmark mark='b'/>With it, the derivative "
            "becomes what Leibniz said it was: the difference quotient with an infinitesimal step, rounded to the "
            "nearest real number. <bookmark mark='c'/>For x squared, the quotient is two x plus epsilon, and "
            "rounding gives two x. <bookmark mark='d'/>Bishop Berkeley mocked Leibniz's infinitesimals in 1734 as "
            "the ghosts of departed quantities. Two hundred years later, logic proved them consistent."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(eps))
            vo.wait_until("b")
            self.play(Write(der))
            vo.wait_until("c")
            self.play(Write(ex))
            vo.wait_until("d")
            self.play(FadeIn(lb))
        self.clear_scene()
