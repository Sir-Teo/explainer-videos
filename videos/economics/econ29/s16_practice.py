from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ the model in the institution", r"Who runs these models, \ and for what?",
             "Chapter fourteen. In practice: the model in the institution.", lit={1996: r"Dynare"},
             scale=("nation",), horizon=("a quarter", "a few years"))
        self.volatility()
        self.hours()
        self.institutions()
        self.workflow()

    def _fact(self, key, data_m, theory_m, agora_m, colours):
        f = next(x for x in facts.FACTS if x.key == key)
        return fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                          (r"Agora", agora_m)), width=12.4, font_size=22,
                         colors=colours).move_to(UP * 0.3)

    def volatility(self):
        F = load("facts")
        d, m = F["data"], F["model"]
        data_m = label(rf"US 1948--2019: \\ investment {d['i']['rel']:.1f}$\times$ output; \\ consumption "
                       rf"{d['c']['rel']:.2f}$\times$", font_size=18, color=WHITE)
        theory_m = label(r"smoothing: \ spread a \\ temporary gain over years; \\ capital absorbs the rest",
                         font_size=18, color=CONS)
        agora_m = label(rf"the Island: \ investment \\ {m['i']['rel']:.1f}$\times$; \ consumption \\ "
                        rf"{m['c']['rel']:.2f}$\times$", font_size=18, color=E.AGORA)
        fc = self._fact("volatility", data_m, theory_m, agora_m, (WHITE, CONS, None))
        tag = data_tag(r"BEA via FRED; \ the Island: \ simulated", corner=DR, font_size=12)
        with self.voiceover(
            "Two of the series' facts now get Agora's column. <bookmark mark='a'/> Investment is about three times "
            f"as volatile as output, consumption less. In American data, investment moves {d['i']['rel']:.1f} times "
            f"as much as output, and consumption {d['c']['rel']:.2f} times, durables included. "
            "<bookmark mark='b'/> The theory: households smooth consumption, spreading a temporary gain over years, "
            "so capital absorbs the swings. <bookmark mark='c'/> On the Island, investment moves "
            f"{m['i']['rel']:.1f} times as much as output and consumption {m['c']['rel']:.2f}: the right order, too "
            "smooth on both counts."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()

    def hours(self):
        F = load("facts")
        d, m = F["data"], F["model"]
        data_m = label(rf"hours {d['n']['rel']:.2f}$\times$ output, \\ correlation {d['n']['corr']:.2f}; \\ with "
                       rf"productivity {d['corr_nw']:.2f}", font_size=18, color=WHITE)
        theory_m = label(r"work when work pays: \\ intertemporal \\ substitution", font_size=18, color=HOURS)
        agora_m = label(rf"the Island: \ {m['n']['rel']:.2f}$\times$, \\ but with productivity \\ "
                        rf"{m['corr_nw']:.2f}", font_size=18, color=E.AGORA)
        fc = self._fact("hours", data_m, theory_m, agora_m, (WHITE, HOURS, None))
        tag = data_tag(r"BLS via FRED; \ the Island: \ simulated", corner=DR, font_size=12)
        with self.voiceover(
            "<bookmark mark='a'/> Hours rise in booms and fall in recessions: in the data they move "
            f"{d['n']['rel']:.2f} times as much as business output, with a correlation of {d['n']['corr']:.2f}. "
            "<bookmark mark='b'/> The theory: people work when work pays best. <bookmark mark='c'/> The Island gets "
            f"the size, {m['n']['rel']:.2f}, with Hansen's help, but its hours move in lockstep with productivity, "
            "and America's do not. A fact can be matched for the wrong reason."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()

    def institutions(self):
        cards = point_cards([
            (r"central banks", r"the New York Fed's DSGE model \\ publishes forecasts; \ the ECB, \\ the Bank of "
                               r"England and \\ the Riksbank run their own", OUTPUT),
            (r"what they are", r"this part's model, \ plus sticky \\ prices and wages, \ money, \\ credit, \ and "
                               r"many shocks", INVEST),
            (r"what they are for", r"forecasts that add up; \\ stories for each forecast; \\ `what if' for each "
                                   r"policy", TECH),
            (r"the software", r"Dynare, \ free and open: \\ write the conditions; \\ it linearizes, \ solves \\ "
                              r"and simulates", VALUE),
        ], width=12.8, cols=2, font_size=21).move_to(DOWN * 0.1)
        tag = published_tag(r"Federal Reserve Bank of New York, \ \emph{Liberty Street Economics}; \ Dynare "
                            r"(dynare.org)", corner=DR, font_size=12)
        with self.voiceover(
            "Where does this live now? <bookmark mark='a'/> In central banks. The Federal Reserve Bank of New "
            "York publishes the forecasts of its DSGE model; the European Central Bank, the Bank of England and "
            "Sweden's Riksbank run their own. <bookmark mark='b'/> Each is this part's model at its core, with "
            "sticky prices and wages, money, credit, and many shocks added. <bookmark mark='c'/> They are used for "
            "forecasts whose pieces add up, for a story behind each forecast, and for asking what would happen "
            "under a different policy. <bookmark mark='d'/> And they are solved with software like Dynare, free "
            "and open: you write down the equilibrium conditions, and it linearizes, solves and simulates exactly "
            "as chapter eight did by hand."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def workflow(self):
        steps = [
            (r"1. \ write the conditions", r"optimality, \ markets, \ shocks", VALUE),
            (r"2. \ the steady state", r"match the long-run facts", INVEST),
            (r"3. \ calibrate or estimate", r"the parameters", E.ACCENT),
            (r"4. \ solve", r"linearize; \ count the roots", TECH),
            (r"5. \ test", r"moments and responses \ against the data", OUTPUT),
            (r"6. \ use", r"a forecast, \ a scenario, \ a policy", HOURS),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=23, color=c), label(b, font_size=20, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b, c in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The modeller's job follows this part step by step. <bookmark mark='a'/> Write down the conditions: "
            "optimality, market clearing, and the shocks. <bookmark mark='b'/> Find the steady state, and make it "
            "match the long-run facts. <bookmark mark='c'/> Calibrate or estimate the parameters. "
            "<bookmark mark='d'/> Solve, by linearizing and counting the roots. <bookmark mark='e'/> Test the "
            "model's moments and responses against the data's, honestly, misses included. "
            "<bookmark mark='f'/> And only then use it: for a forecast, a scenario, or a policy question."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
