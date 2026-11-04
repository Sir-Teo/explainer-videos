from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import PART, ask, illustration, load

TOT = WHITE
RES = QC.OPTION
RRP = QC.REALIZED


class Balance(VoiceoverScene):
    def construct(self):
        p = load("policy")
        self.card()
        self.sheet(p)
        self.identity(p)
        self.qt(p)

    def card(self):
        c = chapter_card(2, r"QE and QT: the balance sheet", r"What happens when the Fed buys, and stops?", lit=(2008,),
                         part=PART)
        with self.voiceover("Chapter two. Quantitative easing, and its reverse."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, p):
        tw, w = np.asarray(p["WALCL"]["t"]), np.asarray(p["WALCL"]["v"]) / 1e3
        tr, r = np.asarray(p["WRESBAL"]["t"]), np.asarray(p["WRESBAL"]["v"]) / 1e3
        tq, q = np.asarray(p["RRPONTSYD"]["t"]), np.asarray(p["RRPONTSYD"]["v"]) / 1e3
        g = axes([2007, 2026], [0, 10], x_length=8.0, y_length=4.6, xlabel=r"year", ylabel=r"\$ trillion",
                 xticks=[2008, 2012, 2016, 2020, 2024], yticks=[0, 2, 4, 6, 8, 10], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax

        def area(t, v, col, op):
            return Polygon(*[ax.c2p(a, b) for a, b in zip(t, v)], ax.c2p(t[-1], 0), ax.c2p(t[0], 0), stroke_width=0,
                           fill_color=col, fill_opacity=op)
        A_tot = curve(ax, tw, w, TOT, stroke_width=3)
        A_res = area(tr, r, RES, 0.45)
        A_rrp = area(tq, q, RRP, 0.45)
        ev = [(2008.9, r"QE1"), (2010.9, r"QE2"), (2012.7, r"QE3"), (2017.8, r"runoff"), (2020.2, r"March 2020"),
              (2022.45, r"QT")]
        marks = VGroup()
        for x, s in ev:
            y = float(np.interp(x, tw, w))
            marks.add(VGroup(Line(ax.c2p(x, y + 0.2), ax.c2p(x, y + 0.9), color=GREY_B, stroke_width=1.5),
                             label(s, font_size=15, color=GREY_A).move_to(ax.c2p(x, y + 1.2))))
        leg = legend([(TOT, r"total assets"), (RES, r"bank reserves"), (RRP, r"overnight reverse repos")],
                     font_size=18).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        pk = p["walcl_peak"]
        side = VGroup(
            MathTex(rf"0.9 \to {pk['bn'] / 1e3:.2f}", font_size=34, color=TOT),
            label(r"\$ trillion, August 2008 to April 2022", font_size=17, color=GREY_B),
            wrapped_label(r"QE: the Fed buys long bonds with new reserves. It takes duration out of the market, which "
                          r"is meant to lower long yields (chapter 14)", 3.3, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(leg, DOWN, buff=0.5, aligned_edge=LEFT)
        side.shift(LEFT * max(0.0, side.get_right()[0] - 6.75))
        with self.voiceover(
            "The floor needs plenty of reserves, and the Fed created them by buying bonds. In August 2008 its balance "
            f"sheet was under a trillion dollars. <bookmark mark='a'/> Three rounds of quantitative easing took it to "
            "four and a half trillion by 2014. A first runoff shrank it from 2017, until the repo market seized in "
            "September 2019. <bookmark mark='b'/> In March 2020 it bought more in a few weeks than in any earlier year, "
            f"and by April 2022 it held {pk['bn'] / 1e3:.2f} trillion. <bookmark mark='c'/> Reserves, in pink, are most "
            "of what it owes; the overnight reverse repos, in teal, are cash that money-market funds park at the Fed "
            "when they have nowhere better to put it. Buying long bonds also takes interest-rate risk out of private "
            "hands, which is meant to lower long yields. Chapter fourteen measures what investors charge for that risk."
        ) as vo:
            self.play(FadeIn(g), Create(A_tot), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.5), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks[4]), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(A_res), FadeIn(A_rrp), FadeIn(leg[1]), FadeIn(leg[2]), FadeIn(marks[5]), FadeIn(side[2]))
        self.add(illustration(r"FRED: WALCL, WRESBAL, RRPONTSYD; weekly"))
        self.wait(0.5)
        self.clear_scene()

    def identity(self, p):
        rows = [cmath(r"\text{assets}", r"=", r"\text{currency} + \text{reserves} + \text{RRP} + \text{TGA} + \text{other}",
                      font_size=34, colors={r"\text{assets}": TOT}),
                cmath(r"\Delta\,\text{reserves}", r"=", r"\Delta\,\text{assets} - \Delta\,\text{RRP} - \Delta\,\text{TGA}"
                      r" - \Delta\,\text{currency} - \dots", font_size=34, colors={r"\Delta\,\text{reserves}": RES}),
                cmath(r"\text{QT}:\ \Delta\,\text{assets} < 0", r"\Rightarrow",
                      r"\text{reserves fall, unless RRP falls first}", font_size=34, colors={r"\Rightarrow": WHITE})]
        whys = [why(r"the balance sheet balances: every dollar the Fed holds is a dollar it owes someone"),
                why(r"so a change in what it owns must show up in one of its liabilities; TGA is the Treasury's own "
                    r"account at the Fed"),
                why(r"the reverse repo facility is a buffer: money funds take their cash out to buy the bills the "
                    r"Treasury issues instead, and reserves are spared")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.7, edge=6.8)
        with self.voiceover(
            "Why the two colours matter: the balance sheet balances. Everything the Fed owns is matched by something "
            "it owes. <bookmark mark='a'/> So when its assets shrink, some liability must shrink with them: reserves, "
            "the reverse repos, the Treasury's account, or currency. <bookmark mark='b'/> Which one is not up to the "
            "Fed. If money-market funds pull cash out of the reverse repo facility to buy Treasury bills, the shrinking "
            "comes out of that buffer, and banks' reserves are spared."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def qt(self, p):
        a, b = p["qt"]["peak"], p["qt"]["end"]
        cats = [("walcl", r"total assets", TOT), ("reserves", r"reserves", RES), ("rrp", r"reverse repos", RRP)]
        g = axes([-0.5, 2.5], [0, 10], x_length=6.4, y_length=4.4, ylabel=r"\$ trillion", xticks=[], yticks=[0, 2, 4, 6, 8, 10],
                 font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, (k, name, col) in enumerate(cats):
            for j, (src, op) in enumerate(((a, 0.35), (b, 0.85))):
                x0 = i - 0.32 + 0.34 * j
                p0, p1 = ax.c2p(x0, 0), ax.c2p(x0 + 0.3, src[k])
                bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.02), stroke_width=0, fill_color=col,
                                   fill_opacity=op).move_to((p0 + p1) / 2))
            bars.add(label(name, font_size=17, color=col).next_to(ax.c2p(i, 0), DOWN, buff=0.15))
        side = VGroup(
            label(r"April 2022 (faint) to November 2025 (solid)", font_size=19, color=GREY_A),
            MathTex(rf"\Delta\,\text{{assets}} = {b['walcl'] - a['walcl']:+.2f}", font_size=32, color=TOT),
            MathTex(rf"\Delta\,\text{{RRP}} = {b['rrp'] - a['rrp']:+.2f}", font_size=32, color=RRP),
            MathTex(rf"\Delta\,\text{{reserves}} = {b['reserves'] - a['reserves']:+.2f}", font_size=32, color=RES),
            wrapped_label(rf"the reverse repo facility peaked at \${p['rrp_daily_max']['bn'] / 1e3:.2f} trillion on 30 "
                          r"December 2022. The FOMC ended the runoff on 1 December 2025 (statement of 29 October)",
                          5.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Quantitative tightening tested it. From June 2022 the Fed let bonds mature without replacing them. "
            f"<bookmark mark='a'/> From the peak to November 2025, its assets fell by {a['walcl'] - b['walcl']:.1f} "
            f"trillion dollars. The reverse repos fell by {a['rrp'] - b['rrp']:.1f} trillion, nearly all the way to "
            f"zero. Reserves fell by only {a['reserves'] - b['reserves']:.1f}. <bookmark mark='b'/> With the buffer "
            "empty, the next dollar of runoff would come straight out of reserves, and repo rates had begun to creep "
            "above the floor. On the twenty-ninth of October 2025 the committee announced that runoff would stop on "
            "the first of December."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.15, run_time=2.5),
                      FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[1:4]], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        q = ask(r"QT ran for three and a half years. Why did repo rates start rising only at the very end?")
        with self.voiceover("A question for you: QT ran for three and a half years. Why did the strain show only at the end?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
