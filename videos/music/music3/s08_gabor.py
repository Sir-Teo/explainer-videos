from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Gabor(SoundScene):
    def construct(self):
        chapter(self, 7, r"The limit", r"Can you know exactly when, \ and exactly what pitch?", lit=(1807,),
                extra=((1946, r"Gabor, \ ``Theory of communication''"),))
        self.two_windows()
        self.count()
        self.law()
        self.bursts()
        self.quiz()

    # ------------------------------------------------------------------
    def two_windows(self):
        d = load("gabor")
        ps = picture(d["pic_short"], -40, 0, 5.8, 3.0)
        pl = picture(d["pic_long"], -40, 0, 5.8, 3.0)
        Group(ps, pl).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.3)
        caps = VGroup(label(rf"a short stretch: \ {d['short_ms']:.0f} ms", font_size=28, color=TUNE).next_to(ps, UP, buff=0.15),
                      label(rf"a long stretch: \ {d['long_ms']:.0f} ms", font_size=28, color=AIR).next_to(pl, UP, buff=0.15))
        sig = label(rf"one sound: \ two clicks {d['clicks_ms']} ms apart, \ then two tones {d['tones_hz']} Hz apart", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        v1 = VGroup(label(r"two clicks: \ yes", font_size=24, color=GOOD), label(r"two tones: \ no, \ one blur", font_size=24, color=BAD)).arrange(DOWN, buff=0.08).next_to(ps, DOWN, buff=0.15)
        v2 = VGroup(label(r"two clicks: \ no, \ one smear", font_size=24, color=BAD), label(r"two tones: \ yes", font_size=24, color=GOOD)).arrange(DOWN, buff=0.08).next_to(pl, DOWN, buff=0.15)
        with self.voiceover(
            "In chapter two we found that telling two close notes apart takes a long stretch of sound. Here is the "
            "other side of that. One short test sound: two clicks, three hundredths of a second apart, and then "
            "two steady tones, forty hertz apart. <bookmark mark='a'/> Analyse it in short stretches. The two "
            "clicks stand apart cleanly, but the two tones have merged into one thick band. "
            "<bookmark mark='b'/> Analyse it in long stretches. Now the two tones are two sharp lines, and the "
            "clicks have smeared into one. <bookmark mark='c'/> No choice of stretch shows both. That is not a "
            "weakness of our method. It is a fact about waves."
        ) as vo:
            raw = Scope(width=10.4, height=2.4, color=AIR)
            sgn = np.asarray(d["signal"], dtype=float)
            raw.set_wave(np.clip(sgn, -2.4, 2.4), gain=0.4)
            rt = label(r"the test sound, \ as pressure against time", font_size=24, color=GREY_B).next_to(raw, DOWN, buff=0.15)
            self.play(FadeIn(sig), FadeIn(raw), FadeIn(rt))
            vo.wait_until("a")
            self.play(FadeOut(raw), FadeOut(rt), run_time=0.3)
            self.play(FadeIn(ps), FadeIn(caps[0]), FadeIn(v1))
            vo.wait_until("b")
            self.play(FadeIn(pl), FadeIn(caps[1]), FadeIn(v2))
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        head = label(r"Why? \ Count the cycles", font_size=38, color=TUNE).to_edge(UP, buff=0.45)
        g = axes([0, 1.0], [-1.2, 1.2], x_length=11.0, y_length=2.6, xlabel=r"seconds", ylabel=r"", xticks=[0, 0.1, 0.5, 1.0], yticks=[], font_size=20)
        g.move_to(UP * 0.4)
        t = np.linspace(0, 1, 1600)
        a = curve(g.ax, t, np.sin(2 * np.pi * 10 * t), TUNE, stroke_width=2.5)
        b = curve(g.ax, t, np.sin(2 * np.pi * 11 * t), AIR, stroke_width=2.5)
        leg = VGroup(label(r"10 cycles a second", font_size=24, color=TUNE), label(r"11 cycles a second", font_size=24, color=AIR)).arrange(RIGHT, buff=0.8).next_to(g, UP, buff=0.1)
        early = SurroundingRectangle(VGroup(Dot(g.ax.c2p(0, 1.1)), Dot(g.ax.c2p(0.1, -1.1))), color=BAD, buff=0.0, stroke_width=2.5)
        e_t = label(r"after a tenth of a second: \ still nearly in step", font_size=24, color=BAD).next_to(g, DOWN, buff=0.7).align_to(g, LEFT)
        late = SurroundingRectangle(VGroup(Dot(g.ax.c2p(0.9, 1.1)), Dot(g.ax.c2p(1.0, -1.1))), color=GOOD, buff=0.0, stroke_width=2.5)
        l_t = label(r"after a whole second: \ one has made exactly one more cycle", font_size=24, color=GOOD).next_to(e_t, DOWN, buff=0.2).align_to(g, LEFT)
        rule = MathTex(r"\text{to tell apart tones}\ \Delta f\ \text{hertz apart, \ listen for about}\ \frac{1}{\Delta f}\ \text{seconds}", font_size=34).to_edge(DOWN, buff=0.4)
        tag = label(r"illustrative: \ slowed two-hundredfold", font_size=18, color=GREY_C).next_to(g, RIGHT, buff=-2.6).shift(DOWN * 1.55)
        with self.voiceover(
            "The reason is almost embarrassingly simple. Here are two tones, one making ten cycles a second and "
            "one making eleven: slowed down so that we can count. <bookmark mark='a'/> Look at the first tenth of a "
            "second. They are nearly in step. Nothing you could measure in that time would tell them apart. "
            "<bookmark mark='b'/> You have to wait until one of them has pulled a whole cycle ahead of the other, "
            "and that takes a full second. <bookmark mark='c'/> To tell apart two tones one hertz apart, you must "
            "listen for about one second. Ten hertz apart, a tenth of a second. A frequency is a count of cycles, "
            "and counting takes time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(a), Create(b), FadeIn(leg), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(early), FadeIn(e_t))
            vo.wait_until("b")
            self.play(Create(late), FadeIn(l_t))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        d = load("gabor")
        thm = theorem_card(r"The uncertainty of time and frequency",
                           MathTex(r"\Delta t \;\cdot\; \Delta f \;\ge\; \frac{1}{4\pi}", font_size=48),
                           who=r"Dennis Gabor, 1946: \ the same mathematics as Heisenberg's principle", width=8.6, color=GOOD).to_edge(UP, buff=0.4)
        rows = VGroup(VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"shape", r"how long", r"how wide", r"times the limit")]))
        for r in d["rows"]:
            wide = rf"{r['times_floor']:.2f}" if r["times_floor"] < 2 else rf"{r['times_floor']:.0f}"
            rows.add(VGroup(label(r["name"], font_size=28), label(rf"{r['dt_ms']:.1f} ms", font_size=28, color=TIME),
                            label(rf"{r['df_hz']:.0f} Hz", font_size=28, color=FREQ),
                            label(wide, font_size=28, color=GOOD if r["times_floor"] < 1.1 else BAD)))
        xs = [-5.2, -1.2, 1.2, 3.6]
        for i, r in enumerate(rows):
            for cell, x in zip(r, xs):
                cell.move_to([x, -0.2 - 0.62 * i, 0], aligned_edge=LEFT)
        note_ = label(r"sharp edges are expensive: \ they need a very wide band of frequencies", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Dennis Gabor wrote the law down in 1946. Measure how long a sound lasts, and how wide a band of "
            "frequencies it occupies. Their product can never be smaller than one over four pi. "
            "<bookmark mark='a'/> A sound can be short, or it can be narrow in frequency. It cannot be both. The "
            "mathematics is the same as Heisenberg's uncertainty principle in quantum mechanics, and for the same "
            "reason: both are statements about waves. <bookmark mark='b'/> We measured the product for four "
            "shapes. A smooth bell curve sits exactly on the limit, and nothing can beat it. The Hann window is "
            "within three percent. <bookmark mark='c'/> Shapes with sharp edges are far worse."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bursts(self):
        d = load("gabor")
        c = clip("gabor.bursts")
        head = label(r"one tone, \ 440 Hz, \ shorter and shorter", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cols = VGroup()
        for b in d["bursts"]:
            sc = Scope(width=2.7, height=1.5, color=TUNE)
            t = np.linspace(-1, 1, 600)
            sigma = max(b["ms"] / 200.0, 0.012) * 0.5
            sc.set_wave(np.exp(-0.5 * (t / sigma) ** 2) * np.sin(2 * np.pi * 440 * b["ms"] / 1000 * t / (2 * sigma * 2)), gain=0.9)
            wide = Rectangle(width=min(2.7, max(0.08, 2.7 * b["semitones"] / 12.3)), height=0.3, stroke_width=0, fill_color=FREQ, fill_opacity=0.8)
            txt = VGroup(label(rf"{b['ms']} ms", font_size=28, color=TIME),
                         label(rf"{b['cycles']:.0f} cycles" if b["cycles"] >= 2 else r"barely one cycle", font_size=22, color=GREY_A))
            txt.arrange(DOWN, buff=0.08)
            spread = label(rf"spread over {b['semitones']:.1f} semitones" if b["semitones"] < 10 else r"spread over an octave", font_size=22, color=FREQ)
            cols.add(VGroup(txt, sc, wide, spread).arrange(DOWN, buff=0.22))
        cols.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to(DOWN * 0.3)
        with self.voiceover(
            "You can hear the limit. Take one tone, the A an orchestra tunes to, and make it shorter and shorter. "
            "At a fifth of a second it is plainly a note. <bookmark mark='a'/> At a twentieth it is still a note, "
            "though its frequency is already smeared over most of a semitone. <bookmark mark='b'/> At twelve "
            "thousandths of a second, five cycles, the smear is three semitones wide. <bookmark mark='c'/> At three "
            "thousandths it covers an octave. Each one twice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]))
            for mark, col in zip("abc", cols[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(col))
        with self.listen(c) as snd:
            window(snd, r"200, \ 50, \ 12 and 3 milliseconds of one tone", kind="synthesized", detail=r"one tone, shorter and shorter", corner=DL, tag_corner=UR)
            for b, col in zip(d["bursts"], cols):
                t0 = snd.time_of(f"b{b['ms']}")
                snd.wait_until(t0)
                frame = SurroundingRectangle(col, color=EAR, buff=0.12, stroke_width=3)
                snd.show(frame)
                end = t0 + 1.55
                snd.drive(frame, lambda m, t, t0=t0, end=end: m.set_stroke(opacity=(0.5 + 0.5 * np.cos(2 * PI * (t - t0) / 0.72)) if t0 <= t < end else 0.0))
                snd.wait_until(end)
        with self.voiceover(
            "The note turned into a click. Nothing was done to it except to make it short. A click is what a tone "
            "becomes when there is no time for it to have a pitch."
        ):
            self.play(Indicate(cols[-1], color=TUNE, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("gabor")
        c, e = clip("gabor.quiz"), clip("gabor.easy")
        q = listen_card(rf"Two pairs of very short tones, \ {d['quiz_ms']} ms each. \\ In one pair the two tones are the "
                        r"same. \ In the other they are a semitone apart. \ Which pair is the semitone?", width=10.4).to_edge(UP, buff=0.5)
        boxes = ab_boxes(y=0.0)
        with self.voiceover("A question for your ears. Two pairs of very short tones. In one pair, the two are the same "
                            "note. In the other they are a semitone apart. Which pair is the semitone?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))

        def run(cl, text):
            with self.listen(cl) as snd:
                window(snd, text, kind="synthesized", tag_corner=DR)
                for key, box, end in (("A", boxes[0], snd.time_of("B") - 0.3), ("B", boxes[1], cl.duration)):
                    t0 = snd.time_of(key)
                    snd.wait_until(t0)
                    glow_on(snd, box, t0, end)
                    snd.wait_until(end)
                    box[1].set_color(GREY_A)

        run(c, r"pair A, \ then pair B")
        with self.voiceover(
            f"It was {d['quiz_answer']}, and if you could not tell, that is the limit at work: at five thousandths "
            "of a second each tone is smeared over far more than a semitone. Here is the same question with tones "
            "twenty times longer."
        ):
            self.play(boxes[1][0].animate.set_stroke(GOOD, width=4))
        run(e, r"the same pairs, \ 120 ms each")
        cons = VGroup(label(r"a drum stroke: \ all time, \ no pitch", font_size=28, color=TIME),
                      label(r"an organ note: \ all pitch, \ no moment", font_size=28, color=FREQ),
                      label(r"fast low notes blur: \ there is not time for the ear, \ or any machine, \ to tell them apart", font_size=26, color=GREY_A)
                      ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Easy. So this limit runs through music. A drum stroke is all moment and no pitch. A held organ note is "
            "all pitch and no moment. <bookmark mark='a'/> And it is why fast passages low in the bass turn to mud: "
            "there is not time, for an ear or for any machine, to tell those notes apart."
        ) as vo:
            self.play(FadeIn(cons[0]), FadeIn(cons[1]))
            vo.wait_until("a")
            self.play(FadeIn(cons[2]))
        self.wait(0.3)
        self.clear_scene()
