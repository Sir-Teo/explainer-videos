from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


class Tables(VoiceoverScene):
    def construct(self):
        self.card()
        self.berkeley_table()
        self.chi2()
        self.measures()
        self.or_vs_rr()
        self.logistic_link()
        self.rxc()

    def card(self):
        card = chapter_card(7, r"Two-way tables", r"Counting by category, \ and comparing proportions", lit=(1900,), part=PART)
        with self.voiceover("Chapter seven. Two-way tables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def berkeley_table(self):
        d = load("tables")
        B = museum.BERKELEY
        ma, mr = sum(v[0] for v in B.values()), sum(v[1] for v in B.values())
        fa, fr = sum(v[2] for v in B.values()), sum(v[3] for v in B.values())
        tab = table_rows([[r"", r"admitted", r"rejected", r"total", r"share admitted"],
                          [r"men", rf"{ma:,}", rf"{mr:,}", rf"{ma + mr:,}", rf"{100 * d['men_rate']:.1f}\%"],
                          [r"women", rf"{fa:,}", rf"{fr:,}", rf"{fa + fr:,}", rf"{100 * d['women_rate']:.1f}\%"]],
                         font_size=30, col_buff=0.9, row_buff=0.35, colors=[GREY_B, MEN, WOMEN]).move_to([0, 1.2, 0])
        hc = history_card(1973, r"the University of California, \ Berkeley", r"graduate applications for the autumn: \ the six largest "
                          r"departments, \ 4,526 applicants. \ An associate dean, \ Eugene Hammel, \ worried about a lawsuit",
                          color=S.MUSEUM, width=10.0, font_size=22).move_to([0, -1.6, 0])
        tag = historical_tag(r"Bickel, \ Hammel \& O'Connell (1975)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> In the autumn of 1973, the graduate division of the University of California at Berkeley "
            "received thousands of applications. Here are the six largest departments together: of two thousand six hundred and "
            "ninety-one men, forty-four and a half percent were admitted; of one thousand eight hundred and thirty-five women, "
            "thirty point four percent. <bookmark mark='b'/> The graduate division's associate dean, Eugene Hammel, worried that the "
            "university could be sued for discrimination, asked the statistician Peter Bickel to look at the data. Their "
            "analysis, published in Science in 1975 with J. William O'Connell, is one of the most famous in statistics. We'll start where "
            "anyone would: with this table."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def chi2(self):
        d = load("tables")["pooled"]
        rows = [
            cmath(r"E_{ij}", r"=", r"\frac{(\text{row } i \text{ total})(\text{column } j \text{ total})}{n}", font_size=32),
            cmath(r"X^2", r"=", r"\sum_{ij}\frac{(O_{ij} - E_{ij})^2}{E_{ij}}", font_size=34),
            cmath(r"X^2", r"=", rf"{d['chi2']:.1f}\ \text{{on 1 df}}:\quad p = 8 \times 10^{{-22}}", font_size=32),
            cmath(r"\text{Fisher's exact test}", r":", r"p = 5 \times 10^{-22}", font_size=32),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the counts expected if sex and admission were independent"), why(r"Pearson (1900), \ Part 10"),
                why(r"$(r - 1)(c - 1) = 1$ degree of freedom"), why(r"conditioning on the margins (Part 10)")]
        intro = label('Compare observed counts with independence expectations', font_size=36)
        with self.voiceover(
            "Is admission independent of sex? <bookmark mark='a'/> If it were, each cell's expected count would be its row "
            "total times its column total, over the grand total. <bookmark mark='b'/> Pearson's chi-squared statistic, from Part "
            "10, adds up the squared gaps between observed and expected counts, each divided by the expected count. "
            "<bookmark mark='c'/> Here it's ninety-two, on one degree of freedom, a p-value of about ten to the minus "
            "twenty-one. <bookmark mark='d'/> Fisher's exact test, conditioning on the table's margins, agrees. Whatever is "
            "going on, these counts strongly disagree with the aggregate independence model. The question is what it is."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def measures(self):
        d = load("tables")["pooled"]
        rows = [
            cmath(r"\text{risk difference}", r"=", rf"p_1 - p_2 = {d['p1']:.3f} - {d['p2']:.3f} = {d['p1'] - d['p2']:.3f}", font_size=30),
            cmath(r"\text{relative risk}", r"=", rf"p_1/p_2 = {d['rr']:.2f}\ \ [{d['rr_ci'][0]:.2f},\ {d['rr_ci'][1]:.2f}]", font_size=30),
            cmath(r"\text{odds ratio}", r"=", rf"\frac{{ad}}{{bc}} = {d['or']:.2f}\ \ [{d['or_ci'][0]:.2f},\ {d['or_ci'][1]:.2f}]", font_size=30),
            cmath(r"\mathrm{SE}(\log \widehat{\text{OR}})", r"=", r"\sqrt{1/a + 1/b + 1/c + 1/d}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"14 percentage points"), why(r"men 1.47 times as likely to be admitted"),
                why(r"the odds of admission, \ men over women"), why(r"Woolf (1955): \ the interval on the log scale")]
        intro = label('Risk difference, risk ratio and odds ratio', font_size=36)
        with self.voiceover(
            "Three ways to say how different the two proportions are. <bookmark mark='a'/> The risk difference: forty-four and a "
            "half minus thirty point four, fourteen percentage points. <bookmark mark='b'/> The relative risk: men were one point "
            "four seven times as likely to be admitted. <bookmark mark='c'/> And the odds ratio: the odds of admission for men, "
            "divided by the odds for women, a d over b c in the table's letters: one point eight four. <bookmark mark='d'/> Its "
            "log has a simple standard error, the square root of the sum of the reciprocals of the four counts, which Barnet "
            "Woolf gave in 1955. Why have three measures, and why do statisticians love the odds ratio?"
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def or_vs_rr(self):
        p2 = np.linspace(0.005, 0.6, 200)
        A = axes([0, 0.6], [1, 3.2], x_length=7.0, y_length=4.2, xlabel=r"baseline risk $p_2$", ylabel=r"", xticks=[0, 0.2, 0.4, 0.6],
                 yticks=[1, 2, 3], center=[-2.4, 0.2, 0])
        ax = A.ax
        orr = 2.0
        odds1 = orr * p2 / (1 - p2)
        p1 = odds1 / (1 + odds1)
        c_or = curve(ax, p2, np.full_like(p2, orr), OBS, 3)
        c_rr = curve(ax, p2, p1 / p2, S.ALT, 3)
        rows = fit_rows(VGroup(
            label(r"hold the odds ratio at 2", font_size=24, color=OBS),
            label(r"the relative risk depends on the baseline", font_size=24, color=S.ALT),
            label(r"rare outcomes: \ OR $\approx$ RR", font_size=24),
            label(r"common outcomes: \ OR is farther from 1 than RR when OR $>1$", font_size=24, color=RES),
            label(r"but the OR survives case--control sampling: \ chapter ten", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hold the odds ratio fixed at two, and vary the baseline risk. <bookmark mark='b'/> The relative "
            "risk isn't fixed: <bookmark mark='c'/> when the outcome is rare, a few percent, the two nearly agree, <bookmark mark='d'/> "
            "but when it's common, an odds ratio of two can mean a relative risk of only one point three. Reporting an odds "
            "ratio as if it were a relative risk exaggerates effects on common outcomes, a classic error in medical "
            "journalism. <bookmark mark='e'/> So why use odds ratios at all? They're what logistic regression estimates, "
            "and, as chapter ten will show, they survive a way of collecting data that relative risks don't."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c_or), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c_rr), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def logistic_link(self):
        d = load("tables")
        rows = [
            cmath(r"\text{logit}\,P(\text{admit})", r"=", r"\beta_0 + \beta_1\,\text{woman}", font_size=32),
            cmath(r"\hat\beta_1", r"=", rf"{d['logit_women_pooled']:.3f}", font_size=34),
            cmath(r"e^{-\hat\beta_1}", r"=", rf"{np.exp(-d['logit_women_pooled']):.2f} = \text{{the table's odds ratio}}", font_size=32),
            cmath(r"\text{a } 2 \times 2 \text{ table}", r"=", r"\text{logistic regression on one dummy}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"one binary predictor"), why(r"women's log-odds, \ relative to men's"), why(r"exactly"),
                why(r"so more variables can join the model")]
        with self.voiceover(
            "<bookmark mark='a'/> The table is also a logistic regression: admission on a single dummy variable for women. "
            "<bookmark mark='b'/> The fitted coefficient is minus point six one, the difference in log-odds. "
            "<bookmark mark='c'/> Exponentiate its negative and you get one point eight four, the table's odds ratio, exactly. "
            "<bookmark mark='d'/> A two-by-two table is logistic regression on one dummy, and that's the door through which "
            "other variables can enter. At Berkeley, one variable changes everything."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rxc(self):
        d = load("tables")
        rows = [
            cmath(r"r \times c\ \text{table}", r":", r"X^2 = \sum_{ij}\frac{(O_{ij} - E_{ij})^2}{E_{ij}},\ \ (r - 1)(c - 1)\ \text{df}", font_size=30),
            cmath(r"\text{department} \times \text{admission}", r":", rf"X^2 = {d['chi_dept_admit']:.0f}\ \text{{on {d['df_rxc']} df}}", font_size=30),
            cmath(r"\text{sex} \times \text{department}", r":", rf"X^2 = {d['chi_sex_dept']:.0f}\ \text{{on {d['df_rxc']} df}}", font_size=30),
            cmath(r"\text{both enormous}", r":", r"\text{the department is tied to admission and to sex}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"asymptotic reference; sufficient expected counts"), why(r"departments admit at very different rates"),
                why(r"men and women applied to different departments"), why(r"the ingredients of the next chapter")]
        intro = label('Larger tables use the same independence comparison', font_size=36)
        with self.voiceover(
            "The chi-squared test isn't limited to two-by-two tables. <bookmark mark='a'/> For a table with r rows and c "
            "columns, the same sum has r minus one times c minus one degrees of freedom. <bookmark mark='b'/> Cross the six "
            "departments with admission: chi-squared of seven hundred and seventy-nine on five degrees of freedom. The "
            "departments admitted at wildly different rates. <bookmark mark='c'/> Cross sex with department: over a thousand. "
            "Men and women applied to very different departments. <bookmark mark='d'/> A variable tied strongly both to the "
            "outcome and to the group being compared: those are the ingredients of the next chapter."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
