from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Compas(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Machine bias", r"Was the risk score fair?", lit=(2016,), part=PART)
        with self.voiceover("Chapter one. Machine bias."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.numbers()
        self.aftermath()
        self.actuarial()
        self.pretrial()
        self.stakes()

    def aftermath(self):
        head = label(r"After the analysis", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"\textit{State v. Loomis} \ (2016)", r"Wisconsin's supreme court allowed COMPAS scores at sentencing, \ with written warnings about their limits", RESP),
                (r"Dressel and Farid \ (2018)", r"untrained people online predicted reoffending about as accurately as COMPAS: \ 67\% against 65\%", EXPL),
                (r"a simple rule", r"a regression on two features, \ age and prior convictions, \ did as well", FAIRC),
                (r"the question", r"not only whether the tool is accurate, \ but which errors fall on whom", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The case spread beyond journalism. <bookmark mark='a'/>In State versus Loomis, of 2016, Wisconsin's "
            "supreme court allowed COMPAS scores to be used at sentencing, provided judges were warned in writing "
            "about their limits. <bookmark mark='b'/>Julia Dressel and Hany Farid reported in 2018 that untrained "
            "people recruited online predicted reoffending about as accurately as COMPAS, sixty seven percent against "
            "sixty five. <bookmark mark='c'/>And a simple regression on just two features, age and the number of "
            "prior convictions, did as well. <bookmark mark='d'/>The deeper question is not only whether such a tool "
            "is accurate, but how its errors are distributed, and on whom they fall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def stakes(self):
        head = label(r"Where machines now decide", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"credit", r"lending models decide who borrows, \ and at what rate", EXPL),
                (r"hiring", r"Amazon scrapped a résumé screener in 2018 after it learned to penalize the word `women's'", RESP),
                (r"health", r"Obermeyer et al. \ (2019): \ an algorithm using past costs as a proxy for need under-referred Black patients", FAIRC),
                (r"faces", r"Buolamwini and Gebru \ (2018): \ commercial classifiers erred far more on darker-skinned women", PRIV)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The same questions arise wherever models allocate. <bookmark mark='a'/>Lending models decide who can "
            "borrow, and at what rate. <bookmark mark='b'/>Amazon, as Reuters reported in 2018, scrapped an "
            "experimental résumé screener after it learned to penalize résumés containing the word women's. <bookmark "
            "mark='c'/>Ziad Obermeyer and colleagues showed in 2019 that a widely used health algorithm, which "
            "predicted future costs as a proxy for medical need, referred Black patients for extra care far less "
            "often than equally sick white patients. <bookmark mark='d'/>And Joy Buolamwini and Timnit Gebru found in "
            "2018 that commercial face analysis systems erred far more often on darker-skinned women than on "
            "lighter-skinned men."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def numbers(self):
        head = label(r"The ProPublica analysis \ (Angwin et al., \ 2016), \ as reported", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"\text{Black defendants}", r"\text{white defendants}"]
        cells = [[label(r"did not reoffend, \ labelled higher risk", font_size=19, color=RESP),
                  label(r"44.9\%", font_size=22), label(r"23.5\%", font_size=22)],
                 [label(r"reoffended, \ labelled lower risk", font_size=19, color=FAIRC),
                  label(r"28.0\%", font_size=22), label(r"47.7\%", font_size=22)],
                 [label(r"of those labelled higher risk, \ reoffended", font_size=19, color=EXPL),
                  label(r"63\%", font_size=22), label(r"59\%", font_size=22)]]
        grid = ValueGrid(hd, cells, col_w=[5.6, 2.8, 2.8], cell_h=0.7, font_size=20).move_to([0, 0.8, 0])
        foot = stack([(r"rows 1 and 2: \ false-positive and false-negative rates \ (ProPublica)", GREY_A),
                      (r"row 3: \ positive predictive value, \ nearly equal \ (Dieterich, \ Mendoza and Brennan, \ "
                       r"Northpointe, \ 2016)", GREY_A),
                      (r"both analyses were correct; \ they measured different kinds of fairness", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In May 2016 the newsroom ProPublica published an analysis of COMPAS, a risk score used by courts in "
            "Broward County, Florida, and elsewhere, to predict whether defendants would reoffend. <bookmark "
            "mark='a'/>Among defendants who did not go on to reoffend, ProPublica reported, Black defendants had been "
            "labelled higher risk almost twice as often as white defendants: forty five percent against twenty three. "
            "<bookmark mark='b'/>Among those who did reoffend, white defendants had been labelled lower risk almost "
            "twice as often: forty eight percent against twenty eight. <bookmark mark='c'/>The company that made the "
            "score, then called Northpointe, replied that among defendants labelled higher risk, the share who "
            "reoffended was nearly the same in both groups, sixty three and fifty nine percent: the score meant the "
            "same thing whatever one's race. <bookmark mark='d'/>Both analyses were arithmetically correct. They "
            "measured different kinds of fairness, and this part shows why both cannot hold at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[i]], FadeIn(foot[min(i, 1)]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def actuarial(self):
        head = history_card(1928, r"Ernest Burgess", r"parole prediction in Illinois", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Burgess \ (1928)", r"21 factors, \ each scored 0 or 1, \ for 3,000 Illinois parolees: \ the more points, \ the likelier success", HIST),
                (r"Meehl \ (1954)", r"\textit{Clinical versus Statistical Prediction}: \ simple formulas matched or beat expert judgment", EXPL),
                (r"Grove et al. \ (2000)", r"a meta-analysis of 136 studies: \ mechanical prediction was as good or better in the great majority", FAIRC),
                (r"Harcourt \ (2007)", r"\textit{Against Prediction}: \ policing by prediction can ratchet up the share of one group under control", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Scoring people for risk is almost a century old. <bookmark mark='a'/>In 1928 the sociologist Ernest "
            "Burgess studied three thousand men paroled in Illinois. He scored twenty-one factors, one point for each "
            "favourable one, and found that the more points a man had, the likelier he was to succeed on parole. "
            "Illinois began using the score in the nineteen thirties. <bookmark mark='b'/>In 1954 the psychologist "
            "Paul Meehl reviewed studies comparing clinical judgment with simple statistical formulas, and found the "
            "formulas matched or beat the experts. <bookmark mark='c'/>Half a century later, a meta-analysis of one "
            "hundred and thirty-six studies by William Grove and colleagues found mechanical prediction as good or "
            "better in the great majority. <bookmark mark='d'/>Bernard Harcourt's Against Prediction, in 2007, argued "
            "the other side: if a group is policed more because it is predicted to offend more, its members are "
            "caught more, its share of the records rises, and the prediction ratchets upward. The accuracy of a tool "
            "and its justice were separate questions long before COMPAS."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pretrial(self):
        head = label(r"Risk tools in pretrial justice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the setting", r"most people held in American jails have not been convicted: \ they are awaiting trial", RESP),
                (r"New Jersey \ (2017)", r"largely replaced cash bail with a risk assessment and release conditions; \ the pretrial jail population fell sharply", FAIRC),
                (r"California \ (2020)", r"voters rejected Proposition 25, \ which would have replaced cash bail with risk assessment", BAD),
                (r"the comparison", r"the alternative to a tool is not perfect justice, \ but a judge's hunch, \ a bail schedule, \ or the ability to pay", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Where do these tools actually decide things? Often before any trial. <bookmark mark='a'/>Most people "
            "held in American jails have not been convicted of anything: they are waiting for their cases to be "
            "heard, often because they cannot pay bail. <bookmark mark='b'/>In 2017 New Jersey largely replaced cash "
            "bail with a risk assessment and conditions of release, and its pretrial jail population fell sharply. "
            "<bookmark mark='c'/>In 2020 California's voters went the other way. They rejected Proposition "
            "twenty-five, which would have replaced cash bail with risk assessment, after a campaign in which some "
            "civil-rights groups opposed the tools as biased. <bookmark mark='d'/>The philosophical point is the "
            "baseline. The alternative to an algorithm is not perfect justice; it is a judge's hunch, a fixed "
            "schedule of bail amounts, or release for those who can pay. Whether a tool is fair depends on what it "
            "replaces as well as on its error rates."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
