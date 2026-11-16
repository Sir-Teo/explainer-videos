from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Compare(SoundScene):
    def construct(self):
        chapter(self, 4, r"Surprise across melodies", r"Is good music predictable or surprising?")
        self.bars()
        self.drafts()
        self.extremes()
        self.evidence()
        self.balance()

    # ------------------------------------------------------------------
    def bars(self):
        d = load("compare")
        x0, W = -2.0, 5.0
        mx = max(d["mean_ic"])
        rows_ = VGroup()
        for i, (n, a, b) in enumerate(zip(d["names"], d["mean_ic"], d["mean_entropy"])):
            y = 2.0 - 0.62 * i
            w = W * a / mx
            rows_.add(VGroup(label(n, font_size=17, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                             Rectangle(width=w, height=0.38, stroke_width=0, fill_color=EAR, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                             label(rf"{a:.2f} bits \ (uncertainty {b:.2f})", font_size=15, color=WHITE).move_to([x0 + w + 0.2, y, 0], aligned_edge=LEFT)))
        head = label(r"mean surprise a note, \ heard by the same listener", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"the Tune and Ode to Joy each heard by a model trained on the other tunes", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.6)
        names = d["names"]
        val = dict(zip(names, d["mean_ic"]))
        with self.voiceover(
            "Point the listener at other melodies. <bookmark mark='a'/> The Tune and the Ode to Joy cost about two bits a "
            "note. Part 42's searcher kept a draft that cost "
            f"{say(val.get('Part 42: the kept draft', 0), 1)} bits, and threw away one that cost "
            f"{say(val.get('Part 42: a rejected draft', 0), 1)}: its critics, without being told to, preferred the more "
            "predictable. Its chain of order four, which copied whole phrases, costs about the same as a real folk tune; "
            "order one costs much more; and random notes of the scale cost most of all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        items = [
            (r"Pearce and colleagues \ (2010): \ high-information notes evoke larger brain responses and lower expectedness ratings", WHITE),
            (r"the model's surprise also predicts where listeners hear phrase boundaries: \ after a run of predictable notes, \ a surprise", WHITE),
            (r"models trained on one culture's music predict that culture's listeners better than another's", WHITE),
            (r"expectation is real, \ measurable, \ and learned from exposure", TUNE),
            (r"but is predictable music good, \ or surprising music?", GREY_A),
        ]
        rows_scene(self, r"does the model hear as we do?", items,
                   "Does such a model hear as we do? <bookmark mark='b'/> Pearce and colleagues showed in 2010 that "
                   "high-information notes evoke larger brain responses and lower ratings of expectedness. "
                   "<bookmark mark='c'/> The model's surprise also predicts where listeners hear phrase boundaries, after a run of "
                   "predictable notes, at a surprise. <bookmark mark='d'/> And models trained on one culture's music predict that "
                   "culture's listeners better than another's. <bookmark mark='e'/> Expectation is real, measurable, and learned "
                   "from exposure. <bookmark mark='f'/> But is predictable music good, or surprising music?", marks="bcdef")

    # ------------------------------------------------------------------
    def balance(self):
        items = [
            (r"Daniel Berlyne \ (1971): \ liking rises and then falls with complexity, \ an inverted U", WHITE),
            (r"too predictable is boring; \ too surprising is noise", WHITE),
            (r"the peak moves with familiarity: \ the more you know a style, \ the more complexity you enjoy", WHITE),
            (r"mere exposure: \ repetition raises liking, \ up to a point", TUNE),
            (r"chapter 5: \ surprise used on purpose, \ in three endings", GREY_A),
        ]
        rows_scene(self, r"the inverted U", items,
                   "The classic answer is: neither, but in between. <bookmark mark='b'/> Daniel Berlyne proposed in 1971 that "
                   "liking rises and then falls with complexity, an inverted U: <bookmark mark='c'/> too predictable is boring, "
                   "too surprising is noise. <bookmark mark='d'/> The peak moves with familiarity: the more you know a style, the "
                   "more complexity you enjoy. <bookmark mark='e'/> And mere exposure raises liking, up to a point. "
                   "<bookmark mark='f'/> Chapter five uses surprise on purpose, in three endings.", marks="bcdef")

    # ------------------------------------------------------------------
    def drafts(self):
        d = load("drafts")
        c = clip("drafts.two")
        cells = VGroup(VGroup(label(r"Part 42's first rejected draft", font_size=20, color=GREY_A), label(rf"{d['ic']['rejected']:.2f} bits a note", font_size=18, color=EAR)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"the draft its critics kept", font_size=20, color=TUNE), label(rf"{d['ic']['kept']:.2f} bits a note", font_size=18, color=EAR)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"the searcher's drafts, \ heard by the listener", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("Hear the two drafts, melody alone: the rejected one first, then the kept one."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two drafts", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["rejected"], st["kept"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["kept"], c.duration, buff=0.1)
        with self.voiceover(
            "The rejected draft lurches; the kept one moves by step and sequence. The critics knew nothing of this listener, "
            "but they encoded the same style, so they chose the draft the listener finds more predictable."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extremes(self):
        d = load("extremes")
        c = clip("extremes.two")
        cells = VGroup(VGroup(label(r"random notes of the scale", font_size=20, color=WHITE), label(rf"{d['ic']['random']:.2f} bits a note", font_size=18, color=EAR)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"Part 42's chain of order 4", font_size=20, color=WHITE), label(rf"{d['ic']['chain']:.2f} bits a note", font_size=18, color=EAR)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"the two ends of the scale", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("And the two ends of the scale: random notes of the scale, then Part 42's chain of order four."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"random, \ then the chain", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["random"], st["chain"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["chain"], c.duration, buff=0.1)
        with self.voiceover("Random notes never let an expectation form; the chain borrows a folk tune's whole shape. These sketches illustrate a proposed complexity trade-off; they do not establish what all listeners value."):
            self.play(Indicate(cells[0]), Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()
