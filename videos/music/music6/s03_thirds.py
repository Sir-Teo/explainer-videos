from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Thirds(SoundScene):
    def construct(self):
        chapter(self, 2, r"The other comma", r"Can the fifths and the thirds both be pure?", lit=(1584,), extra=((1558, r"Zarlino: \ the pure third"),))
        self.four_fifths()
        self.three_thirds()
        self.lattice()
        self.just_wolf()

    # ------------------------------------------------------------------
    def four_fifths(self):
        d = load("syntonic")
        c = clip("syntonic.thirds")
        chain = VGroup(*[label(n, font_size=40, color=TUNE if n in ("C", "E") else GREY_A) for n in ("C", "G", "D", "A", "E")]).arrange(RIGHT, buff=1.3).move_to(UP * 2.2)
        arrows = VGroup(*[VGroup(Arrow(a.get_right(), b.get_left(), buff=0.12, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.2),
                                 MathTex(r"\times\tfrac32", font_size=26, color=GREY_B).move_to((a.get_right() + b.get_left()) / 2 + UP * 0.35))
                          for a, b in zip(chain[:-1], chain[1:])])
        eqs = VGroup(MathTex(r"\left(\tfrac32\right)^4 = \tfrac{81}{16} \quad\Rightarrow\quad \text{two octaves down: } \tfrac{81}{64}", font_size=34),
                     MathTex(r"\text{the pure third: } \tfrac54 = \tfrac{80}{64}", font_size=34, color=GOOD),
                     MathTex(rf"\tfrac{{81}}{{64}} \div \tfrac{{80}}{{64}} = \tfrac{{81}}{{80}}: \quad {d['comma_cents']:.1f}\ \text{{cents}}", font_size=36, color=BAD)
                     ).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        bx = boxes((r"A", r"B"), buff=0.6, width=2.6, height=1.0, font_size=40).move_to(RIGHT * 3.6 + DOWN * 2.3)
        q = listen_card(r"Two major thirds on C, \ A and B. \\ One is made of four pure fifths. \ One is 5 to 4. \ Which is which?", width=6.4, font_size=24).move_to(LEFT * 3.3 + DOWN * 2.3)
        with self.voiceover(
            "There is a second gap, and for the history of music it mattered more. Go up four pure fifths from C: "
            "G, D, A, E. <bookmark mark='a'/> That E is eighty-one sixteenths of C, or, two octaves lower, "
            "eighty-one to sixty-four. <bookmark mark='b'/> But the smooth major third, the one that sits in a "
            "valley of Part 5's curve, is five to four, which is eighty to sixty-four. <bookmark mark='c'/> The "
            f"E reached by fifths is too high, by the ratio eighty-one to eighty: {say(d['comma_cents'], 1)} "
            "cents. This is the syntonic comma. It is nearly the same size as the Pythagorean comma, and it has "
            "nothing to do with it: this one is the disagreement between the number three and the number five. "
            "Here are the two thirds, in an order I will not tell you. Which is which?"
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in chain], lag_ratio=0.3), LaggedStart(*[FadeIn(x) for x in arrows], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(bx), FadeIn(q))
        with self.listen(c) as snd:
            window(snd, r"third A, \ then third B", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=UR)
            for ev, b in zip(("fifths", "pure"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        tags = VGroup(label(r"four fifths: \ 81 : 64", font_size=24, color=BAD).next_to(bx[0], UP, buff=0.12), label(r"pure: \ 5 : 4", font_size=24, color=GOOD).next_to(bx[1], UP, buff=0.12))
        self.play(FadeIn(tags), run_time=0.4)
        with self.voiceover(
            f"A was the third made of fifths. It beats, {say(d['beat'])} times a second on these notes. B is still. So here "
            "is the dilemma in one sentence: pure fifths give bad thirds. And by about 1500, composers wanted "
            "thirds in every chord."
        ):
            self.play(Indicate(bx[1][0], color=GOOD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_thirds(self):
        d = load("syntonic")
        c = clip("syntonic.diesis")
        chain = VGroup(*[label(n, font_size=40, color=TUNE if k in (0, 3) else GREY_A) for k, n in enumerate(("C", "E", r"G$\sharp$", r"B$\sharp$"))]).arrange(RIGHT, buff=1.7).move_to(UP * 2.2)
        arrows = VGroup(*[VGroup(Arrow(a.get_right(), b.get_left(), buff=0.12, color=GOOD, stroke_width=3, max_tip_length_to_length_ratio=0.2),
                                 MathTex(r"\times\tfrac54", font_size=26, color=GOOD).move_to((a.get_right() + b.get_left()) / 2 + UP * 0.35))
                          for a, b in zip(chain[:-1], chain[1:])])
        p, q = d["three_thirds"]
        eqs = VGroup(MathTex(rf"\left(\tfrac54\right)^3 = \tfrac{{{p}}}{{{q}}} = 1.953", font_size=36), MathTex(r"\text{an octave: } 2 = \tfrac{128}{64}", font_size=36, color=GOOD),
                     MathTex(rf"\text{{short by }} \tfrac{{128}}{{125}}: \quad {d['diesis_cents']:.0f}\ \text{{cents}}", font_size=38, color=BAD)).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        bx = boxes((r"C and the C above", r"C and B$\sharp$"), buff=0.6, width=3.6, height=1.1, font_size=28).move_to(DOWN * 2.2)
        with self.voiceover(
            "And there is a third gap, which the thirds make all by themselves. Go up three pure major thirds from "
            "C: to E, to G sharp, and to B sharp, which on a keyboard is the same key as C. <bookmark mark='a'/> "
            "Five quarters, three times over, is a hundred and twenty-five sixty-fourths. <bookmark mark='b'/> An "
            "octave is a hundred and twenty-eight sixty-fourths. <bookmark mark='c'/> Three pure thirds fall short "
            f"of the octave by {say(d['diesis_cents'])} cents, nearly a quarter-tone. Here is a true octave, and "
            "then C against that B sharp."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in chain], lag_ratio=0.3), LaggedStart(*[FadeIn(x) for x in arrows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"an octave, \ then C against B sharp", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("octave", "thirds"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.2)
        with self.voiceover(
            "So a keyboard with pure thirds cannot use one key for G sharp and for A flat, or for B sharp and for "
            "C. They are different notes. Remember this gap. It is about to turn into a wolf."
        ):
            self.play(Indicate(eqs[2], color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self):
        d = load("syntonic")
        sx, sy = 1.9, 1.5
        origin = LEFT * 1.2 + DOWN * 0.3
        nodes = {}
        g = VGroup()
        for n in d["lattice"]:
            if n["fifths"] is None:
                continue
            p = origin + RIGHT * sx * n["fifths"] + UP * sy * n["thirds"]
            col = TUNE if n["name"] in ("C", "D", "E", "F", "G", "A", "B") else GREY_B
            node = VGroup(Circle(radius=0.36, stroke_color=col, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=1), label(note_tex(n["name"]), font_size=24, color=col),
                          MathTex(rf"\tfrac{{{n['ratio'][0]}}}{{{n['ratio'][1]}}}", font_size=22, color=GREY_B))
            node[0].move_to(p)
            node[1].move_to(p)
            node[2].next_to(node[0], DOWN, buff=0.06)
            nodes[n["name"]] = node
            g.add(node)
        lines = VGroup()
        for a in d["lattice"]:
            for b in d["lattice"]:
                if a["fifths"] is None or b["fifths"] is None:
                    continue
                if (b["fifths"] - a["fifths"], b["thirds"] - a["thirds"]) in ((1, 0), (0, 1)):
                    horizontal = b["thirds"] == a["thirds"]
                    lines.add(Line(nodes[a["name"]][0].get_center(), nodes[b["name"]][0].get_center(), color=AIR if horizontal else GOOD, stroke_width=2.5).set_z_index(-1))
        axes_l = VGroup(VGroup(Arrow(ORIGIN, RIGHT * 1.3, buff=0, color=AIR, stroke_width=3), label(r"a pure fifth, \ $\times\tfrac32$", font_size=22, color=AIR)).arrange(RIGHT, buff=0.15),
                        VGroup(Arrow(ORIGIN, UP * 0.9, buff=0, color=GOOD, stroke_width=3), label(r"a pure third, \ $\times\tfrac54$", font_size=22, color=GOOD)).arrange(RIGHT, buff=0.15)
                        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        head = label(r"just intonation: \ every note a pure fifth or a pure third from its neighbours", font_size=24, color=GREY_A).to_edge(UP, buff=0.35).shift(RIGHT * 1.9)
        tri = VGroup(*[Line(nodes[a][0].get_center(), nodes[b][0].get_center(), color=TUNE, stroke_width=6) for a, b in (("C", "E"), ("E", "G"), ("C", "G"))]).set_z_index(-0.5)
        tl = label(r"a triangle is a pure chord", font_size=24, color=TUNE).next_to(nodes["E"], UP, buff=0.5)
        with self.voiceover(
            "The obvious cure is to use both. Lay the notes out on a grid. <bookmark mark='a'/> One step to the "
            "right is a pure fifth. One step up is a pure third. Every note is then a ratio of small powers of "
            "two, three and five. <bookmark mark='b'/> This is just intonation, and the seven notes of the C "
            "major scale sit in it as a compact patch. <bookmark mark='c'/> Any three notes at the corners of one "
            "of these triangles form a chord that is pure in every interval: no beats at all. The major scale "
            "contains three of them, on C, on F and on G. Renaissance theorists thought they had found the true "
            "scale of nature."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(axes_l), FadeIn(lines), FadeIn(g), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(tri), FadeIn(tl))
        self.nodes, self.lat = nodes, VGroup(g, lines, tri, tl, axes_l, head)
        self.wait(0.3)

    # ------------------------------------------------------------------
    def just_wolf(self):
        d = load("syntonic")
        c = clip("syntonic.wolf")
        nodes = self.nodes
        bad = DashedLine(nodes["D"][0].get_center(), nodes["A"][0].get_center(), color=BAD, stroke_width=5, dash_length=0.12).set_z_index(-0.4)
        p, q = d["d_a_ratio"]
        bl = VGroup(label(rf"D to A: \ ${p}:{q}$", font_size=26, color=BAD), label(rf"{d['d_a_cents']:.0f} cents: \ a comma short of a fifth", font_size=24, color=BAD)
                    ).arrange(DOWN, buff=0.1).scale(0.9).move_to(RIGHT * 5.0 + DOWN * 1.3)
        with self.voiceover(
            "They had not, and you can see why on the grid. D is two steps to the right of C. A is one step to "
            "the left and one up. <bookmark mark='a'/> They are not neighbours. The fifth from D up to A, which "
            f"every piece in C major uses, comes out as {p} to {q}: a whole comma short of a pure fifth. It is "
            "just intonation's own wolf, and it is in the middle of the scale. Here is the fifth from C to G, "
            "and then the fifth from D to A."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(bad), FadeIn(bl), Indicate(nodes["D"][0], color=BAD), Indicate(nodes["A"][0], color=BAD))
        good = Line(nodes["C"][0].get_center(), nodes["G"][0].get_center(), color=GOOD, stroke_width=7).set_z_index(-0.3)
        self.add(good)
        with self.listen(c) as snd:
            window(snd, r"C to G, \ then D to A, \ in just intonation", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            t1 = snd.time_of("da")
            snd.drive(good, lambda m, t: m.set_stroke(opacity=(0.6 + 0.4 * np.sin(18 * t)) if t < t1 - 0.3 else 0.2))
            snd.drive(bad, lambda m, t: m.set_stroke(opacity=(0.6 + 0.4 * np.sin(18 * t)) if t >= t1 else 0.3))
        with self.voiceover(
            "A singer could fix that by singing a slightly different D when it has to go with A. But then there "
            "are two Ds, a comma apart, and a keyboard has only one key for each. Worse is to come. Even with "
            "voices, which can sing any pitch they like, pure chords lead somewhere unexpected."
        ):
            self.play(Indicate(nodes["D"][0], color=WHITE, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()
