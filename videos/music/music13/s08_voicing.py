from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403

CURVE_C = {"3": MINOR_C, "4": MAJOR_C, "7": AUG_C, "12": "#C4B5FD"}
CURVE_N = {"3": r"minor third", "4": r"major third", "7": r"fifth", "12": r"octave"}


class Voicing(SoundScene):
    def construct(self):
        chapter(self, 7, r"Same chord, \ different sound", r"Why is a low third muddy?")
        self.thirds()
        self.why()
        self.limits()
        self.spacing()

    # ------------------------------------------------------------------
    def thirds(self):
        d = load("voicing")
        c = clip("voicing.thirds")
        regs = d["registers"]
        kb = keys(24, 84, width=12.6, height=1.5).move_to(UP * 1.6)
        bars = VGroup()
        top = max(d["third_roughness"])
        for b, r, nm in zip(regs, d["third_roughness"], d["register_names"]):
            x = (kb.key[b - 60].get_center()[0] + kb.key[b + 4 - 60].get_center()[0]) / 2
            h = 2.2 * r / top
            bar = Rectangle(width=0.55, height=h, stroke_width=0, fill_color=TUNE, fill_opacity=0.9).move_to([x, 0.45 - h / 2, 0])
            bars.add(VGroup(bar, label(f"{r:.2f}", font_size=22, color=WHITE).next_to(bar, DOWN, buff=0.1), label(nm, font_size=22, color=GREY_B).move_to([x, 2.65, 0])))
        head = label(r"one major third, \ on five different Cs", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the second puzzle from the opening. A chord's name says which notes. Its voicing says "
            "where they are, and the voicing can matter more than the name. Start with a single "
            "interval. Here is a major third, four semitones, on five different Cs, from high to low."
        ):
            self.play(FadeIn(head), FadeIn(kb), *[FadeIn(b[2]) for b in bars])
            for b in regs:
                kb.on(b), kb.on(b + 4)
        kb.clear()
        with self.listen(c) as snd:
            window(snd, r"a third, \ going down", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [[b, b + 4] for b in regs], d["third_times"], end=c.duration)
            for k in range(5):
                pulse(snd, bars[k][2], d["third_times"][k], d["third_times"][k + 1] if k < 4 else c.duration, buff=0.1)
        kb.clear()
        cap = label(r"roughness, \ by Part 5's model", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "At the top, clear. At the bottom, a rumble in which you can hardly tell that there are two "
            "notes. <bookmark mark='a'/> Part 5's roughness model puts numbers on it: each time the "
            "third drops an octave it is nearly twice as rough, and at the bottom it is eleven times as "
            "rough as at the top. The interval never changed."
        ) as vo:
            for b in regs:
                kb.on(b), kb.on(b + 4)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(b[0], b[1])) for b in bars], lag_ratio=0.3), FadeIn(cap), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d = load("voicing")
        names, bands = d["register_names"], d["third_bands"]
        g = VGroup()
        base_y, unit = -1.9, 2.2
        for k, (nm, w) in enumerate(zip(names, bands)):
            x = (k - 2) * 2.1
            bar = Rectangle(width=1.0, height=unit * w, stroke_width=0, fill_color=TUNE if w >= 1 else EAR, fill_opacity=0.9).move_to([x, base_y + unit * w / 2, 0])
            g.add(VGroup(bar, label(f"{w:.2f}", font_size=26, color=WHITE).next_to(bar, UP, buff=0.12), label(nm, font_size=28, color=GREY_A).move_to([x, base_y - 0.35, 0])))
        one = DashedLine([-5.6, base_y + unit, 0], [5.6, base_y + unit, 0], color=WHITE, stroke_width=2)
        onel = label(r"one critical band", font_size=24, color=WHITE).next_to(one, UP, buff=0.08).align_to(one, RIGHT)
        head = label(r"how wide a major third is, \ in critical bands of the ear", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Part 4 explains it. The ear sorts sound into critical bands, and two tones that fall inside "
            "one band interfere: that is roughness. But a critical band is not a fixed musical interval. "
            "High up, it is narrower than a minor third. Low down, it is wider than a fifth. "
            "<bookmark mark='a'/> So measure our major third in critical bands. On the C above middle "
            f"C it spans {say(bands[0], 1)} bands: the two notes are heard apart. On middle C, a little "
            f"over one. <bookmark mark='b'/> An octave below that, {say(bands[2], 1)}: now they share a "
            f"band. And at the bottom, {say(bands[4], 1)} of a band. The two fundamentals grind against "
            "each other, and all their harmonics with them."
        ) as vo:
            self.play(FadeIn(head), Create(one), FadeIn(onel))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), run_time=0.6)
            self.wait(2.5)
            self.play(FadeIn(g[1]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(g[2]), run_time=0.6)
            self.wait(2.0)
            self.play(FadeIn(g[3]), FadeIn(g[4]), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        d = load("voicing")
        xs = np.array(d["basses"], dtype=float)
        g = axes([24, 84], [0, 4.2], x_length=10.5, y_length=4.0, xlabel=r"the lower note of the interval", ylabel=r"roughness", xticks=[24, 36, 48, 60, 72, 84], yticks=[1, 2, 3, 4],
                 xfmt=lambda v: rf"\mathrm{{C}}{int(v) // 12 - 1}", font_size=22).move_to(LEFT * 0.9 + DOWN * 0.2)
        curves = {k: curve_from(g, xs, np.minimum(np.array(d["curves"][k]), 4.2), CURVE_C[k]) for k in ("3", "4", "7", "12")}
        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.5, color=CURVE_C[k], stroke_width=4), label(CURVE_N[k], font_size=24, color=CURVE_C[k])).arrange(RIGHT, buff=0.15) for k in ("3", "4", "7", "12")]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 5.4 + UP * 1.4)
        ref = DashedLine(g.ax.c2p(24, d["reference"]), g.ax.c2p(84, d["reference"]), color=WHITE, stroke_width=2)
        marks = VGroup()
        for k in ("3", "4", "7", "12"):
            m = d["limits"][k]
            marks.add(VGroup(Dot(g.ax.c2p(m, d["reference"]), radius=0.08, color=CURVE_C[k]),
                             label(tex(d["limit_names"][k].replace("#", "♯")), font_size=22, color=CURVE_C[k]).next_to(g.ax.c2p(m, d["reference"]), UP if k in ("4", "12") else DOWN, buff=0.15)))
        with self.voiceover(
            "Here is Part 5's roughness model, run for four intervals, with the lower note on every key "
            "from the bottom C to the top. <bookmark mark='a'/> Every curve climbs toward the bass. And "
            "the narrower the interval, the sooner it climbs: the minor third first, then the major "
            "third, then the fifth, and the octave last."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(curves[k]) for k in ("12", "7", "4", "3")], lag_ratio=0.4), FadeIn(legend), run_time=5.0)
        with self.voiceover(
            "Draw a line at the roughness of a major third on the C below middle C, which is about "
            "where arrangers stop writing thirds. <bookmark mark='a'/> To stay under that line, a minor "
            f"third must be no lower than {d['limit_names']['3'][0]}; a fifth can go down to F sharp, "
            "half an octave lower; and an octave lower still. <bookmark mark='b'/> Arrangers keep tables "
            "like this, called low-interval limits. Theirs differ by a few notes from book to book, and "
            "with the instrument: soft strings forgive more than loud brass. The shape is always this "
            "one. Thirds live in the middle of the keyboard; the bass belongs to octaves and fifths."
        ) as vo:
            self.play(Create(ref))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(label(r"low-interval limits", font_size=28, color=TUNE).next_to(legend, DOWN, buff=0.6)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spacing(self):
        d = load("voicing")
        c = clip("voicing.spread")
        t = d["bw_times"]
        kb = keys(36, 84, width=12.0, height=1.6).move_to(UP * 1.5)
        cards = VGroup(
            VGroup(label(r"the roughest", font_size=28, color=EAR), label(rf"{d['worst_roughness']:.1f}", font_size=30, color=WHITE)).arrange(DOWN, buff=0.12),
            VGroup(label(r"the smoothest", font_size=28, color=TUNE), label(rf"{d['best_roughness']:.1f}", font_size=30, color=WHITE)).arrange(DOWN, buff=0.12),
            VGroup(label(r"harmonics 1 to 6 of the low C", font_size=28, color=BLUE), label(r"octave, \ fifth, \ fourth, \ third, \ third", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=1.0).next_to(kb, DOWN, buff=0.55)
        head = label(rf"C major in four voices over a low C: \ {d['count']} ways", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The lesson for chords: wide at the bottom, close at the top. Monochord listed every way to "
            f"voice a C major triad in four parts above a low C. There are {say(d['count'])}. "
            "<bookmark mark='a'/> Ranked by roughness, the worst has all four notes crowded into the "
            "bottom octave. <bookmark mark='b'/> The best has a bare twelfth at the bottom and the third "
            "at the very top. <bookmark mark='c'/> And look at the harmonic series of the low C itself: "
            "an octave, then a fifth, a fourth, a third, each interval smaller than the one below. The "
            "best spacing imitates the way a single note is already built. Listen to all three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kb))
            vo.wait_until("a")
            for m in d["worst"]:
                kb.on(m, RED)
            self.play(FadeIn(cards[0]))
            vo.wait_until("b")
            kb.clear()
            for m in d["best"]:
                kb.on(m)
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            kb.clear()
            for m in d["series"]:
                kb.on(m, BLUE)
            self.play(FadeIn(cards[2]))
        kb.clear()
        with self.listen(c) as snd:
            window(snd, r"three spacings of one chord", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [d["worst"], d["best"], d["series"]], t, end=c.duration, colors=[RED, GOLD, BLUE])
            for k in range(3):
                pulse(snd, cards[k], t[k], t[k + 1] - 0.15 if k < 2 else c.duration, buff=0.15)
        kb.clear()
        with self.voiceover(
            f"By the model the first is {say(d['worst_roughness'] / d['best_roughness'])} times as rough "
            "as the second, and they are the same chord. Orchestration books give the rule in one "
            "line: space a chord the way the harmonic series spaces itself. The opening puzzle is "
            "solved. The mud was never in the chord. It was in where the chord was put."
        ):
            self.play(Indicate(cards[0], color=EAR), Indicate(cards[1], color=TUNE))
        self.wait(0.4)
        self.clear_scene()
