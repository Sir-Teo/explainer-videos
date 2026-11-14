from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403

FIG_COL = "#7DD3FC"


def fretboard(spots, frets: int = 12, width: float = 11.0, height: float = 2.2) -> VGroup:
    """A guitar's neck seen from the front: six strings, the lowest at the bottom, and dots where a note lives."""
    g = VGroup()
    dy = height / 5
    xs = [width * (1 - 2 ** (-k / 12)) / (1 - 2 ** (-frets / 12)) for k in range(frets + 1)]       # frets get closer together
    for s in range(6):
        g.add(Line([0, s * dy, 0], [width, s * dy, 0], color=STR, stroke_width=3.2 - 0.35 * s))
    for k, x in enumerate(xs):
        g.add(Line([x, 0, 0], [x, height, 0], color=GREY_C, stroke_width=5 if k == 0 else 1.6))
    for k in (3, 5, 7, 9, 12):
        g.add(label(str(k), font_size=26, color=GREY_B).move_to([(xs[k - 1] + xs[k]) / 2, -0.35, 0]))
    g.dots = VGroup()
    for s, f in spots:
        x = (xs[f - 1] + xs[f]) / 2 if f else -0.2
        g.dots.add(Dot([x, s * dy, 0], radius=0.14, color=INK))
    g.add(g.dots)
    return g


class Tab(SoundScene):
    def construct(self):
        chapter(self, 5, r"What to do", r"Why write the action instead of the sound?", extra=((1507, r"printed lute tablature"), (1600, r"figured bass")))
        self.tab()
        self.choices()
        self.figures()
        self.twice()

    # ------------------------------------------------------------------
    def tab(self):
        d = load("tab")
        c = clip("tab.phrase")
        st = Staff(phrase_score(0, 4), width=11.6, space=0.18, show_time=False).move_to(UP * 2.0)
        tb = tablature([tuple(p) for p in d["best"]], width=11.6, space=0.36, names=d["strings"], font_size=30).move_to(DOWN * 0.9)
        for n, s in zip(tb.notes, st.notes):
            n.set_x(s.head.get_x())
        cap = label(r"six strings; \ a number is a fret; \ 0 is the open string", font_size=26, color=GREY_A).next_to(tb, DOWN, buff=0.35)
        self.st, self.tb = st, tb
        with self.voiceover(
            "A staff tells you what you will hear. There is another idea entirely: write down what to do. "
            "This is tablature. <bookmark mark='a'/> There are six lines, but they are not Guido's lines. "
            "They are the six strings of a guitar, the lowest at the bottom. A number on a line tells you "
            "which fret to press on that string, and zero is the open string. <bookmark mark='b'/> Lute "
            "players wrote like this from the fourteen hundreds; the first printed books of lute music, in "
            "1507, are in tablature; guitarists read it every day. In 1958 Charles Seeger gave the two "
            "kinds of writing their names. The staff is descriptive: it describes a sound. Tablature is "
            "prescriptive: it prescribes an action."
        ) as vo:
            self.play(FadeIn(st))
            vo.wait_until("a")
            self.play(FadeIn(tb.lines), FadeIn(tb.names), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(n) for n in tb.notes], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(cap))
        with self.listen(c) as snd:
            window(snd, r"the Tune from tablature", detail=r"Part 7's guitar", corner=DL, tag_corner=DR)
            ts = [snd.time_of(f"n{k}") for k in range(14)]
            light(snd, [n.ink for n in st.notes], ts, end=c.duration)
            light(snd, [n.mark for n in tb.notes], ts, end=c.duration)
            for k, t in enumerate(ts):
                snd.wait_until(t)
                self.play(tb.notes[k].animate(rate_func=there_and_back).scale(1.35), run_time=0.22)
        self.wait(0.2)

    # ------------------------------------------------------------------
    def choices(self):
        d = load("tab")
        st, tb = self.st, self.tb
        fb = fretboard([tuple(p) for p in d["middle_c"]]).move_to(DOWN * 1.3)
        fb.shift(LEFT * fb.get_center()[0])
        head = label(r"middle C on a guitar: \ three places", font_size=30, color=INK).next_to(fb, UP, buff=0.35)
        with self.voiceover(
            "Why would anyone want that? Because on a guitar the staff leaves a question open. Take the "
            "first note, middle C. <bookmark mark='a'/> It is on the second string at the first fret. It "
            "is also on the third string at the fifth fret, and on the fourth string at the tenth. One "
            "note on the staff, three places for the hand, and three slightly different sounds, as Part 7 "
            "would tell you."
        ) as vo:
            self.play(FadeOut(tb))
            vo.wait_until("a")
            self.play(FadeIn(fb), FadeIn(head))
            self.play(LaggedStart(*[Flash(dt, color=INK, flash_radius=0.3) for dt in fb.dots[::-1]], lag_ratio=0.8), run_time=4.0)
        self.wait(0.3)
        self.play(FadeOut(fb), FadeOut(head), FadeOut(st))
        best = tablature([tuple(p) for p in d["best"]], width=10.4, space=0.26, names=d["strings"], font_size=24)
        one = tablature([tuple(p) for p in d["one_string"]], width=10.4, space=0.26, names=d["strings"], font_size=24)
        g = VGroup(best, one).arrange(DOWN, buff=1.0).move_to(DOWN * 0.9 + RIGHT * 0.3)
        lb = label(rf"the least movement: \ effort {d['cost_best']:.0f}", font_size=26, color=GOOD).next_to(best, UP, buff=0.15)
        lo = label(rf"all on one string: \ effort {d['cost_one']:.0f}", font_size=26, color=BAD).next_to(one, UP, buff=0.15)
        count = VGroup(label(r"tablatures of these fourteen notes:", font_size=28, color=GREY_A), label(r"{:,}".format(d["count_phrases"]).replace(",", "{,}"), font_size=40, color=TUNE)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        whole = label(r"of the whole Tune: \ about $2 \times 10^{19}$", font_size=28, color=GREY_A).next_to(count, DOWN, buff=0.2)
        with self.voiceover(
            "So one page of staff notation stands for many tablatures. For the fourteen notes of these two "
            "phrases, Monochord counts more than two million. <bookmark mark='a'/> For the whole Tune, "
            "about twenty billion billion. <bookmark mark='b'/> It picks one by dynamic programming: for "
            "every note, and every place that note could be played, it keeps only the cheapest way of "
            "arriving there, where cheap means that the hand travels little along the neck. "
            "<bookmark mark='c'/> The winner never leaves the first five frets. Playing the same notes "
            "along one string costs twice the effort. A tablature records that choice, which is why "
            "players like it. <bookmark mark='d'/> And what does it throw away? The notes. You cannot see "
            "the shape of the melody in those numbers, and you cannot play them on a flute."
        ) as vo:
            self.play(FadeIn(count))
            vo.wait_until("a")
            self.play(FadeIn(whole))
            vo.wait_until("b")
            self.play(FadeIn(best), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(one), FadeIn(lo))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[n.mark for n in best.notes]), color=INK, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bass_staff(self, width=11.6, y=-2.0):
        d = load("figured")
        low = SC.Score([SC.Voice([SC.Note(P(b), SC.H) for b in d["bass"]], clef="bass")], time=(4, 4))
        st = Staff(low, width=width, space=0.2, show_time=False, proportional=True, lead=1.6).move_to(UP * y)
        figs = VGroup(*[Text(f or " ", font="FreeSerif", font_size=30, color=FIG_COL, weight="BOLD").move_to([n.head.get_x(), st.get_bottom()[1] - 0.3, 0]) for n, f in zip(st.notes, d["figures"])])
        return st, figs

    def figures(self):
        d = load("figured")
        st, figs = self.bass_staff(y=0.6)
        rules = VGroup(
            VGroup(label(r"no figure", font_size=32, color=FIG_COL), label(r"the third and the fifth above the bass", font_size=32, color=GREY_A)),
            VGroup(label(r"6", font_size=36, color=FIG_COL), label(r"the third and the sixth", font_size=32, color=GREY_A)),
            VGroup(label(r"7", font_size=36, color=FIG_COL), label(r"the third, \ the fifth and the seventh", font_size=32, color=GREY_A)),
        )
        for r in rules:
            r.arrange(RIGHT, buff=0.5)
        rules.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 2.2)
        for r in rules:
            r[1].align_to(rules[0][1], LEFT)
        rules.set_x(0)
        head = label(r"a bass line, \ and a few figures: \ about 1600", font_size=30, color=TUNE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Around 1600, in Italy, musicians invented another way of writing what to do, for the player "
            "who accompanies a singer. Write only the bass line, and under some of its notes a small "
            "figure. <bookmark mark='a'/> No figure means: play the third and the fifth above this bass "
            "note. <bookmark mark='b'/> A six means the third and the sixth. <bookmark mark='c'/> A seven "
            "means the third, the fifth and the seventh. In which octave? How many notes, and which one "
            "on top? That is left to the player, who decides while playing. It is called figured bass, "
            "and for a hundred and fifty years nearly every accompaniment in Europe was written this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in figs], lag_ratio=0.2), run_time=1.5)
            for mark, r in zip("abc", rules):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twice(self):
        d = load("figured")
        c = clip("figured.twice")
        st, figs = self.bass_staff(width=11.0, y=-1.75)
        rolls, groups = [], []
        for chords, col, x in ((d["a"], TUNE, -3.2), (d["b"], FIG_COL, 3.2)):
            rows = []
            for k, ch in enumerate(chords):
                rows.append((k, 1, P(d["bass"][k]).midi + 12))             # the bass, drawn an octave up so that both fit one picture
                rows += [(k, 1, m) for m in ch]
            r = piano_roll(rows, width=5.4, height=3.0, lo=54, hi=82, color=col, total=8).move_to([x, 1.55, 0])
            for k in range(8):
                r.notes[4 * k].set_fill(GREY_B)
            rolls.append(r)
            groups.append([VGroup(*r.notes[4 * k + 1: 4 * k + 4]) for k in range(8)])
        tags = VGroup(*[label(t, font_size=28, color=col).next_to(r, UP, buff=0.12) for t, r, col in zip((r"player A", r"player B"), rolls, (TUNE, FIG_COL))])
        note = listen_note(r"two players read the same bass and the same figures", width=8.4).move_to(UP * 1.0)
        with self.voiceover("Here is that bass line, played twice. Two players read the same eight notes and the same four figures."):
            self.play(FadeIn(st), FadeIn(figs), FadeIn(note))
        self.play(FadeOut(note), FadeIn(rolls[0].frame), FadeIn(rolls[1].frame), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"one figured bass, \ filled in twice", detail=r"a plucked keyboard, \ modelled", corner=DL, tag_corner=DR)
            pulse(snd, tags[0], snd.time_of("A"), snd.time_of("B") - 0.2)          # whose turn it is: never a still screen
            pulse(snd, tags[1], snd.time_of("B"), c.duration)
            for nm, r, grp in zip("AB", rolls, groups):
                ts = d["times"][nm]
                light(snd, [n.ink for n in st.notes], ts, end=ts[-1] + 1.5)
                for k, t in enumerate(ts):
                    snd.wait_until(t)
                    self.play(FadeIn(r.notes[4 * k], scale=0.8), FadeIn(grp[k], scale=0.8), run_time=0.3)
        count = label(r"ways to fill these eight chords within a hand's reach: \ " + r"{:,.0f}".format(d["count"]).replace(",", "{,}"), font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Both are correct. Every chord in each has the notes its figure asks for; the players only "
            "chose different octaves and different notes on top. <bookmark mark='a'/> Monochord counted "
            "more than six million ways to fill these eight chords within the reach of a hand, and chose "
            "two in which the upper voices move smoothly. The rules for choosing well are the subject of "
            "Parts 16 and 17. And the bargain itself never went away: a jazz musician's lead sheet, a "
            "melody with chord symbols over it, is figured bass four centuries on."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(tags), FadeIn(count))
        self.wait(0.4)
        self.clear_scene()
