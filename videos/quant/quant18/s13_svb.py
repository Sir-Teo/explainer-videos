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
        c = chapter_card(18, r"March 2023: Silicon Valley Bank", r"How does the safest asset sink a bank?", lit=(2023,),
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
            label(r"31 December 2022, from the 10-K", font_size=21, color=GREY_A),
            wrapped_label(rf"held-to-maturity bonds: \${H20:.1f} bn at the end of 2020, \${H21:.1f} bn a year later: "
                          r"deposits from a venture-capital boom, invested when yields were near their lows", 5.4, 19,
                          ZERO),
            wrapped_label(r"weighted-average duration 6.2 years, mostly agency mortgage bonds of 10 years or more "
                          r"(Fed review)", 5.4, 19, GREY_A),
            wrapped_label(rf"{r['uninsured_share']}\% of deposits uninsured: over the \$250{{,}}000 limit, mostly start-ups' "
                          r"operating cash", 5.4, 19, QC.OPTION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Silicon Valley Bank's balance sheet at the end of 2022, from its annual report. On the left, its assets: "
            f"{A:.0f} billion dollars, of which {H:.0f} billion were bonds classified as held to maturity. "
            "<bookmark mark='a'/> Two years earlier that pile was seventeen billion. Venture capital poured deposits "
            "into the bank in 2020 and 2021, and the bank bought long bonds with them, at some of the lowest yields in "
            "history. Their duration was six point two years. <bookmark mark='b'/> On the right, what it owed: "
            f"deposits of {D:.0f} billion, {r['uninsured_share']} percent of them above the insurance limit, mostly "
            "the operating cash of start-ups. And a thin slice of equity."
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
            legend([(BAD, r"loss on the held-to-maturity book, estimated"), (GOOD, r"equity on the balance sheet")],
                   font_size=17),
            wrapped_label(rf"white dot: the loss the 10-K reported, \${rep:.2f} bn", 4.0, 18, WHITE),
            wrapped_label(r"held to maturity, at amortized cost: the loss stays off the income statement and out of "
                          r"regulatory capital. The books said the bank was fine", 4.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now the hook's chart, read properly. In red, the estimated loss on that book, day by day: duration times "
            "the change in the six-year yield times the book. <bookmark mark='a'/> In green, the bank's equity. By the "
            "middle of October 2022 the estimate had reached it, and it stayed close for the rest of the year. The white dot is the loss the bank itself reported for the end "
            f"of the year: {rep:.2f} billion, against equity of {EQ:.2f}. <bookmark mark='b'/> Because the bonds were "
            "held to maturity, at amortized cost, the loss ran through neither its earnings nor its regulatory capital. "
            "On paper the bank was well capitalized. At market prices it was "
            "close to worthless."
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
        after = wrapped_label(r"12 March: the Fed's Bank Term Funding Program lends to any bank for up to a year against "
                              r"Treasuries and agency bonds valued at par, not at market: the duration loss, lent "
                              r"against at face value", 12.0, 21, GOOD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The end took three days. On the eighth of March the bank sold twenty-one billion of its other bonds at a "
            "loss of one point eight billion, to raise cash, and announced it would raise capital. "
            "<bookmark mark='a'/> Its depositors read that as a confession. On the ninth they withdrew over forty "
            "billion dollars, coordinated through the same venture-capital networks that had brought the money in. "
            "<bookmark mark='b'/> The bank expected over a hundred billion more the next day, about "
            f"{r['deposit_base_share_run']} percent of its deposits in two days, and on the tenth California closed it. "
            "<bookmark mark='c'/> Two days later the Fed opened a facility that lends to banks against Treasuries and "
            "agency bonds valued at par: at face value, as if the duration loss did not exist."
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
            wrapped_label(r"asset side: a default-free book with a duration of six years, unhedged, funded by deposits "
                          r"that could leave in a day. The Fed's review: the bank removed interest rate hedges as rates "
                          r"rose", 11.6, 21, GREY_A),
            wrapped_label(r"liability side: uninsured deposits behave like overnight money in a panic, whatever their "
                          r"history says", 11.6, 21, GREY_A),
            wrapped_label(r"system: Jiang, Matvos, Piskorski and Seru mark US banks' assets to market for the rise in "
                          r"rates from early 2022 to early 2023: an average fall of 10\%, about \$2 trillion", 11.6, 21,
                          GREY_A),
            wrapped_label(r"the measure that would have shown it: the economic value of equity under a rate shock, "
                          r"with key-rate DV01s for assets and a realistic duration for deposits", 11.6, 21, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What does the record show? On the asset side, a book with no credit risk and a duration of six years, "
            "unhedged; the Fed's review found the bank had removed its interest rate hedges as rates rose. "
            "<bookmark mark='a'/> On the liability side, deposits that had looked stable for years and left in a day. "
            "<bookmark mark='b'/> And it was not alone: marking every American bank's assets to market for the rise in "
            "rates, Erica Jiang and coauthors found an average fall of ten percent, about two trillion dollars. "
            "<bookmark mark='c'/> The measure that shows all this is the economic value of equity under a rate shock, "
            "computed with key-rate DV01s, which is exactly what this part has built."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        q = ask(r"SVB's assets could not default. What number should its risk report have put at the top of page one?")
        with self.voiceover("Its assets could not default. What number should have been at the top of its risk report?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
