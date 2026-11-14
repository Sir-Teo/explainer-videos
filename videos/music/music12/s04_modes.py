from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403

WHITE_CHAIN = ["F", "C", "G", "D", "A", "E", "B"]
TEX = {"♭": r"$\flat$", "♯": r"$\sharp$"}


def tex(name: str) -> str:
    for k, v in TEX.items():
        name = name.replace(k, v)
    return name


def mode_table(rows, font_size: int = 28, step: float = 0.56) -> VGroup:
    """The seven modes on C, one to a row: name, then its seven notes; the note that changed from the row above is red."""
    g = VGroup()
    g.rows = []
    prev = None
    for i, r in enumerate(rows):
        nm = label(r["name"], font_size=font_size, color=TUNE).move_to([-4.4, -i * step, 0], aligned_edge=LEFT)
        notes = VGroup()
        for k, n in enumerate(r["names"]):
            changed = prev is not None and prev[k] != n
            notes.add(label(tex(n), font_size=font_size, color=BAD if changed else WHITE).move_to([-1.6 + k * 0.95, -i * step, 0]))
        row = VGroup(nm, notes)
        g.add(row)
        g.rows.append(row)
        prev = r["names"]
    return g


class Modes(SoundScene):
    def construct(self):
        chapter(self, 3, r"Seven notes, \ seven modes", r"Which of the seven is home?", extra=((1547, r"Glarean names twelve modes"),))
        self.chain_view()
        self.on_c()
        self.quiz()
        self.degrees()
        self.relative()
        self.the_tune()

    # ------------------------------------------------------------------
    def chain_view(self):
        d = load("modes")
        ch = chain(WHITE_CHAIN, lit=range(7), gap=1.3, font_size=40).move_to(UP * 1.6)
        ch.shift(LEFT * ch.get_center()[0])
        order = [r["name"] for r in d["rows"]]
        tags = VGroup(*[label(nm, font_size=24, color=GREY_A).next_to(cell, DOWN, buff=0.45) for nm, cell in zip(order, ch.cells)])
        arrow = Arrow(tags.get_left() + DOWN * 0.6, tags.get_right() + DOWN * 0.6, buff=0, color=GREY_B, stroke_width=3, tip_length=0.18)
        ends = VGroup(label(r"brightest", font_size=24, color=TUNE).next_to(arrow, LEFT, buff=0.15), label(r"darkest", font_size=24, color=GREY_B).next_to(arrow, RIGHT, buff=0.15))
        with self.voiceover(
            "Seven notes are not yet a scale. A scale needs a home: one note that the others are heard "
            "against, where a tune comes to rest. Here are our seven notes as the stack made them, each a "
            "fifth above the last. <bookmark mark='a'/> Any of the seven can be home, and each choice is "
            "called a mode. The names are Greek, borrowed and misapplied by medieval theorists; the full "
            "set dates from 1547. <bookmark mark='b'/> What matters is the order. Make F the home note, "
            "and every other note lies above it in the chain of fifths: that is the brightest mode, "
            "Lydian. Make B the home note, and every other note lies below it: Locrian, the darkest. "
            "Between them the other five line up in order."
        ) as vo:
            self.play(FadeIn(ch))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(ends))
            self.play(Indicate(ch.cells[0], color=TUNE), Indicate(tags[0], color=TUNE))
            self.wait(3.0)
            self.play(Indicate(ch.cells[6], color=WHITE), Indicate(tags[6], color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def on_c(self):
        d = load("modes")
        c = clip("modes.seven")
        tb = mode_table(d["rows"]).move_to(UP * 0.5)
        head = label(r"all seven with the same home note, \ C", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        note = listen_note(r"seven scales on C, \ over a held C. \ Each has one note a semitone lower than the scale before", width=10.4, font_size=26).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "To compare them fairly, give all seven the same home note, C. <bookmark mark='a'/> Lydian is "
            "a major scale with its fourth note raised. Lower that note by a semitone and you have "
            "the major scale itself, which as a mode is called Ionian. <bookmark mark='b'/> Lower one more "
            "note, the seventh, and it is Mixolydian. And so on down the table: each mode is the one "
            "above it with a single note lowered by a semitone, shown in red. Listen to all seven, over "
            "a held C."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tb.rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(tb.rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb.rows[2:]], lag_ratio=0.35), FadeIn(note), run_time=4.0)
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"the seven modes, \ bright to dark", detail=r"Part 7's piano over a held C", corner=DL, tag_corner=DR)
            for k, row in enumerate(tb.rows):
                t0 = d["starts"][k]
                pulse(snd, row[0], t0, t0 + 3.0, buff=0.08)
                ts = d["note_times"][k]
                flash(snd, [row[1][j % 7] for j in range(8)], ts, base=WHITE, hot=TUNE, fade=0.2)
        for row in tb.rows:
            for m in row[1]:
                m.set_color(WHITE)
        with self.voiceover(
            "Bright to dark in six steps. The top three have a major third above the home note, and "
            "sound major. The next three have a minor third, and sound minor; the fifth of them, "
            "Aeolian, is the natural minor scale. The last, Locrian, has no perfect fifth above its home "
            "note, and almost no music is written in it."
        ):
            self.play(Indicate(VGroup(*[r[1][2] for r in tb.rows[:3]]), color=TUNE), run_time=1.5)
            self.play(Indicate(VGroup(*[r[1][2] for r in tb.rows[3:6]]), color=SHORT), run_time=1.5)
            self.play(Indicate(tb.rows[6][1][4], color=BAD), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("modes")
        c = clip("modes.quiz")
        card = listen_card(r"Two modes on the same note. \ Which is the brighter: \ A or B?", width=8.6)
        with self.voiceover("Try your ear on it. Two modes, on the same home note. Which is the brighter: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano over a held C", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 0.9)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
        ans = VGroup(label(r"A: \ Dorian \ (minor third, \ minor seventh)", font_size=28, color=GREY_A), label(r"B: \ Mixolydian \ (major third, \ minor seventh)", font_size=28, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "B. It was Mixolydian, and A was Dorian. They are neighbours in the table, and they differ "
            "in one note only: the third. That one semitone is the difference between major and minor."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def degrees(self):
        d = load("modes")
        st = scale_staff([0, 2, 4, 5, 7, 9, 11], width=8.6, space=0.22).move_to(UP * 1.7)
        nums = VGroup(*[label(str(k + 1), font_size=32, color=TUNE).move_to([n.head.get_x(), st.get_bottom()[1] - 0.35, 0]) for k, n in enumerate(st.notes)])
        names = VGroup(*[label(nm, font_size=22, color=GREY_A).move_to([n.head.get_x(), st.get_bottom()[1] - (0.85 if k % 2 == 0 else 1.25), 0]) for k, (nm, n) in enumerate(zip(d["degree_names"], st.notes))])
        rows = VGroup(*[VGroup(label(nm, font_size=28, color=TUNE), label(r" \ \ ".join(tex(x) for x in d["formulas"][nm]), font_size=30, color=WHITE)) for nm in ("Lydian", "Mixolydian", "Dorian", "Phrygian")])
        for r in rows:
            r.arrange(RIGHT, buff=0.7)
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        x1 = max(r[0].get_right()[0] for r in rows) + 0.7
        for r in rows:
            r[1].align_to(np.array([x1, 0, 0]), LEFT)
        rows.move_to(DOWN * 2.2)
        with self.voiceover(
            "Musicians need to talk about the notes of a scale without saying which key they are in, so "
            "the seven places have numbers, and names. <bookmark mark='a'/> One is the tonic, the home "
            "note. Five is the dominant, a fifth above it; four, the subdominant, a fifth below. Three "
            "is the mediant, halfway between tonic and dominant. And seven, when it lies a semitone "
            "under the tonic, is the leading note; we will hear why shortly. <bookmark mark='b'/> With "
            "numbers, a mode is a short formula: the major scale with some places lowered or raised. "
            "Lydian is major with a sharp four. Mixolydian, major with a flat seven. Dorian, flat three "
            "and flat seven. A jazz player reads those formulas the way you read a word."
        ) as vo:
            self.play(FadeIn(st), FadeIn(nums))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in (names[0], names[4], names[3], names[2], names[6], names[1], names[5])], lag_ratio=0.5), run_time=7.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), run_time=5.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        d = load("modes")
        c = clip("modes.relative")
        kb = keyboard(-3, 21, width=10.4, height=1.9).move_to(UP * 1.1)
        rows = VGroup(label(r"C major: \ home on C", font_size=30, color=TUNE), label(r"A minor: \ the same seven notes, \ home on A", font_size=30, color=SHORT),
                      label(r"relatives: \ same notes, \ different home. \ \ Parallels: \ same home, \ different notes", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "There are two ways to compare a major scale with a minor one, and the difference matters. "
            "We compared C major with the darker modes on C: the same home, different notes. Those are "
            "parallel scales. But the white keys also contain a minor scale: start on A. Same seven "
            "notes, different home. C major and A minor are called relatives. Listen: the notes of C "
            "major from C; the same notes from A; and then the two home chords."
        ):
            self.play(FadeIn(kb), FadeIn(rows[0]), FadeIn(rows[1]))
        with self.listen(c) as snd:
            window(snd, r"C major; \ A minor; \ their home chords", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            s = d["relative_starts"]
            play_keys(snd, kb, [0, 2, 4, 5, 7, 9, 11, 12] + [-3, -1, 0, 2, 4, 5, 7, 9] + [0, 4, 7] + [-3, 0, 4],
                      [s[0] + 0.3 * k for k in range(8)] + [s[1] + 0.3 * k for k in range(8)] + [s[2]] * 3 + [s[2] + 1.2] * 3, hold=0.3)
            pulse(snd, rows[0], s[0], s[0] + 2.9, buff=0.08)
            pulse(snd, rows[1], s[1], s[1] + 2.9, buff=0.08)
            snd.drive(rows[0], lambda m, t: m.set_opacity(1.0))
        kb.clear()
        with self.voiceover(
            "Nothing changed but where the music came to rest. That is what a mode is: not a set of "
            "notes, but a set of notes and a decision about which of them is home. Every major key has "
            "a relative minor a minor third below it, and a piece can pass from one to the other "
            "without changing a single note."
        ):
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def the_tune(self):
        d = load("modes")
        rows = VGroup()
        for r in d["rows"]:
            ch = d["tune_changed"][r["name"]]
            text = r"the same tune" if not ch else (r"changes degree " + ", ".join(str(x) for x in ch))
            rows.add(VGroup(label(r["name"], font_size=28, color=TUNE), label(text, font_size=28, color=GOOD if not ch else GREY_A)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.6)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        x1 = max(r[0].get_right()[0] for r in rows) + 0.8
        for r in rows:
            r[1].align_to(np.array([x1, 0, 0]), LEFT)
        rows.move_to(DOWN * 0.4)
        head = label(r"the Tune uses only six notes of its scale: \ degrees 1 to 6", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "What do the modes do to our Tune? Less than you might expect, and the reason is worth "
            "noticing. The Tune uses only six notes of its scale; it never touches the seventh. "
            "<bookmark mark='a'/> So in the Mixolydian mode, which differs from major only in the "
            "seventh, the Tune does not change at all. A melody of six notes cannot tell those two modes "
            "apart. Guido's hexachord, from Part 10, had the same blind spot, and it is why his singers "
            "needed more than one of them. When we play the Tune in every mode, at the end of this part, "
            "we will give it a second voice that does use the seventh."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.2), run_time=2.5)
            self.play(Indicate(rows[1], color=GOOD), Indicate(rows[2], color=GOOD))
        self.wait(0.4)
        self.clear_scene()
