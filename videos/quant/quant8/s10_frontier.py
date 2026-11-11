from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE

NODES = {"DP": (r"dynamic programming", (-4.6, 1.6), VALUE), "HJB": (r"HJB / Merton", (-1.2, 2.4), VALUE),
         "STOP": (r"optimal stopping", (2.6, 2.2), OVER), "BSDE": (r"BSDEs", (5.0, 0.6), ALT),
         "MFG": (r"mean-field games", (3.0, -1.4), ALT), "RL": (r"reinforcement learning", (-1.0, -0.6), GOOD),
         "KELLY": (r"Kelly and ergodicity", (-4.8, -1.4), KELLY)}

PAPERS = [  # (edge, title, what it found)
    (("RL", "HJB"), r"Jia and Zhou (2023), ``q-Learning in Continuous Time'', \textit{JMLR} 24",
     r"what a Q-function becomes as the time step shrinks, and how to learn it"),
    (("RL", "HJB"), r"Dai, Dong, Jia and Zhou (2023; rev.\ 2026), ``Data-Driven Merton's Strategies via Policy "
                    r"Randomization'', arXiv 2312.11797",
     r"the mean of the best randomized policy solves Merton: learn it by actor--critic without estimating $\mu$"),
    (("RL", "HJB"), r"Dai, Dong, Jia and Zhou (2026), ``Merton's Problem with Recursive Perturbed Utility'', arXiv "
                    r"2602.13544", r"a closed-form Gaussian policy that does not depend on wealth"),
    (("DP", "RL"), r"Huh, Jeon, Koo and Lim (2025), ``Breaking the Dimensional Barrier for Constrained Dynamic "
                   r"Portfolio Choice'', arXiv 2501.12600",
     r"Pontryagin-guided neural methods: constrained numerical examples up to a hundred assets; tensor grids scale exponentially"),
    (("DP", "RL"), r"Huh and Koo (2026), arXiv 2601.03175", r"parameter uncertainty in high dimensions; a model-free "
                                                            r"PPO baseline ``remains far from the targets''"),
    (("MFG", "RL"), r"Lauri\`ere, Perrin, P\'erolat et al., ``Learning in Mean Field Games: A Survey'', arXiv 2205.12944",
     r"model-free learning of crowd equilibria"),
    (("STOP", "BSDE"), r"Chee, Frikha and Li (2026), ``A Monotone Limit Approach to Entropy-Regularized American "
                       r"Options'', arXiv 2602.18062", r"exploration meets reflected BSDEs, with convergence rates"),
    (("KELLY", "RL"), r"Toda (2023), ``Ergodicity Economics is Pseudoscience'', arXiv 2306.03275",
     r"a critique of the ergodicity programme of chapter 10"),
]


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.graph()

    def card(self):
        c = chapter_card(18, r"The frontier, 2023 to 2026", r"Where are learning and control meeting now?",
                         lit=(2025,), part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def graph(self):
        nodes = {}
        for k, (name, (x, y), col) in NODES.items():
            t = label(name, font_size=22, color=col)
            box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=col,
                                   stroke_width=1.5, fill_color="#0E141C", fill_opacity=1).move_to([x, y + 0.6, 0])
            t.move_to(box)
            nodes[k] = VGroup(box, t).set_z_index(2)  # above every edge: lines run behind the opaque boxes
        base = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=GREY_D, stroke_width=1.5)
                        for a, b in (("DP", "HJB"), ("HJB", "STOP"), ("STOP", "BSDE"), ("BSDE", "MFG"), ("HJB", "MFG"),
                                     ("DP", "RL"), ("HJB", "RL"), ("MFG", "RL"), ("KELLY", "DP"), ("KELLY", "RL"))])
        base.set_z_index(0)

        def cap(i):
            _, title, what = PAPERS[i]
            c = VGroup(wrapped_label(title, 12.6, 19, WHITE), wrapped_label(what, 12.6, 19, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            return c.to_edge(DOWN, buff=0.35)

        def lit(i):
            a, b = PAPERS[i][0]
            return Line(nodes[a].get_center(), nodes[b].get_center(), color=KELLY, stroke_width=6).set_z_index(1)

        self.cur, self.hi = None, None

        def show(i):
            new, newl = cap(i), lit(i)
            anims = [FadeIn(new), Create(newl)]
            if self.cur is not None:
                anims += [FadeOut(self.cur), self.hi.animate.set_stroke(color=GREY_B, width=3)]
            self.play(*anims)
            self.cur, self.hi = new, newl

        with self.voiceover(
            "The chapters of this part form a graph, and current research lives on its edges. "
            "<bookmark mark='a'/> Between learning and the HJB equation: Yanwei Jia and Xun Yu Zhou's 2023 paper in "
            "the Journal of Machine Learning Research works out what Q-learning means when time is continuous."
        ) as vo:
            self.play(*[FadeIn(n_) for n_ in nodes.values()], Create(base), run_time=1.5)
            vo.wait_until("a")
            show(0)
        with self.voiceover(
            "Min Dai, Yuchao Dong, Jia and Zhou showed that the best randomized policy for Merton's problem has Merton's fraction as its mean, so an actor-critic learner can find it from data without ever estimating the expected return, the input chapter five called the least certain number in finance. Avoiding an explicit drift estimate does not remove statistical uncertainty; the claim is specific to the randomized-control model and objective."
        ):
            show(1)
        with self.voiceover(
            "In a 2026 paper the same group finds, for a recursive version of the problem, a closed-form Gaussian policy that "
            "does not depend on wealth, and whose spread shrinks as risk aversion and volatility rise: exploration, priced "
            "into the objective."
        ):
            show(2)
        with self.voiceover(
            "Between dynamic programming and deep learning: Jeonggyu Huh, Jaegi Jeon, Hyeng Keun Koo and Byung Hwa "
            "Lim use Pontryagin's maximum principle to steer neural networks to constrained portfolio optima with a "
            "hundred assets, far beyond what a grid can handle."
        ):
            show(3)
        with self.voiceover(
            """Huh and Koo's 2026 follow-up studies parameter uncertainty and reports that its model-free PPO baseline remains far from the targets in that model and protocol. This is a benchmark result, not a universal limit on reinforcement learning."""
        ):
            show(4)
        with self.voiceover(
            "For crowds, a survey by Mathieu Laurière and colleagues maps how agents can learn mean-field equilibria "
            "without a model, the way our damped best-response example did with one."
        ):
            show(5)
        with self.voiceover(
            "Daniel Chee, Noufel Frikha and Libo Li join stopping, exploration and reflected backward equations in a "
            "2026 paper on American options, with rates of convergence."
        ):
            show(6)
        with self.voiceover(
            "And on the Kelly branch, Alexis Akira Toda's 2023 critique of ergodicity economics keeps chapter ten's argument "
            "open. Notice the pattern: almost every edge is a learning method meeting a classical structure, the HJB, the "
            "boundary, the fixed point, and the structure is what makes the learning work. Each of these was checked at its "
            "source; their assumptions and numerical settings differ."
            " Next: the House's sizing module, put together."
        ):
            show(7)
        self.wait(0.4)
        self.clear_scene()
