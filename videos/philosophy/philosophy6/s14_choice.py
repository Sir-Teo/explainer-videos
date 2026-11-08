from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403

DIRS = {"a": RIGHT, "A": LEFT, "b": UP, "B": DOWN}
FIRST_COL = {"a": "#7BD389", "A": "#FF6B6B", "b": "#6FB7FF", "B": "#FFD166"}


def cayley(words, center, step=1.55, ratio=0.5):
    """The Cayley graph of the free group on a, b: each reduced word is a point; edges halve in length per letter."""
    c = np.asarray(center, float)
    pts = {"": c}
    edges = VGroup()
    for w in sorted(words, key=len):
        if not w:
            continue
        parent = w[:-1]
        p = pts[parent] + DIRS[w[-1]] * step * ratio ** (len(w) - 1)
        pts[w] = p
        edges.add(Line(pts[parent], p, color=FIRST_COL[w[0]], stroke_width=3.2 * ratio ** (len(w) - 1) + 0.8))
    dots = VGroup(*[Dot(p, radius=0.07 * ratio ** max(len(w) - 1, 0) + 0.02,
                        color=FIRST_COL[w[0]] if w else WHITE) for w, p in pts.items()])
    return VGroup(edges, dots), pts


class Choice(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"The axiom of choice", r"Can you choose infinitely often, without a rule?",
                            lit=(1904, 1924), part=PART)
        with self.voiceover("Chapter thirteen. The axiom of choice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.shoes()
        self.equivalents()
        self.vitali()
        self.banach()

    def shoes(self):
        head = label(r"Russell: \ infinitely many pairs of shoes, \ and of socks", font_size=30, color=CONN).to_edge(
            UP, buff=0.5)
        shoes = VGroup()
        socks = VGroup()
        for i in range(6):
            x = -5.4 + 1.1 * i
            l_ = RoundedRectangle(width=0.32, height=0.55, corner_radius=0.12, color=GOAL, fill_opacity=0.25).move_to([x - 0.2, 1.1, 0])
            r_ = RoundedRectangle(width=0.32, height=0.55, corner_radius=0.12, color=GOAL, fill_opacity=0.25).move_to([x + 0.2, 1.1, 0])
            shoes.add(VGroup(l_, r_))
            s1 = RoundedRectangle(width=0.3, height=0.55, corner_radius=0.12, color=P.CLAIM, fill_opacity=0.25).move_to([x - 0.2, -1.0, 0])
            s2 = s1.copy().move_to([x + 0.2, -1.0, 0])
            socks.add(VGroup(s1, s2))
        sd = MathTex(r"\cdots", font_size=40, color=GREY_B).next_to(shoes, RIGHT, buff=0.3)
        kd = MathTex(r"\cdots", font_size=40, color=GREY_B).next_to(socks, RIGHT, buff=0.3)
        rule = label(r"shoes: \ `take the left one' \ is a rule", font_size=26, color=OK).move_to([3.6, 1.1, 0])
        norule = label(r"socks: \ no rule tells them apart", font_size=26, color=BAD).move_to([3.6, -1.0, 0])
        ac = definition_card(r"axiom of choice", r"for every family of nonempty sets, \ there is a function choosing "
                             r"one member from each", width=9.0, font_size=24, color=P.CLAIM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Bertrand Russell gave the clearest picture of the axiom of choice. <bookmark mark='a'/>From infinitely "
            "many pairs of shoes, you can choose one shoe from each pair by a rule: take the left one. "
            "<bookmark mark='b'/>From infinitely many pairs of socks, there is no rule: the two socks of a pair are "
            "indistinguishable. To choose one from each pair, you need an axiom saying that a choice exists. "
            "<bookmark mark='c'/>The axiom of choice says exactly that: for any family of nonempty sets, there is a "
            "function picking one member from each."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(shoes), FadeIn(sd), FadeIn(rule), *[s[0].animate.set_fill(OK, 0.7) for s in shoes])
            vo.wait_until("b")
            self.play(FadeIn(socks), FadeIn(kd), FadeIn(norule))
            vo.wait_until("c")
            self.play(FadeIn(ac))
        self.clear_scene()

    def equivalents(self):
        hc = history_card(1904, r"Ernst Zermelo", r"`Proof that every set can be well-ordered'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        texts = [r"the well-ordering theorem: \ every set can be well-ordered \ (Zermelo 1904)",
                 r"Zorn's lemma: \ if every chain has an upper bound, \ there is a maximal element \ (1935)",
                 r"every vector space has a basis \ (Blass 1984)",
                 r"Tychonoff's theorem: \ any product of compact spaces is compact \ (Kelley 1950)"]
        rows_ = VGroup(*[VGroup(MathTex(r"\iff", font_size=30, color=GREY_B), label(t, font_size=25)).arrange(
            RIGHT, buff=0.3) for t in texts])
        eq = VGroup(label(r"the axiom of choice", font_size=28, color=GOAL), *rows_).arrange(
            DOWN, aligned_edge=LEFT, buff=0.32).move_to([0.2, -0.5, 0])
        bars = VGroup(*[r[0] for r in rows_])
        eq = VGroup(eq[0], *[r[1] for r in rows_])
        with self.voiceover(
            "Zermelo made choice explicit in 1904, to prove that every set can be well-ordered, even the real "
            "numbers. <bookmark mark='a'/>The proof was controversial, but the principle turned out to be "
            "everywhere. <bookmark mark='b'/>Choice is equivalent to the well-ordering theorem, to Zorn's lemma, "
            "used throughout algebra, to the fact that every vector space has a basis, and to Tychonoff's theorem in "
            "topology. Much of modern mathematics rests on it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(eq[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(eq[i]), FadeIn(bars[i - 1])) for i in range(1, 5)],
                                  lag_ratio=0.4), run_time=4)
        self.clear_scene()

    def vitali(self):
        hc = history_card(1905, r"Giuseppe Vitali", r"a set of reals with no length at all", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        line = NumberLine(x_range=[0, 1, 0.25], length=10.0, include_numbers=True, color=GREY_C, font_size=22,
                          decimal_number_config={"num_decimal_places": 2}).move_to([0, 0.2, 0])
        rng = np.random.default_rng(5)
        reps = rng.uniform(0.02, 0.98, 14)
        dots = VGroup(*[Dot(line.n2p(x), radius=0.06, color=GOAL) for x in reps])
        cols = [SETC, ORD, CARD, "#F28EC2", "#6FB7FF", OK]
        copies = VGroup(*[VGroup(*[Dot(line.n2p((x + k / 7) % 1) + UP * 0.28 * k, radius=0.05, color=c)
                                   for x in reps]) for k, c in enumerate(cols, 1)])
        tags = VGroup(*[MathTex(rf"V + \tfrac{{{k}}}{{7}}", font_size=22, color=c).move_to(
            line.n2p(1) + RIGHT * 0.75 + UP * 0.28 * k) for k, c in enumerate(cols, 1)])
        steps = VGroup(label(r"call $x \sim y$ when $x - y$ is rational; \ choose one point from each class: \ $V$",
                             font_size=24),
                       label(r"the rational shifts of $V$ fill $[0, 1]$ \ (up to wrapping), \ disjointly, \ countably "
                             r"many", font_size=24),
                       label(r"so length$(V)$ $\times\ \infty$ \ must equal 1: \ neither 0 nor anything positive works",
                             font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "But choice also builds monsters. <bookmark mark='a'/>In 1905 Giuseppe Vitali called two numbers between "
            "zero and one equivalent when they differ by a fraction, and chose one number from each equivalence "
            "class. <bookmark mark='b'/>Sliding this set along by each fraction, and wrapping around, gives "
            "countably many disjoint copies that together fill the whole interval. <bookmark mark='c'/>If the set "
            "had a length, the copies would all have that same length, adding up to one. But countably many equal "
            "lengths add up to zero or to infinity, never to one. So Vitali's set has no length at all."
        ) as vo:
            self.play(FadeIn(hc), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(TransformFromCopy(dots, c), FadeIn(t)) for c, t in
                                    zip(copies, tags)], lag_ratio=0.35), run_time=3.5)
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.clear_scene()

    def banach(self):
        d = load("freegroup")
        hc = history_card(1924, r"Stefan Banach \& Alfred Tarski", r"one ball, cut into five pieces, reassembled into "
                          r"two", width=6.4, color=HIST).to_corner(UL, buff=0.3)
        graph, pts = cayley(d["words"], center=[-2.6, -0.6, 0])
        keys = VGroup(*[VGroup(Dot(radius=0.08, color=FIRST_COL[k]), MathTex(rf"W({n})", font_size=26,
                                                                           color=FIRST_COL[k])).arrange(RIGHT, buff=0.15)
                        for k, n in (("a", "a"), ("A", "a^{-1}"), ("b", "b"), ("B", "b^{-1}"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.4, 1.2, 0])
        eq = VGroup(MathTex(r"F_2 = W(a) \cup a\,W(a^{-1})", font_size=34, color=GOAL),
                    MathTex(r"F_2 = W(b) \cup b\,W(b^{-1})", font_size=34, color=GOAL)).arrange(DOWN, buff=0.25).move_to(
            [3.6, -0.6, 0])
        c = d["check"]
        chk = label(rf"the Reasoner: \ both identities hold on all {c['words']} words of length $\le {c['n']}$ "
                    r"$\checkmark$", font_size=22, color=OK).next_to(eq, DOWN, buff=0.3)
        moral = label(r"four pieces of the group make two copies of it; \ Hausdorff's rotations carry this onto the "
                      r"sphere", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        assert c["W(a) + aW(A)"] and c["W(b) + bW(B)"]
        with self.voiceover(
            "The most famous monster came from Stefan Banach and Alfred Tarski in 1924: a solid ball can be cut into "
            "five pieces and reassembled, by rotations alone, into two balls the same size as the first. "
            "<bookmark mark='a'/>The heart of the proof is this tree: the free group on two moves, a and b, and "
            "their inverses. Every word in the moves is a point. <bookmark mark='b'/>Sort the words by their first "
            "letter, into four colours. <bookmark mark='c'/>Now the paradox. Take the words that start with a "
            "inverse, and apply a in front: the a cancels, and you get every word that does not start with a. "
            "Together with the words that do start with a, that is the whole group. The same works for b. So two of "
            "the four pieces make a whole copy, and the other two make another. <bookmark mark='d'/>The Reasoner "
            "checks both identities on every word up to length six. Felix Hausdorff found two rotations of the "
            "sphere that behave like a and b; choice picks the points, and the ball doubles."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(graph[0]), FadeIn(graph[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(keys))
            vo.wait_until("c")
            self.play(FadeIn(eq))
            vo.wait_until("d")
            self.play(FadeIn(chk), FadeIn(moral))
        self.clear_scene()
