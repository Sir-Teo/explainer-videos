from __future__ import annotations

import itertools

from videos.philosophy.philosophy13.common import *  # noqa: F403

PR = 0.2
PS = {True: 0.01, False: 0.4}
PW = {(True, True): 0.99, (True, False): 0.9, (False, True): 0.8, (False, False): 0.0}


def joint():
    out = []
    for r, s, w in itertools.product([True, False], repeat=3):
        p = (PR if r else 1 - PR) * (PS[r] if s else 1 - PS[r]) * (PW[(s, r)] if w else 1 - PW[(s, r)])
        out.append((r, s, w, p))
    return out


def tf(b: bool) -> str:
    return r"\mathrm{T}" if b else r"\mathrm{F}"


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Bayesian machines", r"What can a Bayesian actually compute?", lit=(1988,),
                            part=PART)
        with self.voiceover("Chapter thirteen. Bayesian machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.network()
        self.enumerate_()
        self.cost()
        self.omniscience()
        self.brains()

    def network(self):
        hc = history_card(1988, r"Judea Pearl", r"\textit{Probabilistic Reasoning in Intelligent Systems}",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        pos = {"R": [-4.2, 0.4, 0], "S": [-1.4, 0.4, 0], "W": [-2.8, -1.8, 0]}
        names = {"R": r"rain", "S": r"sprinkler", "W": r"wet grass"}
        nodes = {k: VGroup(Circle(radius=0.62, color=CRED, fill_color="#16222F", fill_opacity=1, stroke_width=3),
                           label(names[k], font_size=20)).move_to(v) for k, v in pos.items()}
        edges = VGroup(Arrow(pos["R"], pos["S"], buff=0.65, color=GREY_B, stroke_width=3),
                       Arrow(pos["R"], pos["W"], buff=0.65, color=GREY_B, stroke_width=3),
                       Arrow(pos["S"], pos["W"], buff=0.65, color=GREY_B, stroke_width=3))
        cpts = stack([
            (r"$P(\text{rain}) = 0.2$", WHITE),
            (r"$P(\text{sprinkler} \mid \text{rain}) = 0.01$, \ \ $P(\text{sprinkler} \mid \lnot\text{rain}) = 0.4$",
             WHITE),
            (r"$P(\text{wet} \mid s, r)$: \ $0.99,\ 0.9,\ 0.8,\ 0$", WHITE),
        ], font_size=21, aligned_edge=LEFT, width=6.0).move_to([3.4, 0.9, 0])
        fac = MathTex(r"P(R, S, W) = P(R)\,P(S \mid R)\,P(W \mid S, R)", font_size=30, color=CRED).move_to(
            [3.4, -0.7, 0])
        note = label(r"each variable depends only on its parents", font_size=21, color=GREY_A).next_to(fac, DOWN,
                                                                                                    buff=0.25)
        with self.voiceover(
            "How does a machine hold a credence function? <bookmark mark='a'/>Judea Pearl's answer, in 1988, was the "
            "Bayesian network. Rain makes the sprinkler less likely to be on, and either one can wet the grass. "
            "<bookmark mark='b'/>Each variable gets a small table, giving its chances conditional on its parents. "
            "<bookmark mark='c'/>The joint credence over all the variables is the product of those tables. "
            "Independence does the work: each variable depends only on its parents."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for n in nodes.values()])
            self.play(*[GrowArrow(e) for e in edges])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cpts], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(fac), FadeIn(note))
        self.clear_scene()

    def enumerate_(self):
        d = load("bayesnet")
        J = joint()
        head = label(r"The grass is wet. \ Did it rain?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{rain}", r"\text{sprinkler}", r"\text{wet}", r"P"]
        rows = [[tf(r), tf(s), tf(w), f"{p:.4f}"] for r, s, w, p in J]
        grid = ValueGrid(hd, rows, col_w=[1.4, 1.8, 1.2, 1.6], cell_h=0.44, font_size=22).move_to([-3.2, -0.5, 0])
        wet = [i for i, (_, _, w, _) in enumerate(J) if w]
        rain_wet = [i for i, (r, _, w, _) in enumerate(J) if w and r]
        boxes_w = VGroup(*[SurroundingRectangle(grid.row(i), color=BET, buff=0.03) for i in wet])
        boxes_r = VGroup(*[SurroundingRectangle(grid.row(i), color=OK, buff=0.06, stroke_width=4) for i in rain_wet])
        pw = sum(J[i][3] for i in wet)
        prw = sum(J[i][3] for i in rain_wet)
        steps = VGroup(
            MathTex(rf"P(\text{{wet}}) = {pw:.4f}", font_size=30, color=BET),
            MathTex(rf"P(\text{{rain}} \land \text{{wet}}) = {prw:.4f}", font_size=30, color=OK),
            MathTex(rf"P(\text{{rain}} \mid \text{{wet}}) = \frac{{{prw:.4f}}}{{{pw:.4f}}} = "
                    rf"{d['p_rain_given_wet']:.3f}", font_size=32, color=CRED),
            label(r"up from 0.2: \ the wet grass is evidence of rain", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.3, 0])
        assert abs(prw / pw - d["p_rain_given_wet"]) < 1e-9
        with self.voiceover(
            "Now the grass is wet. Did it rain? <bookmark mark='a'/>Exact inference by enumeration: the Reasoner "
            "multiplies out the joint credence for all eight combinations. <bookmark mark='b'/>Keep the rows where "
            "the grass is wet, and add them: point four four eight. <bookmark mark='c'/>Among those, keep the rows "
            "with rain: point one six. <bookmark mark='d'/>Divide. The credence in rain, given wet grass, is point "
            "three five eight, up from point two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(LaggedStart(*[FadeIn(grid.row(i)) for i in range(8)], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(Create(boxes_w), FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(Create(boxes_r), FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(steps[3]))
        self.clear_scene()

    def cost(self):
        d = load("bayesnet")
        head = label(r"The price of exactness", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sizes = d["table_sizes"]
        bars = bar_row([s for _, s in sizes], [rf"{n} variables" for n, _ in sizes], [CRED] * len(sizes), width=3.4,
                       font_size=21, log=True, fmt=lambda v: f"{v:,.0f}" if v < 1e7 else
                       rf"{v / 10 ** int(np.log10(v)):.1f} \times 10^{{{int(np.log10(v))}}}").move_to([-3.4, 0.3, 0])
        bt = label(r"entries in the full joint table \ (log scale)", font_size=21, color=GREY_B).next_to(bars, UP,
                                                                                                    buff=0.25)
        rows = stack([
            (r"a network stores far less: \ one small table per variable", OK),
            (r"but exact inference is NP-hard \ (Cooper, \ 1990)", BAD),
            (r"so is approximating it to a fixed accuracy \ (Dagum and Luby, \ 1993)", BAD),
            (r"and checking coherence: \ chapter 2's LP has one column per world, \ $2^n$", INC),
            (r"in practice: \ sampling \ (MCMC), \ variational methods, \ structure", GREY_A),
        ], font_size=22, aligned_edge=LEFT, width=5.9).move_to([3.7, -0.4, 0])
        with self.voiceover(
            "That was eight rows. <bookmark mark='a'/>With n yes-or-no variables, the full joint table has two to "
            "the n entries: a thousand for ten variables, a million for twenty, a billion for thirty, and over a "
            "thousand trillion for fifty. <bookmark mark='b'/>A network stores far less, one small table per "
            "variable. <bookmark mark='c'/>But Gregory Cooper proved in 1990 that exact inference in Bayesian "
            "networks is NP-hard. <bookmark mark='d'/>Paul Dagum and Michael Luby then proved that even "
            "approximating it to a fixed accuracy is NP-hard. <bookmark mark='e'/>Coherence itself is no easier: "
            "the Dutch book program of chapter two has one column for each possible world, two to the n of them. "
            "<bookmark mark='f'/>Real systems approximate: they sample, with Markov chain Monte Carlo; they fit "
            "simpler distributions, with variational methods; and they exploit structure."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.3), run_time=3)
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def omniscience(self):
        head = label(r"Logical omniscience", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"probabilism: \ every logical truth gets credence 1", WHITE),
            (r"`the $10^{100}$th digit of $\pi$ is 7': \ credence 1 or 0, \ before anyone computes it", BAD),
            (r"no real reasoner can comply: \ Part 7's limits apply to minds too", GREY_A),
            (r"repairs: \ Hacking \ (1967), \ Garber \ (1983): \ treat logical facts as learnable", OK),
            (r"logical induction \ (Garrabrant et al., \ 2016): \ credences in mathematics that are never "
             r"exploitable by efficient traders", OK),
        ], font_size=24, buff=0.35, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "There is a deeper idealization. <bookmark mark='a'/>Probabilism gives every logical truth credence "
            "one. <bookmark mark='b'/>So the proposition that the googolth digit of pi is seven must get credence one "
            "or zero, before anyone has computed it. <bookmark mark='c'/>No real reasoner can comply, and Part 7's "
            "limits on proof apply to minds as much as to machines. <bookmark mark='d'/>Ian Hacking and Daniel Garber "
            "proposed treating logical facts as things one can learn. <bookmark mark='e'/>And in 2016 Scott "
            "Garrabrant and colleagues defined logical induction: a way of assigning credences to mathematical "
            "claims that no efficient trader can exploit, a Dutch book criterion for a bounded reasoner."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brains(self):
        head = label(r"Bayesian brains?", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"vision and motor control: \ near-optimal cue combination \ (Ernst and Banks, \ 2002)", OK),
            (r"predictive processing: \ perception as inference", WHITE),
            (r"the critics: \ any behaviour fits \textit{some} prior \ (Jones and Love, \ 2011)", BAD),
            (r"resource rationality: \ optimal given the cost of thinking \ (Lieder and Griffiths, \ 2020)", GOAL),
            (r"and in base-rate problems, \ people are far from Bayesian \ (chapter 5)", GREY_A),
        ], font_size=24, buff=0.35, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Are we Bayesian machines? <bookmark mark='a'/>In some ways, strikingly so. When we combine sight and "
            "touch to judge a size, Marc Ernst and Martin Banks found that we weight each cue almost exactly as "
            "Bayes would. <bookmark mark='b'/>Predictive processing theories treat all of perception as inference. "
            "<bookmark mark='c'/>Critics such as Matt Jones and Bradley Love reply that with a free choice of prior "
            "and of utilities, any behaviour can be described as Bayesian. <bookmark mark='d'/>Resource rationality "
            "takes the middle path: minds are optimal given the cost of computation, which is exactly what this "
            "chapter says a Bayesian must pay. <bookmark mark='e'/>And in base-rate problems like chapter five's, "
            "people are far from Bayes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
