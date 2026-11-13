from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Wave(SoundScene):
    def construct(self):
        chapter(self, 2, r"A wave that sorts", r"How does a tube of fluid tell one frequency from another?", lit=(1863,),
                extra=((1928, r"B\'ek\'esy sees the travelling wave"),))
        self.unroll()
        self.film()
        self.places()
        self.map()
        self.cells()

    # ------------------------------------------------------------------
    def unroll(self):
        d = load("wave")
        ear = ear_diagram()
        spiral = ear.cochlea.copy().move_to(UP * 1.3).scale(1.2)
        co = Cochlea(width=9.6).move_to(DOWN * 0.3)
        facts = VGroup(label(rf"{d['length_mm']:.0f} mm long, \ two and a half turns", font_size=26, color=GREY_A),
                       label(r"a membrane runs its whole length", font_size=26, color=BONE)).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.45)
        harp = VGroup(*[Line(co.p(mm, 0.12 + 0.012 * mm), co.p(mm, -0.12 - 0.012 * mm), color=RATIO, stroke_width=2) for mm in np.arange(1, 35, 1.4)])
        hl = label(r"Helmholtz: \ a harp of resonators, \ each with its own note", font_size=26, color=RATIO).move_to(UP * 1.5)
        card = history_card(1928, r"Georg von B\'ek\'esy, \ Budapest",
                            r"a telephone engineer: opens the cochlea, scatters silver dust on the membrane, and watches "
                            r"it under a flashing light", width=6.2).move_to(DOWN * 2.6 + LEFT * 2.8)
        saw = label(r"he sees no harp. \\ He sees a wave that travels.", font_size=30, color=EAR).move_to(DOWN * 2.6 + RIGHT * 3.6)
        with self.voiceover(
            "Unroll the cochlea. <bookmark mark='a'/> It is a tube thirty-five millimetres long, and a membrane "
            "runs down the whole length of it, dividing the fluid in two. The membrane is not the same all the "
            "way along. At the base, by the window where the stirrup pushes, it is narrow and stiff. Towards the "
            "far end, the apex, it grows wider and slacker, hundreds of times slacker. <bookmark mark='b'/> "
            "Helmholtz took the obvious meaning from that: a harp. Short stiff strings at one end for the high "
            "notes, long slack ones at the other for the low notes, each answering to its own frequency, like the "
            "glass globes of Part 3. <bookmark mark='c'/> In 1928 a Hungarian telephone engineer, Georg von Békésy, "
            "decided to look. He opened cochleas, scattered fine silver dust on the membrane, and watched it "
            "under a flashing light. <bookmark mark='d'/> He did not see a harp. He saw a wave, travelling from "
            "the base towards the apex."
        ) as vo:
            self.play(Create(spiral), run_time=1.2)
            vo.wait_until("a")
            self.play(ReplacementTransform(spiral, co.membrane), FadeIn(co.mid), FadeIn(co.axis), FadeIn(co.marks), FadeIn(co.unit),
                      FadeIn(co.base), FadeIn(co.apex), FadeIn(facts), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(facts), LaggedStart(*[Create(h) for h in harp], lag_ratio=0.05), FadeIn(hl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(card))
            vo.wait_until("d")
            self.play(FadeOut(harp), FadeOut(hl), FadeIn(saw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def film(self):
        d = load("wave")
        row = next(r for r in d["rows"] if r["hz"] == 1000.0)
        co = Cochlea(width=10.4, scale=1.15).move_to(UP * 0.55)
        tr = co.trace(TUNE)
        counter = film(tr, d["frames"], loop=True)
        lens = co.lens(d["env_1000"], color=TUNE, opacity=0.16)
        head = label(r"Monochord's cochlea: \ a tone of 1000 Hz", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        how = VGroup(label(r"2000 slices of membrane, \ each a mass on its own spring,", font_size=24, color=GREY_B),
                     label(r"joined by the fluid they all sit in", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.06).move_to(DOWN * 2.2)
        peak = co.pin(row["peak_mm"], rf"peak: \ {row['peak_mm']:.1f} mm", color=TUNE, up=1.45)
        own = co.pin(row["resonant_mm"], r"", color=GOOD, up=0.9)
        zones = VGroup(
            label(r"here the slices are stiff and quick: \\ they follow the wave easily, \ and pass it on", font_size=22, color=AIR),
            label(r"here a slice's own note is 1000 Hz: \\ the wave slows, \ piles up, \ and is absorbed", font_size=22, color=GOOD),
            label(r"here the slices are too slow \\ to follow at all", font_size=22, color=GREY_B),
        )
        zones[0].move_to(co.p(6.5) + DOWN * 2.2)
        zones[1].move_to(co.p(19.5) + DOWN * 3.25)
        zones[2].move_to(co.p(30.5) + DOWN * 2.2)
        run(counter, 7.0)
        with self.voiceover(
            "Here is that wave in Monochord's own cochlea. The model is simple: two thousand slices of membrane, "
            "each one a mass on a spring of its own, stiff at the base and slack at the apex, all coupled by the "
            "fluid they sit in. We push on the base a thousand times a second, and slow the film down. "
            "<bookmark mark='a'/> The wave enters at the left and runs along the membrane, quickly at first. Then "
            "it slows, its ripples crowd together, and it grows, to a peak "
            f"{say(row['peak_mm'], 1)} millimetres from the base. <bookmark mark='b'/> And then, within a couple "
            "of millimetres, it is gone. Nothing reaches the apex at all. <bookmark mark='c'/> Why does it stop? "
            "Each slice has a note of its own, high at the base and low at the apex. Near the base the slices are "
            "tuned far above a thousand hertz. They are stiff and quick, they follow the push easily and hand the "
            "wave on. <bookmark mark='d'/> Further along, the wave reaches slices whose own note is close to a "
            "thousand hertz. There the membrane resonates, the wave slows almost to a halt, and its energy is "
            "absorbed. <bookmark mark='e'/> Beyond that place the slices are too slack and slow to follow a "
            "thousand hertz at all, so there is nothing to carry the wave further. Helmholtz and Békésy were "
            "both right. There is a wave, and it ends at a resonance."
        ) as vo:
            self.play(FadeIn(co), FadeIn(tr), FadeIn(head), FadeIn(how))
            vo.wait_until("a")
            self.play(FadeIn(lens), run_time=1.0)
            self.wait(max(vo.until("b") - 2.5, 0.1))
            self.play(FadeIn(peak))
            vo.wait_until("c")
            self.play(FadeOut(how), FadeIn(zones[0]))
            vo.wait_until("d")
            self.play(FadeIn(zones[1]), FadeIn(own))
            vo.wait_until("e")
            self.play(FadeIn(zones[2]))
        self.wait(0.3)
        halt(counter)
        self.clear_scene()

    # ------------------------------------------------------------------
    def places(self):
        d = load("wave")
        c = clip("wave.glide")
        co = Cochlea(width=10.4, scale=1.3).move_to(UP * 0.5)
        head = label(r"seven tones, \ each an octave above the last", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Change the frequency and the peak moves. Listen to seven tones, each an octave above the one "
            "before, from a hundred and twenty-five hertz to eight thousand, and watch where each one's wave "
            "comes to rest."
        ):
            self.play(FadeIn(co), FadeIn(head))
        lenses, pins = [], []
        for r in d["rows"]:
            hz = int(r["hz"])
            col = harmonic_color(1) if False else interpolate_color(ManimColor(AIR), ManimColor(BAD), np.log2(hz / 125) / 6)
            lenses.append(co.lens(d[f"env_{hz}"], color=col, opacity=0.35))
            pins.append(co.pin(r["peak_mm"], rf"${hz_name(hz)}$", color=col, font_size=24, up=1.55))
        with self.listen(c) as snd:
            window(snd, r"125 Hz to 8000 Hz, \ an octave at a time", kind="synthesized", detail=r"pure tones", corner=DL, tag_corner=DR)
            for r, ln, pn in zip(d["rows"], lenses, pins):
                t0 = snd.time_of(f"t{int(r['hz'])}")
                snd.wait_until(t0)
                ln.set_amp(0.0)
                self.add(ln, pn)
                snd.drive(ln, lambda m, t, t0=t0: m.set_amp((0.82 + 0.18 * np.sin(40 * (t - t0))) if t0 <= t < t0 + 0.8
                                                            else (0.45 if t >= t0 + 0.8 else 0.0)))
        for ln in lenses:
            ln.set_amp(0.45)
        step = d["mm_per_octave"]
        br = VGroup()
        for a, b in zip(pins[:-1], pins[1:]):
            x0, x1 = b[0].get_start()[0], a[0].get_start()[0]
            br.add(Line([x0 + 0.04, 0, 0], [x1 - 0.04, 0, 0], color=RATIO, stroke_width=3).set_y(co.p(0)[1] - 0.55))
        bl = label(rf"each octave: \ the same {step:.1f} mm", font_size=28, color=RATIO).move_to(co.p(18)[0] * RIGHT + (co.p(0)[1] - 2.25) * UP)
        with self.voiceover(
            "High tones stop near the base. Low tones travel all the way to the apex. And notice the spacing. "
            f"<bookmark mark='a'/> Every octave moved the peak by the same distance, {say(step, 1)} millimetres. "
            "Equal ratios of frequency are equal distances along the membrane. The cochlea is a keyboard, rolled "
            "up, and it measures frequency the way music does: by ratio."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in br], lag_ratio=0.15), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def map(self):
        d = load("wave")
        step = d["mm_per_octave"]
        g = faxes(60, 20000, [0, 35], x_length=6.6, y_length=3.9, ylabel=r"place of the peak (mm from the base)", yticks=[0, 10, 20, 30],
                  fticks=(100, 1000, 10000), font_size=20)
        g.move_to(RIGHT * 2.9 + DOWN * 0.2)
        mod = fcurve(g, d["map_hz"], d["map_mm"], TUNE)
        # Greenwood's function, drawn the other way round: the frequency whose place is x
        xs = np.linspace(0.5, 34.5, 120)
        from explainer.music.monochord import ear as E
        gw = fcurve(g, E.greenwood(xs / 1000), xs, GOOD)
        leg = VGroup(label(r"Monochord's model", font_size=24, color=TUNE), label(r"measured in human ears (Greenwood, 1990)", font_size=24, color=GOOD)
                     ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(g, UP, buff=0.3)
        ask = pause_card(r"A tone of 1000 Hz peaks 18.7 mm from the base. \\ Where does a tone of 3000 Hz peak?", width=5.6).move_to(LEFT * 3.9 + UP * 1.2)
        oct_ = np.log2(3.0)
        ans = VGroup(MathTex(rf"\log_2 3 = {oct_:.2f}\ \text{{octaves up}}", font_size=30),
                     MathTex(rf"{oct_:.2f}\times{step:.1f} = {oct_ * step:.1f}\ \text{{mm towards the base}}", font_size=30),
                     MathTex(rf"18.7 - {oct_ * step:.1f} = {18.7 - oct_ * step:.1f}\ \text{{mm}}", font_size=34, color=GOOD)
                     ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 3.9 + DOWN * 1.6)
        with self.voiceover(
            "Use that. A thousand hertz peaks eighteen point seven millimetres from the base. Where does three "
            "thousand hertz peak? Pause and work it out."
        ):
            self.play(FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Three thousand is a ratio of three above a thousand, which is {say(oct_, 2)} octaves. At "
            f"{say(step, 1)} millimetres an octave that is {say(oct_ * step, 1)} millimetres closer to the base: "
            f"{say(18.7 - oct_ * step, 1)} millimetres. <bookmark mark='a'/> Here is the whole map of our model, "
            "frequency against place: a straight line, because the frequency axis is logarithmic. "
            "<bookmark mark='b'/> And here is the map measured in human ears, collected by Donald Greenwood. Over "
            "most of the range the two run side by side. At the low end the real ear bends: below about five "
            "hundred hertz it packs its octaves closer together. Remember that bend. It is the reason bass notes "
            "are harder to tell apart, and it will matter in the next chapter."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(a) for a in ans], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(g), Create(mod), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(gw), FadeIn(leg[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cells(self):
        d = load("wave")
        co = Cochlea(width=10.4, names=False, ticks=()).move_to(UP * 1.6)
        co.remove(co.axis, co.unit)
        inner = VGroup(*[Dot(co.p(mm) + DOWN * 0.45, radius=0.035, color=EAR) for mm in np.linspace(0.3, 34.7, 110)])
        outer = VGroup(*[Dot(co.p(mm) + DOWN * (0.75 + 0.14 * k), radius=0.028, color=LIMIT) for k in range(3) for mm in np.linspace(0.3, 34.7, 110)])
        rows = VGroup(
            label(rf"one row of inner hair cells: \ about {d['inner']:,}".replace(",", "{,}"), font_size=28, color=EAR),
            label(rf"each bends with the membrane beneath it, \ and signals to the brain along {d['fibres']:,} nerve fibres".replace(",", "{,}"), font_size=26, color=GREY_A),
            label(rf"three rows of outer hair cells: \ about {d['outer']:,}".replace(",", "{,}"), font_size=28, color=LIMIT),
            label(r"these send almost nothing to the brain. \ What are they for? \quad $\rightarrow$ chapter 11", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(DOWN * 1.2)
        with self.voiceover(
            "One more thing sits on the membrane, and it is the part that hears. <bookmark mark='a'/> Along its "
            f"whole length runs a single row of inner hair cells, about {say(d['inner'])} of them in each ear. "
            "When the membrane beneath a hair cell moves, the cell's hairs bend, and it signals the brain. "
            f"<bookmark mark='b'/> About {say(d['fibres'])} nerve fibres carry those signals, and each fibre "
            "comes from one place, so each fibre has one best frequency. That is the first of the ear's two "
            "codes: which fibres are firing says which frequencies are present. <bookmark mark='c'/> Beside them "
            f"are three more rows, the outer hair cells, about {say(d['outer'])}. They outnumber the inner cells "
            "three to one, and yet they send almost nothing to the brain. <bookmark mark='d'/> What they are for "
            "was a mystery for a century. Hold that thought until the last chapter."
        ) as vo:
            self.play(FadeIn(co))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in inner], lag_ratio=0.01), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in outer], lag_ratio=0.004), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
