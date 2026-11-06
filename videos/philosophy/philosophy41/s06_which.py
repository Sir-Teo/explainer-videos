from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Which(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Which fairness?", r"Which criterion does fairness really require?", lit=(2020,), part=PART)
        with self.voiceover("Chapter five. Which fairness?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.coins()
        self.replies()
        self.worldviews()
        self.political()
        self.court()

    def coins(self):
        head = history_card(2021, r"Brian Hedden", r"``On Statistical Criteria of Algorithmic Fairness''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the coins", r"people hold coins of different biases; \ a predictor announces each coin's true bias", EXPL),
                (r"the result", r"perfectly fair by any reasonable standard, \ yet error rates differ between groups whose coins differ", RESP),
                (r"Hedden's conclusion", r"only calibration-like criteria are necessary for fairness; \ error-rate balance is not", FAIRC),
                (r"our population", r"exactly this: \ scores equal to true risks, \ and false-positive rates of 10\% and 31\%", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Which criterion is right? Brian Hedden argued in 2021 with a thought experiment. <bookmark "
            "mark='a'/>People in two rooms hold coins of different biases, and a predictor announces each coin's true "
            "bias before it is tossed. <bookmark mark='b'/>Nothing could be fairer, yet if the coins in one room are "
            "biased differently from those in the other, the predictor's error rates differ between the rooms. "
            "<bookmark mark='c'/>So, Hedden concluded, equal error rates cannot be necessary for fairness; only "
            "calibration-like criteria are. <bookmark mark='d'/>The Reasoner's population was exactly this case: "
            "scores equal to true risks, and false-positive rates of ten and thirty one percent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def replies(self):
        head = label(r"Why error rates may still matter", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the burden", r"a false positive can mean jail: \ who bears mistakes is a question of justice, \ not of accuracy", RESP),
                (r"Long \ (2021)", r"equal false-positive rates are not a requirement of fairness: \ they compare people unlike each other", EXPL),
                (r"Hellman \ (2020)", r"`Measuring Algorithmic Fairness': \ error-rate balance matters, \ because it tracks the burdens the system imposes", FAIRC),
                (r"base rates", r"if base rates reflect past injustice, \ calibration to them carries it forward", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Others reply that error rates still matter. <bookmark mark='a'/>A false positive in criminal justice can "
            "mean detention; who bears the mistakes is a question of justice, not of accuracy. <bookmark "
            "mark='b'/>Robert Long argued in 2021 that equal false-positive rates are not required by fairness, "
            "because they compare people who differ in risk. <bookmark mark='c'/>Deborah Hellman's Measuring "
            "Algorithmic Fairness, of 2020, defended the significance of error-rate balance, because it tracks the "
            "burdens a system imposes on each group. <bookmark mark='d'/>And if the base rates themselves reflect "
            "past injustice, a score calibrated to them carries that injustice forward."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def political(self):
        head = label(r"Fairness as political philosophy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Binns \ (2018)", r"`Fairness in Machine Learning: \ Lessons from Political Philosophy': \ each metric is a theory of justice", FAIRC),
                (r"equal opportunity", r"Rawls's fair equality of opportunity and Roemer's types: \ compensate circumstances, \ not choices \ (Part 38)", EXPL),
                (r"luck", r"is membership in a high-base-rate group a matter of brute luck? \ then error-rate balance looks right", RESP),
                (r"no metric is neutral", r"choosing one is choosing a conception of justice", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The debate is political philosophy in new dress. <bookmark mark='a'/>Reuben Binns argued in 2018 that "
            "each fairness metric encodes a theory of justice. <bookmark mark='b'/>Equal opportunity, as Hardt and "
            "colleagues named their criterion, echoes Rawls's fair equality of opportunity and Roemer's compensation "
            "for circumstances from Part 38. <bookmark mark='c'/>If belonging to a group with a high base rate is a "
            "matter of brute luck, the luck egalitarian will favour equal error rates. <bookmark mark='d'/>No metric "
            "is neutral: choosing one is choosing a conception of justice."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def court(self):
        head = history_card(2023, r"\textit{SFFA v. Harvard}", r"the US Supreme Court on race-conscious admissions", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the ruling", r"race-conscious admissions at Harvard and the University of North Carolina were held unlawful", BAD),
                (r"for algorithms", r"group-specific thresholds use the group explicitly: \ the same objection applies", RESP),
                (r"the tension", r"disparate-impact law looks at outcomes by group; \ disparate-treatment law forbids deciding by group", EXPL),
                (r"Ho and Xiang \ (2020)", r"`Affirmative Algorithms': \ fairness may require awareness of the group, \ and the law must make room for it", FAIRC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The choice among criteria is also a legal one. <bookmark mark='a'/>In 2023, in Students for Fair "
            "Admissions against Harvard, the United States Supreme Court held that race-conscious admissions at "
            "Harvard and at the University of North Carolina were unlawful. <bookmark mark='b'/>Group-specific "
            "thresholds, like the ones in chapter four, use the group explicitly, and face the same objection: they "
            "treat two people with the same score differently because of their group. <bookmark mark='c'/>This puts "
            "the law in tension with itself. Disparate-impact doctrine looks at outcomes by group and asks for "
            "unequal effects to be justified, while disparate-treatment doctrine forbids deciding by group at all. A "
            "model can satisfy one by violating the other. <bookmark mark='d'/>Daniel Ho and Alice Xiang argued that "
            "many fairness methods need awareness of the group to work, and that the law must find room for them, "
            "perhaps in the doctrines that once allowed government contractors to remedy their own past "
            "discrimination. The mathematics of chapter three meets the constitution here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def worldviews(self):
        head = label(r"Two worldviews \ (Friedler, \ Scheidegger and Venkatasubramanian)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"construct space", r"the qualities we actually care about, \ like risk of harm or merit, \ which are never observed directly", PRIV),
                (r"what you see is what you get", r"the observed features measure the construct faithfully: \ treat similar scores alike, \ and individual fairness suffices", EXPL),
                (r"we're all equal", r"the groups do not differ in the construct: \ observed differences are bias in measurement, \ and group parity is required", FAIRC),
                (r"the upshot", r"which criterion is right depends on how the observed relates to the construct: \ an assumption the data cannot test", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Sorelle Friedler, Carlos Scheidegger and Suresh Venkatasubramanian located the disagreement in a single "
            "assumption. <bookmark mark='a'/>Distinguish the construct space, the qualities we actually care about, "
            "such as the risk of causing harm, or merit, from the observed space, the features we can measure. We "
            "never see the construct directly. <bookmark mark='b'/>One worldview, what you see is what you get, "
            "assumes the observed features measure the construct faithfully. Then a calibrated score is the truth "
            "about each person, and treating similar scores alike is all fairness asks. <bookmark mark='c'/>The "
            "opposite worldview, we're all equal, assumes the groups do not differ in the construct, so any "
            "difference in the observed scores is bias in measurement, and fairness demands parity between groups. "
            "<bookmark mark='d'/>Each worldview makes one family of criteria correct, and the choice between them is "
            "an assumption about the relation between the observed and the unobserved, which the observed data alone "
            "cannot test. Hedden and Hellman were arguing, in part, about which world we are in."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
