from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ testing Ricardo in the fields", r"Can we see comparative advantage directly?",
             "Chapter fifteen. Frontier: testing Ricardo in the fields.",
             lit={2002: r"Eaton and Kortum", 2012: r"Costinot and Donaldson"}, scale=("world",),
             horizon=("a year", "a decade"))
        self.fields()
        self.questions()

    def fields(self):
        CD = tables.COSTINOT_DONALDSON_2012.data
        cards = point_cards([
            (r"the problem", r"productivity is seen \\ only in goods \\ a country makes: \\ the rest are \\ "
                             r"counterfactual", WHITE),
            (r"the agronomists' answer", rf"an FAO model predicts \\ the yield of {CD['crops']} crops \\ on "
                                        rf"{CD['parcels'] / 1e6:.1f} million plots \\ in {CD['countries']} countries, "
                                        r"\\ grown or not", GAIN),
            (r"the test", rf"log output on \\ predicted output: \\ slope {CD['slope']:.2f}, \\ precisely estimated",
             CAPITAL),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"Costinot and Donaldson (2012): \ Ricardo, \ seen directly", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Costinot and Donaldson, \ \emph{AER P\&P} 102(3) (2012)", corner=DR, font_size=12)
        with self.voiceover(
            "Ricardo's theory is about productivity in goods a country does not make, which is why it is hard to "
            "test. <bookmark mark='a'/> You see how good Portugal is at wine, but not how good it would be at cloth "
            "if it tried. <bookmark mark='b'/> In agriculture, Arnaud Costinot and Dave Donaldson found a way "
            "round it. Agronomists at the Food and Agriculture Organization model how much of each crop any plot of "
            f"land could yield, given its soil and climate, whether or not the crop is grown there: "
            f"{CD['crops']} crops, {CD['parcels'] / 1e6:.1f} million plots, {CD['countries']} countries. "
            "<bookmark mark='c'/> Feed those productivities into a Ricardian model, predict what each country "
            f"should grow, and compare with what it does grow: the slope is {CD['slope']:.2f}, far from one but "
            "clearly positive. Comparative advantage, measured where it can be, has real explanatory power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"Eaton and Kortum (2002): \ Ricardo with many countries and random productivity, \ the engine of "
                  r"Part 36", font_size=21, color=GAIN),
            label(r"how large are the gains with many sectors and intermediate goods?", font_size=22,
                  color=CAPITAL),
            label(r"how fast does comparative advantage change, \ and can policy change it?", font_size=22,
                  color=ISLAND),
            label(r"who inside a country gains, \ and how long adjustment takes", font_size=22, color=TARIFF),
            label(r"trade in services and in tasks, \ not just goods", font_size=22, color=FISH),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Eaton and Kortum, \ \emph{Econometrica} 70(5) (2002); \ Costinot and "
                            r"Rodr\'iguez-Clare (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "The open questions. <bookmark mark='a'/> In 2002 Jonathan Eaton and Samuel Kortum turned Ricardo into "
            "a model of many countries, each drawing its productivity in each good at random; it is the engine of "
            "Part thirty-six. <bookmark mark='b'/> How large the gains are once there are many sectors and goods "
            "traded as inputs. <bookmark mark='c'/> How fast comparative advantage changes, and whether policy can "
            "change it, the question of industrial policy in Part sixty-six. <bookmark mark='d'/> Who inside a "
            "country gains, and how long adjustment takes. <bookmark mark='e'/> And trade in services and in tasks, "
            "which the old theories were not built for."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
