from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Additive(SoundScene):
    def construct(self):
        chapter(self, 7, r"Long beats and short", r"Must the beats of a bar be equal?", extra=((1951, r"Br\u{a}iloiu on \textit{aksak}"),), spoken="Chapter seven. Long beats and short.")
        self.seven()
        self.count()

    # ------------------------------------------------------------------
    def seven(self):
        d = load("additive")
        c = clip("additive.seven")
        cols = VGroup()
        for comp in d["sevens"]:
            starts = list(np.concatenate([[0], np.cumsum(comp)[:-1]]).astype(int))
            nk = necklace(7, onsets=starts, radius=1.25, color=TUNE)
            cols.add(VGroup(nk, MathTex(" + ".join(str(x) for x in comp), font_size=44)).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=1.1).move_to(UP * 0.5)
        seven = VGroup(*[Dot(radius=0.16, color=WEAK) for _ in range(7)]).arrange(RIGHT, buff=0.7).move_to(UP * 0.8)
        no = label(r"seven pulses: \ no way to cut them into equal beats", font_size=30, color=BAD).next_to(seven, DOWN, buff=0.7)
        with self.voiceover(
            "So far every beat in a bar has been the same length. It need not be. Take seven quick "
            "pulses to the bar. Seven is prime: it cannot be cut into equal beats. But it can be cut into "
            "beats of two pulses and beats of three. <bookmark mark='a'/> Two, two, three. "
            "<bookmark mark='b'/> Two, three, two. <bookmark mark='c'/> Three, two, two. A bar of three "
            "beats, one of them half as long again as the others. In Turkish the word for it is aksak, "
            "limping, and through the Balkans, Turkey and beyond, people dance to it without a thought. "
            "Listen to the three sevens. The drums mark the beats; the wood block ticks all seven pulses."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in seven], lag_ratio=0.15), run_time=2.0)
            self.wait(4.0)
            self.play(FadeIn(no))
            vo.wait_until("a")
            self.play(FadeOut(seven), FadeOut(no))
            for mark, col in zip("abc", cols):
                vo.wait_until(mark)
                self.play(FadeIn(col), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"seven, \ three ways", detail=r"drums and wood block, \ modelled", corner=DL, tag_corner=DR)
            for k, col in enumerate(cols):
                t0 = d["starts"][k]
                end = t0 + 28 * d["pulse"]
                pulse(snd, col[1], t0, end, buff=0.12)
                snd.drive(col[0].hand, col[0].turn(7 * d["pulse"], t0, end))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("additive")
        ns = [5, 7, 8, 9, 11, 12]
        table = VGroup()
        for n in ns:
            table.add(VGroup(label(str(n), font_size=34, color=GREY_A), label(str(d["counts"][str(n)]), font_size=40, color=TUNE)).arrange(DOWN, buff=0.3))
        table.arrange(RIGHT, buff=0.9)
        heads = VGroup(label(r"pulses in the bar", font_size=24, color=GREY_B), label(r"ways to fill it with twos and threes", font_size=24, color=GREY_B))
        heads[0].next_to(table, LEFT, buff=0.5).align_to(table[0][0], UP)
        heads[1].next_to(table, LEFT, buff=0.5).align_to(table[0][1], DOWN)
        VGroup(table, heads).move_to(UP * 1.9)
        rule = MathTex(r"a(n) = a(n-2) + a(n-3)", font_size=44).move_to(UP * 0.2)
        why = label(r"a bar begins with a two, \ and $n - 2$ pulses are left; \ or with a three, \ and $n - 3$ are", font_size=26, color=GREY_A).next_to(rule, DOWN, buff=0.3)
        dances = rows_card([
            (r"7 = 2 + 2 + 3", r"r\u{a}chenitsa, \ Bulgaria"),
            (r"7 = 3 + 2 + 2", r"lesnoto, \ Macedonia"),
            (r"9 = 2 + 2 + 2 + 3", r"daichovo, \ Bulgaria"),
            (r"11 = 2 + 2 + 3 + 2 + 2", r"kopanitsa, \ Bulgaria"),
        ], left=-5.4, text_left=-0.6, top=-1.35, step=0.55, name_size=26, text_size=24)
        with self.voiceover(
            "How many such meters are there? Monochord counts every way to fill a bar with twos and "
            "threes. <bookmark mark='a'/> Five pulses: two ways. Seven: three. Nine: five. Twelve: "
            "twelve. <bookmark mark='b'/> The numbers obey a simple rule. A bar must begin with a two or "
            "a three; after a two there are n minus two pulses left to fill, and after a three, n minus "
            "three. So each count is the sum of two earlier ones. <bookmark mark='c'/> And these are not "
            "curiosities. Each of these is, as it is usually counted, the meter of a dance that whole "
            "villages know. Bartok, who collected them, called it Bulgarian rhythm. Notice the ratio "
            "of a long beat to a short one: three to two, again."
        ) as vo:
            self.play(FadeIn(heads))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in table], lag_ratio=0.45), run_time=5.0)
            vo.wait_until("b")
            self.play(FadeIn(rule), FadeIn(why))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in dances], lag_ratio=0.4), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
