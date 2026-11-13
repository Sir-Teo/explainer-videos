from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.zhu()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        d = load("pump")
        c = clip("pump.rounds")
        rows = d["rows"]
        names = {"C": r"C", "A": r"A minor", "D": r"D minor", "G": r"G"}
        grid = VGroup()
        for r in range(4):
            row = VGroup(*[label(names[rows[1 + 4 * r + j]["root"]] if j < 4 else "", font_size=30, color=GREY_D) for j in range(4)])
            for j, x in enumerate(row):
                x.move_to(LEFT * 5.2 + RIGHT * 2.0 * j + UP * (1.9 - 0.85 * r))
            grid.add(row)
        first = label(r"C", font_size=30, color=GREY_D).move_to(LEFT * 5.2 + LEFT * 0.0 + UP * 2.75)
        ruler = Line(UP * 2.4, DOWN * 2.0, color=GREY_C, stroke_width=2).shift(RIGHT * 4.6)
        ticks = VGroup()
        for k, v in enumerate(d["drift"]):
            y = ruler.get_top() + DOWN * 4.4 * (abs(v) / 100.0)
            ticks.add(VGroup(Line(y + LEFT * 0.12, y + RIGHT * 0.12, color=GREY_C, stroke_width=2), label(rf"{v:+.0f}" if k else r"0", font_size=22, color=GREY_B).next_to(y, RIGHT, buff=0.2)))
        semi = ruler.get_top() + DOWN * 4.4
        ticks.add(VGroup(Line(semi + LEFT * 0.12, semi + RIGHT * 0.12, color=BAD, stroke_width=2), label(r"$-100$: \ a semitone", font_size=20, color=BAD).next_to(semi, RIGHT, buff=0.2)))
        rl = label(r"the note C, \ in cents", font_size=22, color=GREY_A).next_to(ruler, UP, buff=0.2)
        mark = Triangle(color=TUNE, fill_color=TUNE, fill_opacity=1).scale(0.13).rotate(-PI / 2).next_to(ruler.get_top(), LEFT, buff=0.1)
        self.play(FadeIn(first), FadeIn(grid), FadeIn(ruler), FadeIn(ticks), FadeIn(rl), FadeIn(mark), run_time=0.6)
        cells = [first] + [x for row in grid for x in row[:4]]
        with self.listen(c) as snd:
            window(snd, r"one progression, \ four times, \ every chord pure", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for k in range(len(rows)):
                snd.wait_until(f"c{k}")
                if k < len(cells):
                    cells[k].set_color(TUNE)
                if k:
                    cells[min(k, len(cells)) - 1].set_color(GREY_B)
                if k == len(rows) - 1:
                    cells[-1].set_color(GREY_B)
                if rows[k]["tonic_cents"] is not None:
                    y = ruler.get_top() + DOWN * 4.4 * (abs(rows[k]["tonic_cents"]) / 100.0)
                    self.play(mark.animate.next_to(y, LEFT, buff=0.1), run_time=0.5)
                else:
                    self.play(Indicate(cells[min(k, len(cells) - 1)], color=WHITE, scale_factor=1.08), run_time=0.5)
        with self.voiceover(
            "Four chords, played four times round, and every chord in it was perfectly in tune: pure thirds, pure "
            "fifths, nothing beating. Any note that two neighbouring chords had in common was held at exactly the "
            "same pitch from one to the next, as good singers do. <bookmark mark='a'/> And the music sank. Each "
            f"time round, the home chord came back about a fifth of a semitone lower. After four rounds it is "
            f"{say(abs(d['total']))} cents flat: most of a semitone. Listen to the first chord, and then the last."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(mark, color=WHITE, scale_factor=1.6))
        cmp_ = clip("pump.compare")
        bx = boxes((r"the first chord", r"the last chord"), buff=0.6, width=3.2, height=1.1, font_size=26).move_to(LEFT * 2.2 + DOWN * 2.3)
        self.play(FadeIn(bx), run_time=0.4)
        with self.listen(cmp_) as snd:
            window(snd, r"the first chord, \ then the last", kind="synthesized", corner=DL, tag_corner=DR, tag=False)
            for ev, b in zip(("first", "last"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.0)
        with self.voiceover(
            "Nobody sang a wrong note. The arithmetic of pure intervals does not add up, and this part is about "
            "what musicians have done about that for two and a half thousand years."
        ):
            self.play(Indicate(ticks[-2], color=BAD, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zhu(self):
        d = load("equal")
        card = history_card(1584, r"Zhu Zaiyu, \ a prince of the Ming dynasty",
                            r"gives up his title to study music and the calendar, and with an abacus of eighty-one rods computes one number to twenty-four decimal places.",
                            width=6.2).to_corner(UL, buff=0.45)
        num = MathTex(r"\sqrt[12]{2} \;=\; " + d["root"][:14] + r"\,", d["root"][14:], font_size=40).move_to(DOWN * 0.4)
        num[1].set_color(GREY_B)
        why = VGroup(label(r"multiply a string's frequency by this number twelve times, \ and it has exactly doubled", font_size=28, color=GREY_A),
                     label(r"twelve equal steps to the octave: \ every interval slightly wrong, \ and none of them bad", font_size=28, color=TUNE),
                     label(r"it is the tuning of every piano, \ guitar and synthesizer today", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.22).move_to(DOWN * 2.2)
        with self.voiceover(
            "In 1584 Zhu Zaiyu, a prince of the Ming dynasty who had given up his title for the study of music "
            "and the calendar, sat down with an abacus of eighty-one rods and computed a single number to "
            "twenty-four decimal places. <bookmark mark='a'/> The twelfth root of two. Multiply a string's "
            "frequency by it twelve times over, and the frequency has exactly doubled. <bookmark mark='b'/> It is "
            "one answer to the problem you have just heard: twelve equal steps to the octave, in which every "
            "interval but the octave is slightly wrong and none of them is bad. <bookmark mark='c'/> Today it is "
            "the tuning of every piano, every guitar and every synthesizer. But it took three centuries to win, "
            "and it was neither the first answer nor, for most music, the best-sounding one."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Write(num), run_time=2.5)
            self.play(FadeIn(why[0]))
            vo.wait_until("b")
            self.play(FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"why twelve pure fifths miss seven octaves: \ the Pythagorean comma",
            r"why four pure fifths miss a pure third: \ the syntonic comma, \ and the pump",
            r"meantone: \ pure thirds for eight keys, \ and a wolf in the rest",
            r"well temperaments: \ every key usable, \ no two alike",
            r"equal temperament: \ what it costs, \ how it is tuned, \ and why twelve",
            r"what pianos, \ singers and string players actually do",
        ], title=r"Part 6: \ Tuning", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "Part 5 found that the smoothest intervals are the ones where partials line up: two to one, three to "
            "two, five to four. This part asks whether you can have them all at once. <bookmark mark='a'/> We "
            "will find that twelve pure fifths miss seven octaves, <bookmark mark='b'/> and that four pure fifths "
            "miss a pure third: two small gaps, called commas, which between them drive the whole subject. "
            "<bookmark mark='c'/> Then three ways of hiding them. Meantone, which keeps the thirds pure in eight "
            "keys and pays for it with a wolf in the others. <bookmark mark='d'/> The well temperaments, in which "
            "every key is usable and no two sound alike. <bookmark mark='e'/> And equal temperament: what it "
            "costs, how a tuner sets it by counting beats, and why the number is twelve. <bookmark mark='f'/> "
            "Last, what pianos, singers and string players really do, which is none of the above. Every tuning "
            "in this part is computed by Monochord in exact fractions, and checked against the published tables."
        ) as vo:
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
