from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


def tick(ok: bool) -> str:
    return r"$\checkmark$" if ok else r"$\times$"


class Calculus(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The do-calculus", r"Which causal questions can data answer?", lit=(1995, 2006),
                            part=PART)
        with self.voiceover("Chapter eight. The do-calculus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.derive()
        self.complete()
        self.bad_controls()

    def rules(self):
        hc = history_card(1995, r"Judea Pearl", r"`Causal Diagrams for Empirical Research'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        note = label(r"$G_{\overline{X}}$: \ delete arrows into $X$; \ \ $G_{\underline{Z}}$: \ delete arrows out of $Z$",
                     font_size=21, color=GREY_A).next_to(hc, DOWN, buff=0.35).set_x(0)
        r1 = MathTex(r"\textbf{1.}\quad P(y \mid do(x), z, w) = P(y \mid do(x), w)", r"\quad\text{if } (Y \perp Z \mid X, W)"
                     r"_{G_{\overline{X}}}", font_size=30)
        r2 = MathTex(r"\textbf{2.}\quad P(y \mid do(x), do(z), w) = P(y \mid do(x), z, w)",
                     r"\quad\text{if } (Y \perp Z \mid X, W)_{G_{\overline{X}\,\underline{Z}}}", font_size=30)
        r3 = MathTex(r"\textbf{3.}\quad P(y \mid do(x), do(z), w) = P(y \mid do(x), w)",
                     r"\quad\text{if } (Y \perp Z \mid X, W)_{G_{\overline{X}\,\overline{Z(W)}}}", font_size=30)
        rules = VGroup(r1, r2, r3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(note, DOWN, buff=0.45)
        for r, c in zip(rules, (EFFECT, DOC, CAUSE)):
            r[0].set_color(c)
            r[1].set_color(GREY_A)
        if rules.width > 13.2:
            rules.width = 13.2
        rules.set_x(0)
        gloss = stack([(r"1: \ ignore an observation that tells us nothing more", EFFECT),
                       (r"2: \ an action is as good as an observation, \ when no back door is open", DOC),
                       (r"3: \ ignore an action that cannot reach $Y$", CAUSE)], font_size=21).next_to(
            rules, DOWN, buff=0.45)
        with self.voiceover(
            "In 1995 Pearl gave a calculus for the do-operator: three rules that turn expressions containing do into "
            "other expressions, each licensed by a d-separation in a surgically altered graph. "
            "<bookmark mark='a'/>Two surgeries are needed: delete the arrows into a variable, written with a bar "
            "above, or delete the arrows out of it, written with a bar below. <bookmark mark='b'/>Rule one: an "
            "observation may be ignored if, in the graph where X has been set, it is independent of Y given the "
            "rest. <bookmark mark='c'/>Rule two: an action may be exchanged for an observation, when no back-door "
            "path connects it to Y. <bookmark mark='d'/>Rule three: an action may be deleted, when it has no way to "
            "reach Y. <bookmark mark='e'/>In words: ignore what tells you nothing; treat doing as seeing when no "
            "back door is open; and ignore actions that cannot matter."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(note))
            for mk, r in zip("bcd", rules):
                vo.wait_until(mk)
                self.play(Write(r))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in gloss], lag_ratio=0.3))
        self.clear_scene()

    def derive(self):
        d = load("calculus")["derivation"]
        head = label(r"The front door, \ derived", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g = CausalGraph({"S": [-5.6, 1.2, 0], "T": [-4.2, 1.2, 0], "C": [-2.8, 1.2, 0], "U": [-4.2, 2.5, 0]},
                        [("S", "T"), ("T", "C"), ("U", "S"), ("U", "C")], hidden=("U",), radius=0.32, font_size=18,
                        colors={"S": CAUSE, "C": EFFECT}, dashed=(("U", "S"), ("U", "C")))
        eqs = [
            (r"P(c \mid do(s)) = \sum_t P(c \mid do(s), t)\, P(t \mid do(s))", r"\text{probability}", None),
            (r"P(t \mid do(s)) = P(t \mid s)", r"\text{rule 2}", d["steps"][0]["ok"]),
            (r"P(c \mid do(s), t) = P(c \mid do(s), do(t))", r"\text{rule 2}", d["steps"][1]["ok"]),
            (r"P(c \mid do(s), do(t)) = P(c \mid do(t))", r"\text{rule 3}", d["steps"][2]["ok"]),
            (r"P(c \mid do(t)) = \sum_{s'} P(c \mid t, s')\, P(s')", r"\text{back door via } S", d["steps"][3]["ok"]),
        ]
        rows = VGroup()
        for e, why, ok in eqs:
            m = MathTex(e, font_size=26, color=WHITE)
            w = MathTex(why, font_size=22, color=GREY_A)
            t = label(tick(ok) if ok is not None else "", font_size=24, color=OK if ok else BAD)
            rows.add(VGroup(m, w, t))
        y = 1.9
        for r in rows:
            r[0].move_to([-1.9 + r[0].width / 2, y, 0])
            r[1].move_to([5.0, y, 0])
            r[2].move_to([6.5, y, 0])
            y -= 0.78
        res = MathTex(r"\Rightarrow\; P(c \mid do(s)) = \sum_t P(t \mid s) \sum_{s'} P(c \mid t, s')\, P(s')",
                      font_size=32, color=GOAL).move_to([0.6, y - 0.15, 0])
        bow = stack([(r"the bow arc \ ($X \to Y$, \ hidden $U$ into both): \ rule 2 " + tick(d["bow"]["rule 2 (do(x) to x)"])
                      + r", \ rule 3 " + tick(d["bow"]["rule 3 (delete do(x))"]) + r": \ \ no first step exists", BAD),
                     (r"every step's side condition is a d-separation, \ checked by the Reasoner", GREY_A)],
                    font_size=21).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the front-door formula, derived in the calculus. <bookmark mark='a'/>First, plain probability: "
            "sum over the values of tar. <bookmark mark='b'/>Smoking's effect on tar: by rule two, doing equals "
            "seeing, because once smoking's outgoing arrow is cut, nothing connects smoking to tar. "
            "<bookmark mark='c'/>Next, given smoking was set, observing tar is as good as setting it, by rule two "
            "again. <bookmark mark='d'/>Then the action on smoking can be deleted, by rule three: once tar is set, "
            "smoking cannot reach cancer. <bookmark mark='e'/>Tar's effect on cancer is a back-door adjustment, with "
            "smoking blocking the path through the gene. <bookmark mark='f'/>Assemble the pieces and the do has "
            "disappeared: an expression in observational probabilities only. <bookmark mark='g'/>In the bow arc, by "
            "contrast, neither rule applies to the first step, and no derivation can begin."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(Write(r[0]), FadeIn(r[1]), FadeIn(r[2]))
            vo.wait_until("f")
            self.play(Write(res))
            vo.wait_until("g")
            self.play(FadeIn(bow))
        self.clear_scene()

    def complete(self):
        head = label(r"Completeness, \ and what it buys", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Tian and Pearl \ (2002)", r"c-components: \ split the variables by hidden confounding; \ identify "
                                        r"each piece", EFFECT),
            (r"Shpitser and Pearl \ (2006)", r"the ID algorithm: \ returns a formula whenever one exists, \ and a "
                                             r"`hedge' proving none does otherwise", OK),
            (r"Huang and Valtorta \ (2006)", r"independently: \ the three rules are complete for identification", OK),
            (r"Bareinboim and Pearl \ (2012--16)", r"transportability: \ when a trial in one population tells us "
                                                   r"about another; \ selection bias as a graph", CAUSE),
            (r"the philosophical point", r"every identification is relative to a graph: \ the missing arrows are "
                                         r"the assumptions, \ and they are visible", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.0, x_text=-1.9)
        with self.voiceover(
            "Is the calculus enough? <bookmark mark='a'/>Jin Tian and Pearl showed how to split a graph into "
            "pieces linked by hidden confounding, and identify each piece. <bookmark mark='b'/>Ilya Shpitser and "
            "Pearl gave an algorithm that returns a formula for the causal effect whenever one exists; when none "
            "does, it returns a structure called a hedge that proves it. <bookmark mark='c'/>Yimin Huang and Marco "
            "Valtorta proved, independently in the same year, that the three rules are complete: any identifiable "
            "effect can be derived with them. <bookmark mark='d'/>Elias Bareinboim and Pearl extended the "
            "machinery to transportability: when does a trial in one population tell us about another? "
            "<bookmark mark='e'/>The philosophical point is that every identification is relative to a graph. The "
            "absent arrows are the assumptions, and the graph puts them where everyone can see and dispute them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bad_controls(self):
        d = load("calculus")["mbias"]
        head = label(r"Do not adjust for everything: \ M-bias", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g = CausalGraph({"U1": [-5.2, 1.6, 0], "U2": [-2.0, 1.6, 0], "M": [-3.6, 0.5, 0], "X": [-5.2, -0.8, 0],
                         "Y": [-2.0, -0.8, 0]},
                        [("U1", "X"), ("U1", "M"), ("U2", "M"), ("U2", "Y"), ("X", "Y")], hidden=("U1", "U2"),
                        radius=0.42, font_size=18, colors={"X": CAUSE, "Y": EFFECT, "M": WHITE})
        side = stack([(r"$M$ comes before $X$, \ and correlates with both", WHITE),
                      (r"unadjusted: \ " + f"{d['naive']:.2f}" + r" \ = truth " + f"{d['truth']:.2f}", OK),
                      (r"adjusted for $M$: \ " + f"{d['adjusted_M']:.2f}" + r": \ conditioning on a collider opens "
                       r"$X \leftarrow U_1 \to M \leftarrow U_2 \to Y$", BAD),
                      (r"back-door criterion: \ $\varnothing$ " + tick(d["criterion_empty"]) + r", \ $\{M\}$ " +
                       tick(d["criterion_M"]), GREY_A),
                      (r"other bad controls: \ mediators, \ descendants of the outcome \ (Cinelli, \ Forney and Pearl, "
                       r"\ 2022)", GOAL)], font_size=21, aligned_edge=LEFT, width=7.0).move_to([3.0, -0.4, 0])
        with self.voiceover(
            "One practical lesson cuts against a common habit: adjust for every variable you have. "
            "<bookmark mark='a'/>Here M is measured before the treatment, and correlates with both treatment and "
            "outcome: the textbook picture of a confounder. <bookmark mark='b'/>But M is a collider of two hidden "
            "causes. Without adjustment, the comparison is already unbiased: point three, the true effect. "
            "<bookmark mark='c'/>Adjusting for M opens the path through both hidden causes, and the estimate falls "
            "to point two two. <bookmark mark='d'/>The back-door criterion sees it at once: the empty set "
            "qualifies, and M does not. <bookmark mark='e'/>Mediators and descendants of the outcome are other "
            "bad controls. Which variables to adjust for is a causal question, not a statistical one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for mk, r in zip("abcde", side):
                vo.wait_until(mk)
                if mk == "c":
                    self.play(Indicate(g.node["M"], color=BAD), FadeIn(r))
                else:
                    self.play(FadeIn(r))
        self.clear_scene()
