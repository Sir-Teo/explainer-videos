from __future__ import annotations

import numpy as np

from videos.music.music68.common import *  # noqa: F403

ACT_COLORS = ["#F5C542", "#9DD6F0", "#FFB070", "#B39DDB", "#7DD3FC", "#A3E635", "#F472B6", "#FB7185", "#94A3B8", "#5EEAD4", "#FDE68A", "#E5E7EB"]


def act_index(p: int) -> int:
    for i, (_, (a, b)) in enumerate(ACTS):
        if a <= p <= b:
            return i
    return 0


class Order(SoundScene):
    def construct(self):
        chapter(self, 5, r"Ordering a suite", r"In what order should sixty-seven Variations be played?")
        self.problem()
        self.map_()
        self.lengths()
        self.pairs()
        self.nearest()
        self.choice()

    # ------------------------------------------------------------------
    def problem(self):
        s = load("suite")
        items = [
            (r"sixty-seven Variations, \ 39 minutes in all: \ too long, \ and too uneven, \ for one sitting", WHITE),
            (rf"an excerpt of each: \ the first {s['excerpt']:g} seconds from its first sound, \ brought to one loudness \ (a rule fixed in advance, \ not chosen by ear)", WHITE),
            (r"then an order: \ a suite is heard in sequence, \ and each piece is heard against the one before", WHITE),
            (r"three candidates: \ as they were made; \ each followed by the one that sounds nearest; \ at random", TUNE),
        ]
        rows_scene(self, r"from sixty-seven Variations to a suite", items,
                   "The plan for this part promised a suite. <bookmark mark='b'/> Sixty-seven Variations last about thirty-nine "
                   "minutes, too long and too uneven for one sitting. <bookmark mark='c'/> So the suite takes an excerpt of each: "
                   "the first eight and a half seconds from its first sound, brought to one loudness. The rule was fixed in "
                   "advance, not chosen by ear, so no excerpt was picked for flattering its part. <bookmark mark='d'/> Then it "
                   "needs an order, because a suite is heard in sequence, each piece against the one before. "
                   "<bookmark mark='e'/> Three candidates: the order they were made in; each followed by whichever sounds nearest; "
                   "and at random.", marks="bcde")

    # ------------------------------------------------------------------
    def map_(self):
        o = load("order")
        xy = np.array(o["xy"])
        xy = (xy - xy.mean(axis=0)) / (np.abs(xy).max(axis=0) + 1e-9)
        pts = [np.array([4.6 * x, 2.4 * y - 0.3, 0]) for x, y in xy]
        dots = VGroup(*[Dot(p, radius=0.07, color=ACT_COLORS[act_index(i + 1)]) for i, p in enumerate(pts)])
        nums = VGroup(*[label(str(i + 1), font_size=11, color=GREY_A).next_to(d, UR, buff=0.02) for i, d in enumerate(dots)])
        path = VMobject(stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.5).set_points_as_corners(pts)
        key = VGroup(*[VGroup(Dot(radius=0.06, color=ACT_COLORS[i]), label(ACTS[i][0], font_size=12, color=GREY_A)).arrange(RIGHT, buff=0.1) for i in range(12)])
        key.arrange_in_grid(rows=2, cols=6, buff=(0.3, 0.12)).to_edge(DOWN, buff=0.15)
        head = label(r"the sixty-seven excerpts, \ placed by how they sound", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        with self.voiceover(
            "To compare orders, each excerpt is described by the content features of Part 63: the levels and spread of "
            "twenty-four frequency bands, a chroma, and the flux of the spectrum, each standardized. <bookmark mark='a'/> Here "
            "they are, flattened onto the page by classical scaling, coloured by act: excerpts that sound alike by these "
            "measures sit close together. <bookmark mark='b'/> And here is the path in the order they were made. It wanders, "
            "but in places it stays in a neighbourhood for several parts at a time, where consecutive parts share their "
            "instruments."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02), FadeIn(nums), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(path), run_time=3.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        o = load("order")
        hist, edges = np.array(o["random_hist"]), np.array(o["random_edges"])
        lo, hi = min(o["nearest"], edges[0]) * 0.95, edges[-1] * 1.02
        ax = frame_axes(width=10.0, height=3.0, xlo=lo, xhi=hi, ylo=0, yhi=hist.max() * 1.15, center=DOWN * 0.4)
        bars = VGroup()
        for h, a, b in zip(hist, edges, edges[1:]):
            p0, p1 = ax.to(a, 0), ax.to(b, h)
            bars.add(Rectangle(width=max(p1[0] - p0[0] - 0.01, 0.01), height=max(p1[1] - p0[1], 0.001), stroke_width=0, fill_color=GREY_B, fill_opacity=0.7).move_to((p0 + p1) / 2))

        def mark(x, text, color):
            ln = Line(ax.to(x, 0), ax.to(x, hist.max() * 1.1), color=color, stroke_width=3)
            return VGroup(ln, label(text, font_size=15, color=color).next_to(ln, UP, buff=0.08))

        built = mark(o["built"], rf"as made: \ {o['built']:.0f}", TUNE)
        near = mark(o["nearest"], rf"nearest next: \ {o['nearest']:.0f}", EAR)
        cap = label(rf"2000 random orders \ (grey): \ {o['random_lo']:.0f} to {o['random_hi']:.0f} \ (95\%)", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        head = label(r"the length of the path, \ in standardized units", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        pct = 100 * (1 - o["built_below_random"])
        with self.voiceover(
            "Add up the steps of a path and you have a measure of how far, in sound, a suite travels. <bookmark mark='a'/> "
            f"Two thousand random orders travel between {say(round(o['random_lo']))} and {say(round(o['random_hi']))} units, "
            f"ninety-five times in a hundred. <bookmark mark='b'/> The order the Variations were made in travels "
            f"{say(round(o['built']))}: shorter than {say(pct, 1)} per cent of the random ones. Consecutive parts sound alike "
            "more often than chance. <bookmark mark='c'/> And a rule that always moves to the nearest excerpt not yet played "
            f"travels only {say(round(o['nearest']))}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bars), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(built))
            vo.wait_until("c")
            self.play(FadeIn(near))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("pairs")
        c = clip("order.pairs")
        card = listen_card(r"Two pairs of neighbours from the suite, \ five seconds each. \ "
                           r"Which pair sounds closer together, \ the first or the second?", width=9.6)
        with self.voiceover(
            "Two pairs of neighbours from the suite as it was made, five seconds of each Variation. Which pair sounds closer "
            "together, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.0, height=1.0, corner_radius=0.12, stroke_color=TUNE), label(rf"Variation {n}", font_size=20, color=TUNE)).arrange(ORIGIN)
                         for n in (d["big"], d["big"] + 1, d["small"], d["small"] + 1)])
        pa = VGroup(boxes[0], boxes[1]).arrange(RIGHT, buff=0.3)
        pb = VGroup(boxes[2], boxes[3]).arrange(RIGHT, buff=0.3)
        VGroup(pa, pb).arrange(RIGHT, buff=1.4).move_to(UP * 0.6)
        tags = VGroup(label(r"first pair", font_size=18, color=GREY_A).next_to(pa, UP, buff=0.2), label(r"second pair", font_size=18, color=GREY_A).next_to(pb, UP, buff=0.2))
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(tags))
        st = d["starts"]
        ks = ["a1", "a2", "b1", "b2"]
        with self.listen(c) as snd:
            window(snd, r"two pairs of neighbours", kind="synthesized", detail=r"physical models and synthesis, \ as their parts made them", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        o = load("order")
        res = VGroup(
            label(rf"by the features, \ the second: \ the step from {d['small']} to {d['small'] + 1} is the suite's shortest, \ from {d['big']} to {d['big'] + 1} its longest", font_size=18, color=TUNE),
            label(rf"{SHORT[d['big']]} \ $\to$ \ {SHORT[d['big'] + 1]}; \ \ {SHORT[d['small']]} \ $\to$ \ {SHORT[d['small'] + 1]}", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.6)
        with self.voiceover(
            f"By the features, the second: the step from Variation {say(d['small'])} to {say(d['small'] + 1)} is the shortest "
            f"in the suite, and the step from {say(d['big'])} to {say(d['big'] + 1)} the longest. Whether your ear agreed is "
            "the real test of the features, and it may not have: they measure bands and chroma, not everything a listener "
            "hears."
        ):
            self.play(FadeIn(res))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nearest(self):
        d = load("nearest")
        c = clip("order.nearest")
        cells = VGroup(*[VGroup(RoundedRectangle(width=1.3, height=0.9, corner_radius=0.1, stroke_color=EAR), label(str(n), font_size=24, color=EAR)).arrange(ORIGIN) for n in d["parts"]])
        cells.arrange(RIGHT, buff=0.18).move_to(UP * 0.5)
        head = label(r"the nearest-next order, \ its first eight steps", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the nearest-next order, its first eight steps, four seconds each. Listen to how smoothly it moves, and "
            "how little it tells you."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = {int(k): v for k, v in d["starts"].items()}
        ps = d["parts"]
        with self.listen(c) as snd:
            window(snd, r"nearest next", kind="synthesized", detail=r"eight Variations, \ four seconds each", corner=DL, tag_corner=DR)
            for i, p in enumerate(ps):
                end = st[ps[i + 1]] - 0.2 if i + 1 < len(ps) else c.duration
                pulse(snd, cells[i], st[p], end, buff=0.05)
        res = label(r"smooth, \ and shuffled across sixty-seven parts: \ the story of the series is gone", font_size=20, color=WHITE).move_to(DOWN * 1.5)
        with self.voiceover("Smooth, and shuffled across the whole series: the story of how the Tune changed, part by part, is gone."):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choice(self):
        items = [
            (r"the nearest-next order is smoothest, \ and tells no story", WHITE),
            (r"a random order is neither smooth nor a story", WHITE),
            (r"the order as made is a history: \ each Variation uses what the ones before it built", WHITE),
            (r"and it is already smoother than nearly every random order", WHITE),
            (r"so the suite is played as the Variations were made, \ in three movements", TUNE),
        ]
        rows_scene(self, r"the order chosen", items,
                   "Which order, then? <bookmark mark='b'/> The nearest-next order is the smoothest, and tells no story. "
                   "<bookmark mark='c'/> A random order is neither smooth nor a story. <bookmark mark='d'/> The order they were "
                   "made in is a history: each Variation uses what the parts before it built. <bookmark mark='e'/> And it is "
                   "already smoother than nearly every random order. <bookmark mark='f'/> So the suite is played as the "
                   "Variations were made, in three movements.", marks="bcdef")
