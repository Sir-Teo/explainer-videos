from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Rondo(SoundScene):
    def construct(self):
        chapter(self, 5, r"Rondo and variation", r"How else can a piece come back to its start?")
        self.quiz()
        self.picture()
        self.variation()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("rondo")
        c = clip("rondo.five")
        card = listen_card(r"A piece built on the Tune. \ Count: \ how many times do you hear the Tune's opening strain?", width=9.6)
        with self.voiceover(
            "A piece built on the Tune, about half a minute long. Count how many times you hear the Tune's opening "
            "strain."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        total = d["starts"][-1] + 16
        bar = strip(d["starts"], ["?"] * len(d["starts"]), total, width=11.0, height=0.6, colors={"?": GREY_B}, font_size=26).move_to(UP * 0.4)
        cur = Line(ORIGIN, ORIGIN, color=WHITE, stroke_width=3)
        self.play(FadeOut(card), FadeIn(bar))
        with self.listen(c) as snd:
            window(snd, r"count the returns", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bar, 0.0, c.duration, buff=0.12)

            def upd(m, t):
                b = min(max(t / d["beat"], 0.0), total)
                x = bar.get_left()[0] + bar.width * b / total
                m.put_start_and_end_on([x, bar.get_bottom()[1] - 0.2, 0], [x, bar.get_top()[1] + 0.2, 0])

            snd.drive(cur, upd)
            self.add(cur)
        names = d["plan"].split()
        bar2 = strip(d["starts"], names, total, width=11.0, height=0.6, font_size=26).move_to(UP * 0.4)
        cap = label(r"A \ B \ A \ C \ A: \ a rondo", font_size=30, color=TUNE).next_to(bar2, DOWN, buff=0.5)
        with self.voiceover(
            "Three times: A, then a contrasting B in the dominant, A again, then C, the opening of the Ode to Joy in "
            "F major, and A once more. A refrain that keeps returning between different episodes is a rondo, the "
            "favourite last movement of the classical concerto and sonata."
        ):
            self.play(FadeOut(bar), FadeIn(bar2), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def picture(self):
        d = load("forms")
        imgs = Group()
        for name, t in (("rondo", r"A B A C A"), ("variations", r"A A1 A2 A1")):
            img = ssm_image(d[name]["ssm"], size=3.9)
            imgs.add(Group(label(rf"{name}: \ {t}", font_size=24, color=GREY_A), img).arrange(DOWN, buff=0.25))
        imgs.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        cap = label(r"rondo: \ the bright blocks of A, \ one in every other row; \ variations: \ the whole picture stays bright", font_size=22, color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Their pictures. In the rondo, the refrain lights up a bright block at every return, in a regular lattice: "
            "A against A, wherever they fall. The episodes, B and C, are dark against everything but themselves. "
            "<bookmark mark='a'/> On the right, a set of variations: the Tune's strain, then with its notes "
            "rearranged, then with its rhythm doubled. Because every variation keeps the harmony, the whole picture "
            "stays bright, and the boundaries are hard to see at all."
        ) as vo:
            self.play(FadeIn(imgs[0]))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(cap))
        c = clip("forms.variations")
        with self.listen(c) as snd:
            window(snd, r"the variations: \ A A1 A2 A1", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            self.add(diag_cursor(snd, imgs[1][1], d["variations"]["beats"], d["variations"]["beat"]))
            pulse(snd, imgs[1][0], 0.0, c.duration, buff=0.08)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def variation(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"theme and variations: \ the same plan, \ the same harmony, \ over and over", WHITE),
            (r"what changes: \ the melody's surface, \ the rhythm, \ the mode, \ the texture", WHITE),
            (r"Mozart's twelve variations on this Tune, \ about 1781 \ (Part 26)", TUNE),
            (r"this series is a set of variations: \ the ledger, \ one variation a part", EAR),
            (r"form by return \ (rondo) \ against form by transformation \ (variation)", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"variation form", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Variation form keeps the plan of the theme, its phrases and its harmony, and changes what lies on top: "
            "<bookmark mark='a'/> the surface of the melody, its rhythm, its mode, its texture. <bookmark mark='b'/> "
            "Mozart wrote twelve variations on this very Tune, probably around 1781, which Part 26 will take apart. "
            "<bookmark mark='c'/> And this series is itself a set of variations: every part ends with a variation on the "
            "Tune, and the ledger records them. <bookmark mark='d'/> So there are two ways to make a long piece from "
            "short material: bring it back, as a rondo does, or transform it, as variations do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("abcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
