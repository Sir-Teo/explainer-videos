from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ solvers that differentiate", r"What if the solver also returned derivatives?",
             "Chapter sixteen. Frontier: solvers that differentiate.",
             lit={2021: r"Maliar, Maliar and Winant", 2022: r"Azinovic et al."}, scale=("nation", "world"),
             horizon=("a decade",))
        self.derivative()
        self.deep()
        self.open_questions()

    def derivative(self):
        F = load("frontier")
        eq = MathTex(r"R(\theta;\beta) = 0 \;\Longrightarrow\; \frac{d\theta}{d\beta} = -\Big(\frac{\partial R}"
                     r"{\partial\theta}\Big)^{-1}\frac{\partial R}{\partial\beta}", font_size=42,
                     color=THEORY).move_to(UP * 1.7)
        rows = VGroup(
            label(r"the collocation equations hold at the solution for every $\beta$, \ so differentiate them",
                  font_size=21, color=WHITE),
            label(rf"implicit function theorem: \ $dc(k^*)/d\beta = {F['dc_ift']:.6f}$".replace("-", "{-}"),
                  font_size=23, color=PROJ),
            label(rf"solving twice and differencing: \ ${F['dc_fd']:.6f}$".replace("-", "{-}"), font_size=23,
                  color=VFI),
            label(r"one linear solve instead of two more solutions: \ what differentiable programming automates",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.6)
        with self.voiceover(
            "The frontier first. Estimation needs to know how the solution moves when a parameter moves. <bookmark "
            "mark='a'/> The collocation equations hold at the solution for every value of beta, so they can be "
            "differentiated: the derivative of the coefficients is one linear solve with the matrix Newton's method "
            "already built. <bookmark mark='b'/> Here, how consumption at the steady-state capital responds to "
            f"the discount factor: {say_num(F['dc_ift'], 4)}, <bookmark mark='c'/> the same, to six digits, as "
            "solving the model twice and differencing. <bookmark mark='d'/> Differentiable programming, the "
            "machinery of modern machine learning, does this automatically through any solver, so that "
            "estimation can follow gradients instead of guessing."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def deep(self):
        chain = flow_chain([(r"draw states \\ at random", GRID), (r"a neural network \\ gives the policy", VALUE),
                            (r"the Euler residuals \\ at those states", ERR), (r"adjust the weights \\ to shrink them",
                                                                               POLICY)],
                           box_w=2.7, box_h=1.1, buff=0.45, font_size=19,
                           notes=[r"no grid", r"thousands of \\ weights", r"chapter eight's \\ yardstick",
                                  r"gradient descent"], note_size=15)
        chain.move_to(UP * 0.8)
        foot = VGroup(
            label(r"economies with hundreds of state variables: \ generations, \ firms, \ countries", font_size=21,
                  color=WHITE),
            label(r"the same test applies: \ Euler errors on states the network never saw", font_size=21,
                  color=ERR),
        ).arrange(DOWN, buff=0.3).next_to(chain, DOWN, buff=0.8)
        tag = published_tag(r"Maliar, Maliar and Winant, \ JME (2021); \ Azinovic, Gaegauf and Scheidegger, \ IER "
                            r"(2022)", corner=DR, font_size=11)
        with self.voiceover(
            "Second, the curse of dimensionality, attacked with machine learning. <bookmark mark='a'/> Draw states "
            "of the economy at random, with no grid at all. <bookmark mark='b'/> Let a neural network propose the "
            "policy at each. <bookmark mark='c'/> Compute the Euler residuals there, the yardstick of chapter "
            "eight, <bookmark mark='d'/> and adjust the network's weights to shrink them. Lilia Maliar, Serguei "
            "Maliar and Pablo Winant, and Marlon Azinovic, Luca Gaegauf and Simon Scheidegger, published such "
            "methods in 2021 and 2022. <bookmark mark='e'/> They solve economies with hundreds of state variables, "
            "such as many overlapping generations, and they must be checked the same way as any other method: by "
            "Euler errors on states the network never saw."
        ) as vo:
            self.play(FadeIn(tag))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if i == 0:
                    self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
                else:
                    self.play(GrowArrow(chain.arrows[i - 1]), FadeIn(chain.boxes[i]), FadeIn(chain.notes[i]),
                              run_time=0.9)
            vo.wait_until("e")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
        self.clear_scene()

    def open_questions(self):
        cards = point_cards([
            (r"certifying accuracy", r"a bound on the error in a hundred dimensions, \ not just a sample of it",
             ERR),
            (r"many households, \ fast", r"linearizing in sequence space, \ around a solved household \ (Part 52)",
             EGM),
            (r"global and local", r"when a perturbation is safe, \ and when only a global method will do", PERT),
            (r"reproducible training", r"networks trained with randomness: \ seeds, \ hardware, \ reports", VALUE),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Certifying accuracy: in a hundred dimensions the errors can "
            "only be sampled, and a bound on the worst one is hard to come by. <bookmark mark='b'/> Solving models "
            "with millions of different households quickly, for which the newest methods linearize around a solved "
            "household in sequence space, the subject of the next part. <bookmark mark='c'/> Knowing in advance when "
            "a local method is safe and when only a global one will do. <bookmark mark='d'/> And making "
            "computations that involve random training as reproducible as the ones in this film."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
