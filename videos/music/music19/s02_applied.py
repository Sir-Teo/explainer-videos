from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Applied(SoundScene):
    def construct(self):
        chapter(self, 1, r"One borrowed leading note", r"How can any chord become a temporary home?")
        self.idea()
        self.chain()
        self.tonicize()
        self.bach()

    # ------------------------------------------------------------------
    def idea(self):
        ex = [(72, 69, 66, 50), (71, 67, 62, 43)]
        st = block_staff(ex, width=4.0, beats=2).move_to(LEFT * 3.8 + DOWN * 0.2)
        tags = VGroup(label(r"D7: \ F$\sharp$ is G's leading note", font_size=22, color=EAR), label(r"G", font_size=22, color=GREY_A)).arrange(RIGHT, buff=1.2).next_to(st, DOWN, buff=0.35)
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"in C major, \ F$\sharp$ is not in the key", WHITE),
            (r"but a semitone below G, \ it leans on G as B leans on C", WHITE),
            (r"D, F$\sharp$, A, C: \ the dominant seventh of G, \ `V7 of V'", WHITE),
            (r"any major or minor chord of the key can be given its own dominant", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 7.6))
        rows_.move_to(RIGHT * 2.4 + DOWN * 0.1)
        with self.voiceover(
            "In common-practice major and harmonic-minor contexts, a leading note helps establish a tonic, the seventh degree a semitone below home. <bookmark mark='a'/> Now borrow one note from outside C major: F sharp. <bookmark mark='b'/> It sits a semitone below G, and leans on G exactly as B leans on C. <bookmark mark='c'/> Build D seven containing it: D, F sharp, A, C, and G becomes, for a moment, a home of its own. The chord is called five-seven of five, an applied or secondary dominant. <bookmark mark='d'/> Every major or minor chord in a key can be given one."
        ) as vo:
            self.play(FadeIn(st), FadeIn(tags))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chain(self):
        d = load("applied")
        c = clip("applied.chain")
        st = block_staff(d["chords"], width=12.4, beats=2).move_to(UP * 0.8)
        names = VGroup(*[label(n, font_size=22, color=EAR if "/" in n else TUNE) for n in d["names"]])
        for k, n in enumerate(names):
            n.move_to([st.get_left()[0] + 1.25 + (st.width - 1.5) * (k + 0.5) / len(names), st.get_bottom()[1] - 0.4, 0])
        cap = label(r"each pink chord borrows one or two notes, \ and points at the next chord as if it were home", font_size=24, color=GREY_A).to_edge(DOWN, buff=1.35)
        with self.voiceover(
            "Here is a chain of them in C major. Each chosen chord is preceded by its own dominant: four by its "
            "dominant, five by its dominant, six, two, and at the end the real dominant leads home. Every pink chord "
            "borrows one or two notes from outside the key, and each lasts only a moment. The key never changes; it is "
            "lit from new angles."
        ):
            self.play(FadeIn(st), FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"applied dominants in C", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(names), d["times"], hot=WHITE, base=TUNE)
            pulse(snd, cap, 0.0, c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tonicize(self):
        from explainer.music.monochord import key as K
        d = load("applied")
        ch = d["chords"]
        whole = K.key_name(K.find_key(K.distribution([p for c in ch for p in c])))
        local = [K.key_name(K.find_key(K.distribution([p for c in ch[i:i + 2] for p in c])), short=True) for i in range(len(ch) - 1)]
        n = len(d["names"])
        w = 12.0 / n
        x0 = -6.0
        names = VGroup(*[label(nm, font_size=22, color=EAR if "/" in nm else TUNE).move_to([x0 + w * (k + 0.5), 1.6, 0]) for k, nm in enumerate(d["names"])])
        bars = VGroup()
        for i, kn in enumerate(local):
            r = RoundedRectangle(width=2 * w - 0.12, height=0.42, corner_radius=0.1, stroke_width=1.5, stroke_color=GREY_B, fill_color=BLUE, fill_opacity=0.18)
            r.move_to([x0 + w * (i + 1), 0.8 - 0.5 * (i % 2), 0])
            bars.add(VGroup(r, label(tex(kn), font_size=20, color=WHITE).move_to(r)))
        whole_bar = VGroup(RoundedRectangle(width=12.0, height=0.5, corner_radius=0.12, stroke_width=2, stroke_color=TUNE, fill_color=TUNE, fill_opacity=0.15).move_to([0, -0.9, 0]))
        whole_bar.add(label(r"all eleven chords: \ " + whole, font_size=22, color=TUNE).move_to(whole_bar[0]))
        lt = label(r"Part 15's key finder, \ two chords at a time", font_size=22, color=GREY_A).move_to([-4.2, 2.4, 0])
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"each applied pair, \ heard alone, \ is in the key it points to", WHITE),
            (r"heard whole, \ the passage never leaves C major", WHITE),
            (r"tonicization: \ a key for a moment; \ modulation: \ a key confirmed by a cadence", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 2.4)
        with self.voiceover(
            "Is the music in a new key when it borrows a leading note? Ask Part 15's key finder, the probe-tone "
            "correlation, to judge the chain two chords at a time. <bookmark mark='a'/> Each applied dominant and its "
            "target, heard alone, reads as the key they point to: F, then G, then A minor, then D minor. "
            f"<bookmark mark='b'/> Heard whole, all eleven chords read as {whole}. <bookmark mark='c'/> Theorists call "
            "the brief kind tonicization: a chord made a home for a moment, inside a key that never changes. A "
            "modulation is a new key confirmed, usually by a cadence of its own. The difference is one of scale, and "
            "the key finder's window decides which one it sees."
        ) as vo:
            self.play(FadeIn(lt), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), FadeIn(rows_[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(whole_bar), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        d = load("applied")
        b = d["bach"]
        keys = sorted(b, key=lambda k: -b[k])
        ch = columns([b[k] for k in keys], keys, width=7.0, height=2.6, color=WEAK, hot=(0,), hot_color=EAR, fmt="{:.0f}", font_size=22).move_to(LEFT * 2.0 + DOWN * 0.6)
        t = label(r"in Bach's major chorales: \ major chords and sevenths on 1, \ 2, \ 3 or 6, \ on the beat", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(rf"{100 * d['bach_share']:.0f} beats in a hundred", font_size=30, color=EAR),
                      label(r"II, \ the dominant of the dominant, \ the commonest", font_size=24, color=WHITE),
                      label(r"chromatic harmony began inside the key", font_size=24, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.3)
        with self.voiceover(
            "How common are they in Bach's chorales? Count beats in major chorales whose chord is major, or a dominant "
            "seventh, on a degree where the key itself has a minor chord, or on the tonic with a seventh pointing to "
            f"four. <bookmark mark='a'/> About {say(round(100 * d['bach_share']))} beats in a hundred: the dominant of the "
            "dominant most of all, then the dominants of six and of two. <bookmark mark='b'/> Chromatic harmony did not "
            "begin with Wagner. It began inside the key, as a borrowed leading note, and by Bach's time it was routine."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
