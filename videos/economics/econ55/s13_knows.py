from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Knows(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Forecasts, \ and what macroeconomics knows", r"Which answers survive every method?",
             "Chapter eleven. Forecasts, and what macroeconomics knows.",
             lit={2016: r"Ramey", 2018: r"Nakamura and Steinsson"}, scale=("nation", "world"), horizon=("a decade",))
        self.forecasts()
        self.knows()

    def forecasts(self):
        rows = VGroup(
            label(r"a model that identifies effects should also forecast: \ the toughest test, \ out of sample",
                  font_size=22, color=WHITE),
            label(r"August 2008: \ the professional forecasters expected growth in 2009 \ (Part 1)", font_size=21,
                  color=ERR),
            label(r"June 2021: \ the Federal Reserve expected inflation of 2.1\% in 2022 \ (Part 28)", font_size=21,
                  color=ERR),
            label(r"models fitted to calm decades are least reliable at the turns that matter most", font_size=21,
                  color=E.ACCENT),
            label(r"Part 57 grades the forecasters, \ and the models, \ properly", font_size=21, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.1)
        with self.voiceover(
            "If a model really knows what causes what, it should also forecast. <bookmark mark='a'/> Forecasting "
            "out of sample is the toughest test there is, because the model never saw the answer. <bookmark "
            "mark='b'/> The record at the turns is sobering. In August 2008 the professional forecasters expected "
            "the American economy to grow in 2009; it shrank by more than in any year since 1946. <bookmark "
            "mark='c'/> In June 2021 the Federal Reserve's median projection had inflation falling to 2.1 percent "
            "in 2022; it was 6.1 percent. <bookmark mark='d'/> Models fitted to calm decades are least reliable "
            "at exactly the turning points that matter most. <bookmark mark='e'/> Part fifty-seven grades the "
            "forecasters, and the models, properly."
        ) as vo:
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def knows(self):
        cards = point_cards([
            (r"money is not neutral", r"a surprise tightening lowers output for a year or two, \ and prices more "
             r"slowly; \ every method agrees on the sign and the delay", MONEY),
            (r"but its size is contested", r"the estimates differ several times over, \ with the method and the "
             r"decades used \ (the Dial)", ERR),
            (r"regions are not the nation", r"relative multipliers above one; \ national ones near or below one",
             DEMAND),
            (r"identified moments discipline models", r"a model must reproduce what the clean designs found, \ not "
             r"just the averages", THEORY),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.15)
        head = label(r"what macroeconomics knows, \ and how", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Ramey, \ Handbook of Macroeconomics 2 (2016); \ Nakamura and Steinsson, \ JEP 32(3) "
                            r"(2018)", corner=DR, font_size=12)
        with self.voiceover(
            "So what does macroeconomics know, and how does it know it? Valerie Ramey's survey of the shocks and "
            "their effects, and Nakamura and Steinsson's essay on identification, give a sober answer. <bookmark "
            "mark='a'/> Money is not neutral: a surprise tightening lowers output for a year or two and prices more "
            "slowly, and every credible method agrees on the sign and the delay. <bookmark mark='b'/> How much is "
            "contested: the estimates differ several times over with the method and the decades used, as the "
            "Dial will show. <bookmark mark='c'/> Regions are not the nation: relative multipliers are above one, "
            "national ones near or below it. <bookmark mark='d'/> And the clean findings, which Nakamura and "
            "Steinsson call identified moments, are the test a model must pass: not just matching averages, but "
            "reproducing what the best designs have found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
