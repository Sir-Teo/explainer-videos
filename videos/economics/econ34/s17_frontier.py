from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ who sets exchange rates?", r"If not fundamentals, what moves currencies?",
             "Chapter fifteen. Frontier: who sets exchange rates?",
             lit={2015: r"Gabaix and Maggiori", 2021: r"Itskhoki and Mukhin"}, scale=("market", "world"),
             horizon=("a day", "a decade"))
        self.intermediaries()
        self.questions()

    def intermediaries(self):
        cards = point_cards([
            (r"financiers with limited balance sheets", r"Gabaix and Maggiori (2015): \\ currencies are priced by \\ "
                                                        r"intermediaries who must be \\ paid to hold the risk", USD),
            (r"the disconnect", r"Itskhoki and Mukhin (2021): \\ a shock in financial markets, \\ not in goods, \\ "
                                r"explains why rates are \\ volatile and disconnected", GBP),
            (r"convenience", r"dollar bonds pay less \\ because they are useful: \\ the convenience yield \\ that "
                             r"moves the dollar", DEM),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"the exchange-rate disconnect: \ rates move a lot, \ and not with output, \ prices or money",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Gabaix and Maggiori, \ \emph{QJE} 130(3) (2015); \ Itskhoki and Mukhin, \ \emph{JPE} "
                            r"129(8) (2021)", corner=DR, font_size=12)
        with self.voiceover(
            "This part's evidence adds up to a puzzle with a name: the exchange-rate disconnect. Exchange rates move "
            "a lot, and their moves have little to do with output, prices or money. The frontier looks for what "
            "moves them in finance. <bookmark mark='a'/> Xavier Gabaix and Matteo Maggiori model currencies as "
            "priced by financiers whose balance sheets are limited, who must be paid to hold currency risk; when "
            "their capacity shrinks, exchange rates move with no change in fundamentals. <bookmark mark='b'/> Oleg "
            "Itskhoki and Dmitry Mukhin show that a single shock in financial markets, rather than in goods markets, "
            "reproduces the random walk, the forward premium puzzle and the slow return to parity all at once. "
            "<bookmark mark='c'/> And a growing literature traces the dollar's moves to the convenience of dollar "
            "assets, which investors accept lower returns to hold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"how long the dollar's dominance lasts, \ and what could replace it", font_size=22, color=USD),
            label(r"whether floating insulates anyone from the global financial cycle", font_size=22, color=CRISIS),
            label(r"when capital controls and reserves are the right tools", font_size=22, color=RES),
            label(r"what makes a currency union last: \ the euro's unfinished design", font_size=22, color=DEM),
            label(r"why parity returns so slowly", font_size=22, color=GBP),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.2)
        tag = published_tag(r"Rey (2013); \ Gopinath et al.\ (2020); \ Itskhoki and Mukhin (2021)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> How long the dollar's dominance lasts, and what could replace "
            "it. <bookmark mark='b'/> Whether a floating exchange rate insulates anyone from the global financial "
            "cycle. <bookmark mark='c'/> When capital controls and large reserves are the right tools. "
            "<bookmark mark='d'/> What makes a currency union last, with the euro's design still unfinished. "
            "<bookmark mark='e'/> And why parity returns so slowly."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
