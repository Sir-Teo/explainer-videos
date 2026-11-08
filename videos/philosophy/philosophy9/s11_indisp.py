from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Indisp(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Indispensable?", r"Does science commit us to numbers?", lit=(1948, 2005), part=PART)
        with self.voiceover("Chapter ten. Indispensable?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.cicadas()
        self.objections()

    def argument(self):
        hcs = VGroup(history_card(1948, r"W.\ V.\ O.\ Quine", r"`On what there is'", width=4.2, color=HIST),
                     history_card(1971, r"Hilary Putnam", r"\textit{Philosophy of Logic}", width=4.2, color=HIST),
                     history_card(2001, r"Mark Colyvan", r"\textit{The Indispensability of Mathematics}", width=4.6,
                                  color=HIST)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        prem = VGroup(
            label(r"1. \ we ought to believe in all and only the entities \ indispensable to our best scientific "
                  r"theories", font_size=24),
            label(r"2. \ mathematical entities are indispensable to them: \ physics quantifies over numbers, "
                  r"functions, spaces", font_size=24),
            label(r"3. \ so we ought to believe in mathematical entities", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        sup = VGroup(label(r"naturalism: \ science is our best guide to what there is", font_size=22, color=GREY_A),
                     label(r"holism: \ theories face the evidence as wholes, \ mathematics included \ (Parts 11 and 15)",
                           font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The strongest argument for platonism comes from science. <bookmark mark='a'/>Its sources are Quine's "
            "'On what there is', of 1948, and Putnam's Philosophy of Logic, of 1971; Mark Colyvan gave it its "
            "standard form. <bookmark mark='b'/>One: we ought to believe in all and only the entities that are "
            "indispensable to our best scientific theories. Two: mathematical entities are indispensable to them, "
            "since physics cannot be stated without numbers, functions and spaces. Three: so we ought to believe in "
            "mathematical entities. <bookmark mark='c'/>Behind it stand two Quinean views. Naturalism: science is our "
            "best guide to what exists. And holism: theories meet the evidence as wholes, so the mathematics in a "
            "confirmed theory is confirmed with it. Parts 11 and 15 return to that idea."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in prem], lag_ratio=0.7), run_time=6)
            vo.wait_until("c")
            self.play(FadeIn(sup))
        self.clear_scene()

    def cicadas(self):
        d = load("cicadas")["rows"]
        hc = history_card(2005, r"Alan Baker", r"`Are there genuine mathematical explanations of physical "
                          r"phenomena?'", width=5.6, color=HIST).to_corner(UL, buff=0.3)
        bars = VGroup()
        vmax = max(r["overlap"] for r in d)
        H = 3.6
        base_y = -2.5
        for k, r in enumerate(d):
            h = H * r["overlap"] / vmax
            col = OK if r["prime"] else GREY_C
            b = Rectangle(width=0.42, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-6.0 + 0.56 * k, base_y + h / 2, 0])
            lab = MathTex(str(r["cycle"]), font_size=24, color=OK if r["prime"] else GREY_A).next_to(b, DOWN,
                                                                                                    buff=0.12)
            bars.add(VGroup(b, lab))
        xl = label(r"years between emergences", font_size=20, color=GREY_B).next_to(bars, DOWN, buff=0.15)
        yl = label(r"how often an emergence meets a predator's peak \ (predators every 2 to 9 years)",
                   font_size=20, color=GREY_B).next_to(bars, UP, buff=0.25)
        best = sorted([r for r in d if 12 <= r["cycle"] <= 18], key=lambda r: r["overlap"])[:2]
        assert sorted(r["cycle"] for r in best) == [13, 17]
        side = VGroup(label(r"periodical cicadas: \ 13 or 17 years underground", font_size=22, color=CONCRETE),
                      label(r"the Reasoner: \ sum of $1/\mathrm{lcm}(c, p)$ \ over predator periods $p$", font_size=20,
                            color=GREY_A),
                      label(r"the primes are the low points; \ between 12 and 18, \ 13 and 17", font_size=22,
                            color=OK),
                      label(r"the explanation is mathematical: \ \textit{because 13 and 17 are prime}",
                            font_size=22, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(
            [3.6, -0.4, 0])
        with self.voiceover(
            "Alan Baker gave the argument a sharper form in 2005, with an example from biology. <bookmark mark='a'/>"
            "Periodical cicadas spend thirteen or seventeen years underground, then emerge all at once. Why those "
            "numbers? <bookmark mark='b'/>Suppose predators boom on cycles of two to nine years. The Reasoner works "
            "out, for each cycle length from ten to twenty, how often an emergence coincides with a predator's peak. "
            "<bookmark mark='c'/>The prime cycles are the low points, because a prime shares no factor with a shorter "
            "cycle. Among cycles from twelve to eighteen years, the two lowest are thirteen and seventeen: exactly "
            "the cicadas'. <bookmark mark='d'/>The explanation is mathematical: the cicadas do well because thirteen "
            "and seventeen are prime. If mathematics does real explaining in science, Baker argued, it earns the "
            "same belief as electrons."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(yl), FadeIn(xl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                      FadeIn(side[1]), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def objections(self):
        head = label(r"Three objections", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        cards = VGroup(*[VGroup(label(a, font_size=26, color=c), label(b, font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.15) for a, b, c in (
            (r"Maddy (1992): \ practice", r"chemists used atoms for a century, \ yet doubted them until Perrin (1908); "
             r"\ frictionless planes are indispensable, \ and believed by nobody", CONCRETE),
            (r"Sober (1993): \ no test", r"mathematics is never the hypothesis at risk: \ no experiment \ chooses "
             r"between arithmetics", NUM),
            (r"Melia (2000): \ weaseling", r"use the mathematics, \ then take it back: \ `and nothing I said about "
             r"numbers is literally true'", ABSTRACT))]).arrange(DOWN, buff=0.45).move_to([0, -0.2, 0])
        for c in cards:
            if c.width > 12.5:
                c.width = 12.5
        moral = label(r"or show the mathematics can be removed: \ Field's project, \ next", font_size=24,
                      color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There are three main objections. <bookmark mark='a'/>Penelope Maddy pointed to practice. Chemists used "
            "atoms for a century while doubting they existed, until Jean Perrin's experiments of 1908. And "
            "frictionless planes are indispensable to mechanics, though nobody believes in them. Indispensability "
            "is not the scientists' own test of existence. <bookmark mark='b'/>Elliott Sober noted that mathematics "
            "is never the hypothesis at risk: no experiment chooses between rival arithmetics, so it is not "
            "confirmed the way electrons are. <bookmark mark='c'/>Joseph Melia proposed weaseling: use the "
            "mathematics, then take back its existential claims. <bookmark mark='d'/>Or, most ambitious, show that "
            "the mathematics can be removed from science altogether. That was Hartry Field's project."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
