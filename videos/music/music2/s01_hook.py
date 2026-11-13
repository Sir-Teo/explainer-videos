from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.krakatoa()
        self.barographs()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        t = load("tune")
        c = clip("krakatoa.opening")
        fills = {k["degree"]: k["fill"] for k in t["checks"]}
        row = bottle_row(fills, height=3.0, gap=0.6).move_to(UP * 0.2)
        words = VGroup(*[label(w, font_size=30, color=GREY_B) for w in ("Twin-", "kle,", "twin-", "kle,", "lit-", "tle", "star,")])
        words.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(row), FadeIn(words), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"six bottles, \ struck on the mouth")
            for k, n in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                p = puff(row, n["degree"])
                snd.show(p)
                snd.drive(p, ring(at=n["t"], rate=7.0))
                words[k].set_color(TUNE)
                row.by[n["degree"]][-1].set_color(TUNE)
                if k:
                    row.by[c.notes[k - 1]["degree"]][-1].set_color(TUNE if c.notes[k - 1]["degree"] == n["degree"] else GREY_B)
        with self.voiceover(
            "No string this time. Six bottles, each with a different amount of water in it, and the only thing "
            "making that sound is air. By the end of this part you will know how much water goes in each one. "
            "But first, the loudest sound anyone has ever written down."
        ):
            self.play(row.animate.scale(0.8).shift(UP * 0.3), FadeOut(words))
        self.clear_scene()

    # ------------------------------------------------------------------
    def krakatoa(self):
        d = load("krakatoa")
        head = VGroup(label(r"27 August 1883", font_size=40, color=HIST), label(r"Krakatoa", font_size=40)).arrange(RIGHT, buff=0.5)
        head.to_edge(UP, buff=0.45)
        # a strip of ocean: the volcano at the right, distance running left (west) to Rodrigues
        x0, x1 = 5.6, -5.6
        km_max = 5200.0

        def X(km):
            return x0 + (x1 - x0) * km / km_max

        sea = Line([x1, -0.6, 0], [x0, -0.6, 0], color=GREY_D, stroke_width=2)
        vol = VGroup(Triangle(color=BAD, fill_opacity=0.9).scale(0.28), label(r"Krakatoa", font_size=24, color=BAD))
        vol[0].move_to([x0, -0.35, 0])
        vol[1].next_to(vol[0], UP, buff=0.15)
        marks = VGroup()
        for row in d["rows"]:
            dot = Dot([X(row["km"]), -0.6, 0], radius=0.07, color=AIR)
            name = label(row["place"], font_size=24).next_to(dot, DOWN, buff=0.2)
            km = label(rf"{row['km']:,} km".replace(",", "{,}"), font_size=22, color=RATIO).next_to(name, DOWN, buff=0.1)
            hrs = label(rf"{row['hours'] * 60:.0f} min" if row["hours"] < 1 else rf"{row['hours']:.1f} hours",
                        font_size=22, color=TIME).next_to(km, DOWN, buff=0.1)
            marks.add(VGroup(dot, name, km, hrs))
        marks[0][1:].shift(LEFT * 0.5)
        front = Line([x0, -0.6, 0], [x0, 1.4, 0], color=AIR, stroke_width=5)
        clock = label(r"0.0 hours after the explosion", font_size=28, color=TIME).move_to(UP * 2.2)
        tr = ValueTracker(0.0)
        front.add_updater(lambda m: m.set_x(X(min(tr.get_value(), 4.7) * 3600 * d["speed_obs"] / 1000)))
        clock.add_updater(lambda m: m.become(label(rf"{tr.get_value():.1f} hours after the explosion", font_size=28,
                                                   color=TIME).move_to(UP * 2.2)))
        quote = label(r"``like the distant roar of heavy guns''", font_size=30, color=GREY_A).move_to(UP * 1.3 + LEFT * 2.8)
        with self.voiceover(
            "On the twenty-seventh of August, 1883, the volcano Krakatoa, between Java and Sumatra, blew itself "
            "apart. <bookmark mark='a'/> In Batavia, a hundred and sixty kilometres away, the pressure gauge at the "
            "gasworks leapt off its scale. <bookmark mark='b'/> In Perth, three thousand kilometres away, people "
            "heard what they took for artillery. <bookmark mark='c'/> And on the island of Rodrigues, "
            "four thousand eight hundred kilometres across the Indian Ocean, the chief of police wrote down a sound "
            "like the distant roar of heavy guns. "
            f"<bookmark mark='d'/> It reached him about {say(d['rows'][2]['hours'])} hours after the explosion."
        ) as vo:
            self.play(FadeIn(head), Create(sea), FadeIn(vol), FadeIn(front), FadeIn(clock))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), tr.animate.set_value(d["rows"][0]["hours"]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), tr.animate.set_value(d["rows"][1]["hours"]), run_time=max(vo.until("c") - 0.2, 1.0),
                      rate_func=linear)
            self.play(FadeIn(marks[2]), tr.animate.set_value(d["rows"][2]["hours"]), run_time=max(vo.until("d") - 0.5, 1.0),
                      rate_func=linear)
            self.play(FadeIn(quote))
        front.clear_updaters()
        clock.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def barographs(self):
        d = load("krakatoa")
        T = d["circuit_hours"]
        ax = axes([0, 126], [-1.2, 1.6], x_length=11.0, y_length=2.6, xlabel=r"hours after the explosion",
                  ylabel=r"air pressure at one station", xticks=[0, 24, 48, 72, 96, 120], yticks=[], font_size=20)
        ax.move_to(UP * 0.7)
        # one station a quarter of the way round: the pulse passes outward bound, then homeward bound, lap after lap
        t0 = 0.25 * T
        times = sorted([t0 + k * T for k in range(4)] + [T - t0 + k * T for k in range(3)])
        hrs = np.linspace(0, 126, 1600)
        y = 0.05 * np.sin(hrs / 3.1) + 0.04 * np.sin(hrs / 1.3 + 1.0)
        for i, t in enumerate(times):
            y += (1.0 * 0.78 ** i) * np.exp(-((hrs - t) / 0.7) ** 2) * (1 if i % 2 == 0 else -1)
        trace = curve(ax.ax, hrs, y, AIR, stroke_width=2.5)
        nums = VGroup(*[label(str(i + 1), font_size=24, color=TUNE).move_to(ax.ax.c2p(t, 1.35 if i % 2 == 0 else -1.0))
                        for i, t in enumerate(times)])
        tag = label(r"schematic: \ the times are computed, \ the shape of the trace is drawn", font_size=20, color=GREY_B)
        tag.next_to(ax, DOWN, buff=0.15)
        sums = VGroup(
            MathTex(r"\frac{40{,}000\ \text{km}}{%.0f\ \text{hours}}" % T, r"\;\approx\;", r"%.0f\ \text{m/s}" % d["speed_obs"],
                    font_size=44),
            label(r"the speed of sound", font_size=34, color=TUNE)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.7)
        sums[0][2].set_color(TUNE)
        with self.voiceover(
            "Then something stranger. Weather stations keep barographs: pens that trace the pressure of the air on a "
            "slowly turning drum. <bookmark mark='a'/> Over the next five days, pens all round the world twitched, "
            "and twitched again: seven times in all. It was the same pulse of pressure, running out to the far side "
            f"of the planet and back, each lap taking about {say(T)} hours. <bookmark mark='b'/> Divide the distance "
            f"by the time, and you get a little over three hundred metres a second. That is the speed of sound."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(trace), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.9), run_time=max(vo.until("b") - 0.3, 4.0),
                      rate_func=linear)
            self.play(FadeIn(sums))
        self.wait(0.3)
        self.play(FadeOut(sums), FadeOut(tag), run_time=0.4)
        qs = VGroup(label(r"What was it that travelled?", font_size=36, color=TUNE),
                    label(r"Why at that speed?", font_size=36, color=TUNE),
                    label(r"Why does sound fade, \ bend round corners, \ hum in a bottle, \ drop in pitch as it passes?",
                          font_size=32, color=EAR)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "So what was it that travelled? Not the air: no wind crosses an ocean in four hours. "
            "<bookmark mark='a'/> Why that speed, and no other? <bookmark mark='b'/> And why does sound do the odd "
            "things it does: fade with distance, bend round corners, hum one note in a bottle, and drop in pitch as "
            "it goes by?"
        ) as vo:
            self.play(FadeIn(qs[0]))
            vo.wait_until("a")
            self.play(FadeIn(qs[1]))
            vo.wait_until("b")
            self.play(FadeIn(qs[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Waves in Air", font_size=46).to_edge(UP, buff=0.35)
        smap = series_map(current=PART, done=PART - 1, height=6.3).next_to(title, DOWN, buff=0.3)
        obj = objectives_card([
            r"sound is a wave of pressure: \ what moves, \ and how little",
            r"its speed, \ from the gas law: \ Newton's mistake and Laplace's correction",
            r"loudness in numbers: \ intensity, \ the decibel, \ the inverse-square law",
            r"wavelength: \ why bass bends round a wall and treble does not; \ interference",
            r"air in a pipe and in a bottle: \ the notes of a tube, \ Helmholtz's resonator",
            r"impedance, \ a moving source, \ and what happens when sound is too loud",
        ], font_size=26).move_to(DOWN * 0.25)
        with self.voiceover(
            "This is Part 2 of Music, Built. In Part 1 we found out why a string has a pitch. A string on its own is "
            "nearly silent, though. What reaches your ear is the air. <bookmark mark='a'/> In this part: what a sound "
            "wave is, and how small. Where its speed comes from. How loudness is measured. What wavelength does to "
            "sound at a wall and between two sources. Why a pipe and a bottle each have notes of their own. And three "
            "things the simple picture leaves out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
