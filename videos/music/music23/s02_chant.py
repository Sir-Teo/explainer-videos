from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Chant(SoundScene):
    def construct(self):
        chapter(self, 1, r"Chant and the eight modes", r"How was one line of melody organized?", extra=((800, r"the first tonaries"),))
        self.chant()
        self.modes()
        self.psalmody()
        self.quiz()
        self.classifier()

    # ------------------------------------------------------------------
    def chant(self):
        d = load("chant")
        c = clip("chant.ut")
        notes = d["ut"]
        g = mroll(notes, width=11.6, height=1.9, lo=58, hi=71, total=max(n[1] + n[2] for n in notes)).move_to(UP * 0.2)
        syl = VGroup()
        for k in d["ut_lines"][:6]:
            syl.add(label(d["ut_syllables"][k], font_size=24, color=TUNE).next_to(g.notes[k], DOWN, buff=0.2))
        head = label(r"\textit{Ut queant laxis}, \ a hymn for St John the Baptist", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"one line, \ no harmony, \ no written rhythm: \ the notes last as long as the words want", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Western polyphony grew out of a repertory of single-line song: the chant of the Latin church, called "
            "Gregorian after a pope, Gregory the Great, who almost certainly had nothing to do with it. It took its form in the Frankish kingdoms of the "
            "eighth and ninth centuries, and was first written down in neumes, signs that show the shape of a melody "
            "but not its exact pitches. One voice, or many in unison; no independently composed accompanying voices in this monophonic model; early notation leaves many rhythmic details open. Here is a hymn "
            "whose tune will matter in the next chapter, Ut queant laxis, sung by one synthetic voice."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(syl), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"\textit{Ut queant laxis}", detail=r"one synthetic voice", kind="synthesized", corner=UL, tag_corner=UR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        d = load("chant")
        lo, hi = 55, 78
        W, x0 = 6.4, -0.6
        rows_ = VGroup()
        for k, m in enumerate(range(1, 9)):
            info = d["modes"][str(m)]
            y = 2.3 - 0.58 * k
            nm = label(rf"{m}. \ {info['name']}", font_size=20, color=TUNE if m % 2 else BLUE).move_to([-4.6, y, 0]).align_to(LEFT * 6.3, LEFT)
            r0, r1 = info["range"]
            bar = Rectangle(width=W * (r1 - r0) / (hi - lo), height=0.26, stroke_width=0, fill_color=TUNE if m % 2 else BLUE, fill_opacity=0.35)
            bar.move_to([x0 + W * ((r0 + r1) / 2 - lo) / (hi - lo), y, 0])
            fin = Dot([x0 + W * (info["final"] - lo) / (hi - lo), y, 0], radius=0.09, color=WHITE)
            ten = Square(side_length=0.17, stroke_width=0, fill_color=EAR, fill_opacity=1).move_to([x0 + W * (info["tenor"] - lo) / (hi - lo), y, 0])
            rows_.add(VGroup(nm, bar, fin, ten))
        axis = VGroup(*[label(NAMES[p % 12], font_size=15, color=GREY_B).move_to([x0 + W * (p - lo) / (hi - lo), 2.85, 0]) for p in range(lo, hi + 1) if p % 12 in (0, 2, 4, 5, 7, 9, 11)])
        key = VGroup(VGroup(Dot(radius=0.08, color=WHITE), label(r"final", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(side_length=0.15, stroke_width=0, fill_color=EAR, fill_opacity=1), label(r"reciting tone", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15),
                     VGroup(Rectangle(width=0.5, height=0.2, stroke_width=0, fill_color=TUNE, fill_opacity=0.35), label(r"range", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "By about 800, the singers had sorted their chants into eight modes, listed in books called tonaries. "
            "<bookmark mark='a'/> A mode is fixed by three things. Its final, the note the chant ends on: D, E, F or G, "
            "the four maneriae, protus, deuterus, tritus and tetrardus. <bookmark mark='b'/> Its range: an authentic "
            "mode runs from the final up an octave; its plagal partner, from a fourth below the final to a fifth or "
            "sixth above. So each final has two modes, odd and even. <bookmark mark='c'/> And its reciting tone, the "
            "note on which psalm verses are chanted: usually a fifth above the final in the authentic modes, with historical exceptions such as the Phrygian reciting tone, a third or "
            "fourth in the plagal ones, moved up to C wherever it would have fallen on the unstable B. "
            "<bookmark mark='d'/> The Greek names, Dorian, Phrygian and the rest, were borrowed in the Middle Ages and "
            "used differently from ancient Greek theory; the ancient Greeks meant something else by them."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(VGroup(*[r[0] for r in rows_])), FadeIn(VGroup(*[r[2] for r in rows_])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows_], lag_ratio=0.1), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows_], lag_ratio=0.1), FadeIn(key[0]), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[r[0] for r in rows_]), color=WHITE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def psalmody(self):
        items = [
            (r"the monks sang all 150 psalms every week, \ each verse to a short formula: \ a psalm tone", WHITE),
            (r"intonation up to the reciting tone; \ recitation; \ a mediant cadence; \ recitation; \ a termination", WHITE),
            (r"each psalm framed by an antiphon, \ and the antiphon's mode chose the tone", WHITE),
            (r"several endings for each tone, \ the \textit{differentiae}, \ chosen to lead smoothly back into the antiphon", WHITE),
            (r"the modes were practical: \ a singer had to know which formula to use, \ eight times a day", TUNE),
        ]
        rows_scene(self, r"why the modes mattered", items,
                   "Why did the singers need a system at all? <bookmark mark='b'/> Because a monastery sang all hundred "
                   "and fifty psalms every week, each verse to a short melodic formula called a psalm tone. "
                   "<bookmark mark='c'/> A tone rises from the intonation to the reciting tone, recites as many syllables "
                   "as the verse has, dips at the half-verse in a mediant cadence, recites again, and falls in a "
                   "termination. <bookmark mark='d'/> Each psalm was framed by an antiphon, a short chant sung before and "
                   "after it, and the antiphon's mode decided which of the eight tones the psalm was sung to, "
                   "<bookmark mark='e'/> and even which of several endings, the differentiae, so that the last verse led "
                   "smoothly back into the antiphon. <bookmark mark='f'/> So the modes were not an abstraction: a singer "
                   "had to know which formula to use, at every service, eight times a day.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("chant")
        c = clip("chant.modes")
        card = listen_card(r"Two psalm verses, \ both ending on D. \ One is in the first mode \ (authentic: \ it lives above its final); \ "
                           r"one in the second \ (plagal: \ it lives around it). \ Which is the first mode, \ A or B?", width=10.6)
        with self.voiceover(
            "A question for your ears. Two psalm verses, both ending on D. One is in the first mode, authentic, living "
            "above its final; the other in the second, plagal, living around it. Which is the first mode, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        qA = [[p, k, 1.0] for k, p in enumerate(d["quiz"]["A"])]
        qB = [[p, k, 1.0] for k, p in enumerate(d["quiz"]["B"])]
        gA = mroll(qA, width=5.2, height=1.8, lo=60, hi=71, total=len(qA) + 1).move_to(LEFT * 3.2 + DOWN * 0.2)
        gB = mroll(qB, width=5.2, height=1.8, lo=60, hi=71, total=len(qB) + 1).move_to(RIGHT * 3.2 + DOWN * 0.2)
        fl = VGroup(*[DashedLine(g.frame.get_left() + UP * (g.frame.height * (62 - 60) / 11 - g.frame.height / 2), g.frame.get_right() + UP * (g.frame.height * (62 - 60) / 11 - g.frame.height / 2), color=GREY_B, stroke_width=1.5) for g in (gA, gB)])
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb), FadeIn(fl))
        u = d["quiz_unit"]
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"one synthetic voice", kind="synthesized", corner=DL, tag_corner=DR)
            flash(snd, gA.notes, [d["quiz_starts"]["A"] + n[1] * u for n in qA], hot=WHITE, base=TUNE)
            flash(snd, gB.notes, [d["quiz_starts"]["B"] + n[1] * u for n in qB], hot=WHITE, base=TUNE)
            pulse(snd, la, d["quiz_starts"]["A"], d["quiz_starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["quiz_starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"mode 2: \ recites on F", font_size=24, color=BLUE).next_to(gA, DOWN, buff=0.35),
                     label(r"mode 1: \ recites on A", font_size=24, color=TUNE).next_to(gB, DOWN, buff=0.35))
        cap = label(r"the dashed line: \ the final, \ D", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "B is the first mode. It climbs a fifth from D and recites on A, high above its final; A recites on F, only a "
            "third up, and stays close to home. Same final, same scale, a different centre of gravity. That is most of "
            "what a mode is."
        ):
            self.play(FadeIn(ans), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def classifier(self):
        d = load("chant")
        rows_ = text_rows([
            (r"the theorists' rule: \ the last note gives the final; \ the range gives authentic or plagal", WHITE),
            (r"if the range does not decide, \ the more frequent reciting tone does", WHITE),
            (rf"\textit{{Ut queant laxis}}: \ final D, \ range C to A: \ mode {d['ut_mode']}", TUNE),
            (r"the eight psalm tones of the film: \ all eight classified correctly", WHITE),
            (r"but modes were assigned after the chants existed: \ a theory laid over a repertory", EAR),
        ])
        head = label(r"a mode classifier", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The medieval rule for finding a mode is already an algorithm. <bookmark mark='a'/> Read the last note: "
            "that is the final, and it fixes the pair. Read the range: if the chant goes well below its final it is "
            "plagal; if it climbs a sixth or more above it, authentic. <bookmark mark='b'/> Where the range does not "
            "decide, count which of the two reciting tones the chant leans on. <bookmark mark='c'/> Ut queant laxis "
            f"ends on D and dips to the C below it: mode {say(d['ut_mode'])}. <bookmark mark='d'/> The eight psalm "
            "tones of this film all come out right. <bookmark mark='e'/> But be careful what that proves. Many chants "
            "are older than the system, and singers sometimes bent them to fit their assigned mode. The modes were a "
            "theory laid over a repertory, which is why some chants sit awkwardly in any of them; chapter thirteen "
            "returns to classifiers trained on thousands of chants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
