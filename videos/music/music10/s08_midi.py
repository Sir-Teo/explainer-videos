from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def tune_rows(count: int = 14):
    rows, t = [], 0.0
    for n in TUNE_SCORE.voices[0].notes[:count]:
        b = float(n.dur * 4)
        rows.append((t, b, n.pitch.midi))
        t += b
    return rows


class Midi(SoundScene):
    def construct(self):
        chapter(self, 7, r"Holes and bytes", r"What does a machine need to be told?", lit=(1983,), extra=((1904, r"the reproducing piano"),))
        self.roll()
        self.bytes()
        self.forgets()
        self.pair()

    # ------------------------------------------------------------------
    def roll(self):
        roll = piano_roll(tune_rows(), width=10.5, height=3.2, color=PAGE, grid="#3A3226").move_to(UP * 0.6)
        roll.frame.set_fill("#5A4A36", opacity=0.35)
        bar = Line(roll.frame.get_corner(UL) + UP * 0.15, roll.frame.get_corner(DL) + DOWN * 0.15, color=INK, stroke_width=5)
        lt = label(r"along the paper: \ time", font_size=26, color=TIME).next_to(roll, DOWN, buff=0.25)
        lp = label(r"across it: \ pitch", font_size=26, color=FREQ).rotate(PI / 2).next_to(roll, LEFT, buff=0.25)
        welte = label(r"1904: \ a pianist's performance, \ recorded as holes", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In the eighteen nineties a new kind of reader appeared: the player piano. Its music is a roll "
            "of paper with holes punched in it. Where there is a hole, air rushes through and a key goes "
            "down, and the longer the hole, the longer the note. <bookmark mark='a'/> Time runs along the "
            "paper and pitch runs across it. This is Guido's graph with everything else stripped away: no "
            "staff, no clef, no shapes. The graph itself has become a machine part. <bookmark mark='b'/> "
            "In 1904 the Welte company went one step further and recorded pianists straight onto rolls: "
            "when each key went down, when it came up, and roughly how hard. A roll like that keeps exactly "
            "what a score leaves out, the timing of one real performance. And it keeps nothing else."
        ) as vo:
            self.play(FadeIn(roll.frame), FadeIn(roll.grid))
            self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in roll.notes], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(lp), FadeIn(bar))
            self.play(bar.animate.shift(RIGHT * 10.5), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(welte))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bytes(self):
        d = load("midi")
        data = bytes(d["bytes"])
        rows = byte_row(data, groups=[tuple(g) for g in d["groups"]], per_row=22, font_size=22, step=0.5, row_step=0.5)
        rows.move_to(UP * 2.3)
        for a, b, col in ((d["header"][0], d["track"][1], GREY_D), (d["meta"][0], d["meta"][1], "#8A9BB0")):
            for t in rows.bytes[a:b]:
                t.set_color(col)
        l1 = label(r"dark: \ the file's header", font_size=24, color=GREY_C)
        l2 = label(r"blue-grey: \ tempo, \ metre, \ key", font_size=24, color="#8A9BB0")
        VGroup(l1, l2).arrange(RIGHT, buff=1.0).next_to(rows, DOWN, buff=0.3)
        g0 = rows.groups[0]
        parts = [(0, 1, r"wait 0 ticks"), (1, 4, r"note on: \ key 60 (middle C), \ struck with velocity 80"), (4, 6, r"wait 480 ticks: \ one quarter note"), (6, 9, r"note off: \ key 60")]
        decode = VGroup()
        for a, b, text in parts:
            code = Text(" ".join(f"{x:02X}" for x in data[d["first"] + a: d["first"] + b]), font=MONO, font_size=28, color=INK)
            decode.add(VGroup(code, label(text, font_size=28, color=GREY_A)))
        for r in decode:
            r.arrange(RIGHT, buff=0.5)
        decode.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        for r in decode:
            r[1].align_to(decode[1][1], LEFT).shift(RIGHT * 0.0)
            r[1].set_x(decode[0][0].get_left()[0] + 2.6, direction=LEFT)
        decode.move_to(DOWN * 1.2)
        total = label(rf"nine bytes a note; \ the whole Tune: \ {d['size']} bytes", font_size=28, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1983 the makers of synthesizers agreed on a way for one instrument to tell another what "
            "is being played. They called it MIDI, and it is a piano roll sent down a wire. Here is the "
            "start of the Tune as a MIDI file, byte by byte. <bookmark mark='a'/> First a header, and the "
            "tempo, the metre and the key. Then the notes. <bookmark mark='b'/> A zero: wait no time. "
            "<bookmark mark='c'/> Three bytes: note on, key number sixty, which is middle C, struck with a "
            "velocity of eighty. <bookmark mark='d'/> Two bytes: wait four hundred and eighty ticks, which "
            "this file defines as one quarter note. <bookmark mark='e'/> Three bytes: note off, key sixty. "
            f"<bookmark mark='f'/> Nine bytes for a note, and {say(d['size'])} for the whole Tune. Which "
            "key, when down, when up, how hard. Nothing more."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t) for t in rows.bytes], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(g0.animate.set_color(INK), FadeIn(decode[0]))
            for mark, r in zip("cde", decode[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
            vo.wait_until("f")
            self.play(LaggedStart(*[Indicate(g, color=INK, scale_factor=1.1) for g in rows.groups], lag_ratio=0.4), FadeIn(total), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forgets(self):
        d = load("midi")
        wrote = SC.Score([SC.Voice([SC.Note(P(n), SC.Q) for n in d["written"]])], key=-3, time=(4, 4))
        back = SC.Score([SC.Voice([SC.Note(P(n), SC.Q) for n in d["read_back"]])], key=0, time=(4, 4))
        a = Staff(wrote, width=4.6, space=0.24, show_time=False).move_to(LEFT * 4.1 + UP * 0.6)
        b = Staff(back, width=4.6, space=0.24, show_time=False).move_to(RIGHT * 4.1 + UP * 0.6)
        keys = VGroup(*[Text(str(k), font=MONO, font_size=32, color=INK) for k in d["keys"]]).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        box = SurroundingRectangle(keys, color=GREY_C, buff=0.25, corner_radius=0.1, stroke_width=2)
        tag = label(r"a MIDI file", font_size=24, color=GREY_B).next_to(box, UP, buff=0.12)
        ar1 = Arrow(a.get_right(), box.get_left(), buff=0.15, color=GREY_B, stroke_width=3, tip_length=0.18)
        ar2 = Arrow(box.get_right(), b.get_left(), buff=0.15, color=GREY_B, stroke_width=3, tip_length=0.18)
        la = label(r"written: \ E$\flat$ \ G \ B$\flat$ \ E$\flat$", font_size=28, color=GOOD).next_to(a, DOWN, buff=0.5)
        lb = label(r"read back: \ D$\sharp$ \ G \ A$\sharp$ \ D$\sharp$", font_size=28, color=BAD).next_to(b, DOWN, buff=0.5)
        with self.voiceover(
            "So what does a key number forget? Monochord wrote these four notes into a MIDI file: E flat, "
            "G, B flat, E flat. <bookmark mark='a'/> The file holds four key numbers. <bookmark mark='b'/> "
            "And when Monochord reads the file back, it gets D sharp, G, A sharp, D sharp. The same four "
            "keys of the piano. Not the same notes on the page. A reader has to guess the spelling, and a "
            "file of key numbers gives it nothing to go on, any more than a piano keyboard does."
        ) as vo:
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(GrowArrow(ar1), FadeIn(box), FadeIn(tag), LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(GrowArrow(ar2), FadeIn(b), FadeIn(lb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pair(self):
        d = load("midi")
        c = clip("midi.pair")
        card = listen_card(r"Two notes, \ X and Y. \ On a piano they are the same key. \ Are they the same note?", width=9.4)
        with self.voiceover("Does the spelling matter? Listen. Two notes, X and Y. On a piano they are the same key. Are they the same note?"):
            self.play(FadeIn(card))
        self.wait(1.0)
        bx = boxes(("X", "Y", r"E with X", r"E with Y"), buff=0.5, width=2.6, height=1.1, font_size=34).move_to(UP * 1.7)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"X, \ Y, \ X, \ Y; \ then each with the note E", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for ev, k in (("x1", 0), ("y1", 1), ("x2", 0), ("y2", 1)):
                pulse(snd, bx[k], snd.time_of(ev), snd.time_of(ev) + 1.1)
            pulse(snd, bx[2], snd.time_of("third"), snd.time_of("third") + 2.2)
            pulse(snd, bx[3], snd.time_of("wolf"), snd.time_of("wolf") + 2.2)
            for ev, k in (("x1", 0), ("y1", 1), ("x2", 0), ("y2", 1), ("third", 2), ("wolf", 3)):
                snd.wait_until(ev)
                self.play(bx[k].animate(rate_func=there_and_back).shift(UP * 0.12), run_time=0.35)
        g = axes([400, 425], [0, 1], x_length=10.0, y_length=0.6, xlabel=r"hertz", ylabel="", xticks=[400, 405, 410, 415, 420, 425], yticks=[], font_size=22).move_to(DOWN * 2.0)
        marks = VGroup()
        for hz, name, col, up in ((d["g_sharp"], r"X: \ G$\sharp$", GOOD, 1.0), (d["equal"], r"the piano's key", GREY_B, 1.9), (d["a_flat"], r"Y: \ A$\flat$", BAD, 1.0)):
            p = g.ax.c2p(hz, 0)
            marks.add(VGroup(Line(p, p + UP * up, color=col, stroke_width=5), label(name + rf" \ {hz:.1f}", font_size=24, color=col).next_to(p + UP * up, UP, buff=0.08)))
        with self.voiceover(
            f"They are not the same. Y is higher than X by {say(d['diesis_cents'])} cents, about a fifth of "
            "a tone. <bookmark mark='a'/> X is G sharp: a pure major third above E, with the frequencies "
            "five to four from Part 5. Y is A flat: a pure major third below the C above. With E, the G "
            "sharp is calm. With E, the A flat is the wolf we met in Part 6, when we tuned an organ in "
            "meantone. <bookmark mark='b'/> The piano's one key sits between the two and is neither. A "
            "singer or a violinist who reads G sharp on a staff knows which one the composer meant, and "
            "tunes it. A machine that reads key number sixty-eight does not."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(marks[0]), FadeIn(marks[2]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
        self.wait(0.4)
        self.clear_scene()
