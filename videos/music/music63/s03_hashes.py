from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Hashes(SoundScene):
    def construct(self):
        chapter(self, 2, r"Hashes and votes", r"How do ten seconds find their place among millions?")
        self.pairs()
        self.table()
        self.votes()

    # ------------------------------------------------------------------
    def pairs(self):
        ax = frame_axes(width=8.0, height=3.4, xlo=0, xhi=10, ylo=0, yhi=10, center=DOWN * 0.3 + LEFT * 1.2)
        rng = np.random.default_rng(3)
        pts = sorted([(float(rng.uniform(0.3, 9.7)), float(rng.uniform(0.5, 9.5))) for _ in range(22)])
        dots = VGroup(*[Dot(ax.to(t, f), radius=0.06, color=GREY_B) for t, f in pts])
        a = 6
        anchor = Dot(ax.to(*pts[a]), radius=0.1, color=TUNE)
        zone = Rectangle(width=8.0 * 3.0 / 10, height=3.4 * 5.0 / 10, stroke_color=TUNE, stroke_width=2).move_to(ax.to(pts[a][0] + 1.7, pts[a][1]))
        targets = [j for j in range(a + 1, len(pts)) if pts[j][0] - pts[a][0] < 3.2 and abs(pts[j][1] - pts[a][1]) < 2.5][:5]
        links = VGroup(*[Line(ax.to(*pts[a]), ax.to(*pts[j]), color=TUNE, stroke_width=2) for j in targets])
        eq = VGroup(MathTex(r"h = (f_1,\ f_2,\ \Delta t)", font_size=34, color=TUNE),
                    label(r"9 + 9 + 6 bits: \ about 16 million possible hashes", font_size=17, color=WHITE),
                    label(r"stored with the anchor's time, \ $t_1$", font_size=17, color=WHITE),
                    label(r"each anchor paired with up to 5 later peaks", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5)
        head = label(r"pairs of peaks", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A single peak says little: a frequency at a time. Wang's trick is to pair them. <bookmark mark='a'/> Take each "
            "peak as an anchor, <bookmark mark='b'/> and pair it with a few later peaks in a zone ahead of it. "
            "<bookmark mark='c'/> Each pair becomes a hash: the two frequencies and the time between them, packed into twenty-four "
            "bits, one of sixteen million possible values. It does not depend on when the query started, only on the music's "
            "own intervals of time and frequency. Store it with the anchor's time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(anchor))
            vo.wait_until("b")
            self.play(Create(zone), Create(links))
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        lib = load("library")
        items = [
            (rf"the library: \ every clip of Parts 1 to 60, \ {lib['clips']:,} clips, \ {lib['hours']:.1f} hours", WHITE),
            (rf"{lib['hashes']:,} hashes, \ each stored under its value with \ (clip, \ time)", WHITE),
            (r"a lookup is one step, \ however large the table: \ that is what a hash table is for", WHITE),
            (r"a commercial service holds tens of millions of recordings, \ billions of hashes, \ on many machines", TUNE),
        ]
        rows_scene(self, r"the hash table", items,
                   "Then index the library. <bookmark mark='b'/> Monochord's library is every clip of Parts 1 to 60: "
                   f"{say(lib['clips'])} clips, {say(lib['hours'], 1)} hours of sound. <bookmark mark='c'/> That makes "
                   f"{say(lib['hashes'])} hashes, each stored under its value with the clip and the time it came from. "
                   "<bookmark mark='d'/> Looking a hash up is one step, however large the table; that is what a hash table is for. "
                   "<bookmark mark='e'/> A commercial service holds tens of millions of recordings and billions of hashes, spread "
                   "over many machines.", marks="bcde")

    # ------------------------------------------------------------------
    def votes(self):
        d = load("hook")
        lines = VGroup(
            label(r"the query's hashes are looked up; \ each hit is a vote for a clip and an offset", font_size=20, color=WHITE),
            MathTex(r"\text{offset} = t_{\text{clip}} - t_{\text{query}}", font_size=36, color=TUNE),
            label(r"a true match: \ many hits at one offset, \ because the query's peaks keep their spacing", font_size=20, color=WHITE),
            label(r"chance hits: \ scattered over clips and offsets", font_size=20, color=GREY_A),
            label(rf"the bar: \ {d['result'][0]['votes']} votes at one offset for the right clip; \ the runner-up, \ {d['result'][1]['votes'] if len(d['result']) > 1 else 0}", font_size=20, color=TUNE),
        ).arrange(DOWN, buff=0.38)
        head = label(r"voting", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The search is a vote. <bookmark mark='a'/> Look up each of the query's hashes; every hit is a vote for a clip and "
            "an offset, <bookmark mark='b'/> the clip's time minus the query's. <bookmark mark='c'/> For the right clip the "
            "votes pile up at a single offset, because the query's peaks keep their spacing. <bookmark mark='d'/> Chance hits "
            "scatter over clips and offsets. <bookmark mark='e'/> In the noisy bar, the right Variation collected "
            f"{say(d['result'][0]['votes'])} votes at one offset, and the runner-up "
            f"{say(d['result'][1]['votes'] if len(d['result']) > 1 else 0)}."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()
