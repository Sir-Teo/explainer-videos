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
        l1 = VGroup(label(r"eligible Treasury collateral", font_size=19, color=ZERO).next_to(d1[0], UP, buff=0.08),
                    label(r"cash, less a haircut", font_size=19, color=MKT).next_to(d1[1], DOWN, buff=0.08))
        notes = VGroup(
            wrapped_label(r"At repurchase, cash plus agreed interest is returned. The annualized rate depends on the term and day-count convention; collateral does not remove counterparty or liquidity risk", 12.0, 21, GREY_A),
            wrapped_label(r"General collateral: securities within an agreed eligible basket are substitutable. Special: a particular issue is sought and can fund below GC. Specialness = GC rate minus special rate", 12.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Repo is one way to finance a bond position. A dealer sells eligible collateral for cash and agrees to repurchase it later. In this overnight example, the repurchase amount includes agreed interest; the repo quote annualizes it under a day-count convention. <bookmark mark='a'/> A haircut provides a collateral buffer, but counterparty, valuation, rollover and liquidity risks remain. <bookmark mark='b'/> In general-collateral repo, securities in an agreed basket are substitutable. A specific issue sought by short sellers may instead trade special, at a rate below general collateral. That lowers the owner's financing cost relative to GC; it is not a guaranteed extra return independent of price and financing conditions."
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
            wrapped_label(r"Federal Home Loan Banks have been major federal-funds lenders under ample reserves; they hold Fed accounts but do not earn interest on reserve balances", 11.6, 22, GREY_A),
            wrapped_label(r"eligible banks can borrow below reserve remuneration and hold funds at the Fed; the gross gap faces costs and access limits", 11.6, 22, GREY_A),
            wrapped_label(r"Balance-sheet costs, regulatory charges, credit limits and segmented access can sustain a gross spread; it is not unlimited net profit", 11.6, 22, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Federal Home Loan Banks have been major federal-funds lenders in the ample-reserves system. They can hold Federal Reserve accounts but do not earn interest on reserve balances. <bookmark mark='a'/> Eligible banks can borrow below their reserve remuneration and hold the funds at the Fed. The gross gap is not all profit. <bookmark mark='b'/> Balance-sheet capacity, regulatory charges, credit limits and market segmentation constrain competition. These frictions help explain a persistent spread, without implying a universal fixed gap or a risk-free unlimited trade."
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
            wrapped_label(r"published by the New York Fed since April 2018; a transaction-based volume-weighted median across specified Treasury repo market segments", 5.6, 19, GOOD),
            wrapped_label(r"30 June 2023: the last USD LIBOR panel ends; a synthetic version for old contracts stops "
                          r"after 30 September 2024", 5.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "LIBOR used panel-bank submissions about unsecured borrowing costs, with a trimmed average determining its settings. Manipulated submissions affected many loans and derivatives. <bookmark mark='a'/> On June twenty-seventh, 2012, Barclays agreed to penalties of two hundred million dollars to the CFTC, a hundred sixty million to the Justice Department, and fifty-nine-point-five million pounds to Britain's FSA. <bookmark mark='b'/> In 2017 the Alternative Reference Rates Committee selected SOFR. The New York Fed began publishing this transaction-based volume-weighted median of specified overnight Treasury repo segments in April 2018. It is secured and overnight, so it is not economically identical to term unsecured LIBOR. <bookmark mark='c'/> The dollar bank panel ended June thirtieth, 2023; the remaining synthetic dollar settings ended after their final publication on September thirtieth, 2024."
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
        g = axes([2018.2, 2026], [-0.2, 6], x_length=8.4, y_length=2.9, xlabel=r"start of approximate 91-day window",
                 ylabel=r"percent", xticks=[2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6], font_size=14).to_edge(
            DOWN, buff=0.95).to_edge(LEFT, buff=0.6)
        ax = g.ax
        l_s = curve(ax, t, so, MKT, stroke_width=2)
        l_a = curve(ax, t, ar, ARR, stroke_width=2.5)
        l_b = curve(ax, t, bi, BILL, stroke_width=2)
        leg = legend([(MKT, r"SOFR on the first day"), (ARR, r"realized SOFR, approx. 91 days in arrears"),
                      (BILL, r"3-month bill bank-discount quote at start")], font_size=16).next_to(g, RIGHT, buff=0.25).shift(UP * 0.8)
        note_ = wrapped_label(rf"91--94-day full-fixing windows. March 2022--July 2023 start dates: realized rate averaged {s['gap_hikes_bp']:.0f} bp above the first "
                              rf"SOFR fixing; whole sample, {s['gap_all_bp']:.0f} bp. The spike: "
                              rf"{s['sep2019']['max']:.2f}\% on 17 September 2019 (Part 2)", 3.4, 16, GREY_A).next_to(
            leg, DOWN, buff=0.3, aligned_edge=LEFT)
        credit = illustration(r"FRED: SOFR, DTB3; daily, sampled weekly")
        with self.voiceover(
            f"A compounded-in-arrears rate uses realized overnight fixings weighted by their calendar-day accruals. It becomes known near the end, subject to the contract's publication, lookback and payment rules. <bookmark mark='a'/> This retrospective example targets ninety-one days, but keeps complete fixing intervals, making some windows ninety-two or ninety-four days. It is not an exact standard quarterly contract schedule. A constant overnight rate also produces a small compounding uplift, rather than exact equality with its annualized simple quote. <bookmark mark='b'/> For start dates from March 2022 through July 2023, the realized period rate averages {s['gap_hikes_bp']:.0f} basis points above the start fixing. It uses future realized observations, not a forecast known then. The bill series is a bank-discount quote, with different conventions and liquidity; it cannot be read as a pure forecast of future SOFR or compared directly without conversion."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(l_s), Create(l_a), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_b), FadeIn(leg[2]), FadeIn(note_), FadeIn(credit), run_time=2)
        self.play(FadeOut(credit), run_time=0.3)
        q = ask(r"in arrears, a borrower learns the quarter's rate only at its end. How does it budget, and what did "
                r"the market invent for that?")
        with self.voiceover("If you learn the rate only at the end of the quarter, how do you budget? And what did the "
                            "market invent for that?"):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Forward-looking term SOFR can set eligible contracts in advance from derivatives markets. Advance averages and fixed-rate hedges offer other trade-offs; none guarantees the future realized overnight rate.", 11.8, 26, GOOD).move_to(ORIGIN)
        with self.voiceover("Forward-looking term SOFR can set eligible contracts in advance using derivatives markets. Advance averages or a fixed-rate hedge offer other trade-offs. None guarantees the future realized overnight rate."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
