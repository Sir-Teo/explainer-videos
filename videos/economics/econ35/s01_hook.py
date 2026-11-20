from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.challenge()
        self.answer()
        self.trade()
        self.question()
        self.title()
        self.objectives()

    def challenge(self):
        who = point_cards([
            (r"Stanis{\l}aw Ulam", r"mathematician: \\ probability, \\ the Monte Carlo method", FISH),
            (r"Paul Samuelson", r"economist: \\ the first American \\ Nobel in economics", ARCH),
        ], width=10.4, cols=2, font_size=22).move_to(UP * 0.4)
        q = wrapped_label(r"``Name me one proposition in all of the social sciences which is both true and "
                          r"non-trivial.''", 11.0, 28, WHITE).next_to(who, DOWN, buff=0.6)
        tag = published_tag(r"Samuelson, \ ``The Way of an Economist'' (1969), \ as widely quoted", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The mathematician Stanislaw Ulam was one of the inventors of the Monte Carlo method. "
            "<bookmark mark='a'/> One day he put a challenge to his friend Paul Samuelson, who would "
            "become the first American to win the Nobel prize in economics. <bookmark mark='b'/> Name me one "
            "proposition in all of the social sciences, he said, which is both true and not trivial. Samuelson had "
            "no answer that day."
        ) as vo:
            self.play(FadeIn(who.cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who.cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def answer(self):
        S = tables.SAMUELSON_ULAM.data
        head = label(r"years later: \ Ricardo's comparative advantage", font_size=32, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.7)
        qc = quote_card(tex_safe(S["quote"]), r"Paul Samuelson, \ 1969, \ as he told it", width=11.6,
                        font_size=25).next_to(head, DOWN, buff=0.6)
        tag = published_tag(r"Samuelson (1969); \ the wording as reproduced in several sources", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Years later, as Samuelson told it, he had his answer: David Ricardo's theory of comparative advantage. "
            "<bookmark mark='a'/> That it is logically true, he said, need not be argued before a mathematician. "
            "That it is not trivial is attested by the thousands of important and intelligent men who have never "
            "been able to grasp the doctrine for themselves, or to believe it after it was explained to them. "
            "<bookmark mark='b'/> This part is about that idea, what it gets right and what it leaves out: above "
            "all, that trade makes a country richer without making everyone in it richer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(Indicate(head, color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def trade(self):
        O = load("openness")
        ax = plane([1870, 2021], [0, 80], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.0, y_length=4.6,
                   xticks=[1870, 1900, 1930, 1960, 1990, 2020], yticks=[0, 20, 40, 60, 80],
                   ylabel=r"exports plus imports, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        wars = shade(ax, [(1914, 1918), (1939, 1945)], 0, 80, RECESS, 0.6)
        med = path(ax, O["years"], O["median"], WHITE, 3.4, smooth=False)
        us = path(ax, O["usa_y"], O["usa"], USA, 2.4, smooth=False)
        key = VGroup(label(r"the median of 18 rich economies", font_size=16, color=WHITE),
                     label(r"the United States", font_size=16, color=USA)).arrange(RIGHT, buff=0.5).next_to(
            ax, UP, buff=0.12)
        side = VGroup(
            label(rf"1870: \ {O['m1870']:.0f}\%", font_size=20, color=WHITE),
            label(rf"1913: \ {O['m1913']:.0f}\%", font_size=20, color=WHITE),
            label(rf"{O['m1932_y']}: \ {O['m1932']:.0f}\%", font_size=20, color=TARIFF),
            label(rf"2019: \ {O['m2019']:.0f}\%", font_size=20, color=GAIN),
            label(rf"America: \ {O['us1932']:.0f}\% in 1932, \\ {O['us2019']:.0f}\% in 2019", font_size=18,
                  color=USA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6", corner=DR, font_size=12)
        with self.voiceover(
            "And it matters more than ever. <bookmark mark='a'/> Here is trade, exports plus imports, as a share of "
            "output in eighteen rich economies since 1870. In the median economy it was "
            f"{O['m1870']:.0f} percent in 1870 <bookmark mark='b'/> and {O['m1913']:.0f} percent by 1913, the "
            f"first globalization. <bookmark mark='c'/> Then two wars and a depression: by {O['m1932_y']} it was "
            f"down to {O['m1932']:.0f} percent. <bookmark mark='d'/> It took until the 1970s to recover, and by "
            f"2019 it was {O['m2019']:.0f} percent. <bookmark mark='e'/> America, a continent that trades mostly "
            f"with itself, went from {O['us1932']:.0f} percent in 1932 to {O['us2019']:.0f} percent."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(wars), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(med), Create(us), FadeIn(side[0]), run_time=2.5)
            for mk, r_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why does a country that is worse at everything still have something to sell?", font_size=25,
                  color=ISLAND),
            label(r"what do endowments of labour, \ capital and land decide?", font_size=25, color=CAPITAL),
            label(r"who loses, \ why do they win in politics, \ and could the winners pay them?", font_size=25,
                  color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: why do countries trade, and who wins and loses when they do? "
            "<bookmark mark='a'/> Why does a country that is worse at making everything still have something to "
            "sell? <bookmark mark='b'/> What do a country's endowments, its labour, capital and land, decide about "
            "what it trades? <bookmark mark='c'/> And who loses, why do the losers so often win in politics, and "
            "could the winners pay them?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1929, 2025], [0, 20], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], TARIFF, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 35 \ $\cdot$ \ Trade I: \ Comparative Advantage", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-five: trade, and comparative advantage."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VII \ $\cdot$ \ The World Economy", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"a game with four numbers; \ Ricardo; \ many goods; \ Japan opens",
            r"factor proportions; \ Stolper and Samuelson; \ Leontief's paradox; \ the missing trade",
            r"specific factors; \ tariffs and quotas; \ the optimal tariff",
            r"protection for sale; \ trade agreements as a way out of a dilemma; \ compensation",
            r"a new dial: \ the gains from trade; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> A game with four numbers, then Ricardo's own, then many goods, "
            "and a test: Japan, opened to trade under American naval pressure in the 1850s. "
            "<bookmark mark='b'/> A second theory, "
            "in which what a country has decides what it sells, its theorems about who loses, and the paradox and "
            "the puzzle that its tests turned up. <bookmark mark='c'/> Who loses first, and what a tariff does. "
            "<bookmark mark='d'/> Why protection is for sale, why countries sign trade agreements, and whether the "
            "winners can pay the losers. <bookmark mark='e'/> And a new dial: how much a country gains from trade."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
