from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Intervention(VoiceoverScene):
    def construct(self):
        self.card()
        self.fade()
        self.perry()
        self.many_outcomes()
        self.abecedarian()
        self.word_gap()
        self.one_hour()

    def card(self):
        card = chapter_card(8, r"Early intervention", r"Can a programme in early childhood change a life?",
                            lit={1962: r"Perry Preschool", 1972: r"Abecedarian", 1995: r"Hart \& Risley"},
                            part=PART, scale=("person", "group", "society"), marr=("what",))
        with self.voiceover("Chapter eight. Early intervention."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fade(self):
        d = load("programmes")
        head = heading(r"Fade-out")
        A = axes([0, 6], [0, 0.7], x_length=6.0, y_length=4.0, xticks=[0, 2, 4, 6], yticks=[0, 0.2, 0.4, 0.6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"years after the programme ends",
                 ylabel=r"effect on test scores \ (SD)", center=[-3.0, -0.4, 0], font_size=16)
        f = curve(A.ax, d["years"], d["fade"], CARE, stroke_width=5)
        sh = label(r"illustrative shape", font_size=16, color=GREY_B).next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"Part 30 met the pattern: \ a programme raises test scores, \ and within a few years the children "
             r"who missed it catch up", WHITE),
            (r"Perry Preschool's IQ gain faded; \ Head Start's early effects were largely gone by third grade", CARE),
            (r"yet Perry's children did better as adults: \ effects that vanish from tests can reappear in lives",
             GOOD),
            (r"so the question is what a programme changes, \ and how anyone could tell from so few children", YOU),
        ], 5.6, 22, 0.38).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.fade\_out}: \ illustrative")
        with self.voiceover(
            "Part 30 met the central puzzle of early programmes. <bookmark mark='a'/> A programme raises test "
            "scores, and within a few years the children who missed it catch up. <bookmark mark='b'/> Perry "
            "Preschool's IQ gain faded, and Head Start's early effects were largely gone by third grade. "
            "<bookmark mark='c'/> And yet Perry's children did better as adults. Effects that vanish from tests can "
            "reappear in lives. <bookmark mark='d'/> So this chapter asks what a programme changes, and how anyone "
            "could tell from so few children."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(sh))
            vo.wait_until("a")
            self.play(Create(f), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def perry(self):
        head = heading(r"Perry Preschool at forty")
        A = axes([-0.6, 3.6], [0, 100], x_length=5.6, y_length=3.8, xticks=None, yticks=None,
                 center=[-3.2, -0.3, 0], font_size=16)
        b = bars(A.ax, [0, 1], [76, 62], [GOOD, GREY_B], width=0.7)
        b2 = bars(A.ax, [2.4, 3.4], [100 * 20800 / 25000, 100 * 15300 / 25000], [GOOD, GREY_B], width=0.7)
        t1 = label(r"employed at 40 \ (\%)", font_size=18).next_to(A.ax.c2p(0.5, 0), DOWN, buff=0.25)
        t2 = label(r"median earnings", font_size=18).next_to(A.ax.c2p(2.9, 0), DOWN, buff=0.25)
        v = VGroup(label(r"76", font_size=18, color=GOOD).next_to(b[0], UP, buff=0.08),
                   label(r"62", font_size=18).next_to(b[1], UP, buff=0.08),
                   label(r"\$20{,}800", font_size=16, color=GOOD).next_to(b2[0], UP, buff=0.08),
                   label(r"\$15{,}300", font_size=16).next_to(b2[1], UP, buff=0.08))
        key = legend([(GOOD, r"programme"), (GREY_B, r"no programme")], font_size=17).next_to(A, UP, buff=0.15)
        rows = rows_of([
            (r"Ypsilanti, \ Michigan, \ 1962 to 1967: \ 123 children aged 3 and 4 from poor families, \ 58 assigned "
             r"to the programme and 65 not", WHITE),
            (r"at 40, \ with 97\% of the living participants interviewed: \ more employed, \ higher earnings, \ "
             r"fewer arrests", GOOD),
            (r"James Heckman and colleagues, \ 2010: \ the assignment had been compromised, \ so they modelled it; "
             r"\ a social rate of return of about 7 to 10\% a year", CARE),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Schweinhart et al.\ (2005); \ Heckman et al.\ (2010)")
        with self.voiceover(
            "Perry Preschool is the most quoted study in this field. <bookmark mark='a'/> In Ypsilanti, Michigan, "
            "from 1962 to 1967, a hundred and twenty-three children aged three and four, from poor families, were "
            "assigned either to a half-day preschool with home visits or to no programme: fifty-eight and sixty-five. "
            "<bookmark mark='b'/> At forty, with ninety-seven percent of the living participants interviewed, more "
            "of the programme group were employed, seventy-six percent against sixty-two, their median earnings "
            "were higher, twenty thousand eight hundred dollars against fifteen thousand three hundred, and they had "
            "been arrested less. <bookmark mark='c'/> But the assignment hadn't been a clean randomization; some "
            "children were swapped between groups. James Heckman and colleagues modelled that in 2010 and estimated "
            "a social rate of return of about seven to ten percent a year, lower than earlier claims, and still "
            "above the long-run return on stocks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(b2), FadeIn(t1), FadeIn(t2), FadeIn(v), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def many_outcomes(self):
        d = load("programmes")
        head = heading(r"Small trials, \ many outcomes")
        A = axes([0, 60], [0, 1.0], x_length=5.8, y_length=3.8, xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"outcomes tested, \ $m$",
                 ylabel=r"P(at least one $p < .05$)", center=[-3.0, -0.4, 0], font_size=16)
        c = curve(A.ax, d["m"], d["fwer"], LOST, stroke_width=5)
        mk = VGroup(Dot(A.ax.c2p(10, d["fwer10"]), radius=0.08, color=WHITE),
                    Dot(A.ax.c2p(30, d["fwer30"]), radius=0.08, color=WHITE))
        rows = rows_of([
            (r"with no true effect, \ each test has a 5\% chance of $p < .05$; \ with $m$ independent outcomes, "
             r"\ $1 - 0.95^m$ of finding at least one", WHITE),
            (rf"ten outcomes: \ {pct(d['fwer10'])}; \ thirty: \ {pct(d['fwer30'])}", LOST),
            (r"Michael Anderson, \ 2008: \ Perry, \ Abecedarian and the Early Training Project, \ outcomes "
             r"grouped into indices, \ $p$-values corrected for multiplicity", CARE),
            (r"girls gained substantially, \ in the short and long run; \ for boys, \ no significant long-term "
             r"benefits", GOOD),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Anderson (2008)")
        with self.voiceover(
            "These trials are small, and they measured hundreds of outcomes over decades. That's a problem Part 4 "
            "warned about. <bookmark mark='a'/> With no true effect, each test has a five percent chance of a p "
            "below 0.05, and with m independent outcomes the chance of at least one is one minus 0.95 to the power "
            f"m. <bookmark mark='b'/> Ten outcomes give {100 * d['fwer10']:.0f} percent; thirty give "
            f"{100 * d['fwer30']:.0f} percent. "
            "<bookmark mark='c'/> In 2008 the economist Michael Anderson reanalysed Perry, the Abecedarian project "
            "and the Early Training Project, grouping outcomes into indices and correcting the p-values for "
            "multiplicity. <bookmark mark='d'/> Girls had gained substantially, in the short and the long run. For "
            "boys, there were no significant long-term benefits. The effects are real, and narrower than the "
            "headlines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(mk), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def abecedarian(self):
        head = heading(r"Abecedarian: \ from infancy, \ to health at 35")
        rows = rows_of([
            (r"North Carolina, \ from 1972: \ 111 infants from poor families, \ randomized; \ the programme ran "
             r"from the first months of life to age 5", WHITE),
            (r"Frances Campbell and colleagues, \ 2014: \ medical examinations in the participants' mid-thirties",
             CARE),
            (r"treated men: \ mean systolic blood pressure 126, \ against 143 in the control men; \ one control man "
             r"in four had the metabolic syndrome, \ no treated man did", GOOD),
            (r"the samples were small, \ and the analysis used exact permutation tests for that reason; \ how a "
             r"preschool would lower blood pressure thirty years later is not known", LOST),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Campbell et al.\ (2014)")
        with self.voiceover(
            "The Abecedarian project started earlier still. <bookmark mark='a'/> In North Carolina, from 1972, a "
            "hundred and eleven infants from poor families were randomized, and the programme ran from the first "
            "months of life to age five. <bookmark mark='b'/> In 2014, Frances Campbell and colleagues reported "
            "medical examinations of the participants in their mid-thirties. <bookmark mark='c'/> The treated men "
            "had a mean systolic blood pressure of 126, against 143 in the control men, and one control man in four "
            "had the metabolic syndrome, while no treated man did. <bookmark mark='d'/> The samples were small, and "
            "the analysis used exact permutation tests for that reason. And how a preschool would lower blood "
            "pressure thirty years later isn't known."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def word_gap(self):
        head = heading(r"The thirty-million-word gap")
        rows = rows_of([
            (r"Betty Hart and Todd Risley, \ 1995: \ 42 Kansas families, \ one hour recorded each month for two "
             r"and a half years", WHITE),
            (r"children in professional families heard far more words than children in families on welfare; \ "
             r"projected to age four, \ a gap of about 30 million words", CARE),
            (r"one of the most cited findings in education, \ and the basis of programmes that coach parents to "
             r"talk more", PERIOD),
            (r"Douglas Sperry, \ Linda Sperry and Peggy Miller, \ 2019: \ 42 children in five American "
             r"communities; \ counting the speech children overhear as well, \ the gap by income "
             r"disappeared", COHORT),
            (r"Jill Gilkerson and colleagues, \ 2017: \ 3{,}213 day-long automated recordings: \ lower-income "
             r"children heard fewer adult words, \ with wide variation inside every group", AGE),
        ], 12.4, 23, 0.34).move_to([0, -0.3, 0])
        tag = published_tag(r"Hart \& Risley (1995); \ Sperry et al.\ (2019); \ Gilkerson et al.\ (2017)")
        with self.voiceover(
            "A different kind of early-childhood finding started a movement. <bookmark mark='a'/> Betty Hart and "
            "Todd Risley recorded forty-two Kansas families for one hour each month, for two and a half years. "
            "<bookmark mark='b'/> Children in professional families heard far more words than children in families "
            "on welfare. Projected to age four, it came to a gap of about thirty million words. "
            "<bookmark mark='c'/> It became one of the most cited findings in education, and the basis of programmes "
            "that coach parents to talk more. <bookmark mark='d'/> In 2019 Douglas Sperry, Linda Sperry and Peggy "
            "Miller recorded forty-two children in five American communities. When the speech children overhear was "
            "counted as well, the gap by income disappeared. <bookmark mark='e'/> And in "
            "2017 Jill Gilkerson and colleagues analysed over three thousand day-long automated recordings: "
            "lower-income children did hear fewer adult words, with wide variation inside every group."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def one_hour(self):
        d = load("wordgap")
        head = heading(r"How good is one hour a month?")
        lim = [float(np.log10(d["true"].min()) - 0.35), float(np.log10(d["true"].max()) + 0.35)]
        A = axes(lim, lim, x_length=4.6, y_length=4.6, xticks=None, yticks=None,
                 xlabel=r"a family's true rate \ (log)", ylabel=r"estimated \ (log)", center=[-3.6, -0.5, 0],
                 font_size=15)
        diag = DashedLine(A.ax.c2p(lim[0], lim[0]), A.ax.c2p(lim[1], lim[1]), color=GREY_B, stroke_width=2)
        hour = scatter(A.ax, np.log10(d["true"]), np.log10(d["one_hour"]), LOST, radius=0.06)
        day = scatter(A.ax, np.log10(d["true"]), np.log10(d["one_day"]), GOOD, radius=0.06)
        key = legend([(LOST, r"one random hour a month"), (GOOD, r"one whole day a month")], font_size=16)
        key.next_to(A, UP, buff=0.15)
        rows = rows_of([
            (r"Psyche's families talk at different rates, \ and talk varies hugely from hour to hour within a day",
             WHITE),
            (rf"one recorded hour a month for a year: \ correlation with the truth {d['r_hour']:.2f}", LOST),
            (rf"one whole day a month: \ {d['r_day']:.2f}", GOOD),
            (r"so small, \ noisy samples spread the families out, \ and a gap between groups gets multiplied by "
             r"every waking hour of four years when it is projected", YOU),
            (r"the contested part is the size and the cause of the gap, \ not that children who hear more "
             r"talk directed at them learn more words", AGE),
        ], 6.4, 20, 0.32).move_to([3.0, -0.3, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.hour\_sampling}")
        with self.voiceover(
            "Part of the disagreement is measurement, and Psyche can show how much. <bookmark mark='a'/> Its "
            "families talk at different average rates, and talk varies hugely from hour to hour within a day. "
            "<bookmark mark='b'/> Estimate each family's rate from one random recorded hour a month for a year, and "
            f"the estimates correlate {d['r_hour']:.2f} with the truth. <bookmark mark='c'/> Record one whole day "
            f"a month instead, and it's {d['r_day']:.2f}. <bookmark mark='d'/> Small, noisy samples spread the "
            "families out, and any gap between groups gets multiplied by every waking hour of four years when it's "
            "projected. <bookmark mark='e'/> The contested part is the size and the cause of the gap, not the "
            "well-supported finding that children who hear more talk directed at them tend to learn more words."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in hour], lag_ratio=0.03), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in day], lag_ratio=0.03), FadeIn(rows[2]))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
