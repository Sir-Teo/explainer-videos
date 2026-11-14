from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Model(SoundScene):
    def construct(self):
        chapter(self, 10, r"A model that is surprised", r"Can a machine expect the next note?", extra=((2005, r"Pearce's model of expectation"),))
        self.build()
        self.tune()
        self.extremes()
        self.orders()

    # ------------------------------------------------------------------
    def build(self):
        d = load("model")
        a = d["after"]["C, C"]
        ch = columns([x["p"] for x in a], [x["note"] + (r" below" if x["pitch"] < 0 else "") for x in a], width=5.5, height=2.2, color=WEAK, hot=(0, 1), hot_color=TUNE, fmt="{:.2f}", font_size=24, top=0.5).move_to(RIGHT * 3.3 + DOWN * 0.8)
        q = label(r"after \ C, \ C: \ what next?", font_size=30, color=WHITE).next_to(ch, UP, buff=0.5)
        steps = VGroup(label(r"1. \ count: \ after these two notes, \ what came next?", font_size=26, color=WHITE), label(r"2. \ never seen those two? \ use the last one", font_size=26, color=WHITE),
                       label(r"3. \ never seen that? \ use how common each note is", font_size=26, color=WHITE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.2 + UP * 0.3)
        head = label(r"a listener made of counts: \ fifty-three tunes, \ and not the Tune", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now build the listener. Give Monochord fifty-three tunes, everything except the Tune, and "
            "let it count. <bookmark mark='a'/> After these two notes, what came next, and how often? "
            "<bookmark mark='b'/> When it has never met those two notes together, it falls back on the "
            "last one alone; <bookmark mark='c'/> and then on nothing but how common each note is. That "
            "is a variable-order Markov model. It is the core of Marcus Pearce's model of melodic "
            "expectation, which he called IDyOM."
        ) as vo:
            self.play(FadeIn(head))
            for mark, s in zip("abc", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        with self.voiceover(
            "Ask it what follows C, C. <bookmark mark='a'/> It says: probably another C, or a D, about "
            "one chance in three each. It has never heard of Twinkle, Twinkle, Little Star."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(ch))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("model")
        c = clip("model.tune")
        t = d["tune"]
        n = len(t["pitches"])
        r = roll(t["pitches"], t["beats"], width=11.5, height=1.7, lo=-1, hi=10, lines=(0,), phrase_ends=t["phrase_ends"], color=TUNE).move_to(DOWN * 1.5)
        s = d["surprise"][:n]
        bars = VGroup()
        base = r.get_top()[1] + 0.35
        for k in range(n):
            h = 0.42 * s[k]
            x = r.notes[k].get_left()[0] + 0.12
            bars.add(Rectangle(width=0.2, height=h, stroke_width=0, fill_color=EAR, fill_opacity=0.9).move_to([x, base + h / 2, 0]))
        axis = Line([r.get_left()[0], base, 0], [r.get_right()[0], base, 0], color="#3A4250", stroke_width=2)
        yl = label(r"surprise, \ in bits", font_size=22, color=EAR).next_to(axis, UP, buff=2.35).align_to(r, RIGHT)
        for b in bars:
            b.set_opacity(0.0)
        head = label(r"the Tune, \ heard by a model that has never heard it", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("Now play it the Tune, and measure its surprise at every note, in bits."):
            self.play(FadeIn(head), FadeIn(r), FadeIn(axis), FadeIn(yl))
            self.add(bars)
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ and its surprise", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r, d["times"], hot=WHITE, base=TUNE)
            for k in range(n):
                snd.wait_until(d["times"][k])
                bars[k].set_opacity(0.9)
        peak = label(rf"{d['peak']:.1f} bits: \ the leap of a fifth", font_size=26, color=EAR).next_to(bars[d["peak_at"]], UR, buff=0.1)
        with self.voiceover(
            "The spike is the third note: the leap of a fifth, from C up to G. "
            f"<bookmark mark='a'/> {say(d['peak'], 1)} bits: the model gave that note about three "
            "chances in a hundred. Everything after it is cheap: repeats, and steps downward, around two "
            "bits each. The Tune spends its surprise at once, and then walks home. A great many "
            "melodies are built that way: one bold move near the start, and the rest of the phrase "
            "making sense of it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(peak), Indicate(bars[d["peak_at"]], color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orders(self):
        d = load("model")
        c = clip("model.orders")
        ev = c.events
        g = d["generated"]
        names = [r"no memory", r"one note of memory", r"two notes of memory"]
        rolls = VGroup(*[roll(g[k], width=9.0, height=1.0, lo=-6, hi=10, lines=(0,), color=CHANCE_C, thick=0.11) for k in "012"]).arrange(DOWN, buff=0.32).move_to(RIGHT * 1.0 + UP * 1.0)
        tags = VGroup(*[label(nm, font_size=24, color=GREY_A).next_to(r, LEFT, buff=0.3) for nm, r in zip(names, rolls)])
        head = label(r"three melodies made up by the model", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A model that predicts can also invent: draw each next note from its own expectations. "
            "Here are three melodies it made up: with no memory, with one note of memory, with two."
        ):
            self.play(FadeIn(head), FadeIn(rolls), FadeIn(tags))
        note = listen_note(r"When does it begin to sound like a tune? \ And what is still missing?", width=7.5).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"three made-up melodies", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(3):
                sing(snd, rolls[k], d["gen_times"][str(k)], hot=WHITE, base=CHANCE_C)
                pulse(snd, tags[k], ev[f"o{k}"], ev[f"o{k + 1}"] - 0.5 if k < 2 else c.duration, buff=0.1)
        with self.voiceover(
            "With no memory, the notes are the right notes and the result is nonsense. With memory, it "
            "begins to step and to repeat, and for a moment it sounds like something. But it has no "
            "phrases, no arch, no questions and answers, and no home. Those are shapes longer than two "
            "notes, and a model has to be built to look for them."
        ):
            self.play(FadeOut(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extremes(self):
        d = load("more")["extremes"]
        c = clip("model.extremes")
        ev = c.events
        e, h = d["easy"], d["hard"]
        re_ = roll(e["pitches"], e["beats"], width=5.6, height=2.2, lines=(0,), color=TUNE).move_to(LEFT * 3.3 + UP * 0.3)
        rh = roll(h["pitches"], h["beats"], width=5.6, height=2.2, lines=(0,), color=EAR).move_to(RIGHT * 3.3 + UP * 0.3)
        le = VGroup(label(r"easiest: \ \textit{Ode to Joy}", font_size=26, color=TUNE), label(rf"{e['bits']:.1f} bits a note", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(re_, UP, buff=0.2)
        lh = VGroup(label(r"hardest: \ \textit{Korobeiniki} \ (Russia)", font_size=26, color=EAR), label(rf"{h['bits']:.1f} bits a note", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(rh, UP, buff=0.2)
        head = label(r"every tune, \ scored by a model that learnt from the other fifty-three", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Do the same for every tune in the library: train on the others, and score the one left "
            f"out. The Tune, at {say(d['tune_bits'], 1)} bits a note, is number {say(d['tune_rank'])} "
            "of fifty-four: ordinary. The most predictable is Beethoven's Ode to Joy, almost nothing "
            "but steps. The least predictable is a Russian tune in a minor key. Listen to the opening "
            "of each."
        ):
            self.play(FadeIn(head), FadeIn(re_), FadeIn(le), FadeIn(rh), FadeIn(lh))
        with self.listen(c) as snd:
            window(snd, r"easiest, \ then hardest", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, re_, d["times"]["easy"], hot=WHITE, base=TUNE)
            sing(snd, rh, d["times"]["hard"], hot=WHITE, base=EAR)
            pulse(snd, le, ev["easy"], ev["hard"] - 0.5, buff=0.1)
            pulse(snd, lh, ev["hard"], c.duration, buff=0.1)
        cap = VGroup(label(r"the model grew up on tunes in major keys.", font_size=28, color=WHITE), label(r"what a listener expects is what that listener has heard.", font_size=30, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Nothing is wrong with the second tune: millions of people know it by heart. But our model "
            "grew up almost entirely on tunes in major keys, and a minor-key melody from somewhere else "
            "surprises it at every turn. That is not a flaw in the method. It is the most important "
            "thing the method shows. What a listener expects is what that listener has heard, and a "
            "tune that is obvious in one tradition is strange in another."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
