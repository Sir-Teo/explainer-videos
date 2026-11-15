from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


def slots_plot(a, b, f, width=10.5, height=2.6, center=ORIGIN, ca=EAR, cb=TUNE, top=None):
    """Two sets of levels at multiples of f/2 as paired stems (whole harmonics and the slots between)."""
    n = top or len(a)
    ax = frame_axes(width=width, height=height, xlo=0, xhi=n / 2 + 0.5, ylo=-60, yhi=0, center=center)
    j = np.arange(1, n + 1) / 2
    sa = stems(j - 0.06, np.array(a)[:n], ax.to, color=ca, r=0.045, base_y=-60)
    sb = stems(j + 0.06, np.array(b)[:n], ax.to, color=cb, r=0.045, base_y=-60)
    ticks = VGroup(*[label(f"{k:g}", font_size=13, color=GREY_A).next_to(ax.to(k, -60), DOWN, buff=0.08) for k in (0.5, 1, 2, 3, 4, 6, 8, 10, 12) if k <= n / 2])
    return VGroup(ax, ticks, sa, sb), sa, sb


class Fit(SoundScene):
    def construct(self):
        chapter(self, 10, r"Fitting a patch", r"Given a sound, \ which knobs make it?")
        self.inverse()
        self.distance()
        self.check()
        self.landscape()
        self.target()
        self.organ()
        self.limits()

    # ------------------------------------------------------------------
    def inverse(self):
        items = [
            (r"synthesis runs from knobs to sound; \ sound design often wants the reverse", WHITE),
            (r"a player hears a tone and asks: \ which oscillator, \ which cutoff, \ how much resonance?", WHITE),
            (r"for a computer: \ choose a distance between sounds, \ then search for the knobs that make it smallest", WHITE),
            (r"Part 41's orchestration solver did the same with instruments for knobs", WHITE),
            (r"the hook's patch was found this way: \ three knobs, \ 350 settings tried", TUNE),
        ]
        rows_scene(self, r"the inverse problem", items,
                   "Synthesis runs from knobs to sound. Sound design often wants the reverse. <bookmark mark='c'/> A player hears a "
                   "tone and asks: which oscillator, which cutoff, how much resonance? <bookmark mark='d'/> For a computer the recipe "
                   "is to choose a distance between sounds, then search for the knobs that make it smallest. <bookmark mark='e'/> "
                   "Part 41's orchestration solver did the same with instruments for knobs. <bookmark mark='f'/> The hook's patch "
                   "was found this way: three knobs, three hundred and fifty settings tried.", marks="cdef")

    # ------------------------------------------------------------------
    def distance(self):
        lines = VGroup(
            label(r"the patch: \ a sawtooth and a square, \ mixed by $m$, \ through the ladder at cutoff $f_c$ with feedback $k$", font_size=19, color=WHITE),
            label(r"each sound measured at every multiple of half its note: \ the harmonics, \ and the slots between them", font_size=19, color=WHITE),
            label(r"the slots between catch what a patch cannot make: \ an octave below, \ or a fifth below", font_size=17, color=GREY_A),
            label(r"levels in dB re the loudest, \ floored at $-60$", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.8)
        eq = MathTex(r"D = \sqrt{\frac{1}{|J|}\sum_{j \in J} \big(L_j^{\text{target}} - L_j^{\text{patch}}\big)^2}", font_size=36).to_edge(DOWN, buff=1.2)
        el = label(r"$J$: \ the slots where either sound has anything", font_size=16, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        head = label(r"a distance between two tones", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "First the knobs. <bookmark mark='a'/> Our patch is a sawtooth and a square, mixed by m, through the ladder at "
            "cutoff f c with feedback k. <bookmark mark='b'/> Then the distance. Measure each sound at every multiple of half "
            "its note: the harmonics, and the slots between them. The slots between catch what a patch like ours cannot make, "
            "such as a tone an octave below. Levels in decibels below the loudest, floored at minus sixty. "
            "<bookmark mark='c'/> The distance is the root-mean-square difference, in decibels, over the slots where either "
            "sound has anything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1:]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(el))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("fit")
        kn, rc = d["known"], d["recovered"]
        rows = VGroup(VGroup(label(r"patch", font_size=20, color=GREY_A), label(r"cutoff", font_size=20, color=GREY_A), label(r"feedback $k$", font_size=20, color=GREY_A), label(r"mix", font_size=20, color=GREY_A)),
                      VGroup(label(r"hidden", font_size=20, color=GREY_A), label(rf"{kn['cutoff']:.0f} Hz", font_size=22, color=WHITE), label(rf"{kn['res']:.1f}", font_size=22, color=WHITE), label(rf"{kn['mix']:.2f}", font_size=22, color=WHITE)),
                      VGroup(label(r"found", font_size=20, color=TUNE), label(rf"{rc['cutoff']:.0f} Hz", font_size=22, color=TUNE), label(rf"{rc['res']:.1f}", font_size=22, color=TUNE), label(rf"{rc['mix']:.2f}", font_size=22, color=TUNE))).arrange(DOWN, buff=0.45)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.2 + 2.9 * i)
        rows.move_to(UP * 0.3)
        res = label(rf"distance {rc['distance_db']:.2f} dB; \ cutoff off by {100 * (rc['cutoff'] / kn['cutoff'] - 1):+.1f}\%", font_size=20, color=WHITE).to_edge(DOWN, buff=1.2)
        why = label(r"the cutoff search is a grid of 14, \ then 9 finer steps: \ it lands on the nearest step", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"the search, \ checked", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Before trusting the search, check it on an answer we know. <bookmark mark='a'/> Make a sound with the patch itself, "
            "at fourteen hundred hertz, feedback two, an even mix, and hide the settings. <bookmark mark='b'/> The search finds "
            f"{say(rc['cutoff'])} hertz, feedback {say(rc['res'], 1)}, mix {say(rc['mix'], 2)}, at a distance of "
            f"{say(rc['distance_db'], 2)} decibels. <bookmark mark='c'/> The cutoff is off by {say(abs(100 * (rc['cutoff'] / kn['cutoff'] - 1)), 1)} "
            "per cent only because the search tries a grid of fourteen cutoffs and then nine finer steps, and lands on the "
            "nearest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landscape(self):
        d = load("fit")
        cuts, ress = d["cutoffs"], d["ress"]
        val = {(round(g[0], 3), g[1]): g[3] for g in d["grid"]}
        lo = min(g[3] for g in d["grid"])
        hi = max(g[3] for g in d["grid"])
        cw, ch = 0.62, 0.62
        cells = VGroup()
        best = None
        for i, c in enumerate(cuts):
            for j, r in enumerate(ress):
                v = val[(round(c, 3), r)]
                u = (np.log(v) - np.log(lo)) / (np.log(hi) - np.log(lo))
                sq = Square(side_length=cw * 0.94, stroke_width=0, fill_color=interpolate_color(ManimColor(TUNE), ManimColor("#1B1F2A"), u), fill_opacity=1.0)
                sq.move_to([-4.0 + cw * i, -1.6 + ch * j, 0])
                cells.add(sq)
                if best is None or v < best[0]:
                    best = (v, sq)
        mark = SurroundingRectangle(best[1], color=WHITE, buff=0.03, stroke_width=3)
        xt = VGroup(*[label(f"{c:.0f}", font_size=12, color=GREY_A).next_to(cells[i * len(ress)], DOWN, buff=0.1) for i, c in enumerate(cuts) if i % 3 == 0])
        yt = VGroup(*[label(f"{r:g}", font_size=14, color=GREY_A).next_to(cells[j], LEFT, buff=0.12) for j, r in enumerate(ress)])
        xl = label(r"cutoff, \ Hz", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yl = label(r"feedback $k$", font_size=15, color=GREY_A).next_to(yt, LEFT, buff=0.2).rotate(PI / 2)
        f = d["fit"]
        side = VGroup(label(r"distance to the hook's target", font_size=18, color=WHITE),
                      label(rf"bright: \ near, \ {lo:.1f} dB", font_size=16, color=TUNE),
                      label(rf"dark: \ far, \ up to {hi:.0f} dB", font_size=16, color=GREY_A),
                      label(rf"best: \ {f['cutoff']:.0f} Hz, \ $k = {f['res']:g}$, \ mix {f['mix']:g}", font_size=16, color=WHITE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"the landscape, \ at the best mix", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what the search saw for the hook's target, at the best mix: the distance for every cutoff and feedback "
            "it tried. <bookmark mark='a'/> Bright squares are close, dark ones far. The valley runs along the cutoff: too low "
            "and the patch is dull, too high and it is buzzy, with a broad good region between. <bookmark mark='b'/> The best "
            f"lies near {say(round(f['cutoff'], -2))} hertz with feedback {say(f['res'])}. With three knobs a grid is "
            "cheap; with thirty it would not be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.01), FadeIn(side[1:3]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def target(self):
        d = load("fit")
        g, sa, sb = slots_plot(d["spec"]["target"], d["spec"]["fit"], d["f"], top=30, center=DOWN * 0.4)
        xl = label(r"multiples of middle C", font_size=15, color=GREY_A).next_to(g, DOWN, buff=0.15)
        key = VGroup(label(r"target: \ forty sines", font_size=17, color=EAR), label(rf"patch: \ {d['fit']['distance_db']:.1f} dB away", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.1)
        t = d["spec"]["target"]
        p = d["spec"]["fit"]
        gap = max(t[j] - p[j] for j in (5, 7, 9))
        note = label(rf"the 3rd, \ 4th and 5th harmonics: \ the target's bump, \ up to {gap:.0f} dB above the patch", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"the hook's target, \ slot by slot", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Back to the hook, slot by slot. <bookmark mark='a'/> The target's harmonics, and the patch's beside them, with the "
            "empty slots between. <bookmark mark='b'/> Below the bump and above it the two agree within a few decibels. "
            f"<bookmark mark='c'/> At the third, fourth and fifth harmonics the target is up to {say(gap)} decibels louder: "
            "a ladder low-pass can make a peak at its cutoff, but not a broad hump with the highs still bright above it. The "
            "search settled for the best compromise, a cutoff above the bump. A peaking filter, Part 49's, would close the gap: "
            "a richer patch, one more knob."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(g[1]), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(sa), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(sb), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def organ(self):
        d = load("fit")
        c = clip("fit.organ")
        g, sa, sb = slots_plot(d["spec"]["organ"], d["spec"]["organ_fit"], d["f"], top=24, center=DOWN * 0.6, ca=BLUE)
        key = VGroup(label(r"Hammond, \ 888000000", font_size=17, color=BLUE), label(rf"best patch: \ {d['organ']['distance_db']:.0f} dB away", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.1)
        sub = SurroundingRectangle(VGroup(sa[0], sa[2]), color=GREY_A, buff=0.1, corner_radius=0.08)
        sl = label(r"16' \ and 5 1/3': \ below and between the note's harmonics", font_size=15, color=GREY_A).next_to(sub, UP, buff=0.12)
        boxes = choice_boxes([r"the organ", r"the best patch"], width=3.2, height=0.8, buff=1.4, size=20, colors=[BLUE, TUNE]).to_edge(DOWN, buff=0.3)
        head = label(r"a sound no setting can make", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Some targets are out of reach. <bookmark mark='a'/> Jimmy Smith's registration on middle C has tones at half the "
            "note, the sixteen-foot drawbar, and at one and a half times it, the fifth below the octave: slots that no "
            "filtered sawtooth or square on that note can fill. <bookmark mark='b'/> The best of three hundred and fifty settings "
            f"is {say(d['organ']['distance_db'])} decibels away. Hear the organ and the best patch."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(g[1]), FadeIn(sa), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(sub), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(sb), FadeIn(key[1]), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"organ, \ then patch", kind="synthesized", detail=r"middle C", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["organ"], st["patch"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["patch"], c.duration, buff=0.08)
        with self.voiceover(
            "The organ sits an octave lower than its key, round and deep; the patch is a bright, mostly square tone at the key's own "
            "pitch. A distance can say that a sound is out of reach, but not which module would bring it closer. Here the "
            "answer is a second oscillator an octave down: a change to the patch, not to its knobs."
        ):
            self.play(Indicate(sub, color=GREY_A, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"our distance hears only the steady spectrum: \ not the attack, \ not the envelope, \ not the movement", WHITE),
            (r"a grid grows exponentially: \ ten values each for 30 knobs is $10^{30}$ patches", WHITE),
            (r"genetic algorithms and other searches took over in the 1990s and 2000s", WHITE),
            (r"spectral distances have valleys that mislead: \ a patch an octave off can look nearer than one a semitone off", WHITE),
            (r"the frontier: \ learn the inverse directly, \ or make the synthesizer differentiable", TUNE),
        ]
        rows_scene(self, r"why fitting is hard", items,
                   "Fitting real synthesizers is harder in four ways. <bookmark mark='b'/> Our distance hears only the steady "
                   "spectrum: not the attack, not the envelope, not the movement. <bookmark mark='c'/> A grid grows exponentially: "
                   "ten values each for thirty knobs is ten to the thirtieth patches. <bookmark mark='d'/> So genetic algorithms "
                   "and other searches took over in the 1990s and 2000s. <bookmark mark='e'/> And spectral distances have valleys "
                   "that mislead: a patch an octave off can look nearer than one a semitone off. <bookmark mark='f'/> The frontier "
                   "learns the inverse directly, or makes the synthesizer itself differentiable.", marks="bcdef")
