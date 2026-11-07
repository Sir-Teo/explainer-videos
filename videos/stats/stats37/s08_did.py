from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class DiD(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.picture()
        self.formula()
        self.debate()
        self.world()
        self.event()

    def card(self):
        card = chapter_card(7, r"Difference-in-differences", r"Two changes, \ subtracted", lit=(1855, 1994), part=PART)
        with self.voiceover("Chapter seven. Difference-in-differences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def story(self):
        rows = fit_rows(VGroup(
            label(r"Snow had a second argument: \ in 1849 both companies drew from the tidal Thames", font_size=26, color=GREY_A),
            label(r"Lambeth moved upstream in 1852; \ its customers' cholera fell, \ its rival's did not", font_size=26, color=Y0C),
            label(r"New Jersey, \ 1 April 1992: \ the minimum wage rises from \$4.25 to \$5.05", font_size=26, color=Y1C),
            label(r"Card \& Krueger survey 410 fast-food restaurants, \ before and after, \ in New Jersey and eastern Pennsylvania", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Snow had a second argument, about time. In the epidemic of 1849, both companies drew their "
            "water from the tidal Thames in London. <bookmark mark='b'/> Lambeth moved its intake upstream in 1852. Between "
            "the two epidemics, cholera fell among Lambeth's customers and not among its rival's: a change compared with a "
            "change. <bookmark mark='c'/> The design's modern classic: on the first of April 1992, New Jersey raised its "
            "minimum wage from four dollars twenty-five to five dollars five. Neighbouring Pennsylvania did not. <bookmark "
            "mark='d'/> David Card and Alan Krueger surveyed four hundred and ten fast-food restaurants on both sides of the "
            "border, before the rise and eight months after."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def picture(self):
        ck = museum.CARD_KRUEGER
        A = axes([-0.3, 1.3], [17, 25], x_length=6.4, y_length=4.4, xlabel=r"", ylabel=r"full-time-equivalent employees per store",
                 xticks=[], yticks=[18, 20, 22, 24], center=[-2.4, 0.2, 0])
        ax = A.ax
        lab = VGroup(label(r"Feb--Mar 1992", font_size=20, color=GREY_B).next_to(ax.c2p(0, 17), DOWN, buff=0.2),
                     label(r"Nov--Dec 1992", font_size=20, color=GREY_B).next_to(ax.c2p(1, 17), DOWN, buff=0.2))
        pa = VGroup(Line(ax.c2p(0, ck["PA"][0]), ax.c2p(1, ck["PA"][1]), color=Y0C, stroke_width=4),
                    Dot(ax.c2p(0, ck["PA"][0]), color=Y0C), Dot(ax.c2p(1, ck["PA"][1]), color=Y0C))
        nj = VGroup(Line(ax.c2p(0, ck["NJ"][0]), ax.c2p(1, ck["NJ"][1]), color=Y1C, stroke_width=4),
                    Dot(ax.c2p(0, ck["NJ"][0]), color=Y1C), Dot(ax.c2p(1, ck["NJ"][1]), color=Y1C))
        cf_end = ck["NJ"][0] + ck["PA"][1] - ck["PA"][0]
        cf = DashedLine(ax.c2p(0, ck["NJ"][0]), ax.c2p(1, cf_end), color=Y1C, stroke_width=3, stroke_opacity=0.6)
        arr = DoubleArrow(ax.c2p(1.12, cf_end), ax.c2p(1.12, ck["NJ"][1]), buff=0, color=TAUC, stroke_width=3, tip_length=0.12)
        side = fit_rows(VGroup(
            label(rf"Pennsylvania: \ {ck['PA'][0]:.2f} $\to$ {ck['PA'][1]:.2f}", font_size=22, color=Y0C),
            label(rf"New Jersey: \ {ck['NJ'][0]:.2f} $\to$ {ck['NJ'][1]:.2f}", font_size=22, color=Y1C),
            label(r"dashed: \ New Jersey had it moved like Pennsylvania", font_size=22, color=GREY_A),
            label(rf"the difference in differences: \ +{ck['NJ'][1] - ck['NJ'][0] - ck['PA'][1] + ck['PA'][0]:.2f}", font_size=22, color=TAUC),
        ), 4.4, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Employment per restaurant, in full-time equivalents. In Pennsylvania, without the "
            "rise, it fell from twenty-three point three to twenty-one point two: a regional slump. <bookmark "
            "mark='b'/> In New Jersey, with the higher minimum wage, it rose slightly, from twenty point four to "
            "twenty-one point zero. <bookmark mark='c'/> Had New Jersey followed Pennsylvania's path, it would have "
            "ended near eighteen point three. <bookmark mark='d'/> The difference between the two changes is plus two"
            " point seven five employees per store. The estimated comparison is positive, conditional on the design "
            "assumptions; this is not a universal conclusion about every minimum-wage policy."
        ) as vo:
            self.add(ck_tag())
            self.play(FadeIn(A), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(nj), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromCenter(arr), FadeIn(side[3]))
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"\hat\tau_{\text{DiD}}", r"=", r"(\bar Y_{T,\text{post}} - \bar Y_{T,\text{pre}}) - (\bar Y_{C,\text{post}} - \bar Y_{C,\text{pre}})", font_size=30),
            cmath(r"\text{assume}", r":", r"E[Y(0)_{\text{post}} - Y(0)_{\text{pre}} \mid T] = E[\,\cdot \mid C]", font_size=30),
            cmath(r"\Rightarrow", r":", r"\hat\tau_{\text{DiD}} \text{ estimates the ATT}", font_size=30),
            cmath(r"Y_{it}", r"=", r"\alpha_i + \gamma_t + \tau D_{it} + \varepsilon_{it}", font_size=30),
        ]
        rows[1][-1].set_color(Y0C)
        whys = [why(r"two changes"), why(r"parallel trends"), why(r"levels may differ, \ trends may not"),
                why(r"the regression version: \ two-way fixed effects")]
        with self.voiceover(
            "<bookmark mark='a'/> The estimator is the change among the treated minus the change among the controls. "
            "<bookmark mark='b'/> It assumes parallel trends: without the policy, the treated group's average "
            "untreated outcome would have changed by as much as the control group's did. <bookmark mark='c'/> With "
            "consistency, no anticipation and no relevant interference as well, the difference in differences "
            "identifies the average effect on the treated. The groups may differ in level, as New Jersey and "
            "Pennsylvania did; the levels cancel. Only the trends must agree. <bookmark mark='d'/> As a regression: a"
            " fixed effect for each unit, a fixed effect for each period, and the treatment indicator, which with two"
            " groups and two periods gives exactly the same number. With more periods and staggered adoption, chapter"
            " nine shows it does not."
        ) as vo:
            intro=label('Parallel trends and no anticipation identify a treated-group effect',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def debate(self):
        ck = museum.CARD_KRUEGER
        rows = fit_rows(VGroup(
            label(rf"Card \& Krueger: \ +{ck['did']:.2f} \ (SE {ck['se_did']:.2f}): \ no sign that jobs were lost", font_size=26, color=TAUC),
            label(r"against the textbook prediction that a price floor on labour reduces employment", font_size=26),
            label(r"Neumark \& Wascher (2000): \ payroll records give the opposite sign; \ Card \& Krueger (2000) reply", font_size=26, color=MISSC),
            label(r"the design made the disagreement about data and comparisons, \ not about models", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Card and Krueger reported a difference of plus two point seven six, with a standard error "
            "of one point three six. <bookmark mark='b'/> It went against the textbook prediction that a price floor on "
            "labour reduces employment, and it caused an uproar. <bookmark mark='c'/> David Neumark and William Wascher, "
            "using payroll records instead of telephone surveys, found the opposite sign; Card and Krueger replied with "
            "official employment data of their own. <bookmark mark='d'/> But the design changed the nature of the argument. "
            "It was about which data and which comparison group, things anyone could check, not about whose model was right."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def world(self):
        d = load("did")
        yrs = np.asarray(d["years"], float)
        p09, pN, cf = (np.asarray(d[k], float) for k in ("path09", "pathN", "cf09"))
        lo, hi = float(min(p09.min(), pN.min(), cf.min())) - 1, float(max(p09.max(), pN.max())) + 1
        A = axes([2000, 2019], [lo, hi], x_length=7.6, y_length=4.2, xlabel=r"year", ylabel=r"employment rate (\%)",
                 xticks=[2000, 2005, 2010, 2015], yticks=[round(lo + 1), round((lo + hi) / 2), round(hi - 1)],
                 xfmt=lambda v: f"{v:.0f}", center=[-1.8, 0.2, 0])
        ax = A.ax
        cN = polyline(ax, yrs, pN, Y0C, 3.5)
        c9 = polyline(ax, yrs, p09, Y1C, 3.5)
        k = yrs >= 2008
        ccf = polyline(ax, yrs[k], cf[k], Y1C, 2.5, opacity=0.5)
        start = DashedLine(ax.c2p(2009, lo), ax.c2p(2009, hi), color=GREY_B, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(rf"the World: \ {d['n09']} towns adopt a jobs programme in 2009", font_size=22, color=Y1C),
            label(rf"{d['nN']} towns never do", font_size=22, color=Y0C),
            label(r"faint red: \ the 2009 towns without it \ (the World knows)", font_size=22, color=GREY_A),
            label(rf"2009--13 vs 2008: \ DiD {d['two']:.2f}; \ truth {d['truth_two']:.2f}", font_size=22, color=TAUC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has a policy too. In 2009, " + str(d["n09"]) + " of its two hundred towns adopted "
            "a jobs programme. <bookmark mark='b'/> " + str(d["nN"]) + " towns never did. Their employment rates differ in "
            "level and share a common cycle. <bookmark mark='c'/> The World also knows what the 2009 towns would have done "
            "without the programme, the faint line: parallel to the never-treated towns, up to noise. <bookmark mark='d'/> "
            "Comparing 2009 to 2013 with 2008, the difference in differences is " + say(d["two"], 2) + " points; the truth for "
            "those years is " + say(d["truth_two"], 2) + "."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), Create(start))
            vo.wait_until("a")
            self.play(Create(c9), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cN), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ccf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def event(self):
        d = load("did")["ev09"]
        e = np.asarray(d["e"], float)
        att, se = np.asarray(d["att"], float), np.asarray(d["se"], float)
        truth = np.asarray(d["truth"], float)
        A = axes([-9, 10], [-1.5, 3.5], x_length=7.8, y_length=4.2, xlabel=r"years since adoption", ylabel=r"effect estimate",
                 xticks=[-8, -4, 0, 4, 8], yticks=[-1, 0, 1, 2, 3], center=[-1.8, 0.2, 0])
        ax = A.ax
        bnd = band(ax, e, att - 1.645 * se, att + 1.645 * se, Y1C, 0.18)
        est = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=Y1C) for a, b in zip(e, att)])
        tr = polyline(ax, e, truth, TRUEC, 2.5)
        zero = DashedLine(ax.c2p(-9, 0), ax.c2p(10, 0), color=GREY_C, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"an event study: \ one DiD per year, \ against 2008", font_size=22),
            label(r"leads (before 2009): \ a check on parallel trends", font_size=22, color=Y0C),
            label(r"lags: \ the effect builds, \ 0.3 a year", font_size=22, color=Y1C),
            label(r"gold: \ the truth", font_size=22, color=TRUEC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An event study repeats the comparison for every year, always against the year before "
            "adoption, and plots the estimates against years since adoption. <bookmark mark='b'/> The leads, before 2009, "
            "check parallel trends: they should be zero. Here they wander a little below zero, within their bands, as two "
            "groups of towns with persistent shocks will. <bookmark mark='c'/> The lags show the programme's effect building "
            "by about point three a year. <bookmark mark='d'/> They track the truth. Note how wide the bands are, with only "
            "twenty comparison towns; chapter ten asks what a lead that is not quite zero should do to our conclusions."
        ) as vo:
            self.add(rollout_tag())
            self.play(FadeIn(A), Create(zero), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bnd), FadeIn(est), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(tr), FadeIn(side[3]))
        self.clear_scene()
