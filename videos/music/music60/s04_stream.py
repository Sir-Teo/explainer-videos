from __future__ import annotations

import numpy as np

from videos.music.music60.common import *  # noqa: F403


class Stream(SoundScene):
    def construct(self):
        chapter(self, 3, r"Where a stream's money goes", r"What does one stream pay a songwriter?")
        self.thirty()
        self.month()
        self.million()
        self.context()

    # ------------------------------------------------------------------
    def thirty(self):
        d = load("stream")
        c = clip("stream.thirty")
        bar = Rectangle(width=10.0, height=0.35, stroke_color=GREY_B, stroke_width=2).move_to(DOWN * 0.2)
        mark30 = Line(bar.get_left() + RIGHT * 10.0 * 30 / d["seconds"] + UP * 0.35, bar.get_left() + RIGHT * 10.0 * 30 / d["seconds"] + DOWN * 0.35, color=TUNE, stroke_width=4)
        t30 = label(r"30 s: \ now it counts as a stream", font_size=17, color=TUNE).next_to(mark30, UP, buff=0.15)
        fill = Rectangle(width=0.01, height=0.35, stroke_width=0, fill_color=BLUE, fill_opacity=0.8).align_to(bar, LEFT).align_to(bar, DOWN)
        head = label(r"one stream", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Start with one stream: our session playing the whole Tune. On the largest service, a thirty-second listening rule is one counting condition on Spotify; payment also depends on eligibility, territory, policy and contracts, so it is not an unconditional per-play payout."):
            self.play(FadeIn(head), FadeIn(bar), FadeIn(mark30), FadeIn(t30))
        self.add(fill)
        sec = d["seconds"]

        def grow(m, t):
            m.become(Rectangle(width=max(0.01, 10.0 * min(t, sec) / sec), height=0.35, stroke_width=0,
                               fill_color=TUNE if t >= 30.0 else BLUE, fill_opacity=0.8).align_to(bar, LEFT).align_to(bar, DOWN))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ whole", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            snd.drive(fill, grow)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def month(self):
        d = load("waterfall")
        rows_ = [r for r in d["month"] if not r.get("part") and r["amount"] > 0]
        total = d["terms"]["price"]
        cols = {"the service": GREY_B, "the label": BLUE, "the artist (credited, against the advance)": BLUE, "the producer": BLUE,
                "collecting societies and administrators": TUNE, "the publisher": TUNE}
        x0, w = -6.0, 12.0
        y = 1.3
        segs, tags = VGroup(), VGroup()
        acc = 0.0
        for k, r in enumerate(rows_):
            ww = w * r["amount"] / total
            col = cols.get(r["who"], TUNE)
            seg = Rectangle(width=ww, height=0.8, stroke_color=BLACK, stroke_width=1.5, fill_color=col, fill_opacity=0.35 + 0.15 * (k % 3)).move_to([x0 + w * acc / total + ww / 2, y, 0])
            acc += r["amount"]
            name = r["who"].replace(" (credited, against the advance)", r" \ (credited, \ against the advance)").replace("collecting societies and administrators", r"societies and administrators")
            sw = Square(side_length=0.22, stroke_width=0, fill_color=col, fill_opacity=0.35 + 0.15 * (k % 3))
            t = VGroup(sw, label(name, font_size=16, color=col), label(rf"\${r['amount']:.2f}", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.18)
            segs.add(seg)
            tags.add(t)
        tags.arrange_in_grid(rows=4, cols=2, buff=(1.0, 0.28), col_alignments="ll", flow_order="dr").move_to(DOWN * 0.75)
        each = [r for r in d["month"] if r.get("part")][0]
        note = label(rf"one subscriber's month, \ \${total:.2f}: \ the service keeps 30\%; \ the recording takes 55\%, \ the composition 15\%; \ each of three songwriters, \ \${each['amount']:.2f}",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"one month's subscription, \ divided \ (illustrative terms)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Now follow the money, on illustrative terms. A subscriber pays {say(total, 2)} dollars a month. "
            "<bookmark mark='a'/> The service keeps about thirty percent. <bookmark mark='b'/> Of the seventy that go to rights "
            "holders, about fifty-five points go to the recording: the label keeps most, and credits the artist with a royalty, "
            "here eighteen percent of its receipts, and the producer with three. <bookmark mark='c'/> About fifteen points go to "
            "the composition: the societies take their costs, the publisher its share, and the songwriters split the rest. "
            f"Each of three writers gets about {say(100 * each['amount'], 0)} cents of the month."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(segs[0]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(segs[i], tags[i])) for i in range(1, 4)], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(segs[i], tags[i])) for i in range(4, len(segs))], lag_ratio=0.3), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def million(self):
        d = load("waterfall")
        lab, ind = d["million_label"], d["million_indie"]
        keys = ["the service", "the distributor", "the label", "the artist (credited, against the advance)", "the producer",
                "collecting societies and administrators", "the publisher", "each songwriter"]
        names = {"the artist (credited, against the advance)": r"the artist", "collecting societies and administrators": r"societies and administrators",
                 "each songwriter": r"each of three songwriters"}
        g = VGroup()
        for k in keys:
            g.add(VGroup(label(names.get(k, k), font_size=18, color=WHITE), label(rf"\${lab[k]:,.0f}", font_size=18, color=BLUE),
                         label(rf"\${ind[k]:,.0f}", font_size=18, color=TUNE)))
        g.arrange(DOWN, buff=0.22)
        for r in g:
            r[0].set_x(-3.0)
            r[1].set_x(1.6)
            r[2].set_x(4.4)
        top = VGroup(label(r"a label deal", font_size=17, color=BLUE).move_to([1.6, g.get_top()[1] + 0.45, 0]),
                     label(r"self-released, \ 15\% to a distributor", font_size=17, color=TUNE).move_to([4.4, g.get_top()[1] + 0.45, 0]))
        top[1].set_x(4.6)
        g.add(top)
        g.move_to(DOWN * 0.2)
        rate_ = label(rf"the service pays the rights holders about {100 * d['rate']:.2f} cents a stream \ (our simulated service, \ Chapter 5); \ the artist's label credit is recoupable",
                      font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"one million streams", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"Scale it up to a million streams, at the rate our simulated service of Chapter 5 pays: about {say(100 * d['rate'], 2)} "
            f"cents a stream to all the rights holders together, {say(1e6 * d['rate'])} dollars in all. <bookmark mark='a'/> On a "
            f"label deal the artist is credited about {say(lab['the artist (credited, against the advance)'])} dollars, and "
            "credited is the word: it is set against the advance, and normally paid out only after the contractual recoupment balance is cleared. <bookmark mark='b'/> "
            f"Self-released through a distributor taking fifteen percent, the artist keeps about {say(ind['the artist (credited, against the advance)'])}, "
            f"but paid for the recording themselves. <bookmark mark='c'/> Either way, each of three songwriters gets about "
            f"{say(lab['each songwriter'])} dollars per million streams."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in g[:-1]])), FadeIn(rate_))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[r[1] for r in g[:-1]])), FadeIn(top[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r[2] for r in g[:-1]])), FadeIn(top[1]))
            vo.wait_until("c")
            self.play(Indicate(g[len(keys) - 1], color=TUNE, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def context(self):
        items = [
            (r"a CD in 1999 sold for about \$15; \ the same money now buys about 3,000 streams at the rights holders' rate", WHITE),
            (r"a fan who bought one album a year paid more than a subscriber who streams for an hour every day pays to any one artist", WHITE),
            (r"but recorded music's revenue has grown again: \ worldwide it passed its 1999 peak \ (in money of the day) \ in the early 2020s", WHITE),
            (r"the money is real, \ and large; \ it is divided among far more music, \ and far more musicians", TUNE),
        ]
        rows_scene(self, r"is that a lot?", items,
                   "Is that a lot? <bookmark mark='b'/> A CD in 1999 cost about fifteen dollars; at the rights holders' rate, the same money is about three thousand streams. <bookmark mark='c'/> Comparisons depend on listening concentration, deal terms and costs; retail album price and rights-holder streaming receipts are not directly equivalent. <bookmark mark='d'/> Yet recorded music's revenue has grown again: worldwide, it passed its 1999 peak, in money of the day, in the early 2020s. <bookmark mark='e'/> The money is real, and large; it is divided among far more music, and far more musicians, than ever before.", marks="bcde")
