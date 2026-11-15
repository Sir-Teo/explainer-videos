from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403

LCOL = {"0.0": GREY_A, "-3.0": TUNE, "-4.5": BLUE, "-6.0": EAR}


def box(text, color=GREY_B, w=1.5, h=0.7, size=16):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5), label(text, font_size=size, color=color))


class Balance(SoundScene):
    def construct(self):
        chapter(self, 6, r"Balance and panning", r"What does a mixing console actually do?")
        self.strip()
        self.faders()
        self.laws()
        self.mono()
        self.ours()

    # ------------------------------------------------------------------
    def strip(self):
        names = [(r"input \ and gain", GREY_A), (r"high-pass", WHITE), (r"equalizer", WHITE), (r"compressor", WHITE), (r"fader", TUNE), (r"pan", TUNE)]
        chain = VGroup(*[box(n, c_) for n, c_ in names]).arrange(RIGHT, buff=0.35).move_to(UP * 1.0)
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(len(chain) - 1)])
        sends = box(r"sends", BLUE).next_to(chain[4], DOWN, buff=0.9)
        sa = Arrow(chain[4].get_bottom(), sends.get_top(), buff=0.05, color=BLUE, stroke_width=3)
        buses = box(r"reverb and echo buses", BLUE, w=3.2).next_to(sends, RIGHT, buff=0.8)
        ba = Arrow(sends.get_right(), buses.get_left(), buff=0.05, color=BLUE, stroke_width=3)
        master = box(r"stereo bus, \ master", EAR, w=2.6).next_to(chain[5], DOWN, buff=2.2).shift(RIGHT * 0.6)
        ma = VGroup(Arrow(chain[5].get_bottom(), master.get_top(), buff=0.05, color=EAR, stroke_width=3), Arrow(buses.get_bottom(), master.get_left() + UP * 0.1, buff=0.05, color=EAR, stroke_width=3))
        note = label(r"Monochord's console: \ \texttt{studio.Channel} and \texttt{studio.mix}", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"one channel of a console", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A mixing console is many copies of one channel. <bookmark mark='a'/> The input sets the gain; a high-pass filter "
            "removes rumble below the instrument; the equalizer shapes its spectrum with Part 49's biquads; a compressor, "
            "Part 50's, tames its level. <bookmark mark='b'/> Then the fader sets how loud it is in the mix, and the pan "
            "where. <bookmark mark='c'/> Sends tap the signal after the fader to shared buses, a reverb or an echo, so that "
            "many channels share one room. <bookmark mark='d'/> And everything meets on the stereo bus, the master. Monochord's "
            "console does exactly this, channel by channel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(chain, sends, buses, master), 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(chain[:4]), FadeIn(arrows[:3]))
            vo.wait_until("b")
            self.play(FadeIn(chain[4:]), FadeIn(arrows[3:]))
            vo.wait_until("c")
            self.play(FadeIn(sends), FadeIn(sa), FadeIn(buses), FadeIn(ba))
            vo.wait_until("d")
            self.play(FadeIn(master), FadeIn(ma), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def faders(self):
        items = [
            (r"a fader is calibrated in decibels: \ 0 is unity, \ $-10$ dB is about half as loud \ (Part 4's sones), \ $-\infty$ is off", WHITE),
            (r"balance is the first act of a mix: \ which part leads, \ which supports, \ which is felt rather than heard", WHITE),
            (r"one common way: \ the voice first, \ then the kick and bass that carry the groove, \ then the rest around them", WHITE),
            (r"a balance is a ranking, \ and every ranking is a choice: \ the three mixes of the hook are three rankings", TUNE),
        ]
        rows_scene(self, r"faders", items,
                   "The faders come first. <bookmark mark='b'/> A fader is calibrated in decibels: nought is unity, minus ten is "
                   "about half as loud, by Part 4's sones, and minus infinity is off. <bookmark mark='c'/> Balance is the first act "
                   "of a mix: which part leads, which supports, which is felt rather than heard. <bookmark mark='d'/> One common "
                   "way is to set the voice first, then the kick and bass that carry the groove, then the rest around them. "
                   "<bookmark mark='e'/> A balance is a ranking, and every ranking is a choice: the hook's three mixes were three "
                   "rankings of the same parts.", marks="bcde")

    # ------------------------------------------------------------------
    def laws(self):
        d = load("pan")
        p = np.array(d["p"])
        a1 = frame_axes(width=5.0, height=2.6, xlo=-1, xhi=1, ylo=0, yhi=1.05, center=LEFT * 3.3 + DOWN * 0.3)
        a2 = frame_axes(width=5.0, height=2.6, xlo=-1, xhi=1, ylo=-7, yhi=4, center=RIGHT * 3.3 + DOWN * 0.3)
        g = VGroup(*[curve(p, d["laws"][k]["gL"], a1.to, color=LCOL[k], width=2.5) for k in LCOL])
        pw = VGroup(*[curve(p, d["laws"][k]["stereo_db"], a2.to, color=LCOL[k], width=2.5) for k in LCOL])
        t1 = label(r"the left channel's gain", font_size=17, color=GREY_A).next_to(a1, UP, buff=0.15)
        t2 = label(r"total power in stereo, \ dB", font_size=17, color=GREY_A).next_to(a2, UP, buff=0.15)
        xt = VGroup(*[VGroup(label(r"left", font_size=13, color=GREY_A).next_to(a.to(-1, lo), DOWN, buff=0.08), label(r"right", font_size=13, color=GREY_A).next_to(a.to(1, lo), DOWN, buff=0.08))
                      for a, lo in ((a1, 0), (a2, -7))])
        yt = VGroup(*[label(f"{v:+d}" if v else "0", font_size=13, color=GREY_A).next_to(a2.to(-1, v), LEFT, buff=0.08) for v in (3, 0, -3, -6)])
        key = VGroup(*[label(rf"{float(k):g} dB in the centre", font_size=16, color=LCOL[k]) for k in LCOL]).arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.0)
        head = label(r"four pan laws", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 55 compared two pan laws; consoles offer four. <bookmark mark='a'/> They differ in how much a centred sound "
            "is turned down in each channel: nought decibels, a plain balance control; minus three, constant power; minus six, "
            "constant amplitude; and minus four and a half, between the two. <bookmark mark='b'/> In stereo, only the minus "
            "three law keeps the total power the same as a sound moves; the others bulge or sag by up to three decibels in the "
            "middle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(a1), FadeIn(a2), FadeIn(t1), FadeIn(t2), FadeIn(xt), FadeIn(yt), FadeIn(ghost(VGroup(g, pw), 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in g], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in pw], lag_ratio=0.3), run_time=1.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mono(self):
        d = load("pan")
        rows = VGroup(VGroup(label(r"law", font_size=17, color=GREY_A), label(r"centre, \ each side", font_size=17, color=GREY_A),
                             label(r"centre in stereo", font_size=17, color=GREY_A), label(r"centre in mono", font_size=17, color=GREY_A)))
        for k in LCOL:
            v = d["laws"][k]
            rows.add(VGroup(label(rf"{float(k):g} dB", font_size=19, color=LCOL[k]), label(rf"{v['centre_db']:+.1f} dB", font_size=19, color=WHITE),
                            label(rf"{v['centre_stereo_db']:+.1f} dB", font_size=19, color=WHITE), label(rf"{v['centre_mono_db']:+.1f} dB", font_size=19, color=WHITE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.5 + 3.0 * i)
        rows.move_to(UP * 0.2)
        note = label(r"each relative to the same sound panned hard to one side; \ mono is $(L + R)/2$, \ as on a phone or a radio", font_size=17, color=GREY_A).next_to(rows, DOWN, buff=0.4)
        head = label(r"stereo against mono", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "But mixes are also heard in mono, on phones, radios and shop speakers, where the two channels are added. "
            "<bookmark mark='a'/> Then a centred sound under the minus three law comes out three decibels louder than the same "
            "sound panned to one side, while under the minus six law it comes out the same. <bookmark mark='b'/> No law is "
            "right both ways: minus three is true in stereo, minus six in mono, and minus four and a half splits the "
            "difference. Broadcast consoles often use minus six; music consoles minus three or four and a half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        from videos.music.music56.compute import CARVE, TRACKS
        cols = {"vox": TUNE, "piano": BLUE, "guitar": "#A3E635", "bass": EAR, "kick": GREY_A, "snare": GREY_A, "hat": GREY_A}
        strips = VGroup()
        for i, k in enumerate(TRACKS):
            g, p, hpf, eq = CARVE[k]
            x = -5.4 + 1.8 * i
            slot = Line([x, -2.2, 0], [x, 1.2, 0], color=GREY_D, stroke_width=6)
            yv = -2.2 + 3.4 * (g + 12) / 18
            cap = Rectangle(width=0.5, height=0.22, fill_color=cols[k], fill_opacity=1, stroke_width=0).move_to([x, yv, 0])
            knob = Circle(radius=0.25, stroke_color=GREY_B, stroke_width=2).move_to([x, 2.0, 0])
            ang = -p * 2.4
            needle = Line(knob.get_center(), knob.get_center() + 0.25 * np.array([np.sin(-ang), np.cos(ang), 0]), color=cols[k], stroke_width=3)
            nm = label(k, font_size=17, color=cols[k]).move_to([x, -2.65, 0])
            vals = label(rf"{g:+.0f} dB", font_size=13, color=WHITE).next_to(cap, RIGHT, buff=0.08)
            strips.add(VGroup(slot, cap, knob, needle, nm, vals))
        pl = label(r"pan", font_size=14, color=GREY_A).move_to([-6.5, 2.0, 0])
        note = label(r"the close-and-dry mix: \ the voice up, \ piano left, \ guitar right, \ bass, \ kick and snare in the centre", font_size=17, color=WHITE).to_edge(DOWN, buff=0.2)
        head = label(r"our faders and pans", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here are our own faders and pans for the close-and-dry mix. <bookmark mark='a'/> The voice a decibel up and in "
            "the centre; the piano half left and the guitar half right, so that they flank the voice; bass, kick and snare in "
            "the centre, where the low end belongs, because it must survive mono and both loudspeakers share the work; the "
            "hi-hat a little right, as a drummer would see it from the audience. The equalizers come next, because they are "
            "about masking."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pl), FadeIn(ghost(strips, 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in strips], lag_ratio=0.15), FadeIn(note), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
