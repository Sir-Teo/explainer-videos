from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403

SCALE = [("合", "he", "sol"), ("四", "si", "la"), ("一", "yi", "ti"), ("上", "shang", "do"), ("尺", "che", "re"), ("工", "gong", "mi"), ("凡", "fan", "fa"),
         ("六", "liu", "sol"), ("五", "wu", "la"), ("乙", "yi", "ti")]


class East(SoundScene):
    def construct(self):
        chapter(self, 6, r"Numbers and characters", r"Does a notation need a staff at all?", extra=((1742, r"Rousseau's numbers"),))
        self.characters()
        self.numbers()
        self.both()
        self.qin()
        self.graphic()

    # ------------------------------------------------------------------
    def characters(self):
        d = load("east")
        cols = VGroup()
        for ch, py, sol in SCALE:
            low = ch in "合四一"
            cols.add(VGroup(Text(ch, font=CJK, font_size=44, color=GREY_B if low else WHITE), label(py, font_size=24, color=GREY_B if low else TUNE), label(sol, font_size=22, color=GREY_B)).arrange(DOWN, buff=0.18))
        cols.arrange(RIGHT, buff=0.42).move_to(UP * 1.9)
        chars = d["gongche"]
        tune = gongche(chars, beats=d["beats"], height=3.0, font_size=34, columns=2).move_to(RIGHT * 4.3 + DOWN * 1.4)
        arrow = VGroup(Arrow(tune.get_corner(UR) + UP * 0.3 + RIGHT * 0.15, tune.get_corner(DR) + RIGHT * 0.15, buff=0, color=GREY_B, stroke_width=2.5, tip_length=0.15))
        cap = label(r"read down, \ then to the left", font_size=22, color=GREY_B).next_to(tune, DOWN, buff=0.25)
        text = VGroup(label(r"gongche: \ a character for each note of the scale", font_size=32, color=GREY_A),
                      label(r"a mark beside a character: \ hold it for the beat", font_size=30, color=GREY_A),
                      label(r"how long, \ otherwise? \ the singer learned that from a teacher", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(LEFT * 1.6 + DOWN * 1.3)
        self.gong = tune
        with self.voiceover(
            "A staff is one answer to the question of pitch. China had found a different one at least a "
            "thousand years ago: give every note of the scale a character. <bookmark mark='a'/> Their "
            "names are shang, cheh, gong, fahn, lee-oh, woo and ee. They stand for do, re, mi, fa, sol, la "
            "and ti. The system is named gongche, after two of them. <bookmark mark='b'/> Here are the first two phrases of the Tune. They read "
            "from the top down, and the columns run from right to left. A small mark beside a character "
            "shows where the beat is held. <bookmark mark='c'/> Otherwise, how long each note lasts is "
            "shown only roughly. A singer learned the rhythm from a teacher, with the page as a guide."
        ) as vo:
            self.play(FadeIn(text[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.35), run_time=5.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n) for n in tune.notes], lag_ratio=0.12), FadeIn(arrow), FadeIn(cap), FadeIn(text[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(text[2]))
        self.wait(0.3)
        self.play(FadeOut(cols), FadeOut(text), FadeOut(arrow), FadeOut(cap), FadeOut(tune))

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("east")
        card = history_card(1742, r"Jean-Jacques Rousseau, \ to the Academy of Sciences in Paris", r"write the seven notes of the scale as the numbers 1 to 7", width=7.4, font_size=24).to_edge(UP, buff=0.4)
        jp = jianpu(d["degrees"], d["beats"], width=11.0, font_size=44, key="1 = C").move_to(DOWN * 0.4)
        self.jp = jp
        how = VGroup(label(r"1 is the keynote", font_size=26, color=GREY_A), label(r"a dash: \ one more beat", font_size=26, color=GREY_A),
                     label(r"a line under a number: \ half a beat", font_size=26, color=GREY_A), label(r"a dot above or below: \ an octave", font_size=26, color=GREY_A)).arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.3), cell_alignment=LEFT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "And Europe produced a staffless notation too. In 1742 a young music copyist named "
            "Jean-Jacques Rousseau, who was not yet a philosopher, stood before the Academy of Sciences in "
            "Paris with a proposal: write the seven notes of the scale as the numbers one to seven. The "
            "Academy was polite, and unconvinced. <bookmark mark='a'/> But French schoolteachers made a "
            "singing method out of it; from France it went to Japan; and from Japan, soon after 1900, to "
            "China. There it is called jianpu, simple notation, and it became the everyday way to write "
            "music down. <bookmark mark='b'/> One is the keynote. A dash holds a note for another beat. A "
            "line under a number halves it, and a dot above or below moves it by an octave."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in jp], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h) for h in how], lag_ratio=0.5), run_time=4.0)
        self.wait(0.3)
        new_key = Text("1 = F", font=MONO, font_size=32, color=INK).move_to(jp.key).align_to(jp.key, LEFT)
        st_c = Staff(phrase_score(0, 2), width=5.6, space=0.15, show_time=False, final_bar=False).move_to(LEFT * 3.3 + DOWN * 2.4)
        in_f = SC.Score([SC.Voice([SC.Note(n.pitch.up(3, 5), n.dur) for n in phrase_notes(0)])], key=-1, time=(4, 4))
        st_f = Staff(in_f, width=5.6, space=0.15, show_time=False, final_bar=False).move_to(RIGHT * 3.3 + DOWN * 2.4)
        arrow = label(r"$\rightarrow$", font_size=44, color=GREY_B).move_to(DOWN * 2.4)
        with self.voiceover(
            "And it can do something that the staff cannot. To sing the Tune in another key, change one "
            "sign: one equals F. <bookmark mark='a'/> Nothing else on the page moves. On a staff, every "
            "note would have to be redrawn four lines and spaces higher, with a flat added. Jianpu "
            "does not write where a note is on the keyboard. It writes the note's place in the scale, "
            "which is what a singer needs."
        ) as vo:
            self.play(FadeOut(how), FadeOut(card))
            self.play(Transform(jp.key, new_key))
            vo.wait_until("a")
            self.play(FadeIn(st_c), FadeIn(arrow), FadeIn(st_f))
        self.wait(0.3)
        self.play(FadeOut(st_c), FadeOut(arrow), FadeOut(st_f))

    # ------------------------------------------------------------------
    def both(self):
        d = load("east")
        c = clip("east.flute")
        jp = self.jp
        tune = gongche(d["gongche"], beats=d["beats"], height=2.6, font_size=32, columns=2).move_to(RIGHT * 4.8 + DOWN * 0.5)
        self.play(jp.animate.scale(0.8).move_to(LEFT * 1.6 + UP * 0.3), FadeIn(tune))
        with self.listen(c) as snd:
            window(snd, r"the Tune in numbers and in characters", detail=r"Part 8's flute", corner=DL, tag_corner=DR)
            ts = [snd.time_of(f"n{k}") for k in range(14)]
            light(snd, [n[0] for n in jp.notes], ts, end=c.duration)
            light(snd, [n[0] for n in tune.notes], ts, end=c.duration)
            for k, t in enumerate(ts):
                snd.wait_until(t)
                self.play(jp.notes[k].animate(rate_func=there_and_back).scale(1.3), tune.notes[k].animate(rate_func=there_and_back).scale(1.3), run_time=0.22)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def qin(self):
        ch = qin_character(2.6).move_to(LEFT * 3.4 + DOWN * 0.2)
        top, hook, num = ch.parts
        rows = VGroup(label(r"an open string", font_size=30, color=TUNE), label(r"the middle finger pulls inward", font_size=30, color=TUNE), label(r"the third string", font_size=30, color=TUNE))
        rows.arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(RIGHT * 2.6 + UP * 0.3)
        arrows = VGroup(*[Arrow(r.get_left() + LEFT * 0.15, p.get_right() + RIGHT * 0.1, buff=0.05, color=GREY_B, stroke_width=2.5, tip_length=0.15) for r, p in zip(rows, (top, hook, num))])
        head = label(r"guqin tablature: \ one sign, \ one gesture", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        none = label(r"and not one mark about rhythm", font_size=30, color=BAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "One more, and the most radical. The goo-chin, China's seven-string zither, has had its own "
            "tablature for more than a thousand years. Each sign is put together from fragments of "
            "characters. <bookmark mark='a'/> The top says: an open string. <bookmark mark='b'/> The hook "
            "says: pull inward with the middle finger. <bookmark mark='c'/> And the strokes inside say: "
            "the third string. A whole gesture in one sign. <bookmark mark='d'/> And nothing at all about "
            "rhythm. The player works the timing out; two masters' versions of the same old piece can "
            "differ throughout. It is the tablet from Ugarit again: the page holds the actions, and a "
            "living tradition holds the rest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch))
            for mark, r, a, p in zip("abc", rows, arrows, (top, hook, num)):
                vo.wait_until(mark)
                self.play(FadeIn(r), GrowArrow(a), p.animate.set_color(INK), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(none))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def graphic(self):
        rng = np.random.default_rng(5)
        grid = VGroup()
        cell = 0.62
        for r, name in enumerate((r"low", r"middle", r"high")):
            grid.add(label(name, font_size=22, color=GREY_B).move_to([-0.7, r * cell, 0]))
            for cidx in range(12):
                grid.add(Square(side_length=cell, stroke_color=GREY_D, stroke_width=1.2).move_to([cidx * cell, r * cell, 0]))
        marks = VGroup()
        for cidx, r, w in ((0, 2, 1), (2, 0, 2), (3, 1, 1), (5, 2, 1), (6, 0, 1), (8, 1, 2), (10, 2, 1), (11, 0, 1)):
            marks.add(Rectangle(width=cell * w - 0.12, height=cell - 0.2, stroke_width=0, fill_color=TUNE, fill_opacity=0.9).move_to([(cidx + (w - 1) / 2) * cell, r * cell, 0]))
        left = VGroup(grid, marks).scale(0.85).move_to(LEFT * 3.1 + UP * 0.6)
        cap_l = label(r"boxes on a grid: \ which register, \ and when. \\ The notes are the player's. \ (after Feldman, \ 1950)", font_size=24, color=GREY_A).next_to(left, DOWN, buff=0.4)
        shapes = VGroup(Line(LEFT * 2.6, RIGHT * 2.6, color=GREY_B, stroke_width=2))
        for _ in range(7):
            x, y, r = float(rng.uniform(-2.3, 2.3)), float(rng.uniform(-0.9, 0.9)), float(rng.uniform(0.12, 0.5))
            shapes.add(Circle(radius=r, color=WHITE, stroke_width=float(rng.uniform(2, 5))).move_to([x, y, 0]))
        shapes.add(VMobject(color=WHITE, stroke_width=4).set_points_smoothly([np.array([x, 0.7 * np.sin(1.7 * x) + 0.2 * x, 0]) for x in np.linspace(-2.5, 2.5, 9)]))
        right = shapes.scale(0.9).move_to(RIGHT * 3.6 + UP * 0.6)
        cap_r = label(r"lines and shapes, \ and no instructions at all. \\ (in the manner of Cardew's \textit{Treatise}, \ 1963--67)", font_size=24, color=GREY_A).next_to(right, DOWN, buff=0.4).align_to(cap_l, UP)
        head = label(r"keeping less, \ on purpose", font_size=32, color=TUNE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Every notation so far kept as much as its makers could manage. In the twentieth century some "
            "composers went the other way, on purpose. <bookmark mark='a'/> In 1950 Morton Feldman wrote "
            "pieces as boxes on a grid: play something high here, something low there, for this long. "
            "Which notes is the player's business. <bookmark mark='b'/> And Cornelius Cardew's Treatise "
            "is a hundred and ninety-three pages of lines and shapes with no instructions whatever. A "
            "notation is a contract between the writer and the reader, and these contracts leave nearly "
            "everything to the reader."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), FadeIn(cap_l), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s) for s in shapes], lag_ratio=0.15), FadeIn(cap_r), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
