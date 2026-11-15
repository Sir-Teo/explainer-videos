from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class Gating(SoundScene):
    def construct(self):
        chapter(self, 3, r"LUFS and gating", r"How do you measure the loudness of a whole song with one number?")
        self.formula()
        self.gates()
        self.checked()
        self.lra()
        self.units()

    # ------------------------------------------------------------------
    def formula(self):
        lines = VGroup(
            MathTex(r"z_c = \frac{1}{T}\int_{\text{block}} y_c^2(t)\,dt \qquad (\text{K-weighted channel } c,\ 400\ \text{ms blocks},\ 75\%\ \text{overlap})", font_size=28),
            MathTex(r"L_K = -0.691 + 10\log_{10}\sum_c G_c\, z_c \qquad (G = 1 \text{ for left, right, centre};\ 1.41 \text{ for the surrounds})", font_size=28),
            MathTex(r"\text{gate 1: drop blocks below } -70\ \text{LUFS}; \quad \text{gate 2: drop blocks 10 LU below what remains}", font_size=28),
            MathTex(r"\text{integrated loudness} = -0.691 + 10\log_{10}\Bigl(\text{mean of the surviving blocks' } \textstyle\sum_c G_c z_c\Bigr)", font_size=28, color=TUNE),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"BS.1770, \ in four lines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The rest of the meter is four lines. <bookmark mark='a'/> Cut the K-weighted signal into blocks of four hundred "
            "milliseconds, overlapping by three quarters, and take each channel's mean square in each block. "
            "<bookmark mark='b'/> Add the channels, with surround channels weighted by one point four one, take ten log ten, and "
            "subtract nought point six nine one, a constant that makes a one-kilohertz tone at full scale read about minus "
            "three. <bookmark mark='c'/> Then gate: drop every block below minus seventy, which is silence, and then every "
            "block more than ten units below the loudness of what remains, which is quiet passages. <bookmark mark='d'/> The "
            "integrated loudness is the level of the mean of the surviving blocks, in LUFS: loudness units relative to full "
            "scale. One LU is one decibel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gates(self):
        b = load("meters")["blocks"]
        t = np.array(b["t"])
        lk = np.array(b["lk"])
        kept = np.array(b["kept"])
        ax = frame_axes(width=10.4, height=3.2, xlo=0, xhi=t[-1] + 0.4, ylo=-80, yhi=0, center=DOWN * 0.4)
        dots = VGroup(*[Dot(ax.to(x, max(v, -79)), radius=0.035, color=TUNE if k else (GREY_D if v < b["abs"] else EAR)) for x, v, k in zip(t, lk, kept)])
        g1 = DashedLine(ax.to(0, b["abs"]), ax.to(t[-1] + 0.4, b["abs"]), color=GREY_A, stroke_width=2)
        g2 = DashedLine(ax.to(0, b["rel"]), ax.to(t[-1] + 0.4, b["rel"]), color=EAR, stroke_width=2)
        g1l = label(r"$-70$ LUFS: \ silence", font_size=14, color=GREY_A).next_to(g1, UP, buff=0.05).align_to(g1, RIGHT)
        g2l = label(rf"{b['rel']:.1f}: \ 10 LU below the ungated {b['ungated']:.1f}", font_size=14, color=EAR).next_to(g2, UP, buff=0.05).align_to(g2, RIGHT)
        il = DashedLine(ax.to(0, b["integrated"]), ax.to(t[-1] + 0.4, b["integrated"]), color=TUNE, stroke_width=3)
        ill = label(rf"integrated: \ {b['integrated']:.1f} LUFS", font_size=16, color=TUNE).next_to(il, UP, buff=0.05).align_to(il, LEFT)
        yt = VGroup(*[label(f"{v}", font_size=13, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (0, -20, -40, -60, -80)])
        xt = VGroup(*[label(f"{v} s", font_size=13, color=GREY_A).next_to(ax.to(v, -80), DOWN, buff=0.08) for v in range(0, int(t[-1]) + 1, 2)])
        note = label(r"our mix with 1.5 s of silence and a first phrase 14 dB quieter: \ each dot is one 400 ms block", font_size=16, color=WHITE).to_edge(DOWN, buff=0.3)
        head = label(r"the gates at work", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the gates at work, on our mix with a second and a half of silence in front and a first phrase fourteen "
            "decibels quieter than the rest. Each dot is one block. <bookmark mark='a'/> The silent blocks fall below minus "
            "seventy and are dropped. <bookmark mark='b'/> The quiet phrase's blocks fall more than ten units below the "
            f"loudness of the rest and are dropped too. <bookmark mark='c'/> What remains reads {say(-b['integrated'], 1)} "
            f"below full scale, where without gates it would read {say(-b['ungated'], 1)}: the song's loudness is the loudness "
            "of its music, not of its pauses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xt), FadeIn(dots), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(g1), FadeIn(g1l))
            vo.wait_until("b")
            self.play(Create(g2), FadeIn(g2l))
            vo.wait_until("c")
            self.play(Create(il), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checked(self):
        d = load("meters")["checks"]
        rows = VGroup(VGroup(*[label(h, font_size=16, color=GREY_A) for h in (r"signal", r"integrated: \ ours", r"ffmpeg", r"true peak: \ ours", r"ffmpeg", r"LRA: \ ours", r"ffmpeg")]))
        for r in d:
            rows.add(VGroup(label(r["name"], font_size=17, color=WHITE), label(f"{r['ours_I']:.1f}", font_size=17, color=TUNE), label(f"{r['ffmpeg_I']:.1f}", font_size=17, color=WHITE),
                            label(f"{r['ours_TP']:.1f}", font_size=17, color=TUNE), label(f"{r['ffmpeg_TP']:.1f}", font_size=17, color=WHITE),
                            label(f"{r['ours_LRA']:.1f}", font_size=17, color=TUNE), label(f"{r['ffmpeg_LRA']:.1f}", font_size=17, color=WHITE)))
        rows.arrange(DOWN, buff=0.3)
        xs = [-5.0, -2.6, -1.2, 0.6, 2.0, 3.8, 5.2]
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(xs[i])
        rows.move_to(DOWN * 0.1)
        dI = max(abs(r["ours_I"] - r["ffmpeg_I"]) for r in d)
        dT = max(abs(r["ours_TP"] - r["ffmpeg_TP"]) for r in d)
        note = label(rf"integrated within {dI:.2f} LU, \ true peak within {dT:.1f} dB \ (ffmpeg rounds to 0.1); \ LRA within 0.4 LU, \ whose histogram method differs", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"Monochord's meter against ffmpeg's", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The series has used this meter since Part 1, to set the level of every example. <bookmark mark='a'/> Here it is "
            "checked against ffmpeg's EBU R 128 meter, which shares none of its code, on four signals. <bookmark mark='b'/> The "
            "integrated loudness agrees to a few hundredths, the true peak to a tenth, which is how finely ffmpeg prints it, and "
            "the loudness range, which the two compute by different histograms, to within half a unit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lra(self):
        d = load("meters")["checks"]
        q = [r for r in d if r["name"] == "quiet start"][0]
        m = [r for r in d if r["name"] == "the mix"][0]
        items = [
            (r"momentary loudness: \ 400 ms; \ short-term: \ 3 s; \ integrated: \ the whole programme", WHITE),
            (r"loudness range \ (LRA, \ EBU Tech 3342): \ the spread of the short-term levels, \ 10th to 95th percentile, \ gated", WHITE),
            (rf"our steady mix: \ {m['ours_LRA']:.1f} LU; \ the same with a quiet first phrase: \ {q['ours_LRA']:.1f} LU", WHITE),
            (r"LRA measures the song's dynamics, \ verse against chorus; \ the peak-to-loudness ratio \ (PLR) \ measures the hits'", TUNE),
        ]
        rows_scene(self, r"three time scales, \ and a range", items,
                   "The standard has three time scales. <bookmark mark='b'/> Momentary loudness over four hundred milliseconds, "
                   "short-term over three seconds, and integrated over the whole programme. <bookmark mark='c'/> And EBU Tech 3342 "
                   "adds the loudness range: the spread of the short-term levels, from the tenth to the ninety-fifth percentile, "
                   f"after gating. <bookmark mark='d'/> Our steady mix has a range of {say(m['ours_LRA'], 1)} units; with its first "
                   f"phrase fourteen decibels quieter, {say(q['ours_LRA'], 1)}. <bookmark mark='e'/> The loudness range measures a "
                   "song's dynamics, verse against chorus; the peak-to-loudness ratio, true peak minus integrated loudness, measures "
                   "its hits. Remember the two: the loudness war will treat them very differently.", marks="bcde")

    # ------------------------------------------------------------------
    def units(self):
        rows = VGroup(VGroup(label(r"standard", font_size=17, color=GREY_A), label(r"target", font_size=17, color=GREY_A), label(r"peak ceiling", font_size=17, color=GREY_A)))
        data = [(r"EBU R 128 \ (European broadcast, \ 2010)", r"$-23$ LUFS", r"$-1$ dBTP"), (r"ATSC A/85 \ (US broadcast)", r"$-24$ LKFS", r"$-2$ dBTP"),
                (r"AES TD1004 \ (streaming, \ 2015)", r"$-16$ to $-20$ LUFS", r"$-1$ dBTP"), (r"music streaming services", r"about $-14$ to $-16$ LUFS", r"$-1$ to $-2$ dBTP"),
                (r"this series' narration", r"$-16$ LUFS", r"$-1$ dBTP")]
        for a, b_, c_ in data:
            rows.add(VGroup(label(a, font_size=18, color=WHITE), label(b_, font_size=18, color=TUNE), label(c_, font_size=18, color=WHITE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].set_x(-3.0)
            r[1].set_x(1.8)
            r[2].set_x(4.6)
        rows.move_to(DOWN * 0.1)
        head = label(r"targets", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "With a meter, regulators and services could set targets. <bookmark mark='a'/> European broadcasting adopted EBU "
            "R 128 in 2010: programmes at minus twenty-three LUFS, true peaks under minus one. American broadcast uses minus "
            "twenty-four, under the name LKFS. The AES recommends minus sixteen to minus twenty for streaming; music services "
            "play at about minus fourteen to minus sixteen. <bookmark mark='b'/> And this series' narration sits at minus "
            "sixteen, the usual figure for online video."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:5]], lag_ratio=0.25), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
