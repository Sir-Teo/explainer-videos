from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403

LEVELS = [(r"images, shadows", r"imagining", GREY_B), (r"physical things", r"belief", P.TRUE),
          (r"mathematical objects", r"thought", P.CLAIM), (r"the Forms", r"understanding", GOAL)]


class Line(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The divided line and the cave", r"Are there levels of knowing?", lit=(-380,),
                            part=PART)
        with self.voiceover("Chapter six. The divided line and the cave."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.line()
        self.equal()
        self.thirdman()
        self.cave()

    def segs(self, k):
        d = load("line")
        cut = next(c for c in d["cuts"] if c["k"] == k)
        return [a / b for a, b in cut["segments"]]

    def line(self):
        segs = self.segs([2, 1])
        H = 6.0
        y0 = -3.0
        g = VGroup()
        y = y0
        bars, labels_ = VGroup(), VGroup()
        for (obj, faculty, col), s in zip(LEVELS, segs[::-1]):
            h = s * H
            r = Rectangle(width=0.5, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.35)
            r.move_to([-3.6, y + h / 2, 0])
            bars.add(r)
            labels_.add(VGroup(label(obj, font_size=26, color=col), label(faculty, font_size=22, color=GREY_A))
                        .arrange(RIGHT, buff=0.4).next_to(r, RIGHT, buff=0.4))
            y += h
        q = quote_card(r"Take a line divided into two unequal sections, and cut each section again in the same "
                       r"ratio.", r"Socrates, \textit{Republic} VI, 509d", r"trans.\ Grube and Reeve", width=6.0,
                       font_size=24).to_corner(UR, buff=0.4)
        with self.voiceover(
            "In the Republic, Plato draws knowledge as a line. <bookmark mark='a'/>Take a line, he says, divided "
            "into two unequal parts, and cut each part again in the same ratio. <bookmark mark='b'/>From the bottom: "
            "images and shadows, grasped by mere imagining; physical things, grasped by belief; mathematical "
            "objects, grasped by thought; and at the top the Forms themselves, grasped by understanding. Each level "
            "is the reality of which the level below is an image."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in labels_], lag_ratio=0.35))
        self.bars, self.labels_ = bars, labels_

    def equal(self):
        d = load("line")
        bars = self.bars
        mid = VGroup(bars[1], bars[2])
        box = SurroundingRectangle(mid, color=GOAL, buff=0.08)
        rows = VGroup()
        for c in d["cuts"]:
            k = c["k"][0] / c["k"][1]
            s = [a / b for a, b in c["segments"]]
            rows.add(MathTex(rf"k = {k:g}:\quad {s[0]:.3f},\ \ {s[1]:.3f},\ \ {s[2]:.3f},\ \ {s[3]:.3f}", font_size=28))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35).set_y(-0.4)
        for r in rows:
            pass
        proof = MathTex(r"\frac{k}{1+k}\cdot\frac{1}{1+k} \;=\; \frac{1}{1+k}\cdot\frac{k}{1+k}", font_size=36,
                        color=GOAL).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "There is a small surprise hidden in Plato's instruction. <bookmark mark='a'/>Whatever ratio you choose, "
            "the two middle segments, physical things and mathematical objects, always come out exactly equal. "
            "<bookmark mark='b'/>Here are four ratios, computed in exact fractions: the second and third numbers "
            "agree every time. <bookmark mark='c'/>The proof is one line: each middle piece is the product of the "
            "same two fractions, in a different order. Did Plato intend it? Scholars disagree. But it is the kind "
            "of fact that made Plato think mathematics was a window onto a reality more exact than the visible world."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(box))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Write(proof))
        self.clear_scene()

    def cave(self):
        wall_ = Rectangle(width=6.0, height=2.6, stroke_color=GREY_C, stroke_width=2, fill_color=GREY_E,
                          fill_opacity=0.4).move_to([-3.0, 0.4, 0])
        fire = VGroup(*[Triangle(fill_color=c, fill_opacity=0.9, stroke_width=0).scale(s).move_to([3.8, -0.3 + dy, 0])
                        for c, s, dy in ((P.AGENT, 0.45, 0), (GOAL, 0.3, 0.1))])
        people = VGroup(*[Circle(radius=0.18, stroke_color=WHITE, stroke_width=2).move_to([x, -1.8, 0])
                          for x in (-4.2, -3.4, -2.6, -1.8)])
        shadows = VGroup(*[Ellipse(width=0.9, height=0.5, fill_color=BLACK, fill_opacity=0.7, stroke_width=0)
                           .move_to([x, 0.6, 0]) for x in (-4.4, -3.0, -1.6)])
        carried = VGroup(*[Square(0.35, stroke_color=GREY_A, stroke_width=2).move_to([x, 0.2, 0]) for x in (1.4, 2.0, 2.6)])
        sun = Circle(radius=0.5, fill_color=GOAL, fill_opacity=0.9, stroke_width=0).move_to([5.6, 2.6, 0])
        lab = label(r"the cave \ (\textit{Republic} VII, 514a)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.35)
        sch = schematic_tag()
        with self.voiceover(
            "Book Seven turns the line into a story. <bookmark mark='a'/>Prisoners are chained in a cave, facing a "
            "wall. Behind them a fire burns, and people carry objects past it, so that the prisoners see only "
            "shadows, and take the shadows for reality. <bookmark mark='b'/>One prisoner is freed, turns, is dazzled "
            "by the fire, and is dragged up into the sunlight, where at last he sees things as they are. "
            "<bookmark mark='c'/>Returned to the cave, he cannot see the shadows well any more, and the others "
            "think the journey has ruined him. <bookmark mark='d'/>The parable asks the question the next parts "
            "take up with tools Plato did not have: how could we ever know that what we see is not a shadow? It is "
            "Descartes' question in Part 10, and the brain in a vat in Part 11."
        ) as vo:
            self.play(FadeIn(wall_), FadeIn(people), FadeIn(sch), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(fire), FadeIn(carried), FadeIn(shadows))
            vo.wait_until("b")
            self.play(people[-1].animate.move_to([4.6, 1.8, 0]), FadeIn(sun), run_time=2)
            vo.wait_until("c")
            self.play(people[-1].animate.move_to([-1.8, -1.8, 0]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(shadows, color=GREY_A))
        self.clear_scene()

    def thirdman(self):
        d = load("thirdman")
        pl = PriceList([(c["key"], c["text"]) for c in d["claims"]], mus=d["mus"], radius=2.75, width=4.0,
                       font_size=21, center=[0, -0.5, 0])
        title = label(r"The Price List: \ the Third Man (\textit{Parmenides} 132a)", font_size=32, color=P.PRICE)
        title.to_edge(UP, buff=0.25)
        bridge = note(r"bridge premise (Vlastos 1954): \ one over many, self-predication and non-identity "
                      r"generate a second Form, a third, \dots", font_size=20).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Plato saw a problem with his own Forms. In the Parmenides, the old philosopher presses young Socrates "
            "with a regress that Aristotle later called the Third Man. <bookmark mark='a'/>Four claims. Any group of "
            "large things has a Form of Largeness over it. The Form of Largeness is itself large. A Form is not one "
            "of the things it is over. And there is exactly one Form of Largeness. <bookmark mark='b'/>Gregory "
            "Vlastos showed in 1954 that the first three generate a second Form, over the large things and the first "
            "Form, and then a third: an infinite regress, contradicting uniqueness."
        ) as vo:
            self.play(FadeIn(title), *[FadeIn(c.copy().set_opacity(0.15)) for c in pl.cards])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in pl.cards], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(pl.conflict), FadeIn(bridge))
        a1, _ = pl.position(("SP",), r"Deny self-predication", r"most modern readers: the Form is not large the "
                            r"way large things are", width=3.0)
        with self.voiceover(
            "Most modern readers take the exit through self-predication: the Form of Largeness is not large in the "
            "way an elephant is large. Others deny that every group has a Form, as Aristotle did. Plato never said "
            "which exit he chose, and the dialogue ends without one."
        ):
            self.play(*a1, run_time=1.2)
        self.play(*pl.reset())
        self.clear_scene()
