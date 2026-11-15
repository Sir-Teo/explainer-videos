from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Parcels(SoundScene):
    def construct(self):
        chapter(self, 2, r"What moves", r"If the air does not travel, \ what does?", lit=(1687,))
        self.pulse()
        self.tone()
        self.pressure_and_velocity()
        self.sizes()

    # ------------------------------------------------------------------
    def pulse(self):
        d = load("parcels")
        row = ParcelRow(n=61, width=11.0, rows=7, gap=0.2, gain=0.42 / d["pulse_scale"]).place(UP * 0.9)
        marked = [k * 61 + 30 for k in range(7)]
        for k in marked:
            row.dots[k].set_color(TUNE).scale(1.5)
        piston = Rectangle(width=0.18, height=1.7, stroke_width=0, fill_color=GREY_B, fill_opacity=1)
        piston.add_updater(lambda m: m.move_to(row.dots[0].get_center() * RIGHT + UP * 0.9 + LEFT * 0.2))
        tr = film(row, d["pulse"])
        caps = VGroup(label(r"each dot: \ a parcel of air", font_size=26, color=AIR),
                      label(r"one parcel, \ marked", font_size=26, color=TUNE)).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.6)
        facts = VGroup(label(r"the push travels the length of the row", font_size=30),
                       label(r"each parcel moves only a little", font_size=30, color=TUNE)).arrange(DOWN, buff=0.25).move_to(DOWN * 2.1)
        with self.voiceover(
            "Picture the air in a long tube as a row of small parcels, each one touching the next. "
            "<bookmark mark='a'/> Push the first one. It crowds its neighbour. The crowded air pushes back, and "
            "pushes forward, so the neighbour moves, and crowds the next. <bookmark mark='b'/> The push runs down "
            "the row. But watch the marked parcel. It is shoved forward, and then it stops, and it stays about where "
            "it was. <bookmark mark='c'/> That is the answer to the Krakatoa question. What crossed the Indian Ocean "
            "was not air. It was a push, handed from each parcel of air to the next."
        ) as vo:
            self.play(FadeIn(row), FadeIn(piston), FadeIn(caps))
            vo.wait_until("a")
            duration = max(vo.until("c") - 0.2, 6.0)
            slow = duration / ((len(d["pulse"]) - 1) * d["pulse_dt"])
            scale_note = label(rf"motion slowed {slow:.0f} times; \ displacement exaggerated",
                               font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
            self.add(scale_note)
            self.play(tr.animate.set_value(len(d["pulse"]) - 1), run_time=duration, rate_func=linear)
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
        piston.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tone(self):
        d = load("parcels")
        row = ParcelRow(n=61, width=11.0, rows=7, gap=0.2, gain=0.16).place(UP * 1.9)
        tr = film(row, d["tone_xi"], loop=True)
        g = axes([0, 1], [-1.3, 1.3], x_length=11.0, y_length=1.9, xlabel=r"", ylabel=r"pressure", xticks=[], yticks=[0],
                 font_size=20)
        g.move_to(DOWN * 0.55)
        xs = np.linspace(0, 1, 61)
        pc = curve(g.ax, xs, d["tone_p"][0], FORCE, stroke_width=3)

        def upd(m):
            f = tr.get_value() % (len(d["tone_p"]) - 1)
            i = int(f)
            a = f - i
            y = (1 - a) * d["tone_p"][i] + a * d["tone_p"][i + 1]
            m.set_points_as_corners([g.ax.c2p(x, v) for x, v in zip(xs, y)])

        pc.add_updater(upd)
        tags = VGroup(label(r"crowded: \ pressure above normal", font_size=24, color=FORCE),
                      label(r"spread out: \ pressure below normal", font_size=24, color=AIR)).arrange(RIGHT, buff=1.0)
        tags.next_to(g, DOWN, buff=0.2)
        card = definition_card(r"Sound", r"a travelling disturbance of the pressure of the air: \ each parcel swings "
                               r"back and forth about its own place, \ and hands its motion on", width=10.4, font_size=26)
        card.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now push and pull the end of the row steadily, as a vibrating string or a loudspeaker would. "
            "<bookmark mark='a'/> Bands of crowding move down the tube, with bands of thinning between them. "
            "Underneath is the pressure along the tube: above normal where the parcels are crowded, below normal "
            "where they are spread. <bookmark mark='b'/> That travelling pattern of pressure is the sound. Each "
            "parcel only swings back and forth about its own place, along the direction the sound is going. A wave "
            "like that is called longitudinal. The string of Part 1 moved across its length; the air moves along it."
        ) as vo:
            self.play(FadeIn(row), FadeIn(g), FadeIn(pc))
            self.play(tr.animate.set_value(vo.until("a") * 9), run_time=vo.until("a"), rate_func=linear)
            self.add(tags)
            start = tr.get_value()
            self.play(tr.animate.set_value(start + vo.until("b") * 9), run_time=vo.until("b"), rate_func=linear)
            self.add(card)
            start = tr.get_value()
            left = vo.remaining() + 0.1
            self.play(tr.animate.set_value(start + left * 9), run_time=left, rate_func=linear)
        pc.clear_updaters()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pressure_and_velocity(self):
        d = load("parcels")
        head = label(r"How hard the air is pushed, \ and how fast it moves", font_size=34, color=GREY_A).to_edge(UP, buff=0.5)
        rows = [
            MathTex(r"\rho\,\frac{\partial u}{\partial t}", r"=", r"-\,\frac{\partial p}{\partial x}", font_size=42),
            MathTex(r"\frac{\partial}{\partial t}", r"=", r"-\,c\,\frac{\partial}{\partial x}", font_size=42),
            MathTex(r"p", r"=", r"\rho\, c\; u", font_size=52),
            MathTex(r"\langle I\rangle", r"=", r"\langle p\,u\rangle \;=\; \frac{p_{\rm rms}^2}{\rho c}", font_size=42),
        ]
        whys = [why(r"Newton's law for one parcel: \ it is pushed by the difference in pressure across it"),
                why(r"a plane wave travelling right at speed $c$"),
                why(r"pressure and velocity rise and fall together"),
                why(r"mean power per square metre; \ rms pressure")]
        rows[2][0].set_color(FORCE), rows[2][2].set_color(AIR), rows[3][0].set_color(LEVEL)
        step = ladder(self, rows, whys, keep=4, top=1.7, buff=0.55, x=-2.4)
        num = label(rf"$1$ Pa rms: \ {d['one_pa']['mm_s']:.1f} mm/s rms \quad ($\rho c\approx {d['z']:.0f}$)",
                    font_size=28, color=TUNE)
        num.move_to(UP * 2.65)
        symbols = label(r"$p$: \ pressure change; \ $u$: \ particle velocity", font_size=23,
                        color=GREY_B).move_to(UP * 2.65)
        parcel = Rectangle(width=1.2, height=1.0, color=AIR, fill_opacity=0.12)
        left_push = Arrow(LEFT * 3.0, LEFT * 0.65, color=FORCE, buff=0, stroke_width=6)
        right_push = Arrow(RIGHT * 2.0, RIGHT * 0.65, color=FORCE, buff=0, stroke_width=3)
        intro = VGroup(parcel, left_push, right_push,
                       label(r"higher pressure", font_size=25, color=FORCE).next_to(left_push, UP, buff=0.25),
                       label(r"lower pressure", font_size=25, color=GREY_A).next_to(right_push, UP, buff=0.25),
                       label(r"one parcel", font_size=25, color=AIR).next_to(parcel, DOWN, buff=0.3))
        with self.voiceover(
            "There is one relation between the push and the motion that we will need again and again. A parcel "
            "speeds up when the pressure behind it is higher than the pressure in front: <bookmark mark='a'/> that "
            "is Newton's law. <bookmark mark='b'/> In a plane wave travelling in one direction, the pattern slides at the speed "
            "of sound, so a change in time is the same as a change in place. <bookmark mark='c'/> Put the two "
            "together and the pressure is simply the density, times the speed of sound, times the speed of the "
            f"air. In a room that product is about {say(d['z'])}, <bookmark mark='d'/> so a pressure swing of one "
            f"pascal rms gives a particle velocity of {say(d['one_pa']['mm_s'], 1)} millimetres a second rms. "
            "<bookmark mark='e'/> Instantaneous intensity is pressure times particle velocity. Average it in time "
            "and you get rms pressure squared, over rho c. That is the relation for this progressive plane wave; "
            "reflections can change it. It is why sound level will use rms pressure, squared."
        ) as vo:
            self.play(FadeIn(head), FadeIn(symbols), FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.3)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(symbols), FadeIn(num))
            vo.wait_until("e")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sizes(self):
        d = load("parcels")
        head = VGroup(*[label(t, font_size=24, color=GREY_B) for t in
                        (r"", r"level", r"pressure (rms)", r"of one atmosphere", r"peak motion (1 kHz tone)")])
        xs = [-6.5, -3.5, -2.1, 0.1, 3.5]
        rows = VGroup()
        for i, r in enumerate(d["sizes"]):
            move = (rf"{r['nm_1khz']:.1f} nm" if r["nm_1khz"] < 1 else rf"{r['nm_1khz']:.0f} nm") if r["nm_1khz"] < 1000 else rf"{r['nm_1khz'] / 1000:.0f} $\mu$m"
            inv = 1 / r["atm"]
            atm = r"1 part in %s" % (f"{inv / 1e6:.0f} million" if inv >= 1e6 else f"{round(inv, -2):,.0f}".replace(",", "{,}"))
            pa = rf"{r['pa'] * 1000:.1f} mPa" if r["pa"] < 0.01 else (rf"{r['pa']:.2f} Pa" if r["pa"] < 1 else rf"{r['pa']:.0f} Pa")
            rows.add(VGroup(label(r["name"], font_size=28), label(rf"{r['db']} dB", font_size=28, color=LEVEL),
                            label(pa, font_size=28, color=FORCE), label(atm, font_size=28, color=GREY_A),
                            label(move, font_size=28, color=TUNE)))
        for j, h in enumerate(head):
            h.move_to([xs[j], 2.3, 0], aligned_edge=LEFT)
        for i, r in enumerate(rows):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 1.4 - 0.85 * i, 0], aligned_edge=LEFT)
        scale = VGroup(label(r"for scale: \ a hair is about 70 $\mu$m across; \ an atom, \ a tenth of a nanometre", font_size=26,
                             color=GREY_A)).to_edge(DOWN, buff=0.6)
        talk = d["sizes"][1]
        with self.voiceover(
            "How big is this motion? Astonishingly small. <bookmark mark='a'/> Ordinary speech changes the pressure "
            f"of the air by about two hundredths of a pascal rms: one part in {say(1 / talk['atm'] / 1e6)} million of the "
            f"atmosphere's own pressure. A one-kilohertz tone at that level has a peak parcel displacement of about "
            f"{say(talk['nm_1khz'])} nanometres: <bookmark mark='b'/> around a hundred atoms' width. "
            "<bookmark mark='c'/> At an orchestra's hundred-decibel level, the same tone would move the air about "
            "a thousandth of a millimetre. And a sound loud enough to hurt is still less "
            "than a thousandth of an atmosphere. <bookmark mark='d'/> So for music, the disturbance is tiny compared "
            "with the air it rides on. That is why sounds pass through each other untouched, and why the simple "
            "wave equation of Part 1 works so well. In the last chapter we will see what happens when it is not tiny."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(scale))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Indicate(rows[3][3], color=TUNE, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()
