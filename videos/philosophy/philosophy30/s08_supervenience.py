from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


def world(w, centre, title):
    box = RoundedRectangle(width=2.4, height=1.6, corner_radius=0.15, color=GREY_B).move_to(centre)
    g = VGroup(box, label(title, font_size=15, color=GREY_A).next_to(box, UP, buff=0.08))
    for i, (name, (p, m)) in enumerate(sorted(w.items())):
        x = centre[0] - 0.55 + 1.1 * i
        g.add(VGroup(Dot([x, centre[1] + 0.25, 0], radius=0.09, color=WHITE),
                     MathTex(name, font_size=20).move_to([x, centre[1] + 0.55, 0]),
                     MathTex(p.replace("P", r"P_").replace("_1", "_1").replace("_2", "_2"), font_size=20,
                             color=PHYS).move_to([x, centre[1] - 0.1, 0]),
                     MathTex(m.replace("M", r"M_"), font_size=20, color=MIND).move_to([x, centre[1] - 0.45, 0])))
    return g


class Supervenience(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Supervenience", r"What does it take for the mental to depend on the physical?",
                            lit=(1970, 1984), part=PART)
        with self.voiceover("Chapter seven. Supervenience."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.definitions()
        self.checked()
        self.uses()

    def idea(self):
        head = label(r"No mental difference without a physical difference", font_size=30, color=CONN).to_edge(UP,
                                                                                                             buff=0.35)
        rows = stack([(r"Davidson \ (1970): \ mental events are physical, \ yet there are no strict laws linking mental "
                       r"and physical kinds", HIST),
                      (r"anomalous monism needed a weaker tie than identity of kinds", GREY_A),
                      (r"supervenience: \ things alike in every physical respect cannot differ mentally", MIND),
                      (r"like a picture's beauty and its pixels: \ no change in beauty without a change in pixels",
                       GOAL)], font_size=22, aligned_edge=LEFT, width=12.0, buff=0.35).move_to([0, -0.2, 0])
        with self.voiceover(
            "If pain is not identical with any one physical kind, how is the mental tied to the physical at all? "
            "<bookmark mark='a'/>Donald Davidson held in 1970 that every mental event is a physical event, but that "
            "there are no strict laws linking mental kinds with physical kinds: anomalous monism. "
            "<bookmark mark='b'/>That needed a tie weaker than identity. <bookmark mark='c'/>The tie is supervenience: "
            "things alike in every physical respect cannot differ in any mental respect. <bookmark mark='d'/>As a "
            "picture's beauty supervenes on its pixels: no change in the beauty without some change in the pixels, "
            "though beauty is no particular pattern of them. Jaegwon Kim showed in 1984 that the slogan hides at "
            "least three different relations."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def definitions(self):
        head = label(r"Three supervenience relations \ (Kim, \ 1984)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = VGroup(
            VGroup(label(r"weak", font_size=24, color=PHYS),
                   MathTex(r"\Box\,\forall x \forall y\, \big(x \approx_P y \;\rightarrow\; x \approx_M y\big)",
                           font_size=30), label(r"within each world, \ physical twins are mental twins", font_size=18,
                                                color=GREY_A)),
            VGroup(label(r"strong", font_size=24, color=FUNC),
                   MathTex(r"\forall w, w' \;\forall x \in w,\; y \in w'\, \big(x \approx_P y \;\rightarrow\; x \approx_M "
                           r"y\big)", font_size=30), label(r"across worlds too", font_size=18, color=GREY_A)),
            VGroup(label(r"global", font_size=24, color=MIND),
                   MathTex(r"\forall w, w'\, \big(w \approx_P w' \;\rightarrow\; w \approx_M w'\big)", font_size=30),
                   label(r"worlds with the same physical distribution have the same mental one", font_size=18,
                         color=GREY_A)))
        for d in defs:
            d[1].next_to(d[0], RIGHT, buff=0.5)
            d[2].next_to(d[1], DOWN, buff=0.12).align_to(d[1], LEFT)
        defs.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, -0.2, 0])
        with self.voiceover(
            "Write x is physically like y, and x is mentally like y. <bookmark mark='a'/>Weak supervenience: within "
            "each possible world, any two things that are physical twins are mental twins. "
            "<bookmark mark='b'/>Strong supervenience: the same holds across worlds; a physical twin of yours in any "
            "possible world is your mental twin. <bookmark mark='c'/>Global supervenience compares whole worlds: any "
            "two worlds with the same physical distribution have the same mental distribution."
        ) as vo:
            self.play(FadeIn(head))
            for mk, d in zip("abc", defs):
                vo.wait_until(mk)
                self.play(FadeIn(d[0]), Write(d[1]), FadeIn(d[2]))
        self.clear_scene()

    def checked(self):
        d = load("supervenience")
        head = label(r"Checked on three sets of worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["A"]["weak"], d["A"]["strong"], d["A"]["global"]) == (True, False, False)
        assert (d["B"]["weak"], d["B"]["strong"], d["B"]["global"]) == (False, False, True)
        assert all(d["C"][k] for k in ("weak", "strong", "global"))
        sets = VGroup()
        for i, k in enumerate("ABC"):
            ws = d[k]["worlds"]
            y = 1.5 - 1.95 * i
            g = VGroup(label(rf"set {k}", font_size=22, color=CONN).move_to([-6.0, y, 0]),
                       world(ws[0], [-3.8, y, 0], r"world 1"), world(ws[1], [-0.9, y, 0], r"world 2"))
            marks = VGroup(*[VGroup(label(n, font_size=17, color=GREY_A), mark(d[k][n], 26)).arrange(RIGHT, buff=0.15)
                             for n in ("weak", "strong", "global")]).arrange(RIGHT, buff=0.45).move_to([3.9, y, 0])
            sets.add(VGroup(g, marks))
        foot = label(r"strong implies weak and global; \ neither weak nor global implies the other", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner checks all three on small sets of worlds, each with two individuals, a and b. "
            "<bookmark mark='a'/>In set A, a and b are physical and mental twins within each world, so weak "
            "supervenience holds. But a has the same physical state in both worlds and a different mental state, so "
            "strong supervenience fails, and so does global: the two worlds are physically identical and mentally "
            "different. <bookmark mark='b'/>In set B, a and b are physical twins in world one with different mental "
            "states, so weak supervenience fails. Yet global supervenience holds, because no two worlds share their "
            "physical distribution. <bookmark mark='c'/>In set C, one function from physical to mental states holds "
            "everywhere, and all three hold. <bookmark mark='d'/>Strong supervenience implies the other two; weak and "
            "global are independent of each other. Which one physicalism needs is itself a question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", sets):
                vo.wait_until(mk)
                self.play(FadeIn(s[0]))
                self.play(FadeIn(s[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def uses(self):
        head = label(r"What supervenience does, \ and does not do", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"minimal physicalism", r"Jackson \ (1998): \ any minimal physical duplicate of our world is a duplicate "
                                     r"simpliciter", PHYS),
            (r"not explanation", r"it states a covariation; \ it does not say \textit{why} the mental depends on the "
                                 r"physical \ (Horgan, \ 1993)", BAD),
            (r"not enough", r"a dualist's God could guarantee it by fiat: \ supervenience is compatible with "
                            r"emergence", MIND),
            (r"next", r"if the mental merely supervenes, \ can it cause anything?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "What is supervenience good for? <bookmark mark='a'/>Frank Jackson used global supervenience to state "
            "minimal physicalism: any world that is a minimal physical duplicate of ours is a duplicate of it in "
            "every respect. <bookmark mark='b'/>But supervenience only states a pattern of covariation. It does not "
            "explain why the mental depends on the physical, as Terence Horgan stressed. "
            "<bookmark mark='c'/>And it is weaker than it looks: a dualist's God could guarantee it by decree, so it "
            "is compatible with genuinely emergent minds. <bookmark mark='d'/>The pressing question comes next. If "
            "the mental merely supervenes on the physical, can it cause anything?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
