from __future__ import annotations

from fractions import Fraction

from videos.philosophy.philosophy14.common import *  # noqa: F403

COLS = {"AC": OK, "A~C": BAD, "~A~C": GREY_B, "~AC": BEL}
TEX = {"AC": r"AC", "A~C": r"A\bar C", "~A~C": r"\bar A \bar C", "~AC": r"\bar A C"}


def bars(probs: dict, x0=-4.6, base=-2.2, scale=4.2, w=0.9, gap=1.25) -> VGroup:
    g = VGroup()
    for i, (k, p) in enumerate(probs.items()):
        h = max(scale * float(p), 0.02)
        b = Rectangle(width=w, height=h, stroke_width=0, fill_color=COLS[k], fill_opacity=0.85).move_to(
            [x0 + i * gap, base + h / 2, 0])
        v = MathTex(str(Fraction(p).limit_denominator(100)), font_size=26, color=COLS[k]).next_to(b, UP, buff=0.08)
        n = MathTex(TEX[k], font_size=26).move_to([x0 + i * gap, base - 0.3, 0])
        g.add(VGroup(b, v, n))
    return g


class Trivial(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The probability of conditionals", r"Is the probability of `if $A$, $C$' the "
                                                                   r"probability of $C$ given $A$?",
                            lit=(1976,), part=PART)
        with self.voiceover("Chapter eight. The probability of conditionals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.proof()
        self.search()
        self.imaging()
        self.price()
        self.brick()

    def thesis(self):
        head = label(r"How likely is a conditional?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        q = label(r"a card is drawn: \ `if it is red, \ it is a heart'", font_size=26, color=NEW).next_to(
            head, DOWN, buff=0.4)
        opts = VGroup(
            VGroup(label(r"the material conditional", font_size=22, color=GREY_A),
                   MathTex(r"P(\lnot\text{red} \lor \text{heart}) = \tfrac12 + \tfrac14 = \tfrac34", font_size=30)),
            VGroup(label(r"the conditional probability", font_size=22, color=GREY_A),
                   MathTex(r"P(\text{heart} \mid \text{red}) = \tfrac12", font_size=30, color=OK)))
        for o in opts:
            o.arrange(DOWN, buff=0.15)
        opts.arrange(RIGHT, buff=1.0).next_to(q, DOWN, buff=0.5)
        rows = stack([
            (r"almost everyone says $\tfrac12$ \ (Evans and Over; \ Oberauer)", WHITE),
            (r"Adams's thesis: \ the assertability of `if $A$, $C$' is $P(C \mid A)$", BEL),
            (r"Stalnaker's thesis: \ there is a proposition $A \to C$ with $P(A \to C) = P(C \mid A)$", NEW),
        ], font_size=23, buff=0.3, width=12.4).next_to(opts, DOWN, buff=0.5)
        with self.voiceover(
            "How likely is a conditional to be true? <bookmark mark='a'/>A card is drawn from a deck. If it is red, "
            "it is a heart. <bookmark mark='b'/>Read materially, the conditional is true unless the card is a red "
            "diamond: three quarters. <bookmark mark='c'/>But nearly everyone says a half: the chance it is a heart, "
            "given that it is red. Psychologists such as Jonathan Evans and David Over have confirmed this many times. "
            "<bookmark mark='d'/>Ernest Adams made it a thesis: the assertability of if A, C is the conditional "
            "probability of C given A. <bookmark mark='e'/>Robert Stalnaker went further: there is a proposition, if "
            "A then C, whose probability is the conditional probability. David Lewis proved in 1976 that this cannot "
            "be."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(opts[0]))
            vo.wait_until("c")
            self.play(FadeIn(opts[1]), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def proof(self):
        d = load("trivial")["proof"]
        head = label(r"Lewis's triviality proof, \ on three worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        P0 = {"AC": Fraction(1, 3), "A~C": Fraction(1, 3), "~A~C": Fraction(1, 3)}
        b0 = bars(P0)
        PC = {"AC": Fraction(1), "A~C": Fraction(0), "~A~C": Fraction(0)}
        PN = {"AC": Fraction(0), "A~C": Fraction(1, 2), "~A~C": Fraction(1, 2)}
        bC, bN = bars(PC), bars(PN)
        lines = stack([
            (rf"$P(C \mid A) = {d['P(C|A)']}$", WHITE),
            (r"condition on $C$: \ $P_C(C \mid A) = 1$, \ so $P_C(X) = 1$: \ $X \ni AC$", OK),
            (r"condition on $\lnot C$: \ $P_{\lnot C}(C \mid A) = 0$, \ so $X$ misses $A\bar C$ and $\bar A \bar C$", BAD),
            (r"so $X = \{AC\} = C$, \ and \ $P(X) = P(C) = " + d["P(C)"] + r"$", BEL),
            (rf"but $P(X)$ should be $P(C \mid A) = {d['P(C|A)']}$: \ contradiction", BAD),
        ], font_size=22, aligned_edge=LEFT, width=7.0).move_to([2.9, 0.0, 0])
        gen = label(r"in general: \ $P(A \to C) = P(C)$ \ whenever both $A C$ and $A \bar C$ are possible", font_size=21,
                    color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is Lewis's proof, on three worlds. <bookmark mark='a'/>A credence spreads a third each over three "
            "worlds: A and C, A and not C, and neither. The credence of C given A is one half. Suppose some "
            "proposition X has the probability of C given A, for this credence and for everything it can become by "
            "conditioning. <bookmark mark='b'/>Condition on C. All the mass slides onto the A-and-C world, and now C "
            "given A is certain; so X must contain that world. <bookmark mark='c'/>Condition instead on not C. Now C "
            "given A has probability zero, so X must miss both of the other worlds. <bookmark mark='d'/>So X is just "
            "C, and its probability is a third. <bookmark mark='e'/>But it should be a half. Contradiction. "
            "<bookmark mark='f'/>In general the argument shows that the probability of the conditional must equal the "
            "probability of C itself, whenever both A-worlds are possible: conditional probability collapses into "
            "plain probability, which is the triviality."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(b0), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Transform(b0, bC), FadeIn(lines[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Transform(b0, bN), FadeIn(lines[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(Transform(b0, bars(P0)), FadeIn(lines[3]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
            vo.wait_until("f")
            self.play(FadeIn(gen))
        self.clear_scene()

    def search(self):
        d = load("trivial")
        head = label(r"The Reasoner searches every proposition", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = []
        for key, name in (("search4", r"four worlds: \ $AC,\ A\bar C,\ \bar A C,\ \bar A \bar C$"),
                          ("search3", r"three worlds: \ $AC,\ A\bar C,\ \bar A \bar C$"),
                          ("trivial", r"no $A\bar C$ world \ (trivial)")):
            s = d[key]
            rows.append([label(name, font_size=21), MathTex(str(s["propositions"]), font_size=26),
                         MathTex(str(s["members"]), font_size=26),
                         MathTex(rf"{s['best_fits']}/{s['members']}", font_size=26,
                                 color=OK if s["winners"] else BAD),
                         mark(bool(s["winners"]), 26)])
        hd = [label(r"model", font_size=21, color=P.CLAIM), label(r"propositions $X$", font_size=21, color=P.CLAIM),
              label(r"credences", font_size=21, color=P.CLAIM), label(r"best fit", font_size=21, color=P.CLAIM),
              label(r"some $X$ works?", font_size=21, color=P.CLAIM)]
        grid = ValueGrid(hd, rows, col_w=[5.0, 2.2, 1.8, 1.8, 2.2], cell_h=0.65, font_size=21).next_to(head, DOWN,
                                                                                                    buff=0.6)
        note = stack([(r"credences: \ the uniform one on every set of worlds \ (closed under conditioning)", GREY_A),
                      (r"only the trivial model, \ where $A$ settles $C$, \ has a proposition that works", GOAL)],
                     font_size=22, width=12.4).next_to(grid, DOWN, buff=0.5)
        with self.voiceover(
            "The Reasoner checks the result by brute force. <bookmark mark='a'/>It takes every proposition on a small "
            "model, and every credence in a family closed under conditioning: the uniform credence on each set of "
            "worlds. <bookmark mark='b'/>With four worlds, sixteen propositions and twelve credences: no proposition "
            "matches the conditional probability for more than six of them. <bookmark mark='c'/>With three worlds, no "
            "proposition works either. <bookmark mark='d'/>Only in the trivial model, with no world where A holds and "
            "C fails, does one work, and there the conditional is certain anyway."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(note[0]))
            for mk, r in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(m) for m in grid.cell[r]])
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def imaging(self):
        d = load("trivial")["imaging"]
        head = label(r"Imaging: \ what a counterfactual's probability is", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        P0 = {"AC": 0.2, "A~C": 0.2, "~AC": 0.4, "~A~C": 0.2}
        b0 = bars(P0, x0=-5.2, gap=1.2)
        cond = {"AC": 0.5, "A~C": 0.5, "~AC": 0.0, "~A~C": 0.0}
        img = {"AC": 0.6, "A~C": 0.4, "~AC": 0.0, "~A~C": 0.0}
        rows = stack([
            (r"conditioning on $A$: \ the $\bar A$ mass is spread \textit{in proportion}", OK),
            (rf"$P(C \mid A) = {d['P(C|A)']:.1f}$", OK),
            (r"imaging on $A$: \ each $\bar A$ world sends its mass to its \textit{closest} $A$-world", NEW),
            (rf"$P_A(C) = {d['P_A(C)']:.1f}$", NEW),
            (r"Lewis: \ $P(A > C) = P_A(C)$ \ for Stalnaker's counterfactual", GOAL),
            (r"here $\bar A C$'s closest $A$-world is $AC$; \ $\bar A \bar C$'s is $A\bar C$", GREY_A),
        ], font_size=22, aligned_edge=LEFT, width=6.8).move_to([3.1, 0.0, 0])
        with self.voiceover(
            "Lewis also said what the probability of a counterfactual is. <bookmark mark='a'/>Take a credence over "
            "four worlds. To condition on A, delete the not-A worlds and spread their mass over the A-worlds in "
            "proportion: <bookmark mark='b'/>C given A is a half. <bookmark mark='c'/>To image on A instead, let each "
            "not-A world send its mass to its own closest A-world. <bookmark mark='d'/>Here the probability of C "
            "becomes point six. <bookmark mark='e'/>Lewis showed that the probability of Stalnaker's counterfactual is "
            "exactly the imaged probability, not the conditional one. Counterfactuals are propositions, and "
            "indicatives, if Adams is right, behave like something else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(b0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(Transform(b0, bars(cond, x0=-5.2, gap=1.2)), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Transform(b0, bars(P0, x0=-5.2, gap=1.2)), FadeIn(rows[2]), FadeIn(rows[5]))
            self.play(Transform(b0, bars(img, x0=-5.2, gap=1.2)), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def price(self):
        d = load("trivial")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=3.8, font_size=20,
                       center=[0, -0.45, 0], title=r"The Price List: \ the triviality cluster")
        assert d["mcs"] == [["T1"], ["T2"], ["T3"], ["T4"]]
        positions = [(("T3",), r"Adams, \ Edgington", r"indicatives have no truth conditions: \ they express a "
                                                       r"conditional credence"),
                     (("T1",), r"Lewis, \ Jackson", r"`if' is material; \ $P(C \mid A)$ measures only "
                                                    r"assertability"),
                     (("T2",), r"context-dependence", r"the proposition expressed shifts with the credence \ "
                                                     r"(van Fraassen; \ Khoo and Mandelkern)"),
                     (("T4",), r"nobody", r"credences that never separate $P(C \mid A)$ from $P(C)$")]
        with self.voiceover(
            "The Reasoner sets out the cluster as a Price List. <bookmark mark='a'/>Four claims: the probability of a "
            "conditional is the conditional probability, for every credence; rational credences stay rational when "
            "conditioned; a conditional is true or false at each world; and some credence makes the conditional "
            "probability differ from the plain one. <bookmark mark='b'/>Together inconsistent; any one can go. "
            "<bookmark mark='c'/>Ernest Adams and Dorothy Edgington give up the third: indicative conditionals have no "
            "truth conditions; to accept one is to have a high conditional credence. <bookmark mark='d'/>Lewis and "
            "Frank Jackson give up the first: if is material, and the conditional probability measures only how "
            "assertable it is. <bookmark mark='e'/>Others give up the second, in effect: the proposition a conditional "
            "expresses shifts with the credence, as Bas van Fraassen and, recently, Justin Khoo and Matthew Mandelkern "
            "propose. <bookmark mark='f'/>Giving up the fourth would make credence trivial, and nobody does."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=2.8)
                self.play(*anims)
        self.clear_scene()

    def brick(self):
        w = wall(upto=14, current=14).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(14, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the fourteenth brick in the Wall. <bookmark mark='a'/>The dream: conditionals as ordinary "
            "propositions, believed by the Ramsey test and believed to the degree of the conditional probability. "
            "<bookmark mark='b'/>The wall: Lewis's triviality theorem, and Gärdenfors's impossibility theorem. "
            "<bookmark mark='c'/>What they force: conditionals may not state facts at all; or, if they do, the facts "
            "they state shift with what we know. Either way, if is not a connective like and or or."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[14], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1]))
            vo.wait_until("c")
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()
