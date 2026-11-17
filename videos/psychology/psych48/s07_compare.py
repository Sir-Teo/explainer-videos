from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Compare(VoiceoverScene):
    def construct(self):
        self.card()
        self.criteria()
        self.confusion()
        self.crossval()

    def card(self):
        card = chapter_card(6, r"Model comparison", r"Which program made the data?",
                            lit={1974: r"Akaike", 2002: r"Pitt \& Myung"}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter six. Model comparison."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def criteria(self):
        head = heading(r"Four ways to compare")
        data = (
            (r"likelihood ratio", r"for nested models: \ twice the gain in log-likelihood, \ against a chi-square", SYMP),
            (r"AIC and BIC", r"penalize each parameter: \ AIC by 2 (prediction), \ BIC by $\log n$ (finding the "
                             r"true model, \ if it is among them)", MODEL),
            (r"cross-validation", r"fit on some trials or people, \ predict the rest: \ the most direct test of "
                                  r"generalization", GOOD),
            (r"Bayes factors", r"the evidence for each model averaged over its prior: \ honest about flexibility, \ "
                               r"sensitive to the prior (\emph{Statistics, Built} Part 28)", PERSON),
            (r"over a group", r"different people may use different models: \ estimate how common each model is, \ "
                              r"not just which wins on the pooled data", AUTH),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.0), wrapped_label(how, 9.2, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, -0.3, 0])
        with self.voiceover(
            "How to choose among models. <bookmark mark='a'/> For nested models, a likelihood ratio test. "
            "<bookmark mark='b'/> AIC and BIC penalize each parameter, AIC for the sake of prediction, BIC for "
            "finding the true model if it's among the candidates. <bookmark mark='c'/> Cross-validation fits on some "
            "trials or people and predicts the rest, the most direct test of generalization. <bookmark mark='d'/> "
            "Bayes factors weigh the evidence for each model averaged over its prior: honest about flexibility, "
            "sensitive to the prior. <bookmark mark='e'/> And over a group: different people may use different "
            "models, so estimate how common each model is, not just which wins on the pooled data."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def confusion(self):
        d = load("confusion")
        head = heading(r"Model recovery")
        names = (r"coin", r"WSLS", r"Q", r"Q + pers.")
        M = np.asarray(d["confusion"])
        cell = 0.85
        grid = VGroup()
        for i in range(4):
            for j in range(4):
                v = float(M[i, j])
                sq = Square(cell, stroke_width=1, stroke_color=BLACK,
                            fill_color=interpolate_color(ManimColor("#14181F"), ManimColor(GOOD), v), fill_opacity=1)
                sq.move_to([-5.2 + j * cell, 1.3 - i * cell, 0])
                grid.add(VGroup(sq, label(f"{v:.2f}", font_size=15, color=WHITE if v < 0.6 else BLACK).move_to(sq)))
        rl = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(grid[4 * i], LEFT, buff=0.1) for i, n in enumerate(names)])
        cl = VGroup(*[label(n, font_size=14, color=GREY_A).next_to(grid[j], UP, buff=0.1) for j, n in enumerate(names)])
        axl = VGroup(label(r"true model (rows)", font_size=13, color=GREY_B).next_to(grid, DOWN, buff=0.2),
                     label(r"chosen by BIC (columns)", font_size=13, color=GREY_B).next_to(cl, UP, buff=0.1))
        rows = rows_of([
            (rf"Psyche simulates {d['reps']} learners from each model, \ fits all four, \ and picks by BIC", WHITE),
            (r"the diagonal is recovery; \ off the diagonal, \ confusion", MODEL),
            (rf"here recovery is good: \ {100 * min(np.diag(M)):.0f}\% or more on the diagonal; \ "
             rf"{100 * M[3, 2]:.0f}\% of perseverating learners still look like plain Q-learners", AUTH),
            (r"so a model that wins on real data has to be checked the same way: \ could the comparison have found "
             r"the alternatives?", YOU),
        ], 5.4, 18, 0.36).move_to([3.8, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.model\_confusion}")
        with self.voiceover(
            "And the comparison itself must be checked. <bookmark mark='a'/> Psyche simulates learners from each of "
            "the four models, fits all four to every dataset, and picks by BIC. <bookmark mark='b'/> The diagonal is "
            "recovery; off it, confusion. <bookmark mark='c'/> Here recovery is good: more than nine in ten of each "
            "model's learners are identified. A few perseverating learners still look like plain Q-learners, because "
            "their pull is too weak for two hundred choices to pay for a third parameter. With fewer trials, or more "
            "similar models, the matrix blurs. <bookmark mark='d'/> So a model that wins on real data must be checked "
            "the same way, for its own task and trial count. Could the comparison have found the alternatives?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(rl), FadeIn(cl), FadeIn(axl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def crossval(self):
        d = load("crossval")
        head = heading(r"Predict the next session")
        A = axes([0.3, 4.7], [-0.8, 0], x_length=6.0, y_length=3.0, xticks=None, yticks=[-0.75, -0.5, -0.25, 0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"log-likelihood per choice, \ new session", center=[-3.1, 0.3, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2, 3, 4], d["held_out"], [GREY_B, GREY_B, MODEL, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.3, 11, WHITE).next_to(A.ax.c2p(i + 1, -0.8), DOWN, buff=0.12) for i, t in
                         enumerate((r"random", r"win-stay lose-shift", r"Q-learning", r"Q + perseveration"))])
        rows = rows_of([
            (r"30 perseverating learners, \ each playing two sessions; \ every model fitted to the first, \ scored "
             r"on the second", WHITE),
            (r"held-out prediction rewards a model only for what generalizes: \ extra parameters that fit noise are "
             r"punished automatically", MODEL),
            (rf"the true model predicts the new session best; \ BIC on the first session chose it for "
             rf"{100 * d['bic_share'][3]:.0f}\% of learners", GOOD),
            (r"when they disagree, \ trust the one that answers the question asked: \ prediction, \ or the true "
             r"model", YOU),
        ], 5.6, 18, 0.34).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.fit}, \ \texttt{fit.loglik}")
        with self.voiceover(
            "Another way to compare: predict data the model hasn't seen. <bookmark mark='a'/> Thirty perseverating "
            "learners each play two sessions. Every model is fitted to the first and scored on the second. "
            "<bookmark mark='b'/> Held-out prediction rewards a model only for what generalizes, so extra parameters "
            "that fit noise are punished automatically. <bookmark mark='c'/> The true model predicts the new session "
            "best, and BIC on the first session chose it for more than nine learners in ten. <bookmark mark='d'/> "
            "When the two disagree, trust the one that answers the question you're asking: prediction, or which "
            "model is true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
