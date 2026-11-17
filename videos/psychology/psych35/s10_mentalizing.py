from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


def side_brain(color=GREY_B) -> VGroup:
    """A schematic left-facing side view of a brain with the temporoparietal junction marked (returns brain, spot)."""
    outline = Ellipse(width=4.2, height=3.0, color=color, stroke_width=3)
    sulcus = VGroup(ArcBetweenPoints([-1.2, 0.2, 0], [0.9, -0.4, 0], angle=-0.4, color=GREY_D, stroke_width=2),
                    ArcBetweenPoints([0.1, 1.4, 0], [-0.2, 0.2, 0], angle=0.3, color=GREY_D, stroke_width=2))
    stem = Line([0.5, -1.4, 0], [0.7, -2.1, 0], color=color, stroke_width=3)
    spot = Dot([1.05, 0.1, 0], radius=0.28, color=MODEL, fill_opacity=0.85)
    return VGroup(VGroup(outline, sulcus, stem), spot)


class Mentalizing(VoiceoverScene):
    def construct(self):
        self.card()
        self.stories()
        self.region()
        self.overlap()

    def card(self):
        card = chapter_card(9, r"Thinking about thinking", r"Is there a part of the brain for other minds?",
                            lit={2003: r"Saxe \& Kanwisher", 2008: r"Mitchell"}, part=PART, scale=("person", "brain"),
                            marr=("how",))
        with self.voiceover("Chapter nine. Thinking about thinking."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stories(self):
        head = heading(r"Two kinds of false story")
        a = VGroup(word_chip(r"a false belief", color=PERSON, font_size=24, width=5.6),
                   wrapped_label(r"a woman leaves her keys in the drawer; \ while she is out, \ her flatmate moves "
                                 r"them to the shelf; \ where will she look?", 5.6, 21, WHITE)).arrange(DOWN, buff=0.3)
        b = VGroup(word_chip(r"a false photograph", color=CROWD, font_size=24, width=5.6),
                   wrapped_label(r"a photograph shows the keys in the drawer; \ afterwards they are moved to the "
                                 r"shelf; \ where are they in the photograph?", 5.6, 21, WHITE)).arrange(DOWN, buff=0.3)
        VGroup(a, b).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.2, 0])
        intro = rows_of([
            (r"Part 30: \ children learn that other people can believe what is false", GREY_A),
            (r"adults track others' beliefs all day; \ where in the brain, \ and against what comparison?", YOU),
        ], 11.0, 22, 0.25).move_to([0, 2.2, 0])
        foot = wrapped_label(r"both are representations that have fallen out of date; \ only one of them is a "
                             r"mind", 11.0, 22, YOU).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"Saxe \& Kanwisher (2003)")
        with self.voiceover(
            "Part 30 showed children working out that other people can believe something false. Adults do it "
            "constantly, without noticing. Where in the brain does it happen? You need a careful comparison. "
            "<bookmark mark='a'/> Here's a story that needs a false belief. A woman leaves her keys in the drawer. "
            "While she's out, her flatmate moves them to the shelf. Where will she look? <bookmark mark='b'/> And "
            "here's one that's just as hard but has no mind in it. A photograph shows the keys in the drawer. "
            "Afterwards they're moved. Where are they in the photograph? <bookmark mark='c'/> Both are "
            "representations that have fallen out of date. Only one of them is a mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(intro[0]))
            self.wait(3.0)
            self.play(FadeIn(intro[1]))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def region(self):
        head = heading(r"The temporoparietal junction")
        brain, spot = side_brain()
        g = VGroup(brain, spot).move_to([-3.6, 0.0, 0])
        sl = label(r"TPJ", font_size=22, color=MODEL).next_to(spot, RIGHT, buff=0.15)
        front = label(r"front", font_size=15, color=GREY_B).next_to(brain, LEFT, buff=0.1)
        rows = rows_of([
            (r"Saxe and Kanwisher, \ 2003: \ ``People thinking about thinking people''", WHITE),
            (r"a region where the temporal lobe meets the parietal responded to stories about "
             r"false beliefs", MODEL),
            (r"not to false photographs, \ and not to stories about mechanical causes", CROWD),
            (r"the false-belief stories became a standard ``localizer'' for the mentalizing network, \ used in "
             r"a great many later studies", YOU),
        ], 6.0, 21, 0.38).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Saxe \& Kanwisher (2003)")
        with self.voiceover(
            "In 2003 Rebecca Saxe and Nancy Kanwisher put both kinds of story in the scanner. "
            "<bookmark mark='a'/> A region where the temporal lobe meets the parietal "
            "responded to the stories about false beliefs. <bookmark mark='b'/> It didn't respond to the false "
            "photographs, or to stories about mechanical causes. <bookmark mark='c'/> The false-belief stories "
            "became a standard way to find the mentalizing network in any brain, used in a great many later studies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain), FadeIn(front), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(spot, scale=0.5), FadeIn(sl), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def overlap(self):
        head = heading(r"Specific, \ or shared?")
        brain, spot = side_brain()
        g = VGroup(brain, spot).move_to([-3.6, 0.0, 0])
        spot2 = Dot(spot.get_center() + np.array([-0.18, 0.12, 0]), radius=0.28, color=CROWD, fill_opacity=0.6)
        key = legend([(MODEL, r"false-belief stories"), (CROWD, r"an attention-shifting task")],
                     font_size=16).next_to(brain, DOWN, buff=0.5)
        rows = rows_of([
            (r"Mitchell, \ 2008: \ in the same people, \ the false-belief stories and a task with no minds in it, "
             r"\ shifting attention to an unexpected spot (Part 18's cueing), \ engaged overlapping parts of the "
             r"right TPJ", WHITE),
            (r"later studies with finer scans found neighbouring but distinct patches", CROWD),
            (r"the general lesson from Part 8: \ a region that responds is not yet a region that is \emph{for} "
             r"something; \ the comparison task decides what you have found", YOU),
        ], 6.0, 21, 0.38).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Mitchell (2008)")
        with self.voiceover(
            "But is that region for minds? <bookmark mark='a'/> In 2008 Jason Mitchell scanned the same people on "
            "the false-belief stories and on a task with no minds in it: shifting attention to an unexpected spot, "
            "Part 18's cueing. The two engaged overlapping parts of the right junction. <bookmark mark='b'/> Later "
            "studies with finer scans found neighbouring but distinct patches. <bookmark mark='c'/> It's Part 8's "
            "lesson. A region that responds isn't yet a region that is for something. The comparison task decides "
            "what you've found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain), FadeIn(spot))
            vo.wait_until("a")
            self.play(FadeIn(spot2), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(spot2.animate.shift(LEFT * 0.35 + UP * 0.25), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
