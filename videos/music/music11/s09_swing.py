from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Swing(SoundScene):
    def construct(self):
        chapter(self, 8, r"Swing", r"What does the page not say about eighth notes?", extra=((2002, r"swing ratios measured"),))
        self.pairs()
        self.measured()
        self.unwritten()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("swing")
        c = clip("swing.three")
        beat = d["beat"]
        rows = VGroup()
        for r, times, lg, sh in zip(d["ratios"], d["times"], d["long_ms"], d["short_ms"]):
            tk = ticks(times[:8], 0.0, 4 * beat, width=7.0, height=0.55, color=TUNE, levels=[1.0 if j % 2 == 0 else 0.6 for j in range(8)])
            name = label(rf"{r:g} : 1", font_size=34, color=TUNE).next_to(tk, LEFT, buff=0.5)
            ms = label(rf"{lg:.0f} ms, \ {sh:.0f} ms", font_size=24, color=GREY_A).next_to(tk, RIGHT, buff=0.4)
            rows.add(VGroup(tk, name, ms))
        rows.arrange(DOWN, buff=0.9).move_to(UP * 0.5)
        for r in rows:
            r.shift(RIGHT * (rows[0][0].base.get_x() - r[0].base.get_x()))
        head = label(r"two eighth notes to the beat: \ long, \ short", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        heads = [r[0].head() for r in rows]
        with self.voiceover(
            "There is one more way to cut a beat, and no notation writes it. In jazz, a pair of eighth "
            "notes is not played evenly. The first is longer and the second shorter: the eighths swing. "
            "How much longer is the swing ratio. <bookmark mark='a'/> One to one is even eighths. "
            "<bookmark mark='b'/> Two to one is the triplet feel that the textbooks describe. "
            "<bookmark mark='c'/> Three to one is a dotted rhythm. Listen to all three on a hi-hat, over "
            "the same four beats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0][0]))
            self.wait(5.0)
            self.play(*[m.animate(rate_func=there_and_back).shift(RIGHT * 0.25) for m in rows[0][0].marks[1::2]], run_time=1.6)
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.add(*heads)
        with self.listen(c) as snd:
            window(snd, r"even, \ two to one, \ three to one", kind="synthesized", detail=r"hi-hat; \ modelled drums", corner=DL, tag_corner=DR)
            for k, (r, h) in enumerate(zip(rows, heads)):
                t0 = d["starts"][k]
                pulse(snd, r[1], t0, t0 + 8 * beat, buff=0.1)
                snd.drive(h, lambda m, t, t0=t0, tk=r[0]: m.set_x(tk.x_of(((t - t0) % (4 * beat)) if t0 <= t < t0 + 8 * beat else 0.0)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("swing")
        g = axes([100, 335], [0.8, 3.8], x_length=9.0, y_length=3.4, xlabel=r"tempo (beats to the minute)", ylabel=r"swing ratio", xticks=[100, 150, 200, 250, 300], yticks=[1, 2, 3], font_size=22).move_to(UP * 0.5 + LEFT * 0.4)
        cv = curve_from(g, d["bpm"], d["ratio"], TUNE, stroke_width=4)
        two = VGroup(Dot(g.ax.c2p(d["triplet_bpm"], 2.0), radius=0.09, color=WHITE), label(rf"two to one, \ at {d['triplet_bpm']:.0f} only", font_size=24, color=WHITE))
        two[1].next_to(two[0], UR, buff=0.12)
        one = VGroup(Dot(g.ax.c2p(d["straight_bpm"], 1.0), radius=0.09, color=WHITE), label(r"even", font_size=24, color=WHITE))
        one[1].next_to(one[0], UP, buff=0.15)
        rule = label(r"if the short note always lasts 100 ms: \ \ ratio $= \dfrac{\text{beat} - 100 \text{ ms}}{100 \text{ ms}}$", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.6)
        card = history_card(2002, r"Anders Friberg and Andreas Sundstr\"om", r"measured on records: \ about 3.5 to 1 at slow tempos, \ 1 to 1 at the fastest; \ the short note near 100 ms", width=5.6, font_size=22).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Which ratio is the real one? In 2002 two Swedish researchers measured it on jazz records, "
            "from the drummers' ride cymbals. The answer was: all of them. <bookmark mark='a'/> At slow "
            "tempos the ratio was as large as three and a half to one. At the fastest it was one to one: "
            "even eighths. Two to one, the triplet feel, turned up only at one tempo in the middle. "
            "<bookmark mark='b'/> And they noticed why. From medium tempos upward the short note stayed "
            "about the same length, a tenth of a second, whatever the tempo. Take that as a rule and the "
            "ratio follows by subtraction. <bookmark mark='c'/> A tenth of a second is the floor we met "
            f"in chapter one. On this curve the ratio is exactly two at {say(d['triplet_bpm'])} beats to "
            f"the minute, and falls to one at {say(d['straight_bpm'])}. Swing is not a ratio. It is a "
            "short note, played as short as a note can usefully be."
        ) as vo:
            self.play(FadeIn(g), FadeIn(card))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(two), FadeIn(one))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unwritten(self):
        d = load("swing")
        st = VGroup(*[sticks(2, width=1.2, height=0.8) for _ in range(4)]).arrange(RIGHT, buff=0.5).move_to(UP * 1.5)
        word = Text("Swing", font="FreeSerif", slant="ITALIC", weight="BOLD", font_size=36).next_to(st, UP, buff=0.3).align_to(st, LEFT)
        rows = VGroup(label(r"the page: \ eight even eighth notes, \ and one word", font_size=28, color=GREY_A),
                      label(rf"the player: \ which ratio, \ at this tempo, \ in this band; \ a few tens of milliseconds", font_size=28, color=TUNE),
                      label(r"in Part 10's terms: \ the page keeps the notes; \ the tradition keeps the rest", font_size=28, color=EAR)).arrange(DOWN, buff=0.4).move_to(DOWN * 1.3)
        with self.voiceover(
            "On the page a swung line looks like this: even eighth notes, and the word swing at the top. "
            "<bookmark mark='a'/> Everything we have just measured is left to the player: which ratio, "
            "at this tempo, with this band, and how the soloist leans against the drummer. The "
            "differences are a few tens of milliseconds, far finer than any notation in Part 10 "
            "records. <bookmark mark='b'/> It is that part's lesson again. The page keeps the notes. A "
            "living tradition keeps the rest, and you learn it by listening."
        ) as vo:
            self.play(FadeIn(st), FadeIn(word), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
