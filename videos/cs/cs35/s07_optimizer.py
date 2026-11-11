from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load, mono, num)


def big(v: int) -> str:
    if v >= 10 ** 9:
        return rf"{v / 1e12:.1f} \ trillion" if v >= 10 ** 12 else rf"{v / 1e9:.1f} \ billion"
    return num(v)


class Optimizer(VoiceoverScene):
    def construct(self):
        self.card()
        self.space()
        self.orders()
        self.dp()

    def card(self):
        card = chapter_card(6, r"The optimizer", r"How do you find the cheapest plan without trying them all?",
                            lit=(1979,), extra=((1979, r"Selinger et al.: \ System R's optimizer"),), part=PART)
        with self.voiceover("Chapter six. The optimizer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def space(self):
        o = load("optimizer")
        head = label(r"How many plans?", font_size=36).to_edge(UP, buff=0.3)
        chain = VGroup(*[box(0.9, 0.6, rf"\text{{{t}}}", c, font_size=22) for t, c in
                         zip("abcde", (DATA, HEAD, LAM, KERN, YES))]).arrange(RIGHT, buff=0.55)
        chain.next_to(head, DOWN, buff=0.45)
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), color=GREY_B) for i in range(4)])
        sizes = VGroup(*[label(rf"{num(o['sizes'][t])} rows", font_size=16, color=GREY_A).next_to(chain[i], DOWN,
                                                                                                  buff=0.1)
                         for i, t in enumerate("abcde")])
        ps = [r for r in o["plan_space"] if r["n"] in (2, 3, 4, 5, 6, 8, 10, 12)]
        tab = grid_table([r"tables", r"join orders \ (left-deep, $n!$)", r"join trees \ (bushy)",
                          r"subsets \ ($2^n$)"],
                         [[str(r["n"]), big(r["left_deep"]), big(r["bushy"]), num(r["subsets"])] for r in ps],
                         widths=[1.4, 3.4, 3.4, 2.2], row_h=0.36, font_size=18, mono_cols=())
        tab.next_to(sizes, DOWN, buff=0.4).set_x(0)
        for r in range(1, len(ps) + 1):
            tab.cells[r][3].set_color(YES)
            tab.cells[r][1].set_color(NO)
        lines = VGroup(
            label(r"and each join can use one of four algorithms, \ each table an index or a scan", font_size=19,
                  color=WHITE),
            label(r"the number of plans grows faster than exponentially; \ the number of \textit{subsets} only "
                  r"exponentially", font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.12).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "Here is a query that joins five tables in a chain, a to b to c to d to e, with sizes from fifty rows to "
            "thirty thousand, asking for the rows of a with small ids. <bookmark mark='a'/> Joins can be done in any "
            "order. Joining one table at a time, five tables can be ordered a hundred and twenty ways; allowing "
            "joins of joins, sixteen hundred and eighty. With twelve tables, which real queries reach, there are half "
            "a billion orders, and twenty-eight trillion trees. <bookmark mark='b'/> And each join has four "
            "algorithms, and each table may have indexes. Nobody can try them all. <bookmark mark='c'/> But look at "
            "the last column: the number of subsets of the tables grows far more slowly. That is the key to the "
            "solution."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chain), FadeIn(links), FadeIn(sizes))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), *[Indicate(tab.cells[r][3], color=YES) for r in range(1, len(ps) + 1)])
        self.wait(0.3)
        self.clear_scene()

    def orders(self):
        o = load("optimizer")
        od = o["orders"]
        head = label(r"Order matters: \ the 120 orders, \ with hash joins", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 3, 1], y_range=[3, 8, 1], x_length=6.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.6, -0.4, 0])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.12)
                      for k in range(3, 9)])
        yl = label(r"pages", font_size=18, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        bars = VGroup()
        for k, (nm, c) in enumerate((("best", YES), ("median", HEAD), ("worst", NO))):
            v = od[nm]["cost"]
            top = ax.c2p(k + 0.5, np.log10(v))
            bot = ax.c2p(k + 0.5, 3)
            b = Rectangle(width=1.1, height=top[1] - bot[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([(top[0]), (top[1] + bot[1]) / 2, 0])
            t = label(num(v), font_size=18, color=c).next_to(b, UP, buff=0.08)
            n = VGroup(label(nm, font_size=18, color=GREY_A),
                       mono(" ".join(od[nm]["order"]), 16, CODE)).arrange(DOWN, buff=0.06).next_to(bot, DOWN,
                                                                                               buff=0.12)
            bars.add(VGroup(b, t, n))
        lines = VGroup(
            label(r"same query, \ same answer", font_size=22, color=WHITE),
            label(r"best: \ start from \textit{a}'s ten rows, \\ grow along the chain", font_size=22, color=YES),
            label(r"worst: \ \textit{b} and \textit{d} share no condition, \\ so joining them first is a cross "
                  r"product \\ of 600 million pairs", font_size=22, color=NO),
            label(rf"a factor of {od['worst']['cost'] / od['best']['cost']:,.0f} \\ between best and worst",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax, RIGHT, buff=0.9)
        with self.voiceover(
            "Does the order matter? We can cost all hundred and twenty left-deep orders of our five tables, using hash "
            "joins throughout. <bookmark mark='a'/> They all compute the same count. <bookmark mark='b'/> The best "
            "starts with the ten rows of a that pass the filter, and grows along the chain, keeping intermediate "
            "results small: twenty-three hundred pages. The median order costs twenty times as much. "
            "<bookmark mark='c'/> The worst starts with b and d, which no condition connects, so the first join is a "
            "cross product, six hundred million pairs. <bookmark mark='d'/> Between the best and the worst is a factor "
            "of ten thousand. Choosing the order is the optimizer's most important decision."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), FadeIn(lines[1]))
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def dp(self):
        o = load("optimizer")
        head = label(r"Selinger's dynamic programming", font_size=36).to_edge(UP, buff=0.3)
        tables = "abcde"
        levels = VGroup()
        for k in range(1, 6):
            subs = ["".join(tables[i:i + k]) for i in range(0, 6 - k)]
            row = VGroup(*[box(0.42 * k + 0.5, 0.5, rf"\text{{{s}}}", [DATA, HEAD, LAM, KERN, YES][k - 1],
                               font_size=18) for s in subs]).arrange(RIGHT, buff=0.18)
            levels.add(row)
        levels.arrange(UP, buff=0.32).move_to([-2.7, 0.1, 0])
        lv = VGroup(*[label(rf"{k} table{'s' if k > 1 else ''}", font_size=16, color=GREY_B).next_to(levels[k - 1],
                                                                                                    LEFT, buff=0.25)
                      for k in range(1, 6)])
        pts = VGroup(
            label(r"for every connected subset, \ smallest first, \\ keep only its \textbf{cheapest} plan",
                  font_size=20, color=WHITE),
            label(r"a plan for $S$ = the best plan for $S - \{t\}$, \ joined to $t$: \\ try each $t$ and each "
                  r"algorithm", font_size=20, color=HEAD),
            label(r"principle of optimality: \ a best plan is built \\ from best sub-plans \ (Part 19)",
                  font_size=20, color=YES),
            label(r"also keep the best plan for each useful \textbf{order}: \\ a sorted result can make a later "
                  r"merge join \\ or ORDER BY free \ (Selinger's \textit{interesting orders})", font_size=20,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
        ex = VGroup(*[mono(ln.split("   (")[0], 13, CODE) for ln in o["explain"].splitlines()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04)
        ex.next_to(pts, DOWN, buff=0.35).align_to(pts, LEFT)
        res = label(rf"{o['dp_considered']} plans costed, \ against {num(o['ex_considered'])} \\ for exhaustive "
                    rf"search; \ both find cost {o['best_cost']:.0f}", font_size=21, color=YES)
        res.next_to(levels, DOWN, buff=0.35)
        with self.voiceover(
            "Patricia Selinger's team at IBM found the method in 1979, for System R, and nearly every optimizer since "
            "descends from it. <bookmark mark='a'/> Work up from small sets of tables to large. For each set, keep only "
            "the cheapest plan that joins exactly those tables. <bookmark mark='b'/> To plan a set of tables, take "
            "away one table, look up the best plan for the rest, which is already known, and join the table back "
            "on, with every algorithm; keep the best result. <bookmark mark='c'/> This is dynamic programming, from "
            "Part 19, and it works because the best plan for a set is built from the best plans for its parts. "
            "<bookmark mark='d'/> One refinement: a more expensive sub-plan may be worth keeping if its output is "
            "sorted, because a later merge join or ORDER BY gets the order for free. Selinger called these interesting "
            "orders. <bookmark mark='e'/> Our database's optimizer does this. It costed 395 plans, where trying "
            "every order and algorithm costs twelve hundred, and found the same plan: start with a's ten rows, join "
            "along the chain. With more tables the gap becomes astronomical."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in levels], lag_ratio=0.3), FadeIn(lv), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), Indicate(levels[3][0], color=HEAD), Indicate(levels[4][0], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
            vo.wait_until("e")
            self.play(FadeIn(ex), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()


_ = (KERN, LAM)
