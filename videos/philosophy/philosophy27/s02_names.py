from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403

COAT = {"white": "#F4F1E8", "yellow": "#E8C547", "black": "#3A3A44"}


def horse(colour, r=0.32):
    body = Circle(radius=r, color=GREY_B, stroke_width=2, fill_color=COAT[colour], fill_opacity=1.0)
    return body


class Names(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The School of Names", r"Is a white horse a horse?", lit=(-280, 1843), part=PART)
        with self.voiceover("Chapter one. The School of Names."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dialogue()
        self.request()
        self.mohists()

    def dialogue(self):
        d = load("horse")
        hc = history_card(r"c.\ 300 BCE", r"Gongsun Long", r"`On the White Horse' \ (\textit{Bai Ma Lun})", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        claim = label(r"`A white horse is not a horse.'", font_size=34, color=TRUTH).next_to(hc, DOWN, buff=0.4).align_to(
            hc, LEFT)
        herd = d["herd"]
        pos = [np.array([x, y, 0]) for x, y in ((-5.0, -0.9), (-3.9, -1.6), (-2.45, -0.75), (-4.7, -2.35),
                                               (-2.55, -2.15), (-3.6, -0.3))]
        dots = VGroup(*[horse(herd[h]).move_to(p) for h, p in zip(sorted(herd), pos)])
        tags = VGroup(*[label(herd[h], font_size=14, color=GREY_A).next_to(dt, DOWN, buff=0.05)
                        for h, dt in zip(sorted(herd), dots)])
        all_ring = Ellipse(width=3.9, height=3.2, color=REF, stroke_width=3).move_to([-3.75, -1.35, 0])
        all_tag = label(r"horse", font_size=20, color=REF).next_to(all_ring, LEFT, buff=0.1)
        wh = [i for i, h in enumerate(sorted(herd)) if herd[h] == "white"]
        white_ring = SurroundingRectangle(VGroup(*[dots[i] for i in wh]), color=NAME, buff=0.15, corner_radius=0.3)
        white_tag = label(r"white horse", font_size=20, color=NAME).next_to(white_ring, UP, buff=0.08)
        assert d["inclusion"] and not d["identity"]
        reads = VGroup(
            VGroup(label(r"`is' as inclusion:", font_size=24, color=GREY_A),
                   MathTex(r"\text{white horse} \subseteq \text{horse}", font_size=30, color=OK), tv(True, 30)
                   ).arrange(RIGHT, buff=0.3),
            VGroup(label(r"`is' as identity:", font_size=24, color=GREY_A),
                   MathTex(r"\text{white horse} = \text{horse}", font_size=30, color=BAD), tv(False, 30)
                   ).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.3, -0.6, 0])
        foot = label(r"so `a white horse is not a horse' is false on one reading of `is', \ true on the other",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Around 300 BCE, in the period of the Warring States, the Chinese logician Gongsun Long defended a "
            "notorious thesis. <bookmark mark='a'/>A white horse is not a horse. <bookmark mark='b'/>Picture a herd: "
            "white horses, yellow, black. The horses are all of them; the white horses are some of them. "
            "<bookmark mark='c'/>Read is as inclusion, and the white horses are among the horses: the thesis is "
            "false. <bookmark mark='d'/>Read is as identity, and the white horses are not the same as the horses: "
            "the thesis is true. <bookmark mark='e'/>So the puzzle is already a puzzle about what words pick out, "
            "and about what the little word is is doing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(claim))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.1), FadeIn(tags))
            self.play(Create(all_ring), FadeIn(all_tag), Create(white_ring), FadeIn(white_tag))
            vo.wait_until("c")
            self.play(FadeIn(reads[0]))
            vo.wait_until("d")
            self.play(FadeIn(reads[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def request(self):
        d = load("horse")
        head = label(r"Gongsun Long's argument", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        herd = d["herd"]
        names = sorted(herd)

        def row(accept, title, col, y):
            t = label(title, font_size=22, color=col).move_to([-4.2, y, 0])
            hs = VGroup(*[horse(herd[h], 0.26) for h in names]).arrange(RIGHT, buff=0.35).move_to([1.2, y, 0])
            marks = VGroup()
            for h, m in zip(names, hs):
                ok = h in accept
                marks.add(MathTex(r"\checkmark" if ok else r"\times", font_size=26, color=OK if ok else BAD).next_to(
                    m, DOWN, buff=0.1))
            return VGroup(t, hs, marks)

        r1 = row(set(d["horse"]), r"`bring me a horse'", REF, 1.4)
        r2 = row(set(d["white_horse"]), r"`bring me a white horse'", NAME, -0.5)
        assert d["yellow_answers_horse"] and not d["yellow_answers_white_horse"]
        side = stack([(r"a yellow horse answers the first request, \ not the second", GOAL),
                      (r"so `horse' and `white horse' do not pick out the same thing", TRUTH),
                      (r"readers still disagree: \ a sophism, \ a joke, \ or a point about compound terms", HIST)],
                     font_size=21, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "His argument is about requests. <bookmark mark='a'/>If you ask for a horse, a yellow or a black horse "
            "may be brought. <bookmark mark='b'/>If you ask for a white horse, a yellow or black one may not. "
            "<bookmark mark='c'/>So what satisfies the one request does not satisfy the other, and horse and white "
            "horse do not pick out the same thing. <bookmark mark='d'/>Readers still disagree about what Gongsun Long "
            "was doing: a sophism, a provocation, or a serious point about how compound terms like white horse are "
            "built from simple ones. His opponents, the later Mohists, answered with a theory of names."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1[0]), FadeIn(r1[1]))
            self.play(LaggedStart(*[FadeIn(m) for m in r1[2]], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(r2[0]), FadeIn(r2[1]))
            self.play(LaggedStart(*[FadeIn(m) for m in r2[2]], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def mohists(self):
        head = label(r"Names: \ the Mohists and Mill", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [
            (r"unrestricted names", r"`thing': \ every object falls under it", WORLD),
            (r"classifying names", r"`horse': \ everything of a kind", REF),
            (r"private names", r"`Zang': \ one individual, \ a proper name", NAME),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=7.6, x_text=-2.4, label_size=22, text_size=21)
        tag = label(r"the later Mohist canons \ (c. 300 BCE)", font_size=18, color=HIST).next_to(g, UP, buff=0.15).align_to(
            g, LEFT)
        q = quote_card(r"Proper names are not connotative: \ they denote the individuals who are called by them; "
                       r"\ but they do not indicate or imply any attributes as belonging to those individuals.",
                       r"John Stuart Mill", r"\textit{A System of Logic} \ (1843)", width=10.6, font_size=22).move_to(
            [0, -1.6, 0])
        foot = label(r"the Millian view: \ a name's whole contribution is its bearer", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The later Mohist canons sort names into three kinds. <bookmark mark='a'/>Unrestricted names, like "
            "thing, which apply to everything. <bookmark mark='b'/>Classifying names, like horse, which apply to "
            "everything of a kind. <bookmark mark='c'/>And private names, like Zang, the name of one person: what we "
            "call proper names. <bookmark mark='d'/>Two thousand years later John Stuart Mill drew the same line. "
            "Proper names, he wrote in 1843, are not connotative: they denote the individuals who are called by "
            "them, but they do not imply any attributes. <bookmark mark='e'/>On this Millian view, a name's whole "
            "contribution to what we say is its bearer. Frege's puzzle is the first serious trouble for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
