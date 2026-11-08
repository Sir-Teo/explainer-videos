from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Criteria(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Three kinds of fairness", r"What does a fair prediction look like?", lit=(2016,), part=PART)
        with self.voiceover("Chapter two. Three kinds of fairness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.three()
        self.pairs()
        self.tradeoff()
        self.measurement()

    def three(self):
        head = history_card(2016, r"Hardt, \ Price and Srebro", r"``Equality of Opportunity in Supervised Learning''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"independence", r"$R \perp A$", FAIRC),
                (r"separation", r"$R \perp A \mid Y$", RESP),
                (r"sufficiency", r"$Y \perp A \mid R$", EXPL),
                (r"the vocabulary", r"Barocas, \ Hardt and Narayanan, \ \textit{Fairness and Machine Learning}: \ fairness as conditional independence", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Each side of the dispute was using a precise criterion, and they can be stated as conditional "
            "independence, following Solon Barocas, Moritz Hardt and Arvind Narayanan. Write A for the group, Y for "
            "the outcome and R for the prediction. Use the same R throughout; for a binary decision, take R to be "
            "Y hat. <bookmark mark='a'/>Independence: the distribution of predictions is the same across groups. "
            "For binary decisions, this is demographic parity. <bookmark mark='b'/>Separation: predictions are "
            "independent of group given the outcome. For binary decisions, this is equal false-positive and "
            "false-negative rates, the comparison ProPublica made. <bookmark mark='c'/>Sufficiency: the outcome is "
            "independent of group given the prediction. Calibration is a common way to achieve this for probability "
            "scores. <bookmark mark='d'/>Each criterion is a different "
            "answer to the question what fairness asks of a prediction."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tradeoff(self):
        sw = load("sweep")
        ts, H, R = sw["ts"], sw["hist"], sw["rates"]
        assert len(ts) == 17 and ts[8] == 0.5
        head = label(r"One threshold, \ two groups", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        x0, x1 = -6.4, 1.0
        w = (x1 - x0) / 20
        base = {"A": 1.25, "B": -1.75}
        cols = {"A": GA, "B": GB}
        panels = VGroup()
        for g in "AB":
            grp = VGroup()
            for k in range(20):
                h1, h0 = H[f"{g}1"][k] * 13, H[f"{g}0"][k] * 13
                x = x0 + (k + 0.5) * w
                if h1 > 1e-3:
                    grp.add(Rectangle(width=w * 0.88, height=h1, fill_color=RESP, fill_opacity=0.75,
                                      stroke_width=0).move_to([x, base[g] + h1 / 2, 0]))
                if h0 > 1e-3:
                    grp.add(Rectangle(width=w * 0.88, height=h0, fill_color=GREY_B, fill_opacity=0.55,
                                      stroke_width=0).move_to([x, base[g] - h0 / 2, 0]))
            grp.add(Line([x0, base[g], 0], [x1, base[g], 0], color=GREY_C, stroke_width=1.5))
            grp.add(label(rf"group {g}: \ base rate {R[g][0]['base'] * 100:.0f}\%", font_size=19,
                          color=cols[g]).move_to([x0 + 1.3, base[g] + 1.2, 0]))
            panels.add(grp)
        axis = VGroup(*[label(f"{v:.1f}", font_size=14, color=GREY_B).move_to([x0 + v * (x1 - x0), -3.25, 0])
                        for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0)])
        axl = label(r"risk score", font_size=16, color=GREY_B).move_to([(x0 + x1) / 2, -3.6, 0])
        key = label(r"above each axis: \ went on to reoffend; \ below: \ did not", font_size=17,
                    color=GREY_A).move_to([(x0 + x1) / 2, 2.85, 0])
        t = ValueTracker(0.5)
        line = always_redraw(lambda: DashedLine([x0 + t.get_value() * (x1 - x0), -3.05, 0],
                                                [x0 + t.get_value() * (x1 - x0), 2.55, 0], color=EXPL, stroke_width=3))
        tl = always_redraw(lambda: label(rf"threshold {t.get_value():.2f}", font_size=18, color=EXPL).next_to(
            line, UP, buff=0.05))
        names = [("fpr", r"false-positive rate", RESP), ("fnr", r"false-negative rate", FAIRC),
                 ("ppv", r"precision \ (PPV)", EXPL), ("selected", r"labelled high risk", GREY_A)]
        table = VGroup()
        hdr = VGroup(label(r"A", font_size=22, color=GA).move_to([4.6, 1.9, 0]),
                     label(r"B", font_size=22, color=GB).move_to([6.0, 1.9, 0]))
        table.add(hdr)
        for k, (key_, nm, c) in enumerate(names):
            y = 1.3 - 0.75 * k
            table.add(label(nm, font_size=18, color=c).move_to([2.7, y, 0]))
            for g, x in (("A", 4.6), ("B", 6.0)):
                vals = [r[key_] for r in R[g]]
                d = DecimalNumber(0, num_decimal_places=2, font_size=26, color=WHITE).move_to([x, y, 0])
                d.add_updater(lambda m, vals=vals: m.set_value(float(np.interp(t.get_value(), ts, vals))))
                table.add(d)
        with self.voiceover(
            "The Reasoner builds its own population to see what is going on. <bookmark mark='a'/>Two groups. In group "
            "A, thirty percent go on to reoffend; in group B, fifty percent. Each person's score is their true risk, "
            "so the score is perfectly calibrated in both groups: among everyone scored point six, sixty percent "
            "reoffend. Above each axis are those who reoffended; below, those who did not. <bookmark mark='b'/>A "
            "single threshold labels everyone above it high risk. At point five, the table shows each group's "
            "false-positive rate, its false-negative rate, and its precision, the share of those labelled high risk "
            "who reoffend. <bookmark mark='c'/>Because group B's scores sit higher, more of its innocent members "
            "cross the line: its false-positive rate is three times A's. <bookmark mark='d'/>Move the threshold down, "
            "and both groups' false positives rise; move it up, and false negatives rise. <bookmark mark='e'/>At no "
            "threshold do the two groups' error rates match, though the score itself treats everyone alike."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels), FadeIn(axis), FadeIn(axl), FadeIn(key))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(tl), FadeIn(table))
            vo.wait_until("c")
            self.play(Indicate(table[1:], color=RESP, scale_factor=1.02))
            vo.wait_until("d")
            self.play(t.animate.set_value(0.3), run_time=2.5)
            self.play(t.animate.set_value(0.75), run_time=3)
            vo.wait_until("e")
            self.play(t.animate.set_value(0.5), run_time=2)
        for m in table:
            m.clear_updaters()
        self.clear_scene()

    def measurement(self):
        head = label(r"What the label measures", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the label", r"$Y$ is usually an arrest or a reconviction, \ not an offence: \ it measures policing as well as behaviour", RESP),
                (r"Lum and Isaac \ (2016)", r"`To Predict and Serve?': \ trained on Oakland drug arrests, \ a predictive-policing model would have sent patrols mostly to Black neighbourhoods, \ though surveys put drug use about evenly across the city", EXPL),
                (r"Ensign et al. \ (2018)", r"runaway feedback loops: \ patrol where crime was found, \ and find crime where you patrol", BAD),
                (r"Jacobs and Wallach \ (2021)", r"`Measurement and Fairness': \ every criterion inherits the gap between a construct and what is measured", FAIRC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "All three criteria take the outcome Y for granted. But what is Y? <bookmark mark='a'/>In criminal "
            "justice it is usually a new arrest or a reconviction, not a new offence. An arrest records where the "
            "police were looking as well as what people did. <bookmark mark='b'/>Kristian Lum and William Isaac ran a "
            "predictive-policing algorithm on Oakland's records of drug arrests. It would have sent patrols mostly to "
            "Black neighbourhoods, though public-health surveys put drug use about evenly across the city. <bookmark "
            "mark='c'/>Danielle Ensign and colleagues showed how this can run away: patrol where crime was recorded, "
            "record more crime where you patrol, and the data confirm the patrols. <bookmark mark='d'/>Abigail Jacobs "
            "and Hanna Wallach drew the general lesson. A fairness criterion is a condition on measured variables, "
            "and every one of them inherits the gap between the thing we care about, like offending or need, and the "
            "thing we managed to measure. A perfectly calibrated score for arrests can be a biased score for crime."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pairs(self):
        head = VGroup(*[label(t, font_size=30, color=CONN) for t in
                        (r"independence", r"separation", r"sufficiency")]).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        rows = [
                (r"independence and sufficiency", r"$p_A\ne p_B,\quad R\perp A\ \Longrightarrow\ Y\not\!\perp A\mid R$", FAIRC),
                (r"independence and separation", r"$p_A\ne p_B,\quad R\perp A,\quad R\perp A\mid Y\ \Longrightarrow\ R\perp Y$", RESP),
                (r"separation and sufficiency", r"$p_A\ne p_B,\quad R\perp A\mid Y,\quad Y\perp A\mid R\ \Longrightarrow\ H(Y\mid R)=0$", EXPL),
                (r"so", r"$R=Y:\quad R\perp A\mid Y,\quad Y\perp A\mid R$", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "How do the three criteria relate? Apply them to the same prediction R. For binary outcomes with "
            "different, nondegenerate base rates, p A and p B, the cases differ. <bookmark mark='a'/>Independence "
            "and sufficiency would force equal base rates, so they cannot coexist here. <bookmark mark='b'/>"
            "Independence and separation together force the prediction to carry no information about the outcome. "
            "An uninformative prediction is an exception to the usual conflict. <bookmark mark='c'/>Separation "
            "and sufficiency force the outcome to be perfectly recoverable from the prediction: zero conditional "
            "entropy. A calibrated probability score would have to predict perfectly. <bookmark mark='d'/>So "
            "perfect prediction can satisfy separation and sufficiency, while an uninformative prediction can "
            "satisfy independence and separation. Also distinguish a score from its thresholded or post-processed "
            "decision: a calibrated score can coexist with an adjusted decision, because they are different "
            "predictions. Chapter three makes the score-level balance theorem precise."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
