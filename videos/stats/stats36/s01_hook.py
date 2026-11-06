from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.experiment()
        self.swap()
        self.table()
        self.verdict()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1986,)).to_edge(UP, buff=0.35)
        hc = history_card(1986, r"Robert LaLonde, \ \emph{Evaluating the Econometric Evaluations of Training Programs}",
                          r"The National Supported Work Demonstration had randomized disadvantaged workers into a job-training "
                          r"programme. \ LaLonde threw away the experiment's control group, \ replaced it with men from national "
                          r"surveys, \ and asked the econometric methods of the day to recover the experimental answer",
                          color=Y1C, width=11.2, font_size=22).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"if the methods work, \ they should agree with the experiment", font_size=24),
            label(r"they did not: \ estimates scattered widely, \ some far from the truth, \ some of the wrong sign", font_size=24, color=MISSC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1986 the economist Robert LaLonde, fresh from his doctorate at Princeton, published one of the most "
            "influential tests in social science. The National Supported Work Demonstration of the mid-1970s had randomly "
            "assigned disadvantaged workers, many of them ex-offenders and former addicts, either to a programme of "
            "subsidized work experience or to a control group. LaLonde kept the programme's participants, threw away the "
            "randomized controls, and replaced them with men drawn from national surveys. Then he asked the econometric "
            "methods of the day to recover the experimental answer. <bookmark mark='b'/> If the methods worked, they would "
            "agree with the experiment. <bookmark mark='c'/> They did not. The estimates scattered widely, many far from the "
            "experimental benchmark and some with the wrong sign, and the specification tests of the time could not tell "
            "the good ones from the bad."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def experiment(self):
        d = load("lalonde")
        rows = fit_rows(VGroup(
            label(rf"Dehejia \& Wahba's subsample: \ {d['n']['treated']} trainees, \ {d['n']['exp_control']} randomized controls", font_size=26),
            label(r"outcome: \ earnings in 1978, \ after the programme (1982 dollars)", font_size=26),
            label(rf"the experiment: \ \${d['exp']['est']:,.0f} \ (95\% CI \${d['exp']['lo']:,.0f} to \${d['exp']['hi']:,.0f})", font_size=26, color=BANDC),
            label(r"a benchmark no observational study gets", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The data have been reanalysed ever since. In the subsample that Rajeev Dehejia and Sadek "
            "Wahba used in 1999, one hundred and eighty-five men took part in the programme and two hundred and sixty were "
            "randomized controls. <bookmark mark='b'/> The outcome is earnings in 1978, after the programme. <bookmark "
            "mark='c'/> The experiment says the programme raised earnings by about one thousand eight hundred dollars, with a "
            "wide interval. <bookmark mark='d'/> It is a benchmark that an observational study, by definition, never gets."
        ) as vo:
            self.add(nsw_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def swap(self):
        d = load("lalonde")
        mn = d["means"]
        rows = [[r"", r"trainees", r"randomized controls", r"PSID men"]]
        for k, nm, f in (("age", r"age", "{:.1f}"), ("black", r"black", "{:.2f}"), ("married", r"married", "{:.2f}"),
                         ("re74", r"earnings 1974", "\\${:,.0f}"), ("re75", r"earnings 1975", "\\${:,.0f}")):
            rows.append([nm, f.format(mn[k]["treated"]), f.format(mn[k]["exp_control"]), f.format(mn[k]["psid"])])
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.28, colors=[GREY_A, None, None, None, None, None]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"now replace the controls with {d['n']['psid']} men from the Panel Study of Income Dynamics", font_size=24),
            label(r"randomization made the first two columns alike; \ nothing makes the third", font_size=24, color=MISSC),
        ), 12.4, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now do what LaLonde did: replace the randomized controls with four hundred and twenty-nine "
            "men from the Panel Study of Income Dynamics, a national household survey. <bookmark mark='b'/> The trainees and "
            "the randomized controls look alike, because a coin divided them. <bookmark mark='c'/> The survey men do not. "
            "They are older, far more likely to be married, much less likely to be black, and in 1974 earned more than twice "
            "as much. Nothing made them comparable."
        ) as vo:
            self.add(nsw_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[:3]) for r in tab[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in tab[1:]], lag_ratio=0.2), FadeIn(foot[1]))
        self.clear_scene()

    def table(self):
        d = load("lalonde")
        rows = fit_rows(VGroup(
            label(rf"the experiment: \ \${d['exp']['est']:,.0f}", font_size=28, color=BANDC),
            label(rf"trainees vs PSID men, \ raw: \ $-$\${-d['naive']['est']:,.0f}", font_size=28, color=MISSC),
            label(rf"adjusting for age, \ education, \ race, \ marriage and past earnings: \ \${d['ols']['est']:,.0f}", font_size=28, color=TAUC),
            label(r"and other reasonable methods give anything from \$400 to \$1,700 \ (chapter 15)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The experiment: plus one thousand eight hundred dollars. <bookmark mark='b'/> Comparing the "
            "trainees with the survey men directly: minus six hundred and thirty-five. The programme appears to hurt. "
            "<bookmark mark='c'/> Adjusting by regression for age, education, race, marriage and past earnings brings the "
            "estimate to about fifteen hundred, much closer. <bookmark mark='d'/> But as we will see in chapter fifteen, "
            "other methods that sound equally reasonable give anything from four hundred to seventeen hundred dollars. "
            "Without the experiment, how would we know which to believe?"
        ) as vo:
            self.add(nsw_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"Dehejia \& Wahba (1999): \ propensity scores, \ on their subsample, \ come close", font_size=26, color=BANDC),
            label(r"Smith \& Todd (2005): \ only on that subsample, \ and only with some specifications", font_size=26, color=MISSC),
            label(r"the debate became a lesson: \ assumptions and overlap, \ not methods, \ decide", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1999, Dehejia and Wahba showed that propensity-score methods, the subject of chapter "
            "seven, come close to the experimental answer on their subsample. <bookmark mark='b'/> In 2005, Jeffrey Smith and "
            "Petra Todd replied that they do so only on that particular subsample, and only with some specifications. "
            "<bookmark mark='c'/> The debate turned into a lesson that this part tries to teach: what decides whether "
            "observational causal inference works is not the cleverness of the method but the assumptions it rests on, and "
            "whether the data contain comparable people at all."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"most causal questions cannot be randomized: \ smoking, \ schooling, \ policy, \ history", font_size=26),
            label(r"so: \ what must we assume to learn causes from observation?", font_size=26, color=TAUC),
            label(r"how do we adjust, \ and for what?", font_size=26, color=Y0C),
            label(r"and how wrong might we be?", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Most causal questions can never be put to a coin: whether smoking causes cancer, whether "
            "schooling raises earnings, whether a policy worked, why a war began. <bookmark mark='b'/> So what must we assume "
            "to learn about causes from observation? <bookmark mark='c'/> How do we adjust, and for what? <bookmark "
            "mark='d'/> And how wrong might we be?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 36", font_size=34, color=GREY_B), label(r"Causes Without Experiments", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"unconfoundedness and overlap; \ causal diagrams and d-separation",
            r"back door, \ front door, \ do-calculus; \ Simpson resolved",
            r"g-computation, \ propensity scores, \ weighting, \ double robustness, \ DML",
            r"heterogeneous effects and causal forests; \ sensitivity analysis",
            r"smoking and lung cancer; \ time-varying treatments; \ LaLonde revisited",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Part 35").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.causal} (II); \ the causal graph; \ data: \ NSW").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-six: causes without experiments. <bookmark mark='b'/> We'll state the "
            "assumptions that replace randomization; draw causal diagrams and read off what to adjust for, and what not to; "
            "resolve Simpson's paradox; estimate effects by g-computation, propensity scores, weighting, doubly robust and "
            "double machine learning methods, each graded against the World's truth; estimate effects that vary between "
            "people; measure how wrong an unmeasured confounder could make us; revisit smoking and lung cancer and "
            "treatments that change over time; and return to LaLonde."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
