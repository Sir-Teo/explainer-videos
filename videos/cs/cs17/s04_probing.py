from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, slots, words)


class Probing(VoiceoverScene):
    def construct(self):
        self.card()
        self.linear()
        self.knuth()
        self.measured()
        self.robin()

    def card(self):
        card = chapter_card(3, r"Open addressing", r"Can the table itself hold the overflow?", lit=(1963,),
                            extra=((1963, r"Knuth: \ linear probing analysed"),), part=PART)
        with self.voiceover("Chapter three. Open addressing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def linear(self):
        d = load("probing")
        head = label(r"Linear probing: \ try the next slot", font_size=34).to_edge(UP, buff=0.3)
        snaps = d["snaps"]
        rows = VGroup()
        for s in snaps:
            sl = slots(s["slots"], w=0.17, h=0.42, color=DATA)
            lab = label(rf"{s['n']} keys", font_size=18, color=GREY_B).next_to(sl, LEFT, buff=0.25)
            cl = label(rf"longest cluster {s['clusters'][0]}", font_size=17, color=NO).next_to(sl, RIGHT, buff=0.25)
            rows.add(VGroup(lab, sl, cl))
        rows.arrange(DOWN, buff=0.3, aligned_edge=RIGHT).next_to(head, DOWN, buff=0.5)
        if rows.width > 13:
            rows.scale_to_fit_width(13)
        pts = VGroup(
            label(r"every key lives in the table: \ on a collision, \ probe $h, h+1, h+2, \ldots$ until a free slot",
                  font_size=21, color=GREY_A),
            label(r"one array, \ no pointers: \ the next probe is usually in the same cache line", font_size=21,
                  color=YES),
            label(r"but runs of full slots merge and grow: \ \textbf{primary clustering}", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Chains cost a pointer per key and a jump in memory per step. Open addressing keeps every key in the "
            "table itself. <bookmark mark='a'/> On a collision, linear probing tries the next slot, and the next, "
            "until it finds a free one; a find follows the same path until it finds the key or an empty slot. "
            "<bookmark mark='b'/> It is one array with no pointers, and the next probe is almost always in the "
            "same cache line, which is why it is so fast in practice. <bookmark mark='c'/> Its weakness is "
            "visible in these snapshots of a sixty-four-slot table filling up. Full slots form runs, and a key "
            "that lands anywhere in a run joins its end, so long runs grow faster than short ones and merge. "
            "This is primary clustering."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def knuth(self):
        head = label(r"Knuth's first analysis of an algorithm \ (1963)", font_size=34).to_edge(UP, buff=0.3)
        f = VGroup(
            MathTex(r"\text{successful search: } \ \tfrac12\Bigl(1 + \frac{1}{1-\alpha}\Bigr)", font_size=36,
                    color=YES),
            MathTex(r"\text{unsuccessful search, or insert: } \ \tfrac12\Bigl(1 + \frac{1}{(1-\alpha)^2}\Bigr)",
                    font_size=36, color=NO),
            MathTex(r"\text{uniform probing, for comparison: } \ \frac{1}{1-\alpha}", font_size=32, color=GREY_A),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"at $\alpha = \tfrac12$: \ 1.5 and 2.5 probes; \ at $\alpha = 0.9$: \ 5.5 and 50.5", font_size=22,
                  color=HEAD),
            label(r"the square is the price of clustering: \ near full, \ linear probing degrades much faster",
                  font_size=22, color=GREY_A),
            label(r"Knuth wrote it up in 1963, \ his first analysis of an algorithm; \ such analysis became a "
                  r"theme of \textit{The Art of Computer Programming}", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(f, DOWN, buff=0.55)
        with self.voiceover(
            "How bad is clustering? Donald Knuth worked it out in 1963, in a note he later called his first "
            "analysis of an algorithm. <bookmark mark='a'/> A successful search costs on average one half of one "
            "plus one over one minus alpha probes. <bookmark mark='b'/> An unsuccessful search, which is also the "
            "cost of an insert, costs one half of one plus one over one minus alpha, squared. <bookmark mark='c'/> "
            "Compare uniform probing, where every key follows its own random sequence of slots: one over one "
            "minus alpha. <bookmark mark='d'/> At half full, linear probing costs one and a half and two and a "
            "half probes. At ninety percent full, an insert costs fifty. <bookmark mark='e'/> The square is the "
            "price of clustering. Keep the table at most half to three quarters full, and linear probing is "
            "both simple and fast."
        ) as vo:
            self.play(FadeIn(head))
            for mk, x in zip("abc", f):
                vo.wait_until(mk)
                self.play(FadeIn(x))
            vo.wait_until("d")
            self.play(FadeIn(pts[0]))
            vo.wait_until("e")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("probing")
        rows = [r for r in d["rows"] if r["alpha"] <= 0.9]
        head = label(rf"Measured: \ a table of {words(d['m'])} slots", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 0.95, 0.1], y_range=[0, np.log10(60), 0.5], x_length=6.6, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)

        def curve(key, color, dash=False):
            pts = [ax.c2p(r["alpha"], np.log10(r[key])) for r in rows]
            if dash:
                return DashedVMobject(VMobject().set_points_smoothly(pts), num_dashes=30).set_color(color)
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.05, color=color) for p in pts])
        lm, lt = curve("linear_miss", NO), curve("knuth_miss", NO, dash=True)
        hm, ht = curve("linear_hit", YES), curve("knuth_hit", YES, dash=True)
        dm = curve("double_miss", LAM)
        xt = VGroup(*[label(f"{v:.1f}", font_size=15, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0.1, 0.3, 0.5, 0.7, 0.9)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, np.log10(v)), LEFT, buff=0.1)
                      for v, t in ((1, "1"), (3, "3"), (10, "10"), (30, "30"))])
        xl = label(r"load factor \ $\alpha$", font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label(r"probes, \ log scale", font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        key = VGroup(
            label(r"linear probing, \ insert: \ measured \ (dashed: \ Knuth)", font_size=19, color=NO),
            label(r"linear probing, \ successful find", font_size=19, color=YES),
            label(r"double hashing, \ insert: \ close to $1/(1-\alpha)$", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        r5 = next(r for r in rows if r["alpha"] == 0.5)
        r8 = next(r for r in rows if r["alpha"] == 0.8)
        nums = label(rf"at $\alpha = 0.5$: \ {r5['linear_miss']:.2f} \ (Knuth {r5['knuth_miss']:.2f}); \ "
                     rf"at $0.8$: \ {r8['linear_miss']:.1f} \ ({r8['knuth_miss']:.1f})", font_size=19,
                     color=GREY_A).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        with self.voiceover(
            "Does the formula hold? <bookmark mark='a'/> We filled a table of sixteen thousand slots to each load "
            "factor, with a random universal hash, and counted probes. The red curve is the cost of an insert, "
            "and the dashed curve under it is Knuth's formula. <bookmark mark='b'/> They agree closely up to "
            "about eighty percent; beyond that, a single long cluster dominates and the measurement becomes "
            "noisy, as the theory's variance predicts. <bookmark mark='c'/> Successful finds, in green, stay "
            "cheap much longer. <bookmark mark='d'/> Double hashing, which steps through the table by a second "
            "hash, breaks up clusters, and its inserts follow the uniform probing curve."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(lm), Create(lt), FadeIn(key[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(nums))
            vo.wait_until("c")
            self.play(Create(hm), Create(ht), FadeIn(key[1]))
            vo.wait_until("d")
            self.play(Create(dm), FadeIn(key[2]))
        self.wait(0.3)
        self.clear_scene()

    def robin(self):
        d = load("probing")
        r = next(x for x in d["rows"] if x["alpha"] == 0.9)
        head = label(r"Robin Hood hashing \ (Celis, \ 1986)", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"$\alpha = 0.9$", r"mean probes", r"variance", r"worst"], [
            [r"linear probing", f"{r['linear_mean']:.2f}", f"{r['linear_var']:.1f}",
             str(r["linear_max"] + 1)],
            [r"Robin Hood", f"{r['robin_mean']:.2f}", f"{r['robin_var']:.1f}", str(r["robin_max"] + 1)],
        ], widths=[3.6, 2.6, 2.4, 2.0], row_h=0.6, font_size=22, mono_cols=(),
            colors=[[NO, WHITE, NO, NO], [YES, WHITE, YES, YES]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"on a collision, \ the key farther from its home slot keeps the slot; \ the other moves on",
                  font_size=22, color=GREY_A),
            label(r"the same average, \ but the far-flung keys are pulled in: \ every find costs about the same",
                  font_size=22, color=YES),
            label(r"its descendants: \ Google's Swiss tables \ (2017) \ and Rust's \texttt{HashMap} probe 16 slots "
                  r"at once with SIMD", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.55)
        with self.voiceover(
            "One refinement changes not the average but the spread. <bookmark mark='a'/> In Robin Hood hashing, "
            "from Pedro Celis's 1986 thesis, when an inserted key meets a key that is closer to its own home slot, "
            "it takes the slot and the richer key moves on. <bookmark mark='b'/> At ninety percent full, the mean "
            "number of probes is the same as plain linear probing, but the variance collapses and the worst find "
            "is a fraction as long. <bookmark mark='c'/> Modern tables go further: Google's Swiss tables, and Rust's "
            "standard hash map, keep a byte of each hash beside the slots and compare sixteen of them at once "
            "with one vector instruction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
