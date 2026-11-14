from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403
from videos.music.variations import rows_before

NAMES = [r"in four", r"a waltz", r"in five: \ 3 + 2", r"in seven: \ 2 + 2 + 3", r"swung", r"hemiola: \ 3 + 3, \ then 2 + 2 + 2"]


def phrase_picture(ph, notes, width: float = 11.0) -> VGroup:
    """One phrase: its pulses as small marks, its accents as tall ones, its melody notes as dots above."""
    total = ph["seconds"]
    pulses = ticks(ph["pulses"], 0.0, total, width=width, height=0.3, color=WEAK, stroke_width=2)
    acc = VGroup(*[Line([pulses.x_of(t), 0, 0], [pulses.x_of(t), 0.75, 0], color=LOW, stroke_width=5) for t in ph["accents"]])
    dots = VGroup(*[Dot([pulses.x_of(n["t"] - ph["t0"]), 1.25, 0], radius=0.13, color=TUNE) for n in notes])
    g = VGroup(pulses, acc, dots)
    g.pulses, g.acc, g.dots = pulses, acc, dots
    return g


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
        c = clip("tune.variation11")
        head = VGroup(label(r"Variation 11", font_size=48, color=TUNE), label(r"one tune, \ six ways to count it", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        chips = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=0.62, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5), label(p["signature"], font_size=22, color=GREY_A)) for p in d["phrases"]]).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.95)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built "
            "ways of counting. <bookmark mark='a'/> So here is the Tune with every phrase in a different "
            "meter: in four, as we have always had it; as a waltz; in five; in seven; swung; and with a "
            "hemiola. The notes are the same forty-two. The tall marks are where the drums put the beats."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in chips], lag_ratio=0.25), run_time=3.0)
        notes = c.notes
        shown = None
        with self.listen(c) as snd:
            window(snd, r"Variation 11", detail=r"Part 7's piano; \ modelled drums", corner=DL, tag_corner=DR)
            for k, ph in enumerate(d["phrases"]):
                snd.wait_until(f"phrase{k}")
                if shown is not None:
                    self.remove(shown)
                mine = [n for n in notes if n["phrase"] == k]
                pic = phrase_picture(ph, mine).move_to(UP * 0.2)
                name = label(NAMES[k], font_size=40, color=TUNE).next_to(pic, UP, buff=0.55)
                hd = pic.pulses.head(extra=0.2)
                shown = VGroup(pic, name, hd)
                self.add(shown)
                t0 = ph["t0"]
                snd.drive(hd, lambda m, t, t0=t0, pic=pic, total=ph["seconds"]: m.set_x(pic.pulses.x_of(float(np.clip(t - t0, 0.0, total)))))
                flash(snd, list(pic.dots), [n["t"] for n in mine], base=TUNE, hot=WHITE, fade=0.2)
                pulse(snd, chips[k], t0, t0 + ph["seconds"], buff=0.06)
        self.remove(shown)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row eleven of the ledger. {say(v['seconds'])} seconds. The measurement is a count: its bars "
            "are counted in four, three, five and seven, and in six, two ways. Not one pitch was changed."
        ):
            self.play(FadeOut(chips), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        s, a, w, k = load("sync"), load("additive"), load("swing"), load("continuum")
        card = objectives_card([
            r"identical clicks are heard in twos: \ metre is added by the listener",
            r"a beat can be felt from about a quarter of a second to two seconds; \ steadiest near two a second",
            r"a metre is nested pulses; \ loud sounds begin groups and long ones end them",
            rf"syncopation: \ notes on weak pulses before silent strong ones; \ the son clave scores {s['patterns'][1]['index']}",
            rf"seven is $2{{+}}2{{+}}3$, \ three ways; \ swing is a short note of about 100 ms, \ not a ratio",
            rf"three against two, \ a hundred times a second, \ is a fifth: \ {k['cents']:.0f} cents",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Identical clicks are heard in pairs: the listener adds the meter. "
            "<bookmark mark='a'/> A beat can be felt only inside a window, from about a quarter of a "
            "second to two seconds, and best near two to the second. <bookmark mark='b'/> A meter is "
            "pulses nested inside pulses; loud sounds begin groups, and long ones end them. "
            "<bookmark mark='c'/> Syncopation can be counted: notes on weak moments, before strong "
            "moments left silent. <bookmark mark='d'/> Beats need not be equal: seven is two, two and "
            "three. And swing is not a ratio but a short note. <bookmark mark='e'/> And three against "
            "two, played a hundred times a second, is a perfect fifth. Rhythm and harmony are one scale "
            "of ratios."
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
            r"A jig is marked 132 beats to the minute in six-eight, \ the beat a dotted quarter. \ How long, \ in milliseconds, \ is a bar, \ a beat and an eighth note? \ "
            r"How fast could the tempo go before the eighth notes reached the limit of 100 ms?",
            r"Let $a(n)$ be the number of ways to fill $n$ pulses with beats of two and three. \ Show that $a(n) = a(n-2) + a(n-3)$, \ and find $a(12)$. \ "
            r"Which of the twelve have four beats?",
            r"\textbf{Ear.} \ The lab plays eight bars of six eighth notes in a random order, \ each grouped $3+3$ or $2+2+2$ by its accents. \ Say which is which.",
            r"\textbf{Build.} \ With \texttt{rhythm.syncopation}, \ find the rhythm of five notes on sixteen pulses with the largest index, \ and the largest among those that sound the downbeat. \ "
            r"Play both: \ can you still feel the beat?",
            r"$\bigstar$ \ Design an experiment that could tell whether listeners' preference for small-integer rhythms comes from hearing and moving, \ or from the music they have heard. \ "
            r"Who would your listeners be, \ and what result would settle it?",
        ], font_size=23)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"rhythm inside a melody", [14]),
            (r"where chords change in the bar", [18]),
            (r"the mathematics of rhythms: \ necklaces and evenness", [33]),
            (r"tala, \ and the timelines of West Africa", [34, 37]),
            (r"swing, \ in the hands of the people who made it", [38]),
            (r"expectation and pleasure; \ machines that find the beat", [46, 62]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Rhythm is half of every melody we will write. Meter decides where "
            "chords change. The circles of this part return as mathematics, where we ask which rhythms "
            "spread their notes most evenly. The cycles of Indian music and the bell patterns of West "
            "Africa get parts of their own, and so does swing. And the listener's expectations, which "
            "began this part, are the subject of a whole part on why music moves us."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"drummers", r"practise with a click on beats two and four only, \ or once a bar, \ so that they must supply the rest of the grid themselves"),
            (r"conductors", r"beat the level of the metre that the players need: \ in two for a fast six-eight, \ in six for a slow one"),
            (r"producers", r"set a ``swing'' amount on a drum machine: \ a percentage that delays every second sixteenth"),
            (r"dancers", r"learn a seven or an eleven as quick and slow steps, \ long before anyone counts it"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A drummer practises with a click on only two of the four beats, or one, so "
            "as to carry the grid alone. A conductor chooses which level of the meter to beat: a fast "
            "six-eight in two, a slow one in six. A producer turns a knob marked swing, which delays "
            "every second sixteenth note by a set percentage. And a dancer learns a bar of seven as "
            "quick, quick, slow, long before anybody counts it."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. London, \ \textit{Hearing in Time: Psychological Aspects of Musical Meter} \ (2nd ed., 2012)",
             r"F. Lerdahl and R. Jackendoff, \ \textit{A Generative Theory of Tonal Music} \ (1983), \ ch. 4",
             r"W. A. Sethares, \ \textit{Rhythm and Transforms} \ (2007)",
             r"H. Cowell, \ \textit{New Musical Resources} \ (1930)"],
            [r"T. L. Bolton, \ ``Rhythm'', \ \textit{American Journal of Psychology} 6 (1894)",
             r"H. Woodrow, \ ``A quantitative study of rhythm'', \ \textit{Archives of Psychology} 14 (1909)",
             r"H. C. Longuet-Higgins and C. S. Lee, \ ``The rhythmic interpretation of monophonic music'', \ \textit{Music Perception} 1 (1984)",
             r"L. van Noorden and D. Moelants, \ ``Resonance in the perception of musical pulse'', \ \textit{J. New Music Research} 28 (1999)",
             r"A. Friberg and A. Sundstr\"om, \ ``Swing ratios and ensemble timing in jazz performance'', \ \textit{Music Perception} 19 (2002)",
             r"R. Brochard et al., \ ``The `ticktock' of our internal clock'', \ \textit{Psychological Science} 14 (2003)",
             r"M. A. G. Witek et al., \ ``Syncopation, body-movement and pleasure in groove music'', \ \textit{PLoS ONE} 9 (2014)",
             r"N. Jacoby et al., \ ``Commonality and variation in mental representations of music \ldots'', \ \textit{Nature Human Behaviour} 8 (2024)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        keys = VGroup()
        for i in range(14):
            keys.add(Rectangle(width=0.5, height=1.9, stroke_color=GREY_D, stroke_width=1.5, fill_color=WHITE, fill_opacity=0.92).move_to([i * 0.5, 0, 0]))
        for i in (0, 1, 3, 4, 5, 7, 8, 10, 11, 12):
            keys.add(Rectangle(width=0.3, height=1.15, stroke_width=0, fill_color=BLACK, fill_opacity=1.0).move_to([i * 0.5 + 0.25, 0.375, 0]))
        keys.move_to(UP * 1.2)
        q = label(r"seven white keys and five black. \ Why those numbers?", font_size=32, color=EAR).move_to(DOWN * 0.6)
        lead = VGroup(label(r"this part: \ when", font_size=40, color=GREY_A), label(r"next: \ which notes", font_size=44, color=TUNE)).arrange(DOWN, buff=0.5)
        nxt = VGroup(label(r"Part 12", font_size=32, color=GREY_B), label(r"Scales and Modes", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We can now say when. Next we ask which: which notes a piece of music chooses from. "
            "<bookmark mark='a'/> Look at a keyboard. Seven white keys and five black to every octave, "
            "the world over. Why seven, and why five? The answer starts from the same three to two that "
            "ended this part: stack fifths one on another, fold them back into an octave, and at certain "
            "numbers of notes something special happens. <bookmark mark='b'/> Next time. Part 12: Scales "
            "and Modes."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(keys), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
