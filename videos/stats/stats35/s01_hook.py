from __future__ import annotations

from explainer.stats import museum
from videos.stats.stats35.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.designs()
        self.table()
        self.why()
        self.blind()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1954,)).to_edge(UP, buff=0.35)
        hc = history_card(1954, r"Thomas Francis Jr. \ and the Poliomyelitis Vaccine Evaluation Center",
                          r"Jonas Salk's killed-virus vaccine is tested on nearly two million American schoolchildren, "
                          r"the `polio pioneers': \ the largest public-health experiment ever run. \ Two designs are used "
                          r"side by side, \ in different parts of the country", color=Y1C, width=11.0,
                          font_size=23).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"polio struck tens of thousands of children a year; \ 1952: \ over 57,000 cases in the US", font_size=24),
            label(r"a rare disease with huge swings from year to year: \ a before-and-after comparison would be confounded by calendar time", font_size=24, color=MISSC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the spring of 1954, the United States ran the largest public-health experiment "
            "in its history. Jonas Salk had made a killed-virus polio vaccine, and nearly two million schoolchildren,"
            " the polio pioneers, took part in testing it, under the direction of Thomas Francis at the University of"
            " Michigan. <bookmark mark='b'/> Polio was terrifying: in 1952 the country had over fifty-seven thousand "
            "cases, many of them children left paralysed. <bookmark mark='c'/> But it was also rare and erratic, with"
            " epidemics that came and went from year to year, so a drop in cases after vaccination would not by "
            "itself identify a vaccine effect. The vaccine had to be tested against a control group in the same year."
            " The question was how to choose the controls."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def designs(self):
        left = VGroup(label(r"\textbf{the observed-control design}", font_size=26, color=MISSC),
                      label(r"the National Foundation's plan", font_size=22, color=GREY_A),
                      label(r"vaccinate second-graders whose parents consent", font_size=22),
                      label(r"controls: \ first- and third-graders", font_size=22),
                      label(r"no placebo; \ doctors know who was vaccinated", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        right = VGroup(label(r"\textbf{the randomized design}", font_size=26, color=BANDC),
                       label(r"insisted on by Francis and state health officers", font_size=22, color=GREY_A),
                       label(r"among children whose parents consent:", font_size=22),
                       label(r"a coin decides: \ vaccine or salt-water placebo", font_size=22),
                       label(r"double blind: \ neither family nor doctor knows", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.3, 0])
        if cols.width > 13.0:
            cols.width = 13.0
        with self.voiceover(
            "<bookmark mark='a'/> The National Foundation for Infantile Paralysis, which had funded the vaccine, proposed "
            "an observed-control design: vaccinate the second-graders whose parents consented, and compare them with the "
            "first- and third-graders, who were not offered the vaccine. No placebo, and the doctors diagnosing polio would "
            "know who had been vaccinated. <bookmark mark='b'/> Francis, and many state health officers, insisted on a "
            "randomized design instead. Among children whose parents consented, a random draw decided who got the vaccine "
            "and who got an injection of salt water that looked identical, and neither the families nor the diagnosing "
            "doctors knew which was which. The compromise was to run both: the observed-control design in some states, "
            "the randomized one in others."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
        self.clear_scene()

    def table(self):
        rows = [[r"design", r"group", r"children", r"paralytic polio per 100,000"]]
        cols = [GREY_A]
        for name, key, c in ((r"randomized", "randomized", BANDC), (r"observed control", "nfip", MISSC)):
            for k, (g, n, r) in enumerate(museum.SALK[key]):
                rows.append([name if k == 0 else "", g, rf"$\approx$ {n:,}", rf"{r}"])
                cols.append(c if k < 2 else GREY_B)
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.25, colors=cols).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"randomized: \ $71 - 28 = 43$ per 100,000", font_size=24, color=BANDC),
            label(r"observed control: \ $54 - 25 = 29$ per 100,000: \ a third smaller", font_size=24, color=MISSC),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The results, as Paul Meier summarized them in 1972, in cases of paralytic polio per"
            " hundred thousand children. <bookmark mark='b'/> In the randomized areas: twenty-eight among the "
            "vaccinated, seventy-one among the placebo group, and forty-six among the children whose parents refused."
            " In the observed-control areas: twenty-five among vaccinated second-graders, fifty-four among the first-"
            " and third-grade controls, and forty-four among second-graders who did not consent. <bookmark mark='c'/>"
            " The randomized comparison estimates forty-three paralytic cases prevented per hundred thousand. The "
            "textbook sample sizes shown here are rounded. <bookmark mark='d'/> The observed-control comparison shows"
            " only twenty-nine. The observed-control risk difference is about a third smaller. These were different "
            "areas, so that gap alone does not identify the exact selection bias."
        ) as vo:
            self.add(historical_tag(r"Francis (1955); \ Meier (1972)"))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def why(self):
        rows = fit_rows(VGroup(
            label(r"who consents? \ wealthier, \ better-educated families", font_size=26),
            label(r"polio was a disease of hygiene: \ cleaner homes, \ later exposure, \ worse infections", font_size=26, color=MISSC),
            label(r"so the consenting second-graders were \emph{more} at risk than the controls", font_size=26, color=MISSC),
            label(r"in the randomized areas, \ refusers: \ 46, \ not 71", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why the difference? Consent was not random. The families who volunteered their "
            "children were, on average, wealthier and better educated. <bookmark mark='b'/> And polio was, "
            "paradoxically, a disease of hygiene: children from cleaner homes met the virus later in childhood, "
            "without their mothers' antibodies, and suffered worse infections. <bookmark mark='c'/> So the vaccinated"
            " second-graders were drawn from the families most at risk, while their controls included everyone. The "
            "comparison mixed the vaccine's effect with the difference between the kinds of family. <bookmark "
            "mark='d'/> The randomized areas illustrate the selection problem: children whose parents refused had "
            "forty-six cases per hundred thousand, far fewer than the seventy-one among the consenting children who "
            "got placebo."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def blind(self):
        rows = fit_rows(VGroup(
            label(r"diagnosis of mild polio was a judgement call", font_size=26),
            label(r"a doctor who knows the child was vaccinated may call it something else", font_size=26, color=MISSC),
            label(r"the placebo and the blinding removed that path too", font_size=26, color=BANDC),
            label(r"April 12, 1955: \ `safe, effective and potent'", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There was a second problem. Many cases of polio were mild, and the diagnosis was a "
            "judgement. <bookmark mark='b'/> A doctor who knew that a child had been vaccinated might be readier to call "
            "the same symptoms something else. <bookmark mark='c'/> The placebo, and the blinding of families and doctors, "
            "closed that path as well. <bookmark mark='d'/> On the twelfth of April 1955, Francis announced the result: the "
            "vaccine was safe, effective and potent. The randomized half of the trial is the part that statisticians still "
            "cite."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"`the vaccine prevented 43 cases per 100,000': \ compared with what?", font_size=26),
            label(r"with what would have happened to the \emph{same} children without it", font_size=26, color=TAUC),
            label(r"which no one can observe", font_size=26, color=MISSC),
            label(r"randomization lets us estimate it anyway: \ this part says exactly how, \ and when it fails", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But what does it mean to say the vaccine prevented forty-three cases per hundred "
            "thousand? <bookmark mark='b'/> It means: compared with what would have happened to the same children without "
            "it. <bookmark mark='c'/> That comparison can never be observed; each child was either vaccinated or not. "
            "<bookmark mark='d'/> Randomization lets us estimate it anyway. This part makes that precise, with the language "
            "of potential outcomes, and then follows experiments into the places where they become difficult."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 35", font_size=34, color=GREY_B), label(r"What If?", font_size=60),
                      label(r"Experiments and Potential Outcomes", font_size=36, color=GREY_A)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"potential outcomes, \ the science table, \ estimands and SUTVA",
            r"why randomization works; \ Fisher's sharp null; \ Neyman's variance",
            r"blocking, \ adjustment (Freedman, \ Lin), \ cluster randomization",
            r"noncompliance and the LATE; \ interference; \ subgroups",
            r"sequential trials, \ surrogates, \ and transporting a trial",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 13 and 23").to_corner(DL, buff=0.3)
        built = note(r"built: \ the World's clinic trial; \ \texttt{statkit.causal} (I); \ the science table").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-five: what if? Experiments and potential outcomes. <bookmark mark='b'/> We'll "
            "define causal effects through potential outcomes, using a World in which, for once, both outcomes of every "
            "patient are known; see exactly why randomization removes selection bias; test Fisher's sharp null and derive "
            "Neyman's variance; block, pair and adjust, and see what Freedman objected to and how Lin answered; randomize "
            "whole schools; handle patients who do not take their pills, and vaccines that protect the neighbours; distrust "
            "subgroups; stop trials early without cheating; doubt surrogate endpoints; and carry a trial's result to the "
            "population that will use it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
