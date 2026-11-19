from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 12, r"In practice: \ forecasting the long run", r"Who forecasts population and growth decades "
             r"ahead, \ and how badly can it go wrong?", "Chapter twelve. In practice: forecasting the long run.",
             lit={1968: r"The Population Bomb", 1980: r"the Simon--Ehrlich wager", 2024: r"the UN's projection"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.called()
        self.wager()
        self.today()

    def called(self):
        c = calls.CALLS["ehrlich"]
        e = load("ehrlich")
        cc = call_card(r"Paul Ehrlich, \ \emph{The Population Bomb}", c.when,
                       r"the battle to feed all of humanity is over: \ in the 1970s hundreds of millions will starve "
                       r"to death",
                       rf"the world's population passed {e['pop_2022'] / 1e9:.0f} billion in 2022 and food per person "
                       r"rose; \ the famines since, \ terrible as they were, \ killed far fewer, \ and most were made "
                       r"by war and policy",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.5)
        q = label(r"Malthus's arithmetic, \ applied just as fertility began to fall and yields to soar",
                  font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Ehrlich (1968), \ prologue; \ UN, \emph{World Population Prospects}", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1968, with the world's population at about "
            f"{e['pop_1968'] / 1e9:.1f} billion and growing by about {100 * e['growth_1968']:.0f} percent a year, the "
            "biologist Paul Ehrlich opened The Population Bomb with a prediction: the battle to feed all of "
            "humanity is over, and in the 1970s hundreds of millions of people will starve to death. "
            f"<bookmark mark='b'/> The world's population passed {e['pop_2022'] / 1e9:.0f} billion in 2022, and food "
            "per person rose. The famines since, terrible as they were, killed far fewer, and most were made by war "
            "and policy rather than by a world short of food. <bookmark mark='c'/> Wrong. It was Malthus's "
            "arithmetic, applied just as fertility began to fall and crop yields began to soar."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()

    def wager(self):
        rows = VGroup(
            label(r"1980: \ the economist Julian Simon offers a bet", font_size=25),
            label(r"Ehrlich and two colleagues choose five metals: \ chromium, \ copper, \ nickel, \ tin, \ tungsten",
                  font_size=22, color=GREY_A),
            label(r"\$1{,}000 of them, \ at 1980 prices: \ dearer in 1990, \ after inflation?", font_size=23,
                  color=WAGE),
            label(r"all five fell; \ in 1990 Ehrlich mailed Simon a cheque for \$576.07", font_size=23, color=GDP),
            label(r"economists later found that over many other decades \ Ehrlich would have won", font_size=21,
                  color=HOLD),
            label(r"the lesson: \ prices call forth substitutes and new supplies, \ but not on a timetable",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Tierney, \emph{New York Times Magazine}, 2 December 1990", corner=DR, font_size=13)
        with self.voiceover(
            "The economists answered with a bet. <bookmark mark='a'/> In 1980 Julian Simon offered one, and Ehrlich "
            "accepted. <bookmark mark='b'/> Ehrlich and two colleagues chose five metals: chromium, copper, nickel, "
            "tin and tungsten. <bookmark mark='c'/> They notionally bought a thousand dollars' worth at 1980 prices. "
            "If, after inflation, the metals were dearer in 1990, Ehrlich would win. <bookmark mark='d'/> All five "
            "fell, and in 1990 Ehrlich mailed Simon a cheque for five hundred and seventy-six dollars and seven "
            "cents. <bookmark mark='e'/> Economists later found that over many other decades Ehrlich would have "
            "won: metal prices swing with booms and busts. <bookmark mark='f'/> The lesson is not that scarcity "
            "never bites, but that prices call forth substitutes and new supplies, on no fixed timetable."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        cards = point_cards([
            (r"the UN", r"world population to peak near \\ 10.3 billion in the mid-2080s", POP),
            (r"already past peak", r"63 countries, \ including China, \\ Germany, \ Japan, \ Russia", DEATH),
            (r"pensions and budgets", r"projections fifty years out \\ drive public finance", WAGE),
            (r"climate models", r"population and income paths \\ are their inputs: \ part 48", TECH),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"forecasting the long run today", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"the transition, \ not the bomb, \ is now the central forecast", font_size=23,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"UN DESA, \emph{World Population Prospects 2024}", corner=DR, font_size=13)
        with self.voiceover(
            "Long-run forecasting is now routine work. <bookmark mark='a'/> The United Nations' projections of 2024 "
            "have the world's population peaking at about 10.3 billion in the mid-2080s, then slowly declining. "
            "<bookmark mark='b'/> Sixty-three countries are already past their peak, among them China, Germany, "
            "Japan and Russia. <bookmark mark='c'/> Treasuries and pension funds plan on projections fifty years "
            "out, <bookmark mark='d'/> and climate models take paths of population and income as their inputs, as "
            "part forty-eight shows. <bookmark mark='e'/> The demographic transition, not the bomb, is now the "
            "central forecast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
