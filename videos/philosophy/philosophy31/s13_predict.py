from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Predict(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Prediction and free energy", r"Is experience the brain's best guess?",
                            lit=(2010,), part=PART)
        with self.voiceover("Chapter twelve. Prediction and free energy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.free_energy()
        self.tmaze()
        self.beast()

    def free_energy(self):
        d = load("tmaze")
        head = label(r"Perception as inference", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["F_exact"], d["F_prior"], d["F_wrong"], d["surprise"]) == (0.6931, 1.9661, 3.8909, 0.6931)
        assert d["posterior"] == [0.98, 0.02]
        f1 = MathTex(r"F(q) \;=\; \mathbb{E}_{q(s)}\big[\ln q(s) - \ln p(o, s)\big]", font_size=34, color=PRED)
        f2 = MathTex(r"=\; \underbrace{D_{\mathrm{KL}}\big(q(s)\,\|\,p(s \mid o)\big)}_{\ge\, 0}"
                     r"\;-\; \ln p(o)", font_size=34, color=PRED)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 1.5, 0])
        fl = label(r"the negative of the ELBO \ (\textit{AI, Built})", font_size=18, color=GREY_A).next_to(fs, DOWN,
                                                                                                          buff=0.2)
        hd = [r"\text{belief } q \text{ after `cue says left'}", r"F \text{ (nats)}"]
        cells = [[label(r"the exact posterior \ $(0.98, \ 0.02)$", font_size=19, color=OK),
                  label(f"{d['F_exact']:.3f}", font_size=20, color=OK)],
                 [label(r"the prior, \ unrevised \ $(0.5, \ 0.5)$", font_size=19, color=GREY_A),
                  label(f"{d['F_prior']:.3f}", font_size=20, color=GREY_A)],
                 [label(r"the wrong way round \ $(0.1, \ 0.9)$", font_size=19, color=BAD),
                  label(f"{d['F_wrong']:.3f}", font_size=20, color=BAD)]]
        grid = ValueGrid(hd, cells, col_w=[6.2, 2.4], cell_h=0.55, font_size=19).move_to([0, -1.4, 0])
        foot = label(r"the minimum is the surprise, \ $-\ln p(o) = \ln 2 = 0.693$: \ reached by the exact posterior",
                     font_size=19, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A third family of theories says the brain is a prediction machine. The idea is Hermann von "
            "Helmholtz's, from 1867: perception is unconscious inference about the causes of our sensations. "
            "<bookmark mark='a'/>Karl Friston gave it a single quantity, the variational free energy F of a belief "
            "q about hidden states s, given an observation o. <bookmark mark='b'/>It splits into two terms: how far "
            "the belief is from the true posterior, which is never negative, minus the log probability of the "
            "observation. It is the negative of the evidence lower bound that trains variational autoencoders in "
            "AI, Built. <bookmark mark='c'/>A small example. A cue says the reward is on the left, and is right "
            "ninety eight times in a hundred. Believe the exact posterior, and F is 0.693 nats. Keep the even prior, "
            "and it is 1.966. Believe the cue backwards, and it is 3.891. <bookmark mark='d'/>The minimum is the "
            "surprise of the observation itself, the log of two: minimizing free energy is doing Bayesian "
            "inference, and bounding surprise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def tmaze(self):
        d = load("tmaze")
        head = label(r"An agent that looks before it leaps, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pol = {r["policy"]: r for r in d["policies"]}
        assert d["best"] == "look at the cue, then the cued arm"
        assert (pol["look at the cue, then the cued arm"]["G"], pol["go left at once"]["G"],
                pol["stay at the centre"]["G"], pol["look at the cue, then the other arm"]["G"]) == (
            -3.4273, -0.6625, 0.0, 2.1023)
        assert pol["look at the cue, then the cued arm"]["p"] == 0.8603
        # the maze
        c = np.array([-4.6, -0.2, 0])
        maze = VGroup(Line(c, c + UP * 1.4, color=GREY_B, stroke_width=6),
                      Line(c + UP * 1.4 + LEFT * 1.4, c + UP * 1.4 + RIGHT * 1.4, color=GREY_B, stroke_width=6),
                      Line(c, c + DOWN * 1.2, color=GREY_B, stroke_width=6))
        agent = Dot(c, radius=0.14, color=PRED)
        cue = VGroup(Square(side_length=0.4, color=SIG, fill_opacity=0.5)).move_to(c + DOWN * 1.2)
        arms = VGroup(label(r"left", font_size=17, color=GREY_A).next_to(c + UP * 1.4 + LEFT * 1.4, UP, buff=0.1),
                      label(r"right", font_size=17, color=GREY_A).next_to(c + UP * 1.4 + RIGHT * 1.4, UP, buff=0.1),
                      label(r"cue", font_size=17, color=SIG).next_to(cue, DOWN, buff=0.1))
        eq = MathTex(r"G(\pi) = \underbrace{-\mathbb{E}[\ln \tilde p(o)]}_{\text{risk}} \;-\; "
                     r"\underbrace{\mathbb{E}[D_{\mathrm{KL}}(q(s\mid o)\,\|\,q(s))]}_{\text{epistemic value}}",
                     font_size=28, color=PRED).move_to([2.2, 2.2, 0])
        hd = [r"\text{policy}", r"\text{risk}", r"\text{epistemic}", r"G", r"P(\pi)"]
        order = ["look at the cue, then the cued arm", "go left at once", "go right at once", "stay at the centre",
                 "look at the cue, then the other arm"]
        cells = [[label(k, font_size=17, color=OK if k == d["best"] else WHITE),
                  label(f"{pol[k]['risk']:.2f}", font_size=18, color=GREY_A),
                  label(f"{pol[k]['epistemic']:.2f}", font_size=18, color=GREY_A),
                  label(f"{pol[k]['G']:.2f}", font_size=18, color=PRED),
                  label(f"{pol[k]['p']:.3f}", font_size=18, color=OK if k == d["best"] else GREY_A)] for k in order]
        grid = ValueGrid(hd, cells, col_w=[4.2, 1.1, 1.6, 1.1, 1.2], cell_h=0.52, font_size=18).move_to([2.2, -0.6, 0])
        foot = label(r"reward $+3$, \ none $-3$ \ (nats of preference); \ two steps; \ the cue right 98\% of the time",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Active inference extends the idea to action. Friston and colleagues' T-maze, simplified. "
            "<bookmark mark='a'/>A reward is in the left arm or the right, with even odds. The agent can go "
            "straight to an arm, where it must stay, or first visit a cue at the bottom that points the right way "
            "ninety eight times in a hundred. <bookmark mark='b'/>Each plan is scored by its expected free energy: "
            "risk, how far the expected outcomes fall short of what the agent prefers, minus epistemic value, how "
            "much it expects to learn about where the reward is. <bookmark mark='c'/>Going straight to an arm has "
            "no expected reward, a coin toss, but it does teach the agent where the reward was: G is minus 0.66. "
            "Staying put teaches nothing: zero. Looking at the cue, then following it, both teaches and rewards: "
            "minus 3.43. Following the cue backwards: plus 2.10. <bookmark mark='d'/>Choosing in proportion to the "
            "exponential of minus G, the agent looks before it leaps eighty six percent of the time. Curiosity and "
            "reward come out of one quantity."
        ) as vo:
            self.play(FadeIn(head), Create(maze), FadeIn(agent), FadeIn(cue), FadeIn(arms))
            vo.wait_until("a")
            self.play(agent.animate.move_to(cue.get_center()), run_time=1.2)
            self.play(agent.animate.move_to(c), run_time=0.8)
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(5):
                self.play(*[FadeIn(x) for x in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(foot))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*grid.cell[0]), color=OK, scale_factor=1.04),
                      Succession(agent.animate.move_to(cue.get_center()), agent.animate.move_to(c),
                                 agent.animate.move_to(c + UP * 1.4), agent.animate.move_to(c + UP * 1.4 + LEFT * 1.4)))
        self.clear_scene()

    def beast(self):
        head = label(r"From prediction to experience?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Clark; \ Hohwy \ (2013)", r"perception as controlled hallucination: \ predictions, \ corrected by "
                                             r"error signals", PRED),
                (r"Seth \ (2021)", r"\textit{Being You}: \ the beast machine: \ emotion and selfhood as predictions "
                                   r"of the body's own state", FEEL),
                (r"the real problem", r"Seth: \ explain, \ predict and control the properties of experience, \ and the "
                                      r"hard problem may dissolve", GOAL),
                (r"the worry", r"a principle that fits every system explains nothing in particular; \ and why would "
                               r"predicting feel like anything?", BAD)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "How does any of this bear on experience? <bookmark mark='a'/>For Andy Clark and Jakob Hohwy, "
            "perception is controlled hallucination: the brain's predictions, held in check by the errors that "
            "the senses send back. What we experience is the prediction, not the input. "
            "<bookmark mark='b'/>Anil Seth's book of 2021 makes the body central: we are beast machines, and "
            "emotion and selfhood are predictions of the body's own condition, made to keep it alive. "
            "<bookmark mark='c'/>Seth calls his project the real problem: explain, predict and control the "
            "properties of experience, and the hard problem may come to look like the vital spirit of chapter ten "
            "of Part 30. <bookmark mark='d'/>The worries are two. The free-energy principle, Friston says, applies "
            "to anything that persists, so it cannot by itself pick out what is conscious. And the old question "
            "returns: why would predicting feel like anything?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
