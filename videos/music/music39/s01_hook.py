from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.fast()
        self.date()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.giant")
        card = listen_card(r"Sixteen bars of chords, \ comped by piano, \ bass and cymbal, \ no melody. \ "
                           r"How many different keys does the progression come home to: \ one, \ two, \ or three?", width=10.4)
        with self.voiceover(
            "A question for your ears. Sixteen bars of chords, comped by piano, bass and cymbal, with no melody. A key is "
            "where a progression comes home to rest. How many different keys does this one come home to: one, two, or "
            "three?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ch = chart(d["changes"], cell_w=2.6, cell_h=0.75, size=20).move_to(UP * 0.2)
        self.play(FadeOut(card), FadeIn(ch))
        bar = 4 * 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"sixteen bars of changes", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            for i in range(16):
                pulse(snd, ch.bars[i], i * bar, (i + 1) * bar - 0.03, buff=0.03)
        colors = {11: TUNE, 7: BLUE, 3: EAR}
        marks = []
        for b, barc in enumerate(d["changes"]):
            for s in barc:
                if not any(s.endswith(q) for q in ("7", "m")):
                    root = {"B": 11, "G": 7, "Eb": 3}[s]
                    marks.append(SurroundingRectangle(ch.bars[b], color=colors[root], buff=0.02, stroke_width=4))
        ans = label(r"three: \ B, \ G and E$\flat$ major, \ each a major third from the next", font_size=22, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            f"Three. The progression comes home to B major, G major and E flat major, again and again, and each is a major third from the next. That is {say(d['chords'])} chords in sixteen bars, a new key every few beats. These are the changes of John Coltrane's Giant Steps, as lead sheets give them; these changes are widely shared practice material; rights in melodies and arrangements require separate consideration, so we play the chords and none of the tune."
        ):
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.05), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fast(self):
        d = load("fast")
        c = clip("fast.giant")
        line = [tuple(x) for x in d["line"]]
        g = line_over(line, d["changes"], width=12.0, height=2.6, color=TUNE, lo=56, hi=86, size=11).move_to(DOWN * 0.2)
        head = label(rf"the same changes at {d['bpm']} beats a minute, \ with this part's improviser on the piano", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Now the same changes at the speed of the original recording, about {say(d['bpm'])} beats a minute, with the "
            "improviser this part will build playing a line through them on the piano. Sixteen bars pass in under fifteen "
            "seconds; eighth notes are about a tenth of a second apart; players can prepare and retrieve larger gestures rather than consciously choose each note from scratch."
        ):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"Giant Steps' changes, \ at speed", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, list(BL.swing_times([e for _, e in line], d["bpm"])), hot=WHITE, base=TUNE)
            cursor(snd, g.roll, 0.0, 30.0 / d["bpm"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def date(self):
        items = [
            (r"5 May 1959, \ New York: \ Coltrane records \textit{Giant Steps}, \ at nearly 290 beats a minute", WHITE),
            (r"the pianist, \ Tommy Flanagan, \ had seen the changes only briefly; \ his solo is short and careful", WHITE),
            (r"a new chord every two beats, \ in keys that share few notes", WHITE),
            (r"why are these changes hard, \ and how do improvisers play through any changes at all?", TUNE),
            (r"this part explains them, \ draws them on Part 31's Tonnetz, \ and builds an improviser", GREY_A),
        ]
        rows_scene(self, r"Giant Steps", items,
                   "On the fifth of May 1959 in New York, John Coltrane recorded Giant Steps, at nearly two hundred and ninety beats a minute. <bookmark mark='b'/> His pianist, Tommy Flanagan, had seen the changes only briefly, and his solo is short and careful, a famous moment of a great player meeting something new. <bookmark mark='c'/> Often a new chord after two beats, in keys that share few notes. <bookmark mark='d'/> Why are these changes hard, and how do improvisers play through any changes at all? <bookmark mark='e'/> This part explains them, draws them on Part 31's Tonnetz, and builds an improviser.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"bebop and the contrafact: \ new melodies on old changes",
            r"the bebop scale, \ and a proof that it lands chord tones on the beat",
            r"enclosures, \ formulas, \ and chord scales",
            r"modal jazz and quartal voicings; \ third cycles on the Tonnetz",
            r"reharmonisation",
            r"an improviser, \ judged; \ free jazz; \ what improvisers are doing",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Bebop, and the contrafact: new melodies on old changes. <bookmark mark='b'/> The bebop "
            "scale, and a proof that it puts chord tones on the beat. <bookmark mark='c'/> Enclosures, formulas, and chord "
            "scales. <bookmark mark='d'/> Modal jazz, quartal voicings, and Coltrane's third cycles drawn on the Tonnetz. "
            "<bookmark mark='e'/> Reharmonisation. <bookmark mark='f'/> And an improviser of our own, judged by the "
            "series' measures; then free jazz, and what improvisers are actually doing. Every line heard is ours or the "
            "program's; well-known tunes appear only as their chords."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
