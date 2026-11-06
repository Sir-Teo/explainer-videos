from __future__ import annotations

import math
import random

from videos.philosophy.philosophy13.common import *  # noqa: F403

OPT, PES, DOG = "#F2A65A", "#6FB7FF", "#F28EC2"
XS = np.linspace(0.0015, 0.9985, 240)


def beta_shape(a: float, b: float, upper: float = 1.0) -> np.ndarray:
    """The Beta(a, b) density on XS (zero above ``upper``), scaled to peak 1."""
    lg = (a - 1) * np.log(XS) + (b - 1) * np.log(1 - XS)
    lg[XS > upper] = -np.inf
    lg -= lg[np.isfinite(lg)].max()
    return np.exp(lg)


def beta_mean(a: float, b: float, upper: float = 1.0) -> float:
    y = beta_shape(a, b, upper)
    return float((XS * y).sum() / y.sum())


class Priors(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Where priors come from", r"Is there one rational place to start?",
                            lit=(1957, 1921), part=PART)
        with self.voiceover("Chapter six. Where priors come from."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.washing()
        self.camps()
        self.maxent()
        self.trouble()

    def problem(self):
        head = label(r"The problem of the priors", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"conditionalization says how to \textit{move}", WHITE),
            (r"not where to \textit{start}", BAD),
            (r"$P_{\text{new}}(H) = P(H \mid E)$ \ inherits everything from the prior $P$", GREY_A),
            (r"is any coherent prior rational? \ or does reason fix one?", GOAL),
        ], font_size=28, buff=0.35).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "We now have rules for the shape of credences at a time, and for how they move. <bookmark mark='a'/>But "
            "conditionalization says only how to move, <bookmark mark='b'/>not where to start. "
            "<bookmark mark='c'/>Every later credence inherits its character from the prior you began with. "
            "<bookmark mark='d'/>So is any coherent prior rational? Or does reason fix a single one? This is the "
            "problem of the priors."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def washing(self):
        head = label(r"Three priors about a coin's bias, \ one stream of flips", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        rnd = random.Random(1763)
        flips = [1 if rnd.random() < 0.6 else 0 for _ in range(1000)]
        heads = np.concatenate([[0], np.cumsum(flips)])
        ax = Axes(x_range=[0, 1, 0.1], y_range=[0, 1.1, 0.5], x_length=7.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([-1.6, -0.6, 0])
        xnums = VGroup(*[MathTex(f"{v:g}", font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.12)
                         for v in (0, 0.5, 1)])
        xl = label(r"the coin's bias, \ $\theta$", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        truth = DashedLine(ax.c2p(0.6, 0), ax.c2p(0.6, 1.1), color=OK, stroke_width=2)
        tl = label(r"truth: \ 0.6", font_size=20, color=OK).next_to(truth, UP, buff=0.08)
        n = ValueTracker(0)

        def counts():
            k = int(round(n.get_value()))
            return k, int(heads[k])
        priors = [("optimist", OPT, 8, 2, 1.0), ("pessimist", PES, 2, 8, 1.0), ("dogmatist", DOG, 1, 1, 0.5)]

        def curve(a, b, up, col):
            def f():
                k, h = counts()
                y = beta_shape(a + h, b + k - h, up)
                return ax.plot_line_graph(XS, y, line_color=col, add_vertex_dots=False, stroke_width=3)
            return always_redraw(f)
        curves = VGroup(*[curve(a, b, up, col) for _, col, a, b, up in priors])
        legend = VGroup()
        for name, col, a, b, up in priors:
            desc = {"optimist": r"Beta$(8, 2)$", "pessimist": r"Beta$(2, 8)$",
                    "dogmatist": r"uniform on $[0, \tfrac12]$: \ zero above"}[name]
            legend.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=4),
                              label(rf"{name}: \ {desc}", font_size=20, color=col)).arrange(RIGHT, buff=0.15))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 1.6, 0])

        def means():
            k, h = counts()
            g = VGroup()
            for name, col, a, b, up in priors:
                g.add(VGroup(label(rf"{name}'s mean:", font_size=20, color=col),
                             DecimalNumber(beta_mean(a + h, b + k - h, up), num_decimal_places=3, font_size=24,
                                           color=col)).arrange(RIGHT, buff=0.15))
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, -0.3, 0])
        mean_g = always_redraw(means)
        flips_l = always_redraw(lambda: VGroup(label(r"flips seen:", font_size=22),
                                               Integer(counts()[0], font_size=28, color=BET)).arrange(
            RIGHT, buff=0.15).move_to([4.6, -1.6, 0]))
        note = label(r"curves scaled to the same height", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        foot = stack([(r"washing out: \ opinions merge \ (Blackwell and Dubins, \ 1962)", GOAL),
                      (r"except where a prior says zero: \ Cromwell's rule \ (Lindley)", DOG)], font_size=22).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "The subjectivist's first reply is that it matters less than it seems. <bookmark mark='a'/>Three people "
            "are unsure of a coin's bias. The optimist's prior leans towards heads; the pessimist's towards tails. "
            "The third, the dogmatist, is sure the bias is at most one half, and gives zero to everything above. "
            "<bookmark mark='b'/>The coin's true bias is point six. <bookmark mark='c'/>All three watch the same "
            "flips and conditionalize. Ten flips. Fifty. <bookmark mark='d'/>Two hundred. A thousand. The optimist "
            "and the pessimist converge on the truth, whatever they started with. The evidence washes out the "
            "prior; David Blackwell and Lester Dubins proved that opinions merge in this way under very general "
            "conditions. <bookmark mark='e'/>But the dogmatist piles up at one half, against the wall of her own "
            "zero, and no evidence will ever move her past it. Dennis Lindley called the lesson Cromwell's rule: never "
            "give zero to anything that could be true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xnums), FadeIn(xl), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(legend), FadeIn(curves), FadeIn(mean_g), FadeIn(flips_l))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(tl))
            vo.wait_until("c")
            self.play(n.animate.set_value(10), run_time=2, rate_func=linear)
            self.play(n.animate.set_value(50), run_time=2, rate_func=linear)
            vo.wait_until("d")
            self.play(n.animate.set_value(200), run_time=2.5, rate_func=linear)
            self.play(n.animate.set_value(1000), run_time=3, rate_func=linear)
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]), Indicate(legend[2], color=DOG))
        self.clear_scene()

    def camps(self):
        head = label(r"Subjective and objective Bayesians", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        cols = []
        for title, col, items in (
                (r"subjective", OPT, [r"de Finetti, \ Savage", r"any coherent prior is permitted",
                                      r"rationality constrains change, \ not content",
                                      r"worry: \ a prior can be crazy yet coherent"]),
                (r"objective", PES, [r"Jeffreys, \ Jaynes, \ J.\ Williamson", r"evidence fixes a unique prior",
                                     r"symmetry, \ calibration to known chances, \ maximum entropy",
                                     r"worry: \ which symmetry? \ (next chapter)"])):
            g = VGroup(label(title, font_size=28, color=col))
            for i, t in enumerate(items):
                g.add(label(t, font_size=22, color=GREY_A if i == 0 else (BAD if i == 3 else WHITE)))
            g.arrange(DOWN, buff=0.25)
            cols.append(g)
        cols = VGroup(*cols).arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(head, DOWN, buff=0.6)
        mid = label(r"between them: \ permissivism vs.\ uniqueness \ (White, \ 2005)", font_size=24,
                    color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two camps. <bookmark mark='a'/>Subjective Bayesians, following de Finetti and Savage, permit any "
            "coherent prior. Rationality constrains how credences change, not what they start as. The worry: a prior "
            "can be coherent and crazy. <bookmark mark='b'/>Objective Bayesians, from Harold Jeffreys to Edwin Jaynes "
            "and Jon Williamson, hold that the evidence fixes a unique rational prior: respect symmetries, match known "
            "chances, and otherwise be as noncommittal as possible. <bookmark mark='c'/>The modern form of the "
            "dispute is permissivism against uniqueness: given a body of evidence, is there exactly one rational "
            "credence, as Roger White argues, or more than one?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("ab", cols):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(m) for m in c], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(mid))
        self.clear_scene()

    def maxent(self):
        d = load("maxent")
        p = d["p"]
        hc = history_card(1957, r"Edwin Jaynes", r"`Information Theory and Statistical Mechanics'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        ent = MathTex(r"H(p) = -\sum_k p_k \log p_k", font_size=34).move_to([3.4, 2.6, 0])
        q = label(r"a die averages 4.5: \ what should you believe about the next roll?", font_size=24,
                  color=BET).next_to(hc, DOWN, buff=0.35).set_x(0)
        t = ValueTracker(0.0)
        base = np.array([-5.6, -2.6, 0])

        def probs():
            return [1 / 6 + (x - 1 / 6) * t.get_value() for x in p]

        def bars():
            g = VGroup()
            for i, v in enumerate(probs()):
                h = 9.0 * v
                g.add(Rectangle(width=0.62, height=h, stroke_width=0, fill_color=CRED, fill_opacity=0.85).move_to(
                    base + np.array([i * 0.85, h / 2, 0])))
            return g
        bar_g = always_redraw(bars)
        faces = VGroup(*[MathTex(str(k + 1), font_size=24).move_to(base + np.array([k * 0.85, -0.25, 0]))
                         for k in range(6)])
        vals = always_redraw(lambda: VGroup(*[DecimalNumber(v, num_decimal_places=3, font_size=18, color=CRED)
                                              .next_to(bar_g[i], UP, buff=0.08) for i, v in enumerate(probs())]))
        H_me = -sum(x * math.log(x) for x in p)
        sol = VGroup(MathTex(r"p_k = \frac{e^{\lambda k}}{Z}", font_size=36, color=CRED),
                     label(r"$\lambda$ chosen so the mean is 4.5", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.15).move_to([3.4, 0.6, 0])
        comp = VGroup(
            label(rf"maximum entropy: \ $H = {H_me:.2f}$", font_size=22, color=CRED),
            label(rf"half on 4, \ half on 5: \ mean 4.5 too, \ $H = {math.log(2):.2f}$", font_size=22, color=GREY_A),
            label(r"it claims to know far more than you do", font_size=22, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, -1.1, 0])
        foot = label(r"MaxEnt: \ the least committal distribution consistent with what you know", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Edwin Jaynes made the objective view precise. <bookmark mark='a'/>His example: a die has been rolled "
            "many times, and the average is four and a half, not three and a half. That is all you know. What should "
            "you believe about the next roll? <bookmark mark='b'/>Measure how noncommittal a distribution is by its "
            "Shannon entropy. Jaynes's principle: among the distributions that fit what you know, choose the one with "
            "the greatest entropy. <bookmark mark='c'/>Before the constraint, that is the uniform die. "
            "<bookmark mark='d'/>With the mean fixed at four and a half, the Reasoner solves for it: an exponential "
            "family, each face's probability proportional to e to the lambda k. Six gets point three five, one gets "
            "point zero five. <bookmark mark='e'/>Compare a distribution that also averages four and a half, half "
            "on four and half on five. Its entropy is far lower: it claims to know much more than you do. "
            "<bookmark mark='f'/>Maximum entropy is the least committal belief consistent with your evidence. Jaynes "
            "derived statistical mechanics from it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Write(ent))
            vo.wait_until("c")
            self.play(FadeIn(bar_g), FadeIn(faces), FadeIn(vals))
            vo.wait_until("d")
            self.play(t.animate.set_value(1.0), FadeIn(sol), run_time=3)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(c) for c in comp], lag_ratio=0.4))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def trouble(self):
        head = label(r"Where maximum entropy struggles, \ and where it works", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        bad = stack([(r"it depends on how you carve the possibilities", BAD),
                     (r"MaxEnt updating can disagree with conditionalization", BAD),
                     (r"Judy Benjamin \ (van Fraassen, \ 1981): \ learning a conditional", GREY_A)],
                    font_size=22, aligned_edge=LEFT).move_to([-3.4, 0.6, 0])
        good = stack([(r"statistical mechanics: \ Gibbs distributions", OK),
                      (r"logistic regression \ = \ a maximum-entropy classifier", OK),
                      (r"ridge and lasso \ = \ Gaussian and Laplace priors", OK),
                      (r"Jeffreys and reference priors in statistics", GREY_A)],
                     font_size=22, aligned_edge=LEFT).move_to([3.4, 0.6, 0]).align_to(bad, UP)
        foot = label(r"the first worry is the deepest: \ which carving? \ That is Bertrand's paradox.", font_size=25,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Maximum entropy has troubles. <bookmark mark='a'/>Its answer depends on how you carve up the "
            "possibilities: uniform over one description is not uniform over another. <bookmark mark='b'/>Updating "
            "by maximum entropy can disagree with conditionalization, as Abner Shimony and Teddy Seidenfeld showed. "
            "<bookmark mark='c'/>And Bas van Fraassen's Judy Benjamin problem, about learning a conditional "
            "probability, gives answers that strike many as wrong. <bookmark mark='d'/>Yet it works widely in "
            "practice. Statistical mechanics; <bookmark mark='e'/>the logistic regression classifier, which is a "
            "maximum entropy model; <bookmark mark='f'/>regularized regression, where ridge and lasso are Gaussian "
            "and Laplace priors in disguise; <bookmark mark='g'/>and the default priors of Jeffreys and Bernardo in "
            "statistics. <bookmark mark='h'/>The first worry is the deepest. Which way of carving the possibilities "
            "is the right one? That question has a famous answer: none."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", bad):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, r in zip("defg", good):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("h")
            self.play(FadeIn(foot))
        self.clear_scene()
