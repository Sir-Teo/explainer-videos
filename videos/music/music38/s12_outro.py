from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation38")
        head = VGroup(label(r"Variation 38", font_size=48, color=TUNE), label(r"the Tune, \ blue, \ ragged and swung", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        basic = [["C7"], ["C7"], ["C7"], ["C7"], ["F7"], ["F7"], ["C7"], ["C7"], ["G7"], ["F7"], ["C7"], ["G7"]]
        blues = chart(basic, cell_w=0.95, cell_h=0.5, size=15)
        rag_notes = [[m, a / d["rag_q"], du / d["rag_q"]] for m, a, du in d["rag_rh"]]
        rag = mroll(rag_notes, width=3.8, height=1.8, lo=70, hi=92, color=BLUE, total=32, bar_h=0.07)
        riff = chart(basic, cell_w=0.95, cell_h=0.5, size=15)
        panels = VGroup(VGroup(label(r"a twelve-bar blues, \ sung with blue thirds", font_size=17, color=TUNE), blues).arrange(DOWN, buff=0.25),
                        VGroup(label(r"a rag: \ syncopated right hand", font_size=17, color=BLUE), rag).arrange(DOWN, buff=0.25),
                        VGroup(label(r"a riff chart: \ saxes and brass", font_size=17, color=EAR), riff).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        panels.scale_to_fit_width(min(panels.width, 13.2))
        rs = d["rag_sync"]
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First, its two phrases "
            "as a twelve-bar blues: the first phrase over the tonic, again over the subdominant, the second phrase over the "
            "last line, sung by the model voice with its thirds bent thirty-five cents flat. Then as a rag: each note of the "
            "Tune turned into Joplin's short-long-short figure in the right hand, over an oom-pah left hand, "
            f"{say(rs['syncopated'])} of the right hand's {say(rs['onsets'])} attacks syncopated. And last as a riff chart: "
            "the Tune's opening as the saxophones' riff, its cadence as the brass's answer, swung over the rhythm section."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels))
        st = d["starts"]
        bar1 = 4 * 60.0 / d["blues_bpm"]
        bar3 = 4 * 60.0 / d["riff_bpm"]
        with self.listen(c) as snd:
            window(snd, r"Variation 38", kind="synthesized", detail=r"a model voice, \ piano, \ additive horns, \ string and cymbal", corner=DL, tag_corner=DR)
            for i in range(12):
                pulse(snd, blues.bars[i], st["blues"] + i * bar1, st["blues"] + (i + 1) * bar1 - 0.03, buff=0.02)
                pulse(snd, riff.bars[i], st["riff"] + i * bar3, st["riff"] + (i + 1) * bar3 - 0.03, buff=0.02)
            flash(snd, rag.notes, [st["rag"] + a * d["rag_q"] for _, a, _ in rag_notes], hot=WHITE, base=BLUE)
            pulse(snd, panels[1][0], st["rag"], st["riff"] - 0.5, buff=0.08)
        self.play(FadeOut(panels))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-eight of the ledger: {say(v['seconds'])} seconds; the measurements are the blue third, the rag's "
            "syncopations, and the riff's swing ratio."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"the twelve-bar blues: \ three lines of four, \ every chord a seventh",
            r"blue notes are regions, \ not pitches; \ the lyric is AAB, \ with room for answers",
            r"ragtime: \ a syncopated right hand over a march left hand, \ counted in Joplin's rag",
            r"swing: \ about 3 to 1 slow, \ even fast, \ the short note near a tenth of a second",
            r"walking bass and guide tones as shortest paths through the changes",
            r"ii--V--I, \ turnarounds, \ and the tritone shared by two dominants",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The twelve-bar blues is three lines of four, using seventh chords in this basic version. <bookmark mark='a'/> Blue notes are regions, not pitches, and the lyric is A A B, with room for answers. <bookmark mark='b'/> Ragtime sets a syncopated right hand over a march-like left, as the counts in Joplin's rag show. <bookmark mark='c'/> Swing is about three to one at slow tempos and even at fast ones, with the short note near a tenth of a second. <bookmark mark='d'/> These bass and guide-tone solvers optimize their stated costs and constraints; real players use additional musical goals. <bookmark mark='e'/> And two-five-one, turnarounds, and the tritone that two dominant sevenths share are the material of jazz harmony."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Using the model, \ compute the swing ratio and the short note's length at 140 and 240 beats a minute.",
            r"Prove that exactly two dominant seventh chords contain any given tritone.",
            r"\textbf{Ear.} \ The lab plays ii--V--I's, \ some with tritone substitutes; \ say which.",
            r"\textbf{Build.} \ Extend the walking-bass generator with skips and triplets, \ and keep its rules.",
            r"$\bigstar$ \ What makes a performance swing, \ and for whom?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"standards, \ changes and reharmonisation", [39]),
            (r"the riff, \ the backbeat and the song", [40]),
            (r"arranging for a band", [41]),
            (r"performing and improvising", [43]),
            (r"beat tracking and chord recognition", [62]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in standards, changes and reharmonisation. In the riff, the backbeat and the "
            "song. In arranging for a band. In performing and improvising. And in machines that track beats and recognise "
            "chords."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"jazz students", r"practise guide-tone lines through standards before they solo"),
            (r"bassists", r"learn to walk by targeting roots and approaching by semitones"),
            (r"producers", r"set a drum machine's swing amount, \ a ratio by another name"),
            (r"pianists", r"learn Joplin from the score, \ and stride by ear"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Jazz students practise guide-tone lines through standards before they solo. Bassists learn to "
            "walk by targeting roots and approaching them by semitones. Producers set a drum machine's swing amount, which "
            "is a ratio by another name. And pianists learn Joplin from the score, and stride by ear."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"G. Kubik, \ \textit{Africa and the Blues} \ (1999)",
             r"E. Berlin, \ \textit{Ragtime: \ A Musical and Cultural History} \ (1980)",
             r"G. Schuller, \ \textit{The Swing Era} \ (1989)",
             r"P. F. Berliner, \ \textit{Thinking in Jazz} \ (1994)"],
            [r"A. Friberg and J. Sundstr\"om, \ `Swing ratios and ensemble timing in jazz performance' \ (2002)",
             r"F. Benadon, \ `Slicing the beat' \ (2006)",
             r"G. Datseris and others, \ `Does it swing?' \ (2019)",
             r"C. Nelias and others, \ `Downbeat delays are a key component of swing in jazz' \ (2022)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"how do jazz players turn a song's chords into a lifetime of new melodies?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VI: \ many musics", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"The blues and swing gave jazz its language.", font_size=24, color=WHITE).move_to(UP * 1.7)
        lead.scale_to_fit_width(min(lead.width, 12.5))
        nxt = VGroup(label(r"Part 39", font_size=32, color=GREY_B), label(r"Changes", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The blues and swing gave jazz its language. <bookmark mark='a'/> How do jazz players turn a song's chords into a "
            "lifetime of new melodies? <bookmark mark='b'/> Next time. Part 39: Changes."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
