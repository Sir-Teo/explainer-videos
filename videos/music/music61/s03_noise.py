from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Noise(SoundScene):
    def construct(self):
        chapter(self, 2, r"Pitch in noise", r"How much noise can a pitch tracker take?")
        self.tracks()
        self.curve()
        self.lessons()

    # ------------------------------------------------------------------
    def tracks(self):
        d = load("pitch")
        c = clip("pitch.three")
        panels = VGroup()
        for i, (k, name) in enumerate((("20", r"noise 20 dB down"), ("0", r"noise as loud as the voice"), ("-10", r"noise 10 dB louder"))):
            tr = d["tracks"][k]
            t, f0, truth = np.array(tr["t"]), np.array(tr["f0"]), np.array(tr["truth"])
            ax = frame_axes(width=3.6, height=2.4, xlo=0, xhi=t[-1], ylo=50, yhi=85, center=[-4.2 + 4.2 * i, -0.1, 0])
            m_true = 69 + 12 * np.log2(np.where(np.isfinite(truth), truth, np.nan) / 440)
            m_est = 69 + 12 * np.log2(np.clip(f0, 30, 3000) / 440)
            true_dots = VGroup(*[Dot(ax.to(a, b), radius=0.035, color=GREY_B) for a, b in zip(t, m_true) if np.isfinite(b)][::2])
            est_dots = VGroup(*[Dot(ax.to(a, min(max(b, 50), 85)), radius=0.03, color=TUNE) for a, b in zip(t, m_est) if np.isfinite(b)][::2])
            panels.add(VGroup(ax, true_dots, est_dots, label(name, font_size=15, color=WHITE).next_to(ax, UP, buff=0.12)))
        key = label(r"grey: \ the notes sung; \ gold: \ YIN's estimate, \ frame by frame", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"one voice, \ three noise levels", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is Part 8's voice singing the Tune's opening, with white noise twenty decibels down, as loud as the voice, and ten decibels louder. Watch YIN's estimates against the notes sung."):
            self.play(FadeIn(head), FadeIn(VGroup(*[VGroup(p[0], p[1], p[3]) for p in panels])), FadeIn(key))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"20, \ 0, \ $-10$ dB", kind="physical model", detail=r"Part 8's voice, \ white noise", corner=DL, tag_corner=DR)
            ks = ["s20", "s0", "sm10"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                snd.show(panels[i][2])
                snd.drive(panels[i][2], lambda m, t, s0=st[k]: m.set_opacity(min(1.0, max(0.0, (t - s0) / 0.6))))
                pulse(snd, panels[i][0], st[k], end, buff=0.12)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("pitch")
        rows = d["rows"]
        snr = [r["snr"] for r in rows]
        ax = frame_axes(width=8.6, height=3.4, xlo=-10, xhi=30, ylo=0, yhi=1, center=DOWN * 0.4 + LEFT * 0.7)
        cy = curve(snr, [r["yin"] for r in rows], ax.to, color=TUNE, width=3.5)
        ca = curve(snr, [r["acf"] for r in rows], ax.to, color=BLUE, width=3.5)
        dots = VGroup(*[Dot(ax.to(r["snr"], r["yin"]), radius=0.06, color=TUNE) for r in rows], *[Dot(ax.to(r["snr"], r["acf"]), radius=0.06, color=BLUE) for r in rows])
        xt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (-10, 0, 10, 20, 30)])
        yt = VGroup(*[label(f"{int(100 * v)}\\%", font_size=14, color=GREY_A).next_to(ax.to(-10, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        key = VGroup(label(r"YIN", font_size=17, color=TUNE), label(r"plain autocorrelation", font_size=17, color=BLUE),
                     label(r"of frames wrong by more than 20\%", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        r20 = [r for r in rows if r["snr"] == 20][0]
        note = label(rf"at 20 dB: \ median errors {r20['yin_cents']:.0f} and {r20['acf_cents']:.0f} cents", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"gross errors against noise", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        r0 = [r for r in rows if r["snr"] == 0][0]
        rm = [r for r in rows if r["snr"] == -10][0]
        with self.voiceover(
            f"Now count. <bookmark mark='a'/> The share of frames that YIN gets wrong by more than twenty percent, a gross pitch error under this twenty-percent threshold, which also includes smaller-than-octave errors, against the noise. Clean, almost none; with the noise as loud as the voice, {say(100 * r0['yin'])} percent; ten decibels louder, {say(100 * rm['yin'])}. <bookmark mark='b'/> The plain autocorrelation of the same frames does {('better' if rm['acf'] < rm['yin'] else 'worse')} in heavy noise: {say(100 * rm['acf'])} percent at minus ten. It averages over the whole frame, and white noise has no period to confuse it, while YIN's threshold, designed for clean speech, finds no dip and has to guess."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(cy), FadeIn(dots[:len(rows)]), FadeIn(key[0]), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ca), FadeIn(dots[len(rows):]), FadeIn(key[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lessons(self):
        items = [
            (r"no single method wins everywhere: \ YIN is accurate and cheap on clean sound; \ averaging helps in noise", WHITE),
            (r"real noise is worse than white: \ other voices, \ other instruments, \ reverberation, \ all with periods of their own", WHITE),
            (r"later methods track pitch over time: \ probabilistic YIN \ (2014) \ keeps several candidates and chooses a smooth path", WHITE),
            (r"CREPE \ (2018): \ a network trained on rendered audio with known pitch, \ like Monochord's", WHITE),
            (r"measure on the noise you will meet, \ with an answer key", TUNE),
        ]
        rows_scene(self, r"what it means", items,
                   "The lessons. <bookmark mark='b'/> No single method wins everywhere: YIN is accurate and cheap on clean sound, and averaging helps in noise. <bookmark mark='c'/> Real noise is worse than white: other voices, other instruments and reverberation, all with periods of their own. <bookmark mark='d'/> Later methods track pitch over time: probabilistic YIN, in 2014, keeps several candidates in each frame and chooses a smooth path through them. <bookmark mark='e'/> CREPE, in 2018, is a network trained on several pitch-annotated datasets, including recorded and synthesized material; our teaching network is trained on one synthetic instrument. <bookmark mark='f'/> And the method that matters: measure on the noise you will meet, with an answer key.", marks="bcdef")
