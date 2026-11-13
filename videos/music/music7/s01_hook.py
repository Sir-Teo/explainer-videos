from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.blind()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        c = clip("three.notes")
        bx = lane(width=3.4, height=1.6, buff=0.5, font_size=40).move_to(UP * 0.5)
        s = StringView(width=8.0).move_to(DOWN * 2.0)
        lens = Lens(s.p(0.0), s.p(1.0), amp=0.25, color=STR)
        cap = label(r"one string", font_size=26, color=GREY_B).next_to(s, DOWN, buff=0.25)
        self.play(FadeIn(bx), FadeIn(s), FadeIn(cap), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"four notes: \ plucked, \ struck, \ bowed", detail=r"three models, \ one string", corner=DL, tag_corner=DR)
            snd.show(lens)
            for ev, b in zip(("plucked", "struck", "bowed"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.9)
            snd.drive(lens, lambda m, t: m.set_amp(0.35 + 0.65 * abs(np.sin(9.0 * t))))
        with self.voiceover(
            "The same four notes, three times. A string that was plucked. A string that was struck. A string "
            "that was bowed. <bookmark mark='a'/> No instrument was recorded for those sounds. Each one is "
            "Monochord's string, the one this series began with, set going in a different way and attached to a "
            "different box. For six parts that string has been plucked, and we have listened to it directly. "
            "This part builds real instruments around it: a guitar, a piano and a violin."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(s, color=WHITE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blind(self):
        c1 = history_card(2010, r"Indianapolis: \ a hotel room, \ the lights down",
                          r"twenty-one experienced violinists in welder's goggles try six violins: three new, two by Stradivari and one by Guarneri. Which would you take home?",
                          width=6.0, font_size=20).to_corner(UL, buff=0.4)
        c2 = history_card(2012, r"Vincennes, \ near Paris: \ a rehearsal room and a concert hall",
                          r"ten soloists, six new violins, six Old Italian ones, five of them by Stradivari.", width=6.0, font_size=20).next_to(c1, DOWN, buff=0.3)

        def tally(new, old, at):
            dots = VGroup(*[Dot(radius=0.11, color=GOOD) for _ in range(new)], *[Dot(radius=0.11, color=HIST) for _ in range(old)]).arrange_in_grid(cols=7, buff=0.14)
            return dots.move_to(at)

        t1 = tally(13, 8, RIGHT * 3.6 + UP * 2.2)
        l1 = label(r"13 chose a new violin, \ 8 an old one", font_size=26).next_to(t1, DOWN, buff=0.2)
        t2 = tally(6, 4, RIGHT * 3.6 + DOWN * 0.3)
        l2 = label(r"6 chose new, \ 4 chose a Stradivari", font_size=26).next_to(t2, DOWN, buff=0.2)
        guess = VGroup(label(r"asked which were old and which new,", font_size=28, color=GREY_A),
                       label(r"the players did no better than chance", font_size=32, color=EAR)).arrange(DOWN, buff=0.12).move_to(RIGHT * 3.4 + DOWN * 2.4)
        with self.voiceover(
            "Start with the most famous of them. In 2010, in a hotel room in Indianapolis with the lights turned "
            "down, twenty-one experienced violinists put on welder's goggles and tried six violins. Three were "
            "new. Two were by Stradivari and one by Guarneri, together worth about ten million dollars. Each "
            "player was asked one question: which would you take home? <bookmark mark='a'/> Thirteen of the "
            "twenty-one chose a new violin. The least popular instrument of the six was a Stradivari. "
            "<bookmark mark='b'/> The violin world objected: a hotel room is not a concert hall, and these were "
            "not soloists. So in 2012 the same researchers, led by Claudia Fritz and the violin maker Joseph "
            "Curtin, did it again near Paris, with ten international soloists, six new violins and six old "
            "Italian ones, in a rehearsal room and then in a concert hall. <bookmark mark='c'/> Six of the ten "
            "chose a new violin. <bookmark mark='d'/> And when the players were asked to say which instruments "
            "were old and which were new, they did no better than chance."
        ) as vo:
            self.play(FadeIn(c1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in t1], lag_ratio=0.04), FadeIn(l1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in t2], lag_ratio=0.06), FadeIn(l2), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(guess))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        q = label(r"so what makes a violin? \ Or a guitar, \ or a piano?", font_size=38, color=EAR).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"why a string needs a box, \ and what a box does to its sound",
            r"the guitar: \ a plate, \ a hole and a box of air",
            r"plucking in a computer: \ Karplus and Strong's three lines",
            r"the piano: \ a felt hammer, \ a stiff string, \ three strings to a note",
            r"the violin: \ stick and slip, \ Helmholtz's corner, \ how hard to press",
            r"what measurement can say about a great instrument, \ and what it cannot",
        ], title=r"Part 7: \ Strings, Hammers and Bows", font_size=26).move_to(DOWN * 0.45)
        with self.voiceover(
            "None of that means a Stradivari is not a wonderful violin. It means that whatever makes a violin "
            "wonderful is not a secret that died in Cremona. It is physics, and makers alive today have it. So "
            "what is it? What makes a violin, or a guitar, or a piano, sound the way it does? "
            "<bookmark mark='a'/> To find out we will build all three. <bookmark mark='b'/> First, why a string "
            "needs a box at all, and what the box does. <bookmark mark='c'/> Then the guitar's box, which turns "
            "out to be the bottle of Part 2 with a flexible lid. <bookmark mark='d'/> A way of plucking a string "
            "in a computer that takes three lines of code. <bookmark mark='e'/> The piano: a felt hammer, a "
            "string so thick that it is partly a bar, and three strings for every note. <bookmark mark='f'/> And "
            "the violin, where a bow holds the string, lets it go and catches it again, hundreds of times a "
            "second. <bookmark mark='g'/> At the end we will come back to that hotel room."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(card.head))
            for mark, r in zip("bcdefg", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
