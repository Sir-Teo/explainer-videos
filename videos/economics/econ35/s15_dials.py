from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ35.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the gains from trade", r"How much richer is a country for trading?",
             "Chapter thirteen. The Dials: the gains from trade.",
             lit={2005: r"Bernhofen and Brown; \ Irwin", 2012: r"Arkolakis, \ Costinot and Rodr\'iguez-Clare"},
             scale=("nation",), horizon=("a decade",))
        self.formula()
        self.gains()
        self.fact()

    def formula(self):
        D = load("dials")
        eq = MathTex(r"\text{loss from autarky} = 1 - \lambda^{1/\varepsilon}", font_size=46, color=WHITE).move_to(
            UP * 1.6)
        rows = VGroup(
            label(r"$\lambda$: \ the share of spending on goods made at home", font_size=24, color=ISLAND),
            label(r"$\varepsilon$: \ the trade elasticity, \ how strongly trade responds to costs \ (5 to 10)",
                  font_size=22, color=ARCH),
            label(rf"America, \ {D['year']}: \ imports {100 * D['import_share']:.0f}\% of GDP, \ so $\lambda$ about "
                  rf"{D['lambda']:.2f}", font_size=23, color=USA),
            label(rf"loss from autarky: \ {100 * D['gain10']:.1f}\% \ ($\varepsilon$ = 10) \ to "
                  rf"{100 * D['gain5']:.1f}\% "
                  r"\ ($\varepsilon$ = 5)", font_size=24, color=GAIN),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Arkolakis, \ Costinot and Rodr\'iguez-Clare, \ \emph{AER} 102(1) (2012); \ BEA, \ "
                            r"via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "How large are the gains from trade for a country today? In 2012 Costas Arkolakis, Arnaud Costinot and "
            "Andres Rodriguez-Clare showed that in a whole family of models, the answer needs only two numbers. "
            "<bookmark mark='a'/> The share of spending that goes on goods made at home, <bookmark mark='b'/> and "
            "the trade elasticity, how strongly trade responds to its costs, which gravity studies put between five "
            f"and ten. <bookmark mark='c'/> For America in {D['year']}, imports were {100 * D['import_share']:.0f} "
            f"percent of GDP, so roughly {D['lambda']:.2f} of spending stayed at home. <bookmark mark='d'/> Moving to "
            f"autarky would cost between {100 * D['gain10']:.1f} and {100 * D['gain5']:.1f} percent of real income. "
            "This is rough, since GDP is not total spending; the authors' own figure, from a domestic share of "
            f"{D['acr_lambda']:.2f}, was {100 * D['acr10']:.1f} to {100 * D['acr5']:.1f} percent."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def gains(self):
        dial = dials.DIALS["gains_from_trade"]
        head = status_head(dial, r"the gains from trade \ (new)")
        frame, rows = dial_rows(dial, 0, 10, [0, 2, 4, 6, 8, 10], r"percent of real income", top=2.1, step=0.62,
                                fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(
            "That opens a new dial: the gains from trade. <bookmark mark='a'/> Japan's opening in 1859, by "
            "Bernhofen and Brown's upper bound: eight or nine percent of GDP. <bookmark mark='b'/> America's "
            "embargo of 1807, by Irwin's estimate: about five percent. <bookmark mark='c'/> America around 2000, "
            "by the formula: under one and a half percent. <bookmark mark='d'/> And this part's rough update for "
            "today. <bookmark mark='z'/> The status: depends on the setting. Static gains from comparative advantage "
            "are a few percent of income; the models of Part thirty-six, with many sectors, intermediate goods and "
            "firms that differ, raise them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def fact(self):
        F = load("facts")
        f = next(x for x in facts.FACTS if x.key == "intra_industry")
        data_m = VGroup(*[label(rf"{tex_safe(k)}: \ {v['gl']:.2f}", font_size=18, color=WHITE)
                          for k, v in F.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        puzzle_m = label(r"Ricardo, \ Heckscher \\ and Ohlin predict \\ trade in \emph{different} \\ goods",
                         font_size=18,
                         color=TARIFF)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data: \ America, \ 2025", data_m),
                                                         (r"the theories so far", puzzle_m), (r"Agora", None)),
                       width=12.4, font_size=22, colors=(WHITE, TARIFF, None)).move_to(UP * 0.4)
        foot = label(r"Grubel-Lloyd index: \ 1 when exports equal imports, \ 0 when trade runs one way", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = data_tag(r"BEA, \ NIPA table 4.2.5, \ via FRED; \ Grubel and Lloyd (1975)", corner=DR, font_size=12)
        cg, cars = F["capital goods"], F["cars and parts"]
        with self.voiceover(
            "One of the series' facts begins here, as a puzzle. <bookmark mark='a'/> Rich countries mostly trade "
            "similar goods with each other. In 2025 America exported "
            f"{cg['x']:.0f} billion dollars of capital goods and imported {cg['m']:.0f} billion; the Grubel-Lloyd "
            f"index of two-way trade is {cg['gl']:.2f}. In 1967, two years after its auto pact with Canada, its car "
            f"trade scored {cars['gl1967']:.2f}. <bookmark mark='b'/> Nothing in this part explains that: Ricardo "
            "and Heckscher and Ohlin predict trade in different goods, between countries that differ. "
            "<bookmark mark='c'/> Agora's column is empty until Part thirty-six."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc.head), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(Indicate(fc.slots[2], color=E.AGORA))
        self.clear_scene()
