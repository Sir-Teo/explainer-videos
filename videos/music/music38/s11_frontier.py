from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ microtiming and jazz corpora", r"What makes a performance swing?")
        self.debate()
        self.jitter()
        self.corpora()
        self.problem()
        self.credit()

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"J. A. Pr\"ogler \ (1995): \ bass and ride cymbal measured against each other, \ milliseconds apart", WHITE),
            (r"Datseris and colleagues \ (2019): \ removing jazz players' small timing deviations did not make listeners rate them less swinging", WHITE),
            (r"Nelias and colleagues \ (2022): \ but soloists' systematically late downbeats did add to swing, \ in their tests", WHITE),
            (r"random deviations and systematic ones are different things: \ the debate is about which matters", TUNE),
            (r"the measurements are fine; \ the open question is what listeners use", GREY_A),
        ]
        rows_scene(self, r"microtiming, \ argued over", items,
                   "Is swing in the small timing deviations between players? The evidence is argued over. "
                   "<bookmark mark='b'/> In 1995 J. A. Prögler measured bass and ride cymbal against each other and found them "
                   "milliseconds apart. <bookmark mark='c'/> In 2019 George Datseris and colleagues, at the Max Planck Institute "
                   "in Göttingen, found that removing jazz players' small timing deviations did not make listeners rate the music "
                   "less swinging. <bookmark mark='d'/> In 2022 the same group reported that soloists' systematically late "
                   "downbeats did add to swing in their tests. <bookmark mark='e'/> Random deviations and systematic ones are "
                   "different things, and the debate is about which matters. <bookmark mark='f'/> The measurements are fine; the "
                   "open question is what listeners use.", marks="cdef")

    # ------------------------------------------------------------------
    def jitter(self):
        d = load("jitter")
        devs = d["devs"]
        W = 11.0
        ticks = VGroup(*[Line([-W / 2 + W * k / 15, -0.25, 0], [-W / 2 + W * k / 15, 0.25, 0], color=GREY_B, stroke_width=2) for k in range(16)])
        bars_ = VGroup()
        for k, v in enumerate(devs[:15]):
            h = 0.06 * v
            bars_.add(Rectangle(width=0.35, height=max(abs(h), 0.02), stroke_width=0, fill_color=EAR if v > 0 else BLUE, fill_opacity=0.85)
                      .move_to([-W / 2 + W * (k + 0.5) / 15, -1.2 + h / 2, 0]))
        base = Line([-W / 2, -1.2, 0], [W / 2, -1.2, 0], color=GREY_B)
        lab = label(r"each note's random shift, \ first 15 notes: \ pink late, \ blue early", font_size=18, color=GREY_A).next_to(base, DOWN, buff=0.9)
        stage = VGroup(label(r"first: \ exactly on the model's grid", font_size=21, color=WHITE), label(rf"second: \ each note shifted at random \ (sd {d['sd_ms']:.0f} ms, \ largest {d['max_ms']:.0f} ms)", font_size=21, color=WHITE)).arrange(DOWN, buff=0.3).move_to(UP * 1.5)
        head = label(r"random deviations, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear the kind of manipulation such experiments use, with values of our own. A line on an additive saxophone, "
            "first exactly on the swing model's grid, then with every note shifted at random by a few milliseconds, typically "
            f"fifteen, at most {say(round(d['max_ms']))}. Does the second swing more, less, or the same?"
        ):
            self.play(FadeIn(head), FadeIn(stage), FadeIn(base), FadeIn(bars_), FadeIn(lab))
        for name, k in (("grid", 0), ("random", 1)):
            c = clip("jitter.grid") if name == "grid" else clip("jitter.random")
            with self.listen(c) as snd:
                window(snd, {"grid": r"on the grid", "random": r"random deviations"}[name], kind="synthesized", detail=r"an additive saxophone, \ string and cymbal models", corner=DL, tag_corner=DR)
                pulse(snd, stage[k], 0.0, c.duration, buff=0.1)
            self.wait(0.3)
        ans = label(r"random shifts sound looser or sloppier, \ rarely more swinging: \ the deviations that matter are systematic", font_size=20, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            'Judge the two sketches for yourself; this informal comparison establishes no majority response. The cited experiments distinguish kinds of manipulation in particular performances and listener groups, rather than proving that only systematic timing can matter.'
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpora(self):
        items = [
            (r"the Weimar Jazz Database: \ 456 transcribed solos, \ with beats, \ chords and annotations \ (Jazzomat project)", WHITE),
            (r"questions it can answer: \ how swing ratios, \ note choices and patterns vary by player and era", WHITE),
            (r"pattern searches find `licks' that travel between players across decades", WHITE),
            (r"what it cannot answer alone: \ why a performance feels as it does", TUNE),
            (r"Parts 61--63 build such tools for audio", GREY_A),
        ]
        rows_scene(self, r"jazz as data", items,
                   "Jazz is now studied as data too. <bookmark mark='b'/> The Weimar Jazz Database holds four hundred and fifty-six "
                   "transcribed solos, with their beats, chords and annotations, from the Jazzomat project. "
                   "<bookmark mark='c'/> It can answer how swing ratios, note choices and patterns vary by player and era, "
                   "<bookmark mark='d'/> and pattern searches find licks that travel between players across decades. "
                   "<bookmark mark='e'/> What a corpus cannot answer alone is why a performance feels as it does. "
                   "<bookmark mark='f'/> Parts sixty-one to sixty-three build such tools for audio.", marks="cdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take solos from a corpus and resynthesise them with controlled changes", WHITE),
            (r"vary the swing ratio, \ the downbeat delay, \ dynamics and articulation, \ one at a time and together", WHITE),
            (r"ask listeners of different experience to rate swing, \ and model their ratings", WHITE),
            (r"$\bigstar$ \ research problem: \ what makes a performance swing, \ and for whom?", EAR),
            (r"an answer would turn a proverb into a model, \ or show why it cannot be one", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A concrete version. <bookmark mark='a'/> Take solos from a corpus and resynthesise them with controlled changes. "
            "<bookmark mark='b'/> Vary the swing ratio, the downbeat delay, dynamics and articulation, one at a time and "
            "together. <bookmark mark='c'/> Ask listeners of different experience to rate the swing, and model their ratings. "
            "<bookmark mark='d'/> What makes a performance swing, and for whom? <bookmark mark='e'/> An answer would turn a "
            "proverb into a model, or show why it cannot be one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credit(self):
        items = [
            (r"early blues was sold on `race records', \ marketed by segregation", WHITE),
            (r"many performers were paid a flat fee and no royalties; \ publishers often took the credit", WHITE),
            (r"later stars recorded their songs, \ sometimes without acknowledgement", WHITE),
            (r"who made the music, \ and who was paid, \ are part of its history", TUNE),
            (r"Part 60 returns to rights and royalties", GREY_A),
        ]
        rows_scene(self, r"credit", items,
                   "This history has a hard side. <bookmark mark='b'/> Early blues was sold on race records, marketed along the "
                   "lines of segregation. <bookmark mark='c'/> Many performers were paid a flat fee and no royalties, and "
                   "publishers often took the credit. <bookmark mark='d'/> Later stars recorded their songs, sometimes without "
                   "acknowledgement. <bookmark mark='e'/> Who made the music, and who was paid, are part of its history. "
                   "<bookmark mark='f'/> Part sixty returns to rights and royalties.", marks="cdef")
