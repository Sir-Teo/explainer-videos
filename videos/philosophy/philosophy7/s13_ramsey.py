from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


def k_graph(n, red, blue, center=ORIGIN, r=1.4, red_c=None, blue_c=None) -> VGroup:
    pts = [np.array(center) + r * np.array([np.cos(PI / 2 + k * TAU / n), np.sin(PI / 2 + k * TAU / n), 0])
           for k in range(n)]
    g = VGroup()
    for a, b in red:
        g.add(Line(pts[a], pts[b], color=red_c or P.FALSE, stroke_width=4))
    for a, b in blue:
        g.add(Line(pts[a], pts[b], color=blue_c or "#6FB7FF", stroke_width=4))
    dots = VGroup(*[Dot(p, radius=0.09, color=WHITE) for p in pts])
    return VGroup(g, dots)


class Ramsey(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Independence in ordinary mathematics", r"Are the unprovable sentences only "
                            r"curiosities?", lit=(1977,), part=PART)
        with self.voiceover("Chapter twelve. Independence in ordinary mathematics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.party()
        self.ph()
        self.more()

    def question(self):
        head = label(r"Is $G$ a freak?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"$G$ and $\mathrm{Con}(\mathrm{PA})$ are about proofs and codes", font_size=28),
                      label(r"would any mathematician, \ asking an ordinary question, \ meet one?", font_size=28,
                            color=GOAL),
                      label(r"Part 6 already met two: \ Goodstein's sequences \ and the hydra \ (Kirby--Paris 1982)",
                            font_size=26, color=OK)).arrange(DOWN, buff=0.45).move_to([0, 0.4, 0])
        with self.voiceover(
            "For forty years after Gödel, a doubt remained. <bookmark mark='a'/>The undecidable sentences were about "
            "proofs and codes: artificial, a logician's curiosity. <bookmark mark='b'/>Would a mathematician asking "
            "an ordinary question ever meet one? <bookmark mark='c'/>Part 6 has already shown two that they would: "
            "Goodstein's sequences and the hydra, true statements about numbers that PA cannot prove. The first "
            "such example came from a theorem about colouring."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
        self.clear_scene()

    def party(self):
        d = load("ramsey")
        hc = history_card(1930, r"Frank Ramsey", r"`On a problem of formal logic': \ a case of the "
                          r"\textit{Entscheidungsproblem}", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        q = label(r"among any six people, \ are there three mutual friends \ or three mutual strangers?",
                  font_size=26, color=GOAL).next_to(hc, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        k5 = k_graph(5, d["red"], d["blue"], center=[-3.4, -1.4, 0], r=1.35)
        k5l = label(rf"$K_5$: \ {d['k5']} of its {d['k5_colourings']:,} colourings have no one-coloured "
                    rf"triangle".replace(",", "{,}"), font_size=22, color=GREY_A).next_to(k5, DOWN, buff=0.25)
        edges6 = [(a, b) for a in range(6) for b in range(a + 1, 6)]
        k6 = k_graph(6, [], edges6, center=[3.4, -1.4, 0], r=1.35, blue_c=GREY_C)
        k6l = label(rf"$K_6$: \ all {d['k6_colourings']:,} colourings have one".replace(",", "{,}"), font_size=22,
                    color=OK).next_to(k6, DOWN, buff=0.25)
        r33 = MathTex(r"R(3, 3) = 6", font_size=44, color=GOAL).move_to([0, -1.4, 0])
        assert d["k5"] == 12 and d["k6"] == 0
        with self.voiceover(
            "Frank Ramsey proved his theorem in a paper of 1930, while working on a case of Hilbert's decision "
            "problem. <bookmark mark='a'/>Its simplest case is a puzzle about a party. Among any six people, must "
            "there be three who all know each other, or three who are all strangers? Draw people as points, and "
            "colour each pair red for friends, blue for strangers. <bookmark mark='b'/>With five people you can "
            "avoid both: a red pentagon and a blue pentagram have no one-coloured triangle. The Reasoner finds all "
            "twelve such colourings among the thousand and twenty-four. <bookmark mark='c'/>With six people you "
            "cannot. The Reasoner tries all thirty-two thousand, seven hundred and sixty-eight colourings, and every "
            "one contains a red or a blue triangle. The Ramsey number R three three is six. "
            "<bookmark mark='d'/>Ramsey's theorem says the same for any sizes and any number of colours: complete "
            "disorder is impossible."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Create(k5[0]), FadeIn(k5[1]), run_time=2)
            self.play(FadeIn(k5l))
            vo.wait_until("c")
            self.play(Create(k6[0]), FadeIn(k6[1]), run_time=2)
            self.play(FadeIn(k6l), FadeIn(r33))
            vo.wait_until("d")
            self.play(Indicate(r33, color=GOAL, scale_factor=1.05))
        self.clear_scene()

    def ph(self):
        hc = history_card(1977, r"Jeff Paris \& Leo Harrington", r"`A mathematical incompleteness in Peano "
                          r"arithmetic'", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        fin = VGroup(label(r"finite Ramsey: \ for all $n, k, m$ there is an $N$ such that", font_size=26),
                     label(r"colour the $n$-element subsets of $\{1, \dots, N\}$ with $k$ colours: \ some set $H$ of "
                           r"size $m$ has all its $n$-subsets one colour", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 1.0, 0])
        plus = label(r"Paris--Harrington: \ add one condition, \ $|H| \ge \min H$ \ (`$H$ is large')",
                     font_size=28, color=GOAL).next_to(fin, DOWN, buff=0.5)
        res = VGroup(label(r"true: \ it follows from the infinite Ramsey theorem", font_size=26, color=OK),
                     label(r"unprovable in PA: \ the $N$ it needs grows faster than any function PA can prove total",
                           font_size=26, color=BAD)).arrange(DOWN, buff=0.25).next_to(plus, DOWN, buff=0.5)
        with self.voiceover(
            "In 1977 Jeff Paris and Leo Harrington found the first natural example. <bookmark mark='a'/>The finite "
            "Ramsey theorem says: for any sizes, there is an N so large that however you colour the subsets of one "
            "to N, some big set is all one colour. PA proves this easily. <bookmark mark='b'/>Now add one innocent "
            "condition: the one-coloured set must be large, meaning it has at least as many elements as its "
            "smallest element. <bookmark mark='c'/>The strengthened statement is still true; it follows from "
            "Ramsey's theorem for infinite sets. But PA cannot prove it. The N it requires grows faster than any "
            "function that PA can prove is defined everywhere, the way Goodstein's sequences outrun every function "
            "PA knows."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(fin))
            vo.wait_until("b")
            self.play(FadeIn(plus))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.5))
        self.clear_scene()

    def more(self):
        head = label(r"A growing list", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"Goodstein's theorem; \ the hydra", r"Kirby \& Paris 1982", r"not in PA"),
                (r"the Paris--Harrington principle", r"Paris \& Harrington 1977", r"not in PA"),
                (r"Kruskal's tree theorem, \ finite form", r"Friedman 1980s", r"not in $\mathrm{ATR}_0$"),
                (r"$\mathrm{TREE}(3)$ is finite", r"Friedman", r"a number beyond imagining"),
                (r"the graph minor theorem", r"Robertson \& Seymour 2004", r"not in $\Pi^1_1\text{-CA}_0$")]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.6 - 0.78 * i
            la = label(a, font_size=25)
            lb = label(b, font_size=22, color=GREY_B)
            lc = label(c, font_size=24, color=BAD)
            la.move_to([-6.2 + la.width / 2, y, 0])
            lb.move_to([0.4 + lb.width / 2, y, 0])
            lc.move_to([3.9 + lc.width / 2, y, 0])
            tab.add(VGroup(la, lb, lc))
        moral = label(r"incompleteness is not a curiosity: \ it reaches ordinary combinatorics", font_size=26,
                      color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The list has grown. <bookmark mark='a'/>Goodstein and the hydra, from Part 6. The Paris-Harrington "
            "principle. <bookmark mark='b'/>Harvey Friedman showed that a finite form of Kruskal's theorem about "
            "trees cannot be proved even in much stronger systems, and it yields a number, TREE of three, so large "
            "that Graham's number is nothing beside it. <bookmark mark='c'/>The graph minor theorem of Neil "
            "Robertson and Paul Seymour, a pillar of modern graph theory, is unprovable in a still stronger system. "
            "<bookmark mark='d'/>Incompleteness reaches ordinary combinatorics. And in every case the proof that the "
            "statement is true uses infinite objects, or ordinals beyond what the weaker system can reach."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
