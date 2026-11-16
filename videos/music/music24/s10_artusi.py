from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Artusi(SoundScene):
    def construct(self):
        chapter(self, 9, r"The second practice", r"Who decides what a dissonance may do?", extra=((1600, r"Artusi's attack"),))
        self.quarrel()
        self.cruda()
        self.counted()
        self.reply()

    # ------------------------------------------------------------------
    def quarrel(self):
        items = [
            (r"1600, \ Venice: \ Giovanni Maria Artusi, \ \textit{On the imperfections of modern music}", WHITE),
            (r"he quotes passages from madrigals not yet printed, \ without naming the composer", WHITE),
            (r"the composer was Monteverdi; \ one madrigal was \textit{Cruda Amarilli}", TUNE),
            (r"the charge: \ dissonances struck without preparation, \ left by leap, \ against every rule of Zarlino", WHITE),
            (r"Artusi was right about the facts", GREY_A),
        ]
        rows_scene(self, r"an attack in print", items,
                   "In 1600 a canon of Bologna, Giovanni Maria Artusi, published a dialogue on the imperfections of modern "
                   "music. <bookmark mark='b'/> In it he quoted passages from madrigals that had been sung but not yet "
                   "printed, without naming their composer. <bookmark mark='c'/> The composer was Monteverdi, and one of "
                   "the madrigals was Cruda Amarilli, cruel Amaryllis. <bookmark mark='d'/> The charge was precise: "
                   "dissonances struck without preparation and left by leap, against every rule of Zarlino, the great "
                   "theorist of the age. <bookmark mark='e'/> And about the facts, as the numbers will show, Artusi was "
                   "right.")

    # ------------------------------------------------------------------
    def cruda(self):
        d = load("cruda")
        c = clip("cruda.amarilli")
        vs = d["voices"]
        g = voices_roll(vs, width=11.6, height=3.6, colors=[TUNE, BLUE, EAR, "#A3E635", GREY_A, GREY_B], bar_h=0.1).move_to(DOWN * 0.35)
        marks = VGroup()
        for j, t in d["marks"]:
            x = g.frame.get_left()[0] + g.frame.width * t / g.total
            marks.add(Triangle(color=RED, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI).move_to([x, g.frame.get_top()[1] + 0.15, 0]))
        head = label(r"Monteverdi, \ \textit{Cruda Amarilli} \ (Book 5, \ 1605): \ the opening", font_size=24, color=GREY_A).to_edge(UP, buff=0.9)
        cap = label(r"red: \ dissonances the program cannot explain as passing, \ neighbour, \ suspension or cambiata", font_size=20, color=RED).next_to(g, DOWN, buff=0.3)
        with self.voiceover(
            "Here is the opening of Cruda Amarilli, sung from the encoding. The red marks are where the program finds a "
            "dissonance it cannot explain by any of this simplified classifier’s treatment categories. The passage Artusi quoted comes near the end of "
            "this excerpt, where the top voice, on the words ahi lasso, alas, strikes a ninth and a seventh against the "
            "bass without preparation and leaves them by leap."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(marks), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Monteverdi, \ \textit{Cruda Amarilli}", detail=r"from the encoding, \ synthetic voices", kind="synthesized", corner=UL, tag_corner=UR)
            flash_voices(snd, g, vs, 0.0, d["quarter"], colors=[TUNE, BLUE, EAR, "#A3E635", GREY_A, GREY_B])
            flash(snd, list(marks), [t * d["quarter"] for _, t in d["marks"]], hot=WHITE, base=RED, fade=0.6)
            cursor(snd, g, 0.0, d["quarter"])
        with self.voiceover(
            f"The program marks {say(len(d['marks']))} unexplained dissonances in these sixteen bars, all in the top "
            "voice. The two near the end fall in the passage Artusi quoted: the soprano arrives on notes that clash with "
            "the bass, with nothing held over to prepare them. To Artusi this was "
            "simply wrong, a schoolboy's error in a famous composer. To Monteverdi it was the word alas, sung as a cry."
        ):
            self.play(Indicate(marks, color=WHITE, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("dissonance")["groups"]
        names = list(d)
        tags = [r"Palestrina", r"Book 3, \ 1592", r"Book 4, \ 1603", r"Book 5, \ 1605"]
        vals = [100 * d[n]["shares"]["free"] for n in names]
        bars = VGroup()
        for j, v in enumerate(vals):
            h = 3.0 * v / 50
            r = Rectangle(width=1.1, height=max(h, 0.03), stroke_width=0, fill_color=TUNE if j == 0 else EAR, fill_opacity=0.9).move_to([1.6 * j, h / 2, 0])
            bars.add(VGroup(r, label(rf"{v:.1f}", font_size=24, color=WHITE).next_to(r, UP, buff=0.1), label(tags[j], font_size=19, color=GREY_A).next_to(r, DOWN, buff=0.25)))
        bars.move_to(LEFT * 2.0 + DOWN * 0.4)
        t = label(r"free dissonances, \ in 100 dissonances against the bass", font_size=22, color=GREY_A).to_edge(UP, buff=0.6)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"Palestrina: \ {d[names[0]]['total']:,} dissonances".replace(",", "{,}"), WHITE),
            (rf"Monteverdi: \ {sum(d[n]['total'] for n in names[1:]):,} in 48 madrigals".replace(",", "{,}"), WHITE),
            (rf"suspensions: \ {100 * d[names[0]]['shares']['suspension']:.0f} in 100, \ then {100 * d[names[1]]['shares']['suspension']:.0f}, \ {100 * d[names[2]]['shares']['suspension']:.0f}, \ {100 * d[names[3]]['shares']['suspension']:.0f}", WHITE),
            (r"a new rule, \ not no rule", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "Count the whole of the three books against Palestrina. <bookmark mark='a'/> In Palestrina's Masses, "
            f"{d[names[0]]['shares']['free'] * 100:.1f} dissonances in a hundred are free. <bookmark mark='b'/> In "
            f"Monteverdi's third book, from 1592, {say(round(vals[1]))}. In the fourth, {say(round(vals[2]))}; in the "
            f"fifth, {say(round(vals[3]))}. <bookmark mark='c'/> And the suspension, nearly a third of Palestrina's "
            "dissonances, almost disappears. <bookmark mark='d'/> These aggregate differences do not by themselves establish a complete compositional rule system. Monteverdi's dissonances "
            "follow other rules, of the words and of the bass line, and the next generation made those rules into the "
            "harmony of the Baroque."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[1:]], lag_ratio=0.4), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reply(self):
        items = [
            (r"1605: \ Monteverdi's preface to Book 5 promises a reply, \ `The second practice'", WHITE),
            (r"1607: \ his brother Giulio Cesare explains it: \ the first practice is Zarlino's and Palestrina's", WHITE),
            (r"in the second, \ `the words are the mistress of the harmony, \ not its servant'", TUNE),
            (r"both practices are legitimate: \ a style chosen for a purpose", WHITE),
            (r"Part 25: \ the Baroque makes the second practice the norm", GREY_A),
        ]
        rows_scene(self, r"the reply", items,
                   "Monteverdi answered in the preface to his fifth book, in 1605, promising a treatise to be called The "
                   "second practice. <bookmark mark='b'/> He never wrote it, but in 1607 his brother Giulio Cesare "
                   "explained: the first practice is the style of Zarlino's rules and Palestrina's Masses, "
                   "<bookmark mark='c'/> in which the harmony governs the words; in the second, the words are the "
                   "mistress of the harmony, not its servant. <bookmark mark='d'/> Both are legitimate; a composer chooses "
                   "one for a purpose. <bookmark mark='e'/> The next part follows the second practice into the Baroque, "
                   "where it became the norm.")
