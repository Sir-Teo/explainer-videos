from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Simul(SoundScene):
    def construct(self):
        chapter(self, 4, r"Sounds at the same moment", r"Which partials belong to which sound?")
        self.problem()
        self.mistune()
        self.onset()
        self.hear_fate()
        self.hear_place()
        self.fate()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"a chord, \ a voice and a drum arrive as one spectrum: \ hundreds of partials at once", WHITE),
            (r"the ear must decide which partials belong together before it can hear any of the sources", WHITE),
            (r"cues: \ harmonicity, \ common onset, \ common change \ (`common fate'), \ common location", WHITE),
            (r"Part 41's Bol\'ero trick works because instruments on harmonics pass the first test", TUNE),
            (r"each cue can be broken on purpose, \ and heard", GREY_A),
        ]
        rows_scene(self, r"simultaneous grouping", items,
                   "Sounds that arrive together pose a different problem. <bookmark mark='b'/> A chord, a voice and a drum arrive "
                   "as one spectrum, hundreds of partials at once, <bookmark mark='c'/> and the ear must decide which partials "
                   "belong together before it can hear any of the sources. <bookmark mark='d'/> It uses cues: harmonicity, a "
                   "common onset, common change, which Bregman called common fate, and a common location. "
                   "<bookmark mark='e'/> Part 41's Boléro trick works because instruments placed on harmonics pass the first "
                   "test. <bookmark mark='f'/> Each cue can be broken on purpose, and heard.", marks="bcdef")

    # ------------------------------------------------------------------
    def comb(self, mistune, x0=0.0, w=3.0, h=1.2, col=TUNE):
        g = VGroup(Line([x0, 0, 0], [x0 + w, 0, 0], color=GREY_D))
        for k in range(1, 11):
            f = k * (1 + (mistune if k == 4 else 0.0))
            g.add(Line([x0 + w * f / 10.5, 0, 0], [x0 + w * f / 10.5, h, 0], color=EAR if (k == 4 and mistune > 0) else col, stroke_width=3))
        return g

    def mistune(self):
        d = load("mistune")
        c = clip("mistune.four")
        cells = VGroup()
        for m, ct in zip(d["mistunes"], d["cents"]):
            cells.add(VGroup(label(rf"4th harmonic {100 * m:.0f}\% sharp", font_size=18, color=WHITE), self.comb(m), label(rf"{ct:.0f} cents", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.6)).move_to(DOWN * 0.1)
        head = label(r"harmonicity: \ one harmonic pulled out of line", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Harmonicity first. Ten equal harmonics of two hundred hertz, then the same with the fourth harmonic pulled "
            "sharp by one, three and eight per cent. Listen for the moment a separate, thin tone pops out of the buzz."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = list(st)
        with self.listen(c) as snd:
            window(snd, r"one harmonic mistuned", kind="synthesized", detail=r"ten harmonics of 200 Hz", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                pulse(snd, cells[i], st[k], st[k] + 1.2, buff=0.1)
        with self.voiceover(
            "At one per cent the tone is still one sound, perhaps a little rough. By three per cent, about fifty cents, most "
            "listeners hear the fourth harmonic as a second tone on its own; at eight per cent it is plainly separate. Brian "
            "Moore, Brian Glasberg and Robert Peters measured the threshold in 1986: a low harmonic mistuned by a few per "
            "cent stands apart. The ear groups partials by a harmonic template, and rejects what does not fit."
        ):
            self.play(*[Indicate(c_[1][4]) for c_ in cells[1:]])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def onset(self):
        d = load("onset")
        c = clip("onset.two")
        def bars(lead):
            g = VGroup()
            for k in range(1, 11):
                st_ = 0.0 if (k != 4 or lead == 0) else -0.6
                g.add(Rectangle(width=3.2 - st_, height=0.12, stroke_width=0, fill_color=EAR if (k == 4 and lead) else TUNE, fill_opacity=1.0).move_to([st_ / 2 + 1.6, 0.25 * k, 0]))
            return g
        cells = VGroup(VGroup(label(r"all together", font_size=20, color=WHITE), bars(0)).arrange(DOWN, buff=0.3),
                       VGroup(label(r"the 4th, \ 80 ms early", font_size=20, color=WHITE), bars(1)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=2.0).move_to(UP * 0.2)
        cap = label(r"each bar a harmonic, \ time running right", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"common onset", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now onsets. The same ten harmonics, all in tune, starting together; then with the fourth starting eighty "
            "milliseconds before the rest."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"together, \ then early", kind="synthesized", detail=r"ten harmonics of 200 Hz", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["together"], st["early"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["early"], c.duration, buff=0.1)
        with self.voiceover(
            "With the early start, the fourth harmonic is heard as a separate tone at the beginning, and some listeners keep "
            "hearing it as separate throughout. Chris Darwin's experiments showed that a harmonic starting a few tens of "
            "milliseconds early contributes less to the vowel or pitch of the rest: partials that start together belong "
            "together. That is why ensembles work so hard to play together, and why a slightly early note stands out."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fate(self):
        items = [
            (r"common fate: \ partials that change together group together", WHITE),
            (r"Stephen McAdams \ (1984): \ give one set of a mixture's partials a vibrato, \ and a voice emerges from the blend", WHITE),
            (r"a singer's vibrato helps the voice carry over an orchestra: \ its partials move together, \ the orchestra's do not", WHITE),
            (r"location: \ the two ears' differences in time and level group partials by direction \ (Part 55)", TUNE),
            (r"chapter 5: \ what fills a gap", GREY_A),
        ]
        rows_scene(self, r"common fate and place", items,
                   "Two more cues. <bookmark mark='b'/> Common fate: partials that change together group together. "
                   "<bookmark mark='c'/> Stephen McAdams showed in 1984 that giving one set of a mixture's partials a vibrato "
                   "makes a voice emerge from the blend, <bookmark mark='d'/> which helps a singer carry over an orchestra: the voice's "
                   "partials move together, and the orchestra's do not. <bookmark mark='e'/> And location: the differences "
                   "between the two ears group partials by direction, Part 55's subject. <bookmark mark='f'/> Chapter five asks "
                   "what fills a gap.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear_fate(self):
        d = load("fate")
        c = clip("fate.two")
        def comb(moving):
            g = VGroup(Line([0, 0, 0], [3.4, 0, 0], color=GREY_D))
            for k in range(1, 11):
                col = EAR if (moving and k in d["moving"]) else TUNE
                ln = Line([3.4 * k / 10.5, 0, 0], [3.4 * k / 10.5, 1.2, 0], color=col, stroke_width=3)
                g.add(ln)
            return g
        A, B_ = comb(False), comb(True)
        cells = VGroup(VGroup(label(r"all still", font_size=20, color=WHITE), A).arrange(DOWN, buff=0.3),
                       VGroup(label(r"harmonics 3, \ 5 and 7 given a vibrato", font_size=20, color=WHITE), B_).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=1.6).move_to(UP * 0.2)
        head = label(r"common fate, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Common fate, heard. Ten harmonics held still; then the same, with harmonics three, five and seven given a "
            "vibrato after one second, all moving together."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"still, \ then moving", kind="synthesized", detail=r"ten harmonics of 200 Hz", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["still"], st["moving"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["moving"], c.duration, buff=0.1)
            for k in d["moving"]:
                ln = B_[k]
                base = ln.get_center()
                snd.drive(ln, lambda m, now, base=base: m.move_to(base + RIGHT * (0.05 * np.sin(2 * np.pi * 5.5 * now) if now > st["moving"] + d["from"] else 0.0)))
        with self.voiceover(
            "When the three start to wobble together, they leave the buzz and form a second sound of their own, a voice "
            "floating above a drone. Nothing else changed: the same partials, at the same levels, only moving in common."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear_place(self):
        d = load("place")
        c = clip("place.stereo")
        cells = VGroup(label(r"all ten in the centre", font_size=22, color=TUNE), label(r"the 4th moved to the right ear", font_size=22, color=EAR)).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"place, \ heard \ (headphones)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("And place. The same ten harmonics, all in the centre; then with the fourth moved to the right ear alone."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"centre, \ then split", kind="synthesized", detail=r"ten harmonics, \ stereo", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["centre"], st["right"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["right"], c.duration, buff=0.1)
        with self.voiceover(
            "With headphones the fourth harmonic becomes a thin tone on the right, beside a sound in the middle that has lost "
            "a little of its colour. Location groups too, though in rooms, with echoes everywhere, it is the weakest of the "
            "cues."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()
