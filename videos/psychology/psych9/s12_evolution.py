from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Evolution(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.test()
        self.stories()
        self.crow()

    def card(self):
        card = chapter_card(11, r"Evolution as a source of hypotheses", r"What was a mind's feature for, and how would you know?",
                            lit={1989: r"37 cultures"}, part=PART, scale=("person", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter eleven. Evolution as a source of hypotheses."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def why(self):
        head = heading(r"A second kind of ``why''")
        two = VGroup(
            VGroup(label(r"how does it work?", font_size=38, color=MODEL),
                   wrapped_label(r"the mechanism: \ most of this series", 5.2, 30, WHITE)).arrange(DOWN, buff=0.15),
            VGroup(label(r"what was it for?", font_size=38, color=THRESH),
                   wrapped_label(r"the history: \ what helped ancestors survive and have children", 5.6, 30, WHITE)).arrange(
                DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, 1.7, 0])
        rows = rows_of([
            (r"a fear of snakes and of heights; \ a taste for sugar and fat; \ the pain of being left out", WHITE),
            (r"the account: \ useful for a very long time, \ in conditions unlike ours", GREY_A),
            (r"That can generate hypotheses. \ It can also generate stories. \ The difference is the usual one: \ can it "
             r"fail?", P.ACCENT),
        ], 12.4, 31, 0.3).move_to([0, -1.45, 0])
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So far we've studied how people's genes differ. But most of the genome is the same in "
            "everyone, and it's the same because of its history. <bookmark mark='a'/> Natural selection "
            "kept what helped ancestors survive and have children. So for any feature of the mind you can "
            "ask a second kind of why. Not how does it work, but what was it for? <bookmark mark='b'/> A "
            "fear of snakes and of heights. A taste for sugar and fat. The pain of being left out. An "
            "evolutionary account says these were useful for a very long time, in conditions unlike ours. "
            "<bookmark mark='c'/> That's a way of generating hypotheses, and it's produced good ones. It's "
            "also a way of generating stories. The difference between the two is the usual one. Can it "
            "fail?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(two[0]))
            vo.wait_until("a")
            self.play(FadeIn(two[1], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def test(self):
        b = archive.BUSS_1989.data
        head = heading(rf"1989: \ a prediction that could fail in {b['cultures']} places")
        g = np.random.default_rng(2)
        dots = VGroup(*[Dot(radius=0.13, color=MODEL) for _ in range(b["cultures"])]).arrange_in_grid(rows=4, buff=0.22)
        dots.move_to([-4.3, 0.7, 0])
        dots[int(g.integers(0, b["cultures"]))].set_color(OWN)
        dl = wrapped_label(rf"{b['cultures']} samples: \ in {b['financial_prospects']}, women rated a partner's financial "
                           r"prospects higher than men did", 5.0, 29, MODEL).next_to(dots, DOWN, buff=0.3)
        rows = rows_of([
            (rf"{num(b['people'])} people, \ {b['countries']} countries", DATA),
            (rf"in all {b['younger_mates']}, \ men preferred partners younger than themselves", MODEL),
            (r"his own caveats: \ mostly urban, educated samples; \ stated preferences, not choices", GREY_A),
            (r"a rival account: \ the same pattern follows where women have less access to money. \ Tested since; \ "
             r"Part 37", BAD),
        ], 6.0, 30, 0.3).move_to([3.5, -0.2, 0])
        keep_in_frame(rows)
        src = published_tag(archive.BUSS_1989.cite)
        tag = note(r"which sample was the exception: \ not shown").to_corner(DR, buff=0.2)
        with self.voiceover(
            "First, a hypothesis. If the least that a parent must invest in a child differs between the "
            "sexes, then what men and women look for in a long-term partner should differ in particular "
            "ways. And it should differ everywhere, not just in one culture. <bookmark mark='a'/> In 1989 "
            f"David Buss reported a test: {b['people']:,} people, in {b['cultures']} cultures. "
            f"<bookmark mark='b'/> In {b['financial_prospects']} of the {b['cultures']} samples, women "
            "rated a partner's financial prospects higher than men did. In all "
            f"{b['younger_mates']}, men preferred partners younger than themselves. That's a prediction "
            "that could have failed in thirty-seven places, and it didn't. <bookmark mark='c'/> The "
            "caveats are his own. The samples were mostly urban and educated, and a questionnaire "
            "measures what people say they want, not whom they choose. <bookmark mark='d'/> And there's a "
            "rival account. The same pattern is what you'd expect wherever women have less access to "
            "money. That's been tested since, and the story continues in Part 37."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(dots, lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def stories(self):
        head = heading(r"The failure mode: \ a story for everything")
        both = VGroup(
            wrapped_label(r"people are generous: \ generosity was adaptive", 5.6, 31, MODEL),
            wrapped_label(r"people are selfish: \ selfishness was adaptive", 5.6, 31, BAD),
        ).arrange(RIGHT, buff=0.9).move_to([0, 2.0, 0])
        verdict = wrapped_label(r"An account that explains a result and its opposite has explained neither.", 12.4, 31,
                                P.ACCENT).next_to(both, DOWN, buff=0.35)
        needs = [r"a prediction made before the data", r"across cultures: \ a universal cannot be a local habit",
                 r"across species: \ selection leaves relatives with related traits",
                 r"the rival, \ usually learning or culture, \ tested alongside"]
        rows = VGroup(*[VGroup(label(str(i + 1), font_size=36, color=THRESH), wrapped_label(t, 10.6, 30, WHITE)).arrange(
            RIGHT, buff=0.4) for i, t in enumerate(needs)]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        rows.move_to([0, -1.55, 0])
        rl = label(r"what a testable version needs", font_size=30, color=THRESH).next_to(rows, UP, buff=0.25).align_to(rows, LEFT)
        tag = note(r"the warning: Gould and Lewontin, 1979").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Now the failure mode. In 1979 Stephen Jay Gould and Richard Lewontin warned against what "
            "they called just-so stories. Take any trait, invent an advantage it might once have had, and "
            "call it explained. <bookmark mark='a'/> The story is always available. If people are "
            "generous, generosity was adaptive. If they're selfish, so was that. An account that can "
            "explain a result and its opposite has explained neither. <bookmark mark='b'/> So here's what "
            "a testable version needs. A prediction made before the data. A comparison across cultures, "
            "because a universal can't be a local habit. A comparison across species, because selection "
            "leaves relatives with related traits. And the rival explanation, usually learning or culture, "
            "tested alongside. <bookmark mark='c'/> Held to that standard, some evolutionary claims "
            "survive and many don't. We'll meet both kinds: reasoning about cheats in Part 24, and "
            "attraction in Part 37."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(both[0]))
            vo.wait_until("a")
            self.play(FadeIn(both[1]), FadeIn(verdict))
            vo.wait_until("b")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=11.0)
            vo.wait_until("c")
            self.wait(0.5)
        self.clear_scene()

    def crow(self):
        w = archive.WEIR_2002.data
        head = heading(r"The last tool: \ other animals")
        tube = VGroup(Line([-5.6, 1.5, 0], [-5.6, -1.6, 0], color=GREY_B, stroke_width=4),
                      Line([-4.4, 1.5, 0], [-4.4, -1.6, 0], color=GREY_B, stroke_width=4),
                      Line([-5.6, -1.6, 0], [-4.4, -1.6, 0], color=GREY_B, stroke_width=4))
        bucket = VGroup(Rectangle(width=0.6, height=0.45, color=DATA, stroke_width=3, fill_color=DATA, fill_opacity=0.3),
                        Arc(radius=0.3, start_angle=0, angle=PI, color=DATA, stroke_width=3).shift(UP * 0.22))
        bucket.move_to([-5.0, -1.2, 0])
        wire = Line([-3.3, 1.9, 0], [-3.3, -0.4, 0], color=VOLT, stroke_width=5)
        hook = VGroup(Line([-5.0, 2.0, 0], [-5.0, -0.55, 0], color=VOLT, stroke_width=5),
                      Arc(radius=0.2, start_angle=PI, angle=PI, color=VOLT, stroke_width=5).move_arc_center_to([-4.8, -0.55, 0]))
        wl = label(r"a straight wire", font_size=28, color=VOLT).next_to(wire, RIGHT, buff=0.15)
        rows = rows_of([
            (rf"Oxford, 2002: \ a crow called {w['bird']} bends the wire into a hook and lifts the bucket", DATA),
            (r"it looked like insight: \ a bird inventing a tool", WHITE),
            (r"fourteen years later: \ wild crows of her species bend their twig tools as a matter of routine", BAD),
            (r"When crows, apes and octopuses, \ built so differently, \ reach similar solutions, \ the solutions tell "
             r"us what the problem demands.", P.ACCENT),
        ], 7.4, 30, 0.3).move_to([2.9, -0.3, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.WEIR_2002.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The last tool is other animals. <bookmark mark='a'/> In 2002, in Oxford, a New Caledonian "
            f"crow called {w['bird']} was given a straight piece of wire, and a small bucket of food at "
            "the bottom of a tube. She bent the wire into a hook and lifted the bucket out. "
            "<bookmark mark='b'/> It looked like insight: a bird inventing a tool. <bookmark mark='c'/> "
            "Fourteen years later, field workers reported that wild crows of her species bend their twig "
            "tools as a matter of routine. So she was probably doing what her species does, with a new "
            "material. Still remarkable. Less of a miracle. <bookmark mark='d'/> That's how comparative "
            "work goes: a striking observation, and then the careful question of what it shows. Its "
            "value is this. When crows, apes and octopuses, whose brains are built very differently, "
            "arrive at similar solutions, the solutions tell us what the problem demands, and not just "
            "how one kind of brain happens to work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(tube), FadeIn(bucket), FadeIn(wire), FadeIn(wl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(FadeOut(wire), FadeOut(wl), FadeIn(hook))
            self.play(bucket.animate.shift(UP * 1.5), hook.animate.shift(UP * 1.5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
