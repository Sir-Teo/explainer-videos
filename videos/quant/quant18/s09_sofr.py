from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, MKT, PART, ZERO, ask, illustration, load

ARR = QC.DELTA
BILL = QC.REALIZED


class SOFR(VoiceoverScene):
    def construct(self):
        s = load("sofr")
        self.card()
        self.repo()
        self.puzzle()
        self.libor()
        self.arrears(s)

    def card(self):
        c = chapter_card(13, r"Repo, SOFR and the end of LIBOR", r"What is the floating rate, and who sets it?",
                         part=PART)
        with self.voiceover("Chapter thirteen. Repo, SOFR, and the end of LIBOR."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def repo(self):
        a = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.15, color=ZERO).shift(LEFT * 4 + UP * 1.2)
        b = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.15, color=MKT).shift(RIGHT * 4 + UP * 1.2)
        ta = label(r"dealer (needs cash)", font_size=22, color=ZERO).move_to(a)
        tb = label(r"money fund (has cash)", font_size=22, color=MKT).move_to(b)
        d1 = VGroup(Arrow(a.get_right() + UP * 0.3, b.get_left() + UP * 0.3, buff=0.1, color=ZERO),
                    Arrow(b.get_left() + DOWN * 0.3, a.get_right() + DOWN * 0.3, buff=0.1, color=MKT))
        l1 = VGroup(label(r"today: a Treasury as collateral", font_size=19, color=ZERO).next_to(d1[0], UP, buff=0.08),
                    label(r"today: cash, a little less than the bond's value (the haircut)", font_size=19,
                          color=MKT).next_to(d1[1], DOWN, buff=0.08))
        notes = VGroup(
            wrapped_label(r"tomorrow the dealer buys the bond back for the cash plus interest: the repo rate. A loan, "
                          r"secured by the safest collateral there is", 12.0, 21, GREY_A),
            wrapped_label(r"general collateral (GC): any Treasury will do. Special: lenders of cash want one particular "
                          r"bond, often the newest issue that short sellers must deliver, and accept a lower rate to "
                          r"get it. Specialness = GC rate minus the special rate", 12.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Underneath every bond position is the repo market. A dealer who owns a Treasury and needs cash sells it to "
            "a money-market fund today and agrees to buy it back tomorrow, for slightly more. <bookmark mark='a'/> The "
            "difference is the repo rate: interest on a one-day loan secured by the safest collateral there is. "
            "<bookmark mark='b'/> Most repo is general collateral: any Treasury will do. But when short sellers need "
            "one particular bond, often the newest ten-year, cash lenders accept a lower rate to get that bond. The "
            "bond is on special, and its owner earns the difference as extra income."
        ) as vo:
            self.play(Create(a), Create(b), FadeIn(ta), FadeIn(tb))
            self.play(GrowArrow(d1[0]), FadeIn(l1[0]), GrowArrow(d1[1]), FadeIn(l1[1]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self):
        head = label(r"Chapter one's puzzle: fed funds below interest on reserves", font_size=28).to_edge(UP, buff=0.6)
        body = VGroup(
            wrapped_label(r"most federal funds lending now comes from the Federal Home Loan Banks: government-sponsored "
                          r"lenders with accounts at the Fed that cannot earn interest on reserves", 11.6, 22, GREY_A),
            wrapped_label(r"they lend overnight to banks for a little less than the Fed pays banks; the banks deposit the "
                          r"cash at the Fed and keep the gap", 11.6, 22, GREY_A),
            wrapped_label(r"why the gap is not arbitraged to zero: the borrowed cash enlarges the bank's balance sheet, "
                          r"and balance sheet costs capital, the same limit as chapter 11's swap spread", 11.6, 22, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "This explains the puzzle from chapter one. Most lending in the federal funds market today comes from the "
            "Federal Home Loan Banks, government-sponsored lenders with accounts at the Fed but no right to interest on "
            "reserves. <bookmark mark='a'/> They lend overnight to banks a little below the rate on reserves; the banks "
            "park the cash at the Fed and keep the difference. <bookmark mark='b'/> Why doesn't competition push the "
            "gap to zero? Because the borrowing enlarges the bank's balance sheet, and balance sheet costs capital: the "
            "same limit to arbitrage as the negative swap spread."
        ) as vo:
            self.play(FadeIn(head), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1]))
            vo.wait_until("b")
            self.play(FadeIn(body[2]))
        self.wait(0.4)
        self.clear_scene()

    def libor(self):
        cc = crisis_card(r"2008--2012", r"LIBOR",
                         r"each morning a panel of banks said at what rate they could borrow unsecured; the average set "
                         r"the floating rate on hundreds of trillions of dollars of contracts. Traders asked submitters to "
                         r"move it. Barclays settled first, on 27 June 2012",
                         stats=[(r"\$200\,\text{m}", r"CFTC penalty"), (r"\$160\,\text{m}", r"Department of Justice"),
                                (r"\pounds 59.5\,\text{m}", r"FSA fine")], width=6.6, font_size=22)
        cc.to_edge(LEFT, buff=0.5)
        steps = VGroup(
            label(r"what replaced it", font_size=26),
            wrapped_label(r"2017: the Fed's Alternative Reference Rates Committee chooses SOFR, the Secured Overnight "
                          r"Financing Rate: the median rate, weighted by volume, of overnight Treasury repo", 5.6, 19,
                          GREY_A),
            wrapped_label(r"published by the New York Fed since April 2018; over \$3 trillion of trades a day in "
                          r"December 2025: transactions, not opinions", 5.6, 19, GOOD),
            wrapped_label(r"30 June 2023: the last USD LIBOR panel ends; a synthetic version for old contracts stops "
                          r"after 30 September 2024", 5.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "For decades the floating rate in most contracts was not repo. It was LIBOR: each morning, a panel of banks "
            "told an industry body at what rate they believed they could borrow unsecured, and the trimmed average "
            "became the rate on hundreds of trillions of dollars of loans and swaps. It was an opinion, and opinions "
            "can be bought: traders asked submitters to nudge it. <bookmark mark='a'/> In June 2012 Barclays settled "
            "first: two hundred million dollars to the CFTC, a hundred and sixty million to the Justice Department, "
            "fifty-nine and a half million pounds to Britain's FSA. Other banks followed. <bookmark mark='b'/> The "
            "replacement was chosen in 2017: SOFR, the median rate of overnight Treasury repo, computed from over three "
            "trillion dollars of actual trades a day. <bookmark mark='c'/> The last dollar LIBOR panel published on the "
            "thirtieth of June 2023."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(x) for x in cc.stats], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]))
        self.add(illustration(r"CFTC, DOJ and FSA releases, 27 June 2012; FCA, 3 July 2023; NY Fed SOFR volumes"))
        self.wait(0.4)
        self.clear_scene()

    def arrears(self, s):
        rows = [cmath(r"R_{[t, t+\delta]}", r"=", r"\Big(\prod_{i}\big(1 + r_i\,\tfrac{d_i}{360}\big) - 1\Big)\,\frac{360}{"
                      r"\sum_i d_i}", font_size=38, colors={r"R_{[t, t+\delta]}": ARR})]
        whys = [why(r"each day's SOFR $r_i$ applies for $d_i$ calendar days (three over a weekend), compounded: the "
                    r"period's rate is known only at its end. The House's \texttt{compound\_in\_arrears}")]
        step = ladder(self, rows, whys, keep=1, top=3.1, x=-2.6, buff=0.4, edge=6.9, highlight=False)
        t, so, ar, bi = (np.asarray(s[k]) for k in ("t", "sofr", "arrears", "bill"))
        g = axes([2018.2, 2026], [0, 6], x_length=8.4, y_length=3.6, xlabel=r"start of the 3-month period",
                 ylabel=r"percent", xticks=[2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6], font_size=14).to_edge(
            DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        ax = g.ax
        l_s = curve(ax, t, so, MKT, stroke_width=2)
        l_a = curve(ax, t, ar, ARR, stroke_width=2.5)
        l_b = curve(ax, t, bi, BILL, stroke_width=2)
        leg = legend([(MKT, r"SOFR on the first day"), (ARR, r"3 months of SOFR, compounded in arrears"),
                      (BILL, r"3-month bill yield on the first day")], font_size=16).next_to(g, RIGHT, buff=0.25).shift(UP * 0.8)
        note_ = wrapped_label(rf"March 2022 to July 2023: in arrears averaged {s['gap_hikes_bp']:.0f} bp above the first "
                              rf"day's SOFR; over the whole sample, {s['gap_all_bp']:.0f} bp. The spike: "
                              rf"{s['sep2019']['max']:.2f}\% on 17 September 2019 (Part 2)", 3.4, 16, GREY_A).next_to(
            leg, DOWN, buff=0.3, aligned_edge=LEFT)
        with self.voiceover(
            "LIBOR was a term rate: the three-month rate was known at the start of the three months. SOFR is "
            "overnight, so a three-month payment compounds each day's rate, and is known only at the end: compounded "
            "in arrears. <bookmark mark='a'/> Here is what that means in practice. In white, SOFR on the first day of "
            "each three-month period; in yellow, what the period actually paid. They agree when the Fed stands still. "
            "<bookmark mark='b'/> While the Fed hiked, from March 2022 to July 2023, the period paid "
            f"{s['gap_hikes_bp']:.0f} basis points more on average than the rate at its start: the borrower bears the "
            "hikes as they happen. The three-month bill, in teal, had priced them in advance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(l_s), Create(l_a), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_b), FadeIn(leg[2]), FadeIn(note_), run_time=2)
        q = ask(r"in arrears, a borrower learns the quarter's rate only at its end. How does it budget, and what did "
                r"the market invent for that?")
        with self.voiceover("If you learn the rate only at the end of the quarter, how do you budget? And what did the "
                            "market invent for that?"):
            self.play(FadeIn(q))
        self.add(illustration(r"FRED: SOFR, DTB3; daily, sampled weekly"))
        self.wait(0.5)
        self.clear_scene()
