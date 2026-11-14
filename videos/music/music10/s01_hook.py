from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def tablet(line) -> VGroup:
    """A clay tablet: the words of a hymn above a double line, and under it words followed by numbers."""
    rng = np.random.default_rng(3)
    body = RoundedRectangle(width=9.6, height=3.9, corner_radius=0.45, stroke_color="#8B6B4A", stroke_width=3, fill_color=CLAY, fill_opacity=0.22)
    wedges = VGroup()
    for row in range(4):
        x = -4.3
        y = 1.5 - 0.36 * row
        while x < 4.3:
            w = float(rng.uniform(0.08, 0.2))
            wedges.add(Line([x, y, 0], [x + w, y + float(rng.uniform(-0.08, 0.08)), 0], color=CLAY, stroke_width=float(rng.uniform(2, 4))))
            x += w + float(rng.uniform(0.05, 0.16))
    rule = VGroup(Line([-4.4, 0.1, 0], [4.4, 0.1, 0], color=CLAY, stroke_width=2), Line([-4.4, 0.02, 0], [4.4, 0.02, 0], color=CLAY, stroke_width=2))
    words = VGroup()
    for w, n in line:
        words.add(VGroup(Text(w, font_size=30, color=PAGE, slant="ITALIC"), Text(str(n), font_size=34, color=INK, weight="BOLD")).arrange(RIGHT, buff=0.16))
    words.arrange(RIGHT, buff=0.42).move_to([0, -0.75, 0])
    more = VGroup(*[Line([-4.2, -1.35 - 0.3 * k, 0], [4.2 - 1.6 * k, -1.35 - 0.3 * k, 0], color=CLAY, stroke_width=2, stroke_opacity=0.5).set_stroke(opacity=0.45) for k in range(2)])
    g = VGroup(body, wedges, rule, words, more)
    g.words, g.wedges, g.rule = words, wedges, rule
    return g


class Hook(SoundScene):
    def construct(self):
        self.the_tablet()
        self.memory()
        self.plan()

    # ------------------------------------------------------------------
    def the_tablet(self):
        d = load("hook")
        c = clip("hook.readings")
        tab = tablet(d["line"]).move_to(UP * 0.9)
        where = label(r"Ugarit, \ on the coast of Syria \ $\cdot$ \ about 1400 \textsc{bce}", font_size=26, color=GREY_A).next_to(tab, UP, buff=0.2)
        with self.voiceover(
            "This is a clay tablet. It was dug up in the nineteen fifties from the ruins of Ugarit, a port on "
            "the coast of Syria, and it was written about fourteen hundred years before the common era. Above "
            "the double line are the words of a hymn to Nikkal, the goddess of orchards. <bookmark mark='a'/> "
            "Below the line is something else: words, each followed by a number. Three. One. Three. One. Ten. "
            "<bookmark mark='b'/> We know what the words are. Each one is the name of a pair of strings on a "
            "lyre; another tablet lists them. This is written music, the oldest that survives nearly whole. "
            "And nobody knows how it goes."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab.wedges), FadeIn(tab.rule), FadeIn(tab[4]), FadeIn(where), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in tab.words], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("b")
            self.play(*[Indicate(w[0], color=INK, scale_factor=1.08) for w in tab.words], run_time=1.2)
        note = listen_note(r"one line, \ read two ways. \ A: \ the two strings together, \ as many times as the number says. \\ "
                           r"B: \ one string, \ then the other as many times; \ and the lyre counted from its other end.", width=10.5, font_size=24).to_edge(DOWN, buff=0.35)
        bx = boxes(("A", "B"), buff=0.8, width=1.3, height=0.8, font_size=34).next_to(tab, DOWN, buff=0.25)
        with self.voiceover(
            "Here is that first line, read by Monochord in two ways. In the first, the two strings are struck "
            "together, as many times as the number says. In the second, one string is struck and then the "
            "other, and the strings are counted from the other end of the lyre."
        ):
            self.play(FadeIn(note), FadeIn(bx))
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"one line of the tablet, \ two readings", detail=r"Part 1's string; \ not a reconstruction", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 0.9)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
            both = list(d["words_a"]) + list(d["words_b"])
            marks = [w for w in tab.words] * 2
            light(snd, marks[:5], d["words_a"], base=PAGE, end=snd.time_of("B") - 0.9, part=lambda w: w[0])
            for k, t in enumerate(both):                        # each word steps forward as its strings sound
                snd.wait_until(t)
                self.play(marks[k].animate(rate_func=there_and_back).shift(UP * 0.12), run_time=0.3)
        for w in tab.words:
            w[0].set_color(PAGE)
        claim = VGroup(label(r"at least five published reconstructions, \ no two alike", font_size=30, color=BAD),
                       label(r"the scribe left out what every musician in Ugarit already knew", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "The same marks. Neither of those is a claim about what was sung in Ugarit, and that is the "
            "point. <bookmark mark='a'/> At least five scholars have published reconstructions of this hymn, "
            "and no two of them sound alike. Is a pair of strings played together, or one after the other? "
            "Does the number count notes, or beats, or repeats? Which end of the lyre is string one? "
            "<bookmark mark='b'/> The tablet does not say, because it did not need to. The scribe left out "
            "what every musician in Ugarit already knew. Then the musicians died."
        ) as vo:
            self.play(FadeOut(bx))
            vo.wait_until("a")
            self.play(FadeIn(claim[0]))
            vo.wait_until("b")
            self.play(FadeIn(claim[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        card = history_card(630, r"Isidore of Seville, \ \textit{Etymologies}",
                            r"``unless sounds are held in the memory of man, \ they perish, \ for they cannot be written down''", width=7.4, font_size=24).to_edge(UP, buff=0.45)
        t = 0.0
        rows = []
        for n in TUNE_SCORE.voices[0].notes[:14]:
            b = float(n.dur * 4)
            rows.append((t, b, n.pitch.midi))
            t += b
        roll = piano_roll(rows, width=8.0, height=2.4, color=TUNE).move_to(DOWN * 1.3)
        ax_t = Arrow(roll.frame.get_corner(DL) + DOWN * 0.3, roll.frame.get_corner(DR) + DOWN * 0.3, buff=0, color=TIME, stroke_width=3, tip_length=0.18)
        ax_p = Arrow(roll.frame.get_corner(DL) + LEFT * 0.3, roll.frame.get_corner(UL) + LEFT * 0.3, buff=0, color=FREQ, stroke_width=3, tip_length=0.18)
        lt = label(r"when, \ and for how long", font_size=24, color=TIME).next_to(ax_t, DOWN, buff=0.1)
        lp = label(r"which note", font_size=24, color=FREQ).rotate(PI / 2).next_to(ax_p, LEFT, buff=0.1)
        letters = VGroup(*[Text(t, font="FreeSerif", font_size=30, color=INK) for t in ("C", "Z", "Z", "KIZ", "I")])
        words = VGroup(*[Text(t, font="FreeSerif", font_size=36, color=PAGE) for t in ("Ὅ", "σον", "ζῇς", "φαί", "νου")]).arrange(RIGHT, buff=0.3)
        for a, b in zip(letters, words):
            a.next_to(b, UP, buff=0.2)
        greek = VGroup(words, letters, label(r"a Greek song on a tombstone, \ first or second century: \ letters for the notes, \ above the words", font_size=24, color=GREY_A).next_to(words, DOWN, buff=0.4)).move_to(DOWN * 0.3)
        mem = label(r"the chants of the church: \ thousands, \ all held in memory. \ Ten years to train a singer.", font_size=28, color=BAD).move_to(DOWN * 2.4)
        with self.voiceover(
            "Two thousand years later, around the year 630, Isidore, the bishop of Seville, set out to write "
            "down everything that was known. On music he wrote this: unless sounds are held in the memory of "
            "man, they perish, for they cannot be written down. <bookmark mark='a'/> He was wrong. The Greeks "
            "had written melodies with letters, and a song carved on a tombstone in their notation can still "
            "be sung. But in Isidore's world nobody could read it any more. Every chant of the church, "
            "thousands of them, lived in the heads of singers, and it took ten years to train one. "
            "<bookmark mark='b'/> So what would writing a tune down take? A tune is a list of events: which "
            "note, when, and for how long. That is a picture with two axes. Four centuries after Isidore, "
            "somebody drew it."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(greek))
            self.wait(9.0)
            self.play(FadeIn(mem))
            vo.wait_until("b")
            self.play(FadeOut(greek), FadeOut(mem))
            self.play(FadeIn(roll.frame), FadeIn(roll.grid), GrowArrow(ax_t), GrowArrow(ax_p), FadeIn(lt), FadeIn(lp))
            self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in roll.notes], lag_ratio=0.12), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"every notation keeps some things", font_size=32, color=GOOD), label(r"and throws the rest away.", font_size=32, color=BAD)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"neumes: \ a reminder for someone who knows the tune",
            r"Guido's lines: \ pitch becomes height on a page",
            r"shapes that say how long; \ bars and scores",
            r"writing what to do: \ tablature and figured bass",
            r"numbers, \ characters, \ holes in paper, \ bytes",
            r"how many bits a score holds, \ and what no notation holds",
        ], title=r"Part 10: \ Writing It Down", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "Welcome to Act Two. For nine parts we made sounds. Now we have to say which ones, and when, to "
            "somebody who is not in the room. Every way of doing that keeps some things and throws the rest "
            "away, and this part asks, of each notation: what did it keep? <bookmark mark='a'/> We begin "
            "with signs that only remind a singer of a tune already learned. <bookmark mark='b'/> Then four "
            "lines that turn pitch into height on a page. <bookmark mark='c'/> Shapes that say how long a "
            "note lasts, and the bar lines and scores that let many people read together. <bookmark mark='d'/> "
            "Notations that say what to do with your hands instead of what you will hear. <bookmark mark='e'/> "
            "Numbers, characters, holes in paper and bytes. <bookmark mark='f'/> And at the end we count: how "
            "many bits are in a score, how many in its sound, and where the difference goes."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
