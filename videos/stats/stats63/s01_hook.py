from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.linkage()
        self.unique_chart()
        self.more()
        self.lesson()
        self.decisions()
        self.taxonomy()
        self.upgrade()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1997,)).to_edge(UP, buff=0.35)
        hc = history_card(1997, r"L. Sweeney, \ then a graduate student at MIT",
                          r"Massachusetts's Group Insurance Commission had released the hospital records of state employees "
                          r"for research, \ with names and addresses removed. \ The governor, \ William Weld, \ assured "
                          r"them their privacy was protected", color=BADC, width=11.4, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"left in: \ ZIP code, \ birth date, \ sex, \ and the diagnoses", font_size=26, color=GREY_A),
            label(r"for twenty dollars: \ Cambridge's voter roll, \ with names, \ ZIP codes, \ birth dates and sex", font_size=26, color=PRIVC),
            label(r"she mailed the governor his own medical records", font_size=26, color=BADC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the mid-nineteen-nineties, the Group Insurance Commission of Massachusetts released "
            "the hospital records of state employees to researchers. Names and addresses had been removed, and the governor, "
            "William Weld, assured the employees that their privacy was protected. <bookmark mark='b'/> But each record "
            "still carried a ZIP code, a birth date and a sex, next to the diagnoses. <bookmark mark='c'/> Latanya Sweeney, "
            "then a graduate student, bought the voter roll of Cambridge, where the governor lived, for twenty dollars. It "
            "listed every voter's name, address, ZIP code, birth date and sex. <bookmark mark='d'/> She found the governor's "
            "records, and mailed them to his office."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def linkage(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The attack is a join, of the kind every database supports. <bookmark mark='b'/> The "
            "medical table and the voter table share three columns, the quasi-identifiers. <bookmark mark='c'/> In "
            "Cambridge, by the usual account, six people shared the governor's birth date; three of them were men; and only "
            "one of those lived in his ZIP code. <bookmark mark='d'/> Removing names had not made anyone anonymous. It had "
            "only removed one of many keys.",
            [(r"\text{medical}", r":", r"(\text{ZIP}, \ \text{birth date}, \ \text{sex}) \ + \ \text{diagnoses}", 40),
             (r"\text{voters}", r":", r"(\text{ZIP}, \ \text{birth date}, \ \text{sex}) \ + \ \text{name}", 40),
             (r"\text{Cambridge}", r":", r"6 \ \to \ 3 \ \to \ 1", 40),
             (r"\text{lesson}", r":", r"\text{removing names is not anonymity}", 40)],
            [r"a database join", r"the quasi-identifiers", r"birth date, \ sex, \ ZIP", r"Sweeney (2002)"],
            colors=[(2, BADC), (3, BADC)])

    def unique_chart(self):
        d = load("unique")
        rows = d["rows"]
        A = axes([-0.6, 3.6], [0, 1.0], x_length=7.4, y_length=4.2, xlabel=r"", ylabel=r"fraction of adults unique in the sample",
                 xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1], yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-2.4, 0.3, 0])
        ax = A.ax
        cols = [OKC, OKC, BADC, BADC]
        names = [r"age", r"+ sex", r"+ BMI", r"+ blood pressure"]
        bars = VGroup()
        for k, r in enumerate(rows):
            h = max(r["unique"], 0.004)
            b = Rectangle(width=1.0, height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=cols[k], fill_opacity=0.85)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            v = label(rf"{100 * r['unique']:.1f}\%", font_size=22, color=cols[k]).next_to(b, UP, buff=0.1)
            n = label(names[k], font_size=22, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.2)
            bars.add(VGroup(b, v, n))
        side = side_groups([
            [(rf"NHANES: \ {d['n']:,} adults".replace(",", "{,}"), WHITE), (r"complete measurements", GREY_A)],
            [(r"age and sex: \ nobody unique", OKC), (rf"{rows[1]['classes']} classes", GREY_A)],
            [(r"add a BMI to one decimal:", BADC), (rf"{100 * rows[2]['unique']:.1f}\% unique", BADC)],
            [(r"add a blood pressure:", BADC), (rf"{100 * rows[3]['unique']:.1f}\% unique", BADC)],
        ])
        with self.voiceover(
            "<bookmark mark='a'/> The Museum's NHANES extract contains 5,176 adults with complete age, sex, body-mass index and at least one blood-pressure measurement. This is an unweighted complete-case sample, with age top-coded at eighty. <bookmark mark='b'/> Age and sex alone single out nobody in this extract. <bookmark mark='c'/> Adding body-mass index to one decimal makes about eighty-one percent unique within this sample. <bookmark mark='d'/> Adding rounded average systolic pressure makes almost everyone sample-unique. Linking an external record would additionally require matching measurements, inclusion knowledge and a suitable identified source. Sample uniqueness alone is not a demonstrated re-identification attack or a population uniqueness estimate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES (the Museum)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(bars[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[3]), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def more(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The governor was not unlucky. In 2000 Sweeney estimated from the 1990 census that about "
            "eighty-seven percent of Americans were unique by five-digit ZIP code, sex and birth date; Philippe Golle, "
            "repeating it with the 2000 census, found sixty-three percent, still a majority. <bookmark mark='b'/> In 2008 "
            "Arvind Narayanan and Vitaly Shmatikov re-identified users of the Netflix Prize data from a few movie ratings and "
            "their dates. <bookmark mark='c'/> The same year, Nils Homer and colleagues showed that published summary "
            "statistics of a genetic study, allele frequencies alone, could reveal whether a person's DNA was in it, and "
            "access to such summaries was restricted. <bookmark mark='d'/> And Irit Dinur and Kobbi Nissim had proved in "
            "2003 that answering too many counting queries too accurately lets anyone reconstruct the database itself. "
            "Aggregates leak too.",
            [(r"\text{ZIP, sex, birth date}", r":", r"87\% \ (1990), \ \ 63\% \ (2000) \ \text{unique}", 38),
             (r"\text{Netflix Prize}", r":", r"\text{a few ratings and dates}", 40),
             (r"\text{genomics}", r":", r"\text{membership from summary statistics}", 40),
             (r"\text{reconstruction}", r":", r"\text{too many accurate answers}", 40)],
            [r"Sweeney (2000); \ Golle (2006)", r"Narayanan \& Shmatikov (2008)", r"Homer et al. (2008)", r"Dinur \& Nissim (2003)"],
            colors=[(3, BADC)])

    def lesson(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The lesson took a decade to sink in. <bookmark mark='b'/> Anonymity is not a property of "
            "a dataset, because what identifies someone depends on what else the attacker knows, and that cannot be listed in "
            "advance. <bookmark mark='c'/> So privacy has to be a property of the process that produces a release: a "
            "promise about what any attacker, with any side knowledge, can learn about any one person. <bookmark mark='d'/> "
            "That promise is differential privacy, and its price is noise. This part prices it in the statistician's own "
            "currency: mean squared error, coverage and power.",
            [(r"\text{anonymity}", r":", r"\text{not a property of the data}", 40),
             (r"\text{because}", r":", r"\text{side knowledge cannot be listed}", 40),
             (r"\text{instead}", r":", r"\text{a property of the release process}", 40),
             (r"\text{the price}", r":", r"\text{noise, \ in MSE, \ coverage and power}", 40)],
            [r"the linkage lesson", r"any attacker", r"differential privacy", r"chapters 1--7"],
            colors=[(2, PRIVC)])

    def decisions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The same records feed decisions. <bookmark mark='b'/> ProPublica studied COMPAS scores for Broward County defendants in 2016, using two-year rearrest as its outcome. <bookmark mark='c'/> Among defendants without a recorded rearrest, Black defendants were labelled medium or high risk nearly twice as often as white defendants. <bookmark mark='d'/> The company emphasized predictive performance and approximate calibration instead. These are different criteria, and both descriptive patterns can coexist. The empirical predictive values and score-specific rates are not exactly equal across groups; the mathematical conflict does not prove every empirical claim made in that dispute.",
            [(r"\text{COMPAS}", r":", r"\text{a risk score for defendants}", 40),
             (r"\text{ProPublica}", r":", r"\text{false positives twice as common for Black defendants}", 36),
             (r"\text{Northpointe}", r":", r"\text{emphasized approximate predictive parity}", 38),
             (r"\text{both patterns}", r":", r"\text{can coexist}", 40)],
            [r"Broward County, \ Florida", r"Angwin et al. (2016)", r"Dieterich et al. (2016)", r"chapter 9"],
            colors=[(1, GRPA), (2, GRPB), (3, S.ACCENT)])

    def taxonomy(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one to four: differential privacy, the same "
            "definition as a hypothesis test, accountants that add privacy losses, and the minimax cost of privacy. "
            "<bookmark mark='c'/> Chapters five to seven: honest inference on privatized data, the 2020 United States census, "
            "and private machine learning. <bookmark mark='d'/> Chapters eight to eleven: fairness criteria, the theorem "
            "that they cannot all hold, multicalibration, and causal fairness.",
            [(r"the plan:", GREY_A),
             (r"1--4: \ definition, \ testing, \ accounting, \ the cost of privacy", PRIVC),
             (r"5--7: \ private inference, \ the 2020 Census, \ DP-SGD", OKC),
             (r"8--11: \ criteria, \ impossibility, \ multicalibration, \ causal fairness", GRPA)])

    def upgrade(self):
        cards = [
            upgrade_card(18, r"publish the survey's tables and estimates", r"aggregates reveal nothing about anyone",
                         r"chapters 1--6: \ what each release leaks, \ and the price of hiding it"),
            upgrade_card(19, r"judge a classifier by its error rate", r"one error rate for everyone",
                         r"chapters 8--11: \ errors by group, \ and what can be equalized"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part eighteen published a survey's tables as if aggregates revealed "
            "nothing about anyone; chapters one to six measure what each release leaks, and what hiding it costs. <bookmark "
            "mark='b'/> Part nineteen judged a classifier by one error rate; chapters eight to eleven split the errors by "
            "group, and ask which differences can be removed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 63", font_size=34, color=GREY_B), label(r"Privacy and Fairness", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"differential privacy as a hypothesis test; \ accountants; \ the minimax cost of privacy",
            r"confidence intervals on noisy data; \ the 2020 Census; \ private learning and its audits",
            r"fairness criteria on ProPublica's COMPAS data; \ the impossibility theorem; \ multicalibration",
            r"counterfactual fairness; \ two Board rows; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 41, \ 46, \ 50").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.privacy}, \ the trade-off plot").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-three: privacy and fairness. <bookmark mark='b'/> Differential privacy, read "
            "as a hypothesis test; privacy accountants; the minimax cost of privacy; confidence intervals that survive the "
            "noise; the 2020 census; private learning and the attacks that audit it; then fairness criteria on ProPublica's "
            "COMPAS data, the theorem that they conflict, multicalibration, counterfactual fairness, and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
