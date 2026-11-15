from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Stereo(SoundScene):
    def construct(self):
        chapter(self, 2, r"Where things are panned", r"Can two channels be played against each other?")
        self.cancel()
        self.heard()
        self.index()
        self.panmap()

    # ------------------------------------------------------------------
    def cancel(self):
        lines = VGroup(
            MathTex(r"L = \sum_j \sin\theta_j\, s_j, \qquad R = \sum_j \cos\theta_j\, s_j", font_size=34, color=WHITE),
            label(r"a source in the centre, \ $\theta = 45^\circ$, \ is identical in both channels", font_size=20, color=WHITE),
            MathTex(r"L - R = \sum_j (\sin\theta_j - \cos\theta_j)\, s_j", font_size=34, color=TUNE),
            label(r"so subtracting the channels removes it exactly: \ the old trick of karaoke machines", font_size=20, color=WHITE),
            label(r"it also removes everything else in the centre: \ the bass, \ the kick drum", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"centre cancellation", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Stereo gives a first handle. <bookmark mark='a'/> Each source is panned by an angle: some of it in the left "
            "channel, some in the right. <bookmark mark='b'/> A source in the centre is identical in both. "
            "<bookmark mark='c'/> So subtract the channels, <bookmark mark='d'/> and it vanishes exactly: the old trick of "
            "karaoke machines, which removed a centred singer. <bookmark mark='e'/> It also removes everything else in the "
            "centre: the bass and the kick drum go with the voice."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("pan")
        c = clip("pan.three")
        boxes = choice_boxes([r"stereo", r"left minus right", r"the piano's bins"], width=3.4, height=0.9, buff=0.5, size=19).move_to(UP * 0.5)
        note = label(rf"left minus right is {-d['side_level_db']:.0f} dB quieter: \ the centred voice, \ bass and drums are gone; \ the panned piano and guitar remain",
                     font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"stereo, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the session in stereo; then left minus right; then only the time-frequency bins panned where the piano is. Headphones help."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"stereo tricks", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            ks = ["stereo", "side", "piano"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        with self.voiceover("Left minus right keeps only what is panned: the piano and guitar, with the voice, bass and drums gone. The piano's bins hold mostly piano, with traces of whatever shared its frequencies."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def index(self):
        d = load("pan")
        items = [
            (r"per time-frequency bin, \ a panning index: \ $(|L| - |R|) / (|L| + |R|)$, \ from $-1$ \ (right) \ to $+1$ \ (left)", WHITE),
            (r"a source panned to one place lights the bins with that index \ (Avendano, \ 2003)", WHITE),
            (rf"the piano's bins: \ {d['sdr_piano']:.1f} dB SDR: \ where piano and guitar share a bin, \ the index lies between them", WHITE),
            (r"it fails for sources panned to the same place, \ and in the centre, \ where most voices are", TUNE),
        ]
        rows_scene(self, r"selecting by panning", items,
                   "The idea generalizes. <bookmark mark='b'/> In every time-frequency bin, compute a panning index, from minus one "
                   "for hard right to plus one for hard left. <bookmark mark='c'/> A source panned to one place lights the bins with "
                   "that index, as Carlos Avendano showed in 2003. <bookmark mark='d'/> Selecting the piano's bins gives the piano at "
                   f"{say(d['sdr_piano'], 1)} decibels, by the measure of Chapter 9: where piano and guitar share a bin, its index "
                   "falls between them. <bookmark mark='e'/> And it fails for sources panned to the same place, above all the centre, "
                   "where most voices are.", marks="bcde")

    # ------------------------------------------------------------------
    def panmap(self):
        d = load("panmap")
        x = np.array(d["centres"])
        e = 10 * np.log10(np.maximum(np.array(d["energy"]), 1e-4))
        ax = frame_axes(width=10.0, height=3.2, xlo=-1, xhi=1, ylo=-40, yhi=0, center=DOWN * 0.4)
        cv = curve(x, e, ax.to, color=TUNE, width=3)
        xl = VGroup(label(r"$-1$: \ hard right", font_size=14, color=GREY_A).move_to(ax.to(-0.85, -40) + DOWN * 0.3),
                    label(r"0: \ centre", font_size=14, color=GREY_A).move_to(ax.to(0, -40) + DOWN * 0.3),
                    label(r"$+1$: \ hard left", font_size=14, color=GREY_A).move_to(ax.to(0.85, -40) + DOWN * 0.3))
        yl = label(r"energy in bins with that index \ (dB)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        names = {"piano": (r"piano", BLUE), "guitar": (r"guitar", EAR), "hat": (r"hi-hat", GREY_B)}
        marks = VGroup()
        for k, (t, col) in names.items():
            w = d["where"][k]
            marks.add(VGroup(DashedLine(ax.to(w, -40), ax.to(w, 0), color=col, stroke_width=2), label(t, font_size=15, color=col).move_to(ax.to(w, 0) + UP * 0.25)))
        cen = label(r"voice, \ bass, \ kick, \ snare: \ all near 0", font_size=15, color=TUNE).move_to(ax.to(0, -8) + RIGHT * 2.2)
        head = label(r"the session, \ bin by bin", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the session's panning, bin by bin: how much energy sits at each panning index. <bookmark mark='a'/> Most "
            "of it is in the centre, where the voice, bass, kick and snare are. <bookmark mark='b'/> The rest spreads into "
            "broad shoulders, toward the piano on the left and the guitar and hi-hat on the right. They are broad because most "
            "bins hold more than one source, and a shared bin's index falls between its sources' places. So panning selects "
            "the piano only roughly, and the tall peak in the middle holds four sources it cannot tell apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(cv), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(cen))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
