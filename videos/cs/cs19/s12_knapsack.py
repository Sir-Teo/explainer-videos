from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Knapsack(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.greedy()
        self.pseudo()

    def card(self):
        card = chapter_card(11, r"Knapsack, \ and pseudo-polynomial time", r"When is $O(nW)$ not polynomial?",
                            lit=(1957,), extra=((1957, r"Dantzig"), (1975, r"Ibarra and Kim")), part=PART)
        with self.voiceover("Chapter eleven. Knapsack, and pseudo-polynomial time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def table(self):
        d = load("knapsack")
        items, W = d["items"], d["W"]
        head = label(rf"Six items, \ capacity {W}", font_size=34).to_edge(UP, buff=0.3)
        n = len(items)
        V = [[0] * (W + 1) for _ in range(n + 1)]
        for i, (w, v) in enumerate(items, 1):
            for c in range(W + 1):
                V[i][c] = V[i - 1][c] if w > c else max(V[i - 1][c], V[i - 1][c - w] + v)
        cw, ch = 0.5, 0.42
        x0, y0 = -5.3, 2.2
        cells = {}
        for i in range(n + 1):
            for c in range(W + 1):
                val = V[i][c]
                sq = Rectangle(width=0.46, height=0.38, stroke_color=GREY_D, stroke_width=1, fill_color=YES,
                               fill_opacity=0.08 + 0.6 * val / V[n][W]).move_to([x0 + cw * c, y0 - ch * i, 0])
                cells[(i, c)] = VGroup(sq, mono(str(val), 13, WHITE).move_to(sq))
        colh = VGroup(*[mono(str(c), 13, GREY_B).move_to([x0 + cw * c, y0 + 0.42, 0]) for c in range(W + 1)])
        rowh = VGroup(*[label(rf"$w{{=}}{w}, \ v{{=}}{v}$", font_size=15, color=DATA).move_to(
            [x0 - 1.05, y0 - ch * (i + 1), 0]) for i, (w, v) in enumerate(items)])
        cap = label(r"capacity $c \to$", font_size=16, color=GREY_B).next_to(colh, LEFT, buff=0.3)
        rows = [VGroup(*[cells[(i, c)] for c in range(W + 1)]) for i in range(n + 1)]
        chosen = set(d["chosen"])
        trace, c = [], W
        for i in range(n, 0, -1):
            if V[i][c] != V[i - 1][c]:
                trace.append((i, c))
                c -= items[i - 1][0]
        hl = VGroup(*[SurroundingRectangle(cells[p], buff=0.02, color=HEAD, stroke_width=3) for p in trace])
        rec = MathTex(r"V(i, c) = \max\bigl(V(i-1, c),\ V(i-1, c - w_i) + v_i\bigr)", font_size=30,
                      color=LAM).to_edge(DOWN, buff=0.9)
        res = label(rf"best value {d['best']}: \ items of weight " + ", \\ ".join(str(items[k][0]) for k in
                                                                                   sorted(chosen)) +
                    rf" \ (total {sum(items[k][0] for k in chosen)})", font_size=22, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A thief with a knapsack that holds twelve kilograms faces six items, each with a weight and a value. "
            "<bookmark mark='a'/> The subproblem: the best value using only the first i items with capacity c. "
            "Either item i is left out, or it is taken, using up its weight. <bookmark mark='b'/> The table fills "
            "one item at a time; each row needs only the row above. <bookmark mark='c'/> The bottom-right cell is "
            "the answer, a hundred and ten, and tracing back through the cells where the value changed finds the "
            "items: weights three, two and seven, exactly filling the knapsack."
        ) as vo:
            self.play(FadeIn(head), FadeIn(colh), FadeIn(rowh), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rec))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def greedy(self):
        d = load("knapsack")
        head = label(r"Greedy by value per kilogram", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"take items in order of value per unit weight, \ while they fit", font_size=23, color=GREY_A),
            label(rf"on the six items: \ {d['greedy']}, \ against the best {d['best']}", font_size=23, color=NO),
            label(rf"on {d['trials']} random sets of 15 items: \ wrong {d['greedy_worse']} times, \ "
                  rf"once down to {100 * d['greedy_worst']:.0f}\% of the best", font_size=22, color=NO),
            label(r"0/1 choices are not a matroid; \ \textit{fractional} knapsack, \ where items can be cut, \ is "
                  r"solved exactly by this greedy", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.8)
        with self.voiceover(
            "Why not be greedy? <bookmark mark='a'/> Take items in order of value per kilogram, as long as they "
            "fit. <bookmark mark='b'/> On our six items that gives a hundred and five, not a hundred and ten. "
            "<bookmark mark='c'/> On five hundred random sets of fifteen items it was wrong two times in five, "
            "once getting only seventy-eight percent of the best value. <bookmark mark='d'/> The independent sets "
            "here are not a matroid. If items could be cut, like gold dust, the same greedy would be exactly "
            "right: the fractional knapsack is a different, easier problem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def pseudo(self):
        d = load("knapsack")
        head = label(r"$O(nW)$ is not polynomial", font_size=34).to_edge(UP, buff=0.3)
        rows = [[f"{r['W']:,}", str(r["bits"]), f"{r['cells']:,}",
                 f"{r['s'] * 1000:.1f} ms" if r["s"] < 1 else f"{r['s']:.2f} s", str(r["best"])] for r in d["scale"]]
        tab = grid_table([r"capacity $W$", r"bits of $W$", r"table cells", r"time", r"best value"], rows,
                         widths=[2.6, 1.8, 2.8, 2.0, 2.0], row_h=0.48, font_size=20,
                         colors=[[WHITE, HEAD, GREY_A, NO, YES]] * len(rows)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"the same twenty items, \ weights and capacity multiplied by 10, \ 100, \ \ldots: \ the same "
                  r"answer every time", font_size=21, color=GREY_A),
            label(r"input size grows by about 3 bits per step; \ the work grows tenfold: \ exponential in the input",
                  font_size=21, color=NO),
            label(r"\textbf{pseudo-polynomial}: \ polynomial in the \textit{value} of $W$, \ not its length",
                  font_size=22, color=HEAD),
            label(r"0/1 knapsack is NP-hard \ (Karp, \ 1972; \ Part 26); \ but within $1 + \varepsilon$ of optimal "
                  r"in polynomial time \ (Ibarra and Kim, \ 1975)", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The table has n times W cells, which sounds polynomial. It is not. <bookmark mark='a'/> Here are the "
            "same twenty items five times over, with every weight and the capacity multiplied by ten each time. "
            "The problem and its answer never change. <bookmark mark='b'/> But each step adds about three bits to "
            "the input and multiplies the work by ten: from a third of a millisecond to nearly five seconds. Time "
            "proportional to the capacity is exponential in the number of digits used to write it. <bookmark "
            "mark='c'/> Such an algorithm is called pseudo-polynomial: fast when the numbers are small. <bookmark "
            "mark='d'/> No truly polynomial algorithm is known, and Richard Karp proved in 1972 that none exists "
            "unless P equals NP, the subject of Part 26. Yet Oscar Ibarra and Chul Kim showed in 1975 that a "
            "solution within any fixed percentage of the best can be found in polynomial time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
