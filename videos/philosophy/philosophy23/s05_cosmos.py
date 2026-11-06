from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Cosmos(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"First causes and contingency", r"Why is there a world at all?", lit=(1270, 1714),
                            part=PART)
        with self.voiceover("Chapter four. First causes and contingency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ways()
        self.third()
        self.series()
        self.leibniz()

    def ways(self):
        hc = history_card(1270, r"Thomas Aquinas", r"\textit{Summa Theologiae} I, \ q. 2, \ a. 3", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"1. \ motion", r"whatever is moved is moved by another: \ a first unmoved mover", ARG),
            (r"2. \ causes", r"no infinite chain of efficient causes: \ a first cause", ARG),
            (r"3. \ contingency", r"not everything can be contingent: \ a necessary being", ABS),
            (r"4. \ gradation", r"more and less good point to a maximum", GREY_A),
            (r"5. \ governance", r"things without minds act for ends: \ an intelligence directs them", NAT),
        ]
        g = rows_table(rows, top=1.3, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=22)
        note = label(r"`and this everyone understands to be God'", font_size=22, color=DIV).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Thomas Aquinas, in the Summa Theologiae, offered five ways. <bookmark mark='a'/>From motion: whatever is "
            "moved is moved by another, so there is a first, unmoved mover. <bookmark mark='b'/>From efficient "
            "causes: there cannot be an infinite chain of them, so there is a first cause. <bookmark mark='c'/>From "
            "contingency: not everything can be merely possible, so there is a necessary being. "
            "<bookmark mark='d'/>From gradation: more and less good point to a maximum. <bookmark mark='e'/>From "
            "governance: things without minds act for ends, so an intelligence directs them. <bookmark mark='f'/>"
            "Each way ends with the same line: and this everyone understands to be God. The first three are "
            "cosmological, and the third is the most interesting logically."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(note))
        self.clear_scene()

    def third(self):
        d = load("third")
        head = label(r"The third way, \ and a relay", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n, T = d["things"], d["times"]
        ax0 = np.array([-5.4, -0.6, 0])
        dx, dy = 0.72, 0.36
        bars = VGroup()
        for k, life in d["lives"].items():
            k = int(k)
            a, b = life[0], life[-1] + 1
            bars.add(Rectangle(width=(b - a) * dx, height=dy * 0.75, color=NAT, fill_opacity=0.5,
                               stroke_width=1.5).move_to(ax0 + np.array([(a + b) / 2 * dx, (n - 1 - k) * dy + 0.4,
                                                                         0])))
        axis = Arrow(ax0 + LEFT * 0.1, ax0 + np.array([T * dx + 0.3, 0, 0]), buff=0, color=GREY_B, stroke_width=2)
        al = label(r"time", font_size=18, color=GREY_A).next_to(axis, RIGHT, buff=0.1)
        tl = label(r"each bar: \ one contingent thing's lifetime", font_size=17, color=NAT).next_to(bars, UP, buff=0.15)
        f1 = MathTex(r"\forall x\, \exists t\, \lnot E(x, t)", font_size=34, color=WHITE)
        f2 = MathTex(r"\exists t\, \forall x\, \lnot E(x, t)", font_size=34, color=WHITE)
        v1 = tf(d["each_absent_sometime"], 26)
        v2 = tf(d["some_time_empty"], 26)
        g1 = VGroup(f1, v1).arrange(RIGHT, buff=0.3)
        g2 = VGroup(f2, v2).arrange(RIGHT, buff=0.3)
        side = VGroup(label(r"each thing is absent at some time", font_size=18, color=GREY_A), g1,
                      label(r"so at some time nothing exists?", font_size=18, color=GREY_A), g2).arrange(
            DOWN, buff=0.18).move_to([4.2, 0.9, 0])
        rows = stack([(r"the inference swaps the quantifiers: \ invalid, \ and this relay is a countermodel", BAD),
                      (r"Aquinas also needs: \ with infinite time, \ every possibility is realized", GREY_A),
                      (r"repaired, \ the argument becomes Leibniz's: \ why the whole relay?", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The third way argues like this. <bookmark mark='a'/>Each contingent thing, at some time, does not exist. "
            "<bookmark mark='b'/>So, if everything were contingent, at some time nothing would have existed; and "
            "since nothing comes from nothing, nothing would exist now. <bookmark mark='c'/>The Reasoner builds a "
            "relay: eight things, each existing for three moments, their lives overlapping like runners passing a "
            "baton. Every one of them fails to exist at some time; true. But there is no time at which nothing "
            "exists; false. <bookmark mark='d'/>The step from each thing being absent at some time to some time at "
            "which everything is absent swaps the order of the quantifiers, and it is invalid. Aquinas also leaned on "
            "the principle that in infinite time every possibility is realized. <bookmark mark='e'/>Repaired, the "
            "argument becomes Leibniz's: grant the relay; why is there a relay at all?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(g1[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(g2[0]))
            vo.wait_until("c")
            self.play(GrowArrow(axis), FadeIn(al), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.2),
                      FadeIn(tl), run_time=3)
            self.play(FadeIn(v1))
            self.play(FadeIn(v2))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def series(self):
        head = label(r"Two kinds of causal series", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hand = VGroup(label(r"hand", font_size=20, color=HUM), Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=GREY_B),
                      label(r"stick", font_size=20, color=WARM), Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=GREY_B),
                      label(r"stone", font_size=20, color=NAT)).arrange(RIGHT, buff=0.15).move_to([-3.4, 1.2, 0])
        hl = label(r"ordered \textit{per se}: \ each moves only while moved, \ now", font_size=19,
                   color=ABS).next_to(hand, DOWN, buff=0.25)
        gens = VGroup(*[label(t, font_size=20, color=c) for t, c in ((r"grandparent", GREY_A), (r"parent", HUM),
                                                                     (r"child", HUM))])
        arr = VGroup()
        for i in range(2):
            gens[i + 1].next_to(gens[i], RIGHT, buff=0.9)
        for i in range(2):
            arr.add(Arrow(gens[i].get_right(), gens[i + 1].get_left(), buff=0.1, color=GREY_B))
        fam = VGroup(gens, arr).move_to([3.4, 1.2, 0])
        fl = label(r"ordered \textit{per accidens}: \ the earlier may be gone", font_size=19, color=GREY_A).next_to(
            fam, DOWN, buff=0.25)
        rows = stack([(r"Aquinas allows an infinite series \textit{per accidens}: \ a beginningless world is not "
                       r"impossible", WHITE),
                      (r"but a series \textit{per se} needs a first member: \ intermediaries have only borrowed "
                       r"power", DIV),
                      (r"so the first cause is a sustaining cause, \ not a first event in time", GOAL),
                      (r"the objection: \ why could there not be an infinite chain of borrowers?", BAD)],
                     font_size=21, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Aquinas's first and second ways rest on a distinction often missed. <bookmark mark='a'/>A hand moves a "
            "stick, which moves a stone. The stick moves the stone only while the hand moves the stick: the series is "
            "ordered per se, all at once. <bookmark mark='b'/>A grandparent begets a parent, who begets a child; the "
            "grandparent may be long gone. That series is ordered per accidens. <bookmark mark='c'/>Aquinas thought "
            "reason could not rule out an infinite series of the second kind; a world without a beginning was, he "
            "said, not impossible. <bookmark mark='d'/>But a series of the first kind needs a first member, because "
            "the intermediaries have only borrowed power. <bookmark mark='e'/>So his first cause is a sustaining "
            "cause, holding things in being now, not a first event long ago. <bookmark mark='f'/>Critics ask why "
            "there could not be an infinite chain of borrowers, each sustained by the next."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hand), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(fam), FadeIn(fl))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def leibniz(self):
        hc = history_card(1714, r"G. W. Leibniz", r"\textit{Monadology}, \ \S\S 32--38", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ every fact has a sufficient reason why it is so and not otherwise", ABS),
                       (r"2. \ the world, \ the whole series of contingent things, \ is a fact", WHITE),
                       (r"3. \ its reason cannot lie inside the series: \ each member is contingent too", WHITE),
                       (r"4. \ so it lies in a necessary being, \ which carries the reason for its existence in itself",
                        DIV)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.3).move_to([0, 0.4, 0])
        rows = stack([(r"Hume \ (\textit{Dialogues}, \ IX): \ explain each member, \ and you have explained the "
                       r"whole", NAT),
                      (r"Edwards: \ five Inuit in New York, \ each with a reason for being there: \ no further reason "
                       r"for the group", GREY_A),
                      (r"everything rests on premise 1, \ the principle of sufficient reason: \ the next chapter",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Leibniz's argument from contingency is the strongest of the cosmological family. <bookmark mark='a'/>"
            "Every fact has a sufficient reason why it is so and not otherwise. <bookmark mark='b'/>The world, the "
            "whole series of contingent things, is a fact. <bookmark mark='c'/>Its reason cannot lie inside the "
            "series, since each member is contingent and needs a reason itself. <bookmark mark='d'/>So it lies "
            "outside, in a necessary being, which carries the reason for its existence within itself. "
            "<bookmark mark='e'/>In Hume's Dialogues, Cleanthes objected that if you have explained each member of a "
            "series, you have explained the whole. <bookmark mark='f'/>Paul Edwards's example: five Inuit standing on "
            "a corner in New York. Explain why each is there, and nothing remains to explain about the group. "
            "<bookmark mark='g'/>Everything rests on the first premise, the principle of sufficient reason."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, r in zip("efg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
