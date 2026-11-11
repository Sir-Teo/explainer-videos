from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PM_C


class Culture(VoiceoverScene):
    def construct(self):
        self.card()
        self.thorp_simons()
        self.shaw_griffin()
        self.js_millennium()
        self.next_gen()
        self.patterns()
        self.culture()
        self.question()

    def card(self):
        c = chapter_card(9, r"Founding stories, as told in public", r"What do the firms' own histories have in common?",
                         part=PART)
        self.add(c)
        with self.voiceover("Chapter nine. The founding stories of quant firms are retold so often that they have become "
                            "a genre. Here they are as the founders and their biographers have told them in public, and "
                            "what they have in common."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _two(self, a, b):
        return VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)

    def thorp_simons(self):
        cards = self._two(
            firm_card(r"Edward Thorp", r"a mathematics professor who published \textit{Beat the Dealer} (1962) on card "
                      r"counting and \textit{Beat the Market} (1967) on hedging warrants, then ran Princeton/Newport "
                      r"Partners from 1969 on the same mathematics, as he tells it in \textit{A Man for All Markets}",
                      width=6.2, font_size=20),
            firm_card(r"James Simons", r"a geometer, a codebreaker at the Institute for Defense Analyses and chair of "
                      r"mathematics at Stony Brook, who started trading in 1978 and named the firm Renaissance in 1982; "
                      r"it hired mathematicians, physicists and speech-recognition researchers, not traders", width=6.2,
                      font_size=20))
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Two mathematicians. <bookmark mark='a'/> Edward Thorp published a book on beating blackjack in 1962 and one "
            "on hedging warrants in 1967, then ran a fund on the same mathematics, as he tells it in his memoir. "
            "<bookmark mark='b'/> James Simons, a geometer and former codebreaker who chaired the mathematics department "
            "at Stony Brook, started trading in 1978 and named his firm Renaissance in 1982. It hired mathematicians, "
            "physicists and speech-recognition researchers, and, famously, almost no one from Wall Street."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def shaw_griffin(self):
        cards = self._two(
            firm_card(r"David Shaw", r"a Columbia computer scientist who worked on parallel machines, joined Morgan "
                      r"Stanley's quantitative group in 1986, and founded D. E. Shaw in 1988; the firm describes itself as "
                      r"a computational one, and Shaw later founded a computational biochemistry lab, D. E. Shaw Research", width=6.2, font_size=20),
            firm_card(r"Kenneth Griffin", r"traded convertible bonds from his university dormitory from 1987, as widely "
                      r"reported, and founded Citadel in 1990; its market-making arm, Citadel Securities, followed in "
                      r"2002", width=6.2, font_size=20))
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Two founders from computing and from trading. <bookmark mark='a'/> David Shaw, a computer scientist from "
            "Columbia who worked on parallel machines, joined Morgan Stanley's quantitative group in 1986 and founded "
            "his own firm two years later. <bookmark mark='b'/> Kenneth Griffin traded convertible bonds from his "
            "university dormitory from 1987, as widely reported, founded Citadel in 1990, and added the market maker "
            "Citadel Securities in 2002."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def js_millennium(self):
        cards = self._two(
            firm_card(r"Jane Street", r"founded in 2000 by a small group of traders, several from Susquehanna "
                      r"International Group, as reported; it grew as a market maker in exchange-traded funds and is known "
                      r"for hiring by puzzles and for OCaml (Chapter 6)", width=6.2, font_size=20),
            firm_card(r"Millennium", r"founded by Israel Englander in 1989, as reported with about \$35 million; it grew "
                      r"into the platform model of Chapter 3, with hundreds of teams under one risk desk", width=6.2,
                      font_size=20))
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "And two that defined business models. <bookmark mark='a'/> Jane Street was founded in 2000 by a small group "
            "of traders, several from Susquehanna International Group, as reported, and grew as a market maker in "
            "exchange-traded funds. <bookmark mark='b'/> Millennium was founded by Israel Englander in 1989, as reported "
            "with about thirty-five million dollars, and grew into Chapter three's platform."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def next_gen(self):
        cards = self._two(
            firm_card(r"AQR", r"founded in 1998 by Clifford Asness and colleagues from Goldman Sachs Asset Management, as "
                      r"reported; it built its business on publishing its research, the factor and trend series used in "
                      r"Parts 24 and 32 among it", width=6.2, font_size=20),
            firm_card(r"Two Sigma", r"founded in 2001 by John Overdeck, who had worked at D. E. Shaw, and David Siegel, a "
                      r"computer scientist, as reported; it describes itself as a technology company applied to "
                      r"investment", width=6.2, font_size=20))
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "And the next generation, founded by alumni. <bookmark mark='a'/> AQR, founded in 1998 by Clifford Asness and "
            "colleagues from Goldman Sachs's asset management arm, built its business partly on publishing research: "
            "the factor and trend series this series used in Parts twenty-four and thirty-two are theirs. "
            "<bookmark mark='b'/> Two Sigma was founded in 2001 by John Overdeck, a D. E. Shaw alumnus, and David "
            "Siegel, a computer scientist, as reported. Each generation of firms was founded by the last one's "
            "employees."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def patterns(self):
        rows = [cmath(r"\text{a method from outside finance}", r":", r"\text{probability, coding theory, parallel computing}",
                      font_size=28, colors={r"\text{a method from outside finance}": FIRM_C}),
                cmath(r"\text{a market that was slow}", r":", r"\text{warrants, convertibles, ETFs, pairs}", font_size=30,
                      colors={r"\text{a market that was slow}": FIRM_C}),
                cmath(r"\text{survivorship}", r":", r"\text{we hear the stories of the firms that lasted}", font_size=30,
                      colors={r"\text{survivorship}": BAD})]
        whys = [why(r"each founder brought a tool from another field to a market that did not yet use it"),
                why(r"and found a corner where prices were set slowly or by rule of thumb: the edge was the gap"),
                why(r"Part 26 applies to founders too: the many firms that tried the same and closed do not write "
                    r"memoirs")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "What the stories share. <bookmark mark='a'/> A method from outside finance: probability, coding theory, "
            "parallel computing. <bookmark mark='b'/> A market that was slow: warrants, convertibles, exchange-traded "
            "funds, pairs, where prices were set by rule of thumb. <bookmark mark='c'/> And survivorship: we hear the "
            "stories of the firms that lasted. The many that tried the same and closed do not write memoirs, which is "
            "Part twenty-six's lesson applied to founders."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def culture(self):
        cards = VGroup(
            desk_question(r"collaboration over stars", r"several firms describe pooled research and shared pay as a "
                          r"defence against secrecy between teams; platforms choose the opposite, independent pods",
                          width=12.4, font_size=26),
            desk_question(r"secrecy and its cost", r"strategies leak with people, so firms guard both; the cost is that "
                          r"almost nothing they learn is published, and the academic record lags the industry",
                          width=12.4, font_size=26),
            desk_question(r"the same incentives as anyone", r"the pressure to show a good backtest is the same inside a "
                          r"firm as in a paper; the defence is the review of Chapter 4, not virtue", width=12.4,
                          font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "And culture. <bookmark mark='a'/> Some firms describe pooled research and shared pay as their defence "
            "against secrecy between teams; the platforms choose the opposite, independent pods. "
            "<bookmark mark='b'/> Strategies leak with people, so firms guard both, and the cost is that almost nothing "
            "they learn is published. <bookmark mark='c'/> And the pressure to show a good backtest is the same inside a "
            "firm as in a journal. The defence is Chapter four's review, not virtue."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Use the stated assumptions; derive the result and check its units and denominator.')
        working = MathTex('\\mathbb E[N_{10}]=\\sum_{i=1}^{1000}\\Pr(i\\text{ survives 10 years}),\\quad p_{10}=(1/2)^{10}', font_size=32).move_to(UP*0.9)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Independent annual survival within each firm. Cross-firm independence is unnecessary for the expectation, but needed for a binomial survivor count.', 11.7, 23).move_to(DOWN*0.8)
        self.add(working, setup_note, q)
        with self.voiceover('Pause and predict. A thousand hypothetical firms each survive each year with probability one half, independently across years. What is the expected number surviving ten years? Does that guarantee one survivor or prove the survivors had skill?'):
            self.wait(0.5)
        self.wait(0.5)
        self.clear_scene()
