from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import (ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, real_data,
                                        show_card, tbar)


class Event(VoiceoverScene):
    def construct(self):
        f = load("fomc")
        e = load("event")
        self.card()
        self.machinery(e)
        self.turn(e)
        self.slide(f)
        self.placebo(f)
        self.cluster(f)

    def card(self):
        c = chapter_card(10, r"Event studies", r"What happens to prices around an event?", part=PART)
        with self.voiceover("Chapter ten. Event studies."):
            show_card(self, c)
        self.play(FadeOut(c))

    def machinery(self, e):
        hc = history_card(1969, r"Fama, Fisher, Jensen and Roll", r"940 stock splits, 1927--1959, lined up in "
                          r"event time: prices rose in the months before the split, and did not drift after it",
                          color=QC.IDEA, width=4.6).to_corner(UL, buff=0.35)
        C_ = {r"AR_{i\tau}": EST, r"\overline{CAR}": ALT}
        rows = [cmath(r"AR_{i\tau}", r"=", r"R_{i\tau} - (\hat\alpha_i + \hat\beta_i R_{m\tau})", font_size=32, colors=C_),
                cmath(r"\overline{CAR}(\tau_1, \tau_2)", r"=", r"\tfrac1N \textstyle\sum_i \sum_{\tau=\tau_1}^{\tau_2} "
                      r"AR_{i\tau}", font_size=32, colors=C_),
                cmath(r"\mathrm{Var}(\overline{CAR})", r"=", r"\tfrac{1}{N^2} \textstyle\sum_i (\tau_2 - \tau_1 + 1)\,"
                      r"\sigma^2_{\varepsilon_i}", font_size=32, colors=C_),
                cmath(r"\text{same date:}\ \mathrm{Var}", r"=", r"\tfrac{1}{N^2}\textstyle\sum_i\sum_j \mathrm{cov}"
                      r"(CAR_i, CAR_j) \not\to 0", font_size=32, colors=C_),
                cmath(r"J_1", r"=", r"\overline{CAR} / \widehat{\mathrm{se}} \sim N(0, 1)", font_size=32, colors=C_)]
        whys = [why(r"normal return from a market model fitted on an estimation window before the event", 21),
                why(r"average across events, add up over the event window", 21),
                why(r"independent events, ignoring estimation error: the variance shrinks like $1/N$", 21),
                why(r"events that share a calendar date share its shocks: no diversification (MacKinlay 1997)", 21),
                why(r"the test statistic", 21)]
        step = ladder(self, rows, whys, keep=5, top=1.2, x=-0.8, buff=0.5, edge=6.8)
        with self.voiceover(
            "An event study asks what happens to prices around an event. In 1969 Fama, Fisher, Jensen and Roll lined up "
            "nine hundred and forty stock splits in event time: prices rose in the months before, and did not drift "
            "after. <bookmark mark='a'/> MacKinlay's 1997 survey set out the machinery: return minus a market-model "
            "normal return, <bookmark mark='b'/> averaged across events, summed over the window. <bookmark mark='c'/> "
            "Independent events: variance shrinks like one over N. <bookmark mark='d'/> Events sharing a date share its "
            "shocks, which do not average away. <bookmark mark='e'/> Then divide by the right standard error."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def turn(self, e):
        g = axes([-5.5, 5.5], [-0.2, 0.25], x_length=7.4, y_length=3.8, xlabel=r"trading days around the turn of the "
                 r"month ($-1$: last day, $+1$: first)", ylabel=r"abnormal return, \% a day", xticks=[-5, -3, -1, 1, 3, 5],
                 yticks=[-0.1, 0, 0.1, 0.2], yfmt=lambda u: f"{u:.1f}", font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        groups = VGroup()
        for name, col, off in (("1926-1986", EST, -0.2), ("1987-2020", ALT, 0.2)):
            bars = VGroup()
            for row in e[name]["ar"]:
                k = row["k"]
                b = tbar(ax, k + off, 100 * row["ar"], col, width=0.35)
                err = Line(ax.c2p(k + off, 100 * (row["ar"] - 2 * row["se"])),
                           ax.c2p(k + off, 100 * (row["ar"] + 2 * row["se"])), stroke_width=1.5, color=GREY_B)
                bars.add(VGroup(b, err))
            groups.add(bars)
        a, b = e["1926-1986"], e["1987-2020"]
        side = VGroup(
            legend([(EST, r"1926--1986"), (ALT, r"1987--2020")], font_size=20),
            label(r"the window $[-1, +3]$, about 18\% of trading days:", font_size=20, color=GREY_A),
            MathTex(rf"\text{{share of all returns: }} {100 * a['share_of_return']:.0f}\% \ (t = {a['t']:.1f})",
                    font_size=27, color=EST),
            MathTex(rf"\text{{after publication: }} {100 * b['share_of_return']:.0f}\% \ (t = {b['t']:.1f})",
                    font_size=27, color=ALT),
            label(r"Ariel (1987); Lakonishok and Smidt (1988)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A case with no news: the turn of the month. <bookmark mark='a'/> From 1926 to 1986 the last trading day and "
            f"the first three of the next, under a fifth of all days, delivered {100 * a['share_of_return']:.0f} percent of "
            "the market's return; Robert Ariel published it in 1987. <bookmark mark='b'/> Since then, "
            f"{100 * b['share_of_return']:.0f} percent, t of {b['t']:.1f}: weaker, still there."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in groups[0]], lag_ratio=0.1), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in groups[1]], lag_ratio=0.1), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def slide(self, f):
        paths = np.asarray(f["paths"])
        dates = np.asarray(f["pick_dates"])
        yr = dates // 10000 + ((dates // 100) % 100 - 1) / 12
        cal = axes([1993.5, 2021], [-0.06, 0.06], x_length=12.0, y_length=1.6, xticks=[1995, 2000, 2005, 2010, 2015,
                   2020], yticks=[], font_size=15).to_edge(UP, buff=0.5)
        cax = cal.ax
        evt = axes([-5.5, 5.5], [-0.05, 0.05], x_length=6.4, y_length=3.6, xlabel=r"trading days from the FOMC "
                   r"decision", ylabel=r"cumulative abnormal return", xticks=[-5, -1, 0, 1, 5],
                   yticks=[-0.04, 0, 0.04], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        evt.to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.45)
        eax = evt.ax
        taus = np.arange(-5, 6)
        small = VGroup()
        big = VGroup()
        for p, y in zip(paths, yr):
            pts = [cax.c2p(y + t * 0.035, np.clip(v, -0.06, 0.06)) for t, v in zip(taus, p)]
            small.add(VMobject(stroke_color=DATA_C, stroke_width=1.6, stroke_opacity=0.8).set_points_as_corners(pts))
            pts2 = [eax.c2p(t, np.clip(v, -0.05, 0.05)) for t, v in zip(taus, p)]
            big.add(VMobject(stroke_color=DATA_C, stroke_width=1.4, stroke_opacity=0.45).set_points_as_corners(pts2))
        car = np.asarray(f["car"])
        mean_line = curve(eax, taus, car, YELLOW, stroke_width=4)
        zero = DashedLine(eax.c2p(0, -0.05), eax.c2p(0, 0.05), color=GREY_C, stroke_width=1.5)
        run = f["run"]
        k = ValueTracker(0)

        def ro():
            i = int(min(k.get_value(), len(run) - 1))
            N, m, se = run[i]
            return MathTex(rf"N = {N}:\ \ \overline{{AR}}_0 = {1e4 * m:+.0f} \pm {2e4 * se:.0f}\ \text{{bp}}",
                           font_size=30, color=YELLOW)
        rom = always_redraw(lambda: ro().to_edge(RIGHT, buff=0.6).shift(UP * 0.4))
        a, s = f["all"], f["sub"]
        side = VGroup(
            MathTex(rf"\text{{FOMC days: }} {1e4 * a['mean_event']:.0f}\ \text{{bp; other days: }} "
                    rf"{1e4 * a['mean_other']:.0f}\ \text{{bp}}\ (t = {a['t']:.2f})", font_size=27, color=EST),
            MathTex(rf"\text{{{f['n_events']} decisions, {100 * f['share_of_days']:.0f}\% of days, "
                    rf"{100 * f['share_of_return']:.0f}\% of the excess return}}", font_size=25, color=GREY_A),
            MathTex(rf"1994\text{{--}}2011:\ {1e4 * s['1994-2011']['ar']:.0f}\ \text{{bp}}\ \ "
                    rf"(\text{{Lucca--Moench, close to close: about 33}})", font_size=24, color=GREY_A),
            MathTex(rf"2011\text{{--}}2020:\ {1e4 * s['2011-2020']['ar']:.0f}\ \text{{bp}}\ (t = {s['2011-2020']['t']:.2f})",
                    font_size=27, color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.4)
        src = real_data(r"scheduled FOMC decisions 1994--2020 (federalreserve.gov); French's daily market excess return",
                        corner=DL)
        late = s["2011-2020"]
        fade = ("smaller and no longer significant on its own" if late["t"] < 1.96 else "smaller but still significant")
        with self.voiceover(
            "Now the days the Federal Reserve announces its decisions. We transcribed every scheduled FOMC meeting "
            f"from 1994 to 2020 from the Fed's own pages: {f['n_events']} decisions. Here are forty, each a little path of "
            "abnormal returns, in calendar time. <bookmark mark='a'/> Slide each so its decision day sits at zero: "
            "calendar time becomes event time. <bookmark mark='b'/> Average them as decisions are added; the band "
            "narrows like one over root N, fairly, since each decision has its own date. <bookmark mark='c'/> On "
            f"decision days the market earned {1e4 * a['mean_event']:.0f} basis points over the riskless rate, against "
            f"{1e4 * a['mean_other']:.0f} on other days, t of {a['t']:.1f}: three percent of the days carried "
            f"{100 * f['share_of_return']:.0f} percent of the excess return. David Lucca and Emanuel Moench reported in "
            "2015 that since 1994 the S&P 500 rose forty-nine basis points on average in the twenty-four hours before "
            "scheduled announcements, about thirty-three close to close. Our 1994 to 2011 figure: "
            f"{1e4 * s['1994-2011']['ar']:.0f}. <bookmark mark='d'/> From 2011, {1e4 * late['ar']:.0f} basis points, {fade}."
        ) as vo:
            self.play(FadeIn(cal), FadeIn(src), LaggedStart(*[Create(p) for p in small], lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(evt), Create(zero))
            self.play(LaggedStart(*[ReplacementTransform(a_, b_) for a_, b_ in zip(small, big)], lag_ratio=0.04,
                                  run_time=4))
            vo.wait_until("b")
            self.add(rom)
            self.play(Create(mean_line), k.animate.set_value(len(run) - 1), run_time=4, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        rom.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def placebo(self, f):
        pl = np.asarray(f["placebo"])
        real = f["all"]["mean_event"]
        lo, hi = -0.002, 0.0035
        g = axes([lo, hi], [0, 1], x_length=8.0, y_length=3.6, xlabel=rf"mean excess return of {f['n_events']} random "
                 r"non-FOMC days", xticks=[-0.001, 0, 0.001, 0.002, 0.003], xfmt=lambda u: f"{1e4 * u:.0f}",
                 yticks=[], font_size=16).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        edges = np.linspace(lo, hi, 56)
        n = ValueTracker(10)

        def hb():
            v = pl[:int(n.get_value())]
            h = hist_bars(ax, v, edges, DATA_C, density=False)
            peak = max(np.histogram(np.clip(v, lo, hi), edges)[0].max(), 1)
            return h.stretch_to_fit_height(max(3.2 * peak / max(np.histogram(pl, edges)[0].max(), 1), 0.02),
                                           about_edge=DOWN).align_to(ax.c2p(0, 0), DOWN)
        hm = always_redraw(hb)
        mk = Line(ax.c2p(real, 0), ax.c2p(real, 0.95), color=YELLOW, stroke_width=5)
        mkl = MathTex(rf"\text{{FOMC days: }} {1e4 * real:.0f}\ \text{{bp}}", font_size=26, color=YELLOW).next_to(
            mk, UP, buff=0.08)
        cnt = always_redraw(lambda: MathTex(rf"\text{{placebo sets: }} {5 * int(n.get_value()):,}".replace(",", "{,}"),
                                            font_size=26, color=GREY_A).next_to(g, UP, buff=0.1).align_to(g, LEFT))
        side = MathTex(rf"p = {f['p_placebo']:.4f}", font_size=34, color=EST).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            f"A check with no formula: placebos. Draw {f['n_events']} days without a decision, average their returns, "
            "and repeat ten thousand times. That is what an average of that many ordinary days looks like, fat tails, "
            "volatility clusters and all, with no assumption about the distribution. <bookmark mark='a'/> The real "
            f"decision days sit far in the right tail: only {100 * f['p_placebo']:.2f} percent of placebo sets do as "
            "well. The trial counter's logic, in miniature: compare what you found with what chance finds."
        ) as vo:
            self.play(FadeIn(g))
            self.add(hm, cnt)
            self.play(n.animate.set_value(len(pl)), run_time=vo.until("a"), rate_func=rate_functions.ease_in_quad)
            vo.wait_until("a")
            self.play(Create(mk), FadeIn(mkl), FadeIn(side))
        hm.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def cluster(self, f):
        rows = VGroup(
            label(r"When every event shares one date", font_size=32),
            wrapped_label(r"100 firms in one industry announce on the same day; the market model removes the market, "
                          r"not the industry's shock (simulated: industry shock sd 1.5\%, firm noise 2\%)", 11.6, 22,
                          GREY_A),
            MathTex(rf"\text{{naive se}} = s / \sqrt{{100}} \approx {100 * f['cluster_naive']:.2f}\%", font_size=32,
                    color=BAD),
            MathTex(rf"\text{{true sampling sd}} = {100 * f['cluster_true']:.2f}\%", font_size=32, color=GOOD),
            wrapped_label(r"fix: the time series of the portfolio's abnormal returns on non-event days (the crude "
                          r"dependence adjustment), or cluster by date", 11.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.6)
        q = predict(r"A hundred firms all announcing on the same day: is the CAR's standard error $\sigma/\sqrt{100}$?")
        q.next_to(rows, DOWN, buff=0.4)
        ratio = f["cluster_true"] / f["cluster_naive"]
        with self.voiceover(
            "FOMC days were spread over twenty-seven years. Many studies are not so lucky: a rule that hits a hundred "
            "firms on one day. <bookmark mark='a'/> Pause and predict: is the standard error sigma over root a hundred? "
            "<bookmark mark='b'/> Simulate a hundred firms sharing an industry shock the market model does not remove. "
            f"The naive standard error says {100 * f['cluster_naive']:.2f} percent; the true spread is "
            f"{100 * f['cluster_true']:.2f}, {ratio:.0f} times larger. Chapter three again: cluster by date, or use the "
            "portfolio's own time series."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
