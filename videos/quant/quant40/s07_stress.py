from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import (
    BAD,
    PART,
    TAIL_C,
    load,
)


class Stress(VoiceoverScene):
    def construct(self):
        s = load("stress")
        self.card(s)
        self.why_stress()
        self.historical(s)
        self.worst10(load("extra"))
        self.supervisory()
        self.reverse_formula()
        self.reverse_table(s)
        self.maxloss(s)
        self.limits()
        self.question()

    def card(self, s):
        r = s["rev"][1]
        x = r["x"]
        c = chapter_card(6, r"Stress tests", r"What scenario would break us, and how plausible is it?", part=PART)
        with self.voiceover(
            f"Chapter six, and the answer to the pause: a fall of {100 * abs(x[0]):.1f} percent in the market, with small "
            f"losses in the size and value factors, about {r['distance']:.1f} standard deviations away. The most "
            "plausible way to lose a given amount is to move every factor in proportion to its covariance with the "
            "portfolio. This chapter derives it, and sets it against history."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_stress(self):
        cards = VGroup(
            desk_question(r"VaR looks backward and inward", r"it is a quantile of a model fitted to the recent past; it "
                          r"says nothing about events the window never saw", width=12.4, font_size=19),
            desk_question(r"a stress test names the event", r"apply a specific scenario, historical or invented, to "
                          r"today's positions, and revalue everything in full", width=12.4, font_size=19),
            desk_question(r"and asks what would break", r"the reverse question, what is the most likely scenario that "
                          r"costs a given amount, finds weaknesses no list of scenarios contained", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why a second kind of number. <bookmark mark='a'/> VaR is a quantile of a model fitted to the recent past, "
            "silent about what the window never saw. <bookmark mark='b'/> A stress test names the event and revalues "
            "today's positions under it. <bookmark mark='c'/> And a reverse stress test asks the opposite question: "
            "what is the most likely scenario that would cost a given amount?"
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def historical(self, s):
        hx = [-4.2, -1.8, 0.4, 2.6, 4.8]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"historical day", r"market", r"SMB, HML",
                                                                         r"loss, \$m", r"std devs")])
        tab = VGroup(head)
        for x in s["scen"]:
            m, sm, hm = x["x"]
            tab.add(VGroup(label(x["name"], font_size=18), MathTex(rf"{100 * m:+.1f}\%", font_size=24, color=BAD),
                           MathTex(rf"{100 * sm:+.1f},\ {100 * hm:+.1f}", font_size=22),
                           MathTex(f"{x['loss_m']:.1f}", font_size=26, color=BAD),
                           MathTex(f"{x['mahal']:.1f}", font_size=24, color=TAIL_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        foot = wrapped_label(r"a \$100m position in the US market with \$50m each in SMB and HML; distances are Mahalanobis, "
                             r"with the factors' covariance since 1990", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        a, b_, c = s["scen"]
        with self.voiceover(
            "Historical scenarios, on a portfolio of the market with tilts to small and value stocks. <bookmark mark='a'/> "
            f"The nineteenth of October nineteen eighty-seven: a loss of {a['loss_m']:.1f} million, a move "
            f"{a['mahal']:.0f} standard deviations away in the factors' joint distribution. <bookmark mark='b'/> October "
            f"twenty oh eight, {b_['loss_m']:.1f} million; <bookmark mark='c'/> the sixteenth of March twenty twenty, "
            f"{c['loss_m']:.1f}. Each is a day a VaR model fitted to the years before would have called impossible."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def worst10(self, x):
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        hx = [-2.6, 2.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"the five worst ten-day windows since 1926",
                                                                         r"market return")])
        tab = VGroup(head)
        for w in x["worst10"]:
            nm = rf"{months[(w['start'] // 100) % 100]} {w['start'] // 10000}"
            tab.add(VGroup(label(nm, font_size=20), MathTex(rf"{100 * w['ret']:.1f}\%", font_size=28, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        scaled = 100 * x["var1"] * 10 ** 0.5
        w0 = x["worst10"][0]
        foot = wrapped_label(rf"against a ten-day 99\% VaR of {scaled:.1f}\% by the square-root rule from history", 11.0,
                             17, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "History's own ten-day scenarios. <bookmark mark='a'/> October nineteen twenty-nine, "
            f"{100 * abs(w0['ret']):.0f} percent in ten trading days; October nineteen eighty-seven; October twenty oh "
            "eight; May nineteen forty, as France fell; and March twenty twenty. <bookmark mark='b'/> Each is about three "
            f"times the ten-day VaR of {scaled:.1f} percent: the scenarios a stress test must hold, which a ninety-nine "
            "percent number is not built to contain."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def supervisory(self):
        cards = VGroup(
            desk_question(r"supervisory stress tests", r"since the US SCAP of 2009, regulators publish severe scenarios "
                          r"each year and ask whether banks would keep their capital above a minimum through them",
                          width=12.4, font_size=19),
            desk_question(r"what they test", r"macro paths, unemployment, house prices, rates, and a market shock to "
                          r"trading books; the results set buffers and limit dividends", width=12.4, font_size=19),
            desk_question(r"what they miss", r"a scenario chosen by committee tests what someone imagined; the "
                          r"crisis that comes is usually a different one", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Regulators turned scenarios into policy. <bookmark mark='a'/> Since America's first supervisory stress test "
            "of twenty oh nine, they publish severe scenarios each year and ask whether banks keep enough capital "
            "through them. <bookmark mark='b'/> The scenarios are macro paths plus a market shock, and the results set "
            "capital buffers and limit dividends. <bookmark mark='c'/> But a scenario chosen by committee tests what "
            "someone imagined, and the next crisis is usually a different one."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def reverse_formula(self):
        rows = [cmath(r"\min_x\ x^\top\Sigma^{-1}x", r"\ \text{s.t.}\ ", r"-w^\top x = L", font_size=40),
                cmath(r"x^*", r"=", r"-\frac{L}{w^\top\Sigma w}\,\Sigma w", font_size=44, colors={r"x^*": BAD}),
                cmath(r"d^*", r"=", r"\frac{L}{\sqrt{w^\top\Sigma w}}", font_size=44, colors={r"d^*": TAIL_C})]
        whys = [why(r"the most plausible scenario: the factor move closest to the centre, in the covariance's metric, "
                    r"that costs the linear portfolio $w$ exactly $L$ (Breuer, Jandačka, Rheinberger and Summer 2009)"),
                why(r"Lagrange's condition: the move is proportional to $\Sigma w$, each factor's covariance with the "
                    r"portfolio"),
                why(r"its distance is the loss in units of the portfolio's own standard deviation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Reverse stress testing, as a formula. <bookmark mark='a'/> Find the factor move closest to the centre, "
            "measured in the covariance's own metric, that costs the portfolio exactly L. <bookmark mark='b'/> Lagrange's "
            "condition makes it proportional to sigma w: every factor moves in proportion to its covariance with the "
            "portfolio. <bookmark mark='c'/> And its distance is the loss divided by the portfolio's standard deviation."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def reverse_table(self, s):
        hx = [-3.6, -0.8, 1.8, 4.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"loss to cause, \$m", r"market move",
                                                                         r"SMB, HML", r"std devs")])
        tab = VGroup(head)
        for r in s["rev"]:
            m, sm, hm = r["x"]
            tab.add(VGroup(MathTex(f"{r['loss_m']:.0f}", font_size=28), MathTex(rf"{100 * m:+.1f}\%", font_size=26, color=BAD),
                           MathTex(rf"{100 * sm:+.1f},\ {100 * hm:+.1f}", font_size=24),
                           MathTex(f"{r['distance']:.1f}", font_size=26, color=TAIL_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        r10 = s["rev"][1]
        with self.voiceover(
            f"For the portfolio, whose daily standard deviation is {100 * s['sd_daily']:.2f} million dollars. "
            f"<bookmark mark='a'/> To lose ten million, the most plausible day is a market fall of "
            f"{100 * abs(r10['x'][0]):.1f} percent with small falls in the tilts, {r10['distance']:.1f} standard "
            "deviations away. <bookmark mark='b'/> Compare history: nineteen eighty-seven cost more, and was more than "
            "twice as far. The formula finds the cheapest route to a loss; history shows that crises take expensive "
            "routes, moving factors the covariance says should not move together."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def maxloss(self, s):
        rows = [cmath(r"\max_{x^\top\Sigma^{-1}x \le k^2}\ -w^\top x", r"=", r"k\,\sqrt{w^\top\Sigma w}", font_size=38,
                      colors={r"k\,\sqrt{w^\top\Sigma w}": BAD}),
                cmath(r"k = 3", r"\Rightarrow", rf"\${3 * 100 * s['sd_daily']:.1f}\text{{m}}", font_size=40),
                cmath(r"\text{non-linear books}", r":", r"\text{search the ellipsoid}", font_size=38)]
        whys = [why(r"the dual question, Studer's maximum loss: the worst loss over every scenario within $k$ standard "
                    r"deviations"),
                why(r"for this linear portfolio, three times its daily standard deviation"),
                why(r"with options the loss is not linear, and the worst point must be found numerically, by full "
                    r"revaluation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the dual question. <bookmark mark='a'/> Gerold Studer's maximum loss: the worst loss over every scenario "
            "within k standard deviations, k times the portfolio's own deviation for a linear book. "
            f"<bookmark mark='b'/> At three, about {3 * 100 * s['sd_daily']:.1f} million. <bookmark mark='c'/> With options "
            "the loss bends, and the worst point on the ellipsoid must be found by revaluing the book everywhere on it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"the covariance moves", r"in a crisis, the matrix that defines plausibility is itself "
                          r"different: Chapter 5's tails", width=12.4, font_size=19),
            desk_question(r"positions cannot be sold", r"a one-day scenario assumes the book can be closed at the shocked "
                          r"prices; Chapter 9 adds the time to exit", width=12.4, font_size=19),
            desk_question(r"second-round effects", r"forced sellers move prices further: Part 41's spirals are the stress "
                          r"that a static scenario cannot contain", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What stress tests leave out. <bookmark mark='a'/> In a crisis the covariance that defines plausibility is "
            "itself different. <bookmark mark='b'/> A one-day scenario assumes the book can be closed at the shocked "
            "prices. <bookmark mark='c'/> And forced sellers move prices further, the spirals of Part forty-one, which no "
            "static scenario contains."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"three losses each have a 99\% VaR of 9 (Pareto tails with exponent 2). Nothing is known about how "
                       r"they depend on each other. How large can the 99\% VaR of their sum be?")
        with self.voiceover(
            "Pause and predict. Three losses each have a ninety-nine percent VaR of nine, with Pareto tails of exponent "
            "two. Nothing is known about how they depend on each other. How large can the ninety-nine percent VaR of "
            "their sum be?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
