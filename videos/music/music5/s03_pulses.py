from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


def pulse_rows(p: int, q: int, width: float = 9.0, cycles: int = 2) -> VGroup:
    """Two rows of pulses in the ratio p:q over ``cycles`` repeats of their pattern; pulses that coincide are marked."""
    g = VGroup()
    rows = VGroup(*[Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_D, stroke_width=1).shift(UP * y) for y in (0.45, -0.45)])
    g.add(rows)
    ticks = VGroup()
    for row, n, col in ((0, p, AIR), (1, q, TUNE)):
        for k in range(n * cycles + 1):
            x = -width / 2 + width * k / (n * cycles)
            both = (k % n) == 0
            ticks.add(Line(UP * 0.28, DOWN * 0.28, color=GOOD if both else col, stroke_width=6 if both else 3.5).move_to(RIGHT * x + UP * (0.45 - 0.9 * row)))
    g.add(ticks)
    g.ticks = ticks
    return g


class Pulses(SoundScene):
    def construct(self):
        chapter(self, 2, r"Pulses that coincide", r"Does the ear count?", lit=(1638,), extra=((1638, r"Galileo's \textit{Two New Sciences}"),))
        self.galileo()
        self.speedup()
        self.verdict()

    # ------------------------------------------------------------------
    def galileo(self):
        card = history_card(1638, r"Galileo Galilei, \ aged 74, \ under house arrest",
                            r"\textit{Two New Sciences}: a sound is a train of pulses on the eardrum. Consonances are the pairs whose pulses keep arriving together.",
                            width=5.8).to_corner(UL, buff=0.4)
        rows = VGroup()
        for (p, q), name in (((2, 1), r"octave"), ((3, 2), r"fifth"), ((16, 15), r"minor second")):
            r = pulse_rows(p, q, width=7.2, cycles=2 if p < 10 else 1)
            rows.add(VGroup(r, VGroup(label(name, font_size=24, color=GREY_A), MathTex(rf"{p}:{q}", font_size=26, color=RATIO)).arrange(DOWN, buff=0.06).next_to(r, LEFT, buff=0.3)))
        rows.arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(RIGHT * 1.6 + DOWN * 1.2)
        note = label(r"green: \ pulses that arrive together", font_size=22, color=GOOD).next_to(rows, UP, buff=0.25).align_to(rows, RIGHT)
        with self.voiceover(
            "A century before Euler, Galileo had already looked for one. In his last book, written under house "
            "arrest at the age of seventy-four, he proposed that a sound is a train of pulses striking the "
            "eardrum, and that what matters is how the pulses of two notes fall against each other. "
            "<bookmark mark='a'/> In an octave, every pulse of the lower note arrives together with a pulse of "
            "the upper. The eardrum is never, as he put it, kept in perpetual torment, bending two ways at "
            "once. <bookmark mark='b'/> In a fifth, the pulses meet at every second pulse of the lower note. "
            "<bookmark mark='c'/> In a minor second, sixteen against fifteen, they meet so rarely that the ear "
            "receives a tangle. It is the first physical theory of consonance: order in time."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speedup(self):
        d = load("pulses")
        c = clip("pulses.speedup")
        secs = d["seconds"]
        head = label(r"three against two, \ faster and faster", font_size=32, color=GREY_A).to_edge(UP, buff=0.45)
        w = 11.0
        lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, color=GREY_D, stroke_width=1).shift(UP * y) for y in (1.1, 0.0)])
        names = VGroup(label(r"3", font_size=36, color=AIR).next_to(lines[0], LEFT, buff=0.2), label(r"2", font_size=36, color=TUNE).next_to(lines[1], LEFT, buff=0.2))
        now = Line(UP * 1.7, DOWN * 0.6, color=MC.PLAY, stroke_width=2).shift(LEFT * 3.0)
        speed = label(r"3 and 2 pulses a second", font_size=30, color=GREY_A).move_to(DOWN * 1.6)
        rows = [(3.0, 1.1), (2.0, 0.0)]
        window_s = 2.2                                   # seconds of the future shown to the right of the line
        ln100 = np.log(100.0)

        def phase(rate0, t):                             # how many clicks a train has made by time t
            return rate0 * secs / ln100 * (100.0 ** (min(t, secs) / secs) - 1.0) + rate0 * 100.0 * max(t - secs, 0.0)

        def when(rate0, k):                              # the time of click k
            edge = phase(rate0, secs)
            if k <= edge:
                return secs * np.log(1.0 + k * ln100 / (rate0 * secs)) / ln100
            return secs + (k - edge) / (rate0 * 100.0)

        def draw(m, t):
            x0 = now.get_x()
            span = window_s * 100.0 ** (-min(max(t, 0.0) / secs, 1.0))    # the picture zooms as the clicks speed up
            pts = []
            for rate0, y in rows:
                k0, k1 = int(np.ceil(phase(rate0, max(t - 0.25 * span, 0.0)))), int(np.floor(phase(rate0, t + span)))
                for k in range(max(k0, 1), k1 + 1):
                    x = x0 + (when(rate0, k) - t) / span * (w / 2 + 3.0)
                    if -w / 2 < x < w / 2:
                        pts += [[x, y + 0.3, 0], [x, y - 0.3, 0]]
            m.set_points(np.zeros((0, 3)))
            if pts:
                m.set_points_as_corners(pts[:2])
                for k in range(2, len(pts), 2):
                    m.start_new_path(np.array(pts[k]))
                    m.add_line_to(np.array(pts[k + 1]))

        ticks = VMobject(stroke_color=WHITE, stroke_width=3.5)
        draw(ticks, 0.0)
        with self.voiceover(
            "You can hear Galileo's idea directly, and it gives away something remarkable. Here are two trains of "
            "clicks. One clicks three times while the other clicks twice: a rhythm, three against two. Over nine "
            "seconds both speed up together, a hundred times over. Listen to what the rhythm turns into."
        ):
            self.play(FadeIn(head), FadeIn(lines), FadeIn(names), FadeIn(now), FadeIn(speed), FadeIn(ticks))
        with self.listen(c) as snd:
            window(snd, r"clicks: \ three against two, \ speeding up", kind="synthesized", detail=r"two trains of clicks", corner=DL, tag_corner=DR)
            snd.drive(ticks, draw)
            for mark, text in ((0.0, r"3 and 2 pulses a second"), (3.0, r"14 and 9 a second"), (5.5, r"50 and 33 a second"), (7.5, r"140 and 93 a second"),
                               (secs, r"300 and 200 a second: \ a fifth")):
                snd.wait_until(mark)
                self.remove(speed)
                speed = label(text, font_size=30, color=GREY_A if mark < secs else GOOD).move_to(DOWN * 1.6)
                self.add(speed)
        with self.voiceover(
            "It began as a rhythm and ended as a chord. Somewhere around twenty or thirty clicks a second the "
            "separate clicks ran together into two buzzing notes, and the two notes are a perfect fifth. "
            "<bookmark mark='a'/> A rhythm of three against two, played a hundred times faster, is the interval "
            "three to two. Rhythm and harmony are one thing at two speeds. Composers have built pieces on that "
            "idea, and we will come back to it when we reach rhythm, in Part 11."
        ) as vo:
            vo.wait_until("a")
            eq = label(r"rhythm $3 : 2$ \quad $\times\,100$ \quad = \quad the interval $3 : 2$", font_size=34, color=GOOD).move_to(DOWN * 2.6)
            self.play(FadeIn(eq))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        d = load("number")
        rows = {r["name"]: r for r in d["rows"]}
        names = ["octave", "fifth", "fourth", "major third", "minor third", "tritone"]
        table = VGroup(*[VGroup(label(n, font_size=28, color=GREY_A), MathTex(rf"{rows[n]['p']}:{rows[n]['q']}", font_size=30, color=RATIO),
                                label(rf"repeats every {rows[n]['repeat']} cycle" + ("s" if rows[n]["repeat"] > 1 else "") + " of the lower note", font_size=26))
                         for n in names])
        for k, r in enumerate(table):
            r[0].move_to(LEFT * 5.6 + UP * (2.2 - 0.6 * k), aligned_edge=LEFT)
            r[1].move_to(LEFT * 2.6 + UP * (2.2 - 0.6 * k))
            r[2].move_to(LEFT * 1.3 + UP * (2.2 - 0.6 * k), aligned_edge=LEFT)
        bad = VGroup(label(r"the same flaw: \ a fifth 5 cents wide never repeats at all", font_size=28, color=BAD),
                     label(r"and can the ear follow 300 pulses a second?", font_size=28, color=BAD)).arrange(DOWN, buff=0.18).move_to(DOWN * 1.9)
        keep = label(r"Part 4: \ the nerve does fire in time with the wave. \quad Keep this idea for chapter 7.", font_size=28, color=GOOD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So Galileo's measure of an interval is the length of its pattern. <bookmark mark='a'/> An octave "
            "repeats with every cycle of the lower note, a fifth every two, a fourth every three, a major third "
            "every four. The tritone of forty-five to thirty-two repeats only every thirty-two. The shorter the "
            "pattern, the sweeter. It is the same ranking as before, because it is the same arithmetic. "
            "<bookmark mark='b'/> And it has the same flaw. Widen the fifth by five cents and its pattern never "
            "repeats at all. There was also an objection in Galileo's own century: how could the ear possibly "
            "follow three hundred pulses a second? <bookmark mark='c'/> To that one, we now have an answer. In "
            "Part 4 we saw that the auditory nerve does fire in time with the wave, up to a few thousand hertz. "
            "The pulses are there, in the nerve. So do not throw this idea away. It will come back in chapter "
            "seven, repaired. First, the theory that replaced it."
        ) as vo:
            head = label(r"Galileo's measure: \ how long before the pattern repeats", font_size=30, color=GREY_A).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.5), run_time=7.0)
            vo.wait_until("b")
            self.play(FadeIn(bad[0]))
            self.wait(max(vo.until("c") - 6.0, 0.1))
            self.play(FadeIn(bad[1]))
            vo.wait_until("c")
            self.play(FadeIn(keep))
        self.wait(0.3)
        self.clear_scene()
