from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


class Xml(SoundScene):
    def construct(self):
        chapter(self, 8, r"The page as data", r"Can a file hold the page itself?", extra=((2004, r"MusicXML"),))
        self.three()
        self.trips()
        self.table()

    # ------------------------------------------------------------------
    def three(self):
        d = load("xml")
        midi = VGroup(label(r"MIDI \ (1983)", font_size=28, color=TUNE), Text(d["midi_note"][:14], font=MONO, font_size=26, color=WHITE), Text(d["midi_note"][15:], font=MONO, font_size=26, color=WHITE),
                      label(r"9 bytes: \ a key, \ a time", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.25)
        xml = VGroup(label(r"MusicXML \ (2004)", font_size=28, color=TUNE), code_block(d["xml_note"], font_size=24, line_step=0.4)).arrange(DOWN, buff=0.3)
        mei = VGroup(label(r"MEI", font_size=28, color=TUNE), code_block(d["mei_note"], font_size=24, line_step=0.4), label(r"the same facts, \ as attributes", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.3)
        left = VGroup(midi, mei).arrange(DOWN, buff=0.8)
        row = VGroup(left, xml).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
        if row.width > 12.8:
            row.scale(12.8 / row.width)
        head = label(r"the first note of the Tune, \ three ways", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        lines = xml[1].rows
        intro = rows_card([
            (r"MIDI, \ 1983", r"for instruments: \ which key, \ when, \ how hard"),
            (r"MusicXML, \ 2004", r"for notation programs: \ the page, \ so that one program can hand it to another"),
            (r"MEI", r"for scholars and libraries: \ the page, \ and what an editor must say about it: \\ this note is unclear; \ this source reads differently"),
        ], left=-6.2, text_left=-2.6, top=1.6, step=1.5, name_size=32, text_size=26)
        with self.voiceover(
            "MIDI was built for instruments. People who print music, and people who study it, needed the "
            "opposite: a file that holds the page. Two formats have won. MusicXML, from 2004, lets one "
            "notation program hand a page to another. MEI, the Music Encoding Initiative, was built by "
            "scholars and librarians, and it can also say the things an editor has to say: this note is "
            "unclear in the manuscript; this source reads differently. <bookmark mark='a'/> Here is the "
            "first note of the Tune, three ways. In MIDI, key sixty and a time. <bookmark mark='b'/> In "
            "MusicXML: step C, octave four. That is a spelling; a C is not a B sharp here. Type: quarter. "
            "That is the look of the note on the page. And a syllable to print beneath it. "
            "<bookmark mark='c'/> MEI holds the same facts more compactly."
        ) as vo:
            self.play(FadeIn(intro[0]))
            self.wait(5.0)
            self.play(FadeIn(intro[1]))
            self.wait(5.5)
            self.play(FadeIn(intro[2]))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(head))
            self.play(FadeIn(midi))
            vo.wait_until("b")
            self.play(FadeIn(xml[0]), LaggedStart(*[FadeIn(r) for r in lines], lag_ratio=0.25), run_time=4.0)
            self.play(lines[2].animate.set_color(INK), lines[3].animate.set_color(INK))
            self.play(lines[6].animate.set_color(INK))
            vo.wait_until("c")
            self.play(FadeIn(mei))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trips(self):
        d = load("xml")
        src = VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=TUNE, stroke_width=2.5), label(r"Monochord's score \\ of the Tune, \ with words", font_size=24, color=TUNE)).move_to(LEFT * 4.6)
        nodes, outs, arrows = VGroup(), VGroup(), VGroup()
        for y, name, col, lines_ in ((1.6, r"MusicXML", GOOD, [r"42 of 42 notes come back the same:", r"pitch, \ spelling, \ length, \ words"]),
                                     (-1.6, r"MIDI", BAD, [r"the keys and the lengths come back.", r"The spelling and the words do not."])):
            node = VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2), label(name, font_size=28, color=WHITE)).move_to([-0.6, y, 0])
            out = VGroup(*[label(t, font_size=27, color=col) for t in lines_]).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.0, y, 0])
            arrows.add(VGroup(Arrow(src.get_right() + UP * 0.25 * np.sign(y), node.get_left(), buff=0.12, color=GREY_B, stroke_width=3, tip_length=0.16),
                              Arrow(node.get_right(), out.get_left(), buff=0.15, color=col, stroke_width=3, tip_length=0.16)))
            nodes.add(node)
            outs.add(out)
        head = label(r"write it out, \ read it back: \ what survives?", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Monochord can write all of these and read two of them back, so we can test what survives. "
            "Take the Tune with its words. <bookmark mark='a'/> Out to MusicXML and back again: all "
            "forty-two notes return identical, with their spellings, their lengths and their syllables. "
            "<bookmark mark='b'/> Out to MIDI and back: the right keys and the right lengths, and nothing "
            "else. A conversion between notations is a channel, and some channels lose information that "
            "no program can restore. Turning a MIDI file, or a recording, back into a readable page means "
            "guessing what was lost. That guessing is a research field, and we will reach it in Part 61."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0][0]), FadeIn(nodes[0]))
            self.play(GrowArrow(arrows[0][1]), FadeIn(outs[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1][0]), FadeIn(nodes[1]))
            self.play(GrowArrow(arrows[1][1]), FadeIn(outs[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        tb = keep_table(font_size=24, row_step=0.5, col_step=1.9, name_width=3.3).move_to(DOWN * 0.3)
        if tb.width > 12.8:
            tb.scale(12.8 / tb.width)
        head = label(r"what each notation keeps", font_size=32, color=TUNE).to_edge(UP, buff=0.3)
        key = VGroup(VGroup(tick_mark(1), label(r"yes", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.12), VGroup(tick_mark(0.5), label(r"in part", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.12),
                     VGroup(tick_mark(0), label(r"no", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "So here is the whole part on one page. Each row is a notation. Each column is something a "
            "notation might keep: which note, how long, how it is spelled, how to play it, and exactly "
            "when and how loud. <bookmark mark='a'/> Neumes keep the notes only in part. Guido's staff "
            "keeps the notes and their names. Mensural notes add how long. <bookmark mark='b'/> Tablature "
            "and figured bass say what to do, and give up something else for it. <bookmark mark='c'/> "
            "Gongche and jianpu keep the note's place in its scale. <bookmark mark='d'/> The modern staff "
            "keeps the most, with a little about how to play and how loud. <bookmark mark='e'/> The roll "
            "and the MIDI file keep one performance exactly, and forget the spelling. "
            "<bookmark mark='f'/> And the page formats keep the page. Now look for a row with every mark "
            "filled in. There is not one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tb.head), FadeIn(key))
            for mark, idx in zip("abcdef", ((0, 1, 2), (3, 4), (5, 6), (7,), (8, 9), (10,))):
                vo.wait_until(mark)
                self.play(LaggedStart(*[FadeIn(tb.rows[i]) for i in idx], lag_ratio=0.5), run_time=0.6 * len(idx) + 0.4)
        self.wait(1.0)
        self.clear_scene()
