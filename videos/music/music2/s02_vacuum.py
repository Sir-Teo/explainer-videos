from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


def jar(height=3.6, width=2.6) -> VGroup:
    """A bell jar on a plate with a pipe to a pump; ``.inside`` is its middle."""
    dome = ArcBetweenPoints([width / 2, height - width / 2, 0], [-width / 2, height - width / 2, 0], angle=PI,
                            color="#9FB8AD", stroke_width=3)
    sides = VGroup(Line([-width / 2, 0, 0], [-width / 2, height - width / 2, 0], color="#9FB8AD", stroke_width=3),
                   Line([width / 2, 0, 0], [width / 2, height - width / 2, 0], color="#9FB8AD", stroke_width=3))
    plate = Rectangle(width=width + 0.8, height=0.16, stroke_width=0, fill_color=GREY_B, fill_opacity=1).move_to([0, -0.08, 0])
    pipe = VGroup(Line([0.6, -0.16, 0], [0.6, -0.7, 0], color=GREY_B, stroke_width=4),
                  Line([0.6, -0.7, 0], [2.4, -0.7, 0], color=GREY_B, stroke_width=4))
    g = VGroup(dome, sides, plate, pipe)
    g.inside = np.array([0.0, height * 0.45, 0.0])
    return g


class Vacuum(SoundScene):
    def construct(self):
        chapter(self, 1, r"Sound needs air", r"What happens to a sound when the air is taken away?", lit=(1660,))
        self.boyle()
        self.pumped()
        self.media()

    # ------------------------------------------------------------------
    def boyle(self):
        card = history_card(1660, r"Robert Boyle, \ Oxford",
                            r"with Robert Hooke's air pump: a ticking watch hung by a thread in a glass jar, and the "
                            r"air drawn out. Otto von Guericke had tried a bell a few years before.", width=5.6)
        card.to_corner(UL, buff=0.45)
        j = jar().move_to(RIGHT * 2.6 + DOWN * 0.9)
        base = np.array([j[2].get_center()[0], j[2].get_top()[1], 0.0])       # the middle of the plate
        watch = VGroup(Circle(radius=0.34, color=STR, stroke_width=3),
                       Line(ORIGIN, UP * 0.22, color=STR, stroke_width=2.5), Line(ORIGIN, RIGHT * 0.16, color=STR, stroke_width=2.5))
        watch.move_to(base + UP * 1.7)
        thread = Line(watch.get_top(), watch.get_top() + UP * 1.1, color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(radius=0.03, color=AIR) for _ in range(90)])
        rng = np.random.default_rng(3)
        placed = 0
        while placed < len(dots):                      # scattered inside the glass, dome included
            x, y = rng.uniform(-1.15, 1.15), rng.uniform(0.12, 3.4)
            if y < 2.3 or x * x + (y - 2.3) ** 2 < 1.15 ** 2:
                dots[placed].move_to(base + np.array([x, y, 0]))
                placed += 1
        pump = label(r"to the pump", font_size=22, color=GREY_B).next_to(j, RIGHT, buff=0.1).shift(DOWN * 1.6)
        with self.voiceover(
            "Start with the experiment that showed sound needs something to travel in. In 1660 Robert Boyle hung a "
            "ticking watch by a thread inside a glass jar, <bookmark mark='a'/> and had Robert Hooke's pump draw the "
            "air out. <bookmark mark='b'/> The watch went on ticking. He could see it. But as the air thinned, the "
            "ticking faded, until he could hear nothing at all. Let the air back in, and the sound came back."
        ) as vo:
            self.play(FadeIn(card), FadeIn(j), FadeIn(watch), FadeIn(thread), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(pump))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeOut(dot, shift=DOWN * 0.3) for dot in dots[:82]], lag_ratio=0.03), run_time=5.0)
        self.jar, self.base = j, base
        self.play(FadeOut(card), FadeOut(watch), FadeOut(thread), run_time=0.4)

    # ------------------------------------------------------------------
    def pumped(self):
        d = load("vacuum")
        c = clip("vacuum.jar")
        mono = StringView(width=1.7, scale=0.3, stroke_width=3).move_to(self.base + UP * 1.5)
        self.play(FadeIn(mono), run_time=0.4)
        rows = VGroup()
        for i, r in enumerate(d["rows"]):
            frac = r"\tfrac{1}{%d}" % round(1 / r["atm"]) if r["atm"] < 1 else "1"
            rows.add(VGroup(MathTex(frac + r"\ \text{of the air}", font_size=36),
                            MathTex(r"%+.0f\ \text{dB}" % r["db"] if r["db"] else r"0\ \text{dB}", font_size=36, color=LEVEL)
                            ).arrange(RIGHT, buff=0.9))
        rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(LEFT * 3.4 + UP * 0.3)
        meter = Meter(width=0.5, height=3.4).next_to(rows, RIGHT, buff=1.0)
        why_ = label(r"the same motion, \ less air to push: \ the power sent out is proportional to the density",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.55)
        with self.voiceover(
            "We can do Boyle's experiment with the string from Part 1. A small vibrating thing sends out sound power "
            "in proportion to the density of the air it pushes on. <bookmark mark='a'/> So a tenth of the air means "
            "a tenth of the power. Here is our monochord in the jar, with all the air, then a tenth, a hundredth, "
            "and a thousandth."
        ) as vo:
            self.play(FadeIn(why_), FadeIn(meter))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
        with self.listen(c) as snd:
            window(snd, r"all the air, \ a tenth, \ a hundredth, \ a thousandth", detail=r"level by the computed law",
                   corner=DL, tag_corner=UL)
            for i, r in enumerate(d["rows"]):
                snd.wait_until(f"p{i}")
                rows.set_color(GREY_C)
                rows[i].set_color(WHITE)
                rows[i][1].set_color(LEVEL)
                top = 10 ** (r["db"] / 20)
                t0 = snd.time_of(f"p{i}")
                lens = Lens(mono.p(0), mono.p(1), amp=0.16, color=TUNE)      # the string moves as much each time
                snd.show(lens)
                snd.drive(lens, ring(at=t0, rate=1.6, stop_at=t0 + 1.3))
                snd.drive(meter, lambda m, t, top=top, t0=t0: m.set_level(top * float(np.exp(-1.6 * max(t - t0, 0.0)))))
                snd.wait_until(t0 + 1.2)
        with self.voiceover(
            "Each step is ten times less power. We will give that step a name in chapter four. For now, the point "
            "is Boyle's: no air, no sound. <bookmark mark='a'/> Whatever sound is, it is something the air does."
        ) as vo:
            rows.set_color(WHITE)
            for r in rows:
                r[1].set_color(LEVEL)
            vo.wait_until("a")
            self.play(Indicate(why_, color=TUNE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def media(self):
        d = load("vacuum")
        head = label(r"Anything springy will carry sound", font_size=36).to_edge(UP, buff=0.5)
        law = MathTex(r"\text{speed} = \sqrt{\frac{\text{stiffness}}{\text{density}}}", font_size=40, color=AIR).next_to(head, DOWN, buff=0.35)
        top = max(m["speed"] for m in d["media"])
        rows = VGroup()
        for i, m in enumerate(d["media"]):
            bar = Rectangle(width=max(8.0 * m["speed"] / top, 0.05), height=0.36, stroke_width=0, fill_color=AIR if i < 2 else ("#7FB3FF" if i == 2 else STR),
                            fill_opacity=0.85)
            rows.add(VGroup(label(m["name"], font_size=30), bar,
                            label(rf"{m['speed']:,.0f} m/s".replace(",", "{,}"), font_size=28, color=TUNE),
                            label(m["how"], font_size=22, color=GREY_B)))
        for i, r in enumerate(rows):
            y = 0.5 - 0.95 * i
            r[0].move_to([-6.3, y, 0], aligned_edge=LEFT)
            r[1].move_to([-3.6, y, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
            r[3].next_to(r[1], DOWN, buff=0.08).align_to(r[1], LEFT)
        with self.voiceover(
            "Boyle's jar shows that sound needs a medium. It does not have to be air. Anything that springs back "
            "when it is squeezed will carry sound, and the springier and lighter it is, the faster the sound goes. "
            f"<bookmark mark='a'/> In air, about {say(d['media'][0]['speed'])} metres a second: we will see where "
            f"that number comes from in chapter three. <bookmark mark='b'/> In helium, which is seven times "
            f"lighter, nearly three times as fast. That is why a voice full of helium sounds like a cartoon, and "
            "the reason turns out to be subtler than a change of pitch: we will come back to it in Part 8. "
            f"<bookmark mark='c'/> In water, about fifteen hundred. <bookmark mark='d'/> And along a steel rod, "
            f"{say(round(d['media'][3]['speed'], -2))}: put your ear to a railway line and you hear the train "
            "long before the sound arrives through the air. <bookmark mark='e'/> Space, with nothing in it to "
            "squeeze, is silent, whatever the films say."
        ) as vo:
            self.play(FadeIn(head), FadeIn(law))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), FadeIn(r[3]), run_time=0.9)
            vo.wait_until("e")
            self.play(Indicate(head, color=TUNE, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

