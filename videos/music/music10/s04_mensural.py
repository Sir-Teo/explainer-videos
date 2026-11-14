from __future__ import annotations

from fractions import Fraction as F

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def modern_head(hollow: bool = True, stem: bool = False, size: float = 0.3, color=WHITE) -> VGroup:
    """A whole note (hollow, no stem) or a half note (hollow, with a stem)."""
    head = Ellipse(width=1.35 * size, height=0.9 * size, color=color, stroke_width=4, fill_color=color, fill_opacity=0.0 if hollow else 1.0).rotate(0.3)
    g = VGroup(head)
    if stem:
        g.add(Line(head.get_right() + UP * 0.05 * size, head.get_right() + UP * 3.2 * size, color=color, stroke_width=3))
    return g


def row_of(symbols: str, lengths, space: float = 0.42, gap: float = 1.0, color=WHITE) -> VGroup:
    """Shapes in a row with their lengths (in semibreves) written under them."""
    g = VGroup()
    g.shapes, g.nums = [], []
    for k, (s, n) in enumerate(zip(symbols, lengths)):
        sh = mensural_shape(s, space, color)
        sh.shift(np.array([k * gap, 0, 0]) - sh.body.get_center())
        num = label(str(n), font_size=30, color=INK).move_to([k * gap, -0.75, 0])
        g.add(sh, num)
        g.shapes.append(sh)
        g.nums.append(num)
    return g


class Mensural(SoundScene):
    def construct(self):
        chapter(self, 3, r"How long?", r"When did a written note get a length?", extra=((1280, r"Franco of Cologne"),))
        self.problem()
        self.shapes()
        self.signs()
        self.neighbours()
        self.dots()

    # ------------------------------------------------------------------
    def problem(self):
        top = square_staff([4, 5, 4, 3, 4, 5, 6, 5, 4, 3, 4], width=9.0, space=0.36, clef="C", clef_line=1).move_to(UP * 1.9)
        low = square_staff([0, 2, 1, 0], width=9.0, space=0.36, clef="F", clef_line=2).move_to(UP * 0.1)
        q = label(r"which notes sound together?", font_size=30, color=BAD).move_to(DOWN * 1.2)
        card = history_card(1280, r"Franco of Cologne, \ \textit{The Art of Measurable Song}", r"let the shape of a note show how long it lasts", width=7.0, font_size=24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Guido's notes say which pitch. They say nothing about how long. For chant, sung by everyone "
            "together, that was enough. But by the year 1200, at Notre Dame in Paris, singers were singing "
            "different melodies at the same time. <bookmark mark='a'/> One voice has eleven notes, the "
            "other four. Which ones sound together? The page cannot say. For a while the answer was a set "
            "of fixed rhythmic patterns that the singers had to recognize. <bookmark mark='b'/> Then, "
            "about 1280, a treatise by Franco of Cologne made the proposal that every later system has "
            "kept: let the shape of each note show how long it lasts."
        ) as vo:
            self.play(FadeIn(top), FadeIn(low))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeOut(q), FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        names = [("L", r"long"), ("B", r"breve", ), ("S", r"semibreve"), ("M", r"minim")]
        means = [r"", r"``short''", r"``half short''", r"``the least''"]
        cols = VGroup()
        for (sym, nm), mean in zip(names, means):
            sh = mensural_shape(sym, 1.0)
            cols.add(VGroup(sh, label(nm, font_size=38, color=TUNE), label(mean, font_size=28, color=GREY_B) if mean else label(r"\phantom{x}", font_size=28)).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.6, aligned_edge=DOWN).move_to(UP * 1.3)
        whole = VGroup(modern_head(True, False, 0.5), label(r"whole note", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.25)
        half = VGroup(modern_head(True, True, 0.5), label(r"half note", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.25)
        whole.next_to(cols[2], DOWN, buff=0.8)
        half.next_to(cols[3], DOWN, buff=0.8).align_to(whole, DOWN)
        arrows = VGroup(Arrow(cols[2].get_bottom(), whole.get_top(), buff=0.1, color=GREY_B, stroke_width=3, tip_length=0.15),
                        Arrow(cols[3].get_bottom(), half.get_top(), buff=0.1, color=GREY_B, stroke_width=3, tip_length=0.15))
        with self.voiceover(
            "These are Franco's shapes. A square with a tail is the long. <bookmark mark='a'/> A plain "
            "square is the breve, which means short. <bookmark mark='b'/> A lozenge is the semibreve, the "
            "half short. <bookmark mark='c'/> And the next century added the minim, the least, because "
            "composers wanted something quicker still. <bookmark mark='d'/> They are with us yet. Round "
            "off the lozenge and it is our whole note; give the minim a round head and it is our half "
            "note. In Britain they still go by the old names. And notice what happened: composers kept "
            "reaching for shorter notes, the old ones were sung slower and slower, and the note once "
            "called the half short is now the longest one in everyday use."
        ) as vo:
            self.play(FadeIn(cols[0]))
            for mark, col in zip("abc", cols[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(col), run_time=0.6)
            vo.wait_until("d")
            self.play(GrowArrow(arrows[0]), FadeIn(whole), GrowArrow(arrows[1]), FadeIn(half))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signs(self):
        d = load("mensural")
        c = clip("mensural.signs")
        steps = [p + 2 for p in d["positions"]]                 # the bottom line is C
        circle = VGroup(time_sign(True, 0.7), label(r"perfect time: \ a breve is three semibreves", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.5)
        broken = VGroup(time_sign(False, 0.7), label(r"imperfect time: \ a breve is two", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.5)
        signs = VGroup(circle, broken).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.3 + LEFT * 1.0)
        ask = VGroup(mensural_shape("B", 0.8), label(r"$=$", font_size=40, color=GREY_B), mensural_shape("S", 0.8), mensural_shape("S", 0.8), mensural_shape("S", 0.8).set_opacity(0.35),
                     label(r"three semibreves, \ or two?", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.7)
        common = VGroup(label(r"$=$", font_size=40, color=GREY_B), glyph("\U0001D134", 0.6), label(r"``common time''", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.35).next_to(broken, DOWN, buff=0.7).align_to(broken, LEFT)
        with self.voiceover(
            "How many semibreves make a breve? Either three or two. Three was called perfect, two "
            "imperfect, and a sign at the start of the music said which. <bookmark mark='a'/> A whole "
            "circle: perfect time, a breve is worth three. <bookmark mark='b'/> A broken circle: imperfect "
            "time, a breve is worth two. <bookmark mark='c'/> That broken circle is still printed at the "
            "start of music today. The C that stands for common time was never a letter."
        ) as vo:
            self.play(FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeIn(circle))
            vo.wait_until("b")
            self.play(FadeIn(broken))
            vo.wait_until("c")
            self.play(FadeIn(common))
        self.wait(0.3)
        self.clear_scene()
        rows = []
        for perfect, key, y in ((False, "two", 2.2), (True, "three", -0.3)):
            m = mensural(d["marks"], steps, width=12.4, space=0.3, perfect=perfect).move_to(UP * y)
            nums = VGroup(*[label(str(n), font_size=26, color=INK).move_to([nt.body.get_x(), m.lines.get_bottom()[1] - 0.45, 0]) for nt, n in zip(m.notes, d[key]["lengths"])])
            rows.append(VGroup(m, nums))
        note = listen_note(r"the same fourteen marks, \ read in twos and then in threes", width=8.6).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are the first two phrases of the Tune in Franco's marks: six semibreves and a breve, "
            "twice. Above, under the broken circle. Below, the very same marks under the whole circle. "
            "Listen to what the sign does."
        ):
            self.play(FadeIn(rows[0][0]), FadeIn(rows[1][0]), FadeIn(note))
            self.play(FadeIn(rows[0][1]), FadeIn(rows[1][1]))
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"in twos, \ then in threes", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            for key, row in zip(("two", "three"), rows):
                ts = d["times"][key]
                light(snd, [n.body for n in row[0].notes], ts, end=ts[-1] + 1.4)
                for k, t in enumerate(ts):
                    snd.wait_until(t)
                    self.play(row[1][k].animate(rate_func=there_and_back).scale(1.4), run_time=0.22)
        with self.voiceover(
            f"Under the broken circle the phrase takes {say(d['two']['total'] // 2)} beats, and it is our "
            f"Tune. Under the whole circle the breves stretch to three, each phrase takes "
            f"{say(d['three']['total'] // 2)}, and the Tune turns into a dance in triple time. Nothing on "
            "the staff changed but the sign."
        ):
            self.play(Indicate(rows[0][0].sign, color=INK), Indicate(rows[1][0].sign, color=INK))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neighbours(self):
        d = load("mensural")
        head = VGroup(time_sign(True, 0.5), label(r"under the whole circle", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.5)
        ex = VGroup(*[row_of(s, d["examples"][s]) for s in ("BSB", "BSSB", "BSSSB")])
        ex.arrange(DOWN, buff=0.75, aligned_edge=LEFT).scale(1.25).move_to(LEFT * 3.2 + DOWN * 0.4)
        notes_ = VGroup(label(r"the breve gives up a third: \ 2 + 1", font_size=26, color=GREY_A),
                        label(r"the second semibreve is doubled: \ 1 + 2", font_size=26, color=BAD),
                        label(r"three fill a group by themselves", font_size=26, color=GREY_A))
        for n, e in zip(notes_, ex):
            n.next_to(e, RIGHT, buff=1.0).set_x(3.0)
        box = SurroundingRectangle(VGroup(ex[1].shapes[1], ex[1].shapes[2], ex[1].nums[1], ex[1].nums[2]), color=BAD, buff=0.15, stroke_width=3)
        with self.voiceover(
            "And here is the price. Under the whole circle a breve is worth three semibreves, unless a "
            "single semibreve follows it. <bookmark mark='a'/> Then the two of them together make the "
            "three, and the breve shrinks to two. <bookmark mark='b'/> What if two semibreves stand between "
            "two breves? They have to fill a group of three, so the second one is doubled. "
            "<bookmark mark='c'/> Look at those two. They are the same shape, and one lasts twice as long "
            "as the other. <bookmark mark='d'/> With three, each is worth one. To know how long a note "
            "lasts, you have to read its neighbours. Singers learned pages of rules like these, and "
            "Monochord's reader implements them. It was a notation for experts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex[0]), FadeIn(notes_[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex[1]), FadeIn(notes_[1]))
            vo.wait_until("c")
            self.play(Create(box))
            vo.wait_until("d")
            self.play(FadeIn(ex[2]), FadeIn(notes_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dots(self):
        g = P("G4")
        halves = SC.Score([SC.Voice([SC.Note(g, F(1)), SC.Note(g, F(1, 2)), SC.Note(g, F(1, 2)), SC.Note(g, F(1, 4)), SC.Note(g, F(1, 4)), SC.Note(g, F(1, 4)), SC.Note(g, F(1, 4)),
                                     *[SC.Note(g, F(1, 8)) for _ in range(8)]])], time=(4, 4))
        tree = Staff(halves, width=12.0, space=0.22, show_time=False).move_to(UP * 2.0)
        names = label(r"whole \ $=$ \ 2 halves \ $=$ \ 4 quarters \ $=$ \ 8 eighths", font_size=28, color=GREY_A).next_to(tree, DOWN, buff=0.35)
        dotted = SC.Score([SC.Voice([SC.Note(g, F(3, 8)), SC.Note(g, F(1, 8)), SC.Note(g, F(1, 4), tie=True), SC.Note(g, F(1, 4))])], time=(4, 4))
        ex = Staff(dotted, width=5.2, space=0.24, show_time=False).move_to(LEFT * 3.4 + DOWN * 1.5)
        l1 = label(r"a dot adds half", font_size=26, color=INK).next_to(ex.notes[0], UP, buff=0.9)
        l2 = label(r"a tie joins two notes", font_size=26, color=INK).next_to(VGroup(ex.notes[2], ex.notes[3]), UP, buff=0.9)
        with self.voiceover(
            "By about 1600 the threes had gone from the system. Every note is worth two of the next: a "
            "whole note is two halves, four quarters, eight eighths. <bookmark mark='a'/> What is left of "
            "perfect time is the dot. A dot after a note adds half its length. <bookmark mark='b'/> And a "
            "tie, a curved line between two notes of the same pitch, joins them into one."
        ) as vo:
            self.play(FadeIn(tree), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(ex), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(l2))
        self.wait(0.3)
        card = pause_card(r"How would you write a note that lasts five eighths of a whole note? \ And seven eighths?", width=8.6).move_to(RIGHT * 2.4 + DOWN * 1.6)
        with self.voiceover("So try this. How would you write a note that lasts five eighths of a whole note? And one that lasts seven eighths? Pause, and work it out."):
            self.play(FadeOut(ex), FadeOut(l1), FadeOut(l2), FadeIn(card.move_to(DOWN * 1.5)))
        self.wait(2.5)
        self.play(FadeOut(card))
        five = SC.Score([SC.Voice([SC.Note(g, F(1, 2), tie=True), SC.Note(g, F(1, 8)), SC.Rest(F(1, 8)), SC.Rest(F(1, 4))])], time=(4, 4))
        seven = SC.Score([SC.Voice([SC.Note(g, F(7, 8)), SC.Rest(F(1, 8))])], time=(4, 4))
        s5 = Staff(five, width=4.6, space=0.24, show_time=False, final_bar=False).move_to(LEFT * 3.6 + DOWN * 1.3)
        s7 = Staff(seven, width=4.0, space=0.24, show_time=False, final_bar=False).move_to(RIGHT * 3.4 + DOWN * 1.3)
        e5 = MathTex(r"\tfrac58 = \tfrac12 + \tfrac18", font_size=40).next_to(s5, DOWN, buff=0.5)
        e7 = MathTex(r"\tfrac78 = \tfrac12 + \tfrac14 + \tfrac18", font_size=40).next_to(s7, DOWN, buff=0.5)
        with self.voiceover(
            "Five eighths is a half and an eighth: a half note tied to an eighth note. <bookmark mark='a'/> "
            "Seven eighths is a half, a quarter and an eighth. A dot adds the quarter, and a second dot "
            "adds half of that, the eighth: one half note with two dots."
        ) as vo:
            self.play(FadeIn(s5), FadeIn(e5))
            vo.wait_until("a")
            self.play(FadeIn(s7), FadeIn(e7))
        self.wait(0.3)
        rule = MathTex(r"1 + \tfrac12 + \tfrac14 + \cdots + \tfrac{1}{2^n} \;=\; 2 - \tfrac{1}{2^n}", font_size=44).move_to(DOWN * 1.2)
        rule_l = label(r"a note with $n$ dots", font_size=28, color=GREY_A).next_to(rule, UP, buff=0.35)
        third = label(r"a third of a whole note? \ no sum of halvings reaches it: \ it needs a triplet", font_size=28, color=BAD).next_to(rule, DOWN, buff=0.6)
        with self.voiceover(
            "In general, each dot adds half of what the dot before it added. So a note with n dots lasts "
            "one, plus a half, plus a quarter, down to one over two to the n, times its plain length. "
            "<bookmark mark='a'/> That sum is two, minus one over two to the n. However many dots you "
            "write, a note never quite doubles. <bookmark mark='b'/> And a third of a note? No sum of "
            "halvings ever reaches a third. The system's patch for that is the triplet, three notes in "
            "the time of two, marked with a small figure three. Rhythm has all of Part 11 to itself."
        ) as vo:
            self.play(FadeOut(s5), FadeOut(s7), FadeOut(e5), FadeOut(e7), FadeIn(rule_l), FadeIn(rule))
            vo.wait_until("a")
            self.play(Indicate(rule, color=INK))
            vo.wait_until("b")
            self.play(FadeIn(third))
        self.wait(0.4)
        self.clear_scene()
