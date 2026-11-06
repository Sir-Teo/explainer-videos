from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Fate(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Fate", r"If the future is already true, \ is anything up to us?", lit=(),
                            part=PART)
        with self.voiceover("Chapter two. Fate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.seabattle()
        self.cylinder()
        self.lazy()

    def seabattle(self):
        hc = history_card(r"c.\ 350\ BCE", r"Aristotle", r"\textit{On Interpretation}, \ chapter 9", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the worry", r"if `there will be a sea battle tomorrow' is already true, \ the battle cannot fail to "
                               r"happen", LAW),
                (r"logical fatalism", r"so whatever will happen, \ happens necessarily, \ and deliberating is idle",
                 BAD),
                (r"Aristotle", r"perhaps such statements are not yet true or false: \ Part 5's third value", CHANCE),
                (r"the other reply", r"`it is true that $p$' does not imply `necessarily $p$': \ a scope confusion",
                 GOAL)]
        g = rows_table(rows, top=1.2, gap=0.5)
        with self.voiceover(
            "The oldest version of the worry is about truth, not causes. <bookmark mark='a'/>If it is already true "
            "today that there will be a sea battle tomorrow, the battle cannot fail to happen. "
            "<bookmark mark='b'/>Generalized, that is logical fatalism: whatever will happen happens necessarily, "
            "and deliberation is idle. <bookmark mark='c'/>Aristotle seems to have answered that statements about "
            "contingent futures are not yet true or false, the third value of Part 5. <bookmark mark='d'/>Most "
            "logicians now answer differently: from it is true that p, it does not follow that p is necessary. The "
            "argument confuses the necessity of a conditional with the necessity of its consequent."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cylinder(self):
        hc = history_card(r"c.\ 230\ BCE", r"Chrysippus of Soli", r"reported by Cicero, \ \textit{On Fate}, \ "
                                                                 r"\S\S 42--43", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        slope = Line([-6.0, 0.6, 0], [0.0, -2.0, 0], color=GREY_B)
        r = 0.4
        n = (np.array([2.6, 6.0, 0]) / np.linalg.norm([2.6, 6.0, 0]))
        start = np.array([-5.6, 0.6 - 0.4 * 2.6 / 6.0, 0]) + n * r
        cyl = VGroup(Circle(radius=r, color=WILL, fill_opacity=0.2), Line(ORIGIN, UP * r, color=WILL)).move_to(start)
        hand = Arrow(start + LEFT * 1.4 + UP * 0.6, start + LEFT * 0.45 + UP * 0.2, buff=0, color=LAW)
        hl = label(r"the push", font_size=18, color=LAW).next_to(hand, UP, buff=0.1)
        rows = stack([(r"the push is an antecedent cause: \ it starts the motion", LAW),
                      (r"the rolling is from the cylinder's own shape: \ the principal cause", WILL),
                      (r"so with assent: \ an impression strikes us, \ but how we respond comes from our character",
                       SELF),
                      (r"a compatibilism, \ two thousand years early", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=6.2, buff=0.3).move_to([3.4, 0.4, 0])
        end = np.array([-0.9, 0.6 - 2.6 / 6.0 * 5.1, 0]) + n * r
        turns = -np.linalg.norm(end - start) / r
        with self.voiceover(
            "The Stoics believed in fate, a single chain of causes running through everything, and also in "
            "responsibility. <bookmark mark='a'/>Chrysippus explained how with a cylinder, in Cicero's report. "
            "Push a cylinder at the top of a slope, and it rolls. <bookmark mark='b'/>The push is only the starting "
            "cause. That the cylinder rolls, rather than sliding or spinning, comes from its own shape: the "
            "principal cause. <bookmark mark='c'/>So with us. An impression strikes the mind from outside, but "
            "whether and how we assent to it comes from our own character. <bookmark mark='d'/>The act is fated, "
            "and it is still ours: a compatibilism, two thousand years before the word."
        ) as vo:
            self.play(FadeIn(hc), Create(slope), FadeIn(cyl))
            vo.wait_until("a")
            self.play(GrowArrow(hand), FadeIn(hl))
            cyl0 = cyl.copy()
            self.play(UpdateFromAlphaFunc(cyl, lambda m, t: m.become(
                cyl0.copy().rotate(turns * t).move_to(start + (end - start) * t))), run_time=2.5,
                rate_func=rate_functions.ease_in_quad)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lazy(self):
        head = label(r"The lazy argument, \ and co-fated events", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"1.", r"if it is fated that you recover, \ you will recover, \ whether or not you call the doctor",
                 LAW),
                (r"2.", r"if it is fated that you do not, \ you will not, \ whether or not you call", LAW),
                (r"so", r"calling the doctor is pointless", BAD),
                (r"Chrysippus", r"recovering and calling the doctor are co-fated: \ one is fated by way of the other",
                 WILL),
                (r"the moral", r"determinism does not make deliberation idle: \ our choices are among the causes",
                 GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "The Stoics' opponents pressed them with the lazy argument. <bookmark mark='a'/>If it is fated that you "
            "will recover from this illness, you will recover whether or not you call the doctor. "
            "<bookmark mark='b'/>If it is fated that you will not, you will not, whether or not you call. "
            "<bookmark mark='c'/>So calling the doctor is pointless. <bookmark mark='d'/>Chrysippus replied that "
            "some events are co-fated: if your recovery is fated, it is fated to come about by way of your calling "
            "the doctor. <bookmark mark='e'/>That is still the standard answer to fatalism: even if everything is "
            "determined, our deliberations and choices are among the causes, not spectators of them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
