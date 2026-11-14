from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Bach(SoundScene):
    def construct(self):
        chapter(self, 9, r"How smooth is Bach?", r"Does Bach take the shortest paths?", extra=((1731, r"\textit{Wachet auf}, \ BWV 140"),))
        self.phrase()
        self.census()
        self.quiz()
        self.parity()
        self.limits()

    # ------------------------------------------------------------------
    def phrase(self):
        d = load("bach")
        c = clip("bach.phrase")
        g = voices_roll(d["voices"], width=10.6, height=2.6, colors=[TUNE, BLUE, EAR, "#A3E635"]).move_to(UP * 0.9)
        ch = d["changes"]
        cells = VGroup()
        for x in ch:
            cells.add(VGroup(label(rf"{x['actual3']}", font_size=20, color=WHITE), label(rf"{x['minimal3']:.0f}", font_size=20, color=TUNE)).arrange(DOWN, buff=0.12))
        fr = g.frame
        for i, x in enumerate(ch):
            cells[i].move_to([fr.get_left()[0] + fr.width * x["t"] / g.total, fr.get_bottom()[1] - 0.75, 0])
        key = VGroup(label(r"upper three voices: \ semitones Bach moves", font_size=18, color=WHITE),
                     label(r"the smallest possible between the same chords", font_size=18, color=TUNE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(DOWN, buff=0.9)
        head = label(r"\textit{Wachet auf}, \ BWV 140.7: \ the first phrase", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now a measurement. Here is the first phrase of Bach's chorale Wachet auf, in four voices, played on the piano. "
            "Under each change of chord on the beat, two numbers for the upper three voices: the semitones Bach's voices "
            "actually move, and the smallest number any voicing could move between the same two chords. Where the numbers "
            "match, Bach took a shortest path. The first two changes are not changes at all: the same chord, E flat major, "
            "re-voiced as the tune climbs its arpeggio."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cells), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"\textit{Wachet auf}, \ phrase 1", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            cursor(snd, g, 0.0, d["phrase_unit"])
            for i, x in enumerate(ch):
                pulse(snd, cells[i], x["t"] * d["phrase_unit"], x["t"] * d["phrase_unit"] + 0.6, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def census(self):
        d = load("bach")
        a, u = d["all"], d["upper"]
        hist = [u["excess_hist"][k] for k in (0, 2, 4, 6)]
        bars = columns(hist, ["0", "2", "4", "6"], width=5.0, height=2.8, color=GREY_B, hot=(0,), hot_color=TUNE, fmt="{:,.0f}", font_size=17).move_to(LEFT * 3.4 + DOWN * 0.4)
        xl = label(r"semitones more than the minimum \ (upper voices)", font_size=18, color=GREY_A).next_to(bars, DOWN, buff=0.4)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (rf"{u['n']:,} changes of chord on the beat, \ 364 chorales", WHITE),
            (rf"upper three voices: \ the minimum in {100 * u['minimal_share']:.0f} changes in 100", TUNE),
            (rf"mean: \ Bach {u['mean_actual']:.1f}, \ minimum {u['mean_minimal']:.1f}, \ voices shuffled {u['mean_shuffled']:.1f}", WHITE),
            (rf"with the bass: \ minimum in {100 * a['minimal_share']:.0f} in 100; \ mean {a['mean_actual']:.1f} against {a['mean_minimal']:.1f}", EAR),
            (r"the bass leaps by fourths and fifths: \ it carries the roots, \ not a smooth line", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4)).move_to(RIGHT * 3.0)
        head = label(r"all of Bach's chorales, \ measured", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Now all of them: {say(u['n'])} changes of chord on the beat, in three hundred and sixty-four chorales. "
            f"<bookmark mark='a'/> In the upper three voices Bach's voice leading is the smallest possible in "
            f"{say(round(100 * u['minimal_share']))} changes out of a hundred. <bookmark mark='b'/> On average his upper voices move "
            f"{say(round(u['mean_actual'], 1))} semitones per change, against a minimum of {say(round(u['mean_minimal'], 1))}; "
            f"give the same notes to the voices at random and they would move {say(round(u['mean_shuffled'], 1))}. "
            f"<bookmark mark='c'/> With the bass included, the minimum is reached only {say(round(100 * a['minimal_share']))} "
            "times in a hundred, <bookmark mark='d'/> and for a good reason: the bass leaps by fourths and fifths to carry "
            "the roots of the chords, as Part 17 found. Bach writes nearly shortest paths above a bass that does a "
            "different job."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("bach")
        c = clip("bach.quiz")
        card = listen_card(r"The same nine chords twice, \ one on each beat. \ In one, \ the voices are Bach's; \ "
                           r"in the other, \ each chord's upper notes were handed to the voices at random. \ Which is Bach's, \ A or B?", width=10.4)
        with self.voiceover(
            "Can you hear the difference? The beat chords of that phrase, twice. In one, the voices are Bach's. In the "
            "other, each chord's three upper notes were handed out to the soprano, alto and tenor at random, kept near "
            "their own registers. The chords are identical; only the paths between them differ. Which is Bach's, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = voices_roll([[[m[j], float(i), 1.0] for i, m in enumerate(d["chords_a"])] for j in range(4)], width=5.4, height=2.4,
                         colors=[TUNE, BLUE, EAR, "#A3E635"]).move_to(LEFT * 3.2 + DOWN * 0.1)
        gb = voices_roll([[[m[j], float(i), 1.0] for i, m in enumerate(d["chords_b"])] for j in range(4)], width=5.4, height=2.4,
                         colors=[TUNE, BLUE, EAR, "#A3E635"]).move_to(RIGHT * 3.2 + DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            cursor(snd, ga, d["starts"]["A"], d["unit"])
            cursor(snd, gb, d["starts"]["B"], d["unit"])
        ans = VGroup(label(rf"A: \ Bach, \ {d['tot_a']} semitones in the upper voices", font_size=20, color=TUNE).next_to(ga, DOWN, buff=0.35),
                     label(rf"B: \ shuffled, \ {d['tot_b']} semitones", font_size=20, color=EAR).next_to(gb, DOWN, buff=0.35))
        with self.voiceover(
            f"A is Bach's: his upper voices move {say(d['tot_a'])} semitones across the phrase; the shuffled version moves "
            f"{say(d['tot_b'])}, about twice as far, and you can hear the lines jump and tangle. Same chords, same harmony; "
            "the difference is entirely in the paths."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parity(self):
        d = load("bach")
        rows_ = text_rows([
            (r"a curiosity in the census: \ Bach's excess over the minimum is always even: \ 0, \ 2, \ 4, \ 6 ...", WHITE),
            (r"why: \ a voice's real move and its shortest move differ by octaves and direction, \ so their sizes have the same parity", WHITE),
            (r"and the parity of a total move does not depend on which voice gets which note", WHITE),
            (r"so any voicing of a progression has the same parity as the minimum: \ the excess is even", TUNE),
            (r"a theorem checked by 17,339 examples: \ the census and the proof agree", GREY_A),
        ], font_size=23)
        head = label(r"why the excess is always even", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The census hides a curiosity. <bookmark mark='a'/> Bach's excess over the minimum is always an even number: "
            "zero, two, four, six, never one or three. <bookmark mark='b'/> Here is why. A voice's real move and its shortest "
            "move round the octave differ by whole octaves and perhaps by direction, so their sizes are both even or both "
            "odd. <bookmark mark='c'/> And the parity of a total move depends only on the sum of the notes before and after, "
            "not on which voice takes which note. <bookmark mark='d'/> So every voicing of a progression has the same parity "
            f"as the minimum, and the excess must be even. <bookmark mark='e'/> A small theorem, and {say(d['upper']['n'])} "
            "chord changes that agree with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"the minimum ignores register: \ it may cross voices or leave the singers' ranges", WHITE),
            (r"Bach also avoids parallel fifths, \ doubles the right notes, \ shapes the soprano \ (Parts 16, \ 17)", WHITE),
            (r"Tymoczko's reading: \ near-minimal paths among nearly even chords; \ Huron's: \ auditory streaming", WHITE),
            (r"both predict what we measured; \ neither alone explains why one minimal path is chosen over another", TUNE),
            (r"Part 17's harmonizer moved its inner voices half as much as Bach: \ the shortest path is not the whole story", GREY_A),
        ]
        rows_scene(self, r"what the measurement says, \ and does not", items,
                   "What does this show? <bookmark mark='b'/> The minimum ignores register: it may cross voices or leave a "
                   "singer's range. <bookmark mark='c'/> Bach also obeys other rules: no parallel fifths, sensible doublings, a "
                   "shaped melody. <bookmark mark='d'/> Tymoczko reads the result as near-minimal paths among nearly even chords; "
                   "David Huron explains the same habits by how the ear separates voices into streams. <bookmark mark='e'/> Both "
                   "predict what we measured, and neither alone says which of several shortest paths Bach will choose. "
                   "<bookmark mark='f'/> Part 17's harmonizer moved its inner voices about half as much as Bach did: the shortest "
                   "path is not the whole story.", marks="cdef")
