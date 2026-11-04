from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


class BeforeAxioms(VoiceoverScene):
    def construct(self):
        self.card()
        self.cardano()
        self.galileo()
        self.histogram()
        self.mere()
        self.huygens()

    def card(self):
        card = chapter_card(1, r"Before the axioms", r"Equally likely cases, and the art of counting them",
                            lit=(1654,), part=PART)
        with self.voiceover("Chapter one. Before the axioms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cardano(self):
        ring = VGroup(*[die_face(v, 0.8) for v in range(1, 7)])
        for k, f in enumerate(ring):
            ang = PI / 2 - k * TAU / 6
            f.move_to([-3.6 + 1.7 * np.cos(ang), 0.1 + 1.7 * np.sin(ang), 0])
        circ = Circle(radius=1.7, stroke_color=GREY_D, stroke_width=1.5).move_to([-3.6, 0.1, 0])
        cap = label(r"Cardano's \emph{circuit}: \ every way the throw can go", font_size=26, color=GREY_A)
        cap.next_to(circ, DOWN, buff=0.7)
        hc = history_card(r"c.\,1564", r"Gerolamo Cardano: \ physician, \ mathematician, \ gambler",
                          r"\emph{Liber de ludo aleae}, \ the Book on Games of Chance; \ printed in 1663, a century "
                          r"after he wrote it", color=S.MUSEUM, width=5.6, font_size=23).move_to([3.4, 1.6, 0])
        dfn = definition_card(r"Classical probability", r"if the outcomes are \emph{equally likely}, \ "
                              r"$P(A) = \dfrac{\text{outcomes in } A}{\text{all outcomes}} = \dfrac{|A|}{|\Omega|}$",
                              color=EXACT, width=5.6, font_size=24).move_to([3.4, -1.6, 0])
        with self.voiceover(
            "Pascal and Fermat didn't start from nothing. <bookmark mark='a'/> About ninety years earlier, Gerolamo Cardano, "
            "a physician, a mathematician and a compulsive gambler, wrote a little Book on Games of Chance. It sat "
            "unpublished for a hundred years. <bookmark mark='b'/> Cardano's idea was the circuit: list every way a "
            "throw can go. One die has six. If they're equally likely, the fair odds of an event are just the number "
            "of ways it can happen against the number it can't. <bookmark mark='c'/> Say it as a fraction and you "
            "have the classical definition, the one Laplace would make famous: the probability of an event is the "
            "number of outcomes in it over the number of outcomes in all, provided every outcome is equally likely. "
            "<bookmark mark='d'/> Everything rests on that proviso. It sounds harmless. It isn't."
        ) as vo:
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Create(circ), LaggedStart(*[FadeIn(f, scale=0.7) for f in ring], lag_ratio=0.2), FadeIn(cap))
            self.play(*[f[0].animate.set_fill(EVENT) for f in ring[4:]])
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(dfn, color=S.RESID, scale_factor=1.04))
        self.clear_scene()

    def galileo(self):
        d = load("galileo")
        cols = VGroup()
        tot_mobs = {}
        for s, color in ((9, PB), (10, PA)):
            rows = VGroup()
            for part, k in zip(d["parts"][str(s)], d["orders"][str(s)]):
                dice = dice_row(part, size=0.42)
                cnt = MathTex(rf"\times {k}", font_size=28, color=color)
                rows.add(VGroup(dice, cnt).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            head = label(rf"sum {s}: \ six ways", font_size=30, color=color).next_to(rows, UP, buff=0.35)
            tot = MathTex(rf"{sum(d['orders'][str(s)])}", r"\text{ of } 216", font_size=36, color=color)
            tot.next_to(rows, DOWN, buff=0.35)
            tot_mobs[s] = tot
            cols.add(VGroup(head, rows, tot))
        cols.arrange(RIGHT, buff=2.2, aligned_edge=UP).move_to([0.2, -0.3, 0])
        hc = history_card(r"c.\,1620", r"Galileo Galilei", r"\emph{On a discovery concerning dice}", color=S.MUSEUM,
                          width=4.6, font_size=22).to_corner(UL, buff=0.35)
        q = label(r"why does $10$ come up more often than $9$?", font_size=30).to_edge(UP, buff=0.5).shift(RIGHT * 1.8)
        key = label(r"the dice are \emph{distinguishable}: \ count \emph{ordered} triples", font_size=28,
                    color=S.ACCENT).to_edge(DOWN, buff=0.35)
        for c in cols:
            for r in c[1]:
                r[1].set_opacity(0)
            c[2].set_opacity(0)
        with self.voiceover(
            "Around 1620 someone put a question to Galileo. <bookmark mark='a'/> Gamblers playing with three dice "
            "had noticed that a total of ten comes up more often than a total of nine. But both totals can be made "
            "in exactly six ways. <bookmark mark='b'/> Nine is one-two-six, one-three-five, one-four-four, "
            "two-two-five, two-three-four, three-three-three. <bookmark mark='c'/> Ten is one-three-six, "
            "one-four-five, two-two-six, two-three-five, two-four-four, three-three-four. Six each. So why the "
            "difference? <bookmark mark='d'/> Galileo's answer: the six ways are not equally likely. The dice are "
            "three different objects, and the outcomes that are equally likely are the ordered triples, red then "
            "green then blue, six times six times six, two hundred and sixteen of them. <bookmark mark='e'/> "
            "One-two-six can come in six orders. One-four-four in only three: the odd die can be first, second or "
            "third. Three-three-three in only one. <bookmark mark='f'/> Count the orders, and nine has twenty-five "
            "of the two hundred and sixteen, while ten has twenty-seven."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(cols[0][0]), LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.1) for r in cols[0][1]],
                                                      lag_ratio=0.25), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cols[1][0]), LaggedStart(*[FadeIn(r[0], shift=RIGHT * 0.1) for r in cols[1][1]],
                                                      lag_ratio=0.25), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(key, shift=UP * 0.2))
            vo.wait_until("e")
            for c in cols:
                self.play(LaggedStart(*[r[1].animate.set_opacity(1) for r in c[1]], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("f")
            self.play(cols[0][2].animate.set_opacity(1), cols[1][2].animate.set_opacity(1))
            self.play(Indicate(cols[1][2], color=PA, scale_factor=1.2))
        self.clear_scene()

    def histogram(self):
        d = load("galileo")
        pmf = np.asarray(d["pmf3"])
        A = axes([2.5, 18.5], [0, 0.14], x_length=8.2, y_length=4.4, xlabel=r"the sum of three dice",
                 ylabel=r"probability", xticks=list(range(3, 19)), yticks=[0, 0.05, 0.1],
                 center=[-2.5, -0.4, 0])
        ax = A.ax
        bars = VGroup()
        for s, p in zip(range(3, 19), pmf):
            col = PA if s == 10 else PB if s == 9 else GREY_C
            bars.add(Rectangle(width=ax.c2p(0.8, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1],
                               stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(ax.c2p(s, p / 2)))
        engine = code_block(["three = die ** 3", "three.map(sum).P(9)    # 25/216", "three.map(sum).P(10)   # 27/216"],
                            font_size=20).to_corner(UR, buff=0.4)
        n = d["sim_n"]
        chk = VGroup(
            MathTex(rf"P(9) = \tfrac{{25}}{{216}} = {25 / 216:.4f}", font_size=30, color=PB),
            MathTex(rf"\text{{simulated}}\ \ {d['sim_9']:.4f}", font_size=26, color=SIM),
            MathTex(rf"P(10) = \tfrac{{27}}{{216}} = {27 / 216:.4f}", font_size=30, color=PA),
            MathTex(rf"\text{{simulated}}\ \ {d['sim_10']:.4f}", font_size=26, color=SIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.7, -0.6, 0])
        tag = note(rf"computed: exact, and {fmt_int(n)} simulated throws").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's the whole distribution of the total, all two hundred and sixteen ordered throws sorted by their "
            "sum. <bookmark mark='a'/> Ten and eleven are the peak; nine is a little lower. <bookmark mark='b'/> "
            "This is the first time we use the engine we're building. Three dice are a die to the third power, a "
            "product of three independent copies; map each triple to its sum, and ask for the probability of nine "
            "or ten. It answers with exact fractions. <bookmark mark='c'/> And a hundred thousand simulated throws "
            "agree, to about three decimals. The difference between nine and ten is two chances in two hundred and "
            "sixteen, less than one percent. To see it at the table, a gambler would have needed thousands of "
            "throws, and a good memory."
        ) as vo:
            self.play(FadeIn(A))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(bars[7], color=PA), Indicate(bars[6], color=PB))
            vo.wait_until("b")
            self.play(FadeIn(engine, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(chk, shift=LEFT * 0.2), FadeIn(tag))
        self.clear_scene()

    def mere(self):
        d = load("galileo")
        hc = history_card(1654, r"the Chevalier de M\'er\'e's two bets", r"Pascal to Fermat, \ 29 July 1654",
                          color=S.MUSEUM, width=5.2, font_size=22).to_corner(UL, buff=0.35)
        b1 = VGroup(label(r"Bet 1: \ at least one six in $4$ throws of one die", font_size=28),
                    MathTex(r"1 - \left(\tfrac56\right)^{4}", r"=", r"\tfrac{671}{1296}", rf"= {d['bet1_f']:.4f}",
                            font_size=34, color=EXACT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        b2 = VGroup(label(r"Bet 2: \ at least one double six in $24$ throws of two dice", font_size=28),
                    MathTex(r"1 - \left(\tfrac{35}{36}\right)^{24}", rf"= {d['bet2']:.4f}", font_size=34,
                            color=EXACT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bets = VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-2.6, 0.2, 0])
        reason = MathTex(r"\tfrac46", r"=", r"\tfrac{24}{36}", r"\quad\Rightarrow\quad \text{``the same odds''}",
                         font_size=32, color=GREY_A).next_to(bets, DOWN, buff=0.5).align_to(bets, LEFT)
        cross = Cross(reason, stroke_color=S.RESID, stroke_width=4)
        sims = VGroup(MathTex(rf"\text{{simulated}}\ {d['sim1']:.4f}", font_size=26, color=SIM).next_to(b1[1], RIGHT,
                                                                                                        buff=0.5),
                      MathTex(rf"\text{{simulated}}\ {d['sim2']:.4f}", font_size=26, color=SIM).next_to(b2[1], RIGHT,
                                                                                                        buff=0.5))
        # P(at least one double six in n throws)
        A = axes([0, 40], [0, 0.7], x_length=4.4, y_length=3.2, xlabel=r"throws of two dice, $n$",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 0.25, 0.5], center=[4.4, -1.2, 0])
        ax = A.ax
        ns = np.arange(0, 41)
        ps = 1 - (35 / 36) ** ns
        cv = curve(ax, ns, ps, EXACT, 3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(40, 0.5), color=GREY_B, stroke_width=2)
        mark = VGroup(Dot(ax.c2p(24, ps[24]), radius=0.06, color=S.RESID), Dot(ax.c2p(25, ps[25]), radius=0.06,
                                                                              color=S.KEPT))
        ml = label(rf"$24$: \ ${ps[24]:.3f}$ \quad $25$: \ ${ps[25]:.3f}$", font_size=22, color=GREY_A)
        ml.next_to(A, UP, buff=0.2)
        quote = label(r"``He has a very good mind, \ but he is not a geometer.'' \ \textemdash\ Pascal", font_size=26,
                      color=S.MUSEUM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Chevalier de Méré, the gambler who brought Pascal his problem, had a second puzzle. "
            f"<bookmark mark='a'/> He knew it paid to bet on getting at least one six in four throws of a die. The "
            "chance of no six in one throw is five sixths; in four independent throws, five sixths to the fourth; "
            f"so the chance of at least one six is one minus that, {d['bet1_f']:.4f}, a little better than even. "
            "<bookmark mark='b'/> He reasoned that a double six with two dice is six times rarer, so six times as "
            "many throws, twenty-four, should give the same odds: four out of six equals twenty-four out of "
            "thirty-six. <bookmark mark='c'/> But the same calculation gives one minus thirty-five thirty-sixths to "
            f"the twenty-fourth: {d['bet2']:.4f}. Worse than even. <bookmark mark='d'/> Simulation agrees on both. "
            "<bookmark mark='e'/> Probability doesn't scale like a proportion. The chance of at least one double "
            "six crosses one half between twenty-four throws and twenty-five. <bookmark mark='f'/> Pascal told "
            "Fermat that de Méré had a very good mind, but was not a geometer. Whether he really noticed the "
            "difference from his losses is doubtful; the edge is under one percent. But his argument was wrong, "
            "and the mistake, treating chances as if they added up in proportion, is still made every day."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(b1, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(b2[0], shift=RIGHT * 0.2), FadeIn(reason))
            vo.wait_until("c")
            self.play(Write(b2[1]), Create(cross))
            vo.wait_until("d")
            self.play(FadeIn(sims))
            vo.wait_until("e")
            self.play(FadeIn(A), Create(half))
            self.play(Create(cv), run_time=2.0)
            self.play(FadeIn(mark), FadeIn(ml))
            vo.wait_until("f")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()

    def huygens(self):
        hc = history_card(1657, r"Christiaan Huygens, \ \emph{De ratiociniis in ludo aleae}",
                          r"the first printed book on probability: \ fourteen propositions and five problems for "
                          r"the reader", color=S.MUSEUM, width=6.4, font_size=23).move_to([-3.3, 1.5, 0])
        th = theorem_card(r"the value of a chance", r"$p$ chances of winning $a$ and $q$ chances of winning $b$, "
                          r"all equally likely, \ are worth $\dfrac{p\,a + q\,b}{p + q}$", who=r"Huygens 1657, "
                          r"Proposition III", color=EXACT, width=6.4, font_size=24).move_to([3.4, -1.0, 0])
        ex = MathTex(r"(2,1):\quad", r"\frac{1 \cdot 64 + 1 \cdot 32}{2}", r"= 48", font_size=34).move_to([-3.3, -1.6, 0])
        ex[2].set_color(EXACT)
        take = label(r"classical probability counts equally likely cases. \ But which cases are equally likely?",
                     font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1657 the young Dutch scientist Christiaan Huygens, who had heard about the Paris problems on a visit "
            "but never seen the letters, worked out the theory for himself and published it: the first printed book "
            "on probability. <bookmark mark='a'/> Its central idea is what Pascal used for the stake. If you have p "
            "equally likely chances of winning a, and q of winning b, your chance is worth p a plus q b, over p plus "
            "q. <bookmark mark='b'/> At two to one, that's one chance of sixty-four and one of thirty-two: "
            "forty-eight. Huygens' book was the standard text for half a century; its last problem, about two "
            "players gambling until one is ruined, comes back when we study random walks. <bookmark mark='c'/> "
            "So far everything has rested on equally likely cases. Galileo had to think hard about which cases "
            "those were. Our next tool counts cases, and the chapter after it shows what happens when nobody can "
            "agree on which ones are equally likely."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(th, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Write(ex))
            vo.wait_until("c")
            self.play(FadeIn(take, shift=UP * 0.2))
        self.clear_scene()
