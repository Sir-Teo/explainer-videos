from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403

NICE = {"attack_ms": r"attack time", "brightness": r"brightness", "odd_even_db": r"odd over even harmonics",
        "irregularity_db": r"spectral jaggedness", "decay_db_s": r"decay"}
SAID = {"attack_ms": "attack time", "brightness": "brightness", "odd_even_db": "the balance of odd and even harmonics",
        "irregularity_db": "how jagged the spectrum is", "decay_db_s": "how fast the sound decays"}


class Timbre(SoundScene):
    def construct(self):
        chapter(self, 7, r"A timbre space of our instruments", r"Can timbre be mapped?")
        self.tour()
        self.measures()
        self.space()
        self.tstream()
        self.specific()
        self.grouping()

    # ------------------------------------------------------------------
    def tour(self):
        d = load("timbre")
        c = clip("timbre.tour")
        names = list(d["features"])
        cells = VGroup(*[label(n, font_size=18, color=WHITE) for n in names]).arrange_in_grid(rows=3, cols=5, buff=(0.5, 0.6)).move_to(UP * 0.2)
        head = label(rf"{len(names)} instruments the series has built", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Part 41 placed our orchestra on two axes. Now do it properly. Here are {say(len(names))} of the instruments "
            "this series has built: the piano and plucked string models, the additive orchestra, Part 44's chip, and the "
            "model voice. Hear one note of each."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one note each", kind="synthesized", detail=r"physical models, \ additive, \ chip, \ voice", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                pulse(snd, cells[i], st[n], st[n] + 0.85, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measures(self):
        items = [
            (r"attack time: \ how long the sound takes to rise from 10\% to 90\% of its peak \ (logarithmic)", WHITE),
            (r"brightness: \ the spectral centroid over the fundamental \ (Part 41)", WHITE),
            (r"odd over even: \ the clarinet's hollowness, \ in decibels", WHITE),
            (r"spectral jaggedness: \ how much neighbouring harmonics differ; \ decay: \ how fast the level falls", TUNE),
            (r"five numbers per instrument, \ each measured from its sound", GREY_A),
        ]
        rows_scene(self, r"five measurements", items,
                   "Measure each sound five ways. <bookmark mark='b'/> Attack time: how long it takes to rise from ten to ninety "
                   "per cent of its peak, on a logarithmic scale. <bookmark mark='c'/> Brightness: the spectral centroid over the "
                   "fundamental, as in Part 41. <bookmark mark='d'/> The balance of odd and even harmonics, the clarinet's "
                   "hollowness. <bookmark mark='e'/> Spectral jaggedness, how much neighbouring harmonics differ, and decay, how "
                   "fast the level falls. <bookmark mark='f'/> Five numbers per instrument, each measured from its sound.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def space(self):
        d = load("timbre")
        sp = d["space"]
        xy = np.array(sp["coords"])
        names = sp["names"]
        x0, y0, W, H = -4.6, -2.6, 7.6, 5.0
        mn, mx = xy.min(0), xy.max(0)
        def P_(p):
            return [x0 + W * (p[0] - mn[0]) / (mx[0] - mn[0] + 1e-9), y0 + H * (p[1] - mn[1]) / (mx[1] - mn[1] + 1e-9), 0]
        dots = VGroup()
        for n, p in zip(names, xy):
            q = P_(p)
            dots.add(VGroup(Dot(q, radius=0.09, color=TUNE), label(n, font_size=14, color=WHITE).next_to(q, RIGHT, buff=0.08)))
        corr = sp["corr"]
        def top(dim):
            ks = sorted(corr, key=lambda k: -abs(corr[k][dim]))[:2]
            return ks
        t1, t2 = top(0), top(1)
        side = VGroup(label(rf"axis 1 \ ({100 * sp['share'][0]:.0f}\% of the variation): \ " + r", \ ".join(NICE[k] + rf" \ ({corr[k][0]:+.2f})" for k in t1), font_size=16, color=TUNE),
                      label(rf"axis 2 \ ({100 * sp['share'][1]:.0f}\%): \ " + r", \ ".join(NICE[k] + rf" \ ({corr[k][1]:+.2f})" for k in t2), font_size=16, color=TUNE),
                      label(r"numbers: \ each measurement's correlation with the axis", font_size=14, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(UR, buff=0.4)
        side.scale_to_fit_width(min(side.width, 5.6)).to_corner(UR, buff=0.4)
        head = label(r"our timbre space", font_size=26, color=GREY_A).to_corner(UL, buff=0.4)
        with self.voiceover(
            "Now let multidimensional scaling, the method Grey used, find the two axes that best preserve the distances between "
            "the instruments' five measurements. <bookmark mark='a'/> Here is the map. <bookmark mark='b'/> The first axis "
            f"carries {say(100 * sp['share'][0])} per cent of the variation and lines up most with "
            f"{SAID[t1[0]]} and {SAID[t1[1]]}; the second carries {say(100 * sp['share'][1])} per cent and lines up with "
            f"{SAID[t2[0]]} and {SAID[t2[1]]}. Grey and McAdams, asking listeners rather than measuring sounds, found attack "
            "time, brightness and how the spectrum changes over time. Our map is built from measurements, not judgements; "
            "testing it against listeners is the obvious next experiment."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grouping(self):
        items = [
            (r"timbre is also a grouping cue: \ notes far apart in timbre space stream apart", WHITE),
            (r"Iverson \ (1995): \ the more different two timbres are judged, \ the more readily they segregate", WHITE),
            (r"Klangfarbenmelodie \ (Part 41) \ works against this: \ a line passed between timbres can fall apart", WHITE),
            (r"orchestrators use it both ways: \ one timbre to bind a line, \ contrasting timbres to separate layers", TUNE),
            (r"chapter 8: \ pitch itself, \ and its illusions", GREY_A),
        ]
        rows_scene(self, r"timbre and grouping", items,
                   "Timbre also groups. <bookmark mark='b'/> Notes far apart in timbre space stream apart: Paul Iverson found in "
                   "1995 that the more different two timbres are judged, the more readily they segregate. "
                   "<bookmark mark='c'/> A melody of timbres, Part 41's Klangfarbenmelodie, works against this, and a line passed "
                   "between very different timbres can fall apart. <bookmark mark='d'/> Orchestrators use the effect both ways: "
                   "one timbre to bind a line, contrasting timbres to separate layers. <bookmark mark='e'/> Chapter eight turns to "
                   "pitch itself, and its illusions.", marks="bcde")

    # ------------------------------------------------------------------
    def tstream(self):
        d = load("tstream")
        c = clip("tstream.two")
        row = VGroup(*[Rectangle(width=0.34, height=0.34, stroke_width=0, fill_color=TUNE if i % 2 == 0 else BLUE, fill_opacity=1.0) for i in range(16)]).arrange(RIGHT, buff=0.12).move_to(UP * 0.6)
        keys = VGroup(label(r"gold: \ piano", font_size=19, color=TUNE), label(r"blue: \ the chip's thin pulse; \ both on G4", font_size=19, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(row, DOWN, buff=0.4)
        cells = VGroup(label(r"slow", font_size=22, color=WHITE), label(r"fast", font_size=22, color=WHITE)).arrange(RIGHT, buff=3.0).to_edge(DOWN, buff=1.2)
        head = label(r"streaming by timbre alone", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Timbre streams on its own. One pitch, G above middle C, alternating between the piano and the chip's thin "
            "pulse: first slowly, then fast."
        ):
            self.play(FadeIn(head), FadeIn(row), FadeIn(keys), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"one pitch, \ two timbres", kind="synthesized", detail=r"Part 7's piano, \ our chip", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["slow"], st["fast"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["fast"], c.duration, buff=0.1)
            for i, sq in enumerate(row):
                snd.drive(sq, lambda m, now, i=i: m.set_fill(opacity=1.0 if int(((now - (st["fast"] if now >= st["fast"] else st["slow"])) / (d["iois"][1] if now >= st["fast"] else d["iois"][0]))) % 16 == i else 0.35))
        with self.voiceover(
            "Slowly, one line alternating colour. Fast, the pitch never changes, yet the sequence splits into a piano part "
            "and a chip part, each at half the rate."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def specific(self):
        items = [
            (r"McAdams and colleagues \ (1995) \ found shared dimensions, \ and `specificities': \ features unique to one instrument", WHITE),
            (r"the harpsichord's release thump, \ a clarinet's hollowness: \ things no common axis captures", WHITE),
            (r"listener groups weigh the dimensions differently: \ musicians and non-musicians share the map but not the scales", WHITE),
            (r"timbre is many things at once: \ a few shared dimensions plus a signature", TUNE),
            (r"Part 52 builds instruments to match a target timbre", GREY_A),
        ]
        rows_scene(self, r"beyond the map", items,
                   "Maps of timbre leave things out. <bookmark mark='b'/> McAdams and colleagues found shared dimensions, and "
                   "also what they called specificities, features unique to one instrument, <bookmark mark='c'/> like a "
                   "harpsichord's release thump: things no common axis captures. <bookmark mark='d'/> Different groups of "
                   "listeners weigh the dimensions differently: musicians and non-musicians share the map, but not its scales. "
                   "<bookmark mark='e'/> Timbre is many things at once, a few shared dimensions plus a signature. "
                   "<bookmark mark='f'/> Part 52 builds instruments to match a target timbre.", marks="bcdef")
