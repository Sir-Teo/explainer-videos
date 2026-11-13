from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Tabla(SoundScene):
    def construct(self):
        chapter(self, 3, r"A patch of paste", r"How did Indian drum makers get five harmonics from a skin?", lit=(1877,), extra=((1920, r"Raman on the Indian drums"),))
        self.raman()
        self.loaded()
        self.listen_pair()

    # ------------------------------------------------------------------
    def raman(self):
        card = history_card(1920, r"C. V. Raman, \ Calcutta", r"``Musical drums with harmonic overtones'': the tabla and the mridangam sound a fundamental and four true harmonics.", width=5.6, font_size=20).to_corner(UL, buff=0.4)
        head = VGroup(Circle(radius=1.5, color=SKIN, stroke_width=4, fill_color=SKIN, fill_opacity=0.15), Circle(radius=0.6, stroke_width=0, fill_color=BLACK, fill_opacity=1).set_stroke(GREY_B, 2))
        head.move_to(RIGHT * 3.4 + UP * 0.6)
        tags = VGroup(label(r"goatskin", font_size=24, color=SKIN).next_to(head, DOWN, buff=0.2), label(r"the black patch: \ flour paste and iron dust, \\ rubbed on in dozens of thin layers", font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.7))
        notes = VGroup(label(r"a small drum that is tuned to the singer's note", font_size=26, color=GREY_A),
                       label(r"its overtones: \ 1, \ 2, \ 3, \ 4, \ 5", font_size=32, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(LEFT * 3.4 + DOWN * 1.3)
        with self.voiceover(
            "The kettledrum's tuning was a lucky accident, improved by trial. In India, drum makers did "
            "something deliberate, and they did it centuries earlier. <bookmark mark='a'/> The tabla is a "
            "small hand drum, and the player tunes it, with a hammer on the rim, to the note the singer has "
            "chosen. In the middle of its goatskin head is a black disc: a paste of flour and iron dust, "
            "rubbed on in dozens of thin layers and polished with a stone. <bookmark mark='b'/> In 1920 the "
            "physicist C. V. Raman, ten years before his Nobel prize for the scattering of light, studied "
            "these drums with sand and a careful ear. He reported that the tabla sounds a fundamental and "
            "four true harmonics above it: one, two, three, four, five. From a drum."
        ) as vo:
            self.play(FadeIn(head[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), FadeIn(tags), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(card), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loaded(self):
        d = load("tabla")
        g = axes([0.6, 5.6], [0, 2.6], x_length=11.0, y_length=2.4, xlabel=r"frequency, \ in units of the lowest mode", ylabel="", xticks=[1, 2, 3, 4, 5], yticks=[], font_size=20).move_to(UP * 1.3)
        targets = VGroup(*[DashedLine(g.ax.c2p(v, 0), g.ax.c2p(v, 2.6), color=GREY_D, stroke_width=1.5) for v in (1, 2, 3, 4, 5)])
        r1 = tick_row(g, [r["ratio"] for r in d["bare"]], 1.9, GREY_B, font_size=16)
        r2 = tick_row(g, [r["ratio"] for r in d["rows"]], 0.6, TUNE, font_size=16)
        l1 = label(r"a bare skin", font_size=22, color=GREY_B).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        l2 = label(rf"with a patch {d['density']:.0f} times as heavy, \ out to {d['patch']:.1f} of the radius", font_size=22, color=TUNE).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        g2 = axes([1, 16], [0, 600], x_length=5.4, y_length=2.2, xlabel=r"how many times heavier the patch is", ylabel=r"worst miss (cents)", xticks=[1, 4, 8, 12, 16], yticks=[0, 200, 400, 600], font_size=18)
        g2.move_to(LEFT * 3.4 + DOWN * 2.1)
        mc = curve_from(g2, d["densities"], d["misfit"], TUNE)
        why = VGroup(label(r"a heavy centre slows the simple modes most:", font_size=24, color=GREY_A), label(r"they are the ones that move the centre", font_size=24, color=GREY_A),
                     label(rf"miss: \ {d['bare_misfit']:.0f} cents bare, \ {d['loaded_misfit']:.0f} cents loaded", font_size=26, color=TUNE)).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 2.1)
        rows = d["rows"]
        with self.voiceover(
            "Monochord can check that. Take the round skin of chapter one, with its hopeless overtones. "
            "<bookmark mark='a'/> Now make the middle of it heavy: a disc reaching four tenths of the way to "
            "the rim, about ten times as heavy as the skin around it. And solve for the modes again. "
            f"<bookmark mark='b'/> One. {say(rows[1]['ratio'], 2)}. {say(rows[2]['ratio'], 2)} and "
            f"{say(rows[3]['ratio'], 2)}. {say(rows[4]['ratio'], 2)} and {say(rows[5]['ratio'], 2)}. Then three "
            "more, all near five. Nine modes, gathered into five groups, and the groups stand at one, two, "
            "three, four, five. That is just what Raman heard: several modes sharing each harmonic. "
            "<bookmark mark='c'/> Why does it work? The simple modes are the ones that move the centre of "
            "the skin, so a weight at the centre slows them most, and stretches the whole ladder out from "
            "the bottom. Here is how far the worst mode misses a whole number, as the patch gets heavier. "
            f"From {say(d['bare_misfit'])} cents with no patch, to {say(d['loaded_misfit'])} at ten times, "
            "and little better after that. The makers stopped adding layers in the right place."
        ) as vo:
            self.play(FadeIn(g), FadeIn(targets), FadeIn(r1), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(l2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in r2], lag_ratio=0.6), run_time=9.0)
            vo.wait_until("c")
            self.play(FadeIn(why[0]), FadeIn(why[1]))
            self.play(FadeIn(g2), Create(mc), FadeIn(why[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_pair(self):
        c = clip("tabla.pair")
        bare = mode_diagram(0, 1, radius=1.0, up=SKIN, down=SKIN).move_to(LEFT * 3.0 + UP * 0.8)
        loaded = VGroup(mode_diagram(0, 1, radius=1.0, up=SKIN, down=SKIN), Circle(radius=0.4, stroke_width=0, fill_color=BLACK, fill_opacity=1).set_stroke(GREY_B, 2)).move_to(RIGHT * 3.0 + UP * 0.8)
        la = label(r"bare", font_size=28, color=GREY_B).next_to(bare, DOWN, buff=0.25)
        lb = label(r"loaded", font_size=28, color=TUNE).next_to(loaded, DOWN, buff=0.25)
        note = listen_note(r"The same nine modes, \ equally loud, \ on both skins. \\ Only their frequencies differ.", width=7.6, font_size=24).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Hear the two skins. The same nine modes are sounding on each, equally loud. Only their "
            "frequencies are different."
        ):
            self.play(FadeIn(bare), FadeIn(loaded), FadeIn(la), FadeIn(lb), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a skin: \ bare, \ then loaded", detail=r"computed modes", corner=UL, tag_corner=UR)
            pulse(snd, la, snd.time_of("bare"), snd.time_of("bare") + 1.8, buff=0.12)
            pulse(snd, lb, snd.time_of("loaded"), snd.time_of("loaded") + 1.8, buff=0.12)
        with self.voiceover(
            "A clang, and a note. So there are two quite different ways to make a skin sing. Europe loaded "
            "it with air, and found a harmonic series with its fundamental missing. India loaded it with "
            "paste, and got the whole series. Neither knew a Bessel function."
        ):
            self.play(FadeOut(note))
        self.wait(0.3)
        self.clear_scene()
