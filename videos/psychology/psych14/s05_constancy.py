from __future__ import annotations

import numpy as np

from videos.psychology.psych14.common import *  # noqa: F403


def muller_lyer(length=3.0, fins="out", fin=0.55, angle=35, color=WHITE, stroke=4):
    """A shaft with fins at both ends; ``fins`` 'out' (tails, looks longer) or 'in' (arrowheads, looks shorter)."""
    a = np.radians(angle)
    g = VGroup(Line([-length / 2, 0, 0], [length / 2, 0, 0], color=color, stroke_width=stroke))
    for end, s in ((-length / 2, -1), (length / 2, 1)):
        d = s if fins == "out" else -s
        for v in (1, -1):
            g.add(Line([end, 0, 0], [end + d * fin * np.cos(a), v * fin * np.sin(a), 0], color=color, stroke_width=stroke))
    return g


class Constancy(VoiceoverScene):
    def construct(self):
        self.card()
        self.size()
        self.ponzo()
        self.mullerlyer()
        self.culture()

    def card(self):
        card = chapter_card(4, r"Constancy, \ and illusions", r"Why do things keep their size as they move away?",
                            lit={1889: r"Müller-Lyer", 1963: r"Gregory", 1966: r"Segall"}, part=PART,
                            scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. Constancy, and illusions."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def size(self):
        head = heading(r"Size constancy")
        eq = MathTex(r"\text{seen size} \;\approx\; \text{retinal angle} \times \text{seen distance}", font_size=42)
        eq.move_to([0, 2.0, 0])
        people = VGroup()
        for k, dist in enumerate((1.0, 2.0, 4.0)):
            h = 2.2 / dist
            fig = VGroup(Circle(radius=0.16 * h, color=WORLD, stroke_width=3),
                         Line(ORIGIN, DOWN * 0.6 * h, color=WORLD, stroke_width=3))
            fig[1].next_to(fig[0], DOWN, buff=0)
            fig.move_to([-4.6 + 3.0 * k, 0, 0])
            fig.shift(UP * (-0.95 + 0.4 * k - fig.get_bottom()[1]))
            people.add(fig)
        labs = VGroup(*[label(t, font_size=22, color=GREY_B).next_to(people[k], RIGHT, buff=0.2)
                        for k, t in enumerate((r"2 m", r"4 m", r"8 m"))])
        rows = rows_of([
            (r"a person walking away halves their image with each doubling of distance; \ they do not seem to shrink", WHITE),
            (r"the visual system multiplies by the distance it thinks it sees", POST),
            (r"get the distance wrong, \ and the size goes wrong with it", PRIOR),
        ], 12.4, 28, 0.3).to_edge(DOWN, buff=0.7)
        tag = note(r"drawn").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The inverse problem had a size and a distance traded against each other. Here's what the visual system "
            "does about it. <bookmark mark='a'/> A person walking away from you halves the size of their image on your "
            "retina each time their distance doubles. They don't seem to shrink. A friend across the room looks the "
            "size of a friend, not of a doll. <bookmark mark='b'/> To a first approximation, the visual system "
            "multiplies the size of the image by the distance it thinks it sees, and the product stays constant. "
            "That's size constancy. <bookmark mark='c'/> It's an excellent bet, as long as the distance is right. "
            "Get the distance wrong, and the size goes wrong with it, which is what the Ames room did, and what the "
            "next two figures do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in people], lag_ratio=0.5), FadeIn(labs), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(eq))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def ponzo(self):
        head = heading(r"The Ponzo illusion")
        rails = VGroup(Line([-2.0, -2.6, 0], [-0.25, 2.0, 0], color=GREY_B, stroke_width=4),
                       Line([2.0, -2.6, 0], [0.25, 2.0, 0], color=GREY_B, stroke_width=4))
        ties = VGroup(*[Line([-1.9 + 0.36 * k, -2.35 + 0.95 * k, 0], [1.9 - 0.36 * k, -2.35 + 0.95 * k, 0],
                             color=GREY_D, stroke_width=2) for k in range(5)])
        top = Line([-0.6, 1.2, 0], [0.6, 1.2, 0], color=WORLD, stroke_width=8)
        bot = Line([-0.6, -1.6, 0], [0.6, -1.6, 0], color=WORLD, stroke_width=8)
        fig = VGroup(rails, ties, top, bot).move_to([-3.5, -0.3, 0])
        rows = rows_of([
            (r"two bars of the same length; \ the upper one looks longer", WHITE),
            (r"the converging lines say: \ the upper bar is further away", LIKE),
            (r"same image, \ greater distance, \ so a larger thing", POST),
        ], 5.6, 28, 0.36).move_to([3.4, 0.2, 0])
        keep_in_frame(rows)
        tag = note(r"drawn after Ponzo (1911)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Mario Ponzo described this one in 1911. <bookmark mark='a'/> Two yellow bars of exactly the same length, "
            "between converging lines. The upper bar looks longer. <bookmark mark='b'/> The converging lines are a "
            "perspective cue. They look like railway tracks running away from you, and they say that the upper bar "
            "is further away. <bookmark mark='c'/> Two bars cast the same image; the one that's further away must be "
            "the larger. Size constancy, applied to a page where nothing is further away than anything else, gives "
            "the wrong answer. The illusion isn't a failure of the mechanism; it's the mechanism, working on a "
            "picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fig), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(top), Indicate(bot))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def mullerlyer(self):
        head = heading(r"The Müller-Lyer illusion")
        a = muller_lyer(3.0, "in", color=WORLD).move_to([-3.3, 1.3, 0])
        b = muller_lyer(3.0, "out", color=WORLD).move_to([-3.3, -0.6, 0])
        guides = VGroup(DashedLine([-4.8, 2.0, 0], [-4.8, -1.4, 0], color=GREY_C, stroke_width=2),
                        DashedLine([-1.8, 2.0, 0], [-1.8, -1.4, 0], color=GREY_C, stroke_width=2))
        rows = rows_of([
            (r"two shafts of the same length; \ with the fins turned out, \ it looks longer", WHITE),
            (r"Gregory, \ 1963: \ the fins look like corners; \ out-turned is a far inside corner, \ in-turned a near outside one", LIKE),
            (r"if so, \ the illusion should depend on growing up among corners", PRIOR),
            (r"the course's experiment measures your own illusion", YOU),
        ], 6.0, 26, 0.32).move_to([3.4, 0.1, 0])
        keep_in_frame(rows)
        tag = note(r"drawn after Müller-Lyer (1889)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The most studied illusion of all was published by Franz Müller-Lyer in 1889. "
            "<bookmark mark='a'/> Two shafts of exactly the same length. The one with the fins turned outward looks "
            "longer than the one with them turned in. The dashed lines show their ends line up. "
            "<bookmark mark='b'/> Richard Gregory proposed in 1963 that this is size constancy too. Fins turned in "
            "look like the edges of a building's outside corner, coming toward you; fins turned out look like the "
            "inside corner of a room, going away. The shaft that seems further away is seen as longer. "
            "<bookmark mark='c'/> That explanation makes a prediction: the illusion should depend on growing up among "
            "rectangular buildings and rooms. <bookmark mark='d'/> And this part's interactive experiment measures "
            "your own illusion, with the staircase method from Part 11."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(guides))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def culture(self):
        head = heading(r"A carpentered world?")
        rows = rows_of([
            (r"1966: \ Segall, \ Campbell and Herskovits test people in more than a dozen societies", WHITE),
            (r"San foragers in the Kalahari show the least illusion; \ samples from European-derived towns the most", LIKE),
            (r"for fifty years, \ the textbook example of culture shaping perception", GREY_A),
            (r"2025: \ Amir and Firestone reopen it: \ the methods varied, \ and newly sighted children and many animals see it", BAD),
            (r"the illusion is real; \ whether its size depends on buildings is open", PRIOR),
        ], 12.6, 29, 0.36).move_to([0, -0.1, 0])
        tag = published_tag(rf"{archive.SEGALL_1966.cite}; \ {archive.AMIR_FIRESTONE_2025.cite}", corner=DR)
        with self.voiceover(
            "In 1966, Marshall Segall, Donald Campbell and Melville Herskovits published the test of that prediction. "
            "<bookmark mark='a'/> Fieldworkers showed versions of the figure to people in more than a dozen societies. "
            "<bookmark mark='b'/> The San foragers of the Kalahari showed the least illusion, and the samples from "
            "towns of European descent the most. <bookmark mark='c'/> For fifty years this was the textbook example "
            "of culture shaping perception itself, and it's often cited as a reason that psychology's usual samples "
            "aren't representative of humanity. <bookmark mark='d'/> In 2025, Dorsa Amir and Chaz Firestone reopened "
            "it. The methods differed from site to site in ways that could make the differences by themselves; children "
            "in India who gained their sight after cataract surgery saw the illusion within days, before corners "
            "could have taught them anything; and the illusion has been found in species that have never seen a "
            "building, birds and fish among them. <bookmark mark='e'/> The illusion is real. Whether its size depends "
            "on a carpentered environment is open, and nobody has repeated the study with modern methods. We'll put "
            "it in the Ledger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
