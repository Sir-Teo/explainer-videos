from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, illustration, load


class SVB(VoiceoverScene):
    def construct(self):
        v = load("svb")
        self.card()
        self.sheet(v)
        self.mark(v)
        self.run(v)
        self.lessons(v)

    def card(self):
        c = chapter_card(18, r"March 2023: Silicon Valley Bank", r"How do duration and unstable funding interact?", lit=(2023,),
                         part=PART)
        with self.voiceover("Chapter eighteen. March 2023: Silicon Valley Bank, from the public record."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, v):
        f = v["facts"]
        r = v["review"]
        e = "2022-12-31"
        A, D, H, AFS, EQ = (f[k][e] for k in ("Assets", "Deposits", "HeldToMaturitySecurities",
                                              "AvailableForSaleSecuritiesDebtSecurities", "StockholdersEquity"))
        H21 = f["HeldToMaturitySecurities"]["2021-12-31"]
        H20 = f["HeldToMaturitySecurities"]["2020-12-31"]
        scale = 4.6 / A
        left = VGroup(
            Rectangle(width=2.6, height=H * scale, fill_color=ZERO, fill_opacity=0.7, stroke_width=0),
            Rectangle(width=2.6, height=AFS * scale, fill_color=QC.SPOT, fill_opacity=0.6, stroke_width=0),
            Rectangle(width=2.6, height=(A - H - AFS) * scale, fill_color=GREY_D, fill_opacity=0.7, stroke_width=0),
        ).arrange(UP, buff=0)
        right = VGroup(
            Rectangle(width=2.6, height=D * scale, fill_color=QC.OPTION, fill_opacity=0.6, stroke_width=0),
            Rectangle(width=2.6, height=(A - D - EQ) * scale, fill_color=GREY_D, fill_opacity=0.7, stroke_width=0),
            Rectangle(width=2.6, height=EQ * scale, fill_color=GOOD, fill_opacity=0.75, stroke_width=0),
        ).arrange(UP, buff=0)
        VGroup(left, right).arrange(RIGHT, buff=0.15, aligned_edge=DOWN).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        labs = VGroup(
            label(rf"held to maturity \${H:.1f} bn", font_size=17).move_to(left[0]),
            label(rf"available for sale \${AFS:.1f} bn", font_size=15).move_to(left[1]),
            label(r"loans, cash, other", font_size=15).move_to(left[2]),
            label(rf"deposits \${D:.1f} bn", font_size=17).move_to(right[0]),
            label(r"other", font_size=15).move_to(right[1]),
            label(rf"equity \${EQ:.1f} bn", font_size=15).move_to(right[2]),
        )
        heads = VGroup(label(rf"assets \${A:.1f} bn", font_size=20).next_to(left, UP, buff=0.15),
                       label(r"liabilities and equity", font_size=20).next_to(right, UP, buff=0.15))
        side = VGroup(
            label(r"SVB Financial Group, 31 December 2022 10-K", font_size=21, color=GREY_A),
            wrapped_label(rf"held-to-maturity bonds: \${H20:.1f} bn at the end of 2020, \${H21:.1f} bn a year later: "
                          r"deposits from a venture-capital boom, invested when yields were near their lows", 5.4, 19,
                          ZERO),
            wrapped_label(r"weighted-average duration 6.2 years, mostly agency mortgage bonds of 10 years or more "
                          r"(Fed review)", 5.4, 19, GREY_A),
            wrapped_label(rf"Fed review: about {r['uninsured_share']}\% uninsured deposits; concentrated clients and correlated withdrawal needs. "
                          r"", 5.4, 19, QC.OPTION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"These are consolidated SVB Financial Group figures from its 2022 ten-K, rather than a standalone bank balance sheet: assets of {A:.0f} billion dollars and held-to-maturity securities of {H:.0f} billion. <bookmark mark='a'/> The latter grew from about seventeen billion at year-end 2020. The Fed review describes predominantly agency mortgage-backed securities and a reported duration of six-point-two years. Low credit risk did not remove rate, prepayment or liquidity risk. <bookmark mark='b'/> Deposits were {D:.0f} billion. The review reports about {r['uninsured_share']} percent uninsured, with a concentrated client base and correlated cash needs. Insurance status and withdrawal behavior matter separately from the holding company's reported book equity."
        ) as vo:
            self.play(FadeIn(left), FadeIn(heads[0]), FadeIn(labs[:3]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(left[0], color=ZERO), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(heads[1]), FadeIn(labs[3:]), FadeIn(side[3]))
        self.add(illustration(r"EDGAR XBRL facts of SVB Financial Group's 2022 10-K; Federal Reserve review (April 2023)"))
        self.wait(0.4)
        self.clear_scene()

    def mark(self, v):
        f = v["facts"]
        t, mk = np.asarray(v["t"]), np.asarray(v["mark"])
        EQ = f["StockholdersEquity"]["2022-12-31"]
        rep = f["HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss"]["2022-12-31"]
        g = axes([2022, 2023.25], [-5, 20], x_length=8.2, y_length=4.4, xlabel=r"date",
                 ylabel=r"\$ bn", xticks=[2022, 2022.5, 2023], xfmt=lambda x: {2022: "2022", 2022.5: r"\text{mid-}2022",
                                                                              2023: "2023"}[x], yticks=[0, 5, 10, 15, 20],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        m = t <= 2023.25
        eq_line = DashedLine(ax.c2p(2022, EQ), ax.c2p(2023.25, EQ), color=GOOD, stroke_width=2.5)
        loss = curve(ax, t[m], mk[m], BAD, stroke_width=3)
        dot = Dot(ax.c2p(2023.0, rep), radius=0.08, color=WHITE)
        side = VGroup(
            legend([(BAD, r"constant-notional, constant-duration loss proxy"), (GOOD, r"holding-company 2022 year-end book equity")],
                   font_size=17),
            wrapped_label(rf"white dot: gross unrecognized HTM holding loss, \${rep:.2f} bn", 4.0, 18, WHITE),
            wrapped_label(r"HTM amortized-cost accounting generally excludes unrealized rate marks from earnings. This gross asset-side gap is not a full economic-equity valuation or a solvency test", 4.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"The red line is a deliberately simple proxy: fixed year-end 2022 HTM notional times six-point-two duration times the change in the six-year GSW yield since year-end 2021. We treat the reported duration as a modified-duration proxy, hold it constant and omit convexity, portfolio changes and mortgage prepayments. It is not the actual book's daily fair value. <bookmark mark='a'/> Green is fixed year-end holding-company book equity. The white dot is the ten-K's gross unrecognized HTM holding loss of {rep:.2f} billion, compared with equity of {EQ:.2f} billion. Tax treatment and balance-sheet scope differ. <bookmark mark='b'/> HTM amortized-cost treatment generally keeps unrealized interest-rate marks out of earnings. But comparing this gross asset gap to equity does not value loans, deposits, hedges or all other assets and liabilities. It neither proves complete economic insolvency nor makes the loss irrelevant to funding and liquidity."
        ) as vo:
            self.play(FadeIn(g), Create(loss), FadeIn(side[0][0]), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(eq_line), FadeIn(side[0][1]), FadeIn(dot), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def run(self, v):
        r = v["review"]
        days = VGroup(
            VGroup(label(r"8 March", font_size=26, color=QC.IDEA),
                   wrapped_label(rf"sells \${r['afs_sold_bn']} bn of available-for-sale bonds for a "
                                 rf"\${r['afs_loss_bn']} bn loss after tax; plans to raise \$2.25 bn of capital", 3.6, 19,
                                 GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"9 March", font_size=26, color=BAD),
                   wrapped_label(rf"depositors withdraw over \${r['outflow_mar9_bn']} bn in a day, coordinated through "
                                 r"venture-capital networks and social media", 3.6, 19, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15),
            VGroup(label(r"10 March", font_size=26, color=BAD),
                   wrapped_label(rf"management expects over \${r['expected_mar10_bn']} bn more: about "
                                 rf"{r['deposit_base_share_run']}\% of deposits in two days. California closes the bank",
                                 3.6, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(UP, buff=0.8)
        line = Line(days.get_left() + DOWN * 2.6, days.get_right() + DOWN * 2.6, color=GREY_C)
        after = wrapped_label(r"12 March 2023: BTFP announced for eligible depository institutions, against qualifying collateral owned on that date, valued at par. Liquidity loans, not a reversal of market losses; new lending ended 11 March 2024", 12.0, 21, GOOD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            f"On March eighth, 2023, the bank announced a roughly twenty-one-billion-dollar available-for-sale securities sale, a one-point-eight-billion after-tax loss and a capital-raising plan. <bookmark mark='a'/> The Fed review records more than forty billion dollars of deposit outflows on March ninth. <bookmark mark='b'/> Management expected over a hundred billion more the next day, making actual plus expected withdrawals about {r['deposit_base_share_run']} percent of the deposit base. Expected withdrawals are not all completed payments. California closed the bank on March tenth. <bookmark mark='c'/> On March twelfth, the Fed announced the BTFP for eligible depository institutions, with loans against qualifying collateral owned as of that date and valued at par. It supplied liquidity without erasing market losses or changing the bonds' cash flows. New BTFP lending ended in March 2024."
        ) as vo:
            self.play(FadeIn(days[0]))
            vo.wait_until("a")
            self.play(FadeIn(days[1]))
            vo.wait_until("b")
            self.play(FadeIn(days[2]))
            vo.wait_until("c")
            self.play(FadeIn(after))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self, v):
        rows = VGroup(
            label(r"What the public record shows", font_size=30),
            wrapped_label(r"Asset side: long-duration securities, predominantly agency MBS, plus other assets with different risks. The Fed review documents inadequate interest-rate risk management and reduced hedges", 11.6, 21, GREY_A),
            wrapped_label(r"liability side: uninsured deposits behave like overnight money in a panic, whatever their "
                          r"history says", 11.6, 21, GREY_A),
            wrapped_label(r"system: Jiang, Matvos, Piskorski and Seru mark US banks' assets to market for the rise in "
                          r"rates from early 2022 to early 2023: an average fall of 10\%, about \$2 trillion", 11.6, 21,
                          GREY_A),
            wrapped_label(r"Risk report: asset-and-liability economic-value scenarios, deposit behavior, basis and prepayment risk, and cash-flow liquidity stress. Selected local DV01s alone are incomplete", 11.6, 21, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.6)
        with self.voiceover(
            "The public record documents inadequate interest-rate and liquidity risk management, including reductions in interest-rate hedges. It does not say every asset was default-free or that every security had the same duration. <bookmark mark='a'/> Concentrated uninsured deposits can create correlated outflows. Their economic value and behavior require assumptions; uninsured status alone does not mathematically set deposit duration to zero. <bookmark mark='b'/> Jiang and coauthors estimate large systemwide asset mark-to-market losses from tightening, on the order of two trillion dollars. That is an asset valuation estimate under their methods, not a finding that all banks were insolvent. <bookmark mark='c'/> A useful report combines economic-value scenarios for assets and liabilities with deposit behavior and short-horizon liquidity stress. The local key-rate tools in this part support that work, but do not constitute a complete bank EVE or liquidity system."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        q = ask(r"For a long-duration book funded by concentrated runnable deposits, which value and liquidity measures belong together?")
        with self.voiceover('For a long-duration book funded by concentrated runnable deposits, which value and liquidity measures belong together?'):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Combine full asset-and-liability economic-value stress with available cash, usable collateral, withdrawal scenarios and funding capacity. Book capital or asset DV01 alone is insufficient.", 11.8, 26, GOOD).move_to(ORIGIN)
        with self.voiceover("Combine full asset-and-liability economic-value stress with available cash, usable collateral, withdrawal scenarios and funding capacity. Book capital or asset DV01 alone is insufficient."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
