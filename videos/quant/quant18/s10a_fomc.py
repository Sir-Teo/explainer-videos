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
        bins = np.linspace(-30, 30, 31)
        ha, _ = np.histogram(np.clip(a, -29.9, 29.9), bins=bins, density=True)
        hb, _ = np.histogram(np.clip(b, -29.9, 29.9), bins=bins, density=True)
        top = max(ha.max(), hb.max()) * 1.1
        g = axes([-30, 30], [0, top], x_length=8.0, y_length=4.4, xlabel=r"one-day change in the 2-year zero yield, bp",
                 ylabel=r"density", xticks=[-30, -15, 0, 15, 30], yticks=[], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        w = bins[1] - bins[0]

        def hist(h, col, op):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1],
                                                                                          0.005),
                                      stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                [ax.c2p(x + w / 2, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(bins[:-1], h)])
        H_b = hist(hb, OTHER, 0.5)
        H_a = hist(ha, POLICY, 0.6)
        side = VGroup(
            label(rf"{f['n_fomc']} scheduled meetings, 1994--2020", font_size=22, color=POLICY),
            MathTex(rf"\text{{sd on FOMC days}} = {f['sd_fomc']:.1f}\ \text{{bp}}", font_size=30, color=POLICY),
            MathTex(rf"\text{{other days}} = {f['sd_other']:.1f}\ \text{{bp}}", font_size=30, color=OTHER),
            wrapped_label(r"since 1994 the FOMC announces its decision the same afternoon; before, markets inferred it "
                          r"from the Fed's trading", 3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Eight times a year the Federal Open Market Committee meets, and since 1994 it has announced its decision "
            "the same afternoon. Here are the one-day changes in the two-year yield: grey for ordinary days, yellow for "
            f"the {f['n_fomc']} scheduled meeting days through 2020. <bookmark mark='a'/> Meeting days are wider: a "
            f"standard deviation of {f['sd_fomc']:.1f} basis points against {f['sd_other']:.1f}. The two-year yield is "
            "the market's forecast of policy over the next two years, so it is where Fed news lands first. "
            "<bookmark mark='b'/> Part six measured the stock market on these same days; here the question is how far "
            "down the curve the news travels."
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
                20080318: r"a 75 bp cut, less than markets had priced",
                20071211: r"a 25 bp cut; markets wanted more",
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
        head = label(r"The six biggest FOMC days for the 2-year yield", font_size=30).to_edge(UP, buff=0.5)
        rows.next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"what moved yields was the surprise, not the decision: the part markets had not priced. Kuttner "
                             r"(2001) measured it with fed funds futures; Gürkaynak, Sack and Swanson (2005) showed the "
                             r"statement's words about the future move long yields more than the rate decision itself",
                             12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The six biggest meeting days. March 2009: the Fed announced it would buy three hundred billion dollars of "
            "Treasuries, and the two-year fell twenty-six basis points. <bookmark mark='a'/> A year earlier it cut by "
            "three quarters of a point and yields rose, because markets had expected a full point. "
            "<bookmark mark='b'/> What moves yields is the surprise. Kenneth Kuttner measured it in 2001 with fed funds "
            "futures; Refet Gürkaynak, Brian Sack and Eric Swanson showed in 2005 that the statement's words about the "
            "future move long yields more than the decision itself. Actions speak; words speak louder. And the sixth "
            "day is a warning: in June 2002 the Fed did nothing, but WorldCom's accounting fraud had come out the night "
            "before."
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
        g = axes([-30, 30], [-30, 30], x_length=5.6, y_length=5.0, xlabel=r"change in the 2-year yield, bp",
                 ylabel=r"change in the forward rate 10 years ahead, bp", xticks=[-30, 0, 30], yticks=[-30, 0, 30],
                 font_size=14).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.clip(a, -30, 30), np.clip(b, -30, 30)), radius=0.045, color=FWD,
                            fill_opacity=0.8) for a, b in zip(x, y)])
        bt = f["beta_f10"]
        fit = Line(ax.c2p(-30, -30 * bt), ax.c2p(30, 30 * bt), color=WHITE, stroke_width=3)
        side = VGroup(
            MathTex(rf"\Delta f^{{(10)}} = {bt:.2f}\,\Delta y^{{(2)}}", font_size=36, color=FWD),
            MathTex(rf"(\pm {f['se_f10']:.2f})", font_size=26, color=GREY_B),
            wrapped_label(r"a forward rate ten years ahead is far beyond any meeting's horizon; under the expectations "
                          r"hypothesis it should barely react to news about the next two years", 5.0, 19, GREY_A),
            wrapped_label(r"it moves a third as much: news about policy moves the premium for holding long bonds "
                          r"too (Hanson and Stein 2015; Nakamura and Steinsson 2018 use 30-minute windows)", 5.0, 19,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "How far does the news travel? On each meeting day, plot the change in the two-year yield against the "
            "change in the forward rate ten years ahead: the rate for a single year starting a decade from now. "
            "<bookmark mark='a'/> Nothing the committee decides this afternoon should say much about 2035. Yet the "
            f"slope is {bt:.2f}: a third of the move reaches a decade out. <bookmark mark='b'/> Samuel Hanson and "
            "Jeremy Stein found the same in 2015 and read it as the premium moving: some investors reach for yield when "
            "short rates fall. Emi Nakamura and Jón Steinsson used thirty-minute windows around each announcement to "
            "keep out everything else that happens in a day."
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
        self.wait(0.5)
        self.clear_scene()
