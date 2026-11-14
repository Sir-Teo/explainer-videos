from __future__ import annotations

import numpy as np

from videos.music.music40.common import *  # noqa: F403


def verse_grid(syll, cell=0.36, col=TUNE):
    """Four bars of sixteen cells; each syllable written in its cell, accented ones filled, rhymes outlined."""
    g = VGroup()
    g.cells = []
    for bar in range(4):
        row = VGroup()
        for k in range(16):
            box = Square(cell, stroke_color=GREY_B if k % 4 == 0 else GREY_D, stroke_width=1.5 if k % 4 == 0 else 0.8)
            row.add(box)
        row.arrange(RIGHT, buff=0.02)
        g.add(row)
    g.arrange(DOWN, buff=0.12)
    for w, acc, s, r in syll:
        box = g[s // 16][s % 16]
        if acc:
            box.set_fill(col, opacity=0.55)
        if r:
            box.set_stroke(EAR, width=3)
        g.add(label(w, font_size=11, color=WHITE).move_to(box))
        g.cells.append(box)
    return g


class Flow(SoundScene):
    def construct(self):
        chapter(self, 8, r"Flow", r"How does a rapper make words into rhythm?")
        self.rap()
        self.verse()
        self.hear()
        self.measures()
        self.rhyme()
        self.writers()

    # ------------------------------------------------------------------
    def rap(self):
        items = [
            (r"rap: \ rhythmic speech over a beat, \ from 1970s Bronx parties to the world's best-selling genre", WHITE),
            (r"`flow': \ how the syllables are placed against the beat, \ grouped, \ accented and rhymed", WHITE),
            (r"Mitchell Ohriner's \textit{Flow} \ (2019) \ measures it: \ syllables on a sixteenth-note grid", WHITE),
            (r"accented syllables fall into groups of two and three sixteenths, \ like Part 37's timelines", TUNE),
            (r"a verse of ours, \ placed two ways", GREY_A),
        ]
        rows_scene(self, r"rap and flow", items,
                   "Rap is rhythmic speech over a beat, from Bronx parties in the 1970s to the best-selling genre in the world. "
                   "<bookmark mark='b'/> Its rappers speak of flow: how the syllables are placed against the beat, grouped, "
                   "accented and rhymed. <bookmark mark='c'/> The music theorist Mitchell Ohriner's book Flow, from 2019, measures "
                   "it by placing every syllable on a sixteenth-note grid. <bookmark mark='d'/> Accented syllables fall into "
                   "groups of two and three sixteenths, like Part 37's timelines. <bookmark mark='e'/> Here is a verse of ours, "
                   "placed two ways.", marks="bcde")

    # ------------------------------------------------------------------
    def verse(self):
        d = load("flow")
        text = VGroup(*[label(" ".join(words).replace("pa per", "paper").replace("walk ing", "walking").replace("ev ery", "every"), font_size=21, color=WHITE)
                        for words in d["text"]]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        text.move_to(UP * 1.6)
        a = verse_grid([tuple(x) for x in d["layouts"]["beat"]], cell=0.3, col=BLUE).move_to(DOWN * 1.0 + LEFT * 3.3)
        b = verse_grid([tuple(x) for x in d["layouts"]["threes"]], cell=0.3, col=TUNE).move_to(DOWN * 1.0 + RIGHT * 3.3)
        la = label(r"on the beat", font_size=19, color=BLUE).next_to(a, UP, buff=0.15)
        lb = label(r"in threes", font_size=19, color=TUNE).next_to(b, UP, buff=0.15)
        key = label(r"filled: \ accented syllables; \ pink outline: \ rhymes", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(r"a verse of ours", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is a four-line verse of ours, ending each line on the same rhyme. <bookmark mark='a'/> First placed on the "
            "beat: syllables mostly in eighth notes, accents on the beats, every line arriving on its rhyme at the end of "
            "the bar. <bookmark mark='b'/> Then placed in threes: syllables in sixteenths, accents every three sixteenths, "
            "cutting across the beat, the rhyme arriving early."
        ) as vo:
            self.play(FadeIn(head), FadeIn(text))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(key))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("flow")
        step = 60.0 / d["bpm"] / 4
        for kind, col in (("beat", BLUE), ("threes", TUNE)):
            c = clip("flow.beat") if kind == "beat" else clip("flow.threes")
            syll = [tuple(x) for x in d["layouts"][kind]]
            g = verse_grid(syll, cell=0.5, col=col).move_to(DOWN * 0.1)
            head = label({"beat": r"on the beat", "threes": r"in threes, \ against the beat"}[kind], font_size=26, color=col).to_edge(UP, buff=0.35)
            with self.voiceover(
                {"beat": "Hear the first placement, on Part 17's model voice, which can only speak in vowels, over a drum "
                         "machine beat.",
                 "threes": "And the second: the same words, in the same four bars, in threes against the beat."}[kind]
            ):
                self.play(FadeIn(head), FadeIn(g))
            with self.listen(c) as snd:
                window(snd, {"beat": r"on the beat", "threes": r"in threes"}[kind], kind="synthesized", detail=r"a model voice on vowels, \ drum-machine voices", corner=DL, tag_corner=DR)
                flash(snd, g.cells, [s * step for _, _, s, _ in syll], hot=WHITE, base=GREY_D)
            self.wait(0.3)
            self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        d = load("flow")
        A, B = d["stats"]["beat"], d["stats"]["threes"]
        def gaps(st):
            return r", \ ".join(rf"{k}: \ {v}" for k, v in sorted(st["gap_counts"].items(), key=lambda kv: int(kv[0])))
        rows_ = VGroup(
            label(r"measure", font_size=20, color=GREY_A), label(r"on the beat", font_size=20, color=BLUE), label(r"in threes", font_size=20, color=TUNE),
            label(r"syllables a beat", font_size=19, color=WHITE), label(f"{A['per_beat']:.1f}", font_size=19, color=WHITE), label(f"{B['per_beat']:.1f}", font_size=19, color=WHITE),
            label(r"syllables on a beat", font_size=19, color=WHITE), label(f"{round(100 * A['on_beat'])}\\%", font_size=19, color=WHITE), label(f"{round(100 * B['on_beat'])}\\%", font_size=19, color=WHITE),
            label(r"gaps between accents \ (sixteenths: \ count)", font_size=19, color=WHITE), label(gaps(A), font_size=17, color=WHITE), label(gaps(B), font_size=17, color=WHITE),
            label(r"rhyming syllables", font_size=19, color=WHITE), label(f"{round(100 * A['rhyme_share'])}\\%", font_size=19, color=WHITE), label(f"{round(100 * B['rhyme_share'])}\\%", font_size=19, color=WHITE),
        ).arrange_in_grid(rows=5, cols=3, buff=(0.8, 0.35), col_alignments="lcc").move_to(DOWN * 0.1)
        head = label(r"the two flows, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Monochord's flow measures. Both placements carry the same forty syllables, {A['per_beat']:.1f} a beat, "
            f"and rhyme on the same syllables. What differs is where they fall: {say(round(100 * A['on_beat']))} per cent of "
            f"syllables on a beat in the first, {say(round(100 * B['on_beat']))} in the second; and the gaps between accents, "
            "fours and twos in the first, almost all threes in the second, the grouping Ohriner found in many rappers' "
            "most celebrated verses."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rhyme(self):
        items = [
            (r"end rhyme: \ the last syllable of each line, \ on or near the last beat", WHITE),
            (r"internal rhyme: \ rhymes inside the line, \ like `time' and `line' in our first line", WHITE),
            (r"multisyllabic rhyme: \ two or more syllables rhyming at once, \ chained across lines", WHITE),
            (r"rhyme marks the meter: \ it tells the ear where the groups end", TUNE),
            (r"our verse: \ five rhymes on one sound, \ two on another", GREY_A),
        ]
        rows_scene(self, r"rhyme as rhythm", items,
                   "Rhyme in rap is also rhythm. <bookmark mark='b'/> End rhyme falls on the last syllable of each line, on or "
                   "near the last beat. <bookmark mark='c'/> Internal rhyme falls inside the line, like time and line in our "
                   "first line. <bookmark mark='d'/> Multisyllabic rhyme makes two or more syllables rhyme at once, chained across "
                   "lines. <bookmark mark='e'/> And rhyme marks the meter: it tells the ear where the groups end. "
                   "<bookmark mark='f'/> Our verse has five rhymes on one sound and two on another.", marks="cdef")

    # ------------------------------------------------------------------
    def writers(self):
        items = [
            (r"Adam Krims \ (2000) \ named flow styles: \ `sung', \ `percussion-effusive', \ `speech-effusive'; \ Kyle Adams \ (2009) \ their metre", WHITE),
            (r"rappers' notebooks and interviews describe writing to the beat, \ syllable by syllable", WHITE),
            (r"rhyme inside the line, \ across lines, \ and on several syllables at once, \ grew denser over decades", WHITE),
            (r"flow is prosody \ (chapter 5) \ made into the music itself", TUNE),
            (r"chapter 9: \ the build and the drop", GREY_A),
        ]
        rows_scene(self, r"the writers", items,
                   "Writers on rap have described its flows. <bookmark mark='b'/> Adam Krims, in 2000, named styles such as sung, "
                   "percussion-effusive and speech-effusive, and Kyle Adams, in 2009, analysed their metrical techniques. <bookmark mark='c'/> Rappers' notebooks and interviews describe "
                   "writing to the beat, syllable by syllable. <bookmark mark='d'/> Rhyme inside the line, across lines and on "
                   "several syllables at once grew denser over the decades. <bookmark mark='e'/> Flow is chapter five's prosody, "
                   "made into the music itself. <bookmark mark='f'/> Chapter nine turns to the build and the drop.", marks="cdef")
