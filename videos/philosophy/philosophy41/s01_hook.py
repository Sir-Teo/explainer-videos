from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"There's software used across the country to predict future criminals. \ And it's biased "
                       r"against blacks.", r"ProPublica", r"`Machine Bias' \ (Angwin, \ Larson, \ Mattu and Kirchner, "
                       r"\ 2016)", width=8.8, font_size=28).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "This is the first of two final parts about the reasoners we build. Part 40 ended with machines that "
            "judge beauty. Machines now judge people: who gets bail, a loan, a job interview or extra medical care. "
            "<bookmark mark='a'/>In 2016 a newsroom's investigation began by claiming that software "
            "used across the country to predict future criminals was biased against Black "
            "defendants. <bookmark mark='b'/>The company replied that its software was fair. This part shows that both "
            "were right, proves why, and asks what fairness, privacy and explanation require of machines that decide."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=RESP, scale_factor=1.03))
        self.clear_scene()

    def questions(self):
        head = label(r"Four questions about machines that decide", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"fairness", r"which of several incompatible kinds of fairness should a prediction have?", FAIRC),
                (r"discrimination", r"when is treating groups differently wrong, \ and why?", RESP),
                (r"privacy", r"can data be useful without exposing the people in it?", PRIV),
                (r"explanation", r"what are we owed when a machine judges us, \ and who answers for it?", EXPL)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>Fairness: which of several incompatible kinds "
            "of fairness should a prediction have? <bookmark mark='b'/>Discrimination: when is treating groups "
            "differently wrong, and why? <bookmark mark='c'/>Privacy: can data be useful without exposing the people "
            "in it? <bookmark mark='d'/>And explanation: what are we owed when a machine judges us, and who answers "
            "for its mistakes? The answer to the first, an impossibility theorem, is this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"COMPAS: \ ProPublica's numbers, \ Northpointe's reply",
            r"independence, \ separation, \ sufficiency; \ a threshold sweeping two populations",
            r"Chouldechova's identity, \ proved and checked; \ Kleinberg's balance \ (the Wall)",
            r"thresholds for each group; \ the cost of fairness",
            r"Hedden's coins; \ fairness as political philosophy",
            r"individual and counterfactual fairness, \ on a causal model; \ discrimination",
            r"differential privacy: \ the Laplace mechanism, \ randomized response, \ a reconstruction attack",
            r"Shapley and counterfactual explanations; \ opacity; \ responsibility gaps",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The COMPAS controversy, with both sides' numbers. <bookmark "
            "mark='b'/>Three criteria of fairness, and a threshold sweeping across two populations built by the "
            "Reasoner. <bookmark mark='c'/>Chouldechova's identity, proved on screen and checked, and Kleinberg, "
            "Mullainathan and Raghavan's theorem: this part's brick in the Wall. <bookmark mark='d'/>Thresholds for "
            "each group, and the cost of fairness. <bookmark mark='e'/>Hedden's coins, and fairness as political "
            "philosophy. <bookmark mark='f'/>Individual and counterfactual fairness, on a causal model, and the "
            "ethics of discrimination. <bookmark mark='g'/>Differential privacy: the Laplace mechanism, randomized "
            "response, and an attack that rebuilds a database. <bookmark mark='h'/>And explanations, opacity, and who "
            "is responsible when a machine errs."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
