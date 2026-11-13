from __future__ import annotations

import numpy as np

from videos.music.music5.common import *  # noqa: F403


class Culture(SoundScene):
    def construct(self):
        chapter(self, 9, r"What is learned", r"Is the taste for consonance built in?", lit=(2016,), extra=((2016, r"the Tsimane' study"),))
        self.history()
        self.tsimane()
        self.layers()

    # ------------------------------------------------------------------
    def history(self):
        d = load("culture")
        c = clip("culture.thirds")
        py, ju = d["rows"]["pythagorean"], d["rows"]["just"]
        tl = Line(LEFT * 6.0, RIGHT * 6.0, color=GREY_C, stroke_width=2).move_to(UP * 2.3)
        marks = VGroup()
        for x, year, text in ((-5.2, r"1000", r"thirds are \\ dissonances"), (-1.8, r"1500", r"thirds are the \\ basis of harmony"), (1.6, r"1920", r"a seventh chord \\ can end a piece"),
                              (4.8, r"1960", r"stacked fourths, \\ clusters")):
            p = tl.get_center() + RIGHT * x
            marks.add(VGroup(Dot(p, radius=0.07, color=HIST), label(year, font_size=26, color=HIST).next_to(p, UP, buff=0.15), label(text, font_size=22, color=GREY_A).next_to(p, DOWN, buff=0.2)))
        bx = boxes((rf"{py['p']} : {py['q']}", rf"{ju['p']} : {ju['q']}"), buff=1.4, width=3.2, height=1.3, font_size=36).move_to(DOWN * 1.0)
        tags = VGroup(label(r"the third of the Middle Ages: \\ four fifths, \ less two octaves", font_size=22, color=GREY_A).next_to(bx[0], DOWN, buff=0.2),
                      label(r"the pure third", font_size=22, color=GREY_A).next_to(bx[1], DOWN, buff=0.2))
        with self.voiceover(
            "If consonance came entirely from the ear, it would not have a history. It has one. "
            "<bookmark mark='a'/> For the ancient Greeks, and for the theorists of the early Middle Ages who "
            "followed them, the major third was a dissonance. <bookmark mark='b'/> By 1500 it was the foundation "
            "of all harmony. <bookmark mark='c'/> By the 1920s a jazz band could end a piece on a chord with a "
            "seventh in it, which an earlier age would have had to resolve. "
            "<bookmark mark='d'/> And twentieth-century composers and jazz musicians made stable sounds out of "
            "stacked fourths and clusters. Part of that change has a physical cause, and you can hear it. The "
            "third that those early theorists were judging was not our third. It was built from four pure fifths, "
            "and it comes out as eighty-one to sixty-four. Here it is, followed by the pure third, five to four."
        ) as vo:
            self.play(Create(tl))
            for mark, m in zip("abcd", marks):
                vo.wait_until(mark)
                self.play(FadeIn(m), run_time=0.6)
            self.wait(max(vo.remaining() - 9.0, 0.1))
            self.play(FadeIn(bx), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"a third of 81 to 64, \ then one of 5 to 4", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("pythagorean", "just"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        res = VGroup(label(rf"{py['cents'] - ju['cents']:.0f} cents wide: \ its partials beat {py['beat']:.0f} times a second", font_size=26, color=ROUGH).next_to(tags[0], DOWN, buff=0.2),
                     label(r"partials 5 and 4 coincide", font_size=26, color=SMOOTH).next_to(tags[1], DOWN, buff=0.2))
        with self.voiceover(
            f"The medieval third is {say(py['cents'] - ju['cents'])} cents wider than the pure one, and on these "
            f"notes its partials beat {say(py['beat'])} times a second. It has a restless edge. The theorists who "
            "called it a dissonance were describing what they heard. When tuning changed, so that thirds came "
            "out pure, the third became a consonance. That story is Part 6. But tuning cannot explain the rest "
            "of the timeline. Something else moved: what listeners were used to."
        ):
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tsimane(self):
        card = history_card(2016, r"Josh McDermott and colleagues, \ \textit{Nature}",
                            r"travel to the Tsimane', farmers and foragers in the Bolivian Amazon, whose own music is sung one voice at a time and who rarely hear Western music.",
                            width=5.8).to_corner(UL, buff=0.4)
        rows = VGroup(
            VGroup(label(r"listeners in the United States", font_size=26), label(r"prefer consonant chords strongly", font_size=26, color=SMOOTH)),
            VGroup(label(r"Bolivians in the capital and in a town", font_size=26), label(r"prefer them, \ less strongly", font_size=26, color=TUNE)),
            VGroup(label(r"the Tsimane'", font_size=26), label(r"rate consonant and dissonant chords as equally pleasant", font_size=26, color=EAR)),
        )
        for k, r in enumerate(rows):
            r[0].move_to(LEFT * 6.0 + DOWN * (0.3 + 0.8 * k), aligned_edge=LEFT)
            r[1].move_to(LEFT * 0.6 + DOWN * (0.3 + 0.8 * k), aligned_edge=LEFT)
        but = VGroup(label(r"but the Tsimane' did dislike rough sounds, \ as Westerners do,", font_size=26, color=GREY_A),
                     label(r"and rated laughter and gasps as everyone else does", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How much is learned? For a century the question could not be answered, because everyone who could be "
            "tested had grown up with Western harmony on the radio. <bookmark mark='a'/> In 2016 Josh McDermott "
            "and his colleagues went to the Tsimane', a people of the Bolivian Amazon who farm and forage, whose "
            "own music is sung one voice at a time, and who at that time rarely heard anything else. They played "
            "them chords, and asked how pleasant each one was. <bookmark mark='b'/> Listeners in the United "
            "States preferred the consonant chords, strongly. Bolivians in the capital and in a nearby town "
            "preferred them too, less strongly. <bookmark mark='c'/> The Tsimane' rated consonant and dissonant "
            "chords as equally pleasant. <bookmark mark='d'/> It was not that they heard differently, or did not "
            "understand the question. They disliked rough sounds, much as Westerners do, and they rated laughter "
            "and gasps as everyone else does. They "
            "simply had no preference between a fifth and a tritone. The preference for consonance, it seems, "
            "has to be learned, by living with music that uses harmony."
        ) as vo:
            ask = VGroup(label(r"How much is learned?", font_size=44, color=EAR),
                         label(r"everyone who could be tested had grown up with Western harmony", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.4)
            self.play(FadeIn(ask[0]))
            self.play(FadeIn(ask[1]))
            vo.wait_until("a")
            self.play(FadeOut(ask), run_time=0.4)
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.wait(max(vo.until("c") - 5.0, 0.1))
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(but))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        layers = VGroup()
        for name, text, col in ((r"the membrane", r"roughness: \ partials inside one band of the ear. \\ The same in everyone; \ depends on timbre.", ROUGH),
                                (r"the nerve", r"harmonicity: \ partials that fit one series fuse into one pitch. \\ The same machinery in everyone; \ what it is used for can differ.", EAR),
                                (r"the listener", r"familiarity: \ what you have heard is what sounds right. \\ Different in every culture, \ and in every century.", HIST)):
            box = RoundedRectangle(width=12.4, height=1.45, corner_radius=0.15, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.06)
            layers.add(VGroup(box, label(name, font_size=32, color=col).move_to(box.get_left() + RIGHT * 1.7), label(text, font_size=24, color=GREY_A).move_to(box.get_center() + RIGHT * 1.6)))
        layers.arrange(DOWN, buff=0.3).move_to(DOWN * 0.2)
        head = label(r"Three layers", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "So the six answers settle into three layers. <bookmark mark='a'/> At the bottom, the membrane. "
            "Partials that share a band of the ear grind against each other. That is the same in everyone, it "
            "explains why the just ratios are special for instruments with harmonic partials, and it moves "
            "when the timbre moves. <bookmark mark='b'/> Above it, the nerve. Partials that fit one harmonic "
            "series fuse into one pitch. The machinery is the same in everyone too; it is how we hear voices. "
            "But whether a fused sound is preferred is not given. <bookmark mark='c'/> And on top, the listener. "
            "What you have heard all your life is what sounds right, and that differs from one culture to the "
            "next and from one century to the next. Pythagoras, Galileo and Euler were describing the first two "
            "layers by their arithmetic. Helmholtz found the first. Stumpf and Rameau found the second. None of "
            "them was wrong. Each had one layer of the answer."
        ) as vo:
            for mark, l in zip("abc", layers):
                vo.wait_until(mark)
                self.play(FadeIn(l), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()
