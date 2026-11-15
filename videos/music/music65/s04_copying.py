from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Copying(SoundScene):
    def construct(self):
        chapter(self, 3, r"Novelty and copying", r"When does learning from Bach become copying Bach?")
        self.measure()
        self.heard()
        self.trade()

    # ------------------------------------------------------------------
    def measure(self):
        d = load("copy")
        orders = ["1", "2", "3", "4", "6", "8"]
        g = VGroup()
        for k in orders:
            r = d["orders"][k]
            g.add(VGroup(label(rf"order {k}", font_size=19, color=WHITE), label(f"{r['longest']:.1f}", font_size=19, color=TUNE), label(f"{100 * r['share8']:.0f}\\%", font_size=19, color=EAR)))
        b = d["bach"]
        g.add(VGroup(label(r"Bach's own tunes, \ kept back", font_size=19, color=GOLD), label(f"{b['longest']:.1f}", font_size=19, color=GOLD), label(f"{100 * b['share8']:.0f}\\%", font_size=19, color=GOLD)))
        g.arrange(DOWN, buff=0.28)
        for r in g:
            for i, x in enumerate((-3.4, 0.6, 3.6)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.4)
        top = VGroup(label(r"longest run of notes copied \ from one training tune", font_size=15, color=TUNE).move_to([0.6, g.get_top()[1] + 0.55, 0]),
                     label(r"share of notes inside \ a copied run of 8", font_size=15, color=EAR).move_to([3.6, g.get_top()[1] + 0.55, 0]))
        head = label(r"how much is copied?", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        o8, o1 = d["orders"]["8"], d["orders"]["1"]
        with self.voiceover(
            "Measure copying directly. For each of twenty tunes from each order, find the longest run of notes that appears, "
            "note for note, in some training tune, and the share of its notes that sit inside a copied run of eight. "
            f"<bookmark mark='a'/> Order one copies runs of about {say(o1['longest'], 0)} notes, and almost nothing of eight. "
            f"<bookmark mark='b'/> Order eight copies runs of {say(o8['longest'], 0)} notes, and {say(round(100 * o8['share8']))} "
            "per cent of everything it writes is inside a copied run of eight. <bookmark mark='c'/> And the yardstick: Bach's "
            "own tunes, the ones kept back, measured the same way against the training tunes. They share runs of about "
            f"{say(b['longest'], 0)} notes, and {say(round(100 * b['share8']))} per cent: hymn tunes share their stock phrases, "
            "and cadences most of all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[2:6]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(g[6]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("copy")
        c = clip("copy.two")
        lc = d["sample_copy"]
        boxes = choice_boxes([r"an order-8 tune \ (its copied stretch)", rf"{bwv(d['source'])}, \ by Bach"], width=4.6, height=0.9, buff=0.8, size=18).move_to(UP * 0.6)
        res = label(rf"{lc['length']} notes in a row, \ note for note, \ from one chorale", font_size=20, color=EAR).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the copy, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it. The longest copied stretch of an order-eight tune, then the opening of the chorale it came from."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"copy, \ then source", kind="synthesized", detail=rf"an order-8 chain; \ {bwv(d['source'])}", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["sample"], st["source"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["source"], c.duration, buff=0.08)
        with self.voiceover(
            f"{say(lc['length'])} notes in a row, note for note, from {bwv_said(d['source'])}. With eight notes of memory and "
            "only a few thousand notes to learn from, most contexts have been seen once, in one tune, and the chain can only "
            "follow that tune where it went. It sounds like Bach because it is Bach."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trade(self):
        d = load("copy")
        orders = ["1", "2", "3", "4", "6", "8"]
        bits = np.array([d["bits"][k] for k in orders])
        share = np.array([d["orders"][k]["share8"] for k in orders])
        ax = frame_axes(width=7.0, height=3.4, xlo=0, xhi=1, ylo=3.2, yhi=4.0, center=DOWN * 0.4 + LEFT * 1.0)
        cv = curve(share, bits, ax.to, color=TUNE, width=3)
        dots = VGroup(*[VGroup(Dot(ax.to(x, y), radius=0.07, color=TUNE), label(f"{k}", font_size=14, color=GREY_A).next_to(ax.to(x, y), UP, buff=0.1)) for k, x, y in zip(orders, share, bits)])
        b = d["bach"]
        bx = DashedLine(ax.to(b["share8"], 3.2), ax.to(b["share8"], 4.0), color=GOLD, stroke_width=2)
        bl = label(r"Bach's share", font_size=14, color=GOLD).next_to(bx, UP, buff=0.08)
        xl = label(r"share of notes inside a copied run of 8", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"bits per note on new tunes", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(r"too little memory: \ new, \ and aimless", font_size=16, color=WHITE),
                      label(r"too much: \ coherent, \ and copied", font_size=16, color=WHITE),
                      label(r"the best predictor, \ order 2, \ copies a little less than Bach's tunes share", font_size=16, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"the trade nobody escapes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Put the two measures together: copying across, prediction of new tunes up, one dot for each order. "
            "<bookmark mark='a'/> With little memory a model is new and aimless; with much, coherent and copied. "
            "<bookmark mark='b'/> The order that predicts new tunes best, order two, copies a little less than Bach's own "
            "tunes share with one another, and order three a good deal more. That is no accident: a model tuned to predict "
            "new music cannot simply replay old music, and every generator in this part sits somewhere on such a curve. "
            "Alexandre Papadopoulos, Pierre Roy and François Pachet built Markov generators that forbid copying beyond a "
            "chosen length, by construction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(dots), FadeIn(side[0]), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(bl), FadeIn(side[2]))
        self.wait(0.6)
        self.clear_scene()
