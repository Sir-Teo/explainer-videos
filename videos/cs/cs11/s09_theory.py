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
        thm = label("stationary coalescing heap, uniform frees: $M \\approx \\tfrac12 p N$ holes",
                    font_size=24, color=HEAD).next_to(head, DOWN, buff=0.3)
        sub = note("$p$: chance of splitting a hole; \\\\ simplified model neglects boundaries and heap growth", font_size=18).next_to(
            thm, DOWN, buff=0.1)
        steps = VGroup(
            label(r"call a block in use \textit{A}, \ \textit{B} or \textit{C} if 0, \ 1 or 2 of its neighbours are "
                  r"free", font_size=21, color=GREY_A),
            label(r"each hole has two neighbours in use: \ $2M = B + 2C$, \ so $M = C + B/2$", font_size=21,
                  color=DATA),
            label(r"freeing an \textit{A} makes a hole; \ a \textit{C}, \ merges two into one; \ a \textit{B}, \ "
                  r"neither", font_size=21, color=GREY_A),
            label(r"an allocation removes a hole with probability $1 - p$", font_size=21, color=GREY_A),
            label("expected balance: $A-C \\approx (1-p)N$; hence $M \\approx \\tfrac12 pN$", font_size=22, color=YES),
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
        with self.voiceover("Knuth's fifty-percent rule is a statistical balance argument under specific assumptions. <bookmark mark='a'/> Consider a roughly stationary, coalescing heap with N live blocks and uniformly selected frees. Let p be the probability that allocation splits an existing free hole. Ignore boundary and heap-growth corrections in this simplified derivation. <bookmark mark='b'/> Classify live blocks as A, B or C when zero, one or two neighbors are free. <bookmark mark='c'/> For interior holes, counting neighboring live blocks gives twice M equals B plus two C. <bookmark mark='d'/> A uniformly selected free creates a hole with probability A over N and removes one with probability C over N. Freeing B changes neither count. <bookmark mark='e'/> If allocation consumes an entire existing hole with probability one minus p, it removes that hole. <bookmark mark='f'/> Stationary expected gains and losses therefore give A minus C approximately equal to one minus p times N, and M approximately one half p N. This counts holes, not their total bytes, and is not a worst-case guarantee for arbitrary workloads.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(thm), FadeIn(sub), FadeIn(strip), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(steps[0], shift=RIGHT * 0.1))
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.15))
            vo.wait_until('c')
            self.play(FadeIn(steps[1], shift=RIGHT * 0.1), FadeIn(count))
            for mk, s in zip('def', steps[2:]):
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
        punch = label("close agreement on this workload; holes are counts, not free bytes", font_size=24,
                      color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "The simulation tests whether this approximation is useful for a specified workload. <bookmark "
            "mark='a'/> We hold 200, 1,000 or 3,000 live blocks, repeatedly free one uniformly at random and "
            "allocate a uniformly chosen size from sixteen through two thousand bytes. Hole counts are averaged "
            "after warm-up; the recorded p includes the full run. <bookmark mark='b'/> The displayed "
            "holes-per-block ratios are close to p over two, with small differences from finite sampling, "
            "boundaries and heap growth. Agreement on this workload supports this approximation here. It neither "
            "validates arbitrary lifetime correlations nor predicts how many bytes those holes occupy."
        )
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
        head = label("An adversarial trace and the worst-case question", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 7.5, 1], y_range=[0, 5, 1], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xt = VGroup(*[label(rf"{32 * 2 ** k}", font_size=14, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(8)])
        yt = VGroup(*[label(rf"{v}M", font_size=14, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in range(1, 6)])
        xl = label(r"largest block so far \ (bytes)", font_size=16, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        bound = ax.plot(lambda k: 1 + k / 2, x_range=[0, 7], color=HEAD, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(r["phase"], r["heap_over_M"]), radius=0.08, color=NO) for r in rows])
        bl = label("reference: $M(1+\\tfrac12\\log_2 n)$", font_size=20, color=HEAD).next_to(ax.c2p(4, 3.0), UL,
                                                                                            buff=0.1)
        side = VGroup(
            label(r"the adversary, \ in phases:", font_size=20, color=GREY_A),
            label(r"fill the heap with blocks of size $s$, \\ up to $M$ bytes live", font_size=19, color=GREY_A),
            label(r"free half of them, \ choosing so \\ no hole of $2s$ remains", font_size=19, color=GREY_A),
            label(r"double $s$: \ every new block \\ needs fresh memory", font_size=19, color=GREY_A),
            label("first fit, simulated: \\\\ matches this reference trace", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.7)
        punch = label("$n =$ largest / smallest block; \\\\ this replay is not a proof against all allocators",
                      font_size=21, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover("Average-case balance does not prevent bad allocation sequences. <bookmark mark='a'/> Robson's classical lower bounds concern online, nonmoving allocation with a bound M on simultaneously live storage and a largest-to-smallest block-size ratio n. The leading growth is proportional to M log n; exact constants and finite corrections depend on the theorem's model. The plotted one plus half log base two n is our illustrative reference curve. <bookmark mark='b'/> Our constructed trace fills with small blocks, frees selected blocks while keeping holes too small for the next size, then doubles that size. <bookmark mark='c'/> On the implemented first-fit and best-fit policies, the measured heap follows this curve: from M to four and a half M as total block size grows from 32 to 4,096 bytes, so n is 128. This finite replay is not a proof against every allocator. <bookmark mark='d'/> The general impossibility result needs a strategy-dependent adversary and its proof. Moving objects, restricting lifetimes or changing the allocation model changes the assumptions. A compacting collector must also find or redirect references safely.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(bound), FadeIn(bl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(s) for s in side[:4]], lag_ratio=0.4), run_time=3)
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.2), FadeIn(side[4]))
            vo.wait_until('d')
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
