from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Fundamentals(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Geography, \ disease and culture", r"Are institutions the deepest cause, \ or do geography, "
             r"disease and culture rival them?", "Chapter eleven. Geography, disease and culture.",
             lit={1997: r"Guns, Germs, and Steel", 2011: r"Nunn and Wantchekon", 2015: r"Alsan"},
             scale=("nation", "world"), horizon=("a century",))
        self.rivals()
        self.verdict()

    def rivals(self):
        cards = point_cards([
            (r"geography", r"Jared Diamond: \ Eurasia's east--west axis \\ let crops and animals spread; \\ Sachs: "
                           r"tropics and distance from the sea", "#D4A373"),
            (r"disease", r"Marcella Alsan: \ where the tsetse fly \\ thrived, \ Africans kept fewer animals, \\ "
                         r"ploughed less, \ lived less densely", MORT),
            (r"culture", r"Nathan Nunn and Leonard Wantchekon: \\ descendants of groups raided hardest \\ by the slave "
                         r"trades trust less today", RESEARCH),
            (r"institutions", r"Acemoglu, \ Johnson and Robinson; \\ Rodrik, \ Subramanian and Trebbi \\ (2004): "
                              r"``institutions rule''", INST),
        ], width=12.6, cols=2, font_size=21).move_to(DOWN * 0.15)
        head = label(r"four fundamental causes, \ each with its best evidence", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = published_tag(r"Diamond (1997); \ Gallup, Sachs and Mellinger (1999); \ Alsan, AER 105(1) (2015); \ "
                            r"Nunn and Wantchekon, AER 101(7) (2011); \ Rodrik et al., JEG 9(2) (2004)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "Institutions are not the only candidate for the deepest cause. <bookmark mark='a'/> Geography: Jared "
            "Diamond argued that Eurasia's long east-west axis let crops and animals spread across similar "
            "climates, and Jeffrey Sachs and his co-authors that tropical climates and distance from the sea hold "
            "countries back. <bookmark mark='b'/> Disease: Marcella Alsan showed that where the tsetse fly thrived "
            "in Africa, people kept fewer domesticated animals, used the plough less, and lived less densely before "
            "colonization. <bookmark mark='c'/> Culture: Nathan Nunn and Leonard Wantchekon found that people whose "
            "ancestors' groups were raided hardest by the slave trades trust their neighbours and local officials "
            "less today. <bookmark mark='d'/> And institutions, which Dani Rodrik, Arvind Subramanian and Francesco "
            "Trebbi, in a horse race against geography and trade, declared the winner: institutions rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def verdict(self):
        rows = VGroup(
            label(r"the causes are entangled", font_size=30, color=E.ACCENT),
            label(r"disease shaped where settlers went, \ and so institutions", font_size=23, color=MORT),
            label(r"the slave trades shaped trust, \ and trust shapes institutions", font_size=23, color=RESEARCH),
            label(r"geography shaped which crops and animals, \ and so early states", font_size=23, color="#D4A373"),
            label(r"a horse race between them needs instruments for each, \ and those are hard to find", font_size=23,
                  color=HOLD),
            label(r"Part 47 \ (political economy) \ returns to institutions; \ Part 46 \ (development) \ to poverty",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "The honest verdict is that the causes are entangled. <bookmark mark='a'/> Disease decided where "
            "settlers went, and so which institutions they built. <bookmark mark='b'/> The slave trades shaped "
            "trust, and trust shapes institutions. <bookmark mark='c'/> Geography decided which crops and animals "
            "were at hand, and so where the first states rose. <bookmark mark='d'/> A horse race between them needs "
            "a separate instrument for each, and good instruments are scarce. <bookmark mark='e'/> Part forty-seven "
            "comes back to institutions and how they change, and part forty-six to what can be done about poverty "
            "within a generation."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
