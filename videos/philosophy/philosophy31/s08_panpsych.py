from __future__ import annotations

from explainer.zh_text import verbatim
from videos.philosophy.philosophy31.common import *  # noqa: F403


class Panpsychism(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Mind in matter", r"What is matter, \ in itself?", lit=(1927,), part=PART)
        with self.voiceover("Chapter seven. Mind in matter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.structure()
        self.views()
        self.combination()

    def structure(self):
        hc = history_card(1927, r"Bertrand Russell", r"\textit{The Analysis of Matter}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        # a node with arrows: physics says what it does, not what it is
        core = VGroup(Circle(radius=0.55, color=SIG, fill_opacity=0.15),
                      label(r"?", font_size=40, color=SIG)).move_to([-3.0, -0.4, 0])
        dirs = [UP, DOWN, LEFT, RIGHT, UL, DR]
        arrows = VGroup(*[Arrow(core.get_center() + d * 0.6, core.get_center() + d * 1.7, buff=0, color=PHYS,
                                stroke_width=3) for d in dirs])
        al = label(r"mass, \ charge, \ spin: \ what it does to other things", font_size=18,
                   color=PHYS).next_to(arrows, DOWN, buff=0.2)
        rows = stack([(r"physics describes structure and dynamics: \ dispositions, \ relations", PHYS),
                      (r"it is silent on what has the dispositions: \ the intrinsic nature", SIG),
                      (r"the one intrinsic nature we know from inside: \ our own experience", FEEL),
                      (r"Russell; \ Eddington \ (1928): \ perhaps they are the same kind of thing", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.4, buff=0.3).move_to([3.2, -0.2, 0])
        with self.voiceover(
            "Type F, the last row of Chalmers's map, goes back to Bertrand Russell's book of 1927. "
            "<bookmark mark='a'/>Physics tells us what matter does: mass is resistance to acceleration and the "
            "source of gravity; charge is how a particle pushes and pulls on others. Every property is defined by "
            "its relations. <bookmark mark='b'/>Physics is silent about what it is that has these dispositions, "
            "the intrinsic nature that plays the roles. <bookmark mark='c'/>And there is one intrinsic nature we "
            "know from the inside: our own experience. <bookmark mark='d'/>Russell, and Arthur Eddington a year "
            "later, suggested that these might be the same kind of thing: that experience, or something like it, "
            "is what the equations of physics are equations of."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(core))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(al), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(core, color=SIG))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), core[0].animate.set_fill(FEEL, opacity=0.4))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def views(self):
        head = label(r"Russellian monism, \ and its varieties", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the appeal", r"experience gets a causal role: \ it is what physical causes are, \ so no "
                                r"exclusion problem \ (Part 30)", OK),
                (r"panpsychism", r"the intrinsic natures are experiential, \ all the way down \ (Strawson, \ 2006; "
                                 r"\ Goff, \ 2017)", FEEL),
                (r"panprotopsychism", r"they are not experiential, \ but combine to make experience", SIG),
                (r"cosmopsychism", r"the universe as a whole is the one fundamental subject; \ we are its parts",
                 SELF)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "The view is called Russellian monism, and it has varieties. <bookmark mark='a'/>Its appeal is that it "
            "gives experience something to do. If experience is the intrinsic nature of the physical causes, the "
            "exclusion problem of Part 30 never arises: mental causes are physical causes, seen from within. "
            "<bookmark mark='b'/>Panpsychism says the intrinsic natures are themselves experiential, all the way "
            "down: Galen Strawson in 2006, Philip Goff in 2017. <bookmark mark='c'/>Panprotopsychism says they are "
            "not experiential, but something that combines to make experience. <bookmark mark='d'/>And "
            "cosmopsychism starts at the other end: the universe as a whole is the one fundamental subject, and "
            "we are its parts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def combination(self):
        q = quote_card(r"Take a sentence of a dozen words, \ and take twelve men and tell to each one word. \dots\ "
                       r"nowhere will there be a consciousness of the whole sentence.", r"William James",
                       r"\textit{The Principles of Psychology} \ (1890)", width=10.0, font_size=26).to_edge(UP,
                                                                                                         buff=0.5)
        words = [r"the", r"cat", r"sat", r"on", r"the", r"mat"]
        men = VGroup()
        for k, w in enumerate(words):
            x = -4.0 + 1.6 * k
            with verbatim():  # one word each, of an English sentence: it stays as it is in every edition
                wl = label(w, font_size=18, color=SIG).move_to([0, 0.45, 0])
            men.add(VGroup(Circle(radius=0.22, color=SELF), Line([0, -0.22, 0], [0, -0.8, 0], color=SELF),
                           wl).move_to([x, -0.9, 0]))
        rows = stack([(r"the combination problem: \ how do many small subjects make one big one?", BAD),
                      (r"for panpsychism what the hard problem is for physicalism: \ an entailment that seems to "
                       r"fail", GOAL)], font_size=20, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Its great difficulty was stated before the theory existed. <bookmark mark='a'/>William James, in 1890: "
            "take a sentence of a dozen words, and take twelve men and tell to each one word; nowhere will there be "
            "a consciousness of the whole sentence. <bookmark mark='b'/>Each man knows his word. No one knows the "
            "sentence. <bookmark mark='c'/>That is the combination problem: how could the tiny experiences of "
            "particles add up to the single, unified experience of a person? <bookmark mark='d'/>It is to "
            "panpsychism what the hard problem is to physicalism: an entailment, from parts to a whole, that seems "
            "to fail. The view trades one gap for another, and its defenders argue the new one is smaller."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in men], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()
