from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (FREQ, GOOD, HIST, LEFT_C, NODE, PART, RATIO, RIGHT_C, STR, TIME, TUNE, clip,
                                        flat_name, load, say, window)

X = np.linspace(0, 1, 121)


def swing(view: StringView, n: int, amp: float = 1.0, rate: float = 0.35, phase: float = 0.0):
    """Make a StringView swing in its n-th mode, ``rate * n`` times a second (slow motion): a time-based updater."""
    state = {"t": 0.0}

    def upd(m, dt):
        state["t"] += dt
        view.set_shape(amp * np.sin(n * np.pi * X) * np.cos(2 * np.pi * rate * n * state["t"] + phase))

    view.set_shape(amp * np.sin(n * np.pi * X) * np.cos(phase))
    view.add_updater(upd)
    return view


def nodes(view: StringView, n: int, radius=0.06) -> VGroup:
    return VGroup(*[Dot(view.p(k / n), radius=radius, color=NODE) for k in range(1, n)])


class Modes(SoundScene):
    def construct(self):
        self.card()
        self.guess()
        self.gallery()
        self.same()
        self.touch()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Standing waves", r"Can a string swing in place?", lit=(1677, 1701, 1713), part=PART)
        with self.voiceover("Chapter six. Standing waves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def guess(self):
        s = StringView(width=9.6, scale=0.8).move_to(UP * 2.6)
        swing(s, 1, rate=0.5)
        rows = [
            MathTex(r"u(x,t)", r"=", r"X(x)", r"\cos \omega t", font_size=44),
            MathTex(r"-\omega^2\, X", r"=", r"c^2\, X''", font_size=44),
            MathTex(r"X(x)", r"=", r"\sin kx", r",\qquad k = \omega / c", font_size=44),
            MathTex(r"\sin kL", r"=", r"0", r"\;\Longrightarrow\; k = \frac{n\pi}{L}", font_size=44),
        ]
        whys = [why(r"every point keeps the same rhythm"), why(r"put it into the wave equation"),
                why(r"the shape must be a sine"), why(r"both ends are fixed")]
        rows[0][2].set_color(STR), rows[0][3].set_color(TIME)
        step = ladder(self, rows, whys, keep=4, top=1.5, buff=0.42, x=-1.9)
        with self.voiceover(
            "Here is a different kind of motion to look for. Not a shape that travels, but a shape that stays where "
            "it is and swings: every point of the string moving up and down in the same rhythm, some more, some "
            "less. <bookmark mark='a'/> In symbols, a fixed shape, X of x, times a cosine in time. "
            "<bookmark mark='b'/> Put that into the wave equation. The cosine cancels, and what is left says that "
            "the shape's curvature is proportional to minus the shape itself. <bookmark mark='c'/> Only a sine wave "
            "does that. <bookmark mark='d'/> And a sine that is zero at both ends has to fit a whole number of "
            "half-waves into the string."
        ) as vo:
            head = VGroup(label(r"not a shape that travels", font_size=34, color=GREY_B),
                          label(r"a shape that stays where it is, \ and swings", font_size=38, color=STR)
                          ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.4)
            self.play(FadeIn(s), FadeIn(head[0]))
            self.play(FadeIn(head[1], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(head), run_time=0.3)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        res = MathTex(r"f_n", r"=", r"n\,\frac{c}{2L}", r"=", r"n\, f_1", r",\qquad n = 1, 2, 3, \dots", font_size=52)
        res[0].set_color(FREQ), res[4].set_color(GOOD)
        res.move_to(DOWN * 2.6)
        box = SurroundingRectangle(res[:5], color=GOOD, buff=0.18, corner_radius=0.1, stroke_width=2)
        with self.voiceover(
            "So a string can swing in place, but only in certain shapes, and each shape has its own frequency: "
            "<bookmark mark='a'/> one, two, three, four times the frequency we found in the last chapter. Whole "
            "multiples, and nothing in between."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(res), run_time=1.5)
            self.play(Create(box))
        self.wait(0.3)
        s.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        d = load("modes")
        c = clip("modes.series")
        cells = VGroup()
        views = []
        for row in d["table"]:
            n = row["n"]
            v = StringView(width=3.9, scale=0.3, stroke_width=3)
            swing(v, n, rate=0.22)
            nd = nodes(v, n)
            num = MathTex(rf"{n}", font_size=40, color=harmonic_color(n))
            tag = label(rf"{say(row['hz'], 1)} Hz", font_size=24, color=GREY_B)
            name = label(flat_name(row["note"]) + (rf" \ ({row['cents']:+.0f})" if abs(row["cents"]) > 5 else ""),
                         font_size=26, color=harmonic_color(n))
            cell = VGroup(num, VGroup(v, nd), VGroup(tag, name).arrange(DOWN, buff=0.08, aligned_edge=LEFT))
            cell.arrange(RIGHT, buff=0.3)
            cell.num, cell.view, cell.name, cell.tag = num, v, name, tag
            name.set_opacity(0)
            cells.add(cell)
            views.append(v)
        left = VGroup(*cells[:4]).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        right = VGroup(*cells[4:]).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 1.05 + RIGHT * 0.35)
        defn = VGroup(label(r"\textbf{mode}: \ one of the string's own ways of swinging", font_size=26, color=STR),
                      label(r"\textbf{node}: \ a point that stays still", font_size=26, color=NODE),
                      label(r"\textbf{harmonics}: \ the frequencies $f_1, 2f_1, 3f_1, \dots$", font_size=26, color=FREQ)
                      ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "These are the first eight. Each one is called a mode of the string. <bookmark mark='a'/> The second "
            "mode has one point in the middle that never moves: a node. The third has two nodes, the fourth three. "
            "<bookmark mark='b'/> The frequencies, one, two, three, four times the lowest, are called harmonics. "
            "Listen to them in order. Each is a single pure tone, at the frequency of that mode."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(cl) for cl in cells], lag_ratio=0.1), FadeIn(defn[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(defn[1]), Indicate(cells[1][1][1], color=NODE, scale_factor=2.0))
            vo.wait_until("b")
            self.play(FadeIn(defn[2]))
        with self.listen(c) as snd:
            window(snd, r"modes 1 to 8", kind="synthesized", detail=r"pure tones")
            for cell, row in zip(cells, d["table"]):
                snd.wait_until(f"m{row['n']}")
                cell.name.set_opacity(1)
                frame = SurroundingRectangle(cell, color=TUNE, buff=0.1, corner_radius=0.08, stroke_width=2)
                snd.show(frame)
                self.wait(0.8)
                self.remove(frame)
        ratio_tags = VGroup()
        for i, (txt, name) in enumerate(((r"2:1", r"octave"), (r"3:2", r"fifth"), (r"4:3", r"fourth"))):
            a, b = cells[i], cells[i + 1]
            br = Brace(VGroup(a.num, b.num), LEFT, buff=0.12, color=RATIO)
            t = VGroup(MathTex(txt, font_size=30, color=RATIO), label(name, font_size=22, color=RATIO)).arrange(DOWN, buff=0.05)
            t.next_to(br, LEFT, buff=0.1)
            ratio_tags.add(VGroup(br, t))
        with self.voiceover(
            "You heard a staircase whose steps get smaller. From the first mode to the second is an octave: two to "
            "one. <bookmark mark='a'/> From the second to the third, a fifth: three to two. <bookmark mark='b'/> "
            "From the third to the fourth, a fourth: four to three. <bookmark mark='c'/> Those are the monochord's "
            "ratios. Pythagoras found them by moving a bridge between different lengths. They were inside the one "
            "string all along, as the ratios between its own modes."
        ) as vo:
            self.play(FadeIn(ratio_tags[0]))
            vo.wait_until("a")
            self.play(FadeOut(ratio_tags[0]), FadeIn(ratio_tags[1]))
            vo.wait_until("b")
            self.play(FadeOut(ratio_tags[1]), FadeIn(ratio_tags[2]))
            vo.wait_until("c")
            self.play(FadeOut(ratio_tags[2]))
            self.play(*[Indicate(cells[i].num, color=TUNE, scale_factor=1.5) for i in range(4)])
        self.wait(0.3)
        for v in views:
            v.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def same(self):
        top = StringView(width=9.6, scale=0.85).move_to(UP * 2.1)
        mid = StringView(width=9.6, scale=0.85, color=RIGHT_C, stroke_width=3, supports=False).move_to(DOWN * 0.3)
        bot = StringView(width=9.6, scale=0.85, color=LEFT_C, stroke_width=3, supports=False).move_to(DOWN * 2.3)
        n, rate = 3, 0.25
        state = {"t": 0.0}

        def upd(m, dt):
            state["t"] += dt
            ph = 2 * np.pi * rate * state["t"]
            mid.set_shape(0.5 * np.sin(n * np.pi * X - ph))
            bot.set_shape(0.5 * np.sin(n * np.pi * X + ph))
            top.set_shape(np.sin(n * np.pi * X) * np.cos(ph))

        upd(top, 0)
        top.add_updater(upd)
        eq = MathTex(r"\sin kx \,\cos \omega t", r"=", r"\tfrac{1}{2}\sin k(x - ct)", r"+", r"\tfrac{1}{2}\sin k(x + ct)",
                     font_size=36).to_edge(UP, buff=0.35)
        eq[0].set_color(STR), eq[2].set_color(RIGHT_C), eq[4].set_color(LEFT_C)
        tags = VGroup(label(r"standing", font_size=24, color=STR), label(r"going right", font_size=24, color=RIGHT_C),
                      label(r"going left", font_size=24, color=LEFT_C))
        for t, v in zip(tags, (top, mid, bot)):
            t.next_to(v, LEFT, buff=0.15).to_edge(LEFT, buff=0.3)
        with self.voiceover(
            "Is this a new kind of solution, one d'Alembert missed? No. <bookmark mark='a'/> A standing sine wave is "
            "exactly two travelling sine waves of half the height, one going each way. Where they always cancel, "
            "there is a node. A mode is a travelling wave meeting its own reflection."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tags[0]), FadeIn(eq[0]))
            vo.wait_until("a")
            self.play(FadeIn(mid), FadeIn(bot), FadeIn(tags[1:]), FadeIn(eq[1:]))
        self.wait(0.3)
        top.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def touch(self):
        d = load("modes")
        tl = label(r"A trick every guitarist knows", font_size=34).to_edge(UP, buff=0.4)
        s = StringView(width=10.0, scale=0.8).move_to(UP * 1.5)

        def bars(values, y, name):
            b = partial_bars(values, width=6.4, height=1.5, floor_db=-45.0)
            b.move_to([1.2, y, 0])
            t = label(name, font_size=24, color=GREY_A).next_to(b, LEFT, buff=0.5)
            return VGroup(b, t)

        def finger(frac):
            tip = s.p(frac) + UP * 0.08
            return VGroup(Line(tip + UP * 1.0, tip, color=HIST, stroke_width=10),
                          Dot(tip, radius=0.09, color=HIST))

        with self.voiceover(
            "Modes are not just mathematics. You can pick them out with a fingertip. Pluck a string, and then "
            "touch it, very lightly, exactly at its midpoint. <bookmark mark='a'/> Every mode that is moving there "
            "is stopped by the finger. But the modes with a node at the midpoint never moved there in the first "
            "place. They do not feel the finger at all, and they ring on."
        ) as vo:
            minis = VGroup()
            for n in (1, 2, 3, 4):
                v = StringView(width=10.0, scale=0.3, stroke_width=2.5, supports=False)
                swing(v, n, rate=0.3)
                minis.add(VGroup(v, MathTex(str(n), font_size=30, color=harmonic_color(n)).next_to(v, LEFT, buff=0.3)))
            minis.arrange(DOWN, buff=0.42).move_to(DOWN * 1.6)
            mid = DashedLine(s.p(0.5) + DOWN * 0.2, [s.p(0.5)[0], minis.get_bottom()[1] - 0.1, 0], color=HIST,
                             stroke_width=1.5, dash_length=0.1)
            self.play(FadeIn(tl), FadeIn(s), FadeIn(minis), run_time=0.8)
            vo.wait_until("a")
            f0 = finger(0.5)
            self.play(FadeIn(f0, shift=DOWN * 0.3), Create(mid))
            self.play(minis[0].animate.set_opacity(0.15), minis[2].animate.set_opacity(0.15), run_time=1.0)
            self.play(Indicate(minis[1][1], color=GOOD, scale_factor=1.6), Indicate(minis[3][1], color=GOOD, scale_factor=1.6))
        for m_ in minis:
            m_[0].clear_updaters()
        self.play(FadeOut(f0), FadeOut(mid), FadeOut(minis), run_time=0.5)
        for key, frac, words, after_note in (("half", 0.5, r"the midpoint", r"an octave up"),
                                             ("third", 1 / 3, r"one third of the way along", r"an octave and a fifth up")):
            t = d["touch"][key]
            c = clip(f"modes.touch_{key}")
            before = bars(t["before_db"], -0.9, r"before the touch")
            after = bars(t["after_db"], -2.9, r"after")
            lens = Lens(s.p(0), s.p(1), amp=0.28, color=TUNE)
            fg = finger(frac)
            h = t["harmonic"]
            lens2 = VGroup(*[Lens(s.p(k / h), s.p((k + 1) / h), amp=0.16, color=TUNE) for k in range(h)])
            with self.voiceover(f"Here it is on our simulated string. The finger comes down at {words}, one second in."
                                if key == "half" else
                                "And again, with the finger a third of the way along."):
                self.play(FadeIn(before))
            with self.listen(c) as snd:
                window(snd, r"pluck, \ then touch")
                snd.show(lens)
                snd.drive(lens, lambda m, tt: m.set_amp(float(np.exp(-0.9 * tt)) if tt < t["at"] else 0.0))
                snd.wait_until("touch")
                snd.show(fg, lens2)
                for ln in lens2:
                    snd.drive(ln, lambda m, tt: m.set_amp(float(np.exp(-0.9 * (tt - t["at"])))))
                self.play(FadeIn(after), run_time=0.5)
            with self.voiceover(
                (f"Only the even modes are left: two, four, six, eight. The pitch we measure afterwards is "
                 f"{say(t['pitch_after'], 1)} hertz: {after_note}, and nobody moved a bridge.")
                if key == "half" else
                (f"Now modes three, six and nine survive, and the string sings at {say(t['pitch_after'], 1)} hertz: "
                 f"{after_note}. Players call these notes harmonics.")
            ):
                self.play(Indicate(after[0].bars, color=TUNE, scale_factor=1.05))
            self.play(FadeOut(before), FadeOut(after), run_time=0.5)
        card = history_card(1677, r"John Wallis reports the nodes", r"paper riders on a string: \ those sitting on "
                            r"a node stay put, \ the rest are thrown off. \ Sauveur gave nodes and harmonics their "
                            r"names in 1701.", width=6.4).move_to(DOWN * 1.9)
        with self.voiceover(
            "This was how the nodes were first seen, in the sixteen-seventies: little paper riders on a string, "
            "thrown off everywhere except at the nodes. <bookmark mark='a'/> So we have two descriptions of one "
            "string. Shapes that travel, and modes that stand. In 1750 the question of which one is right started "
            "a fight between the best mathematicians in Europe."
        ) as vo:
            swing(s, 3, amp=0.9, rate=0.35)
            riders = VGroup(*[VMobject(stroke_color=HIST, stroke_width=3).set_points_as_corners(
                [[-0.09, 0, 0], [0, 0.2, 0], [0.09, 0, 0]]).move_to(s.p(k / 12) + UP * 0.1) for k in range(1, 12)])
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(riders))
            off = [r for k, r in zip(range(1, 12), riders) if k % 4 != 0]
            self.play(LaggedStart(*[FadeOut(r, shift=UP * 0.9 + RIGHT * 0.2 * ((k % 3) - 1)) for k, r in enumerate(off)],
                                  lag_ratio=0.12), run_time=2.0)
            vo.wait_until("a")
        s.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
