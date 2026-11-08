from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Levels(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Levels of selection", r"Genes, organisms or groups: what does selection act on?",
                            lit=(1962, 2010), part=PART)
        with self.voiceover("Chapter six. Levels of selection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.groups()
        self.decompose()
        self.debate()
        self.brick()

    def groups(self):
        d = load("levels")
        head = label(r"Two groups, \ and a reversal", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        boxes = VGroup()
        for i, g in enumerate(d["groups"]):
            box = RoundedRectangle(width=4.2, height=2.2, corner_radius=0.2, color=GROUP, stroke_width=2.5).move_to(
                [-3.4 + 6.8 * i, 1.0, 0])
            dots = VGroup(*[Dot(radius=0.13, color=ALT if k < g["k"] else SELF) for k in range(g["n"])]).arrange_in_grid(
                2, 5, buff=0.3).move_to(box)
            t = label(f"group {i + 1}: \\ {g['k']} altruists of {g['n']}", font_size=19, color=GROUP).next_to(
                box, UP, buff=0.12)
            boxes.add(VGroup(box, dots, t))
        rows = stack([(r"an altruist pays $c = 0.1$; \ everyone gains $b = 0.5$ times the share of altruists", WHITE),
                      (r"within each group, \ altruists do worse: \ " + ", \\ ".join(
                          f"{g['w_alt']:.1f} vs {g['w_self']:.1f}" for g in d["groups"]), BAD),
                      (r"yet altruist-rich groups grow faster: \ the global share rises from " + f"{d['p0']:.3f}" +
                       r" to " + f"{d['p1']:.3f}", OK),
                      (r"Simpson's paradox \ (Part 16), \ in evolution", GOAL)], font_size=21).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Can selection act on groups? <bookmark mark='a'/>Take two groups of ten. The first has two altruists, "
            "the second eight. An altruist pays a small cost; every member gains in proportion to the share of "
            "altruists in its group. <bookmark mark='b'/>Within each group, altruists have lower fitness than their "
            "selfish neighbours. <bookmark mark='c'/>Yet the altruist-rich group grows faster, and across the whole "
            "population the share of altruists rises. <bookmark mark='d'/>It is Simpson's paradox from Part 16, "
            "inside evolution: the trend in every group reverses in the aggregate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def decompose(self):
        d = load("levels")
        head = label(r"The multilevel Price equation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"\bar w\,\Delta \bar z", r"=", r"\mathrm{cov}_k(W_k, Z_k)", r"+",
                     r"\mathrm{E}_k\big[\mathrm{cov}_i(w_{ik}, z_{ik})\big]", font_size=38).next_to(head, DOWN, buff=0.6)
        eq[2].set_color(GROUP)
        eq[4].set_color(ALT)
        b1 = Brace(eq[2], DOWN, color=GROUP)
        t1 = label(r"between groups", font_size=20, color=GROUP).next_to(b1, DOWN)
        b2 = Brace(eq[4], DOWN, color=ALT)
        t2 = label(r"within groups", font_size=20, color=ALT).next_to(b2, DOWN)
        hd = [r"\text{term}", r"\text{value}"]
        rows = [[MathTex(r"\text{between groups}", font_size=24, color=GROUP), MathTex(f"{d['between']:+.4f}", font_size=24,
                                                                                      color=GROUP)],
                [MathTex(r"\text{within groups}", font_size=24, color=ALT), MathTex(f"{d['within']:+.4f}", font_size=24,
                                                                                   color=ALT)],
                [MathTex(r"\text{total } \Delta \bar z", font_size=24), MathTex(f"{d['delta']:+.4f}", font_size=24)]]
        grid = ValueGrid(hd, rows, col_w=[3.4, 2.0], cell_h=0.55, font_size=20).move_to([-2.6, -1.8, 0])
        side = stack([(r"Price \ (1972), \ Hamilton \ (1975): \ apply the equation twice", WHITE),
                      (r"group selection wins when the between-group term outweighs the within-group term", OK),
                      (r"the two terms sum exactly to the change \ (error below $10^{-15}$)", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=5.6).move_to([3.6, -1.8, 0])
        assert d["check"] < 1e-15
        with self.voiceover(
            "The Price equation explains the reversal. <bookmark mark='a'/>Apply it to groups, and then again to "
            "individuals within each group. The total change splits into two terms. <bookmark mark='b'/>The first "
            "is the covariance, across groups, between a group's share of altruists and its productivity: selection "
            "between groups. <bookmark mark='c'/>The second is the average covariance within groups: selection "
            "within them. <bookmark mark='d'/>The Reasoner computes both. Between groups, plus point zero three; "
            "within groups, minus point zero one three; and their sum is exactly the observed change. "
            "<bookmark mark='e'/>Altruism spreads when the first term outweighs the second. Price and Hamilton "
            "worked this out together in the early 1970s."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq[0]), Write(eq[1]))
            vo.wait_until("b")
            self.play(Write(eq[2]), GrowFromCenter(b1), FadeIn(t1))
            vo.wait_until("c")
            self.play(Write(eq[3]), Write(eq[4]), GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                        lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
        self.clear_scene()

    def debate(self):
        head = label(r"A long argument", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Wynne-Edwards \ (1962)", r"animals restrain breeding for the good of the group", GROUP),
            (r"Williams \ (1966)", r"\textit{Adaptation and Natural Selection}: \ group adaptation is rarely needed; \ "
                                   r"think at the gene's level", GENE),
            (r"Sober and Wilson \ (1998)", r"\textit{Unto Others}: \ multilevel selection is real, \ and can produce "
                                           r"altruism", ORG),
            (r"Nowak, \ Tarnita and Wilson \ (2010)", r"inclusive fitness is unnecessary and limited", BAD),
            (r"Abbot et al. \ (2011)", r"a reply signed by 137 biologists: \ inclusive fitness is well founded", OK),
            (r"Okasha \ (2006)", r"the two bookkeepings are often equivalent: \ the question is which is causally "
                                 r"apt", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=7.8, x_text=-1.8, label_size=20)
        with self.voiceover(
            "The levels-of-selection debate has run for sixty years. <bookmark mark='a'/>In 1962 V. C. Wynne-Edwards "
            "argued that animals restrain their breeding for the good of the group. <bookmark mark='b'/>George "
            "Williams replied in 1966 that adaptations for the group are rarely needed, and that the gene's-eye view "
            "explains more. <bookmark mark='c'/>Elliott Sober and David Sloan Wilson defended multilevel selection "
            "in Unto Others. <bookmark mark='d'/>In 2010 Martin Nowak, Corina Tarnita and Edward O. Wilson argued in "
            "Nature that Hamilton's inclusive fitness theory is unnecessary. <bookmark mark='e'/>A reply signed by "
            "one hundred and thirty-seven biologists defended it. <bookmark mark='f'/>Samir Okasha's diagnosis: the "
            "kin-selection and multilevel accounts are often two ways of keeping the same books. The live question "
            "is which bookkeeping matches the causal structure of a particular case."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brick(self):
        w = wall(upto=19, current=19).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(19, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the nineteenth brick in the Wall. <bookmark mark='a'/>The dream: a single level at which "
            "selection really acts, genes, organisms or groups. <bookmark mark='b'/>The wall: the Price equation "
            "splits any change into between- and within-level terms, at every level at once, so the mathematics "
            "alone never singles one out. <bookmark mark='c'/>What it forces: pluralism about units of selection, "
            "with the choice in each case settled by causal structure, not by algebra."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[19], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
