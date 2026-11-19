from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403


class LaLonde(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The con, and LaLonde's test", r"Did the methods of the day get the right answer?",
             "Chapter six. The con, and LaLonde's test.", lit=("households", "government"), scale=("person",),
             horizon=("a year",))
        self.leamer()
        self.experiment()
        self.table()
        self.dehejia()
        self.called()

    def leamer(self):
        t = tables.LEAMER_1983.data
        who = history_card(r"1983", r"Edward Leamer, UCLA, \ ``Let's Take the Con out of Econometrics''",
                           r"in the \emph{American Economic Review}", color=NONEXP, width=7.4, font_size=25)
        who.to_edge(UP, buff=0.5)
        q1 = quote_card(t["quote"], r"Leamer (1983), p.\ 37", width=11.4, font_size=30, color=NONEXP)
        q2 = quote_card(t["birds"], r"Leamer (1983), p.\ 37", width=11.4, font_size=26, color=NONEXP)
        q1.next_to(who, DOWN, buff=0.45)
        q2.next_to(q1, DOWN, buff=0.3)
        tag = published_tag(r"E.\ E.\ Leamer, AER 73(1) (1983)", corner=DR, font_size=15)
        with self.voiceover(
            "By the early 1980s many economists had lost faith in their own regressions. <bookmark mark='a'/> In "
            "1983 Edward Leamer of UCLA published an article called Let's Take the Con out of Econometrics. "
            "<bookmark mark='b'/> Hardly anyone takes data analyses seriously, he wrote. Or perhaps more "
            "accurately, hardly anyone takes anyone else's data analyses seriously. <bookmark mark='c'/> His "
            "complaint was that results depended on which controls the researcher chose to include, and "
            "researchers reported only the specifications they liked: like elaborately plumed birds, he wrote, we "
            "preen and strut and display our t-values."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(who, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(who, color=NONEXP, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(q1, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(q2, shift=UP * 0.2))
        self.clear_scene()

    def experiment(self):
        la = load("lalonde")
        t5 = la["table5"]
        rows = VGroup(
            label(r"the National Supported Work Demonstration, \ the mid-1970s", font_size=28, color=EXP),
            label(r"hard-to-employ workers guaranteed a job for 9 to 18 months, \ in ten cities", font_size=24,
                  color=GREY_A),
            label(r"applicants assigned \emph{by lottery}: \ some got the programme, \ some did not", font_size=25),
            label(rf"men's 1978 earnings, \ programme minus lottery losers: \ \${t5['experiment'][0]:,}".replace(
                ",", "{,}"), font_size=28, color=EXP),
            label(r"Robert LaLonde, 1986: \ pretend there was no lottery", font_size=26, color=E.ACCENT),
            label(r"compare the trainees with men from national surveys \\ (the PSID, the CPS), \ "
                  r"and apply the methods of the day", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.2)
        tag = published_tag(r"R.\ J.\ LaLonde, AER 76(4) (1986)", corner=DR, font_size=15)
        with self.voiceover(
            "Three years later came the test. <bookmark mark='a'/> In the mid-1970s the United States ran a training "
            "programme called the National Supported Work Demonstration, which guaranteed hard-to-employ workers "
            "a job for nine to eighteen months, working in small crews. <bookmark mark='b'/> And it was run as an experiment: "
            "applicants were assigned by lottery, so those who got the programme and those who didn't were alike "
            "in every way but one. <bookmark mark='c'/> For men, the programme raised 1978 earnings by "
            f"{t5['experiment'][0]} dollars, in the dollars of 1982. <bookmark mark='d'/> Robert LaLonde, a young "
            "economist, asked a devastating question. Suppose there had been no lottery. Suppose an evaluator had "
            "compared the trainees with men from the big national surveys, as evaluators normally did, and "
            "applied the methods of the day. Would they have found the answer?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def table(self):
        t5 = load("lalonde")["table5"]
        lo, hi = -17000, 3000
        x0, x1 = -2.2, 6.0

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        items = [("PSID-1", 0, r"PSID, \ unadjusted"), ("PSID-1", 1, r"PSID, \ regression-adjusted"),
                 ("PSID-1", 2, r"PSID, \ difference in differences"), ("CPS-SSA-1", 0, r"CPS, \ unadjusted"),
                 ("CPS-SSA-1", 1, r"CPS, \ regression-adjusted"), ("CPS-SSA-1", 2, r"CPS, \ difference in "
                                                                                  r"differences"),
                 ("PSID-3", 1, r"a narrower PSID group, \ adjusted"), ("CPS-SSA-3", 1, r"a narrower CPS group, "
                                                                                       r"\ adjusted")]
        axis_y = -2.7
        axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), axis_y - 0.07, 0], [X(v), axis_y + 0.07, 0], color=GREY_C),
                                label(rf"{v / 1000:+.0f}k".replace("+0k", "0").replace("-", "$-$"), font_size=19,
                                      color=GREY_B).move_to([X(v), axis_y - 0.3, 0]))
                         for v in (-15000, -10000, -5000, 0)])
        exp_line = DashedLine([X(t5["experiment"][0]), axis_y, 0], [X(t5["experiment"][0]), 2.6, 0], color=EXP,
                              stroke_width=3)
        exp_lab = label(rf"the experiment: \ $+\${t5['experiment'][0]}$", font_size=22, color=EXP).next_to(
            exp_line, UP, buff=0.08)
        rows = VGroup()
        for k, (grp, j, nm) in enumerate(items):
            y = 2.0 - 0.56 * k
            v = t5[grp][j]
            nmv = label(nm, font_size=20, color=GREY_A).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            d = Dot([X(v), y, 0], radius=0.09, color=NONEXP if abs(v - t5["experiment"][0]) > 1000 else E.ACCENT)
            val = label(f"{v:+,}".replace(",", "{,}").replace("-", "$-$"), font_size=19, color=d.get_color()).next_to(
                d, RIGHT if v < 0 else LEFT, buff=0.12)
            rows.add(VGroup(nmv, d, val))
        unit = label(r"estimated effect on 1978 earnings, \ 1982 dollars", font_size=20, color=GREY_B)
        unit.next_to(axis, DOWN, buff=0.5)
        tag = published_tag(r"LaLonde (1986), table 5 (men)", corner=DR, font_size=15)
        with self.voiceover(
            "Here is the answer, from his table for the men. <bookmark mark='a'/> The dashed line is the truth the "
            "experiment found. <bookmark mark='b'/> Compare the trainees with men from the Panel Study of Income "
            f"Dynamics, and the programme seems to have cut their earnings by {abs(t5['PSID-1'][0]):,} dollars: the "
            "trainees were simply poorer to begin with. <bookmark mark='c'/> Adjust by regression for age, schooling "
            f"and race, and it still cuts them by {abs(t5['PSID-1'][1]):,}. <bookmark mark='d'/> The other methods "
            "of the day scatter around the truth, some near it, some thousands of dollars away, with comparison "
            "groups from the census's survey just as bad. <bookmark mark='e'/> Worse, LaLonde found that the "
            "standard specification tests couldn't tell the good estimates from the bad. Without the experiment, "
            "an honest evaluator would not have known which number to believe."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(unit), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(exp_line), FadeIn(exp_lab))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("e")
            self.play(Indicate(exp_lab, color=EXP))
        self.clear_scene()

    def dehejia(self):
        la = load("lalonde")
        pre = la["pre"]
        head = VGroup(VectorizedPoint(), label(r"trainees", font_size=24, color=EXP),
                      label(r"lottery losers", font_size=24, color=GREY_A),
                      label(r"PSID men", font_size=24, color=NONEXP))
        lines = [("age", r"age", lambda v: f"{v:.1f}"), ("married", r"married", lambda v: f"{100 * v:.0f}\\%"),
                 ("black", r"black", lambda v: f"{100 * v:.0f}\\%"),
                 ("re74", r"earnings, 1974", lambda v: rf"\${v:,.0f}".replace(",", "{,}")),
                 ("re75", r"earnings, 1975", lambda v: rf"\${v:,.0f}".replace(",", "{,}"))]
        table = VGroup(head)
        for k, nm, f in lines:
            table.add(VGroup(label(nm, font_size=23, color=GREY_A), *[label(f(v), font_size=24) for v in pre[k]]))
        for r in table:
            for i, x in enumerate((-4.6, -1.6, 0.9, 3.4)):
                r[i].move_to([x, 0, 0])
        table.arrange(DOWN, buff=0.28).move_to(UP * 1.4)
        for r in table:
            for i, x in enumerate((-4.6, -1.6, 0.9, 3.4)):
                r[i].set_x(x)
        res = VGroup(
            label(rf"the experiment: \ $+\${la['experiment']:,.0f}$".replace(",", "{,}"), font_size=26, color=EXP),
            label(rf"trainees minus PSID men: \ ${'-' if la['raw_psid'] < 0 else '+'}\${abs(la['raw_psid']):,.0f}$"
                  .replace(",", "{,}"), font_size=26, color=NONEXP),
            label(rf"adjusted for age, schooling, race and \emph{{past earnings}}: \ "
                  rf"$+\${la['adj_psid']:,.0f}$".replace(",", "{,}"), font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.7)
        tag = data_tag(r"Dehejia and Wahba's NSW subsample (185 trainees, 260 controls) and 429 PSID men "
                       r"(\emph{Statistics, Built}'s Museum)", corner=DR, font_size=14)
        with self.voiceover(
            "The story has a sequel. <bookmark mark='a'/> In 1999 Rajeev Dehejia and Sadek Wahba went back to "
            "LaLonde's data. Here are the trainees, the lottery losers and a group of survey men, in the subsample "
            "they used. The trainees and the lottery losers look alike. The survey men are older, far more often "
            "married, and earned more than twice as much before the programme. <bookmark mark='b'/> In this "
            "subsample the experiment says the programme added about 1,800 dollars. <bookmark mark='c'/> The raw "
            "comparison with the survey men gets even the sign wrong. <bookmark mark='d'/> But compare like with "
            "like, holding past earnings fixed, and the estimate comes close: about 1,500. "
            "<bookmark mark='e'/> So careful methods can work. The catch is the one LaLonde found: we only know "
            "this one worked because the experiment was there to check it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in table[1:]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]))
            vo.wait_until("d")
            self.play(FadeIn(res[2]))
            vo.wait_until("e")
            self.play(Indicate(res[0], color=EXP))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["lalonde_1986"]
        cc = call_card(r"the standard non-experimental evaluation", c.when,
                       r"a survey comparison group, regression-adjusted: \ $-\$8{,}067$",
                       r"the lottery: \ $+\$886$; \ most methods missed it, \ and their tests could not tell",
                       c.verdict, width=11.6, font_size=25).move_to(UP * 0.2)
        nxt = label(r"what came next: \ find the lotteries the world runs anyway", font_size=27, color=E.ACCENT)
        nxt.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Called it? The series keeps score of predictions, and this one is clear. <bookmark mark='a'/> The "
            "standard evaluation of the day said the programme cut men's earnings by about eight thousand dollars. "
            "The lottery said it raised them by about nine hundred. Wrong, and wrong in sign. "
            "<bookmark mark='b'/> What came next was a change of strategy. If experiments give answers that "
            "regressions can't, then find the experiments: the lotteries, accidents and rules that the world runs "
            "anyway."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]))
            vo.wait_until("a")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()
