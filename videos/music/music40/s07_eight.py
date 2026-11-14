from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


class Eight(SoundScene):
    def construct(self):
        chapter(self, 6, r"The drum machine", r"How do you build a drum from a circuit?")
        self.history()
        self.kick()
        self.hear_kick()
        self.tuned()
        self.hat()
        self.kit()
        self.legacy()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1980: \ the Roland TR-808, \ an analog drum machine with a step sequencer", WHITE),
            (r"its sounds were nothing like real drums, \ and it sold poorly; \ second-hand prices fell", WHITE),
            (r"cheap, \ it reached young producers: \ electro, \ hip hop, \ Miami bass, \ then trap", WHITE),
            (r"Marvin Gaye's \textit{Sexual Healing} \ (1982) \ made it a sound of the charts", TUNE),
            (r"every sound is a small analog circuit: \ we build them from the same principles", GREY_A),
        ]
        rows_scene(self, r"the 808", items,
                   "In 1980 Roland released the TR-808, an analog drum machine with a step sequencer. <bookmark mark='b'/> Its "
                   "sounds were nothing like real drums, it sold poorly, and second-hand prices fell. <bookmark mark='c'/> Cheap, "
                   "it reached young producers, and became the sound of electro, hip hop, Miami bass, and much later trap. "
                   "<bookmark mark='d'/> Marvin Gaye's Sexual Healing, in 1982, made it a sound of the charts. "
                   "<bookmark mark='e'/> Each of its sounds is a small analog circuit, and we can build them from the same "
                   "principles.", marks="bcde")

    # ------------------------------------------------------------------
    def kick(self):
        d = load("eight")
        x0, W = -5.6, 5.6
        t = np.linspace(0, 0.5, 400)
        f0 = 52.0
        freq = f0 * (1 + 0.6 * np.exp(-t / 0.02))
        phase = 2 * np.pi * np.cumsum(freq) * (t[1] - t[0])
        y = np.sin(phase) * np.exp(-t / 0.45)
        wave = VMobject(color=TUNE, stroke_width=2).set_points_as_corners([[x0 + W * tt / 0.5, 0.6 + 1.2 * v, 0] for tt, v in zip(t, y)])
        axis = Line([x0, 0.6, 0], [x0 + W, 0.6, 0], color=GREY_D)
        fl = VMobject(color=EAR, stroke_width=3).set_points_as_corners([[x0 + W * tt / 0.5, -2.0 + 0.012 * (fr - 40), 0] for tt, fr in zip(t, freq)])
        fax = Line([x0, -2.0, 0], [x0 + W, -2.0, 0], color=GREY_D)
        labs = VGroup(label(r"the kick: \ a damped sine", font_size=18, color=TUNE).move_to([x0 + 1.4, 2.2, 0]),
                      label(r"its frequency: \ 81 Hz at the strike, \ 52 Hz within 20 ms", font_size=18, color=EAR).move_to([x0 + 2.2, -0.6, 0]),
                      label(r"0.5 s", font_size=15, color=GREY_A).move_to([x0 + W, 0.3, 0]))
        side = VGroup(label(r"the 808's bass drum: \ a resonant network \ (bridged-T) \ struck by a pulse", font_size=19, color=WHITE),
                      label(r"a struck resonator rings at its own frequency and dies away: \ Part 1's string, \ one mode", font_size=19, color=WHITE),
                      label(r"the strike briefly detunes it: \ a fast downward sweep, \ heard as punch", font_size=19, color=TUNE),
                      label(rf"model: \ {d['pitch']:.1f} Hz measured, \ a decay knob, \ a 1 ms click", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.4)
        head = label(r"a kick from first principles", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The 808's bass drum is a resonant network, a bridged-T filter, struck by an electrical pulse. "
            "<bookmark mark='a'/> A struck resonator rings at its own frequency and dies away, like Part 1's string reduced "
            "to a single mode: a damped sine. <bookmark mark='b'/> The strike also detunes it for a moment, so the pitch "
            "sweeps down from about eighty hertz to fifty-two within twenty milliseconds, which the ear hears as punch. "
            f"Monochord's model rings at {say(round(d['pitch']))} hertz, measured, with a knob for the decay and a millisecond "
            "click from the pulse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), FadeIn(axis), FadeIn(fax))
            vo.wait_until("a")
            self.play(Create(wave), FadeIn(labs[0]), FadeIn(labs[2]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(fl), FadeIn(labs[1]), FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_kick(self):
        d = load("eight")
        c = clip("eight.kick")
        cells = VGroup(*[VGroup(label(rf"decay {x:.2f} s", font_size=22, color=TUNE), label([r"tight", r"medium", r"long, \ almost a bass note"][k], font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)
                         for k, x in enumerate(d["decays"])]).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        with self.voiceover(
            "Hear the model kick at three settings of the decay knob, twice each. At the longest it is almost a bass note, "
            "which is exactly how hip hop and trap producers came to use it: tuned to the song's key, as its bass line."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"three decays", kind="synthesized", detail=r"a struck-resonator model", corner=DL, tag_corner=DR)
            st = d["starts"] + [c.duration]
            for i in range(3):
                pulse(snd, cells[i], st[i], st[i + 1] - 0.3, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuned(self):
        d = load("tuned")
        c = clip("tuned.bass")
        notes = [[m, s, 4.0] for s, m in d["line"]]
        r = mroll(notes, width=11.0, height=2.2, lo=27, hi=38, color=TUNE, total=64, bar_h=0.16).move_to(DOWN * 0.2)
        NNs = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
        names = VGroup(*[label(NNs[m % 12], font_size=15, color=WHITE).next_to(b, UP, buff=0.05) for (m, s, du), b in zip(notes, r.notes)])
        head = label(r"the kick as the bass line", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"each note: \ the same struck resonator, \ tuned, \ with a long decay", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "With a long decay, the kick is a bass note, and producers tune it. Here the same struck resonator plays a bass "
            "line of ours, C, A flat, B flat, F, G, each note a retuned kick, under a clap and hats. In trap the eight-oh-eight "
            "is the bass."
        ):
            self.play(FadeIn(head), FadeIn(r), FadeIn(names), FadeIn(cap))
        step = 60.0 / d["bpm"] / 4
        with self.listen(c) as snd:
            window(snd, r"a tuned kick", kind="synthesized", detail=r"a struck-resonator model", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [s * step for s, m in d["line"]], hot=WHITE, base=TUNE)
            cursor(snd, r, 0.0, step)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hat(self):
        d = load("eight")
        hz = d["hat_hz"]
        x0, W = -5.8, 11.0
        fmax = 4000.0
        ax = Line([x0, -1.5, 0], [x0 + W, -1.5, 0], color=GREY_B)
        bars = VGroup()
        for f in hz:
            for k in (1, 3, 5):
                fk = f * k
                if fk > fmax:
                    continue
                h = 2.2 / k
                bars.add(Line([x0 + W * fk / fmax, -1.5, 0], [x0 + W * fk / fmax, -1.5 + h, 0], color=TUNE if k == 1 else BLUE, stroke_width=4 if k == 1 else 2))
        labs = VGroup(*[label(f"{f:g}", font_size=14, color=TUNE).move_to([x0 + W * f / fmax, -1.8, 0]) for f in hz])
        tick = VGroup(*[label(f"{f} Hz", font_size=14, color=GREY_A).move_to([x0 + W * f / fmax, -2.2, 0]) for f in (1000, 2000, 3000, 4000)])
        side = label(r"six square waves at fixed, \ unrelated frequencies: \ their odd harmonics crowd into a metallic cluster; \ a high-pass filter keeps the top", font_size=19, color=WHITE).to_edge(UP, buff=1.0)
        head = label(r"the 808's hi-hat: \ six oscillators", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The 808's hi-hats and cymbal come from six square-wave oscillators at fixed frequencies that bear no simple "
            "relation to one another: about two hundred and five, three hundred and four, three hundred and seventy, five "
            "hundred and twenty-three, five hundred and forty, and eight hundred hertz. <bookmark mark='a'/> Each square "
            "wave has odd harmonics, a third, a fifth and so on, so together they fill the upper spectrum with a dense, "
            "inharmonic cluster, like Part 9's cymbal; a high-pass filter keeps only the top, and an envelope makes it a "
            "closed hat or an open one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tick), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.05), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kit(self):
        d = load("eight")
        c = clip("eight.kit")
        from explainer.music.monochord import song as S
        p = S.PATTERNS["trap"]
        rows_ = VGroup(pat_row(["x" if i in p["kick"] else "." for i in range(16)], cell=0.42, color=TUNE, name=r"kick", size=18),
                       pat_row(["x" if i in p["snare"] else "." for i in range(16)], cell=0.42, color=EAR, name=r"clap", size=18),
                       pat_row(["x" if i in p["hat"] else "." for i in range(16)], cell=0.42, color=GREY_A, name=r"hat", size=18)).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).move_to(UP * 0.3)
        cap = label(r"with a sine sub-bass under the kick; \ 90 beats a minute, \ half-time", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"the whole kit, \ in a pattern", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And the whole kit in a half-time pattern of the kind trap producers use: the kick, a clap built from three "
            "bursts of noise and a tail, hi-hats in sixteenths, and a sine sub-bass under the kick."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        step = 60.0 / 90 / 4
        with self.listen(c) as snd:
            window(snd, r"the kit", kind="synthesized", detail=r"drum-machine models, \ a sine sub-bass", corner=DL, tag_corner=DR)
            for row, k in zip(rows_, ("kick", "snare", "hat")):
                flash_cells(snd, row.cells, p[k], 0.0, step, 4, 16, color={"kick": TUNE, "snare": EAR, "hat": GREY_A}[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def legacy(self):
        items = [
            (r"Linn's LM-1 \ (1980) \ played samples of real drums; \ the 909 \ (1983) \ mixed both", WHITE),
            (r"the step sequencer made rhythm a grid of switches: \ Part 33's necklaces, \ as hardware", WHITE),
            (r"today the 808's sounds live as samples and software in every studio", WHITE),
            (r"a commercial failure that became a musical language", TUNE),
            (r"chapter 7: \ beats made from records", GREY_A),
        ]
        rows_scene(self, r"after the 808", items,
                   "Other machines followed. <bookmark mark='b'/> Roger Linn's LM-1, also from 1980, played samples of real drums, and "
                   "the 909 of 1983 mixed both. <bookmark mark='c'/> The step sequencer made rhythm a grid of switches: Part 33's "
                   "necklaces, as hardware. <bookmark mark='d'/> Today the 808's sounds live on as samples and software in every "
                   "studio: <bookmark mark='e'/> a commercial failure that became a musical language. <bookmark mark='f'/> "
                   "Chapter seven turns to beats made from records.", marks="cdef")
