from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Learned(SoundScene):
    def construct(self):
        chapter(self, 2, r"Where the ranking comes from", r"Why those ratings?")
        self.counts()
        self.raga()
        self.children()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("profile")
        kk = np.array(d["kk_major"])
        cm = np.array(d["corpus_major"])
        top = note_bars(kk, NAMES12, width=6.0, height=1.9, color=WEAK, hot=(0, 4, 7), hot_color=TUNE, show_values=False, font_size=18, top=7.0).move_to(LEFT * 3.5 + UP * 0.9)
        bot = note_bars(100 * cm, NAMES12, width=6.0, height=1.9, color=WEAK, hot=(0, 4, 7), hot_color=BLUE, show_values=False, font_size=18, top=30.0).move_to(LEFT * 3.5 + DOWN * 2.0)
        lt = label(r"listeners' ratings \ (1982)", font_size=22, color=TUNE).next_to(top, UP, buff=0.15)
        lb = label(r"share of time on each note, \ in our 54 tunes", font_size=22, color=BLUE).next_to(bot, UP, buff=0.15)
        g = axes([0, 30], [1.5, 7], x_length=4.2, y_length=3.6, xlabel=r"\% of the time in the tunes", ylabel=r"rating", xticks=[0, 10, 20, 30], yticks=[2, 4, 6], font_size=20).move_to(RIGHT * 3.8 + DOWN * 0.5)
        pts = VGroup(*[Dot(g.ax.c2p(100 * cm[k], kk[k]), radius=0.06, color=TUNE if k in (0, 4, 7) else WHITE) for k in range(12)])
        rl = label(rf"correlation: \ $r = {d['r']:.2f}$", font_size=32, color=TUNE).next_to(g, UP, buff=0.5)
        with self.voiceover(
            "Why those ratings, and not some others? Here is a clue. Take the fifty-four tunes of Part "
            "14, put them all in C, and measure how much of the time each of the twelve notes is "
            "sounding. <bookmark mark='a'/> Now set that beside the listeners' ratings. The tall bars "
            "are the same bars. <bookmark mark='b'/> Plot one against the other, and the correlation is "
            f"{say(d['r'], 2)}. The notes that listeners say fit best are the notes that tunes use most. "
            "Krumhansl found the same thing in counts of Schubert songs and Mozart arias. The profile "
            "is a statistical summary of the music itself."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lt))
            vo.wait_until("a")
            self.play(FadeIn(bot), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(pts), FadeIn(rl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def raga(self):
        steps = VGroup(label(r"1984: \ listeners in the United States who had never heard Indian music", font_size=26, color=WHITE),
                       label(r"short passages of north Indian ragas, \ then probe tones", font_size=26, color=WHITE),
                       label(r"their ratings followed how long each note had sounded in what they had just heard", font_size=26, color=TUNE),
                       label(r"and matched the ratings of listeners trained in the tradition", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        cap = label(r"a key is learned, \ and the learning is fast", font_size=34, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That could be a coincidence, or it could be cause and effect. An experiment in 1984 "
            "decided it. Mary Castellano, Jamshed Bharucha and Krumhansl took listeners who had never "
            "heard Indian classical music, <bookmark mark='a'/> played them short passages from ragas, "
            "and ran the probe-tone experiment in that music. <bookmark mark='b'/> The ratings these "
            "newcomers gave followed how long each note had sounded in the passage they had just heard; "
            "<bookmark mark='c'/> and they agreed closely with the ratings of listeners who had grown up "
            "with the tradition. <bookmark mark='d'/> So the hierarchy is not built into the ear, and it "
            "is not a rule that anyone was taught. Listeners count, without knowing that they count, "
            "and a short passage is enough to begin."
        ) as vo:
            self.play(FadeIn(steps[0]))
            for mark, s in zip("abc", steps[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(s))
            vo.wait_until("d")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def children(self):
        ages = VGroup(VGroup(label(r"8 months", font_size=32, color=TUNE), label(r"hears a changed note equally well \\ whether or not it stays in the key", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2),
                      VGroup(label(r"about 5 years", font_size=32, color=TUNE), label(r"knows which notes belong to the key", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2),
                      VGroup(label(r"about 7 years", font_size=32, color=TUNE), label(r"knows which chord should come next", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2),
                      VGroup(label(r"adults", font_size=32, color=TUNE), label(r"miss a changed note that stays in the key: \\ the key hides it", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2)).arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.9)).move_to(DOWN * 0.3)
        line = Line(LEFT * 5.5 + UP * 2.2, RIGHT * 5.5 + UP * 2.2, color=GREY_D, stroke_width=2)
        head = label(r"how a child acquires a key \ (Trainor and Trehub, \ 1992 and 1994)", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "You can watch the learning happen in children. Laurel Trainor and Sandra Trehub played a "
            "short melody over and over, and now and then changed one note. <bookmark mark='a'/> "
            "Infants of eight months noticed the change equally well whether the new note stayed inside "
            "the key or went outside it. <bookmark mark='b'/> Adults noticed the outside note easily, "
            "and often missed the inside one: the key hid it from them. In this one test the babies "
            "did better than their parents, because they had no key to be fooled by. "
            "<bookmark mark='c'/> By about five, children know which notes belong to a key; by about "
            "seven, they know which chord ought to come next. Nobody teaches them. It is the same "
            "kind of learning as a first language, and it comes from the same thing: years of listening."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(ages[0]))
            vo.wait_until("b")
            self.play(FadeIn(ages[3]))
            vo.wait_until("c")
            self.play(FadeIn(ages[1]), FadeIn(ages[2]))
        self.wait(0.4)
        self.clear_scene()
