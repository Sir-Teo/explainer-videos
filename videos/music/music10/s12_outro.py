from __future__ import annotations

import numpy as np

from explainer.music.monochord.score import codes, tab, write
from videos.music.music10.common import *  # noqa: F403
from videos.music.variations import rows_before

PAIRS = [("neumes", "guido"), ("mensural", "tab"), ("gongche", "jianpu"), ("staff", "roll"), ("midi", "mei")]
TITLES = {"neumes": r"neumes, \ c. 900", "guido": r"Guido's staff, \ c. 1025", "mensural": r"mensural notes, \ c. 1300", "tab": r"tablature, \ c. 1500",
          "gongche": r"gongche", "jianpu": r"jianpu", "staff": r"the staff", "roll": r"a piano roll, \ c. 1900", "midi": r"MIDI, \ 1983", "mei": r"MEI, \ 2000s"}


def notation(kind: str, k: int):
    """Phrase ``k`` of the Tune in one notation: the drawing, and the marks to light note by note."""
    sc = phrase_score(k)
    notes = sc.voices[0].notes
    steps = steps_of(notes)
    beats = [int(n.dur * 4) for n in notes]
    keys = [n.pitch.midi for n in notes]
    if kind == "neumes":
        m = neumes(steps, width=5.0, size=0.6)
        return m, m.notes
    if kind == "guido":
        m = square_staff(steps, width=5.2, space=0.42)
        return m, m.notes
    if kind == "mensural":
        m = mensural("SSSSSSB", steps, width=5.4, space=0.36, perfect=False)
        return m, [n.body for n in m.notes]
    if kind == "tab":
        m = tablature(tab.fingering(keys)["positions"], width=5.2, space=0.32, font_size=28)
        return m, [n.mark for n in m.notes]
    if kind == "gongche":
        m = gongche(codes.gongche(sc, tonic=P("C4")), beats=beats, height=2.4, font_size=30)
        return m, [n[0] for n in m.notes]
    if kind == "jianpu":
        m = jianpu([s + 1 for s in steps], beats, width=5.2, font_size=38, key=None)
        return m, [n[0] for n in m.notes]
    if kind == "staff":
        m = Staff(sc, width=5.4, space=0.19, show_time=False)
        return m, [n.ink for n in m.notes]
    if kind == "roll":
        rows, t = [], 0.0
        for key, b in zip(keys, beats):
            rows.append((t, b, key))
            t += b
        m = piano_roll(rows, width=5.2, height=2.2, lo=59, hi=70, color=PAGE)
        return m, m.notes
    if kind == "midi":
        data = write.midi(sc)
        first = data.index(bytes([0x90])) - 1
        m = byte_row(data[first: first + 63], groups=[(9 * j, 9 * j + 9) for j in range(7)], per_row=9, font_size=18, step=0.42, row_step=0.33, color=WHITE)
        return m, m.groups
    if kind == "mei":
        durs = {1: "4", 2: "2"}
        text = "\n".join(f'<note pname="{n.pitch.step.lower()}" oct="{n.pitch.octave}" dur="{durs[b]}"/>' for n, b in zip(notes, beats))
        m = code_block(text, font_size=18, line_step=0.33)
        return m, m.rows
    raise KeyError(kind)


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
        c = clip("tune.variation10")
        head = VGroup(label(r"Variation 10", font_size=48, color=TUNE), label(r"one tune, \ ten notations", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.35)
        screens = []
        for k, (a, b) in enumerate(PAIRS):
            ma, la_ = notation(a, k)
            mb, lb_ = notation(b, k)
            pa = panel(ma, TITLES[a], width=6.3, height=3.9).move_to(LEFT * 3.3 + DOWN * 0.1)
            pb = panel(mb, TITLES[b], width=6.3, height=3.9).move_to(RIGHT * 3.3 + DOWN * 0.1)
            screens.append((VGroup(pa, pb), la_, lb_))
        last = Staff(phrase_score(5), width=9.0, space=0.26, show_time=False).move_to(UP * 1.0)
        xs = [n.head.get_x() for n in last.notes]
        y_ms, y_db = -1.0, -2.4
        base_ms = Line([xs[0] - 0.5, y_ms, 0], [xs[-1] + 0.5, y_ms, 0], color=GREY_C, stroke_width=1.5)
        base_db = Line([xs[0] - 0.5, y_db, 0], [xs[-1] + 0.5, y_db, 0], color=GREY_C, stroke_width=1.5)
        ms_bars = [Rectangle(width=0.36, height=max(abs(m) * 0.012, 0.03), stroke_width=0, fill_color=TIME, fill_opacity=0.9).move_to([x, y_ms + m * 0.006, 0]) for x, m in zip(xs, d["late_ms"])]
        db_bars = [Rectangle(width=0.36, height=max(abs(m) * 0.16, 0.03), stroke_width=0, fill_color=LEVEL, fill_opacity=0.9).move_to([x, y_db + m * 0.08, 0]) for x, m in zip(xs, d["db"])]
        l_ms = label(r"late or early", font_size=22, color=TIME).next_to(base_ms, LEFT, buff=0.15)
        l_db = label(r"louder or softer", font_size=22, color=LEVEL).next_to(base_db, LEFT, buff=0.15)
        none = label(r"what none of them says", font_size=30, color=EAR).next_to(last, UP, buff=0.35)
        final = VGroup(last, base_ms, base_db, l_ms, l_db, none)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built ways of "
            "writing. <bookmark mark='a'/> So here is the Tune played off the page, exactly as written, "
            "while the page changes: each phrase in two notations, from the neumes of the ninth century to "
            "the files of this one. Five phrases, ten notations. And then the sixth phrase, played the way "
            "none of the ten can say."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(screens[0][0]))
        ev = c.events
        shown = screens[0][0]
        with self.listen(c) as snd:
            window(snd, r"Variation 10", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(6):
                snd.wait_until(f"phrase{k}")
                self.remove(shown)
                end = ev[f"phrase{k + 1}"] if k < 5 else c.duration
                ts = [ev[f"n{7 * k + j}"] for j in range(7)]
                if k < 5:
                    shown, la_, lb_ = screens[k]
                    self.add(shown)
                    light(snd, la_, ts, end=end, base=PARCHMENT if PAIRS[k][0] == "neumes" else WHITE)
                    light(snd, lb_, ts, end=end)
                    for j, t in enumerate(ts):
                        snd.wait_until(t)
                        self.play(la_[j].animate(rate_func=there_and_back).scale(1.25), lb_[j].animate(rate_func=there_and_back).scale(1.25), run_time=0.2)
                else:
                    shown = final
                    self.add(shown)
                    light(snd, [n.ink for n in last.notes], ts, end=end)
                    for j, t in enumerate(ts):
                        snd.wait_until(t)
                        self.play(FadeIn(ms_bars[j], scale=0.5), FadeIn(db_bars[j], scale=0.5), run_time=0.25)
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row ten of the ledger. {say(v['seconds'])} seconds. The measurement is this part's count: the "
            f"page of the Tune is {say(d['plain_bits'])} bits, and its sound is about "
            f"{say(round(d['ratio'], -3) / 1000)} thousand times as many."
        ):
            self.play(FadeOut(final), *[FadeOut(b) for b in ms_bars + db_bars], FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        n, t, f, m, b = load("neumes"), load("tab"), load("figured"), load("midi"), load("bits")
        card = objectives_card([
            rf"neumes record which way a melody goes: \ {n['counts']['6']} melodies fit one phrase's signs",
            r"Guido's staff is a graph of pitch against time, \ counted in steps of a scale",
            r"shapes gave notes their lengths; \ dots and ties write any $k/2^n$; \ bar lines align the voices",
            r"tablature and figured bass write actions: \ $2 \times 10^{19}$ fingerings, \ six million realizations",
            rf"MIDI keeps the key and forgets the spelling: \ G$\sharp$ and A$\flat$ are {m['diesis_cents']:.0f} cents apart",
            rf"the page is {b['plain_bits']} bits, \ the sound " + r"{:,.0f}".format(round(b["ratio"], -3)).replace(",", "{,}") + r" times more: \ the player supplies the rest",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Neumes record which way a melody goes, and never how far: dozens of "
            "melodies fit the same signs. <bookmark mark='a'/> Guido's staff is a graph of pitch against "
            "time, counted in steps of a scale that the reader must already know. <bookmark mark='b'/> "
            "Shapes gave notes their lengths; dots and ties write any length that halvings can reach; and "
            "bar lines let many people read together. <bookmark mark='c'/> Tablature and figured bass "
            "write actions instead of sounds, and each stands for millions of choices. "
            "<bookmark mark='d'/> A MIDI file keeps the key and the moment, and forgets the spelling, "
            "which can be a fifth of a tone. <bookmark mark='e'/> And the page of a tune is a few hundred "
            "bits, against millions for its sound. The player supplies the rest."
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
            r"How many melodies on the seven notes C to B have the contour up, \ up, \ down, \ down, \ up? \ "
            r"Count them with a table: \ for each note, \ the number of ways to finish the melody from there.",
            r"Show that a note with $n$ dots lasts $2 - 2^{-n}$ times its plain length, \ and that any length $k/2^m$ of a whole note can be written "
            r"with no more tied notes than there are ones in the binary expansion of $k$.",
            r"\textbf{Ear.} \ The lab plays six pairs of notes in quarter-comma meantone. \ For each pair, \ say whether you heard a sharp and the flat next to it, \ "
            r"41 cents apart, \ or the same note twice.",
            r"\textbf{Build.} \ With \texttt{score.tab}, \ change the cost of a move so that open strings are avoided, \ and find the best fingering of the Tune. \ "
            r"How many frets does the hand now span, \ and how many tablatures did you rule out?",
            r"$\bigstar$ \ Design a notation for the Tune that also keeps the four rules of performance from chapter 9, \ in fewer than 300 bits in all. \ "
            r"What must its reader already know? \ Is your notation descriptive or prescriptive?",
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
            (r"note values, \ metre and the bar", [11]),
            (r"key signatures, \ and why notes are spelled", [12, 15]),
            (r"figured bass becomes harmony", [17, 18]),
            (r"neumes and mensural notes in their own centuries", [23, 24]),
            (r"what a performer adds to the page", [43]),
            (r"MIDI, \ sequencers, \ and turning sound back into notes", [53, 61]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? At once: the next part is about rhythm, and its note values and "
            "bars are the ones we met today. Key signatures and the spelling of notes return with scales "
            "and keys. The figures under a bass line grow into the theory of harmony. Neumes and mensural "
            "notes return in the centuries that used them. What a performer adds to the page gets a part "
            "of its own. And MIDI comes back with the sequencer, and again when we ask a machine to turn "
            "sound into notes."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"engravers", r"give long notes more room than short ones, \ but less than in proportion; \ a page spaced by the clock is hard to read"),
            (r"session players", r"read chord charts and number charts at sight: \ figured bass under another name"),
            (r"editors", r"compare every source, \ and mark in the score which notes are their own guesses"),
            (r"programmers", r"keep spelled pitches and exact fractions inside; \ turn them into key numbers and seconds only on the way out"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. An engraver gives a long note more room than a short one, but much less "
            "than in proportion, because a page spaced by the clock is hard to read. A session player "
            "reads a chart of chord symbols at sight, which is figured bass under another name. An editor "
            "compares every source and marks which notes are guesses. And a programmer who writes music "
            "software keeps spelled pitches and exact fractions inside the program, as Monochord does, and "
            "turns them into key numbers and seconds only on the way out."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"T. F. Kelly, \ \textit{Capturing Music: The Story of Notation} \ (2015)",
             r"E. Gould, \ \textit{Behind Bars: The Definitive Guide to Music Notation} \ (2011)",
             r"E. Selfridge-Field (ed.), \ \textit{Beyond MIDI: The Handbook of Musical Codes} \ (1997)",
             r"W. Apel, \ \textit{The Notation of Polyphonic Music, 900--1600} \ (5th ed., 1953)"],
            [r"A. D. Kilmer, \ ``The cult song with music from ancient Ugarit'', \ \textit{Revue d'Assyriologie} 68 (1974)",
             r"M. L. West, \ ``The Babylonian musical notation and the Hurrian melodic texts'', \ \textit{Music \& Letters} 75 (1994)",
             r"C. Seeger, \ ``Prescriptive and descriptive music-writing'', \ \textit{The Musical Quarterly} 44 (1958)",
             r"N. P. McA. Todd, \ ``The dynamics of dynamics: a model of musical expression'', \ \textit{JASA} 91 (1992)",
             r"A. Friberg and J. Sundberg, \ ``Does music performance allude to locomotion?'', \ \textit{JASA} 105 (1999)",
             r"M. Good, \ ``MusicXML for notation and analysis'', \ in \textit{The Virtual Score} (2001)",
             r"J. Calvo-Zaragoza, J. Haji\v{c} jr. and A. Pacha, \ ``Understanding optical music recognition'', \ \textit{ACM Computing Surveys} 53 (2020)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        clicks = VGroup(*[Dot(radius=0.13, color=GREY_A) for _ in range(12)]).arrange(RIGHT, buff=0.55).move_to(UP * 1.4)
        q = label(r"twelve identical clicks. \ Why do we hear them in twos?", font_size=32, color=EAR).move_to(DOWN * 0.1)
        nxt = VGroup(label(r"Part 11", font_size=32, color=GREY_B), label(r"Rhythm and Meter", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        two = SC.Score([SC.Voice([SC.Note(P("G4"), SC.H), SC.Note(P("G4"), SC.Q), SC.Note(P("G4"), SC.Q)])], time=(4, 4))
        st = Staff(two, width=5.0, space=0.24, show_time=False).move_to(UP * 2.0)
        ratio = label(r"on the page, \ a length is a ratio: \ this note is twice that one", font_size=28, color=GREY_A).next_to(st, DOWN, buff=0.4)
        clicks.move_to(DOWN * 0.2)
        q.move_to(DOWN * 1.3)
        with self.voiceover(
            "We can now write down which note, and for how long. But a length on a page is only a ratio: "
            "this note is twice that one. What makes a row of lengths into a rhythm? <bookmark mark='a'/> "
            "Play a row of clicks, every one identical, and listeners hear them in pairs: tick, tock, tick, "
            "tock. Nothing in the sound says so. The grouping is something the listener adds. "
            "<bookmark mark='b'/> Next time: where the beat comes from, how bars and meters organize it, "
            "and what happens when a rhythm is played so fast that it turns into a pitch. Part 11: Rhythm "
            "and Meter."
        ) as vo:
            self.play(FadeIn(st), FadeIn(ratio))
            vo.wait_until("a")
            self.play(st.animate.set_opacity(0.35), ratio.animate.set_opacity(0.35), LaggedStart(*[FadeIn(cl, scale=1.8) for cl in clicks], lag_ratio=0.3), run_time=3.5)
            self.play(*[cl.animate.scale(1.5).set_color(TUNE) for cl in clicks[::2]], FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
