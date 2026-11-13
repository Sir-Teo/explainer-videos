from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ when sound is too loud to be linear", r"What happens when the disturbance is not small?",
                lit=(1883,), extra=((1883, r"Krakatoa"), (1935, r"Fubini's solution"), (1996, r"shock waves in trombones")))
        self.steepen()
        self.brass()
        self.open()

    # ------------------------------------------------------------------
    def steepen(self):
        d = load("nonlinear")
        cols = [GOOD, TUNE, RATIO, BAD]
        panels = VGroup()
        for i, s in enumerate(d["sigma"]):
            sc = Scope(width=2.8, height=1.7, color=cols[i], frame=True)
            sc.set_wave(np.tile(d["waves"][i], 2), gain=0.9)
            t = label(rf"{100 * s:.0f}\% of the way" if i else r"at the start", font_size=24, color=cols[i]).next_to(sc, UP, buff=0.12)
            panels.add(VGroup(sc, t))
        panels.arrange(RIGHT, buff=0.35).move_to(UP * 1.6)
        head = label(rf"a tone of {d['db']:.0f} dB in a tube: \ the wave, \ on its way to breaking after {d['shock_m']:.1f} m",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        bars = VGroup()
        for i, row in enumerate(d["harmonics"]):
            b = partial_bars(np.array(row["sim"]), width=2.6, height=1.3, db=False, numbers=True, font_size=16)
            marks = VGroup(*[Line(LEFT * 0.16, RIGHT * 0.16, color=WHITE, stroke_width=2.5).move_to(
                [bar.get_x(), b.bars[0].get_bottom()[1] + 1.3 * row["fubini"][k] / max(max(row["sim"]), 1e-9), 0])
                for k, bar in enumerate(b.bars)])
            g = VGroup(b, marks)
            g.next_to(panels[i], DOWN, buff=0.45)
            bars.add(g)
        leg = label(rf"bars: \ harmonics of the simulated wave \qquad white ticks: \ Fubini's solution (1935) \qquad largest gap: \ {d['worst']:.4f}",
                    font_size=22, color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Everything so far assumed that sound is a tiny ripple on the air. For music it almost always is. But "
            "make the ripple large and something new happens. The squeezed part of the wave is hotter, so sound "
            "travels faster there, and it is also moving forward with the air. The crests catch up with the troughs. "
            "<bookmark mark='a'/> Here is a very loud pure tone in our row of parcels, looked at further and further "
            "down the tube. The front of each wave gets steeper and steeper, heading for a vertical cliff: a shock. "
            "<bookmark mark='b'/> A steeper wave is a brighter sound. New harmonics appear that the source never "
            "made. Their sizes were worked out exactly by Eugene Fubini in 1935, <bookmark mark='c'/> and our "
            f"parcels, which obey only the gas law, agree with him to {say(d['worst'], 4)} of the wave's height."
        ) as vo:
            idea = VGroup(label(r"where the air is squeezed it is hotter, \ and it is moving forward:", font_size=30, color=GREY_A),
                          label(r"the crests travel faster than the troughs", font_size=34, color=TUNE)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.2)
            self.play(FadeIn(head), FadeIn(panels[0]))
            self.wait(2.0)
            self.play(FadeIn(idea))
            vo.wait_until("a")
            self.play(FadeOut(idea), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in panels[1:]], lag_ratio=0.6), run_time=max(vo.until("b") - 0.3, 3.0))
            self.play(LaggedStart(*[FadeIn(b[0]) for b in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(*[FadeIn(b[1]) for b in bars], FadeIn(leg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def brass(self):
        d = load("nonlinear")
        c = clip("nonlinear.brass")
        card = history_card(1996, r"Hirschberg, Gilbert, Msallam and Wijnands",
                            r"measured shock waves coming out of a trombone played fortissimo: the ``brassy'' sound is "
                            r"made in the air of the tube, not by the lips", width=5.8).to_corner(UL, buff=0.4)
        rows = VGroup(VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"played", r"pressure in the mouthpiece", r"breaks after")]))
        for r in d["horn"]:
            rows.add(VGroup(label(r["name"], font_size=28), label(rf"{r['pa'] / 1000:.1f} kPa \ ({r['db']:.0f} dB)", font_size=28, color=FORCE),
                            label(rf"{r['shock_m']:.1f} m", font_size=28, color=BAD if r["shock_m"] < d["tube_m"] else GOOD)))
        xs = [-0.5, 1.2, 4.9]
        for i, r in enumerate(rows):
            for cell, x in zip(r, xs):
                cell.move_to([x - 0.2, 2.6 - 0.6 * i, 0], aligned_edge=LEFT)
        tube = label(rf"a trombone's tube: \ about {d['tube_m']:.1f} m", font_size=26, color=RATIO).move_to([3.0, -0.1, 0])
        sc = VGroup(Scope(width=4.4, height=1.8, color=GOOD), Scope(width=4.4, height=1.8, color=BAD)).arrange(RIGHT, buff=0.8).move_to(DOWN * 1.9)
        sc[0].set_wave(np.tile(d["waves"][0], 2), gain=0.9)
        sc[1].set_wave(np.tile(d["waves"][-1], 2), gain=0.9)
        st = VGroup(label(r"played softly", font_size=24, color=GOOD).next_to(sc[0], UP, buff=0.1),
                    label(r"played very loud, \ then turned down to match", font_size=24, color=BAD).next_to(sc[1], UP, buff=0.1))
        with self.voiceover(
            "Is anything in music that loud? Inside a brass instrument, yes. <bookmark mark='a'/> In a trombone "
            "played softly, the wave would need twenty-five metres of tube to break, and the tube is under three. "
            "Played as loudly as possible, it breaks in little more than one. <bookmark mark='b'/> In 1996 a group "
            "in Eindhoven and Le Mans measured exactly that: shock waves coming out of a trombone. The hard, "
            "brilliant edge of loud brass is not made by the player's lips. It is made by the air in the tube. "
            "<bookmark mark='c'/> Here is the simulated wave before and after steepening, played at the same "
            "loudness, so that all you hear is the change of shape."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), FadeIn(tube), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(sc), FadeIn(st))
        with self.listen(c) as snd:
            window(snd, r"the gentle wave, \ then the steep one", detail=r"the simulated shape, repeated", corner=DL, tag_corner=DR)
            for ev, k in (("soft", 0), ("loud", 1)):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                w = d["waves"][0 if k == 0 else -1]
                snd.drive(sc[k], lambda m, t, w=w, t0=t0: m.set_wave(np.roll(np.tile(w, 2), -int((t - t0) * 90) % len(w)), gain=0.9))
                snd.wait_until(t0 + 1.6)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        items = VGroup(
            label(r"open, \ and active", font_size=28, color=LIMIT),
            label(r"brassiness as a design number: \ which bores go bright, \ and how soon \ (Gilbert, Campbell, Myers and others)", font_size=24),
            label(r"thermoacoustics: \ sound made by heat (a flame in a tube sings: Rijke, 1859), \ and engines and "
                  r"refrigerators with no moving parts", font_size=24),
            label(r"the same instability shakes rocket engines and gas turbines apart", font_size=24),
            label(r"Krakatoa's pulse was a wave of this kind: \ its modern relative is the 2022 Tonga eruption, \ recorded by "
                  r"thousands of barometers", font_size=24),
            label(r"$\bigstar$ \ Simulate a trombone's bore with the steepening left in, \ and predict when its tone turns brassy.",
                  font_size=24, color=TUNE),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        if items.width > 13.2:
            items.scale_to_fit_width(13.2)
        items.move_to(ORIGIN)
        with self.voiceover(
            "This is live research. Instrument makers now compute a number, called brassiness, that says how soon a "
            "given bore will go bright. <bookmark mark='a'/> Beyond music, the link between sound and heat runs both "
            "ways: a flame in a tube will sing, and a loud enough sound in a tube will pump heat, which gives engines "
            "and refrigerators with no moving parts. <bookmark mark='b'/> The same effect, unwanted, can shake a "
            "rocket engine apart. <bookmark mark='c'/> And Krakatoa has a modern relative: the eruption in Tonga in "
            "2022 sent a pressure pulse round the world that thousands of barometers recorded. "
            "<bookmark mark='d'/> The research problem for this part is the trombone."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(items[1]))
            for mark, it in zip("abcd", items[2:]):
                vo.wait_until(mark)
                self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
