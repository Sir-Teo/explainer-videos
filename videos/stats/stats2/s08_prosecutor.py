from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

INNOCENT = S.KEPT
GUILTY = S.RESID


class Prosecutor(VoiceoverScene):
    def construct(self):
        self.card()
        self.case()
        self.squared()
        self.transposed()
        self.compare()
        self.aftermath()

    def card(self):
        card = chapter_card(7, r"The prosecutor's fallacy", r"The chance of the evidence is not the chance of guilt",
                            lit=(1763,), part=PART)
        with self.voiceover("Chapter seven. The prosecutor's fallacy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def case(self):
        d = load("clark")
        hc = history_card(1999, r"\emph{R v Clark}, \ Chester Crown Court", r"Sally Clark, a solicitor, was tried "
                          r"for the murder of her two baby sons, \ who had died suddenly in 1996 and 1998. \ She was "
                          r"convicted in November 1999.", color=S.MUSEUM, width=6.6, font_size=24).move_to([-3.2, 1.3, 0])
        testimony = VGroup(
            label(r"expert testimony for the prosecution:", font_size=26, color=GREY_A),
            MathTex(r"P(\text{one cot death}) \approx \dfrac{1}{8{,}543}", font_size=34),
            label(r"for an affluent, non-smoking family", font_size=22, color=GREY_B),
            MathTex(r"P(\text{two}) \approx \left(\dfrac{1}{8{,}543}\right)^2", r"=", r"\dfrac{1}{73\ \text{million}}",
                    font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -1.3, 0])
        testimony[3][2].set_color(GUILTY)
        src = historical_tag(r"the trial record; \ the Royal Statistical Society, 2001; \ Hill (2004)")
        with self.voiceover(
            "Bayes' theorem has been tested in court, and the results have not always been just. This chapter is "
            "about a real case, and a real person, so we'll keep to the published record. <bookmark mark='a'/> In "
            "1999 Sally Clark, a solicitor in Cheshire, was tried for murder. Her first son had died suddenly in 1996, "
            "aged eleven weeks; her second in 1998, aged eight weeks. <bookmark mark='b'/> A prominent paediatrician "
            "told the jury that the chance of a single sudden infant death, a cot death, in a family like hers was "
            f"about one in {money(d['one'])}. <bookmark mark='c'/> And so, he said, the chance of two was that "
            "number squared: about one in seventy-three million. She was convicted, by a majority of ten to two. "
            "<bookmark mark='d'/> There are two errors in that number, and they are worth understanding exactly."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(testimony[:3], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(Write(testimony[3]))
            vo.wait_until("d")
            self.play(Indicate(testimony[3], color=GUILTY, scale_factor=1.08))
        self.clear_scene()

    def squared(self):
        d = load("clark")
        rows = [
            cmath(r"P(\text{two})", r"=", r"P(\text{first})\, P(\text{second} \mid \text{first})", font_size=38),
            cmath(r"P(\text{two})", r"=", r"P(\text{first})\, P(\text{second})", font_size=38),
        ]
        whys = [why(r"the multiplication rule: \ always true"), why(r"only if the deaths are \emph{independent}")]
        title = label(r"Error 1: \ squaring", font_size=38, color=GUILTY).to_edge(UP, buff=0.45)
        shared = label(r"siblings share genes, \ a home, \ a way of sleeping", font_size=28, color=GREY_A)
        shared.move_to([0, -0.6, 0])
        dep = MathTex(r"P(\text{second} \mid \text{first})", r"\approx", r"(5 \text{ to } 10) \times \dfrac{1}{8{,}543}",
                      font_size=34).next_to(shared, DOWN, buff=0.4)
        lo, hi = d["square"] / 10 / 1e6, d["square"] / 5 / 1e6
        res = MathTex(rf"P(\text{{two}}) \approx \dfrac{{1}}{{{lo:.1f}\ \text{{million}}}} \text{{ to }} "
                      rf"\dfrac{{1}}{{{hi:.1f}\ \text{{million}}}}", font_size=34, color=EXACT).next_to(dep, DOWN, buff=0.35)
        src = note(r"the dependence factor: \ Hill (2004), \emph{Paediatric and Perinatal Epidemiology}").to_corner(DL,
                                                                                                         buff=0.3)
        with self.voiceover(
            "The first error is the squaring. <bookmark mark='a'/> The multiplication rule says the chance of two "
            "deaths is the chance of the first, times the chance of the second given the first. That's always true. "
            "<bookmark mark='b'/> Squaring replaces the conditional chance with the plain one: it assumes the deaths "
            "are independent, like two tosses of a coin. <bookmark mark='c'/> But two children in one family are not "
            "two coin tosses. They share genes, a home, a way of being put to sleep. Whatever raises the risk for one "
            "raises it for the other. <bookmark mark='d'/> The mathematician Ray Hill, analysing British data, "
            "estimated that after one cot death the chance of a second is five to ten times higher than for a family "
            "with none. <bookmark mark='e'/> That alone moves one in seventy-three million to somewhere between one "
            f"in {lo:.1f} and one in {hi:.1f} million. Still rare. But the second error is much bigger."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.6, buff=0.55)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(shared))
            vo.wait_until("d")
            self.play(Write(dep), FadeIn(src))
            vo.wait_until("e")
            self.play(Write(res))
        self.clear_scene()

    def transposed(self):
        title = label(r"Error 2: \ transposing the conditional", font_size=38, color=GUILTY).to_edge(UP, buff=0.45)
        a = cmath(r"P(", r"\text{two deaths}", r"\mid", r"\text{innocent}", r")", font_size=48)
        b = cmath(r"P(", r"\text{innocent}", r"\mid", r"\text{two deaths}", r")", font_size=48)
        a[1].set_color(GREY_A)
        a[3].set_color(INNOCENT)
        b[1].set_color(INNOCENT)
        b[3].set_color(GREY_A)
        a.move_to([0, 1.2, 0])
        b.move_to([0, -0.6, 0])
        neq = MathTex(r"\ne", font_size=60, color=GUILTY).move_to([0, 0.3, 0])
        al = label(r"what the number estimated", font_size=24, color=GREY_B).next_to(a, UP, buff=0.2)
        bl = label(r"what the jury had to decide", font_size=24, color=GREY_B).next_to(b, DOWN, buff=0.2)
        lot = VGroup(MathTex(r"P(\text{a given ticket wins} \mid \text{a fair draw}) = \dfrac{1}{13{,}983{,}816}",
                             font_size=30),
                     label(r"yet somebody wins most weeks, \ and nobody concludes the draw was rigged", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The second error is in what the number was taken to mean. <bookmark mark='a'/> One in seventy-three "
            "million was offered as the probability of two such deaths in a family where nothing criminal happened. "
            "<bookmark mark='b'/> It's easy to hear it as something else: the probability that she was innocent. "
            "Those two probabilities have the same ingredients in a different order, and they can be wildly "
            "different. <bookmark mark='c'/> Swapping them is called the prosecutor's fallacy. <bookmark mark='d'/> "
            "Here's the same mistake somewhere it's obvious. The chance that a given lottery ticket wins, in a fair "
            "draw, is one in fourteen million. Someone wins most weeks. Nobody concludes the draw was rigged, "
            "because the comparison that matters isn't with one, it's with the alternative: how likely is the "
            "evidence if the draw was rigged, and how likely was a rigged draw to begin with?"
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(Write(a), FadeIn(al))
            vo.wait_until("b")
            self.play(TransformMatchingTex(a.copy(), b, path_arc=PI / 2), FadeIn(bl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(neq, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(lot, shift=UP * 0.2))
        self.clear_scene()

    def compare(self):
        rows = [
            cmath(r"\frac{P(\text{innocent} \mid E)}{P(\text{guilty} \mid E)}", r"=",
                  r"\frac{P(\text{two SIDS})}{P(\text{two murders})}", r"\times", r"\frac{P(E \mid \text{innocent})}{P(E "
                  r"\mid \text{guilty})}", font_size=32),
        ]
        rows[0][0].set_color(S.POST)
        rows[0][2].set_color(S.PRIOR)
        rows[0][4].set_color(S.LIK)
        rows[0].move_to([0, 2.3, 0])
        lr = label(r"$E$: \ two babies died suddenly. \ Both explanations produce $E$, \ so the green ratio is about $1$",
                   font_size=24, color=S.LIK).next_to(rows[0], DOWN, buff=0.3)
        both = label(r"compare two rare events \emph{with each other}", font_size=30, color=S.ACCENT)
        both.next_to(lr, DOWN, buff=0.35)
        # natural frequencies: 100 families with two unexplained infant deaths, at Hill's two ratios
        arrays = VGroup()
        for ratio in (4.5, 9.0):
            k = int(round(100 * ratio / (1 + ratio)))
            arr = icon_array([INNOCENT] * k + [GUILTY] * (100 - k), cols=10, size=0.26, buff=0.05)
            cap = label(rf"ratio ${ratio:g} : 1$: \ {k} of 100 innocent", font_size=24, color=INNOCENT)
            arrays.add(VGroup(arr, cap.next_to(arr, DOWN, buff=0.2)))
        arrays.arrange(RIGHT, buff=2.0).move_to([0, -1.95, 0])
        head = label(r"of 100 families with two such deaths:", font_size=24, color=GREY_A).next_to(arrays, UP, buff=0.25)
        src = note(r"double SIDS $:$ double murder \ estimated at $4.5$ to $9 : 1$ \ (Hill 2004); \ schematic").to_corner(
            DR, buff=0.3)
        with self.voiceover(
            "Bayes' theorem in odds form says exactly what to compare. <bookmark mark='a'/> The odds of innocence "
            "against guilt, given the evidence, are the prior odds, how often two sudden infant deaths are natural "
            "compared with how often they are murders, times the likelihood ratio. <bookmark mark='b'/> Here the "
            "evidence is two sudden deaths, and both explanations produce it, so the likelihood ratio is about one. "
            "<bookmark mark='c'/> Everything rests on comparing two rare events with each other: a double cot "
            "death, and a double murder of babies by their mother, which is rarer still. <bookmark mark='d'/> Hill "
            "estimated that in families with two such deaths, double SIDS was between four and a half and nine "
            "times as likely as double murder. <bookmark mark='e'/> On those figures, of a hundred families like "
            "this, somewhere between eighty-two and ninety are innocent. Not one in seventy-three million: the "
            "statistics, read correctly, pointed the other way."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(lr))
            vo.wait_until("c")
            self.play(FadeIn(both, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(a[0], lag_ratio=0.01) for a in arrays], lag_ratio=0.4), run_time=2.0)
            self.play(*[FadeIn(a[1]) for a in arrays])
        self.clear_scene()

    def aftermath(self):
        items = VGroup(
            label(r"October 2001: \ the Royal Statistical Society says the figure has ``no statistical basis''",
                  font_size=26),
            VGroup(label(r"January 2003: \ the convictions are quashed on a second appeal,", font_size=26),
                   label(r"chiefly because medical evidence pointing to a natural death had not been disclosed",
                         font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            label(r"other convictions resting on similar testimony are reviewed; \ several are overturned",
                  font_size=26),
            label(r"Sally Clark died in 2007, \ aged 42", font_size=26, color=GREY_A),
        )
        for it in items:
            if it.width > 12.6:
                it.width = 12.6
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.9, 0])
        rule = MathTex(r"P(E \mid H)", r"\ne", r"P(H \mid E)", font_size=50).to_edge(DOWN, buff=1.2)
        rule[1].set_color(GUILTY)
        mirror = label(r"its mirror image, the \emph{defence attorney's fallacy}, \ ignores weak evidence that adds "
                       r"up: \ I. J. Good on the Simpson trial (1995)", font_size=22, color=GREY_B)
        mirror.to_edge(DOWN, buff=0.4)
        if mirror.width > 13:
            mirror.width = 13
        with self.voiceover(
            "<bookmark mark='a'/> In October 2001 the Royal Statistical Society took the unusual step of issuing a "
            "public statement: the figure of one in seventy-three million, it said, had no statistical basis, and "
            "the reasoning behind it was a well-known fallacy. <bookmark mark='b'/> In January 2003, on a second "
            "appeal, Sally Clark's convictions were quashed, chiefly because medical evidence suggesting that her "
            "second son had died of natural causes had not been disclosed at her trial. <bookmark mark='c'/> Other "
            "convictions resting on similar testimony were reviewed, and several were overturned. "
            "<bookmark mark='d'/> Sally Clark had spent more than three years in prison. She died in 2007, aged "
            "forty-two. <bookmark mark='e'/> The lesson is a single line. The probability of the evidence given a "
            "hypothesis is not the probability of the hypothesis given the evidence. <bookmark mark='f'/> And the "
            "fallacy has a mirror image, the defence attorney's: dismissing evidence because each piece of it is "
            "weak on its own, when together it is strong. Both are the same failure to do Bayes' theorem."
        ) as vo:
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(items[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(Write(rule))
            vo.wait_until("f")
            self.play(FadeIn(mirror))
        self.clear_scene()
