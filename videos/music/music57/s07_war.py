from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class War(SoundScene):
    def construct(self):
        chapter(self, 6, r"The loudness war in numbers", r"What does a louder master cost?")
        self.history()
        self.table()
        self.curves()
        self.sausages()
        self.heard()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"vinyl and radio limited loudness by physics: \ a louder groove is a wider groove, \ and a shorter side", WHITE),
            (r"the CD \ (1982) \ had a hard ceiling but no other limit; \ digital limiters \ (1990s) \ let masters press against it", WHITE),
            (r"a record louder than the one before stands out on the radio, \ in a shop, \ in a changer: \ so each one was", WHITE),
            (r"by the mid-2000s, \ hit records were mastered 10 dB and more louder than in the 1980s", WHITE),
            (r"Deruty and Tardieu \ (2014), \ measuring decades of records: \ the hits got flatter, \ but songs did not lose their verse-and-chorus dynamics", TUNE),
        ]
        rows_scene(self, r"an arms race", items,
                   "The war was an arms race. <bookmark mark='b'/> Vinyl and radio limited loudness by physics: a louder groove is a "
                   "wider groove, and a shorter side. <bookmark mark='c'/> The CD, from 1982, had a hard ceiling and no other limit, "
                   "and digital look-ahead limiters in the 1990s let masters press against it. <bookmark mark='d'/> A record louder "
                   "than the one before stands out on the radio, in a shop, in a CD changer, so each one was. "
                   "<bookmark mark='e'/> By the mid-2000s hit records were mastered ten decibels and more louder than in the 1980s. "
                   "<bookmark mark='f'/> Emmanuel Deruty and Damien Tardieu, measuring decades of records in 2014, found what the "
                   "war actually took: the hits got flatter, while songs kept their verse-and-chorus dynamics.", marks="bcdef")

    # ------------------------------------------------------------------
    def table(self):
        d = load("war")
        rows = VGroup(VGroup(*[label(h, font_size=16, color=GREY_A) for h in (r"asked for", r"reached", r"true peak", r"PLR", r"crest factor", r"LRA", r"most limiting")]))
        for r in d["rows"]:
            col = TUNE if r["target"] >= -14 else EAR
            rows.add(VGroup(label(f"{r['target']:.0f} LUFS", font_size=17, color=col), label(f"{r['lufs']:.1f}", font_size=17, color=WHITE), label(f"{r['tp']:.1f} dBTP", font_size=17, color=WHITE),
                            label(f"{r['plr']:.1f} dB", font_size=17, color=col), label(f"{r['crest']:.1f} dB", font_size=17, color=WHITE), label(f"{r['lra']:.1f} LU", font_size=17, color=WHITE),
                            label(f"{r['gr_max']:.0f} dB", font_size=17, color=WHITE)))
        rows.arrange(DOWN, buff=0.28)
        xs = [-5.2, -3.4, -1.6, 0.3, 2.0, 3.7, 5.3]
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(xs[i])
        rows.move_to(DOWN * 0.2)
        note = label(r"past about $-7.7$ LUFS this limiter gives no more loudness on this mix, \ however hard it is driven; \ louder needs clipping", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"one mix, \ six masters", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the war in numbers, on our own mix, mastered by Monochord's chain at six loudness targets. "
            "<bookmark mark='a'/> At minus twenty and minus seventeen the limiter does nothing: the mix simply fits. "
            "<bookmark mark='b'/> From minus fourteen it starts to work, and every three decibels of loudness after that costs "
            "about three decibels of peak-to-loudness ratio, and more and more limiting. <bookmark mark='c'/> Asked for minus "
            "seven, it reaches only minus seven point seven: past that, no amount of drive makes this limiter louder on this "
            "mix. The masters of the war got there by clipping. And the loudness range hardly moves, as Deruty and Tardieu "
            "found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:6]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[6]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("war")
        L = np.array([r["lufs"] for r in d["rows"]])
        ax = frame_axes(width=8.6, height=3.2, xlo=-21, xhi=-7, ylo=0, yhi=20, center=DOWN * 0.3 + LEFT * 0.6)
        plr = VGroup(curve(L, [r["plr"] for r in d["rows"]], ax.to, color=TUNE, width=3), *[Dot(ax.to(x, r["plr"]), radius=0.07, color=TUNE) for x, r in zip(L, d["rows"])])
        crest = VGroup(curve(L, [r["crest"] for r in d["rows"]], ax.to, color=BLUE, width=3), *[Dot(ax.to(x, r["crest"]), radius=0.07, color=BLUE) for x, r in zip(L, d["rows"])])
        lra = VGroup(curve(L, [r["lra"] for r in d["rows"]], ax.to, color=GREY_A, width=3), *[Dot(ax.to(x, r["lra"]), radius=0.07, color=GREY_A) for x, r in zip(L, d["rows"])])
        xt = VGroup(*[label(f"{v}", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (-20, -17, -14, -11, -8)])
        xl = label(r"integrated loudness of the master, \ LUFS", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(-21, v), LEFT, buff=0.1) for v in (0, 10, 20)])
        key = VGroup(label(r"peak-to-loudness ratio", font_size=16, color=TUNE), label(r"crest factor", font_size=16, color=BLUE), label(r"loudness range", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        head = label(r"what loudness costs", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Plotted against the loudness of the master: <bookmark mark='a'/> the peak-to-loudness ratio falls from fifteen "
            "decibels to under seven, <bookmark mark='b'/> the crest factor follows it, <bookmark mark='c'/> and the loudness "
            "range stays where it was, near the floor, because our mix was steady to begin with. What the war takes is the "
            "difference between a drum hit and everything around it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(ghost(VGroup(plr, crest, lra), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(plr), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(crest), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(lra), FadeIn(key[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sausages(self):
        d = load("war")
        cols = {"-20.0": GREY_A, "-14.0": TUNE, "-9.0": BLUE, "-7.0": EAR}
        g = VGroup()
        for i, (k, col) in enumerate(cols.items()):
            env = d["env"][k]
            ax = frame_axes(width=10.0, height=1.1, xlo=0, xhi=len(env), ylo=-1, yhi=1, center=np.array([0.6, 1.9 - 1.35 * i, 0]))
            top = [ax.to(j, v) for j, v in enumerate(env)]
            bot = [ax.to(j, -v) for j, v in reversed(list(enumerate(env)))]
            poly = Polygon(*(top + bot), stroke_width=0, fill_color=col, fill_opacity=0.8)
            g.add(VGroup(poly, label(rf"{float(k):.0f} LUFS", font_size=17, color=col).move_to([-5.5, 1.9 - 1.35 * i, 0])))
        head = label(r"the sausage", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And here is what fans saw in 2008, on our mix: the waveforms of four masters drawn at the same scale. "
            "<bookmark mark='a'/> At minus twenty the drum hits stand up from the rest. <bookmark mark='b'/> By minus seven the "
            "waveform is a solid block from edge to edge: the sausage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(g, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(g[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("war")
        c = clip("war.three")
        boxes = choice_boxes([r"$-20$ LUFS", r"$-14$ LUFS", r"$-8$ LUFS"], width=2.8, height=0.9, buff=0.9, size=20).move_to(UP * 0.4)
        note = label(r"as mastered: \ each louder than the last", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"three masters, \ as a CD would play them", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear three of them as a CD player would play them, each louder than the last."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three masters", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["m20"], st["m14"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["m14"], st["m8"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["m8"], c.duration, buff=0.08)
        with self.voiceover("Played like this, the loudest is the most exciting, at first. That is the whole reason for the war, and the next chapter shows how normalization changed the playback advantage."):
            self.play(Indicate(boxes[2], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()
