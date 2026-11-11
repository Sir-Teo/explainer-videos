from __future__ import annotations

from explainer.quant import *  # noqa: F403
import numpy as np

from videos.quant.quant3.common import CASH, PART, load

IS_C = QC.IDEA


class Crisis(VoiceoverScene):
    def construct(self):
        self.card()
        ms = load("mscore")
        self.enron()
        self.wirecard()
        self.more_cases()
        self.beneish(ms)
        self.base_rate(ms)

    def card(self):
        c = chapter_card(16, r"When the statements lie", r"What do you do when the numbers are false?",
                         lit=(2001, 2020), part=PART)
        with self.voiceover("Chapter sixteen. When the statements lie."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def enron(self):
        card = crisis_card(r"8 November -- 2 December 2001", r"Enron",
                           r"America's seventh-largest company by revenue restated four years of earnings, then filed "
                           r"for what was then the largest bankruptcy in US history. Its auditor, Arthur Andersen, "
                           r"collapsed with it.",
                           stats=[(r"\$586\text{m}", r"earnings removed, 1997--2000, by the restatement"),
                                  (r"> \$5\text{bn}", r"loans booked as operating cash flow through ``prepays'', "
                                                      r"1997--2001 (SEC)")],
                           width=7.0)
        how = VGroup(
            label(r"how the statements were bent", font_size=24, color=GREY_A),
            wrapped_label(r"profits booked up front: long-term contracts marked to Enron's own models", 5.0, 21,
                          IS_C),
            wrapped_label(r"debt kept off the balance sheet in partnerships run by its own finance chief", 5.0, 21,
                          QC.CASH),
            wrapped_label(r"loans dressed as commodity trades, so borrowed cash appeared as cash from operations", 5.0,
                          21, CASH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(card, how).arrange(RIGHT, buff=0.6, aligned_edge=UP).scale_to_fit_width(13.2).move_to(ORIGIN)
        with self.voiceover(
            "On the eighth of November 2001 Enron, then America's seventh-largest company by revenue, restated four years of "
            "earnings, removing five hundred and eighty-six million dollars; on the second of December it filed for bankruptcy, the "
            "largest in American history to that day, and its auditor, Arthur Andersen, did not survive. <bookmark mark='a'/> Its "
            "statements had been bent in all three ledgers: profits booked up front from its own models, debt kept in partnerships "
            "run by its finance chief, <bookmark mark='b'/> and, according to the SEC, more than five billion dollars of loans "
            "dressed as commodity trades, so that borrowed money appeared as operating cash. Sloan's accrual signal compares "
            "earnings with cash; Enron had faked the cash too."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(how[0]), FadeIn(how[1]), FadeIn(how[2]))
            vo.wait_until("b")
            self.play(FadeIn(how[3]))
        self.wait(0.4)
        self.clear_scene()

    def wirecard(self):
        card = crisis_card(r"18 -- 25 June 2020", r"Wirecard",
                           r"A German payments company in the DAX told investors that cash held for it in trust "
                           r"accounts at two Philippine banks could not be confirmed; a week later it filed for "
                           r"insolvency. Its chief executive resigned and was arrested.",
                           stats=[(r"\text{EUR\,}1.9\text{bn}", r"cash that most likely did not exist"),
                                  (r"\approx 1/4", r"of its balance sheet")],
                           width=7.0)
        story = VGroup(
            label(r"the warnings were public", font_size=24, color=GREY_A),
            wrapped_label(r"2015--2019: the Financial Times reported irregularities, later from whistle-blowers in "
                          r"its Asian offices", 5.0, 21, GREY_A),
            wrapped_label(r"February 2019: the German regulator BaFin banned new short positions in Wirecard for two "
                          r"months, and filed a criminal complaint against FT journalists", 5.0, 21, QC.LOSS),
            wrapped_label(r"June 2020: the auditor, EY, refused to sign the 2019 accounts", 5.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(card, story).arrange(RIGHT, buff=0.6, aligned_edge=UP).scale_to_fit_width(13.2).move_to(ORIGIN)
        with self.voiceover(
            "Nineteen years later the story was told with cash itself. In June 2020 Wirecard, a German payments company in the DAX, "
            "said one point nine billion euros held for it in trust accounts in the Philippines, about a quarter of its balance "
            "sheet, could not be confirmed; within a week its chief executive had resigned and it was insolvent. "
            "<bookmark mark='a'/> The warnings had been public for years. The Financial Times had reported irregularities since "
            "2015, and in February 2019 the German regulator responded by banning new short positions in the shares and filing a "
            "criminal complaint against the reporters. Short sellers, who had been right, were treated as the threat."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in story], lag_ratio=0.5, run_time=5))
        self.wait(0.4)
        self.clear_scene()

    def more_cases(self):
        luckin = crisis_card(r"April 2019 -- January 2020", r"Luckin Coffee",
                             r"A Chinese coffee chain listed on Nasdaq. The SEC alleged that it fabricated more than "
                             r"\$300 million of retail sales and inflated its expenses to hide it. Luckin settled "
                             r"without admitting or denying the allegations.",
                             stats=[(r"> \$300\text{m}", r"retail sales fabricated (SEC complaint)"),
                                    (r"\$180\text{m}", r"penalty, 16 Dec.\ 2020")], width=6.3, font_size=22)
        khc = crisis_card(r"late 2015 -- 2018", r"Kraft Heinz",
                          r"The SEC found an expense-management scheme that inflated cost savings; the company "
                          r"restated in June 2019 and settled in 2021 without admitting or denying the findings.",
                          stats=[(r"\$208\text{m}", r"cost savings improperly recognised"),
                                 (r"\$62\text{m}", r"civil penalty")], width=6.3, font_size=22)
        VGroup(luckin, khc).arrange(RIGHT, buff=0.4, aligned_edge=UP).scale_to_fit_width(13.2).move_to(UP * 0.3)
        src = note(r"SEC press releases 2020-319 and 2021-174", font_size=18, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Two smaller cases, from the SEC's releases. Luckin Coffee, the SEC alleged, fabricated more than three hundred million "
            "dollars of retail sales in 2019; it paid a hundred and eighty million, without admitting or denying. "
            "<bookmark mark='a'/> And Kraft Heinz: about two hundred and eight million dollars of cost savings booked improperly, "
            "a sixty-two million penalty, also settled. Could ratios have flagged either?"
        ) as vo:
            self.play(FadeIn(luckin, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(khc, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def beneish(self, ms):
        terms = [("DSRI", r"days' sales in receivables"), ("GMI", r"gross margin, falling"), ("AQI", r"asset quality"),
                 ("SGI", r"sales growth"), ("DEPI", r"depreciation slowing"), ("SGAI", r"SG\&A rising"),
                 ("TATA", r"total accruals / assets"), ("LVGI", r"leverage rising")]
        from explainer.quant.house import valuation
        co = valuation.BENEISH
        form = MathTex(r"M = -4.84 + 0.920\,\text{DSRI} + 0.528\,\text{GMI} + 0.404\,\text{AQI} + 0.892\,\text{SGI}"
                       r" + 0.115\,\text{DEPI} - 0.172\,\text{SGAI} + 4.679\,\text{TATA} - 0.327\,\text{LVGI}",
                       font_size=27)
        if form.width > 13.0:  # the eight-term score is wider than the frame at this size
            form.scale_to_fit_width(13.0)
        form.to_edge(UP, buff=0.4)
        cap = label(r"Beneish (1999): fitted on 74 firms caught manipulating earnings against matched controls; "
                    r"flagged above $-1.78$", font_size=19, color=GREY_B).next_to(form, DOWN, buff=0.15)
        K = ms["khc"][-1]
        r_ = K["ratios"]
        g = VGroup()
        for i, (k, name) in enumerate(terms):
            neutral = 0.0 if k == "TATA" else 1.0
            c = co[k] * (r_[k] - neutral)
            w = float(np.clip(c * 6, -2.4, 2.4))
            bar = Rectangle(width=max(abs(w), 0.02), height=0.3, stroke_width=0,
                            fill_color=QC.LOSS if c > 0 else QC.GAIN, fill_opacity=0.85)
            bar.move_to([-2.4 + w / 2, 1.4 - 0.42 * i, 0])
            nm = label(rf"{k}: {name}", font_size=17, color=GREY_A).move_to([-6.0, 1.4 - 0.42 * i, 0], aligned_edge=LEFT)
            val = MathTex(rf"{r_[k]:.2f}", font_size=22, color=GREY_B).move_to([-2.4 + w + (0.35 if w >= 0 else -0.35),
                                                                               1.4 - 0.42 * i, 0])
            g.add(VGroup(nm, bar, val))
        axis = Line([-2.4, 1.65, 0], [-2.4, 1.4 - 0.42 * 7 - 0.25, 0], color=GREY_C, stroke_width=2)
        lab_ = label(r"Kraft Heinz FY2017, from its own 10-K: each term's push above a neutral firm", font_size=18,
                     color=GREY_B).next_to(axis, UP, buff=0.12)
        M = np.asarray(ms["m"])
        h = axes([-4, 0], [0, 1.0], x_length=4.6, y_length=3.2, xlabel=r"M-score", xticks=[-4, -3, -1],
                 xfmt=lambda v: f"{v:g}", yticks=[], font_size=16).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.9)
        hx = h.ax
        hist, edges = np.histogram(np.clip(M, -3.99, -0.01), bins=16, range=(-4, 0))
        hist = hist / hist.max()
        bars = VGroup(*[Rectangle(width=(hx.c2p(0.25, 0)[0] - hx.c2p(0, 0)[0]) * 0.9,
                                  height=max(hx.c2p(0, v * 0.9)[1] - hx.c2p(0, 0)[1], 0.002), stroke_width=0,
                                  fill_color=QC.SPOT, fill_opacity=0.75).move_to(hx.c2p(e + 0.125, 0), aligned_edge=DOWN)
                        for e, v in zip(edges[:-1], hist)])
        thr = DashedLine(hx.c2p(-1.78, 0), hx.c2p(-1.78, 1.0), color=QC.LOSS, stroke_width=2)
        thr = VGroup(thr, MathTex(r"-1.78", font_size=22, color=QC.LOSS).next_to(thr.get_top(), RIGHT, buff=0.08)
                   .shift(DOWN * 0.15))
        kd = Dot(hx.c2p(K["m"], 0.05), radius=0.09, color=QC.HOUSE)
        kl = label(rf"Kraft Heinz 2017: {K['m']:.2f}", font_size=17, color=QC.HOUSE).next_to(kd, RIGHT, buff=0.15).shift(UP * 0.35)
        res = label(rf"{ms['n']} firm-years of 7 large firms: {100 * ms['share_flagged']:.1f}\% flagged", font_size=19,
                    color=GREY_A).next_to(h, UP, buff=0.2)
        miss = label(r"a screen, not a test: no fraud labels; missing inputs set to neutral", font_size=16,
                     color=GREY_B).next_to(h, DOWN, buff=0.15)
        with self.voiceover(
            "In 1999 Messod Beneish built a screen. He took seventy-four firms caught manipulating their earnings, matched them with "
            "controls, and fitted a probit on eight ratios from the statements. <bookmark mark='a'/> Receivables growing faster than "
            "sales. Margins falling. More assets that are neither current nor plant. Fast sales growth. Depreciation slowing. "
            "Overheads rising. Total accruals, with by far the largest weight, Sloan's signal again. And leverage. Above minus one "
            "point seven eight, the firm is flagged. <bookmark mark='b'/> Here is Kraft Heinz's 2017, computed from the numbers in "
            "its own 10-K: each bar is how far one term pushes the score above a neutral firm. Accruals push hardest. "
            f"<bookmark mark='c'/> The score is {K['m']:.2f}, just below the line; it was not flagged. Across the seven large firms "
            f"in the store, {100 * ms['share_flagged']:.1f} percent of firm-years cross it. A scheme of a couple of hundred million "
            "dollars spread over three years, in a company of Kraft Heinz's size, is too small for ratios to see."
        ) as vo:
            self.play(FadeIn(form), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(lab_), LaggedStart(*[FadeIn(x[0]) for x in g], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(x[1], LEFT if x[1].get_x() > -2.4 else RIGHT) for x in g],
                                  lag_ratio=0.15), LaggedStart(*[FadeIn(x[2]) for x in g], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(h), FadeIn(bars), Create(thr), FadeIn(res), FadeIn(miss))
            self.play(FadeIn(kd, scale=1.5), FadeIn(kl))
        self.wait(0.4)
        self.clear_scene()

    def base_rate(self, ms):
        b = ms["base_rate"]
        grid = VGroup()
        n = 100
        flagged = int(round(b["flag"] * 1000))
        for i in range(1000):
            grid.add(Square(0.1, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9))
        grid.arrange_in_grid(rows=20, cols=50, buff=0.03).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        frauds = list(range(0, 10))
        caught = frauds[:5]
        false_flags = list(range(10, 10 + flagged - len(caught)))
        pp = desk_question(r"Pause and predict: a screen flags 15\% of firms. 1\% commit fraud, and the screen catches "
                           r"half of them. What share of flagged firms are frauds?", width=5.4, font_size=21)
        pp.to_edge(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        ans = VGroup(MathTex(r"\frac{0.01 \times 0.5}{0.15}", r"=", rf"{100 * b['ppv']:.1f}\%", font_size=40,
                             color=QC.HOUSE),
                     wrapped_label(r"Bayes: when the base rate is low, most flags are false; Dechow, Ge, Larson and Sloan "
                                   r"(2011) trained a successor, the F-score, on SEC enforcement cases", 5.2, 20, GREY_A))
        ans.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(pp, DOWN, buff=0.4)
        leg = legend([(QC.LOSS, r"a fraud the screen catches"), (QC.IDEA, r"a fraud it misses"),
                      (QC.SPOT, r"an honest firm flagged")], font_size=18).next_to(grid, UP, buff=0.2).align_to(grid, LEFT)
        with self.voiceover(
            "Even a good screen has a problem, and it is arithmetic. Pause and predict: a screen flags fifteen percent of firms. One "
            "percent of firms commit fraud, and the screen catches half of them. What share of the flagged firms are frauds? "
            f"<bookmark mark='a'/> Here are a thousand firms. Ten are frauds; five are caught, five missed. And {flagged - 5} honest "
            f"firms are flagged with them. <bookmark mark='b'/> So {100 * b['ppv']:.1f} percent of the flags are frauds. When the "
            "base rate is low, most alarms are false. Patricia Dechow and coauthors trained a successor in 2011, the F-score, on the "
            "SEC's enforcement cases; it faces the same arithmetic. So the House treats a screen as a reason to read the filing, and "
            "stores every number as first reported, because a backtest on corrected numbers knows what nobody knew."
            " Next: the people whose job is to read these statements and put a value on firms."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeIn(leg), *[grid[i].animate.set_fill(QC.LOSS) for i in caught],
                      *[grid[i].animate.set_fill(QC.IDEA) for i in frauds[5:]])
            self.play(LaggedStart(*[grid[i].animate.set_fill(QC.SPOT) for i in false_flags], lag_ratio=0.01,
                                  run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
