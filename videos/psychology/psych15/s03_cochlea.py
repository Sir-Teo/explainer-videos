from __future__ import annotations

import numpy as np

from videos.psychology.psych15.common import *  # noqa: F403


class Cochlea(VoiceoverScene):
    def construct(self):
        self.card()
        self.path()
        self.bekesy()
        self.place()
        self.amplifier()
        self.bank()

    def card(self):
        card = chapter_card(2, r"The cochlea", r"How does the ear take a sound apart?",
                            lit={1961: r"von Békésy", 1978: r"Kemp"}, part=PART, scale=("circuit",), marr=("how",))
        with self.voiceover("Chapter two. The cochlea."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def path(self):
        head = heading(r"From the air to the fluid")
        drum = Line([-5.6, 0.6, 0], [-5.6, -0.6, 0], color=SOUND, stroke_width=6)
        dl = label(r"eardrum", font_size=22, color=SOUND).next_to(drum, DOWN, buff=0.15)
        bones = VGroup(Circle(radius=0.18, color=GREY_B), Circle(radius=0.15, color=GREY_B), Circle(radius=0.12, color=GREY_B))
        bones.arrange(RIGHT, buff=0.15).next_to(drum, RIGHT, buff=0.25)
        bl = label(r"three small bones", font_size=22, color=GREY_B).next_to(bones, UP, buff=0.3).shift(RIGHT * 0.3)
        mem = Rectangle(width=7.0, height=0.5, color=PLACE, fill_color=PLACE, fill_opacity=0.15).next_to(bones, RIGHT, buff=0.3)
        base = label(r"base: \ narrow, \ stiff", font_size=21, color=PLACE).next_to(mem, DOWN, buff=0.12).align_to(mem, LEFT)
        apex = label(r"apex: \ wide, \ floppy", font_size=21, color=PLACE).next_to(mem, DOWN, buff=0.12).align_to(mem, RIGHT)
        ml = label(r"the cochlea, \ uncoiled: \ the basilar membrane, \ about 35 mm", font_size=22, color=WHITE).next_to(mem, UP, buff=0.15)
        fig = VGroup(drum, dl, bones, bl, mem, base, apex, ml).move_to([0, 0.8, 0])
        keep_in_frame(fig)
        rows = rows_of([
            (r"the bones concentrate the eardrum's push onto a small window: \ a pressure gain of about twenty", WHITE),
            (r"the cochlea is filled with fluid, \ coiled two and a half turns, \ the size of a pea", GREY_A),
            (r"along it runs a membrane that changes from stiff to floppy: \ the key to everything", PLACE),
        ], 12.6, 27, 0.26).to_edge(DOWN, buff=0.75)
        tag = note(r"drawn, \ not to scale").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Sound has to get from air into the fluid of the inner ear, and most of it would simply bounce off. "
            "<bookmark mark='a'/> The eardrum catches the pressure, and three small bones carry it to a window into "
            "the cochlea about twenty times smaller, concentrating the push: a pressure gain of about twenty. "
            "<bookmark mark='b'/> The cochlea is a fluid-filled tube the size of a pea, coiled two and a half times. "
            "Here it is uncoiled. <bookmark mark='c'/> Along it runs the basilar membrane, about thirty-five "
            "millimetres long, narrow and stiff at the base, near the window, and wide and floppy at the far end, the "
            "apex. That gradient is the key to everything that follows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig[:4]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(fig[4:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(fig[4]))
        self.clear_scene()

    def bekesy(self):
        d = load("cochlea")
        head = heading(r"Von Békésy's travelling wave")
        A = axes([0, 1], [-1.2, 1.2], x_length=10.0, y_length=1.6, xticks=[0, 1], xfmt=lambda v: "base" if v == 0 else "apex",
                 yticks=[], ylabel=r"displacement", center=[0, 1.4, 0])
        ax = A.ax
        frames = {f: d[f"w{f}"] for f in (250, 1000, 4000)}
        k = ValueTracker(0.0)
        cols = {250: SOUND, 1000: PLACE, 4000: TIMING}
        which = {"f": 250}

        def snap():
            arr = frames[which["f"]]
            i = int(k.get_value()) % arr.shape[0]
            return curve(ax, 1 - d["xs"][::-1], arr[i][::-1], cols[which["f"]], stroke_width=3)
        wave = always_redraw(snap)
        fl = label(r"250 Hz", font_size=26, color=SOUND).next_to(A, UP, buff=0.1).align_to(A, RIGHT)
        rows = rows_of([
            (r"1920s to 1940s: \ cochleas from cadavers, \ opened, \ watched under strobe light with silver flakes", WHITE),
            (r"each tone sends a wave from the base toward the apex, \ which grows, \ peaks and dies at one place", PLACE),
            (r"high tones peak near the base, \ low tones near the apex: \ a frequency analyser made of membrane", SOUND),
            (r"Nobel Prize, \ 1961; \ his cochleas were dead, \ so their tuning was broad; \ living ones are sharper", GREY_A),
        ], 12.6, 26, 0.26).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.BEKESY_1960.cite)
        with self.voiceover(
            "How the membrane responds was worked out by Georg von Békésy, a Hungarian telephone engineer turned "
            "physiologist. <bookmark mark='a'/> Through the nineteen-thirties and forties he opened the cochleas of "
            "human cadavers, sprinkled silver flakes on the membrane, and watched it move under a microscope with "
            "strobe lighting. <bookmark mark='b'/> A tone sends a wave along the membrane, from the base toward the "
            "apex. It grows as it travels, reaches a peak at one particular place, and then dies away quickly. "
            "<bookmark mark='c'/> Where it peaks depends on the frequency. A low tone travels almost to the apex; a "
            "high tone peaks near the base. The membrane is a frequency analyser: each place along it responds best to "
            "one frequency. <bookmark mark='d'/> It earned him the Nobel Prize in 1961. One caution. His cochleas were "
            "dead, and their tuning was broad. In living ears, measured decades later, it's far sharper, for a reason "
            "we'll see in a moment."
        ) as vo:
            self.add(wave)
            self.play(FadeIn(head), FadeIn(A), FadeIn(fl), FadeIn(tag))
            vo.wait_until("a")
            self.play(k.animate.set_value(36), FadeIn(rows[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(k.animate.set_value(72), FadeIn(rows[1]), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            which["f"] = 1000
            fl.become(label(r"1000 Hz", font_size=26, color=PLACE).move_to(fl))
            self.play(k.animate.set_value(108), run_time=3.0, rate_func=linear)
            which["f"] = 4000
            fl.become(label(r"4000 Hz", font_size=26, color=TIMING).move_to(fl))
            self.play(k.animate.set_value(144), FadeIn(rows[2]), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        wave.clear_updaters()
        self.clear_scene()

    def place(self):
        d = load("cochlea")
        head = heading(r"A map from place to frequency")
        A = axes([0, 1], [1, 4.4], x_length=7.0, y_length=4.4, xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[1, 2, 3, 4], yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"),
                 xlabel=r"distance from the apex (share of the length)", ylabel=r"best frequency (Hz)",
                 center=[-2.4, -0.3, 0])
        ax = A.ax
        g = curve(ax, d["x"], np.log10(d["bf"]), PLACE, stroke_width=4)
        pts = VGroup()
        for f, key, col in ((250, "place250", SOUND), (1000, "place1000", PLACE), (4000, "place4000", TIMING)):
            pts.add(Dot(ax.c2p(d[key], np.log10(f)), color=col, radius=0.08))
        rows = rows_of([
            (r"Greenwood, \ 1990: \ $f = 165.4\,(10^{2.1x} - 0.88)$", WHITE),
            (r"roughly logarithmic: \ each octave gets a similar stretch of membrane", PLACE),
            (rf"250, \ 1000 and 4000 Hz peak at {d['place250']:.2f}, \ {d['place1000']:.2f} and {d['place4000']:.2f} of the way", GREY_A),
            (r"the map is kept all the way to the cortex: \ tonotopy", TIMING),
        ], 4.8, 26, 0.32).move_to([4.4, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ Greenwood's function for the human cochlea")
        with self.voiceover(
            "The place-to-frequency map has a formula. <bookmark mark='a'/> Donald Greenwood fitted one in 1990, from "
            "data across many species, and for people it runs from about twenty hertz at the apex to twenty thousand "
            "at the base. <bookmark mark='b'/> It's close to logarithmic: each octave gets a similar stretch of "
            "membrane, a few millimetres, which is one reason musical intervals are ratios. <bookmark mark='c'/> Two "
            "hundred and fifty hertz peaks about a fifth of the way from the apex, a thousand hertz two fifths, and "
            "four thousand two thirds. <bookmark mark='d'/> And the map isn't thrown away. The nerve fibres keep it, "
            "the brainstem keeps it, and the primary auditory cortex is laid out by frequency too. It's called "
            "tonotopy, hearing's version of the retina's map."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def amplifier(self):
        head = heading(r"An ear that amplifies itself")
        rows = rows_of([
            (r"about 3{,}500 inner hair cells send the signal; \ about 12{,}000 outer hair cells do something else", WHITE),
            (r"1978: \ Kemp puts a microphone in the ear canal: \ the ear sends sound back out", SOUND),
            (r"outer hair cells change length with voltage \ (Brownell, \ 1985), \ pumping energy into the wave", PLACE),
            (r"the cochlear amplifier: \ sharper tuning, \ 40 to 60 dB more sensitivity; \ lost first in most hearing loss", TIMING),
            (r"those echoes are now a screening test for every newborn's hearing", GREY_A),
        ], 12.6, 28, 0.36).move_to([0, -0.1, 0])
        tag = historical_tag(archive.KEMP_1978.cite)
        with self.voiceover(
            "Why are living cochleas so much sharper than dead ones? <bookmark mark='a'/> The membrane carries two kinds "
            "of hair cell. About three and a half thousand inner hair cells send almost all the signal to the brain. "
            "About twelve thousand outer hair cells, it turned out, do something else. <bookmark mark='b'/> In 1978, "
            "David Kemp put a sensitive microphone in the ear canal, played a click, and recorded an echo coming back "
            "out of the cochlea a few milliseconds later: the ear makes sound. <bookmark mark='c'/> In 1985, William "
            "Brownell and colleagues found that outer hair cells lengthen and shorten with their voltage, fast enough "
            "to push the membrane in time with the wave. <bookmark mark='d'/> They're an amplifier, adding energy at "
            "just the right place, sharpening the tuning and adding forty to sixty decibels of sensitivity. They're "
            "also fragile, and their loss is the commonest cause of hearing loss. <bookmark mark='e'/> And Kemp's "
            "echoes are now a routine test of every newborn's hearing in many countries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bank(self):
        d = load("cochlea")
        head = heading(r"Psyche's cochlea: \ a bank of filters")
        lf = np.log10(d["cfs"])
        A = axes([np.log10(80), np.log10(7000)], [-40, 2], x_length=7.6, y_length=4.2,
                 xticks=[np.log10(v) for v in (100, 300, 1000, 3000)], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"),
                 yticks=[-40, -20, 0], xlabel=r"each filter's centre frequency (Hz)", ylabel=r"output (dB)",
                 center=[-2.3, -0.3, 0])
        ax = A.ax
        e1 = curve_in(ax, lf, np.clip(d["ex500"], -40, 0), SOUND, stroke_width=3)
        e2 = curve_in(ax, lf, np.clip(d["ex2000"], -40, 0), PLACE, stroke_width=3)
        e3 = curve_in(ax, lf, np.clip(d["excomplex"], -40, 0), TIMING, stroke_width=4)
        leg = legend([(SOUND, r"a 500 Hz tone"), (PLACE, r"a 2000 Hz tone"), (TIMING, r"harmonics 1 to 10 of 200 Hz")],
                     font_size=20).move_to([4.6, 2.3, 0])
        rows = rows_of([
            (r"48 gammatone filters, \ spaced by the ear's own bandwidths \ (ERBs)", MODEL),
            (rf"each filter's width grows with frequency: \ {d['erb1000']:.0f} Hz at 1 kHz, \ {d['erb4000']:.0f} Hz at 4 kHz", WHITE),
            (r"low harmonics each get their own filter, \ resolved; \ high ones share, \ unresolved", TIMING),
        ], 4.6, 26, 0.34).move_to([4.6, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{hearing.filterbank}")
        with self.voiceover(
            "Psyche's cochlea is the standard engineering model of all this: a bank of filters. "
            "<bookmark mark='a'/> Forty-eight gammatone filters, the shape that best matches measured auditory "
            "filters, spaced by the ear's own bandwidths. Here's the output of every filter, the excitation pattern "
            "along the membrane, for a five hundred hertz tone, and for a two thousand hertz tone. "
            "<bookmark mark='b'/> The filters get wider as frequency rises: about a hundred and thirty hertz wide at a "
            "thousand hertz, about four hundred and fifty at four thousand. <bookmark mark='c'/> So feed it the "
            "harmonic complex, harmonics one to ten of two hundred hertz. The low harmonics each fall in a filter of "
            "their own, and show as separate peaks: they're resolved. The high ones crowd into shared filters and "
            "blur together. Keep that in mind for chapter four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(e1), Create(e2), FadeIn(leg[:2]), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(e3), FadeIn(leg[2]), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()
