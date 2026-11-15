from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Objects(VoiceoverScene):
    def construct(self):
        self.card()
        self.drawbridge()
        self.critique()
        self.core()

    def card(self):
        card = chapter_card(5, r"Objects", r"Do young infants know that hidden things still exist?",
                            lit={1985: r"Baillargeon et al.", 1987: r"Baillargeon", 2000: r"Bogartz et al.",
                                 2007: r"Spelke \& Kinzler"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. Objects."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def drawbridge(self):
        head = heading(r"The drawbridge")
        floor = Line([-6.2, -1.6, 0], [-1.0, -1.6, 0], color=GREY_B)
        pivot = np.array([-3.6, -1.6, 0])
        screen = Rectangle(width=0.12, height=1.8, color=LOOK, fill_color=LOOK, fill_opacity=0.7).move_to(
            pivot + np.array([0, 0.9, 0]))
        box = Square(0.8, color=OBJ, fill_color=OBJ, fill_opacity=0.7).move_to([-2.2, -1.2, 0])
        arc = Arc(radius=1.4, start_angle=PI / 2, angle=-PI / 2, arc_center=pivot, color=GREY_B, stroke_width=2)
        rows = rows_of([
            (r"Ren\'ee Baillargeon, \ Elizabeth Spelke and Stanley Wasserman, \ 1985: \ infants are habituated to a "
             r"screen rotating through 180 degrees, \ like a drawbridge", WHITE),
            (r"then a box is placed behind it: \ the screen stops where it meets the box \ (possible), \ or rotates "
             r"the full 180 degrees, \ through the space the box occupies \ (impossible)", OBJ),
            (r"5-month-olds looked longer at the impossible event; \ in 1987, \ 4.5-month-olds, \ and 3.5-month-olds "
             r"who habituated quickly, \ did too", LOOK),
            (r"read as: \ young infants know the box still exists behind the screen, \ and that solid things do "
             r"not pass through each other", GOOD),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Baillargeon, \ Spelke \& Wasserman (1985); \ Baillargeon (1987)")
        with self.voiceover(
            "If Piaget was right, a young infant shouldn't know that a hidden object still exists. "
            "<bookmark mark='a'/> In 1985 Renée Baillargeon, Elizabeth Spelke and Stanley Wasserman habituated "
            "infants to a screen rotating through a hundred and eighty degrees, like a drawbridge. "
            "<bookmark mark='b'/> Then a box was placed behind it. In the possible event, the screen stopped where "
            "it would meet the box. In the impossible event, it rotated the full hundred and eighty degrees, through "
            "the space the box occupied. <bookmark mark='c'/> Five-month-olds looked longer at the impossible event. "
            "In 1987 Baillargeon found the same in four-and-a-half-month-olds, and in three-and-a-half-month-olds "
            "who habituated quickly. <bookmark mark='d'/> The reading: young infants know the box still exists "
            "behind the screen, and that solid objects don't pass through each other. Months before Piaget's "
            "infants searched for hidden toys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(floor), FadeIn(screen))
            vo.wait_until("a")
            self.play(Rotate(screen, -PI, about_point=pivot), FadeIn(rows[0]), run_time=2.0)
            self.play(Rotate(screen, PI, about_point=pivot), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(box), Create(arc), FadeIn(rows[1]))
            # the possible event: the screen stops where its face meets the box's top corner
            self.play(Rotate(screen, -np.arctan2(1.0, 0.8), about_point=pivot), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def critique(self):
        head = heading(r"A rich reading, \ and a lean one")
        rows = rows_of([
            (r"the impossible event has more motion: \ the screen sweeps 180 degrees instead of about 112", LOST),
            (r"after habituating to a 180-degree sweep, \ a longer look at it could be a familiarity preference, "
             r"\ not surprise", LOST),
            (r"Richard Bogartz, \ Jeanne Shinskey and Thomas Schilling, \ 2000: \ with 5.5-month-olds, \ the "
             r"number of familiarization trials changed which event infants preferred; \ they concluded the study "
             r"did not show object permanence", GREY_A),
            (r"later experiments by Baillargeon and others used many controls and found infants reasoning about "
             r"hidden objects in other designs; \ the looking pattern replicates, \ its meaning is still argued", OBJ),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Bogartz, \ Shinskey \& Schilling (2000)")
        with self.voiceover(
            "Then the lean readings arrived. <bookmark mark='a'/> The impossible event has more motion in it: the "
            "screen sweeps a hundred and eighty degrees, instead of stopping short. <bookmark mark='b'/> And infants "
            "had just been habituated to a hundred-and-eighty-degree sweep, so a longer look at it could be a "
            "preference for the familiar, not surprise. <bookmark mark='c'/> In 2000 Richard Bogartz, Jeanne "
            "Shinskey and Thomas Schilling ran the design with five-and-a-half-month-olds, and found that the number "
            "of familiarization trials changed which event infants preferred. They concluded that the study did not "
            "show object permanence. <bookmark mark='d'/> Baillargeon and others went on to use many controls, and "
            "found infants reasoning about hidden objects in other designs. The looking pattern replicates; its "
            "meaning is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def core(self):
        head = heading(r"Core knowledge")
        prin = VGroup(*[VGroup(word_chip(n, color=OBJ, font_size=22, width=2.8), wrapped_label(t, 3.2, 17, WHITE))
                        .arrange(DOWN, buff=0.15) for n, t in (
            (r"cohesion", r"objects move as connected, \ bounded wholes"),
            (r"continuity", r"they move on connected paths, \ and do not pass through each other"),
            (r"contact", r"they do not act on each other at a distance"))]).arrange(RIGHT, buff=0.4)
        prin.move_to([0, 1.0, 0])
        rows = rows_of([
            (r"Elizabeth Spelke: \ infants start with a few systems of core knowledge, \ for objects, \ number, "
             r"\ agents and places, \ each with a few principles, \ shared with other animals", WHITE),
            (r"learning builds on them; \ it does not have to create them from sensation alone", GOOD),
            (r"the alternative: \ the principles are learned fast, \ from very early experience; \ the next "
             r"chapters weigh both", GREY_A),
        ], 12.2, 24, 0.35).move_to([0, -1.9, 0])
        tag = published_tag(r"Spelke \& Kinzler (2007)")
        with self.voiceover(
            "Elizabeth Spelke turned results like these into a theory. <bookmark mark='a'/> For objects she "
            "proposed three principles. Cohesion: objects move as connected, bounded wholes. Continuity: they move "
            "on connected paths, and don't pass through each other. Contact: they don't act on each other at a "
            "distance. <bookmark mark='b'/> Infants start, on this view, with a few systems of core knowledge, for "
            "objects, number, agents and places, each with a few principles, and shared with other animals. "
            "<bookmark mark='c'/> Learning builds on them; it doesn't have to create them from sensation alone. "
            "<bookmark mark='d'/> The alternative is that the principles are learned very fast, from early "
            "experience. The next chapters weigh both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in prin], lag_ratio=0.4), run_time=3.0)
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
