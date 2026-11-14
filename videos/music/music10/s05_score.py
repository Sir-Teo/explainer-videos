from __future__ import annotations

from fractions import Fraction as F

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def duet() -> tuple[SC.Score, SC.Score]:
    d = load("score")
    top = phrase_score(0, 4)
    low = SC.Score([SC.Voice([SC.Note(P(b), SC.H) for b in d["bass"]], clef="bass")], time=(4, 4), tempo=top.tempo)
    return top, low


class ScoreScene(SoundScene):
    def construct(self):
        chapter(self, 4, r"Bars and scores", r"How do many people read together?", extra=((1577, r"the first printed scores"),))
        self.parts()
        self.score()
        self.model()
        self.more()

    # ------------------------------------------------------------------
    def parts(self):
        top, low = duet()
        a = Staff(top, width=6.0, space=0.17, show_time=False, final_bar=False).move_to(LEFT * 3.4 + UP * 0.4)
        b = Staff(low, width=4.6, space=0.17, show_time=False, final_bar=False).move_to(RIGHT * 3.8 + DOWN * 0.6)
        for s in (a, b):
            s.barlines.set_opacity(0)
        book_a = VGroup(RoundedRectangle(width=6.6, height=2.6, corner_radius=0.12, stroke_color=CLAY, stroke_width=2).move_to(a), label(r"the upper voice's book", font_size=24, color=CLAY))
        book_b = VGroup(RoundedRectangle(width=5.2, height=2.6, corner_radius=0.12, stroke_color=CLAY, stroke_width=2).move_to(b), label(r"the lower voice's book", font_size=24, color=CLAY))
        book_a[1].next_to(book_a[0], UP, buff=0.15)
        book_b[1].next_to(book_b[0], UP, buff=0.15)
        self.a, self.b = a, b
        with self.voiceover(
            "Once notes had lengths, voices could be written apart and still fit together. And for three "
            "hundred years that is how music for several voices was written: each voice by itself, in its "
            "own book or its own corner of a large one. <bookmark mark='a'/> A singer saw one line, and "
            "counted. There were no bar lines; nothing on your page told you what anyone else was "
            "doing. If you lost your place, the page could not help you find it."
        ) as vo:
            self.play(FadeIn(book_a), FadeIn(a))
            self.play(FadeIn(book_b), FadeIn(b))
            vo.wait_until("a")
            self.play(Indicate(a.notes[6].ink, color=INK), Indicate(b.notes[3].ink, color=INK))
        self.wait(0.3)
        self.play(FadeOut(book_a), FadeOut(book_b), FadeOut(a), FadeOut(b))

    # ------------------------------------------------------------------
    def score(self):
        top, low = duet()
        c = clip("score.duet")
        kw = dict(width=11.6, space=0.2, proportional=True, lead=2.3, show_time=False)
        a = Staff(top, **kw).move_to(UP * 1.5)
        b = Staff(low, **kw).move_to(DOWN * 0.7)
        brace = Line(a.systems[0].lines.get_corner(UL), b.systems[0].lines.get_corner(DL), color=WHITE, stroke_width=3)
        joins = VGroup(*[Line(x.get_bottom(), y.get_top(), color=GREY_C, stroke_width=1.5) for x, y in zip(a.barlines, b.barlines)])
        ties = VGroup(*[DashedLine(a.notes[k].head.get_center() + DOWN * 0.25, b.notes[k // 2 if k < 7 else (k + 1) // 2].head.get_center() + UP * 0.25, color=INK, stroke_width=2, dash_length=0.08)
                        for k in (0, 2, 4, 6)])
        a.barlines.set_opacity(0)
        b.barlines.set_opacity(0)
        head = label(r"a score", font_size=34, color=TUNE).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The cure was to stack the voices on one page, so that notes sounded together are written one "
            "above the other. <bookmark mark='a'/> That is a score. And then to rule lines down through "
            "all the staves every few beats: bar lines, a ruler for the eye. <bookmark mark='b'/> Organists "
            "and lute players, who had to play several voices with their own two hands, wrote this way "
            "first. The first printed scores date from the fifteen seventies, and by 1650 the bar line was "
            "everywhere. Guido's graph had gained grid lines."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), FadeIn(brace), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t) for t in ties], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(a.barlines.animate.set_opacity(1), b.barlines.animate.set_opacity(1), LaggedStart(*[Create(j) for j in joins], lag_ratio=0.2), FadeOut(ties), run_time=2.0)
        note = listen_note(r"two voices, \ one clock: \ watch the line cross both staves", width=8.4).to_edge(DOWN, buff=0.4)
        with self.voiceover("Here are the two voices together. One line, crossing both staves, shows where we are."):
            self.play(FadeIn(note))
        self.play(FadeOut(note))
        ca, cb = a.cursor(), b.cursor()
        link = Line(ca.get_bottom(), cb.get_top(), color=INK, stroke_width=3)
        self.add(ca, cb, link)
        with self.listen(c) as snd:
            window(snd, r"the Tune and a bass", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            snd.drive(ca, a.follow())
            snd.drive(cb, lambda m, t: m.set_x(ca.get_x()))
            snd.drive(link, lambda m, t: m.put_start_and_end_on(ca.get_bottom(), cb.get_top()))
            light(snd, [n.ink for n in a.notes], [snd.time_of(f"n{k}") for k in range(14)], end=c.duration)
            light(snd, [n.ink for n in b.notes], [snd.time_of(f"b{k}") for k in range(8)], end=c.duration)
        self.play(FadeOut(ca), FadeOut(cb), FadeOut(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        g = P("G4")
        raw = SC.Score([SC.Voice([SC.Note(g, F(1, 2)), SC.Note(g, F(3, 4)), SC.Note(g, F(3, 4))])], time=(4, 4))
        st = Staff(raw, width=8.0, space=0.26).move_to(DOWN * 1.0)
        lengths = VGroup(*[RoundedRectangle(width=w, height=0.9, corner_radius=0.1, stroke_color=TUNE, stroke_width=2.5, fill_color=TUNE, fill_opacity=0.25) for w in (2.0, 3.0, 3.0)]).arrange(RIGHT, buff=0.06).move_to(UP * 1.9)
        fr = VGroup(*[MathTex(t, font_size=52).move_to(r) for t, r in zip((r"\tfrac12", r"\tfrac34", r"\tfrac34"), lengths)])
        bar = DashedLine(lengths.get_left() + RIGHT * 4.03 + UP * 0.75, lengths.get_left() + RIGHT * 4.03 + DOWN * 0.75, color=BAD, stroke_width=3)
        bl = label(r"a bar line falls here", font_size=24, color=BAD).next_to(bar, UP, buff=0.1)
        cap = label(r"Monochord keeps exact fractions, \ and cuts and ties a note where a bar line crosses it", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The bar line has a cost, and Monochord's score model pays it the way an engraver does. Inside "
            "Monochord a note's length is an exact fraction of a whole note: a half, three quarters, three "
            "quarters. <bookmark mark='a'/> But in four-four time a bar line falls after one whole note, in "
            "the middle of the second note. <bookmark mark='b'/> So on the page that note is cut in two, a "
            "half and a quarter, and the pieces are tied across the line. Three notes are played; four are "
            "written. The page is no longer a list of the notes. It is a drawing of them, fitted to a grid."
        ) as vo:
            self.play(FadeIn(lengths), FadeIn(fr))
            vo.wait_until("a")
            self.play(Create(bar), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(st), FadeIn(cap))
            self.play(Indicate(VGroup(st.notes[1].ink, st.notes[2].ink), color=INK))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def more(self):
        top = phrase_score(0, 2)
        st = Staff(top, width=9.0, space=0.26).move_to(DOWN * 0.2)
        adds = [
            (Text("Allegro", font="FreeSerif", font_size=30, slant="ITALIC", weight="BOLD").next_to(st, UP, buff=0.25).align_to(st, LEFT).shift(RIGHT * 1.2), r"words for speed: \ about 1600"),
            (Text("p", font="FreeSerif", font_size=40, slant="ITALIC", weight="BOLD").next_to(st.notes[0], DOWN, buff=0.75), r"letters for loud and soft: \ about 1600"),
            (VGroup(Line(st.notes[2].head.get_center() + DOWN * 1.15 + LEFT * 0.1, st.notes[5].head.get_center() + DOWN * 0.95, color=WHITE, stroke_width=2.5),
                    Line(st.notes[2].head.get_center() + DOWN * 1.15 + LEFT * 0.1, st.notes[5].head.get_center() + DOWN * 1.35, color=WHITE, stroke_width=2.5)), r"hairpins: \ the 1700s"),
            (Text("♩ = 109", font="FreeSerif", font_size=30).next_to(st, UP, buff=0.25).align_to(st, RIGHT).shift(LEFT * 1.0), r"the metronome mark: \ 1815"),
        ]
        rows = VGroup(*[label(t, font_size=26, color=GREY_A) for _, t in adds]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.9)
        if rows.width > 12.6:
            rows.arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.25)).to_edge(DOWN, buff=0.6)
        head = label(r"what the notes still did not say", font_size=32, color=TUNE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "By 1650, then, the page said which notes and how long. It still did not say how fast, or how "
            "loud. So composers went on adding. <bookmark mark='a'/> Italian words for the speed. "
            "<bookmark mark='b'/> Letters for soft and loud. <bookmark mark='c'/> Hairpins, for growing "
            "louder. <bookmark mark='d'/> And, once Maelzel's metronome was on sale in 1815, a number of "
            "beats to the minute. Every one of those additions is an admission that something was missing. "
            "Hold on to that thought; we will count what is still missing at the end."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st))
            for mark, (m, _), r in zip("abcd", adds, rows):
                vo.wait_until(mark)
                self.play(FadeIn(m), FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
