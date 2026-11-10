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
            "Chains cost a pointer per key and a jump in memory per step. Open addressing keeps every key"
            " in the table itself. <bookmark mark='a'/> On a collision, linear probing tries the next "
            "slot, and the next, until it finds a free one; a find follows the same path until it finds "
            "the key or an empty slot. <bookmark mark='b'/> It is one array with no pointers, and the "
            "next probe is almost always in the same cache line, which is why it is so fast in practice. "
            "<bookmark mark='c'/> Its weakness is visible in these snapshots of a sixty-four-slot table "
            "filling up. Full slots form runs, and a key that lands anywhere in a run joins its end, so "
            "long runs grow faster than short ones and merge. This is primary clustering."
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
            label(r"large-table references: \ independent uniform homes; \ fixed load below one; "
                  r"not exact finite-table identities for this affine hash family", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(f, DOWN, buff=0.55)
        with self.voiceover(
            "Knuth analyzed linear probing under random home addresses. <bookmark mark='a'/> The first "
            "expression is the large-table expected successful-search reference at load alpha. <bookmark "
            "mark='b'/> The second is the unsuccessful-search or insertion reference, which grows with "
            "the square of one over the free fraction. These are not exact finite-table identities for "
            "every fixed hash. <bookmark mark='c'/> Uniform permutation probing is a separate model; its "
            "reciprocal-free-fraction expression is also an asymptotic reference, with finite "
            "corrections. <bookmark mark='d'/> At half load the linear references are one point five and "
            "two point five; at ninety percent they are five point five and fifty point five. <bookmark "
            "mark='e'/> The rapid growth explains why leaving free space matters. Resizing, deletions, "
            "key hashing and adversarial choices need their own accounting."
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
            label(r"double hashing: \ observed misses; \ not uniform permutations", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        r5 = next(r for r in rows if r["alpha"] == 0.5)
        r8 = next(r for r in rows if r["alpha"] == 0.8)
        nums = label(rf"at $\alpha = 0.5$: \ {r5['linear_miss']:.2f} \ (Knuth {r5['knuth_miss']:.2f}); \ "
                     rf"at $0.8$: \ {r8['linear_miss']:.1f} \ ({r8['knuth_miss']:.1f})", font_size=19,
                     color=GREY_A).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        panel = VGroup(key, nums)
        if panel.width > 5.7:
            panel.scale_to_fit_width(5.7)
        panel.to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Here is a finite seeded illustration, not a proof of the random-home model. <bookmark "
            "mark='a'/> Each load uses a new key set and a universal affine hash, which controls pair "
            "collisions but does not supply fully independent home addresses. The red observations count "
            "unsuccessful searches at fixed load; they are the probe cost of one more insert before the "
            "table changes. <bookmark mark='b'/> Actual n over m is recorded, and the reference formulas "
            "use that value. A single table per load cannot establish a confidence interval or explain a "
            "deviation's cause. <bookmark mark='c'/> Successful searches are sampled uniformly from "
            "resident keys. <bookmark mark='d'/> Double hashing uses a second step size. It may resemble "
            "a uniform-probing reference here, but it does not generate an independent uniform "
            "permutation for each key."
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
            colors=[[NO, WHITE, NO, NO], [YES, WHITE, YES, YES]]).next_to(head, DOWN, buff=0.42)
        pts = VGroup(
            label(r"on a collision, \ the key farther from its home slot keeps the slot; \ the other moves on",
                  font_size=22, color=GREY_A),
            label(r"identical keys/order/home hash: \ same displacement sum; \ observed spread differs",
                  font_size=22, color=YES),
            label(r"grouped-control-byte tables are a distinct design; \ vector widths depend on the implementation "
                  r"and target hardware", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.3)
        # keys 0..4 have shared homes [0,0,1,0,2].
        from explainer.cs.algo import ds as D
        home = lambda k: [0, 0, 1, 0, 2][k]
        lp, rh = D.LinearProbing(8, home), D.RobinHood(8, home)
        for k in range(5):
            lp.insert(k); rh.insert(k)
        examples = VGroup()
        for name, table, color in [('LP', lp, NO), ('RH', rh, YES)]:
            values = [(v[0] if isinstance(v, tuple) else v) for v in table.t]
            row = slots([v is not None for v in values], w=0.55, h=0.42, color=color)
            labels = VGroup(*[mono(str(v), 17, WHITE).move_to(row[i]) for i,v in enumerate(values) if v is not None])
            tag = mono(name, 18, color).next_to(row, LEFT, buff=0.16)
            examples.add(VGroup(row, labels, tag))
        examples.arrange(DOWN, buff=0.2).move_to(DOWN * 0.5)
        witness_note = label(r"keys 0..4: \ homes 0,0,1,0,2; \ same occupied slots and total displacement",
                             font_size=19, color=HEAD).next_to(examples, DOWN, buff=0.18)
        with self.voiceover(
            "One refinement redistributes displacement. <bookmark mark='a'/> Robin Hood hashing lets the "
            "key farther from its home slot displace the key closer to home, then carries the displaced "
            "key onward. <bookmark mark='b'/> For a controlled comparison we use identical keys, "
            "insertion order and home hash. Both tables occupy exactly the same slots and have the same "
            "total displacement, so their mean successful scan length agrees exactly. The variance and "
            "maximum differ as displayed. <bookmark mark='c'/> That does not make every lookup equal, and"
            " implementations can use an additional early-stop rule. Modern grouped-control-byte tables "
            "are another design choice; they should not all be identified with this Robin Hood rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(examples), FadeIn(witness_note))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
