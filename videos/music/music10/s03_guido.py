from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403

SYL = ["ut", "re", "mi", "fa", "sol", "la"]


def stairs(rises, width: float = 0.85, unit: float = 0.3, color=GREY_B, names=SYL) -> VGroup:
    """Six steps, each ``rises[k] * unit`` above the last, with the syllables on them."""
    g = VGroup()
    g.steps = []
    y = 0.0
    for k, nm in enumerate(names):
        y += (rises[k - 1] * unit) if k else 0.0
        tread = Line([k * width, y, 0], [(k + 1) * width, y, 0], color=color, stroke_width=4)
        t = label(nm, font_size=30, color=WHITE).next_to(tread, UP, buff=0.1)
        st = VGroup(tread, t)
        if k:
            st.add(Line([k * width, y - rises[k - 1] * unit, 0], [k * width, y, 0], color=color, stroke_width=2))
        g.add(st)
        g.steps.append(st)
    return g


class Guido(SoundScene):
    def construct(self):
        chapter(self, 2, r"Guido's lines", r"How do you write how high?", lit=(1025,))
        self.staff()
        self.graph()
        self.hymn()
        self.half_step()

    # ------------------------------------------------------------------
    def staff(self):
        steps = steps_of(phrase_notes(0))
        st = square_staff(steps, width=10.0, space=0.5, words=WORDS, word_size=30).move_to(UP * 0.9)
        self.st = st
        names = VGroup(*[label(t, font_size=24, color=GREY_B).move_to([st.lines.get_right()[0] + 0.35, st.lines[0].get_y() + k * 0.25, 0]) for k, t in enumerate("CDEFGAB")])
        with self.voiceover(
            "The man was Guido, a monk who taught choirboys in the town of Arezzo, and the year was about "
            "1025. Rule four lines. <bookmark mark='a'/> Every line, and every space between two lines, is "
            "one step of the scale. Then write a letter at the start of a line, to say which note that line "
            "is. Here the letter C sits on the bottom line. So the bottom line is C, the space above it D, "
            "the next line E, and so on up. <bookmark mark='b'/> And here is the Tune: C, C, up to G on the "
            "third line, G, the space above for A, A, and back to G."
        ) as vo:
            self.play(LaggedStart(*[Create(ln) for ln in st.lines], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(st.clef), LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.2), run_time=3.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n, scale=1.5) for n in st.notes], lag_ratio=0.6), FadeIn(st.words), run_time=6.0)
        pairs = VGroup()
        for letter, ch, h in (("G", "\U0001D11E", 1.5), ("F", "\U0001D122", 0.9), ("C", "\U0001D121", 1.0)):
            pairs.add(VGroup(Text(letter, font_size=44, color=RED_LINE, weight="BOLD"), label(r"$\rightarrow$", font_size=34, color=GREY_B), glyph(ch, h)).arrange(RIGHT, buff=0.3))
        pairs.arrange(RIGHT, buff=1.1).move_to(DOWN * 2.3)
        with self.voiceover(
            "That letter is the clef; the word means key. We still use Guido's letters. Centuries of "
            "penmanship have disguised them, but these three signs are a G, an F and a C, and each still "
            "marks the line that carries its note."
        ):
            self.play(FadeOut(names), LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        card = history_card(1030, r"Guido of Arezzo, \ preface to his chant book", r"his singers learn in a year, \ or two at most, \ what used to take ten", width=6.6, font_size=24).move_to(DOWN * 2.2)
        with self.voiceover(
            "Guido was not modest about it. In the preface to his chant book he claimed that with lines and "
            "letters a singer could be trained in a year, or two at most, where ten had been needed. And in "
            "a letter to a friend he reported that his choirboys could sing, correctly, chants they had "
            "never heard. Nobody had been able to say that before. A tune could now travel without a singer "
            "to carry it."
        ):
            self.play(FadeOut(pairs), FadeIn(card))
        self.wait(0.3)
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def graph(self):
        st = self.st
        ax_t = Arrow(st.lines.get_corner(DL) + DOWN * 1.25, st.lines.get_corner(DR) + DOWN * 1.25, buff=0, color=TIME, stroke_width=4, tip_length=0.2)
        ax_p = Arrow(st.lines.get_corner(DL) + LEFT * 0.75 + DOWN * 0.3, st.lines.get_corner(UL) + LEFT * 0.75 + UP * 0.5, buff=0, color=FREQ, stroke_width=4, tip_length=0.2)
        lt = label(r"time", font_size=28, color=TIME).next_to(ax_t, DOWN, buff=0.1)
        lp = label(r"pitch", font_size=28, color=FREQ).rotate(PI / 2).next_to(ax_p, LEFT, buff=0.1)
        path = VMobject(color=INK, stroke_width=3).set_points_as_corners([n.get_center() for n in st.notes])
        note = label(r"Nicole Oresme draws quantities against time: \ the 1350s. \ \ Choirs had been reading this for three hundred years.", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now look at what this is. <bookmark mark='a'/> From left to right is time. From bottom to top "
            "is pitch. <bookmark mark='b'/> It is a graph. Nicole Oresme, who is often given the credit for "
            "the first graphs of a quantity that changes in time, drew his in the thirteen fifties. By then "
            "choirs all over Europe had been reading one for three hundred years."
        ) as vo:
            vo.wait_until("a")
            self.play(GrowArrow(ax_t), FadeIn(lt))
            self.play(GrowArrow(ax_p), FadeIn(lp))
            vo.wait_until("b")
            self.play(Create(path), FadeIn(note), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hymn(self):
        d = load("guido")
        c = clip("guido.hymn")
        st = stairs([1, 1, 1, 1, 1], unit=0.42).move_to(LEFT * 3.9 + DOWN * 0.3)
        head = label(r"\textit{Ut queant laxis}: \ a hymn to Saint John", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        staves = []
        for row in d["lines"]:
            stf = square_staff(steps_of([SC.Note(P(n), SC.Q) for n in row["notes"]], "C3"), width=6.2, space=0.42).move_to(RIGHT * 3.0 + UP * 0.2)
            words = label(rf"\textit{{{row['words']}}}", font_size=34, color=WHITE).next_to(stf, DOWN, buff=0.5)
            staves.append(VGroup(stf, words))
        note = listen_note(r"six lines. \ Where does each one start?", width=7.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How did Guido's boys find their notes? He taught them a hymn they already knew, to Saint John, "
            "and pointed out something about it. Listen to where each line begins. The singer is the voice "
            "we built in Part 8."
        ):
            self.play(FadeIn(head), FadeIn(st), FadeIn(staves[0][0].lines), FadeIn(staves[0][0].clef), FadeIn(note))
        self.play(FadeOut(note))
        self.remove(staves[0][0].lines, staves[0][0].clef)
        shown = None
        with self.listen(c) as snd:
            window(snd, r"the hymn, \ line by line", detail=r"Part 8's voice", corner=DL, tag_corner=DR)
            for k, row in enumerate(d["lines"]):
                snd.wait_until(f"line{k}")
                if shown is not None:
                    self.remove(shown)
                shown = staves[k]
                self.add(shown)
                nxt = snd.time_of(f"line{k + 1}") if k < 6 else c.duration
                light(snd, shown[0].notes, d["times"][k], end=nxt)
                if k < 6:
                    pulse(snd, st.steps[k], snd.time_of(f"line{k}"), nxt - 0.3, buff=0.06)
                    self.play(st.steps[k][1].animate.set_color(INK).scale(1.25), run_time=0.4)
                for t in d["times"][k][1:]:                      # the notes of the line appear as they are sung
                    snd.wait_until(t)
                    j = d["times"][k].index(t)
                    self.play(shown[0].notes[j].animate(rate_func=there_and_back).scale(1.3), run_time=0.2)
        self.remove(shown)
        six = square_staff([0, 1, 2, 3, 4, 5], width=6.2, space=0.42, words=SYL, word_size=30).move_to(RIGHT * 3.0 + UP * 0.9)
        names = VGroup(label(r"ut \ $\rightarrow$ \ do", font_size=34, color=TUNE), label(r"\textbf{S}ancte \textbf{I}ohannes \ $\rightarrow$ \ si", font_size=34, color=TUNE)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.0 + DOWN * 2.0)
        with self.voiceover(
            "Each of the first six lines starts one step higher than the line before. So the first "
            "syllables of those lines became the names of the six notes: ut, re, mi, fa, sol, la. "
            "<bookmark mark='a'/> Six centuries later, in Italy, ut was changed to do, which is easier to "
            "sing. <bookmark mark='b'/> And a seventh name, si, was made from the initials of the last "
            "line: Sancte Iohannes, Saint John. A boy who knew the hymn could find any of the six notes by "
            "singing the start of its line."
        ) as vo:
            self.play(FadeIn(six.lines), FadeIn(six.clef))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(n), FadeIn(w)) for n, w in zip(six.notes, six.words)], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("a")
            self.play(FadeIn(names[0]))
            vo.wait_until("b")
            self.play(FadeIn(names[1]))
        self.wait(0.3)
        self.play(FadeOut(names), FadeOut(head), FadeOut(six))
        self.st2 = st

    # ------------------------------------------------------------------
    def half_step(self):
        d = load("guido")
        st = self.st2
        real = stairs(d["first_steps"], unit=0.26).move_to(st.get_center(), aligned_edge=DOWN).align_to(st, DOWN).align_to(st, LEFT)
        for s in real.steps:
            s[1].set_color(INK)
        staff = square_staff([0, 1, 2, 3, 4, 5], width=5.6, space=0.5).move_to(RIGHT * 3.3 + UP * 0.2)
        cap_l = label(r"how far apart the notes are", font_size=24, color=GREY_A).next_to(real, DOWN, buff=0.4)
        cap_r = label(r"how far apart they look", font_size=24, color=GREY_A).next_to(staff, DOWN, buff=0.4)
        brace = Brace(Line(real.steps[2][0].get_right(), real.steps[3][0].get_left()), DOWN, color=BAD, buff=0.45)
        half = label(r"half a step", font_size=24, color=BAD).next_to(brace, DOWN, buff=0.08)
        gap = SurroundingRectangle(VGroup(staff.notes[2], staff.notes[3]), color=BAD, buff=0.12, stroke_width=3)
        with self.voiceover(
            "The hymn taught one more thing, and it is the thing the staff does not show. Those six steps "
            "are not equal. <bookmark mark='a'/> From mi up to fa is half the size of the others: a "
            "semitone. Tone, tone, semitone, tone, tone. <bookmark mark='b'/> Now look at the same six "
            "notes on Guido's lines. Line, space, line, space: every step looks the same. "
            "<bookmark mark='c'/> The staff counts the steps of a scale. It does not measure distance. "
            "Which of its steps are the small ones is not written anywhere on the page; the singer has to "
            "know. That is why the staff later needed sharps, flats and key signatures, and we will come to "
            "those in Part 12. For now, notice that even Guido's page is written for someone who already "
            "knows something: the scale."
        ) as vo:
            vo.wait_until("a")
            self.play(ReplacementTransform(st, real), FadeIn(cap_l), run_time=1.5)
            self.play(GrowFromCenter(brace), FadeIn(half))
            vo.wait_until("b")
            self.play(FadeIn(staff), FadeIn(cap_r))
            vo.wait_until("c")
            self.play(Create(gap))
        self.wait(0.4)
        self.clear_scene()
