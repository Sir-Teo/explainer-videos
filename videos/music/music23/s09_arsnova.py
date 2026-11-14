from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403

SIGNS = ["O with a dot", "O", "C with a dot", "C"]


def sign_mob(name, size=0.5, color=WHITE):
    circ = "O" in name
    g = VGroup()
    if circ:
        g.add(Circle(radius=size / 2, color=color, stroke_width=3))
    else:
        g.add(Arc(radius=size / 2, start_angle=PI / 4, angle=3 * PI / 2, color=color, stroke_width=3))
    if "dot" in name:
        g.add(Dot(radius=0.05, color=color))
    return g


class ArsNova(SoundScene):
    def construct(self):
        chapter(self, 8, r"The Ars nova and mensuration", r"Why was duple time new?", extra=((1322, r"the \textit{Ars nova}"),))
        self.new_art()
        self.four()
        self.rules()

    # ------------------------------------------------------------------
    def new_art(self):
        items = [
            (r"about 1320: \ treatises from Paris, \ the \textit{Ars nova} \ (after Philippe de Vitry) \ and Johannes de Muris", WHITE),
            (r"a new smallest note, \ the minim; \ and division by two as legitimate as division by three", WHITE),
            (r"1324--25: \ Pope John XXII's bull \textit{Docta sanctorum}: \ notes too quick, \ melodies chopped by hockets", WHITE),
            (r"Jacques de Liège, \ \textit{Speculum musicae}: \ a long defence of the old art", WHITE),
            (r"the first quarrel of ancients and moderns in music, \ and the names stuck: \ \textit{ars antiqua}, \ \textit{ars nova}", TUNE),
        ]
        rows_scene(self, r"a new art", items,
                   "Around 1320 a group of Paris musicians described what they called a new art, the Ars nova. "
                   "<bookmark mark='b'/> The treatises, one based on the teaching of the poet, composer and later bishop "
                   "Philippe de Vitry, another by the astronomer Johannes de Muris, added a smaller note, the minim, and "
                   "said that dividing a note into two was as proper as dividing it into three. <bookmark mark='c'/> Not "
                   "everyone approved. In 1324 or 1325 Pope John the Twenty-second issued a decree complaining that the "
                   "new singers chopped melodies into hockets, ran in quick notes, and drowned the chant. "
                   "<bookmark mark='d'/> An old theorist, Jacques de Liège, wrote a vast encyclopedia whose last book "
                   "defends the old art against the new. <bookmark mark='e'/> It was the first quarrel of ancients and "
                   "moderns in music, and its names stuck: historians still say ars antiqua and ars nova.")

    # ------------------------------------------------------------------
    def four(self):
        d = load("mensuration")
        c = clip("mensuration.four")
        shapes = d["shapes"]
        top = VGroup()
        for sh in shapes:
            if sh == "B":
                m = Rectangle(width=0.4, height=0.3, stroke_width=0, fill_color=WHITE, fill_opacity=1)
            elif sh == "S":
                m = Square(side_length=0.26, stroke_width=0, fill_color=WHITE, fill_opacity=1).rotate(PI / 4)
            else:
                d_ = Square(side_length=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).rotate(PI / 4)
                m = VGroup(d_, Line(d_.get_top(), d_.get_top() + UP * 0.4, color=WHITE, stroke_width=2))
            top.add(m)
        top.arrange(RIGHT, buff=0.35).to_edge(UP, buff=1.0)
        tl = label(r"one row of shapes: \ breve, \ semibreve, \ minim", font_size=20, color=GREY_A).next_to(top, UP, buff=0.2)
        rows_ = VGroup()
        rolls = []
        for k, sign in enumerate(SIGNS):
            r = d["readings"][sign]
            g = mroll(r["notes"], width=7.0, height=0.55, lo=60, hi=67, total=40.0, bar_h=0.12)
            s = sign_mob(sign, size=0.42, color=TUNE if k < 2 else BLUE)
            t = label(rf"{r['modern']}", font_size=20, color=GREY_A)
            rows_.add(VGroup(s, t, g).arrange(RIGHT, buff=0.35))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.9)
        cap = label(r"a circle: \ perfect time, \ three semibreves to the breve; \ a dot: \ major prolation, \ three minims to the semibreve", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The new art measured time on two levels. Tempus says how many semibreves make a breve: three, perfect, or "
            "two, imperfect. Prolation says how many minims make a semibreve: three, major, or two, minor. That gives "
            "four mensurations, written with signs at the start of the music: a circle for perfect time, a broken circle "
            "for imperfect, and a dot inside for major prolation. They correspond, roughly, to our nine-eight, three-four, "
            "six-eight and two-four. Here is one row of note shapes read in all four. The notes on the page do not "
            "change; their lengths do."
        ):
            self.play(FadeIn(tl), FadeIn(top), FadeIn(rows_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the same shapes in four mensurations", detail=r"one synthetic voice", kind="synthesized", corner=UR, tag_corner=UL)
            for k, sign in enumerate(SIGNS):
                st = d["starts"][sign]
                flash(snd, rolls[k].notes, [st + n[1] * d["unit"] for n in d["readings"][sign]["notes"]], hot=WHITE, base=TUNE)
                flash(snd, list(top), [st + n[1] * d["unit"] for n in d["readings"][sign]["notes"]], hot=TUNE, base=WHITE)
                end = d["starts"][SIGNS[k + 1]] - 0.4 if k < 3 else c.duration
                pulse(snd, rows_[k][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        d = load("mensuration")
        f = d["franco"]
        tab = VGroup()
        for shapes, vals in f.items():
            row = VGroup(label(r"\ ".join(shapes), font_size=26, color=WHITE), label(r"$\to$", font_size=26, color=GREY_B),
                         label(r"\ ".join(str(v) for v in vals), font_size=26, color=TUNE),
                         label(rf"= {sum(vals)} = {sum(vals) // 3} perfections", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.35)
            tab.add(row)
        tab.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.7)
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"in perfect time a breve is worth three semibreves \ unless a single semibreve sits next to it: \ then two \ (imperfection)", WHITE),
            (r"two semibreves between breves: \ the second is doubled \ (alteration), \ to fill the perfection", WHITE),
            (r"three: \ one each; \ four: \ the first imperfects the breve before it", WHITE),
            (r"a note's length depends on what comes after it: \ reading needs lookahead", TUNE))]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.45)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        with self.voiceover(
            "In perfect time, reading even the simplest rhythm takes rules, Franco's rules, which the new art kept. "
            "<bookmark mark='a'/> A breve is worth three semibreves, unless a single semibreve stands next to it, which "
            "takes a third of its value: imperfection. So breve, semibreve, breve reads two, one, three. "
            "<bookmark mark='b'/> Two semibreves between breves would leave a perfection one short, so the second is "
            "doubled: alteration. Breve, two semibreves, breve reads three, one, two, three. <bookmark mark='c'/> Three "
            "semibreves fill a perfection by themselves; with four, the first imperfects the breve before it. "
            "<bookmark mark='d'/> The program that reads these rows needs to look ahead: the length of a note depends on "
            "the notes after it. Every reading comes out in whole perfections, which is how the rules were designed, and "
            "how the tests check them."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
