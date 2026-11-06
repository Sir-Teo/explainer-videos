from __future__ import annotations

from videos.stats.stats62.common import *  # noqa: F403


class Identification(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Identification theory: which causal effects can a graph and data determine?", 1,
                            r"Identification theory", r"Beyond the back door", lit=(1995,))
        self.question()
        self.frontdoor()
        self.frontdoor_chart()
        self.bow()
        self.docalculus()
        self.napkin()
        self.id_algorithm()
        self.balke()
        self.limits()

    def question(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part thirty-six's back-door criterion says: if a set of measured variables blocks every "
            "back-door path, adjust for it. <bookmark mark='b'/> When a confounder is unmeasured, no such set may exist. "
            "Is the effect then lost? <bookmark mark='c'/> Not necessarily. The question of identification asks whether the "
            "interventional distribution P of y given do x is a function of the observed distribution, for every model "
            "compatible with the graph. <bookmark mark='d'/> If so, it can be estimated; if not, no amount of data from that "
            "graph will determine it.",
            [(r"\text{back door}", r":", r"P(y \mid do(x)) = \textstyle\sum_z P(y \mid x, z)P(z)", 40),
             (r"\text{hidden confounder}", r":", r"\text{no blocking set}", 40),
             (r"\text{identified}", r":", r"P(y \mid do(x)) = f(P_{\text{obs}}) \ \text{for every compatible model}", 38),
             (r"\text{or not}", r":", r"\text{two models, \ same data, \ different effects}", 40)],
            [r"Part 36", r"the usual failure", r"a functional", r"non-identification"],
            colors=[(2, IDC)])

    def frontdoor(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Judea Pearl's front door, from 1995. A hidden U confounds treatment A and outcome Y, but "
            "the effect of A passes entirely through a mediator M, which U does not touch. <bookmark mark='b'/> The effect "
            "of A on M is unconfounded: compare M across A. <bookmark mark='c'/> The effect of M on Y is confounded only "
            "through A, so adjusting for A identifies it. <bookmark mark='d'/> Chaining the two gives the front-door "
            "formula: the effect is identified although the confounder was never measured.",
            [(r"\text{graph}", r":", r"U \to A \to M \to Y, \ \ U \to Y", 40),
             (r"A \to M", r":", r"\text{unconfounded}", 40),
             (r"M \to Y", r":", r"\text{back door through } A, \ \text{adjust for } A", 40),
             (r"P(y \mid do(a))", r"=", r"\sum_m P(m \mid a)\sum_{a'} P(y \mid m, a')P(a')", 38)],
            [r"Pearl (1995)", r"step one", r"step two", r"the front-door formula"],
            colors=[(3, IDC)])

    def frontdoor_chart(self):
        d = load("frontdoor")
        hdr = [r"estimate", r"value", r"what it assumes"]
        rows = [[r"difference in means", rf"{d['naive']:.2f}", r"no confounding: \ false"],
                [r"back-door adjustment", r"impossible", r"$U$ unmeasured"],
                [r"front-door formula", rf"{d['fd']:.2f}", r"the mediator graph"],
                [r"the truth", rf"{d['truth']:.2f}", r"the simulation"]]
        tab = table_rows([hdr] + rows, font_size=30, col_buff=0.9, row_buff=0.35, colors=[GREY_B, NAIVEC, GREY_A, IDC, GOLDC]).move_to([0, 0.4, 0])
        chk = label(rf"the criterion on the graph: \ front door {'holds' if d['frontdoor_ok'] else 'fails'}; \ the empty set blocks the back door: \ "
                    rf"{'yes' if d['backdoor_empty'] else 'no'}", font_size=24, color=GREY_A).next_to(tab, DOWN, buff=0.6)
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation with {d['n']:,} units. A hidden binary U raises both the chance of "
            f"treatment and the outcome; A acts on Y only through M. <bookmark mark='b'/> The difference in means is "
            f"{say(d['naive'], 2)}, almost three times the truth. <bookmark mark='c'/> No measured set blocks the back door. "
            f"<bookmark mark='d'/> The front-door formula gives {say(d['fd'], 2)}, against a true effect of one. <bookmark "
            f"mark='e'/> statkit's criterion check confirms on the graph what the formula needs."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("e")
            self.play(FadeIn(chk))
        self.clear_scene()

    def docalculus(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Both criteria are special cases of Pearl's do-calculus, three rules for rewriting "
            "expressions with do. <bookmark mark='b'/> Rule one inserts or deletes observations, rule two exchanges an action "
            "for an observation, and rule three inserts or deletes actions, each when a d-separation holds in a modified "
            "graph. <bookmark mark='c'/> An effect is identified if a sequence of rules removes every do. <bookmark "
            "mark='d'/> The rules are complete: Yimin Huang and Marco Valtorta, and Ilya Shpitser and Pearl, proved in 2006 "
            "that if the rules cannot do it, nothing can.",
            [(r"\text{rule 1}", r":", r"\text{insert or delete observations}", 40),
             (r"\text{rule 2}", r":", r"\text{exchange an action and an observation}", 40),
             (r"\text{rule 3}", r":", r"\text{insert or delete actions}", 40),
             (r"\text{complete}", r":", r"\text{no rules} \Rightarrow \text{not identified}", 40)],
            [r"Pearl (1995)", r"by d-separation", r"in modified graphs", r"Huang \& Valtorta; \ Shpitser \& Pearl (2006)"],
            colors=[(3, IDC)])

    def id_algorithm(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The search for a sequence is automated by Jin Tian and Pearl's ID algorithm. <bookmark "
            "mark='b'/> It decomposes the graph into c-components, sets of variables joined by hidden confounding, and "
            "identifies each piece's distribution separately. <bookmark mark='c'/> When it fails, it returns a hedge, a "
            "structure that proves non-identification: two models agreeing on all observed laws but disagreeing on the "
            "effect. <bookmark mark='d'/> So for any graph with hidden variables, the question 'is this effect identified?' "
            "has a mechanical, complete answer, and an estimator follows from the formula it returns.",
            [(r"\text{ID algorithm}", r":", r"\text{Tian \& Pearl (2002); \ Shpitser \& Pearl (2006)}", 38),
             (r"\text{c-components}", r":", r"\text{groups joined by hidden confounders}", 40),
             (r"\text{failure}", r":", r"\text{a hedge: \ a proof of non-identification}", 40),
             (r"\text{so}", r":", r"\text{a complete, \ mechanical answer}", 40)],
            [r"the algorithm", r"divide and conquer", r"a certificate", r"the decision is solved"],
            colors=[(3, IDC)])

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What identification does not solve. <bookmark mark='b'/> It assumes the graph is right; "
            "chapter seven asks whether graphs can be learned. <bookmark mark='c'/> It gives a formula, not an estimator "
            "with good properties: front-door and other identified functionals need Part forty-nine's influence functions "
            "for efficient, doubly robust estimation, worked out by Isabel Fulcher and co-authors in 2020. <bookmark "
            "mark='d'/> And when the answer is 'not identified', the next question is how much can still be said: chapter "
            "two.",
            [(r"\text{assumes}", r":", r"\text{the graph is right}", 40),
             (r"\text{a formula}", r":", r"\text{not yet an efficient estimator}", 40),
             (r"\text{front door, \ efficiently}", r":", r"\text{influence functions; \ doubly robust}", 38),
             (r"\text{not identified}", r":", r"\text{bound it}", 40)],
            [r"chapter 7", r"Part 49", r"Fulcher et al. (2020)", r"chapter 2"],
            colors=[(3, HIDC)])

    def bow(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The smallest unidentified graph is the bow: A causes Y, and a hidden U causes both. "
            "<bookmark mark='b'/> Take two models. In one, A has no effect and U makes A and Y agree; in the other, A has a "
            "strong effect and U does nothing. <bookmark mark='c'/> They can produce exactly the same joint law of A and Y, "
            "so no amount of observational data separates them. <bookmark mark='d'/> Every non-identified graph contains a "
            "structure like this, which is what the ID algorithm's hedge certifies.",
            [(r"\text{bow}", r":", r"A \to Y, \ \ A \leftarrow U \to Y", 40),
             (r"\text{model 1}", r":", r"\text{no effect, \ strong confounding}", 40),
             (r"\text{model 2}", r":", r"\text{strong effect, \ no confounding}", 40),
             (r"\text{same}", r":", r"P(a, y): \ \text{not identified}", 40)],
            [r"the atom of failure", r"observationally equivalent", r"two worlds, \ one dataset", r"the hedge"],
            colors=[(3, NAIVEC)])

    def balke(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> When identification fails, a graph can still bound the effect. <bookmark mark='b'/> With "
            "a binary instrument, treatment and outcome, Alexander Balke and Pearl solved in 1997 a linear program over all "
            "response types consistent with the data: the sharpest possible bounds on the average effect. <bookmark "
            "mark='c'/> With strong compliance the bounds are narrow; with weak compliance they approach Manski's "
            "no-assumption bounds. <bookmark mark='d'/> This is identification's "
            "general form: the set of all effects consistent with the data and the graph, a point when we are lucky.",
            [(r"\text{Balke--Pearl}", r":", r"\text{an LP over response types}", 40),
             (r"\text{output}", r":", r"\text{sharp bounds on the ATE}", 40),
             (r"\text{tight when}", r":", r"\text{compliance is strong}", 40),
             (r"\text{general view}", r":", r"\text{the identified set}", 40)],
            [r"Balke \& Pearl (1997)", r"Part 21's LP", r"Part 37's IV", r"partial identification"],
            colors=[(1, IDC)])

    def napkin(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Some identified effects fit neither criterion. <bookmark mark='b'/> In the napkin graph, "
            "named for being sketched on one, W causes Z, Z causes X, X causes Y, and two hidden variables join W to X and W "
            "to Y. <bookmark mark='c'/> No set blocks the back door from X to Y, and there is no mediator for a front door. "
            "<bookmark mark='d'/> Yet the do-calculus identifies the effect, as a ratio of two adjusted quantities, found by "
            "the ID algorithm mechanically: an answer no one would guess by inspecting the graph.",
            [(r"\text{napkin}", r":", r"W \to Z \to X \to Y; \ \ W \leftrightarrow X, \ W \leftrightarrow Y", 40),
             (r"\text{back door}", r":", r"\text{blocked by nothing}", 40),
             (r"\text{front door}", r":", r"\text{no mediator}", 40),
             (r"\text{yet}", r":", r"P(y \mid do(x)) = \frac{\sum_w P(x, y \mid z, w)P(w)}{\sum_w P(x \mid z, w)P(w)}", 34)],
            [r"Pearl \& Mackenzie (2018)", r"hidden confounding", r"neither criterion", r"identified anyway"],
            colors=[(3, IDC)])
