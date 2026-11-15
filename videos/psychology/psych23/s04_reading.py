from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403

SEG = {  # segment endpoints on a 0..1 by 0..2 letter box, for drawing the 14-segment font
    0: ((0, 2), (1, 2)), 1: ((0, 2), (0, 1)), 2: ((1, 2), (1, 1)), 3: ((0, 1), (0, 0)), 4: ((1, 1), (1, 0)),
    5: ((0, 0), (1, 0)), 6: ((0, 1), (0.5, 1)), 7: ((0.5, 1), (1, 1)), 8: ((0.5, 2), (0.5, 1)),
    9: ((0.5, 1), (0.5, 0)), 10: ((0, 2), (0.5, 1)), 11: ((1, 2), (0.5, 1)), 12: ((0, 0), (0.5, 1)),
    13: ((1, 0), (0.5, 1)),
}


def segment_letter(segs, origin, size: float = 0.5, color=WORD, faint: bool = False) -> VGroup:
    """A letter drawn in the 14-segment font: the segments that are on, with the rest faint."""
    o = np.asarray(origin, float)
    g = VGroup()
    for s, ((x0, y0), (x1, y1)) in SEG.items():
        on = s in segs
        g.add(Line(o + size * np.array([x0, y0, 0]), o + size * np.array([x1, y1, 0]),
                   color=color if on else GREY_D, stroke_width=5 if on else 1.5,
                   stroke_opacity=1 if on else (0.25 if faint else 0.4)))
    return g


class Reading(VoiceoverScene):
    def construct(self):
        self.card()
        self.reicher()
        self.model()
        self.run_model()

    def card(self):
        card = chapter_card(3, r"Recognizing a word", r"Why is a letter easier to see inside a word?",
                            lit={1969: r"Reicher", 1970: r"Wheeler", 1981: r"McClelland \& Rumelhart"},
                            part=PART, scale=("mind", "circuit"), marr=("how",))
        with self.voiceover("Chapter three. Recognizing a word."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def reicher(self):
        head = heading(r"The word superiority effect")
        frames = VGroup()
        for k, (txt, col) in enumerate(((r"WORK", WORD), (r"\ \ \ K", WORD), (r"\#\#\#\#", GREY_B),
                                        (r"\_\_\_K \ \ or \ \ \_\_\_D \ ?", MODEL))):
            box = RoundedRectangle(corner_radius=0.1, width=2.5, height=1.2, stroke_color=GREY_C, stroke_width=2)
            t = label(txt, font_size=34 if k < 3 else 24, color=col).move_to(box)
            frames.add(VGroup(box, t))
        frames[0].move_to([-4.9, 1.4, 0])
        frames[1].move_to([-4.9, -0.2, 0])
        frames[2].move_to([-1.9, 0.6, 0])
        frames[3].move_to([1.3, 0.6, 0])
        lab = VGroup(label(r"word", font_size=18, color=GREY_A).next_to(frames[0], UP, buff=0.08),
                     label(r"letter alone", font_size=18, color=GREY_A).next_to(frames[1], DOWN, buff=0.08),
                     label(r"a mask", font_size=18, color=GREY_A).next_to(frames[2], UP, buff=0.08),
                     label(r"which letter was last?", font_size=18, color=GREY_A).next_to(frames[3], UP, buff=0.08))
        arrows = VGroup(Arrow(frames[0].get_right(), frames[2].get_left(), buff=0.1, color=GREY_C, stroke_width=2),
                        Arrow(frames[1].get_right(), frames[2].get_left(), buff=0.1, color=GREY_C, stroke_width=2),
                        Arrow(frames[2].get_right(), frames[3].get_left(), buff=0.1, color=GREY_C, stroke_width=2))
        rows = rows_of([
            (r"Reicher, \ 1969, \ and Wheeler, \ 1970: \ a brief display, \ then a mask, \ then a choice between two "
             r"letters", WHITE),
            (r"both choices make a word \ (WORK, \ WORD), \ so knowing words cannot help you guess", RULE),
            (r"yet the letter is reported more accurately inside the word than shown alone", MODEL),
            (r"seeing the whole helps you see the part: \ how?", STAT),
        ], 3.9, 22, 0.33).move_to([5.0, 0.2, 0])
        tag = historical_tag(r"Reicher (1969); \ Wheeler (1970)")
        with self.voiceover(
            "Here is a puzzle about reading. <bookmark mark='a'/> In 1969 Gerald Reicher, and in 1970 Daniel "
            "Wheeler, flashed a word, such as work, or a single letter, such as K, for a fraction of a second. A "
            "mask of hash marks followed. Then people chose which letter had been in the last position: K or D? "
            "<bookmark mark='b'/> The trick is that both choices make a word, work and word, so knowing English "
            "can't help you guess. <bookmark mark='c'/> Yet people reported the letter more accurately when it was "
            "inside a word than when it was shown alone. <bookmark mark='d'/> Seeing the whole helped them see the "
            "part. How can that be, if you read a word by first reading its letters?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(frames[0]), FadeIn(frames[1]), FadeIn(lab[0]), FadeIn(lab[1]), FadeIn(rows[0]))
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(frames[2]), FadeIn(lab[2]))
            self.play(GrowArrow(arrows[2]), FadeIn(frames[3]), FadeIn(lab[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def model(self):
        d = load("ia")
        head = heading(r"Derivation: \ the interactive activation model")
        from explainer.psychology.psyche.language import SEGMENTS
        word = "WORK"
        xc, xl = -2.9, -6.8
        feats = VGroup(*[segment_letter(SEGMENTS[c], [xc - 1.65 + 1.0 * k, -3.0, 0], 0.4) for k, c in
                         enumerate(word)])
        letters = VGroup(*[word_chip(c, SOUND, 28, width=0.75).move_to([xc - 1.5 + 1.0 * k, -0.75, 0]) for k, c in
                           enumerate(word)])
        words = VGroup(*[word_chip(w, WORD, 28) for w in ("WORK", "WORD", "WORE", "FORK")]).arrange(RIGHT, buff=0.2)
        words.move_to([xc, 1.3, 0])
        lvl = VGroup(label(r"features", font_size=24, color=GREY_A).move_to([xl, feats.get_center()[1], 0],
                                                                          aligned_edge=LEFT))
        llab = label(r"letters", font_size=24, color=GREY_A).move_to([xl, -0.75, 0], aligned_edge=LEFT)
        wlab = VGroup(label(r"words", font_size=24, color=GREY_A),
                      label(rf"{num(d['lexicon'])} from the novels", font_size=18, color=GREY_B)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([xl, 1.3, 0], aligned_edge=LEFT)
        wlab.next_to(words, UP, buff=0.2).align_to(words, LEFT)
        up = VGroup(*[Arrow([xc - 0.6, feats.get_top()[1], 0], [xc - 0.6, letters.get_bottom()[1], 0], buff=0.08,
                            color=MODEL, stroke_width=3),
                      Arrow([xc - 0.6, letters.get_top()[1], 0], [xc - 0.6, words.get_bottom()[1], 0], buff=0.08,
                            color=MODEL, stroke_width=3)])
        down = Arrow([xc + 0.6, words.get_bottom()[1], 0], [xc + 0.6, letters.get_top()[1], 0], buff=0.08,
                     color=RULE, stroke_width=3)
        eqs = VGroup(
            MathTex(r"n_i = \sum_j \alpha_{ij} [a_j]_+ - \sum_j \gamma_{ij} [a_j]_+", font_size=34),
            MathTex(r"\Delta a_i = \begin{cases} n_i (M - a_i) & n_i > 0 \\ n_i (a_i - m) & n_i \le 0 \end{cases} "
                    r"- \theta (a_i - r_i)", font_size=32, color=MODEL),
        ).arrange(DOWN, buff=0.35).move_to([3.7, 1.7, 0])
        rows = rows_of([
            (r"three levels: \ features, \ letters, \ words; \ consistent units excite, \ inconsistent ones inhibit",
             WHITE),
            (r"within the word level, \ every word inhibits every other: \ they compete", WORD),
            (r"and words send activation \emph{back} to their letters: \ the arrow that explains Reicher", RULE),
            (r"parameters as McClelland and Rumelhart published them; \ common words rest a little higher", GREY_A),
        ], 5.8, 23, 0.32).move_to([3.7, -1.35, 0])
        ptag = psyche_tag(r"\texttt{language.InteractiveActivation}")
        with self.voiceover(
            "In 1981 James McClelland and David Rumelhart answered with a network. <bookmark mark='a'/> It has three "
            "levels: features of letters, such as a vertical stroke on the left; letters, in each of four positions; "
            "and words. Units that are consistent excite each other: a vertical stroke excites K, and K in the "
            "fourth position excites work. Inconsistent units inhibit. <bookmark mark='b'/> Within the word level, "
            "every word inhibits every other, so words compete. <bookmark mark='c'/> And words send activation back "
            "down to their letters. That downward arrow is the key. <bookmark mark='d'/> Each unit sums its "
            "excitation and inhibition from the units that are active, moves its activation toward its maximum or "
            "minimum in proportion, and decays toward rest. We use the parameters McClelland and Rumelhart "
            "published, with common words resting a little higher than rare ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(feats), FadeIn(lvl))
            vo.wait_until("a")
            self.play(FadeIn(letters), FadeIn(llab), GrowArrow(up[0]), FadeIn(words), FadeIn(wlab), GrowArrow(up[1]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(words, color=WORD))
            vo.wait_until("c")
            self.play(GrowArrow(down), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eqs[0]), Write(eqs[1]), FadeIn(rows[3]))
        self.clear_scene()

    def run_model(self):
        d = load("ia")
        head = heading(r"Psyche reads WORK")
        t = np.arange(len(d["word_K"]))
        A = axes([0, 40], [-0.2, 1.0], x_length=5.6, y_length=2.6, xticks=[0, 12, 20, 30, 40],
                 yticks=[-0.2, 0, 0.5, 1.0], yfmt=lambda v: f"{v:.1f}", xlabel=r"cycles", ylabel=r"activation",
                 center=[-3.2, 1.3, 0], font_size=16)
        mask = DashedLine(A.ax.c2p(12, -0.2), A.ax.c2p(12, 1.0), color=GREY_B)
        mlab = label(r"mask", font_size=16, color=GREY_B).next_to(A.ax.c2p(12, 1.0), UP, buff=0.05)
        cw = curve(A.ax, t, d["word_K"], WORD, 3)
        ca = DashedVMobject(curve(A.ax, t, d["alone_K"], SOUND, 3), num_dashes=30)
        cwork = curve(A.ax, t, d["word_WORK"], RULE, 2.5)
        key = legend([(WORD, r"K, \ inside WORK"), (SOUND, r"K, \ alone"), (RULE, r"the word unit WORK")],
                     font_size=16).move_to(A.ax.c2p(30, 0.75))
        B = axes([4, 16], [0.5, 1.0], x_length=5.0, y_length=1.6, xticks=[4, 8, 12, 16], yticks=[0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:.2f}", xlabel=r"cycles before the mask", ylabel=r"correct, \ K or D",
                 center=[-3.2, -2.45, 0], font_size=15)
        aw = curve(B.ax, d["durations"], d["acc_word"], WORD, 3)
        aa = DashedVMobject(curve(B.ax, d["durations"], d["acc_alone"], SOUND, 3), num_dashes=24)
        gain = 100 * (d["acc_word"][-1] - d["acc_alone"][-1])
        rows = rows_of([
            (r"the letters of WORK activate the word WORK, \ and soon WORK sends activation back to its K", WHITE),
            (r"so K inside the word rises faster and higher than K alone, \ before the mask arrives", WORD),
            (rf"the forced choice is more often right: \ up to {gain:.0f} points better in the word, \ none in a "
             r"non-word like OWRK", MODEL),
            (r"smaller than in people, \ but the cause is visible: \ knowledge of words flows down into seeing letters",
             STAT),
        ], 5.4, 23, 0.36).move_to([3.7, 0.0, 0])
        ptag = psyche_tag(r"\texttt{language.InteractiveActivation.forced\_choice}")
        with self.voiceover(
            "Now let Psyche read. <bookmark mark='a'/> When work is shown, its four letters activate the word work. "
            "Within a few cycles work is the most active word, and it begins sending activation back to its own "
            "letters, including the K. <bookmark mark='b'/> So the K inside the word rises faster and higher than a K "
            "shown alone, and it is higher when the mask arrives and starts to wipe the letters out. "
            f"<bookmark mark='c'/> Read out as Reicher's two-way choice, the word condition is up to {gain:.0f} points "
            "more accurate, and a non-word like O W R K gives no advantage at all. <bookmark mark='d'/> The effect is "
            "smaller than in people, but its cause is plain to see: knowledge of words flows down into the seeing of "
            "letters. Perception is not only bottom up, a theme from Part 14 that returns at every level of language."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(A), Create(mask), FadeIn(mlab))
            vo.wait_until("a")
            self.play(Create(cwork), FadeIn(key[2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cw), Create(ca), FadeIn(key[0]), FadeIn(key[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(aw), Create(aa), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
