from __future__ import annotations

from videos.stats.stats3.common import *  # noqa: F403

GROUPS = [
    ("a", ["sum_bern", "hyper_bin", "rare", "first", "sum_geo"]),
    ("b", ["gaps", "sum_exp", "geo_exp"]),
    ("c", ["demoivre", "pois_norm"]),
    ("d", ["neglog", "box_muller", "exp_log", "pareto"]),
    ("e", ["squares", "gamma_chi", "student", "ratio", "t1", "tinf"]),
    ("f", ["order", "gamma_beta"]),
    ("g", ["gp", "mix_p"]),
]


class Tree(VoiceoverScene):
    def construct(self):
        self.card()
        self.tour()
        self.reference()

    def card(self):
        card = chapter_card(14, r"The family tree", r"Sums, limits, transformations and mixtures", lit=(), part=PART)
        with self.voiceover("Chapter fourteen. The family tree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def tour(self):
        ft = FamilyTree().scale(0.92)
        head = label(r"The family tree", font_size=26, color=GREY_B).to_edge(UP, buff=0.2)
        cols = [S.EST, S.LIK, S.ACCENT, S.POST, S.PRIOR, S.TREAT, S.ALT]
        with self.voiceover(
            "Here is the whole tree, dark again, so we can walk it once more. <bookmark mark='a'/> On the discrete "
            "side: Bernoulli trials add up to the binomial; sampling without replacement from a big population is "
            "nearly binomial; the binomial with many rare chances is Poisson; and waiting for successes gives the "
            "geometric and the negative binomial. <bookmark mark='b'/> In continuous time, the gaps of a Poisson "
            "process are exponential, the exponential is the geometric's limit, and sums of exponentials are gamma. "
            "<bookmark mark='c'/> The normal arrives from the binomial, de Moivre's arrow, and from the Poisson with a "
            "large mean. <bookmark mark='d'/> Transformations link the uniform to the exponential and, by Box and "
            "Muller, to the normal, the normal to the log-normal, and the exponential to the Pareto. "
            "<bookmark mark='e'/> The sampling family grows from the normal: chi-squared, a special gamma, then "
            "Student's t, Fisher's F, and at the edges of t, the Cauchy and the normal again. <bookmark mark='f'/> "
            "Order statistics of uniforms are beta, and so is X over X plus Y for independent gammas with a common scale. <bookmark mark='g'/> And mixing "
            "closes two loops: a Poisson with a gamma rate is negative binomial, and a binomial with a beta chance "
            "is beta-binomial. <bookmark mark='h'/> Twenty-four relationships, introduced through derivations and simulation. Some limit proofs await Part 6, and the general theory returns in Part 43. "
            "This is why the same few shapes keep appearing. They aren't independent inventions; they're relatives, "
            "and the operations that relate them, sums, limits, transformations and mixtures, are the operations "
            "nature performs."
        ) as vo:
            self.play(FadeIn(ft), FadeIn(head))
            for (m, keys), col in zip(GROUPS, cols):
                vo.wait_until(m)
                self.play(*ft.light_edges(*keys, color=col), run_time=1.8)
            vo.wait_until("h")
            self.play(*[Indicate(n, color=WHITE, scale_factor=1.08) for n in ft.nodes.values()], run_time=1.5)
        self.clear_scene()

    def reference(self):
        hc = history_card(2008, r"L. Leemis \& J. McQueston, \ ``Univariate distribution relationships''",
                          r"\emph{The American Statistician}: \ 76 distributions and their arrows on one chart", color=S.MUSEUM,
                          width=7.0, font_size=24).move_to([0, 1.4, 0])
        more = label(r"ours has 18 of them: \ the ones this degree uses every day", font_size=28, color=GREY_A)
        more.next_to(hc, DOWN, buff=0.5)
        nxt = label(r"still missing: \ several variables at once \ (Parts 4--5)", font_size=28, color=S.ACCENT)
        nxt.next_to(more, DOWN, buff=0.4)
        intro = label('A map of distribution relationships', font_size=36)
        with self.voiceover(
            "Our tree is a small part of a much bigger one. <bookmark mark='a'/> In 2008 Lawrence Leemis and "
            "Jacquelyn McQueston published a chart of seventy-six distributions and the arrows between them. "
            "<bookmark mark='b'/> Ours has eighteen: the ones this degree will use every day. <bookmark mark='c'/> "
            "And one thing is conspicuously missing: every distribution here describes one variable. Real data come "
            "in rows of many variables at once, and to describe them we need matrices."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(more))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.clear_scene()
