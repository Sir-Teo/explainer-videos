from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Allais(VoiceoverScene):
    def construct(self):
        self.card()
        self.problems()
        self.triangle()
        self.reversals()

    def card(self):
        card = chapter_card(2, r"The violations", r"Do people obey the independence axiom?",
                            lit={1953: r"Allais", 1971: r"Lichtenstein \& Slovic", 1979: r"Kahneman \& Tversky",
                                 1982: r"Machina"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter two. The violations."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _choice(self, name, lot, pct_, col):
        box = RoundedRectangle(corner_radius=0.1, width=5.4, height=1.15, stroke_color=col, stroke_width=2,
                               fill_color=BLACK, fill_opacity=0.5)
        t = label(rf"{name}: \ {lot}", font_size=23, color=col)
        p = label(rf"{pct_}\%", font_size=30, color=WHITE)
        g = VGroup(box, t.move_to(box).shift(LEFT * 0.45), p.next_to(box.get_right(), LEFT, buff=0.25))
        return g

    def problems(self):
        d = load("allais")
        head = heading(r"Allais's paradox, \ as Kahneman and Tversky asked it")
        pr = d["pct"]
        p1 = VGroup(label(r"Problem 1", font_size=24, color=GREY_A),
                    self._choice("A", r"2{,}500 at .33, \ 2{,}400 at .66, \ 0 at .01", pr["A"], RISKY),
                    self._choice("B", r"2{,}400 for sure", pr["B"], SURE)).arrange(DOWN, buff=0.22)
        p2 = VGroup(label(r"Problem 2", font_size=24, color=GREY_A),
                    self._choice("C", r"2{,}500 at .33, \ 0 at .67", pr["C"], RISKY),
                    self._choice("D", r"2{,}400 at .34, \ 0 at .66", pr["D"], SURE)).arrange(DOWN, buff=0.22)
        VGroup(p1, p2).arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"Problem 2 is Problem 1 with a 0.66 chance of 2{,}400 taken out of both options", WHITE),
            (r"by independence, \ B over A must mean D over C; \ most people choose B, \ and then C", LOSS),
            (r"the certainty effect: \ a sure thing is worth more than its probability says", NORM),
        ], 11.8, 25, 0.3).move_to([0, -2.1, 0])
        tag = published_tag(rf"Kahneman \& Tversky (1979), \ Problems 1 and 2, \ $N = {d['n']}$")
        assert d["pt_pair1"] == "B" and d["pt_pair2"] == "C"
        with self.voiceover(
            "In 1953 Maurice Allais posed a pair of choices that breaks the independence axiom. Here is the version "
            "Kahneman and Tversky asked in Israeli pounds in 1979. <bookmark mark='a'/> Problem one: A gives two "
            "thousand five hundred with probability point three three, two thousand four hundred with point six six, "
            f"and nothing with point zero one. B gives two thousand four hundred for sure. {pr['B']} percent of "
            f"{d['n']} people chose B. <bookmark mark='b'/> Problem two: C gives two thousand five hundred with point "
            f"three three, otherwise nothing; D gives two thousand four hundred with point three four. {pr['C']} "
            "percent chose C. <bookmark mark='c'/> Now look closely. Problem two is problem one with a point six six "
            "chance of two thousand four hundred removed from both options. <bookmark mark='d'/> That's exactly the "
            "common part that the independence axiom says can't matter. So anyone who prefers B to A must prefer D "
            "to C, and most people do the opposite. <bookmark mark='e'/> Kahneman and Tversky called it the "
            "certainty effect: a sure thing is weighted more than its probability says it should be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(p1[0]), FadeIn(p1[1]), FadeIn(p1[2]))
            vo.wait_until("b")
            self.play(FadeIn(p2[0]), FadeIn(p2[1]), FadeIn(p2[2]))
            for m, r in zip("cde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def triangle(self):
        d = load("allais")
        head = heading(r"The probability triangle")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$p_1$: \ chance of 0",
                 ylabel=r"$p_3$: \ chance of 2{,}500", center=[-3.2, -0.35, 0], font_size=16)
        ax = A.ax
        tri = Polygon(ax.c2p(0, 0), ax.c2p(1, 0), ax.c2p(0, 1), stroke_color=GREY_B, stroke_width=2,
                      fill_color=GREY_E, fill_opacity=0.35)
        corner = label(r"2{,}400 for sure", font_size=16, color=SURE).next_to(ax.c2p(0, 0), LEFT, buff=0.32)
        s = d["slope"]
        lines = VGroup()
        for c0 in np.linspace(-1.8, 0.9, 10):
            # p3 = c0 + s p1, clipped to the triangle
            p1s = np.linspace(0, 1, 400)
            p3s = c0 + s * p1s
            ok = (p3s >= 0) & (p3s <= 1 - p1s)
            if ok.sum() > 1:
                lines.add(Line(ax.c2p(p1s[ok][0], p3s[ok][0]), ax.c2p(p1s[ok][-1], p3s[ok][-1]), color=NORM,
                               stroke_width=1.5, stroke_opacity=0.6))
        pts = d["pts"]
        dots = VGroup()
        for k, col in zip("ABCD", (RISKY, SURE, RISKY, SURE)):
            p = Dot(ax.c2p(*pts[k]), radius=0.08, color=col)
            lab_ = label(k, font_size=22, color=col).next_to(p, UR if k in "AC" else DR, buff=0.06)
            dots.add(VGroup(p, lab_))
        ab = Arrow(ax.c2p(*pts["B"]), ax.c2p(*pts["A"]), buff=0.08, color=RISKY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12)
        cd = Arrow(ax.c2p(*pts["D"]), ax.c2p(*pts["C"]), buff=0.08, color=RISKY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12)
        rows = rows_of([
            (r"Marschak, \ 1950; \ Machina, \ 1982: \ any lottery over three outcomes is a point in the triangle",
             WHITE),
            (r"expected utility's indifference lines are straight and parallel, \ whatever the utility: \ that is "
             r"the independence axiom, \ drawn", NORM),
            (r"B to A and D to C are the same step: \ one more chance in a hundred of 0, \ 33 more of 2{,}500", RISKY),
            (r"parallel steps across parallel lines: \ both better, \ or both worse; \ never B and C", LOSS),
            (r"people's curves fan out: \ steep near certainty, \ flatter far from it; \ prospect theory, \ with "
             r"Tversky and Kahneman's 1992 values, \ chooses B and C", MODEL),
        ], 6.3, 22, 0.27).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{choice.triangle}, \ \texttt{eu\_slope}, \ \texttt{cpt}")
        with self.voiceover(
            "There's a picture that makes the paradox visible. <bookmark mark='a'/> With three outcomes, nothing, "
            "two thousand four hundred and two thousand five hundred, any lottery is fixed by two numbers: the "
            "chance of the worst and the chance of the best. So every lottery is a point in this triangle, an idea "
            "of Jacob Marschak's that Mark Machina made famous. The bottom-left corner is two thousand four hundred "
            "for sure. <bookmark mark='b'/> For anyone who maximizes expected utility, the indifference curves are "
            "straight, parallel lines, whatever the utility function. The slope depends on the utility; the "
            "parallelism doesn't. That is the independence axiom, drawn. <bookmark mark='c'/> Here are the four "
            "options. Going from B to A is exactly the same step as going from D to C: one more chance in a hundred "
            "of nothing, thirty-three more of the top prize. <bookmark mark='d'/> A step that crosses parallel "
            "lines the same way at both places is either an improvement at both or a loss at both. Choosing B and C "
            "is impossible. <bookmark mark='e'/> What people show instead is curves that fan out: steep near "
            "certainty, where any risk is resisted, and flatter in the interior. Prospect theory, with the values "
            "Tversky and Kahneman published in 1992, computes exactly the popular pair: B, then C."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(tri))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(corner))
            vo.wait_until("b")
            self.play(Create(lines), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(rows[2]))
            self.play(GrowArrow(ab), GrowArrow(cd))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def reversals(self):
        head = heading(r"Preference reversals")
        def bet(name, txt, col):
            box = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.4, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            g = VGroup(label(name, font_size=26, color=col), label(txt, font_size=22, color=WHITE)).arrange(
                DOWN, buff=0.15).move_to(box)
            return VGroup(box, g)
        pb = bet(r"the P-bet", r"a high chance of a small win", SURE)
        db = bet(r"the \$-bet", r"a small chance of a large win", RISKY)
        VGroup(pb, db).arrange(RIGHT, buff=1.4).move_to([0, 1.3, 0])
        choose = VGroup(label(r"asked to choose:", font_size=24, color=GREY_A),
                        label(r"most take the P-bet", font_size=26, color=SURE)).arrange(DOWN, buff=0.12)
        price = VGroup(label(r"asked to name a selling price:", font_size=24, color=GREY_A),
                       label(r"most price the \$-bet higher", font_size=26, color=RISKY)).arrange(DOWN, buff=0.12)
        VGroup(choose, price).arrange(RIGHT, buff=1.6).move_to([0, -0.4, 0])
        rows = rows_of([
            (r"Lichtenstein and Slovic, \ 1971; \ Grether and Plott, \ 1979, \ economists who set out to make it go "
             r"away, \ with real money, \ and could not", WHITE),
            (r"no single ranking of the two bets gives both answers: \ preference depends on how it is asked", LOSS),
            (r"prospect theory does not explain this one; \ the usual account is compatibility: \ a price draws "
             r"attention to the dollars, \ a choice to the chances", MODEL),
        ], 12.0, 24, 0.3).move_to([0, -2.4, 0])
        tag = published_tag(r"Lichtenstein \& Slovic (1971); \ Grether \& Plott (1979); \ Tversky, \ Slovic \& "
                            r"Kahneman (1990)")
        with self.voiceover(
            "A second violation goes deeper, because it threatens the idea that a preference is a single ranking "
            "at all. <bookmark mark='a'/> Take two bets with similar expected values. The P-bet has a high chance of "
            "a small win; the dollar-bet a small chance of a large one. <bookmark mark='b'/> Asked to choose "
            "between them, most people take the P-bet. Asked what price they'd sell each for, most put the higher "
            "price on the dollar-bet. <bookmark mark='c'/> Sarah Lichtenstein and Paul Slovic reported this in 1971. "
            "In 1979 two economists, David Grether and Charles Plott, set out to show it was an artefact, with real "
            "money and careful incentives, and found it just the same. <bookmark mark='d'/> No single ranking of the "
            "two bets produces both answers. What you prefer depends on how you're asked. <bookmark mark='e'/> And "
            "prospect theory doesn't explain this one. The usual account, from Tversky, Slovic and Kahneman in 1990, "
            "is compatibility: naming a price draws attention to the money, and choosing draws it to the chances."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pb), FadeIn(db))
            vo.wait_until("b")
            self.play(FadeIn(choose))
            self.play(FadeIn(price))
            for m, r in zip("cde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
