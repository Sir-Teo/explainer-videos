from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import MKT, PART, POLICY, ask, illustration, load

IORB_C = QC.OPTION
RRP_C = QC.REALIZED
BAND_C = QC.DELTA


class Money(VoiceoverScene):
    def construct(self):
        p = load("policy")
        self.card()
        self.tacct()
        self.demand(p)
        self.rates(p)

    def card(self):
        c = chapter_card(1, r"Money, reserves and the floor", r"What does the Fed actually set?", lit=(2008,), part=PART)
        with self.voiceover("Chapter one. Money, reserves, and the floor."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tacct(self):
        W = 4.6

        def side(title, rows, col):
            head = label(title, font_size=24, color=col)
            items = VGroup(*[label(r, font_size=21, color=GREY_A) for r in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.2)
            return VGroup(head, items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        assets = side(r"Assets", [r"Treasuries", r"agency mortgage bonds", r"loans (discount window, repo)"], QC.SPOT)
        liab = side(r"Liabilities", [r"currency in circulation", r"bank reserves", r"overnight reverse repos (ON RRP)",
                                     r"the Treasury's account"], QC.OPTION)
        assets.move_to(LEFT * W / 2 + UP * 0.6)
        liab.move_to(RIGHT * W / 2 + RIGHT * 0.4 + UP * 0.4)
        top = Line(LEFT * (W + 0.4) + UP * 2.1, RIGHT * (W + 1.2) + UP * 2.1, color=GREY_B)
        mid = Line(UP * 2.1, DOWN * 1.0, color=GREY_B).shift(RIGHT * 0.25)
        title = label(r"The Federal Reserve's balance sheet", font_size=30).to_edge(UP, buff=0.4)
        notes = VGroup(
            wrapped_label(r"reserves are money only banks can hold: their accounts at the Fed. Buying a bond from a bank "
                          r"credits its reserves; the Fed creates them by typing", 12.0, 21, GREY_A),
            wrapped_label(r"the policy rate is the price of overnight money between them: the federal funds rate, a "
                          r"target range set eight times a year by the FOMC", 12.0, 21, POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Start with the central bank's own balance sheet. On one side, what it owns: mostly Treasuries and "
            "government-backed mortgage bonds. On the other, what it owes: the currency in your wallet, and reserves, "
            "which are the deposits that banks keep at the Fed. <bookmark mark='a'/> When the Fed buys a bond from a "
            "bank, it pays by crediting that bank's reserve account. It creates the money by typing. "
            "<bookmark mark='b'/> Banks lend reserves to each other overnight, and the interest rate on those loans "
            "is the federal funds rate: the policy rate. Eight times a year the Federal Open Market Committee sets a "
            "target range for it. The question is how a committee makes a market rate obey."
        ) as vo:
            self.play(FadeIn(title), Create(top), Create(mid))
            self.play(FadeIn(assets), FadeIn(liab))
            vo.wait_until("a")
            self.play(Indicate(assets[1][0]), Indicate(liab[1][1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def demand(self, p):
        f = p["floor"]
        t, R, s = np.asarray(f["t"]), np.asarray(f["reserves"]), np.asarray(f["spread_bp"])
        g = axes([0, 4500], [-40, 160], x_length=6.6, y_length=4.4, xlabel=r"bank reserves, \$ bn",
                 ylabel=r"fed funds minus the rate on reserves, bp", xticks=[0, 1000, 2000, 3000, 4000],
                 yticks=[-40, 0, 40, 80, 120, 160], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        Rs = np.linspace(5, 4500, 300)
        dem = 150 * np.exp(-Rs / 250) - 8  # illustrative: steep when scarce, flat when ample
        dc = curve(ax, Rs, dem, GREY_B, stroke_width=3)
        corridor = VGroup(Line(ax.c2p(40, -40), ax.c2p(40, 160), color=POLICY, stroke_width=3),
                          label(r"scarce: the Fed shifts supply", font_size=16, color=POLICY).next_to(
                              ax.c2p(60, 140), RIGHT, buff=0.1))
        floorl = VGroup(Line(ax.c2p(3000, -40), ax.c2p(3000, 160), color=IORB_C, stroke_width=3),
                        label(r"ample: the floor", font_size=16, color=IORB_C).next_to(ax.c2p(3000, 140), RIGHT,
                                                                                         buff=0.1))
        cols = [interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), (tt - t[0]) / (t[-1] - t[0])) for tt in t]
        dots = VGroup(*[Dot(ax.c2p(r_, s_), radius=0.03, color=c_, fill_opacity=0.8)
                        for r_, s_, c_ in zip(R[::2], s[::2], cols[::2])])
        rows = [cmath(r"i_{ff} - \text{IORB}", r"=", r"f(R),\quad f' < 0,\quad f(R) \to \text{small for large } R",
                      font_size=30, colors={r"i_{ff} - \text{IORB}": MKT}),
                cmath(r"\text{RRP} \le i_{ff}", r"\lesssim", r"\text{IORB}", font_size=32, colors={r"\text{IORB}": IORB_C})]
        side = VGroup(
            rows[0], wrapped_label(r"Poole (1968): banks' demand for reserves slopes down. Scarce reserves sit on the "
                                   r"steep part, where a small change in supply moves the rate", 5.4, 18, GREY_A),
            rows[1], wrapped_label(r"since 2008 the Fed pays interest on reserves (IORB since July 2021) and, through "
                                   r"the overnight reverse repo, lends money-market funds a floor of their own", 5.4, 18,
                                   GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        leg = label(r"dots: every week, 2009 (blue) to 2025 (pink)", font_size=16, color=GREY_B).next_to(g, UP, buff=0.05)
        with self.voiceover(
            "Before 2008 it worked by scarcity. Banks need reserves, and their demand for them slopes down: the scarcer "
            "reserves are, the more a bank will pay to borrow them overnight. William Poole wrote it down in 1968. "
            "<bookmark mark='a'/> With reserves scarce, the system sits on the steep part of that curve, and the Fed's "
            "trading desk hits the target by adding or draining a few billion dollars a day. <bookmark mark='b'/> Then "
            "the crisis flooded the system with reserves, and the Fed began paying interest on them. Now the system "
            "sits on the flat part, the floor, and the rate is set by what the Fed pays: interest on reserve balances "
            "for banks, and the overnight reverse repo rate for money-market funds, which cannot hold reserves. "
            "<bookmark mark='c'/> Here is every week since 2009: reserves against the gap between the funds rate and "
            "the rate on reserves. It never strays more than a few basis points from the floor."
        ) as vo:
            self.play(FadeIn(g), Create(dc), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(corridor))
            vo.wait_until("b")
            self.play(FadeIn(floorl), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=3), FadeIn(leg))
        self.add(illustration(r"curve: illustrative; dots: FRED (WRESBAL, DFF, IOER, IORB)"))
        self.wait(0.5)
        self.clear_scene()

    def rates(self, p):
        g = axes([2007, 2026], [0, 6], x_length=9.0, y_length=4.4, xlabel=r"year", ylabel=r"percent",
                 xticks=[2008, 2012, 2016, 2020, 2024], yticks=[0, 2, 4, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        lo, hi = p["DFEDTARL"], p["DFEDTARU"]
        tl, vl, vh = np.asarray(lo["t"]), np.asarray(lo["v"]), np.asarray(hi["v"])
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(tl, vh)], *[ax.c2p(a, b) for a, b in zip(tl[::-1], vl[::-1])],
                       stroke_width=0, fill_color=BAND_C, fill_opacity=0.25)
        old = curve(ax, np.asarray(p["DFEDTAR"]["t"]), np.asarray(p["DFEDTAR"]["v"]), BAND_C, stroke_width=3)
        io = VGroup(curve(ax, np.asarray(p["IOER"]["t"]), np.asarray(p["IOER"]["v"]), IORB_C, stroke_width=2.5),
                    curve(ax, np.asarray(p["IORB"]["t"]), np.asarray(p["IORB"]["v"]), IORB_C, stroke_width=2.5))
        rrp = curve(ax, np.asarray(p["RRPONTSYAWARD"]["t"]), np.asarray(p["RRPONTSYAWARD"]["v"]), RRP_C, stroke_width=2.5)
        ff = curve(ax, np.asarray(p["DFF"]["t"]), np.asarray(p["DFF"]["v"]), MKT, stroke_width=2)
        so = curve(ax, np.asarray(p["SOFR"]["t"]), np.asarray(p["SOFR"]["v"]), QC.SPOT, stroke_width=1.6)
        leg = legend([(BAND_C, r"target (range since Dec 2008)"), (IORB_C, r"interest on reserves"),
                      (RRP_C, r"overnight reverse repo rate"), (MKT, r"effective fed funds"), (QC.SPOT, r"SOFR (repo)")],
                     font_size=17).to_edge(RIGHT, buff=0.35).shift(UP * 1.0)
        zoom = wrapped_label(r"2022--23: 525 bp of hikes in sixteen months; the market rate moved with the administered "
                             r"ones, every meeting, to the basis point", 3.2, 18, GREY_A).next_to(leg, DOWN, buff=0.4,
                                                                                         aligned_edge=LEFT)
        with self.voiceover(
            "And here is the floor at work, every week since 2007. Before December 2008 the target was a single "
            "number; since then it has been a quarter-point range, shaded in yellow. <bookmark mark='a'/> Interest on "
            "reserves, in pink, sits inside the range. The overnight reverse repo rate, in teal, sits at its bottom. "
            "<bookmark mark='b'/> And the market rates, the effective funds rate in white and the repo rate, SOFR, in "
            "blue, live between them. <bookmark mark='c'/> In 2022 and 2023 the Fed raised rates by five and a quarter "
            "points in sixteen months, and the market followed, meeting by meeting. It did not need to drain a single "
            "dollar of reserves to do it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band), Create(old), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(io), Create(rrp), FadeIn(leg[1]), FadeIn(leg[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ff), Create(so), FadeIn(leg[3]), FadeIn(leg[4]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(zoom))
        q = ask(r"why does fed funds trade below the rate the Fed pays banks on reserves?")
        with self.voiceover(
            "A puzzle before we move on. The funds rate has mostly traded a few basis points below interest on "
            "reserves. Why would anyone lend reserves for less than the Fed pays to hold them? Chapter thirteen's "
            "plumbing has the answer."
        ):
            self.play(FadeOut(zoom), FadeIn(q))
        self.add(illustration(r"FRED: DFEDTAR, DFEDTARL/U, IOER, IORB, RRPONTSYAWARD, DFF, SOFR; weekly"))
        self.wait(0.5)
        self.clear_scene()
