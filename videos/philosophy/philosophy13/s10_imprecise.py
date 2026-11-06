from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403

RED, BLK = "#F25C5C", "#9AA4B2"


def urn(center, known: bool) -> VGroup:
    box = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.25, color=WHITE, stroke_width=3).move_to(center)
    balls = VGroup()
    for i in range(36):
        r, c = divmod(i, 6)
        col = (RED if i % 2 == 0 else BLK) if known else GREY_D
        balls.add(Circle(radius=0.16, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
            np.array(center) + np.array([-1.0 + c * 0.4, 1.0 - r * 0.4, 0])))
    q = VGroup() if known else MathTex(r"?", font_size=80, color=BET).move_to(center)
    return VGroup(box, balls, q)


class Imprecise(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Imprecise credences", r"What if no single number fits your evidence?", lit=(1921,),
                            part=PART)
        with self.voiceover("Chapter nine. Imprecise credences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ellsberg()
        self.credal()
        self.dilation()
        self.elga()
        self.uses()

    def ellsberg(self):
        head = label(r"Ellsberg's urns \ (1961)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        u1 = urn([-3.4, 0.6, 0], True)
        u2 = urn([3.4, 0.6, 0], False)
        l1 = label(r"50 red, \ 50 black", font_size=22).next_to(u1, DOWN, buff=0.2)
        l2 = label(r"100 balls, \ red and black, \ mix unknown", font_size=22).next_to(u2, DOWN, buff=0.2)
        rows = stack([(r"win \$100 if you draw red: \ most people choose the known urn", WHITE),
                       (r"win \$100 if you draw black: \ \textit{again} the known urn", WHITE),
                       (r"no single credence for red in urn 2 explains both choices", BAD)], font_size=23).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "In 1961 Daniel Ellsberg, later famous for the Pentagon Papers, published an experiment. "
            "<bookmark mark='a'/>One urn has fifty red balls and fifty black. <bookmark mark='b'/>Another has a "
            "hundred balls, red and black, in proportions you don't know. <bookmark mark='c'/>You win a hundred "
            "dollars if you draw red. Which urn? Most people choose the known one. <bookmark mark='d'/>Now you win "
            "if you draw black. Most people choose the known urn again. <bookmark mark='e'/>But if your credence in "
            "red from the unknown urn were below a half, you should take it when betting on black; if above, when "
            "betting on red. No single number explains both choices. People are averse to ambiguity, and many "
            "philosophers think they are right to be."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(u1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(u2), FadeIn(l2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def credal(self):
        head = label(r"Credal sets", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"represent a state of belief by a \textit{set} of probability functions, \ $\mathcal{P}$", WHITE),
            (r"$P_*(A) = \min_{P \in \mathcal{P}} P(A)$, \qquad $P^*(A) = \max_{P \in \mathcal{P}} P(A)$", CRED),
            (r"the known urn: \ $\{\tfrac12\}$; \ \ the unknown urn: \ $[0, 1]$", WHITE),
            (r"to learn $E$: \ conditionalize every member", WHITE),
            (r"Keynes \ (1921); \ Levi \ (1974); \ Walley \ (1991); \ Joyce \ (2010)", GREY_A),
        ], font_size=26, buff=0.35).next_to(head, DOWN, buff=0.5)
        line = NumberLine(x_range=[0, 1, 0.5], length=7.0, include_numbers=True, font_size=22, color=GREY_C).to_edge(
            DOWN, buff=0.9)
        sharp = Dot(line.n2p(0.5), color=OK, radius=0.1)
        wide = Line(line.n2p(0), line.n2p(1), color=BET, stroke_width=10, stroke_opacity=0.7)
        with self.voiceover(
            "The imprecise view, which goes back to Keynes and was developed by Isaac Levi, Peter Walley and James "
            "Joyce. <bookmark mark='a'/>Represent a state of belief not by one probability function but by a set of "
            "them, a credal set, perhaps all those compatible with your evidence. <bookmark mark='b'/>Then each "
            "proposition gets a lower and an upper probability. <bookmark mark='c'/>For the known urn, the set is "
            "just one half. For the unknown urn, the credence in red is the whole interval from zero to one. "
            "<bookmark mark='d'/>To learn, conditionalize every member of the set. <bookmark mark='e'/>That simple "
            "rule has a startling consequence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(line), FadeIn(sharp))
            self.play(Create(wide))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def dilation(self):
        d = load("dilation")
        head = label(r"Dilation: \ learning can make you less sure", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        setup = stack([(r"$H$: \ a fair coin lands heads \ \ (credence exactly $\tfrac12$)", OK),
                       (r"$G$: \ something you know nothing about \ \ (credence $[0, 1]$), \ independent of the coin",
                        BET),
                       (r"you learn $M$: \ `the coin matches $G$' \ \ ($H \leftrightarrow G$)", CRED)],
                      font_size=23, aligned_edge=LEFT).next_to(head, DOWN, buff=0.35)
        hd = [r"P(G)", r"P(H)", r"P(H \mid M)"]
        rows = [[f"{r['P(G)']:.1f}", f"{r['P(H)']:.1f}", f"{r['P(H|M)']:.1f}"] for r in d["rows"][::2]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 1.6, 1.8], cell_h=0.42, font_size=22).move_to([-3.6, -1.5, 0])
        for r in range(len(rows)):
            grid.cell[r][2].set_color(CRED)
        why = MathTex(r"P(H \mid M) = \frac{P(H)P(G)}{P(H)P(G) + P(\lnot H)P(\lnot G)} = P(G)", font_size=30).move_to(
            [3.0, -0.6, 0])
        nl = NumberLine(x_range=[0, 1, 0.5], length=5.0, include_numbers=True, font_size=20, color=GREY_C).move_to(
            [3.0, -2.2, 0])
        before = Dot(nl.n2p(0.5), color=OK, radius=0.1)
        bl = label(r"before: \ $\{\tfrac12\}$", font_size=20, color=OK).next_to(before, UP, buff=0.2)
        after = Line(nl.n2p(d["after"][0]), nl.n2p(d["after"][1]), color=BAD, stroke_width=10, stroke_opacity=0.75)
        al = label(r"after: \ $[0, 1]$", font_size=20, color=BAD).next_to(nl, DOWN, buff=0.5)
        foot = label(r"every member is sure of $\tfrac12$ before; \ after, \ they scatter \ (Seidenfeld and "
                     r"Wasserman, \ 1993)", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Dilation. <bookmark mark='a'/>H: a fair coin lands heads; your credence is exactly one half. G: "
            "something you know nothing about, with credence anywhere from zero to one, and independent of the coin. "
            "Now you learn M: the coin's outcome matches G. <bookmark mark='b'/>The Reasoner runs through the members "
            "of your credal set. Every one gives H one half beforehand. <bookmark mark='c'/>After learning M, each "
            "member's credence in H equals its credence in G, by Bayes's theorem. <bookmark mark='d'/>So your "
            "credence in H dilates, from exactly a half to the whole interval. You have learned something, and are "
            "less sure about the coin than before, whatever M turns out to say. Teddy Seidenfeld and Larry Wasserman "
            "studied this in 1993; to critics it shows that imprecise credences are irrational."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in setup], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][0], grid.cell[r][1])) for r in range(len(rows))],
                                  lag_ratio=0.15), FadeIn(nl), FadeIn(before), FadeIn(bl))
            vo.wait_until("c")
            self.play(Write(why))
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(Create(after), FadeIn(al))
            self.play(FadeIn(foot))
        self.clear_scene()

    def elga(self):
        hc = history_card(2010, r"Adam Elga", r"`Subjective Probabilities Should Be Sharp'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        hd = [VGroup(), r"\text{if } H", r"\text{if } \lnot H"]
        rows = [[r"\text{bet A}", r"-10", r"+15"], [r"\text{bet B}", r"+15", r"-10"],
                [r"\text{both}", r"+5", r"+5"]]
        grid = ValueGrid(hd, rows, col_w=[2.0, 1.8, 1.8], cell_h=0.55, font_size=28).move_to([-3.2, -0.4, 0])
        for c in (1, 2):
            grid.cell[2][c].set_color(OK)
        rows_t = stack([
            (r"your credence in $H$: \ anywhere in $[0.1, 0.8]$", CRED),
            (r"offered A, \ then B: \ each alone has no definite expectation", WHITE),
            (r"a permissive rule lets you refuse each", WHITE),
            (r"refuse both, \ and you pass up a sure \$5", BAD),
            (r"replies: \ choose by plans, \ not one bet at a time; \ $\Gamma$-maximin; \ E-admissibility", GREY_A),
        ], font_size=22, aligned_edge=LEFT, width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Adam Elga pressed a pragmatic objection in 2010. <bookmark mark='a'/>Your credence in H is imprecise, "
            "anywhere from point one to point eight. You are offered bet A: lose ten if H, win fifteen if not. Then "
            "bet B: win fifteen if H, lose ten if not. <bookmark mark='b'/>Taken together, the bets win five dollars "
            "for sure. <bookmark mark='c'/>But considered one at a time, each has an expected value that is positive "
            "for some members of your set and negative for others. <bookmark mark='d'/>Many decision rules for "
            "imprecise credence permit refusing each. <bookmark mark='e'/>Refuse both, and you have turned down a sure "
            "five dollars. <bookmark mark='f'/>Defenders reply that a rational agent chooses whole plans, not one bet "
            "at a time, or adopt rules such as gamma-maximin or E-admissibility that force the sequence to cohere."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows_t[0]), FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(m) for m in grid.cell[0]])
            self.play(*[FadeIn(m) for m in grid.cell[1]])
            vo.wait_until("b")
            self.play(*[FadeIn(m) for m in grid.cell[2]])
            for mk, r in zip("cdef", rows_t[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def uses(self):
        head = label(r"Imprecision in practice", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"robust Bayesian analysis: \ report how a conclusion varies across a set of priors", WHITE),
            (r"Dempster--Shafer belief functions \ (1967, \ 1976): \ evidence that supports a set", WHITE),
            (r"climate science: \ the IPCC's `likely' means 66--100\%", WHITE),
            (r"economics: \ ambiguity aversion and the equity premium", WHITE),
            (r"the open question: \ is imprecision a fact about evidence, \ or a failure to think it through?", GOAL),
        ], font_size=24, buff=0.35, width=12.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Imprecise probability is used in practice. <bookmark mark='a'/>Robust Bayesian analysis reports how a "
            "conclusion changes as the prior ranges over a set. <bookmark mark='b'/>Dempster and Shafer's belief "
            "functions model evidence that supports a set of possibilities without dividing it among them. "
            "<bookmark mark='c'/>The climate scientists of the IPCC use calibrated ranges: likely means a "
            "probability of sixty six to a hundred percent. <bookmark mark='d'/>And economists use ambiguity "
            "aversion to model markets. <bookmark mark='e'/>The philosophical question remains open: is imprecision "
            "a fact about evidence, or a failure to finish thinking?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
