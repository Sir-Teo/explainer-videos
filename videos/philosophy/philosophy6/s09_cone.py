from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403

APEX = np.array([-2.6, -3.3, 0])
TOPY = 3.0
HALFW = 3.6


def cone_x(y):
    return HALFW * (y - APEX[1]) / (TOPY - APEX[1])


def cone(color=SETC, halfw=HALFW, apex=APEX, opacity=0.08):
    l = Line(apex, apex + np.array([-halfw, TOPY - apex[1], 0]), color=color, stroke_width=3)
    r = Line(apex, apex + np.array([halfw, TOPY - apex[1], 0]), color=color, stroke_width=3)
    fill = Polygon(apex, apex + np.array([-halfw, TOPY - apex[1], 0]), apex + np.array([halfw, TOPY - apex[1], 0]),
                   stroke_width=0, fill_color=color, fill_opacity=opacity)
    return VGroup(fill, l, r)


def stage(y, name, color=GREY_A, font_size=24):
    w = cone_x(y)
    ln = Line(APEX + np.array([-w, y - APEX[1], 0]), APEX + np.array([w, y - APEX[1], 0]), color=GREY_C,
              stroke_width=1.5)
    t = MathTex(name, font_size=font_size, color=color).next_to(ln, RIGHT, buff=0.2)
    return VGroup(ln, t)


class Cone(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The cumulative hierarchy", r"What is a set, if not the extension of a condition?",
                            lit=(1930,), part=PART)
        with self.voiceover("Chapter eight. The cumulative hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.build()
        self.iterative()
        self.classes()

    def build(self):
        c = cone()
        ys = [-3.0, -2.6, -2.15, -1.6, -0.95]
        names = [r"V_0 = \varnothing", r"V_1", r"V_2", r"V_3", r"V_4"]
        st = VGroup(*[stage(y, n) for y, n in zip(ys, names)])
        dots = MathTex(r"\vdots", font_size=30, color=GREY_B).move_to(APEX + np.array([0, -0.2 - APEX[1], 0]))
        w = stage(0.6, r"V_\omega \ = \bigcup_n V_n \quad \text{(countable)}", GOAL)
        w1 = stage(1.4, r"V_{\omega+1} = \mathcal{P}(V_\omega) \quad \text{(the size of } \mathbb{R})", GOAL)
        w2 = stage(2.3, r"V_{\omega+\omega},\ \dots,\ V_\alpha,\ \dots", ORD)
        spine = Arrow(APEX, APEX + np.array([0, TOPY - APEX[1] + 0.2, 0]), buff=0, color=ORD, stroke_width=3)
        sl = label(r"the ordinals, \ up the middle", font_size=22, color=ORD).next_to(spine.get_end(), LEFT, buff=0.15)
        rule = VGroup(MathTex(r"V_{\alpha+1} = \mathcal{P}(V_\alpha)", font_size=34, color=GOAL),
                      MathTex(r"V_\lambda = \bigcup_{\alpha<\lambda} V_\alpha \ \ (\lambda \text{ a limit})",
                              font_size=30)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(UR, buff=0.5)
        with self.voiceover(
            "Now let the stages run on past the finite. <bookmark mark='a'/>Picture the universe of sets as a cone. "
            "At the bottom, stage zero, is the empty set. Each stage adds every subset of the stage below. "
            "<bookmark mark='b'/>After all the finite stages comes stage omega, their union: the hereditarily "
            "finite sets, countably many. <bookmark mark='c'/>The next stage takes every subset of that, and already "
            "has as many members as there are real numbers. <bookmark mark='d'/>And on it goes, through every "
            "ordinal, which climb up the middle of the cone like a spine. At a limit stage, take the union of what "
            "came before. This cone, V, is the cumulative hierarchy, and every set of ZFC lives somewhere in it."
        ) as vo:
            self.play(Create(c), FadeIn(st[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in st[1:]], lag_ratio=0.3), FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(w))
            vo.wait_until("c")
            self.play(FadeIn(w1))
            vo.wait_until("d")
            self.play(GrowArrow(spine), FadeIn(sl), FadeIn(w2), FadeIn(rule[1]))
        self.clear_scene()

    def iterative(self):
        hcs = VGroup(history_card(1930, r"Ernst Zermelo", r"`On boundary numbers and domains of sets'", width=5.6,
                                  color=HIST),
                     history_card(1971, r"George Boolos", r"`The iterative conception of set'", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.45)
        rows = VGroup(label(r"a set is formed at a stage, \ from things formed at earlier stages", font_size=26,
                            color=GOAL),
                      label(r"$\Rightarrow$ \ union, power set, separation: \ the results are formed later", font_size=24),
                      label(r"$\Rightarrow$ \ foundation: \ no set contains itself, \ no infinite descent", font_size=24),
                      label(r"$\Rightarrow$ \ Russell's set would have to be formed after every set, \ itself included: "
                            r"\ at no stage", font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.next_to(hcs, DOWN, buff=0.6)
        rows.set_x(0)
        moral = label(r"the axioms are not a patch: \ they describe the cone", font_size=28, color=OK).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Why believe the axioms? <bookmark mark='a'/>Zermelo in 1930, and George Boolos in a classic paper of "
            "1971, gave the answer that most set theorists accept: the iterative conception. A set is formed at a "
            "stage, out of things formed at earlier stages. <bookmark mark='b'/>Then unions, power sets and subsets "
            "of what exists are formed at later stages: those axioms are true. <bookmark mark='c'/>No set can "
            "contain itself, since it would have to exist before it was formed: that is foundation. "
            "<bookmark mark='d'/>And Russell's set, or the set of all sets, would have to be formed after every "
            "set, including itself, which happens at no stage. <bookmark mark='e'/>On this view the axioms are not "
            "an ad hoc patch on a broken theory. They describe the cone."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def classes(self):
        c = cone(opacity=0.05)
        vl = MathTex(r"V", font_size=56, color=SETC).move_to(APEX + np.array([0, 4.6, 0]))
        ex = VGroup(label(r"proper classes: \ too big to be sets", font_size=28, color=GOAL),
                    label(r"$V$, \ all sets", font_size=24),
                    label(r"$\mathrm{Ord}$, \ all ordinals \ (Burali-Forti)", font_size=24),
                    label(r"$\{x : x \notin x\}$ \ \ (which, by foundation, is $V$ itself)", font_size=24),
                    label(r"von Neumann (1925): \ a class is a set \ iff \ it is not as big as $V$", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "What about the collections that are not sets? <bookmark mark='a'/>The universe V itself, the cone as a "
            "whole, is not a member of any stage. Neither is the collection of all ordinals, or Russell's "
            "collection, which by foundation is just V again. <bookmark mark='b'/>These are called proper classes: "
            "collections too large to be sets. <bookmark mark='c'/>Von Neumann proposed a second criterion in 1925, "
            "limitation of size: a collection is a set exactly when it is not as large as the whole universe. The "
            "two conceptions, iterative and size-limited, agree on almost everything."
        ) as vo:
            self.play(Create(c), FadeIn(vl))
            vo.wait_until("a")
            self.play(FadeIn(ex[1:4]))
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            vo.wait_until("c")
            self.play(FadeIn(ex[4]))
        self.clear_scene()
