from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


class Bandit(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.fit()
        self.recovery()

    def card(self):
        card = chapter_card(5, r"A bandit, \ and your learning rate", r"Can a model read a learner from its choices?",
                            lit={1952: r"Robbins"}, part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter five. A bandit, and your learning rate."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def game(self):
        d = load("bandit")
        head = heading(r"Two slot machines, \ one of them better, \ for now")
        A = axes([0, 200], [-0.1, 1.1], x_length=10.0, y_length=3.2, xticks=[0, 50, 100, 150, 200], yticks=[0, 0.5, 1],
                 xlabel=r"trial", ylabel=r"value", center=[0, 0.3, 0])
        ax = A.ax
        x = np.arange(200)
        qa = curve(ax, x, d["Q"][:, 0], CUE, 3)
        qb = curve(ax, x, d["Q"][:, 1], REWARD, 3)
        ticks = VGroup()
        for t, (c, r) in enumerate(zip(d["choices"], d["rewards"])):
            y = 1.05 if c == 0 else -0.05
            col = (CUE if c == 0 else REWARD) if r > 0 else GREY_D
            ticks.add(Line(ax.c2p(t, y - 0.03), ax.c2p(t, y + 0.03), color=col, stroke_width=2))
        flip = DashedLine(ax.c2p(100, -0.1), ax.c2p(100, 1.1), color=GREY_C, stroke_width=2)
        fl = label(r"the machines swap", font_size=20, color=GREY_A).next_to(ax.c2p(100, 1.1), UP, buff=0.05)
        lg = legend([(CUE, r"machine A: \ pays 80\%, \ then 20\%"), (REWARD, r"machine B: \ 20\%, \ then 80\%")],
                    font_size=20).next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"ticks: \ each choice, \ coloured when it paid", WHITE),
            (rf"Psyche plays with $\alpha$ = 0.3, \ $\beta$ = 5: \ win-stay {pct(d['win_stay'])}, \ lose-shift "
             rf"{pct(d['lose_shift'])}", MB),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.6)
        tag = psyche_tag(r"computed: \ \texttt{rl.q\_learning\_bandit}")
        with self.voiceover(
            "The simplest place to watch a learner choose is a two-armed bandit, named after slot machines, the "
            "one-armed bandits. <bookmark mark='a'/> Two machines; one pays eighty percent of the time and the other "
            "twenty. Halfway through, without warning, they swap. Here's Psyche playing, a Q-learner with a "
            "learning rate of point three. The lines are its two values; each tick is a choice, coloured when it "
            "paid. <bookmark mark='b'/> It settles on the good machine, keeps sampling the other now and then, and "
            "after the swap it takes a few disappointments to notice and switch. <bookmark mark='c'/> A summary often "
            "used with people is win-stay, lose-shift: how often you repeat a choice that paid, and leave one that "
            "didn't. The course page lets you play this game yourself, and fits your own learning rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(flip), FadeIn(fl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(qa), Create(qb), LaggedStart(*[FadeIn(k) for k in ticks], lag_ratio=0.01), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def fit(self):
        d = load("bandit")
        head = heading(r"Reading the learner back from its choices")
        lines = VGroup(
            MathTex(r"\log L(\alpha, \beta) = \sum_t \log P(a_t \mid Q_t;\ \beta)", font_size=44),
            MathTex(r"Q_{t+1}(a_t) = Q_t(a_t) + \alpha\,\big(r_t - Q_t(a_t)\big)", font_size=44),
        ).arrange(DOWN, buff=0.4).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"replay the choices through the model; \ score how probable each actual choice was", WHITE),
            (r"search for the $\alpha$ and $\beta$ that make the sequence most probable: \ maximum likelihood, \ "
             r"as in Part 11", VALUE),
            (rf"recovered from Psyche's 200 choices: \ $\alpha$ = {d['fit_alpha']:.2f}, \ $\beta$ = "
             rf"{d['fit_beta']:.1f} \ (true: \ 0.3 and 5): \ one player pins $\alpha$ down only loosely", DELTA),
        ], 12.4, 27, 0.34).move_to([0, -1.3, 0])
        tag = psyche_tag(r"computed: \ \texttt{rl.fit\_bandit}, \ L-BFGS from nine starting points")
        with self.voiceover(
            "Now the reverse problem, the one experimenters face. Given only someone's choices and rewards, what are "
            "their learning rate and their beta? <bookmark mark='a'/> Replay the sequence through the model. At each "
            "trial the model, with candidate parameters, says how likely each choice was; multiply the probabilities "
            "of the choices actually made. <bookmark mark='b'/> Then search for the parameters that make the observed "
            "sequence most likely, maximum likelihood, the same idea as fitting a psychometric function in Part 11. "
            "<bookmark mark='c'/> From Psyche's two hundred choices, the fit finds a beta close to the true five, but "
            "a learning rate of point five, where the truth was point three. Two hundred choices from one player "
            "constrain the learning rate only loosely, and that is worth checking systematically."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(lines))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def recovery(self):
        d = load("bandit")
        head = heading(r"Can the fit be trusted? \ Parameter recovery")
        A = axes([0, 1], [0, 1], x_length=3.8, y_length=3.8, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"true $\alpha$", ylabel=r"fitted $\alpha$", center=[-4.0, 0.0, 0])
        B = axes([0, 12], [0, 30], x_length=3.8, y_length=3.8, xticks=[0, 4, 8, 12], yticks=[0, 10, 20, 30],
                 xlabel=r"true $\beta$", ylabel=r"fitted $\beta$", center=[0.6, 0.0, 0])
        da = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_C, stroke_width=2)
        db = DashedLine(B.ax.c2p(0, 0), B.ax.c2p(12, 12), color=GREY_C, stroke_width=2)
        pa = scatter(A.ax, d["true_a"], d["fit_a"], MB, radius=0.06)
        pb = scatter(B.ax, d["true_b"], np.minimum(d["fit_b"], 30), VALUE, radius=0.06)
        rows = rows_of([
            (r"simulate 40 players with known parameters; \ fit each; \ compare", WHITE),
            (rf"learning rate: \ $r$ = {d['r_alpha']:.2f}", MB),
            (rf"inverse temperature: \ $r$ = {d['r_beta']:.2f}; \ large values are poorly pinned down", VALUE),
            (r"check this before reading anything into a fitted parameter, \ for people or for groups", YOU),
        ], 3.9, 24, 0.34).move_to([5.0, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ 40 simulated players, \ 200 trials each")
        with self.voiceover(
            "Before trusting a fitted number, check that the method can find it. <bookmark mark='a'/> Simulate many "
            "players whose parameters you know, fit each one, and compare. <bookmark mark='b'/> The learning rate "
            "comes back well. <bookmark mark='c'/> Beta, the decisiveness, comes back less well, especially when it's "
            "large: two hundred choices can't tell a very decisive player from an extremely decisive one, since both "
            "almost always pick the better machine. <bookmark mark='d'/> This check, parameter recovery, is "
            "routine in computational psychiatry, where fitted parameters are compared between patients and "
            "controls. A difference in a parameter that can't be recovered is a difference in noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), Create(da), Create(db), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pa], lag_ratio=0.05), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pb], lag_ratio=0.05), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
