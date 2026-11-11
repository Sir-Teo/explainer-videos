from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import FWD, PART, POLICY, ask, illustration, load

OTHER = GREY_B


class FOMC(VoiceoverScene):
    def construct(self):
        f = load("fomc")
        self.card()
        self.days(f)
        self.biggest(f)
        self.transmission(f)

    def card(self):
        c = chapter_card(15, r"FOMC days", r"What does a Fed meeting do to the curve?", part=PART)
        with self.voiceover("Chapter fifteen. What Fed meetings do to the curve."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def days(self, f):
        a, b = np.asarray(f["fomc_dy2"]), np.asarray(f["other_dy2"])
        bins = np.linspace(-60, 40, 51)
        ha, _ = np.histogram(a, bins=bins, density=True)
        hb, _ = np.histogram(b, bins=bins, density=True)
        top = max(ha.max(), hb.max()) * 1.1
        g = axes([-60, 40], [0, top], x_length=8.0, y_length=4.4, xlabel=r"one-day change in the 2-year zero yield, bp",
                 ylabel=r"density", xticks=[-60, -40, -20, 0, 20, 40], yticks=[], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        w = bins[1] - bins[0]

        def hist(h, col, op):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1],
                                      stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                [ax.c2p(x + w / 2, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(bins[:-1], h)])
        H_b = hist(hb, OTHER, 0.5)
        H_a = hist(ha, POLICY, 0.6)
        side = VGroup(
            label(rf"{f['n_fomc']} scheduled meetings, 1994--2020", font_size=22, color=POLICY),
            MathTex(rf"\text{{sd on FOMC days}} = {f['sd_fomc']:.1f}\ \text{{bp}}", font_size=30, color=POLICY),
            MathTex(rf"\text{{all other days}} = {f['sd_other']:.1f}\ \text{{bp}}", font_size=30, color=OTHER),
            wrapped_label(r"Grey histogram: every seventh other-day observation retained in cache. Other-day SD uses the full original sample; 1994--2020. No tail pooling", 3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"The 1994-to-2020 sample contains {f['n_fomc']} scheduled meeting observations. Yellow shows their two-year yield changes; grey shows every seventh other-day observation retained in the cache. Full histogram ranges are used, rather than pooling large changes into endpoint bins. <bookmark mark='a'/> The original full-sample standard deviations are {f['sd_fomc']:.1f} basis points on scheduled meeting days and {f['sd_other']:.1f} on other days. The grey histogram is thinned, so its dispersion need not exactly match that second number. The two-year yield reflects expected policy, term premia and other news, rather than a pure policy forecast. <bookmark mark='b'/> These close-to-close observations describe association; scheduled meetings, other news and the crisis composition can differ. They do not isolate an exogenous monetary-policy shock."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in H_b], lag_ratio=0.02), FadeIn(side[2]))
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in H_a], lag_ratio=0.02), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"the Fed's GSW curve; scheduled FOMC dates from the Fed's historical materials"))
        self.wait(0.4)
        self.clear_scene()

    def biggest(self, f):
        what = {20090318: r"the Fed will buy \$300 bn of Treasuries and more mortgage bonds",
                20080318: r"75 bp target cut; daily yield rose (not a causal estimate)",
                20071211: r"25 bp target cut; daily yield fell (other news may enter)",
                19950706: r"the first cut of the 1995 soft landing",
                20040128: r"\emph{considerable period} dropped from the statement",
                20020626: r"rates held; WorldCom's fraud had broken the night before"}
        rows = VGroup()
        for b in f["biggest"]:
            d = b["date"]
            rows.add(VGroup(MathTex(rf"{d // 10000}\text{{-}}{d // 100 % 100:02d}\text{{-}}{d % 100:02d}", font_size=26),
                            MathTex(rf"{b['dy2']:+.0f}\ \text{{bp}}", font_size=28,
                                    color=QC.LOSS if b["dy2"] > 0 else QC.GAIN),
                            label(what.get(d, r""), font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 2.6)
            r_[2].align_to(rows, LEFT).shift(RIGHT * 4.2)
        head = label(r"Six largest absolute daily moves among saved meeting days", font_size=30).to_edge(UP, buff=0.5)
        rows.next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"Daily moves include other news. Kuttner (2001) uses futures to distinguish anticipated policy from surprises; Gürkaynak, Sack and Swanson (2005) distinguish target and path factors",
                             12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The six largest absolute two-year moves among those meeting days are selected after observing their outcomes. March 2009 coincided with an announced three-hundred-billion-dollar Treasury purchase program and a daily decline of about twenty-six basis points. <bookmark mark='a'/> March 2008 combined a seventy-five-basis-point target cut with a daily rise in the two-year yield. A cut need not produce a yield decline: expectations and other news matter. <bookmark mark='b'/> Kuttner separates expected target changes from surprises using fed-funds futures. Gürkaynak, Sack and Swanson distinguish target and policy-path announcement factors. These are separate identification exercises, not replications performed here. June 2002 also followed WorldCom's fraud disclosure, illustrating the contamination in a daily window."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def transmission(self, f):
        x, y = np.asarray(f["fomc_dy2"]), np.asarray(f["fomc_df10"])
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]
        g = axes([-30, 30], [-40, 40], x_length=5.6, y_length=5.0, xlabel=r"change in the 2-year yield, bp",
                 ylabel=r"change in fitted instantaneous forward at 10y, bp", xticks=[-30, 0, 30], yticks=[-40, -20, 0, 20, 40],
                 font_size=14).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=FWD,
                            fill_opacity=0.8) for a, b in zip(x, y)])
        bt = f["beta_f10"]
        alpha = float(y.mean() - bt * x.mean())
        fit = Line(ax.c2p(-30, alpha - 30 * bt), ax.c2p(30, alpha + 30 * bt), color=WHITE, stroke_width=3)
        side = VGroup(
            MathTex(rf"\Delta f^{{(10)}} = {alpha:+.3f}+{bt:.2f}\,\Delta y^{{(2)}}+\varepsilon", font_size=36, color=FWD),
            MathTex(rf"\text{{conventional OLS SE: }}{f['se_f10']:.2f}", font_size=26, color=GREY_B),
            wrapped_label(r"Nominal instantaneous forwards combine expected short rates and risk-premium effects under a model; long-horizon expectations can also react", 5.0, 19, GREY_A),
            wrapped_label(r"This daily OLS slope is descriptive. Hanson--Stein study long-term real rates; Nakamura--Steinsson emphasize identification and central-bank information effects", 5.0, 19,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            f"Each point pairs a meeting day's two-year yield change with the change in the fitted instantaneous nominal forward at ten years. It is not a one-year forward loan rate. All paired values are plotted. <bookmark mark='a'/> The intercept-inclusive daily regression slope is {bt:.2f}, with conventional homoskedastic OLS standard error {f['se_f10']:.2f}. No heteroskedasticity-robust or causal confidence interval is supplied. <bookmark mark='b'/> Long-horizon expectations as well as risk premia may respond; the expectations hypothesis alone does not force this slope to zero. Hanson and Stein study long-term real rates and a risk-premium channel. Nakamura and Steinsson use short announcement windows and examine central-bank information effects. A narrow window reduces other news but does not automatically identify a pure policy shock or separate those channels."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=2))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        q = ask(r"a one-day window also catches the day's other news. How would you isolate what the Fed said?")
        with self.voiceover("A daily window catches everything else that happened that day. How would you isolate what "
                            "the Fed said?"):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Use pre-specified intraday windows and market surprises; check concurrent releases, timing, policy-path news and central-bank information. Identification assumptions still need evidence.", 11.8, 26, FWD).move_to(ORIGIN)
        with self.voiceover("Use pre-specified intraday windows and market surprises. Check concurrent releases, announcement timing, policy-path news and central-bank information. Identification assumptions still need evidence."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
