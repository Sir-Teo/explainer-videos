from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Frankfurt(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Frankfurt cases", r"Does responsibility need the ability to do otherwise?",
                            lit=(1969,), part=PART)
        with self.voiceover("Chapter five. Frankfurt cases."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.case()
        self.model()
        self.replies()

    def case(self):
        hc = history_card(1969, r"Harry Frankfurt", r"`Alternate Possibilities and Moral Responsibility'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        pap = label(r"the principle of alternative possibilities: \ a person is morally responsible for what he has "
                    r"done only if he could have done otherwise", font_size=20, color=LAW).move_to([0, 1.8, 0])
        jones = VGroup(Circle(radius=0.35, color=WILL), label(r"Jones", font_size=18, color=WILL)).move_to(
            [-3.0, -0.2, 0])
        black = VGroup(Circle(radius=0.35, color=BLAME, stroke_opacity=0.5), label(r"Black", font_size=18,
                                                                                  color=BLAME)).move_to([-0.6, 0.8, 0])
        smith = VGroup(Circle(radius=0.35, color=GREY_B), label(r"Smith", font_size=18, color=GREY_B)).move_to(
            [2.4, -0.2, 0])
        shot = Arrow(jones.get_right(), smith.get_left(), buff=0.1, color=WILL)
        watch = DashedLine(black.get_bottom(), jones.get_top(), color=BLAME, dash_length=0.1)
        rows = stack([(r"Jones decides to shoot Smith, \ for his own reasons", WILL),
                      (r"Black, \ unseen, \ would have made him shoot at the first sign he might not", BLAME),
                      (r"Black never acts: \ Jones could not have done otherwise, \ and is responsible", GOAL)],
                     font_size=20, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1969 Harry Frankfurt attacked a principle almost everyone had assumed. <bookmark mark='a'/>The "
            "principle of alternative possibilities: a person is morally responsible for what he has done only if "
            "he could have done otherwise. <bookmark mark='b'/>Jones decides, for reasons of his own, to shoot "
            "Smith, and does. <bookmark mark='c'/>Unknown to Jones, Black wanted Smith shot too, and had arranged to "
            "intervene, with a device in Jones's brain, at the first sign that Jones was about to decide otherwise, "
            "and make him shoot anyway. <bookmark mark='d'/>Black never had to act. Jones could not have done "
            "otherwise, yet he seems fully responsible, because Black's device played no part in what he did."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(pap))
            vo.wait_until("b")
            self.play(FadeIn(jones), FadeIn(smith), GrowArrow(shot), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(black), Create(watch), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def model(self):
        d = load("frankfurt")
        head = label(r"The case, \ on the model of chapter 4", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["N_shoots"] and not d["N_on_his_own"] and not d["can_avoid_shooting"] and d["can_avoid_own"]
        w1 = VGroup(RoundedRectangle(width=3.8, height=1.0, corner_radius=0.2, color=WILL, fill_opacity=0.1),
                    label(r"shoots on his own", font_size=19, color=WILL)).move_to([-3.4, 0.9, 0])
        w2 = VGroup(RoundedRectangle(width=3.8, height=1.0, corner_radius=0.2, color=BLAME, fill_opacity=0.1),
                    wrapped_label(r"shows the sign; \ Black makes him shoot", 3.4, 19, BLAME)).move_to([-3.4, -0.7, 0])
        a1 = label(r"decide to shoot", font_size=17, color=GREY_A).next_to(w1, LEFT, buff=0.2)
        a2 = label(r"begin to decide otherwise", font_size=17, color=GREY_A).next_to(w2, LEFT, buff=0.2)
        for a in (a1, a2):
            if a.get_left()[0] < -7.0:
                a.shift(RIGHT * (-7.0 - a.get_left()[0]))
        res = stack([(r"`Jones shoots': \ true in both worlds: \ $N$ \ $\checkmark$", OK),
                     (r"no choice about whether he shoots", GREY_A),
                     (r"`Jones shoots on his own': \ he can make it false: \ $N$ \ $\times$", BAD),
                     (r"a choice about whether he shoots \textit{on his own}: \ a flicker of freedom", GOAL)],
                    font_size=19, aligned_edge=LEFT, width=6.2, buff=0.28).move_to([3.4, 0.1, 0])
        with self.voiceover(
            "The Reasoner puts the case on the model of chapter four. <bookmark mark='a'/>Jones has two options. If "
            "he decides to shoot, he shoots on his own. If he begins to decide otherwise, he shows the sign, and "
            "Black makes him shoot. <bookmark mark='b'/>Jones shoots is true in both worlds, so N holds: Jones has "
            "no choice about whether he shoots. <bookmark mark='c'/>But Jones shoots on his own is true in only "
            "one, and he could make it false by beginning to decide otherwise. <bookmark mark='d'/>So he does have "
            "a choice: not about what happens, but about whether it happens through him. John Martin Fischer calls "
            "this a flicker of freedom, and asks whether so thin an alternative could be what responsibility rests "
            "on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(a1), FadeIn(a2))
            vo.wait_until("b")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]), Indicate(w1, color=WILL))
            vo.wait_until("d")
            self.play(FadeIn(res[3]))
        self.clear_scene()

    def replies(self):
        head = label(r"Replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"flickers", r"the sign itself is an alternative: \ too thin to ground responsibility? \ "
                              r"(Fischer, \ 1994)", SELF),
                (r"the dilemma", r"Widerker \ (1995): \ if the sign determines the decision, \ the case assumes "
                                 r"determinism; \ if not, \ Black cannot be sure", BAD),
                (r"buffered cases", r"Hunt, \ Pereboom: \ block every route to the other decision in advance", WILL),
                (r"the upshot", r"if Frankfurt is right, \ responsibility is about the actual sequence, \ not about "
                                r"alternatives", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "The cases have been argued over ever since. <bookmark mark='a'/>Fischer himself thinks the flickers "
            "are too thin to carry responsibility, and so concludes that Frankfurt is right. "
            "<bookmark mark='b'/>David Widerker posed a dilemma for the libertarian reading. Either the sign Black "
            "watches for determines Jones's decision, in which case the case assumes determinism, which begs the "
            "question; or it does not, in which case Black cannot be sure to intervene in time. "
            "<bookmark mark='c'/>David Hunt and Derk Pereboom built buffered cases that block every route to the "
            "other decision in advance. <bookmark mark='d'/>If Frankfurt is right, responsibility is a matter of the "
            "actual sequence that produced the act, not of alternatives, and the consequence argument, even if it "
            "is sound, does not show that we are never responsible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
