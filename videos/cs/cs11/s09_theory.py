from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, grid_table, load)


class Theory(VoiceoverScene):
    def construct(self):
        self.card()
        self.fifty()
        self.checked()
        self.robson()

    def card(self):
        card = chapter_card(8, r"Knuth's rule \ and Robson's bound", r"How badly can a heap fragment?",
                            lit=(1968, 1971), extra=((1968, r"Knuth: \ the fifty-percent rule"),
                                                     (1971, r"Robson: \ worst-case bounds")), part=PART)
        with self.voiceover("Chapter eight. Knuth's rule and Robson's bound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fifty(self):
        head = label(r"The fifty-percent rule \ (Knuth, \ 1968)", font_size=34).to_edge(UP, buff=0.3)
        thm = label(r"in equilibrium, \ with $N$ blocks in use, \ there are about $\tfrac12 p N$ free holes",
                    font_size=24, color=HEAD).next_to(head, DOWN, buff=0.3)
        sub = note(r"$p$: \ the chance that an allocation does not use up its hole exactly", font_size=18).next_to(
            thm, DOWN, buff=0.1)
        steps = VGroup(
            label(r"call a block in use \textit{A}, \ \textit{B} or \textit{C} if 0, \ 1 or 2 of its neighbours are "
                  r"free", font_size=21, color=GREY_A),
            label(r"each hole has two neighbours in use: \ $2M = B + 2C$, \ so $M = C + B/2$", font_size=21,
                  color=DATA),
            label(r"freeing an \textit{A} makes a hole; \ a \textit{C}, \ merges two into one; \ a \textit{B}, \ "
                  r"neither", font_size=21, color=GREY_A),
            label(r"an allocation removes a hole with probability $1 - p$", font_size=21, color=GREY_A),
            label(r"equilibrium: \ $A - C = (1 - p) N$, \ so $M = \tfrac12 (N - A + C) = \tfrac12 p N$. "
                  r"\quad $\blacksquare$", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(sub, DOWN, buff=0.35)
        pattern = "UHUUUHUHUU"
        strip = VGroup()
        for k, ch in enumerate(pattern):
            w = 1.0 if ch == "U" else 0.8
            strip.add(Rectangle(width=w, height=0.6, stroke_color=GREY_B, stroke_width=1.2,
                                fill_color=DATA if ch == "U" else GREY_E, fill_opacity=0.45 if ch == "U" else 0.2))
        strip.arrange(RIGHT, buff=0).to_edge(DOWN, buff=1.0)
        kinds = VGroup()
        cols = {"A": GREY_A, "B": CTRL, "C": NO}
        for k, ch in enumerate(pattern):
            if ch == "H":
                kinds.add(label(r"hole", font_size=16, color=GREY_B).move_to(strip[k]))
                continue
            free = sum(1 for j in (k - 1, k + 1) if 0 <= j < len(pattern) and pattern[j] == "H")
            kk = "ABC"[free]
            kinds.add(label(rf"\textit{{{kk}}}", font_size=24, color=cols[kk]).move_to(strip[k]))
        count = label(r"here: \ $M = 3$, \ $B = 4$, \ $C = 1$: \ $2 \cdot 3 = 4 + 2 \cdot 1$", font_size=20,
                      color=DATA).next_to(strip, DOWN, buff=0.2)
        with self.voiceover(
            "How many holes does a heap have? Knuth found a law, in 1968. <bookmark mark='a'/> In a heap that has "
            "settled into equilibrium, with N blocks in use, there are about one half p times N free holes, where p "
            "is the chance that an allocation does not use up its hole exactly. Since p is usually near one, about "
            "half as many holes as blocks. The proof is a counting argument. <bookmark mark='b'/> Classify the "
            "blocks in use by how many of their two neighbours are free: none, one, or two. <bookmark mark='c'/> "
            "Each hole sits between two blocks in use, because neighbouring holes would have been merged, so twice "
            "the number of holes equals B plus two C. <bookmark mark='d'/> Now ask how holes come and go. Freeing an "
            "A-block makes a new hole; freeing a C-block merges two holes and its own space into one; freeing a "
            "B-block just extends a hole. <bookmark mark='e'/> And an allocation removes a hole only when it uses it "
            "up exactly. <bookmark mark='f'/> In equilibrium the gains and losses balance, which says A minus C "
            "equals one minus p, times N. Substitute, and the holes come to one half p N."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(steps[0], shift=RIGHT * 0.1), FadeIn(strip))
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(steps[1], shift=RIGHT * 0.1), FadeIn(count))
            for mk, s in zip("def", steps[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def checked(self):
        f = load("fifty")
        head = label(r"Checked by simulation: \ first fit", font_size=34).to_edge(UP, buff=0.35)
        body = [[f"{r['N']:,}", f"{r['holes']:.0f}", f"{r['ratio']:.3f}", f"{r['p']:.3f}", f"{r['p'] / 2:.3f}"]
                for r in f["rows"]]
        t = grid_table([r"blocks $N$", r"holes", r"holes $/ N$", r"measured $p$", r"$p / 2$"], body,
                       [2.2, 1.8, 2.2, 2.4, 1.8], row_h=0.6, font_size=24,
                       colors=[[GREY_A, GREY_A, YES, CTRL, HEAD]] * 3, mono_cols=()).move_to(UP * 0.2)
        cap = note(rf"each step frees a random block and allocates one of {f['sizes'][0]} to {f['sizes'][1]} bytes; "
                   r"averages over 30,000 steps after a warm-up", font_size=17).next_to(t, DOWN, buff=0.4)
        punch = label(r"to three decimal places: \ the rule is exact enough to plan with", font_size=24,
                      color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "We checked it. <bookmark mark='a'/> A first-fit heap with two hundred, a thousand and three thousand "
            "blocks in use; at every step a random block is freed and a new one of random size allocated. We count "
            "the holes, and measure p by counting how often an allocation split its hole rather than using it up. "
            "<bookmark mark='b'/> Holes per block, against one half of p: point four three eight against point four "
            "three five; point three nine nine against point four oh one; point three eight three against point "
            "three eight three. The rule is exact enough to plan with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), FadeIn(cap))
            vo.wait_until("a")
            for r in (1, 2, 3):
                self.play(FadeIn(VGroup(*t.cells[r][:4])), run_time=0.7)
            vo.wait_until("b")
            self.play(*[FadeIn(t.cells[r][4]) for r in (1, 2, 3)], FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    def robson(self):
        rb = load("robson")
        rows = rb["first_fit"]
        head = label(r"The worst case \ (Robson, \ 1971 and 1974)", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 7.5, 1], y_range=[0, 5, 1], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xt = VGroup(*[label(rf"{32 * 2 ** k}", font_size=14, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(8)])
        yt = VGroup(*[label(rf"{v}M", font_size=14, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in range(1, 6)])
        xl = label(r"largest block so far \ (bytes)", font_size=16, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        bound = ax.plot(lambda k: 1 + k / 2, x_range=[0, 7], color=HEAD, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(r["phase"], r["heap_over_M"]), radius=0.08, color=NO) for r in rows])
        bl = label(r"Robson: \ $M (\tfrac12 \log_2 n + 1)$", font_size=20, color=HEAD).next_to(ax.c2p(4, 3.0), UL,
                                                                                            buff=0.1)
        side = VGroup(
            label(r"the adversary, \ in phases:", font_size=20, color=GREY_A),
            label(r"fill the heap with blocks of size $s$, \\ up to $M$ bytes live", font_size=19, color=GREY_A),
            label(r"free half of them, \ choosing so \\ no hole of $2s$ remains", font_size=19, color=GREY_A),
            label(r"double $s$: \ every new block \\ needs fresh memory", font_size=19, color=GREY_A),
            label(r"first fit, \ simulated: \ exactly \\ on the bound", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.7)
        punch = label(r"no allocator that never moves blocks can do better: \ only compaction escapes \ (Part 15)",
                      font_size=21, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Knuth's rule describes the average heap. What about the worst? <bookmark mark='a'/> In 1971 and 1974 "
            "John Robson proved a sharp answer. If a program never has more than M bytes live, and no block bigger "
            "than n units, then for every allocator there is a program that forces it to use about M times one half "
            "log two n, plus one. <bookmark mark='b'/> The program is an adversary that watches where the allocator "
            "puts things. It fills memory with small blocks, then frees half of them, choosing which so that every "
            "hole is too small for the next, larger size. It doubles the size, and repeats. Each phase forces the "
            "allocator to take about M over two of fresh memory. <bookmark mark='c'/> We ran this adversary against "
            "our first-fit heap. The heap grows by half of M at each doubling, and the dots fall exactly on Robson's "
            "curve: four and a half M for blocks up to four kilobytes. <bookmark mark='d'/> The bound holds for any "
            "allocator that never moves a block. The only escape is to move them, compacting the heap, which needs "
            "to know where every pointer is: a garbage collector, Part 15."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(bound), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side[:4]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.2), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
