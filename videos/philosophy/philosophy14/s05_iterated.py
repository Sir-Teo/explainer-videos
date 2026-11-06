from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

BIRD = {"rf": r"\text{red, flies}", "r~f": r"\text{red, no}", "~rf": r"\text{other, flies}",
        "~r~f": r"\text{other, no}"}


def ladder(rank: dict, x0: float, names=None, y0=-2.4, dy=0.85, font_size=22, color_of=None) -> dict:
    """Worlds as chips stacked by rank (0 at the bottom). Returns {world: chip}."""
    by = {}
    for w, k in rank.items():
        by.setdefault(k, []).append(w)
    chips = {}
    for k, ws in by.items():
        for i, w in enumerate(sorted(ws)):
            col = color_of(w) if color_of else WHITE
            t = MathTex(names[w] if names else wtex(w), font_size=font_size, color=col)
            box = RoundedRectangle(width=max(t.width + 0.3, 1.0), height=0.5, corner_radius=0.1, stroke_color=col,
                                   stroke_width=2, fill_color="#0E1621", fill_opacity=1)
            chip = VGroup(box, t)
            t.move_to(box)
            chip.move_to([x0 + (i - (len(ws) - 1) / 2) * (box.width + 0.15), y0 + k * dy, 0])
            chips[w] = chip
    return chips


class Iterated(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Changing again", r"After a revision, what are the new spheres?", lit=(1988,),
                            part=PART)
        with self.voiceover("Chapter four. Changing again."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.spohn()
        self.magnitudes()
        self.operators()
        self.table()
        self.bird()

    def problem(self):
        head = label(r"AGM revises once", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"input: \ a belief set and its spheres; \ output: \ a belief set", WHITE),
            (r"but the next revision needs the next spheres", BAD),
            (r"so a belief state must be more than a belief set: \ an \textit{ordering} of worlds", GOAL),
            (r"Darwiche and Pearl \ (1997): \ postulates for how the ordering itself should change", NEW),
        ], font_size=26, buff=0.35, width=12.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "AGM describes a single revision. <bookmark mark='a'/>It takes a belief set, with its spheres, and returns "
            "a belief set. <bookmark mark='b'/>But to revise a second time, you need the spheres around the new "
            "beliefs, and AGM says almost nothing about them. <bookmark mark='c'/>So a state of belief must be more "
            "than the set of things believed: it is an ordering of all the worlds by plausibility. "
            "<bookmark mark='d'/>Adnan Darwiche and Judea Pearl proposed postulates for how that ordering should "
            "change."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def spohn(self):
        hc = history_card(1988, r"Wolfgang Spohn", r"`Ordinal Conditional Functions'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        rank = {"pq": 0, "p~q": 1, "~pq": 2, "~p~q": 4}
        chips = ladder(rank, -3.2)
        axis = VGroup(Arrow([-5.6, -2.7, 0], [-5.6, 1.4, 0], buff=0, color=GREY_C, stroke_width=2),
                      label(r"disbelief", font_size=20, color=GREY_B).move_to([-5.6, 1.7, 0]))
        nums = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).move_to([-5.9, -2.4 + k * 0.85, 0])
                        for k in range(5)])
        rows = stack([
            (r"$\kappa(w)$: \ how surprising world $w$ would be \ (0: not at all)", WHITE),
            (r"$\kappa(A) = \min_{w \in A} \kappa(w)$", NEW),
            (r"believe $A$ \ iff \ $\kappa(\lnot A) > 0$; \ firmness \ $= \kappa(\lnot A)$", BEL),
            (r"here: \ believe $p$ (firmness 2) \ and $q$ (firmness 1)", GREY_A),
            (r"like probabilities, \ but with $\min$ for $+$ \ and $+$ for $\times$", GOAL),
        ], font_size=22, aligned_edge=LEFT, width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Wolfgang Spohn's ranking functions are the natural tool. <bookmark mark='a'/>Each world gets a "
            "non-negative whole number: how surprising it would be to learn that it is actual. Zero means not "
            "surprising at all. <bookmark mark='b'/>A proposition is as surprising as its least surprising world. "
            "<bookmark mark='c'/>You believe A when not A is surprising, and how firmly is measured by how surprising. "
            "<bookmark mark='d'/>Here you believe p, with firmness two, and q, with firmness one. "
            "<bookmark mark='e'/>Ranks behave like probabilities on a logarithmic scale: minimum plays the role of "
            "addition, and addition the role of multiplication. Spohn defined conditioning on them, and with it, a "
            "theory of iterated revision."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(axis), FadeIn(nums), *[FadeIn(c) for c in chips.values()])
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def magnitudes(self):
        head = label(r"Ranks as orders of magnitude", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"P(w) \approx \varepsilon^{\kappa(w)} \quad (\varepsilon \text{ tiny})", font_size=40,
                     color=NEW).next_to(head, DOWN, buff=0.5)
        hd = [r"\text{probability}", r"\text{ranks}"]
        rows = [[r"P(A \lor B) = P(A) + P(B)", r"\kappa(A \lor B) = \min(\kappa(A), \kappa(B))"],
                [r"P(A \land B) = P(A)\,P(B \mid A)", r"\kappa(A \land B) = \kappa(A) + \kappa(B \mid A)"],
                [r"P(B \mid A) = P(A \land B) / P(A)", r"\kappa(B \mid A) = \kappa(A \land B) - \kappa(A)"],
                [r"\text{Jeffrey's rule (Part 13)}", r"\text{Spohn's } (A, n)\text{-conditioning}"]]
        grid = ValueGrid(hd, rows, col_w=[5.6, 6.0], cell_h=0.65, font_size=26).next_to(eq, DOWN, buff=0.5)
        foot = label(r"belief is credence so close to 1 \ that only its order of magnitude matters", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why do ranks behave like probabilities? <bookmark mark='a'/>Read a world of rank k as having "
            "probability of the order of epsilon to the k, for some tiny epsilon. <bookmark mark='b'/>Then a sum of "
            "probabilities is dominated by its largest term, which is the smallest rank; a product of probabilities "
            "becomes a sum of ranks; and conditioning becomes subtraction. <bookmark mark='c'/>Spohn's conditioning "
            "on A with strength n is Jeffrey's rule from Part 13, written in orders of magnitude. "
            "<bookmark mark='d'/>On this view, belief is credence so close to one that only its order of magnitude "
            "matters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(m) for m in grid.cell[r]], run_time=0.7)
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in grid.cell[3]])
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def operators(self):
        rank = {"pq": 0, "p~q": 1, "~pq": 2, "~p~q": 4}
        mu = R.P("~p", ("p", "q"))
        head = label(r"Four ways to revise a ranking by $\lnot p$", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ops = [("natural", R.natural, r"best $\lnot p$ world to the bottom; \ rest kept in order"),
               ("lexicographic", R.lexicographic, r"every $\lnot p$ world below every $p$ world"),
               (r"Spohn, \ strength 1", lambda r, A: R.spohn(r, A, 1), r"shift the two halves"),
               ("amnesic", R.amnesic, r"new beliefs at 0; \ everything else at 1")]
        cols = VGroup()
        for i, (name, op, gloss) in enumerate(ops):
            x = -5.1 + i * 3.4
            new = op(rank, mu)
            chips = ladder(new, x, font_size=20, dy=0.72, y0=-2.6,
                           color_of=lambda w: NEW if w in mu else WHITE)
            col = VGroup(label(name, font_size=22, color=BEL).move_to([x, 1.6, 0]),
                         label(gloss, font_size=16, color=GREY_A).move_to([x, 1.15, 0]),
                         VGroup(*chips.values()))
            if col[1].width > 3.2:
                col[1].width = 3.2
            cols.add(col)
        before = label(r"before: \ $pq: 0, \ p\bar q: 1, \ \bar p q: 2, \ \bar p \bar q: 4$", font_size=22,
                       color=GREY_B).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Start from that ranking and revise by not p. Four operators. <bookmark mark='a'/>Craig Boutilier's "
            "natural revision moves the most plausible not-p world to the bottom and keeps everything else in its old "
            "order. <bookmark mark='b'/>Abhaya Nayak's lexicographic revision puts every not-p world below every p "
            "world: the news becomes the most entrenched thing you know. <bookmark mark='c'/>Spohn's conditioning "
            "shifts the not-p worlds down and the p worlds up, by a chosen strength. <bookmark mark='d'/>And an "
            "amnesic operator keeps only the new beliefs and flattens everything else. All four satisfy the AGM "
            "postulates for a single revision."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before))
            for mk, c in zip("abcd", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), FadeIn(c[1]), LaggedStart(*[FadeIn(x) for x in c[2]], lag_ratio=0.15))
        self.clear_scene()

    def table(self):
        d = load("iterated")
        head = label(r"The Darwiche--Pearl postulates", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        dp = VGroup(*[VGroup(label(k, font_size=22, color=BEL), label(f, font_size=22),
                             label(g, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.35)
                      for k, f, g in d["dp"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN,
                                                                                                buff=0.3)
        keys = [k for k, _, _ in d["dp"]]
        names = list(d["table"])
        hd = [label(r"operator", font_size=21, color=P.CLAIM)] + [label(k, font_size=21, color=P.CLAIM) for k in keys]
        rows = [[label(n, font_size=21)] + [mark(d["table"][n][k], 26) for k in keys] for n in names]
        grid = ValueGrid(hd, rows, col_w=[4.2] + [1.3] * 4, cell_h=0.55, font_size=21).next_to(dp, DOWN, buff=0.35)
        foot = stack([(r"Spohn with fixed strength: \ if $\lnot\mu$ was already disbelieved more firmly, \ `revising' "
                       r"by $\mu$ \textit{weakens} it", BAD),
                      (r"amnesic: \ forgets every conditional belief", BAD)], font_size=20, width=12.4).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "Darwiche and Pearl's four postulates constrain the ordering. <bookmark mark='a'/>The first two: revising "
            "by mu leaves the order among the mu-worlds alone, and the order among the not-mu worlds alone. The other "
            "two: a mu-world that was more plausible than a not-mu world stays more plausible, and one that was at "
            "least as plausible never sinks behind it. <bookmark mark='b'/>The Reasoner checks the four operators "
            "against all four, for every pair of propositions. Natural and lexicographic revision pass. "
            "<bookmark mark='c'/>Spohn's conditioning, with a fixed strength of one, fails the last two: if not mu was "
            "already disbelieved more firmly than that, conditioning on mu actually weakens the belief. "
            "<bookmark mark='d'/>And the amnesic operator fails the first three: it forgets every conditional belief."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dp], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in (0, 1):
                self.play(*[FadeIn(m) for m in grid.cell[r]])
            vo.wait_until("c")
            self.play(*[FadeIn(m) for m in grid.cell[2]], FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(m) for m in grid.cell[3]], FadeIn(foot[1]))
        self.clear_scene()

    def bird(self):
        d = load("iterated")["demo"]
        head = label(r"The red bird \ (Darwiche and Pearl)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        start = {"rf": 0, "r~f": 1, "~rf": 1, "~r~f": 2}
        story = stack([(r"you see a red bird that flies", WHITE),
                       (r"told: \ it isn't red", NEW),
                       (r"then: \ it is red after all", NEW)], font_size=23, aligned_edge=LEFT).move_to(
            [-4.6, 1.6, 0])
        x_n, x_a = 0.2, 4.2
        nat0 = ladder(start, x_n, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        am0 = ladder(start, x_a, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        tn = label(r"natural", font_size=24, color=BEL).move_to([x_n, 1.9, 0])
        ta = label(r"amnesic", font_size=24, color=BEL).move_to([x_a, 1.9, 0])
        r_nat1 = R.natural(start, R.P("~r", ("r", "f")))
        r_am1 = R.amnesic(start, R.P("~r", ("r", "f")))
        nat1 = ladder(r_nat1, x_n, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        am1 = ladder(r_am1, x_a, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        nat2 = ladder(d["natural"]["rank"], x_n, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        am2 = ladder(d["amnesic"]["rank"], x_a, names=BIRD, font_size=18, dy=0.75, y0=-2.6)
        verdict = VGroup(label(r"believes it flies", font_size=22, color=OK).move_to([x_n, -3.3, 0]),
                         label(r"has forgotten that it flies", font_size=22, color=BAD).move_to([x_a, -3.3, 0]))

        def move(a, b):
            return [a[w].animate.move_to(b[w].get_center()) for w in a]
        with self.voiceover(
            "Darwiche and Pearl's example shows why the postulates matter. <bookmark mark='a'/>You see a bird; it looks "
            "red, and it flies. <bookmark mark='b'/>Then someone tells you it isn't red. Both agents move to the most "
            "plausible world where it isn't red, and still believe it flies. <bookmark mark='c'/>Then a better look: "
            "it is red after all. The natural reviser returns to the red, flying bird. The amnesic one believes it is "
            "red, and no longer knows whether it flies: the first revision erased the conditional belief that, if it "
            "is red, it flies. <bookmark mark='d'/>Rational revision must preserve what the news does not bear on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tn), FadeIn(ta), *[FadeIn(c) for c in nat0.values()],
                      *[FadeIn(c) for c in am0.values()])
            vo.wait_until("a")
            self.play(FadeIn(story[0]))
            vo.wait_until("b")
            self.play(FadeIn(story[1]), *move(nat0, nat1), *move(am0, am1), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(story[2]), *move(nat0, nat2), *move(am0, am2), run_time=1.6)
            self.play(FadeIn(verdict))
            vo.wait_until("d")
            self.play(Indicate(verdict[1], color=BAD))
        self.clear_scene()
