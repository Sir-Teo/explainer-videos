from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Individual(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Individuals and counterfactuals", r"Would the decision have differed had you been in the other group?", lit=(2012, 2017), part=PART)
        with self.voiceover("Chapter six. Individuals and counterfactuals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.individual()
        self.counterfactual()
        self.critique()
        self.subgroups()

    def individual(self):
        head = history_card(2012, r"Dwork et al.", r"``Fairness Through Awareness''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the principle", r"similar individuals should be treated similarly", FAIRC),
                (r"as a formula", r"$D(M(x), M(y)) \le d(x, y)$: \ the mechanism is Lipschitz in a task-specific metric $d$", EXPL),
                (r"the catch", r"everything rests on $d$: \ deciding who is similar to whom is the moral question itself", BAD),
                (r"and groups", r"individual fairness can coexist with large group disparities, \ and vice versa", RESP)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Group criteria compare averages. Cynthia Dwork and colleagues proposed in 2012 a criterion about "
            "individuals. <bookmark mark='a'/>Similar individuals should be treated similarly. <bookmark "
            "mark='b'/>Formally, the distance between the decisions for x and y should be at most the distance "
            "between x and y themselves, in a metric chosen for the task: a Lipschitz condition. <bookmark "
            "mark='c'/>The catch is that everything rests on that metric: deciding who is relevantly similar to whom "
            "is the moral question itself, now hidden inside a function. <bookmark mark='d'/>And individual fairness "
            "can coexist with large disparities between groups."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def critique(self):
        head = label(r"Can race be a cause?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Kohler-Hausmann \ (2019)", r"race is not a variable that can be toggled while everything else is held fixed: \ it is a social category constituted by many things", BAD),
                (r"path-specific effects", r"Chiappa \ (2019); \ Nabi and Shpitser \ (2018): \ allow some causal paths from the group, \ forbid others", EXPL),
                (r"which paths?", r"whether a path is legitimate \ (through qualifications? \ through neighbourhood?) \ is a moral judgment", FAIRC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The counterfactual approach has critics. <bookmark mark='a'/>Issa Kohler-Hausmann argued in 2019 that "
            "race is not a variable that can be toggled while everything else is held fixed; it is a social category "
            "constituted by many of the very things a model would hold fixed. <bookmark mark='b'/>Path-specific "
            "approaches, by Silvia Chiappa and by Razieh Nabi and Ilya Shpitser, allow some causal paths from group "
            "membership to the decision and forbid others. <bookmark mark='c'/>But which paths are legitimate, "
            "through qualifications or through neighbourhood, is again a moral judgment, not a statistical one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def counterfactual(self):
        d = load("cf")
        P = d["people"]
        assert d["fair_u"] and len(P) == 8
        head = label(r"Counterfactual fairness \ (Kusner et al., \ 2017)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eqs = VGroup(MathTex(r"U \sim N(0, 1)", font_size=28),
                     MathTex(r"X = U - 1.0\,A + \varepsilon", font_size=28),
                     MathTex(r"Y = U", font_size=28)).arrange(RIGHT, buff=0.8).move_to([0, 2.3, 0])
        hd = [r"A", r"U", r"X", r"\text{pred. from } X", r"\text{had } A \text{ differed}",
              r"\text{pred. from } \hat U", r"\text{had } A \text{ differed}"]
        cells = []
        for p0 in P[:6]:
            cells.append([label(str(p0["A"]), font_size=18, color=GA if p0["A"] == 0 else GB),
                          label(f"{p0['U']:+.2f}", font_size=18, color=GREY_A), label(f"{p0['X']:+.2f}", font_size=18),
                          label(f"{p0['pred_x']:+.2f}", font_size=18),
                          label(f"{p0['pred_x_cf']:+.2f}", font_size=18, color=BAD),
                          label(f"{p0['pred_u']:+.2f}", font_size=18),
                          label(f"{p0['pred_u_cf']:+.2f}", font_size=18, color=OK)])
        grid = ValueGrid(hd, cells, col_w=[0.8, 1.2, 1.2, 2.2, 2.4, 2.2, 2.4], cell_h=0.45, font_size=17).move_to([0, 0.1, 0])
        foot = stack([(r"a predictor using the test score $X$ changes by 1.0 when only group membership is changed", BAD),
                      (r"a predictor using the ability recovered by the model, \ $\hat U = X + 1.0\,A$, \ does not change",
                       OK),
                      (r"the price: \ we must trust the causal model", GREY_A)], font_size=20, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Matt Kusner, Joshua Loftus, Chris Russell and Ricardo Silva proposed in 2017 a criterion that uses the "
            "causal models of Part 17. <bookmark mark='a'/>The Reasoner writes one. Each person has an ability U. "
            "Their test score X is the ability, minus one point if they belong to group one, whose schools were "
            "worse, plus a little noise. The outcome to be predicted depends on ability alone. <bookmark mark='b'/>A "
            "predictor that uses the test score directly is accurate on average, but ask the counterfactual question: "
            "what would it have predicted for this very person, with the same ability and the same luck, had they "
            "belonged to the other group? The answer changes by a full point. <bookmark mark='c'/>A predictor that "
            "first recovers ability from the model, adding back the point the group lost, predicts the same in both "
            "worlds. It is counterfactually fair. <bookmark mark='d'/>The price is that we must trust the causal "
            "model, and know how group membership shaped each measurement."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs))
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c0) for rw in grid.cell for c0 in rw[:3]])
            vo.wait_until("b")
            self.play(*[FadeIn(c0) for rw in grid.cell for c0 in rw[3:5]], FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c0) for rw in grid.cell for c0 in rw[5:]], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def subgroups(self):
        head = label(r"Groups within groups", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Crenshaw \ (1989)", r"intersectionality: \ discrimination against Black women can be invisible to a law that checks race and sex separately", HIST),
                (r"fairness gerrymandering", r"Kearns, \ Neel, \ Roth and Wu \ (2018): \ a classifier fair to each race and to each sex can be unfair to their intersections", BAD),
                (r"the fix", r"audit over a rich family of subgroups at once, \ as multicalibration does for scores", FAIRC),
                (r"the price", r"the finer the subgroups, \ the less data in each: \ fairness to the smallest groups is the hardest to certify", EXPL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Between the individual and the group lies a middle ground: groups within groups. <bookmark mark='a'/>In "
            "1989 the legal scholar Kimberlé Crenshaw showed how courts had dismissed claims by Black women because "
            "the employer hired Black men and hired white women, so neither race nor sex discrimination could be "
            "shown. She called the blind spot intersectionality. <bookmark mark='b'/>Michael Kearns, Seth Neel, Aaron "
            "Roth and Steven Wu found the same blind spot in machine learning, and called it fairness gerrymandering: "
            "a classifier can be fair to each race and to each sex while being unfair to their intersections. "
            "<bookmark mark='c'/>Their fix is to audit over a rich family of subgroups at once, the same move "
            "multicalibration makes for scores. <bookmark mark='d'/>The price is statistical. The finer the "
            "subgroups, the fewer people in each, and the noisier every estimate of their error rates; fairness to "
            "the smallest groups is the hardest to certify, though they may need it most."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
