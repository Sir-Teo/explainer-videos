from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Meyer(SoundScene):
    def construct(self):
        chapter(self, 1, r"Expectation", r"Where does musical feeling come from?")
        self.before()
        self.meyer()
        self.itpra()
        self.kinds()
        self.rep()
        self.limits()

    # ------------------------------------------------------------------
    def meyer(self):
        items = [
            (r"Leonard B. Meyer, \ \textit{Emotion and Meaning in Music} \ (1956)", WHITE),
            (r"emotion arises when a tendency to respond is delayed or blocked", WHITE),
            (r"music builds tendencies \ (a leading note, \ a dominant chord) \ and then plays with them", WHITE),
            (r"meaning is the relation between what is heard and what is expected next", TUNE),
            (r"a theory waiting for a way to measure expectation", GREY_A),
        ]
        rows_scene(self, r"Meyer's idea", items,
                   "The modern story starts with Leonard Meyer's book Emotion and Meaning in Music, of 1956. "
                   "<bookmark mark='b'/> His claim: emotion arises when a tendency to respond is delayed or blocked. "
                   "<bookmark mark='c'/> Music builds tendencies, a leading note, a dominant chord, and then plays with them. "
                   "<bookmark mark='d'/> Its meaning lies in the relation between what is heard and what is expected next. "
                   "<bookmark mark='e'/> It was a theory waiting for a way to measure expectation.", marks="bcde")

    # ------------------------------------------------------------------
    def itpra(self):
        stages = [(r"imagination", r"before: \ picturing outcomes", -4.8), (r"tension", r"before: \ arousal rising as the moment nears", -2.4),
                  (r"prediction", r"at the event: \ was it foreseen?", 0.0), (r"reaction", r"at once: \ a fast, \ crude response", 2.4),
                  (r"appraisal", r"after: \ a slower judgement", 4.8)]
        boxes = VGroup()
        for name, sub, x in stages:
            boxes.add(VGroup(RoundedRectangle(width=2.2, height=1.0, corner_radius=0.15, stroke_color=TUNE if name in ("prediction", "reaction") else BLUE, stroke_width=2),
                             label(name, font_size=20, color=WHITE)).arrange(ORIGIN).move_to([x, 0.6, 0]))
        subs = VGroup(*[label(sub, font_size=14, color=GREY_A).next_to(b, DOWN, buff=0.2) for (_, sub, _), b in zip(stages, boxes)])
        ev = VGroup(DashedLine([1.2, -1.4, 0], [1.2, 1.8, 0], color=EAR), label(r"the event", font_size=16, color=EAR).move_to([1.2, 2.05, 0]))
        head = label(r"Huron's ITPRA theory \ (2006)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the prediction response rewards accurate predictions, \ even of unpleasant events", font_size=18, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "David Huron's book Sweet Anticipation, of 2006, splits expectation into five responses around an event. "
            "<bookmark mark='a'/> Before it: imagination, picturing outcomes, and tension, arousal rising as the moment "
            "nears. <bookmark mark='b'/> At it: prediction, whether it was foreseen, and reaction, a fast, crude response. "
            "<bookmark mark='c'/> After it: appraisal, a slower judgement. Huron's key point: the prediction response "
            "rewards accurate prediction itself, so even a foreseen sad cadence can feel good, and a surprise can be "
            "reappraised from alarm into delight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ev))
            vo.wait_until("a")
            self.play(FadeIn(boxes[:2]), FadeIn(subs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[2:4]), FadeIn(subs[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(boxes[4]), FadeIn(subs[4]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"schematic: \ what a style has taught you \ (a dominant goes to the tonic)", WHITE),
            (r"veridical: \ what you know of this particular piece \ (the next note of a tune you know)", WHITE),
            (r"dynamic: \ what the piece so far has taught you \ (a motive repeated twice is expected a third time)", WHITE),
            (r"a deceptive cadence surprises the schema even when you know the piece by heart", TUNE),
            (r"chapter 2: \ where schemas come from", GREY_A),
        ]
        rows_scene(self, r"three kinds of expectation", items,
                   "Huron also separates three kinds of expectation. <bookmark mark='b'/> Schematic: what a style has taught you, "
                   "that a dominant goes to the tonic. <bookmark mark='c'/> Veridical: what you know of this particular piece, the "
                   "next note of a tune you know. <bookmark mark='d'/> Dynamic: what the piece so far has taught you, so a motive "
                   "heard twice is expected a third time. <bookmark mark='e'/> They can disagree: a deceptive cadence still "
                   "surprises the schema even when you know the piece by heart. <bookmark mark='f'/> Chapter two asks where "
                   "schemas come from.", marks="bcdef")

    # ------------------------------------------------------------------
    def rep(self):
        d = load("rep")
        c = clip("rep.four")
        notes, mel, t = d["notes"], [], 0.0
        for m, b in notes:
            mel.append([60 + m, t, b])
            t += b
        r = mroll(mel, width=10.0, height=1.4, lo=57, hi=71, color=TUNE, total=t, bar_h=0.13).move_to(UP * 1.0)
        leaps = [3, 7, 11, 15]
        bars = VGroup()
        for i, (k, v) in enumerate(zip(leaps, d["last_leap_ic"])):
            h = 0.25 * v
            x = r.notes[k].get_x()
            bars.add(VGroup(Rectangle(width=0.5, height=h, stroke_width=0, fill_color=EAR, fill_opacity=0.85).move_to([x, -1.6 + h / 2, 0]),
                            label(rf"{v:.1f}", font_size=16, color=WHITE).move_to([x, -1.85, 0])))
        cap = label(r"bars: \ the listener's surprise at each leap, \ in bits", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"dynamic expectation, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Dynamic expectation, heard. A motive of ours, three times, and then a fourth time with its leap changed."
        ):
            self.play(FadeIn(head), FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"a motive, \ four times", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [n[1] * 0.42 for n in mel], hot=WHITE, base=TUNE)
        v = d["last_leap_ic"]
        with self.voiceover(
            f"The listener's surprise at the leap: {say(v[0], 1)} bits the first time, {say(v[1], 1)} and {say(v[2], 1)} "
            f"once the piece has taught it, and {say(v[3], 1)} when the fourth leap goes somewhere new. The piece itself "
            "built the expectation it then broke."
        ):
            self.play(FadeIn(bars), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"expectation does not explain everything: \ timbre, \ a voice, \ the words and memories attached to a song", WHITE),
            (r"a piece moves us on its hundredth hearing, \ when nothing in it can surprise us", WHITE),
            (r"Meyer's answer, \ and Huron's: \ schematic expectation is never fully overwritten by knowing the piece", WHITE),
            (r"chapter 9 meets the other mechanisms: \ reflexes, \ contagion, \ memory", TUNE),
            (r"expectation is one engine among several, \ but the best measured", GREY_A),
        ]
        rows_scene(self, r"what expectation leaves out", items,
                   "Expectation does not explain everything. <bookmark mark='b'/> There is timbre, a voice, the words, and the "
                   "memories attached to a song. <bookmark mark='c'/> And a piece can move us on its hundredth hearing, when "
                   "nothing in it can surprise us. <bookmark mark='d'/> Meyer's answer, and Huron's, is that schematic "
                   "expectation is never fully overwritten by knowing the piece. <bookmark mark='e'/> Chapter nine meets the other "
                   "mechanisms: reflexes, contagion, memory. <bookmark mark='f'/> Expectation is one engine among several, but "
                   "the best measured.", marks="bcdef")

    # ------------------------------------------------------------------
    def before(self):
        items = [
            (r"Eduard Hanslick, \ \textit{On the Musically Beautiful} \ (1854): \ music's content is `tonally moving forms'", WHITE),
            (r"against him, \ expression theories: \ music represents or arouses the composer's feelings", WHITE),
            (r"the debate ran for a century without a way to measure either side", WHITE),
            (r"Meyer joined them: \ feeling arises from the forms themselves, \ through expectation", TUNE),
            (r"a claim about the forms that could, \ in time, \ be tested", GREY_A),
        ]
        rows_scene(self, r"forms or feelings?", items,
                   "The question is old. <bookmark mark='b'/> In 1854 Eduard Hanslick argued that music's content is tonally "
                   "moving forms, and nothing more. <bookmark mark='c'/> Against him stood expression theories: music represents "
                   "or arouses feelings. <bookmark mark='d'/> The debate ran for a century without a way to measure either side. "
                   "<bookmark mark='e'/> Meyer joined the two: feeling arises from the forms themselves, through expectation, "
                   "<bookmark mark='f'/> a claim about forms that could, in time, be tested.", marks="bcdef")
