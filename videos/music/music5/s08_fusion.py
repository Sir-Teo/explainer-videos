from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Fusion(SoundScene):
    def construct(self):
        chapter(self, 7, r"One note or two?", r"Is roughness the whole story?", lit=(1722,), extra=((1722, r"Rameau's fundamental bass"), (1890, r"Stumpf's fusion")))
        self.stumpf()
        self.bass()
        self.table()
        self.ears()

    # ------------------------------------------------------------------
    def stumpf(self):
        card = history_card(1890, r"Carl Stumpf, \ \textit{Tonpsychologie}",
                            r"plays two notes together to people with no musical training and asks: is that one tone, or two?", width=5.6).to_corner(UL, buff=0.4)
        names = [r"octave", r"fifth", r"fourth", r"third", r"tritone", r"second"]
        bars = VGroup()
        for k, n in enumerate(names):
            h = 2.6 * (1.0 - 0.16 * k)
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=interpolate_color(ManimColor(SMOOTH), ManimColor(ROUGH), k / 5), fill_opacity=0.8)
            b.move_to(RIGHT * (0.3 + 1.05 * k) + DOWN * 1.9 + UP * h / 2)
            bars.add(VGroup(b, label(n, font_size=22, color=GREY_A).next_to(b, DOWN, buff=0.12)))
        yl = label(r"how often two notes were taken for one", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.25)
        tag = label(r"the order he found; \ heights are schematic", font_size=18, color=GREY_C).next_to(bars, DOWN, buff=0.55)
        word = label(r"\textbf{fusion}: \ consonant notes are the ones that melt into one", font_size=30, color=EAR).to_edge(DOWN, buff=0.35)
        doubts = VGroup(label(r"if consonance is only the absence of roughness \ldots", font_size=30, color=GREY_A),
                        label(r"a chord played very softly is still a consonance", font_size=28, color=TUNE),
                        label(r"a chord spread over three octaves, \ with nothing left to beat, \ is still a consonance", font_size=28, color=TUNE)
                        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        with self.voiceover(
            "Roughness explains a great deal. But a younger contemporary of Helmholtz thought it explained the "
            "wrong thing. The psychologist Carl Stumpf pointed out that a chord played very "
            "softly, or spread across registers so that nothing beats, is still a consonance. So he ran a "
            "different experiment. <bookmark mark='a'/> He played two notes together to people with no musical "
            "training, and asked a simple question. Is that one tone, or two? <bookmark mark='b'/> For an octave, "
            "his listeners very often said one. For a fifth, less often. For a fourth, less often still. For "
            "thirds, rarely, and for seconds, almost never. <bookmark mark='c'/> It is the old ranking again, "
            "from a completely different measurement. Stumpf called it fusion. Consonant notes, he said, are the "
            "ones that melt together into a single thing."
        ) as vo:
            self.play(FadeIn(doubts[0]))
            self.wait(5.0)
            self.play(FadeIn(doubts[1]))
            self.play(FadeIn(doubts[2]))
            vo.wait_until("a")
            self.play(FadeOut(doubts), run_time=0.4)
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.5), FadeIn(yl), FadeIn(tag), run_time=7.0)
            vo.wait_until("c")
            self.play(FadeIn(word))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass(self):
        d = load("fusion")
        c = clip("fusion.bass")
        q = listen_card(r"Three high pure tones together. \ Then one low tone, \ alone. \ Then the three again. \\ The second time, \ can you hear the low note inside the chord?",
                        width=10.2, font_size=26).to_edge(UP, buff=0.35)
        g = faxes(150, 2200, [0, 1.15], x_length=9.6, y_length=2.3, ylabel="", yticks=[], fticks=(262, 523, 1047, 1308, 1570), font_size=20)
        g.move_to(DOWN * 1.2)
        high = VGroup(*[Line(g.at(f, 0), g.at(f, 1.0), color=TUNE, stroke_width=7) for f in d["high"]])
        low = DashedLine(g.at(d["high"][0] / 4, 0), g.at(d["high"][0] / 4, 0.7), color=EAR, stroke_width=5, dash_length=0.1)
        nums = VGroup(*[MathTex(str(k), font_size=30, color=TUNE).next_to(h, UP, buff=0.1) for k, h in zip((4, 5, 6), high)])
        with self.voiceover(
            "What could make two notes melt into one? Part 4 has the answer ready. The ear gives a single pitch "
            "to any set of partials that fits one harmonic series, even when the bottom of the series is "
            "missing. So try this. Three high pure tones, sounding together. Then a single low tone. Then the "
            "three again. The second time, listen for the low note inside the chord."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(high))
        self.add(low)
        low.set_stroke(opacity=0)
        with self.listen(c) as snd:
            window(snd, r"three high tones; \ a low one; \ the three again", kind="synthesized", detail=r"pure tones", corner=DL, tag_corner=DR)
            tb, ta = snd.time_of("bass"), snd.time_of("again")
            snd.drive(high, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(20 * t)) if (t < tb - 0.4 or t >= ta) else 0.15))
            snd.drive(low, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(20 * t)) if tb <= t < ta - 0.4 else (0.35 if t >= ta else 0.0)))
        high.set_stroke(opacity=1)
        low.set_stroke(opacity=1)
        res = VGroup(label(r"the three tones are partials 4, 5 and 6 of the low one: \ a major triad, \ $4 : 5 : 6$", font_size=26, color=GREY_A),
                     label(rf"Part 4's pitch model, \ given only the three: \ {d['implied_hz']:.1f} Hz, \ middle C", font_size=28, color=EAR),
                     label(r"Rameau (1722): \ every chord has a \textbf{fundamental bass}, \ the note whose partials it is", font_size=26, color=HIST)
                     ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Most people can, once they know where to listen. It is not in the sound: the chord has no energy "
            "down there. <bookmark mark='a'/> The three tones are at four, five and six times the low note's "
            "frequency. They are a major triad, and they are also three neighbouring partials of one harmonic "
            f"series. <bookmark mark='b'/> Give those three tones to the pitch model of Part 4, and it reports "
            f"{say(d['implied_hz'], 1)} hertz: middle C, two octaves below the chord's own lowest note. "
            "<bookmark mark='c'/> A musician worked this out without any of our machinery. In 1722 Jean-Philippe "
            "Rameau proposed that every chord has a fundamental bass: a single note, often not played at all, "
            "of which, he came to argue, the chord's notes are the partials. He built a theory of harmony on it. What he "
            "had found was the ear's habit of looking for one source."
        ) as vo:
            self.play(FadeOut(q), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]), Indicate(low, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("fusion")
        head = label(r"what the pitch model makes of two notes above middle C", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        rows = VGroup()
        for k, r in enumerate(d["rows"][:4]):
            den = r["bass"][1]
            bar = Rectangle(width=4.2 * r["strength"], height=0.42, stroke_width=0, fill_color=interpolate_color(ManimColor(ROUGH), ManimColor(SMOOTH), r["strength"]), fill_opacity=0.85)
            row = VGroup(label(r["name"], font_size=28), label(r"the note itself" if den == 1 else rf"a note at $\tfrac{{1}}{{{den}}}$ of the lower: \ {r['model_hz']:.0f} Hz", font_size=24, color=EAR),
                         bar, label(rf"{r['strength']:.2f}", font_size=24, color=GREY_A))
            y = 1.7 - 0.95 * k
            row[0].move_to(LEFT * 6.0 + UP * y, aligned_edge=LEFT)
            row[1].move_to(LEFT * 3.6 + UP * y, aligned_edge=LEFT)
            row[2].move_to(RIGHT * 1.5 + UP * y, aligned_edge=LEFT)
            row[3].next_to(row[2], RIGHT, buff=0.15)
            rows.add(row)
        cols = VGroup(label(r"the single pitch it finds", font_size=22, color=GREY_B).move_to(LEFT * 3.6 + UP * 2.45, aligned_edge=LEFT),
                      label(r"how strongly", font_size=22, color=GREY_B).move_to(RIGHT * 1.5 + UP * 2.45, aligned_edge=LEFT))
        gal = VGroup(label(r"the simpler the ratio, \ the shorter the time before both notes repeat together,", font_size=26, color=GREY_A),
                     label(r"and the stronger the single pitch: \ Galileo's pulses, \ counted by the nerve", font_size=28, color=GOOD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So here is a second measure of consonance, quite separate from roughness. Give two notes to the "
            "pitch model, and ask what single pitch it finds, and how strongly. <bookmark mark='a'/> For an "
            "octave it finds the lower note itself, very strongly: the upper note's partials are all partials of "
            "the lower already. <bookmark mark='b'/> For a fifth it finds a note an octave below the lower one, "
            "less strongly. For a fourth, a note at a third of the frequency, weaker again. For a major third, a "
            "quarter, weaker still. <bookmark mark='c'/> The pattern is exact. The simpler the ratio, the sooner "
            "the two notes come back into step, and the more firmly the nerve's timing locks onto one period. "
            "This is Galileo's theory of coinciding pulses, come back as promised. The ear cannot count pulses. "
            "But the auditory nerve can keep time with them, and a brain that is looking for one source will "
            "find one more easily in a fifth than in a tritone. Stumpf's fusion, Rameau's bass and Galileo's "
            "pulses are one idea. Today it is called harmonicity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.7), run_time=7.0)
            vo.wait_until("c")
            self.play(FadeIn(gal))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ears(self):
        d = load("fusion")
        c = clip("fusion.ears")
        note = listen_note(r"For headphones. \ A minor second: \ first both tones in both ears, \\ then one tone in each ear. \ What happens to the roughness?",
                           width=9.6, font_size=26).to_edge(UP, buff=0.35)
        heads = VGroup()
        for k in range(2):
            face = Circle(radius=0.8, stroke_color=GREY_B, stroke_width=3)
            le = Arc(radius=0.22, start_angle=PI / 2, angle=PI, color=GREY_B, stroke_width=3).next_to(face, LEFT, buff=-0.02)
            re = Arc(radius=0.22, start_angle=-PI / 2, angle=PI, color=GREY_B, stroke_width=3).next_to(face, RIGHT, buff=-0.02)
            heads.add(VGroup(face, le, re))
        heads.arrange(RIGHT, buff=3.4).move_to(DOWN * 0.9)
        f1, f2 = (rf"{f:.0f}" for f in d["second"])
        tags = VGroup(label(rf"{f1} + {f2}", font_size=24, color=ROUGH).next_to(heads[0][1], LEFT, buff=0.15), label(rf"{f1} + {f2}", font_size=24, color=ROUGH).next_to(heads[0][2], RIGHT, buff=0.15),
                      label(f1, font_size=24, color=AIR).next_to(heads[1][1], LEFT, buff=0.15), label(f2, font_size=24, color=TUNE).next_to(heads[1][2], RIGHT, buff=0.15))
        with self.voiceover(
            "There is a way to pull the two theories apart, and if you have headphones on you can take part. "
            "Roughness happens when two tones land on the same stretch of one membrane. So put one tone in each "
            "ear. Here is a minor second, first with both tones in both ears, and then with one tone on the left "
            "and the other on the right."
        ):
            self.play(FadeIn(note, shift=DOWN * 0.2), FadeIn(heads), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"a minor second: \ together, \ then one tone to each ear", kind="synthesized", detail=r"needs headphones", corner=DL, tag_corner=DR)
            for ev, h in zip(("together", "apart"), heads):
                t0 = snd.time_of(ev)
                pulse(snd, h, t0, t0 + 2.4, buff=0.25)
        res = VGroup(label(r"one tone to each ear: \ no membrane carries both, \ and the grinding is gone", font_size=28, color=SMOOTH),
                     label(r"McDermott, Lehr and Oxenham (2010): \ how much a listener likes consonance goes with how much", font_size=24, color=GREY_A),
                     label(r"they like harmonic sounds, \ and not with how much they dislike beating", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "On headphones, the grinding disappears. Neither ear receives both tones, so there is nothing on "
            "either membrane to beat. <bookmark mark='a'/> And yet intervals presented this way are still judged "
            "more and less consonant. So roughness cannot be everything. In 2010 Josh McDermott and his "
            "colleagues tested the two ideas against each other, listener by listener. People differ in how "
            "strongly they prefer consonant chords. That strength turned out to go with how much they liked "
            "harmonic sounds over inharmonic ones, and not at all with how much they disliked beating. We now "
            "have two physical causes, and they are not rivals. One comes from the membrane, the other from "
            "the nerve."
        ) as vo:
            self.play(FadeOut(note), FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()
