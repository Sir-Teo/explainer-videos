from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Tristan(SoundScene):
    def construct(self):
        chapter(self, 11, r"Four readings of one chord", r"What is the Tristan chord?", extra=((1920, r"Kurth's \textit{Romantische Harmonik}"),))
        self.again()
        self.readings()
        self.motion()

    # ------------------------------------------------------------------
    def again(self):
        d = load("hook")
        c = clip("hook.tristan")
        st = block_staff([d["first"]["tristan"][::-1], d["first"]["resolution"][::-1]], width=4.6, beats=2).move_to(LEFT * 3.4 + DOWN * 0.3)
        nm = VGroup(label(r"F \ B \ D$\sharp$ \ G$\sharp$", font_size=24, color=EAR), label(r"E \ G$\sharp$ \ D \ B", font_size=24, color=TUNE))
        for k, n in enumerate(nm):
            n.move_to([st.get_left()[0] + 1.0 + (st.width - 1.2) * (k + 0.5) / 2, st.get_bottom()[1] - 0.4, 0])
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"now we have the words for it", GREY_A),
            (r"the second chord: \ E \ G$\sharp$ \ B \ D, \ a dominant seventh", WHITE),
            (r"the dominant of A minor, \ and A minor never comes", WHITE),
            (r"a full resolution comes only at the opera's end", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.0 + DOWN * 0.1)
        with self.voiceover(
            "Back to the chord at the start of this part. Hear it once more, now that we have the words."
        ):
            self.play(FadeIn(st), FadeIn(nm))
        with self.listen(c) as snd:
            window(snd, r"\textit{Tristan}, \ again", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, nm[0], d["chord_at"][0], d["resolve_at"][0] - 0.2, buff=0.1)
            pulse(snd, nm[1], d["resolve_at"][0], d["starts"]["second"] - 0.4, buff=0.1)
            pulse(snd, st, d["starts"]["second"], c.duration, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> The second chord is easy. <bookmark mark='b'/> E, G sharp, B, D: a dominant seventh. "
            "<bookmark mark='c'/> It is the dominant of A minor, and the prelude never gives us A minor: each phrase "
            "stops on a dominant. <bookmark mark='d'/> The opera famously withholds a full resolution of this "
            "harmony until its final bars, hours later. The puzzle is the first chord."
        ) as vo:
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def readings(self):
        d = load("tristan")
        cards = VGroup()
        cols = (EAR, TUNE, BLUE, GREY_A)
        for r, c_ in zip(d["readings"], cols):
            box = RoundedRectangle(width=6.1, height=2.2, corner_radius=0.15, stroke_color=c_, stroke_width=2.5, fill_color=c_, fill_opacity=0.06)
            t = VGroup(label(r["name"], font_size=26, color=c_), label(tex(r["notes"]), font_size=22, color=WHITE),
                       label(tex(r["how"].replace("'", "")), font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
            if t.width > box.width - 0.4:
                t.scale_to_fit_width(box.width - 0.4)
            t.move_to(box)
            cards.add(VGroup(box, t))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.3)).move_to(DOWN * 0.2)
        with self.voiceover(
            "Four readings, each a theory. <bookmark mark='a'/> First: a French sixth in A minor, F, B, D sharp, A, "
            "with G sharp an appoggiatura, a leaning note, that slides up to A; the chord then opens onto the dominant "
            "exactly as chapter four's sixths did. <bookmark mark='b'/> Second: as a sound, it is simply a "
            "half-diminished seventh, F, A flat, C flat, E flat respelled, the chord built on the second degree of E "
            "flat minor, as a pitch-class description; that alone does not settle its function. <bookmark mark='c'/> Third: an altered dominant of E, "
            "B, D sharp, F, A, the five-of-five with its fifth lowered. <bookmark mark='d'/> Fourth: Ernst Kurth, in 1920, "
            "emphasized linear motion and dynamic tension over a single functional label. It is a moment of pure tension, defined by the lines that pass through it, "
            "whose interaction helps shape its tension."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for mark, c_ in zip("bcd", cards[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(c_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def motion(self):
        d = load("tristan")
        vl = d["voice_leading"]
        names = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
        centre = LEFT * 3.2 + DOWN * 0.2
        R = 2.0
        pts = {k: centre + R * np.array([np.sin(2 * np.pi * k / 12), np.cos(2 * np.pi * k / 12), 0]) for k in range(12)}
        ring = Circle(radius=R, color=DIM, stroke_width=2).move_to(centre)
        labs = VGroup(*[label(tex(names[k]), font_size=20, color=GREY_B).move_to(centre + (R + 0.42) * (pts[k] - centre) / R) for k in range(12)])
        a = [p % 12 for p in d["chord"]]
        sq = Polygon(*[pts[k] for k in sorted(a)], color=EAR, stroke_width=4)
        b = vl["to"]
        sq2 = Polygon(*[pts[k] for k in sorted(b)], color=TUNE, stroke_width=4)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"as pitch classes: \ F$\to$E, \ D$\sharp\to$D, \ B and G$\sharp$ stay", WHITE),
            (rf"{vl['cost']} semitones of motion in all", EAR),
            (r"the smallest move from a half-diminished seventh to a dominant seventh", WHITE),
            (r"this is the frontier: \ harmony as voice leading, \ not as keys", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.0 + DOWN * 0.1)
        with self.voiceover(
            "Kurth's reading points to where theory went next. Put the two chords on the clock of pitch classes. "
            "<bookmark mark='a'/> The best way to move from the first to the second: F falls to E, D sharp falls to "
            f"D, and B and G sharp stay where they are. <bookmark mark='b'/> {say(vl['cost'])} semitones in all. "
            "<bookmark mark='c'/> This is the minimum under our pitch-class assignment metric, which ignores register and actual voice identity. "
            "<bookmark mark='d'/> Whatever the first chord is called, the way it moves is a fact we can measure. That is "
            "the idea of the last chapter: harmony as voice leading."
        ) as vo:
            self.play(Create(ring), FadeIn(labs), Create(sq))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]), TransformFromCopy(sq, sq2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()
