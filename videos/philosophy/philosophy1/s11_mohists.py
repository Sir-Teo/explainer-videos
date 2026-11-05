from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


def cn_row(zh_text: str, en: str, color=WHITE, ok=None) -> VGroup:
    """A classical Chinese line (shown as itself in both editions) with its English gloss."""
    z = data_text(zh_text, font=cjk_font(), font_size=30, color=color)
    e = label(en, font_size=22, color=GREY_A)
    g = VGroup(z, e).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    if ok is not None:
        m = MathTex(r"\checkmark" if ok else r"\times", font_size=36, color=OK if ok else BAD).next_to(g, RIGHT, buff=0.3)
        g.add(m)
    return g


def cjk_font():
    from explainer.zh_text import cjk_font as f

    return f()


class Mohists(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The Mohists and the School of Names", r"Did ancient China have a logic?",
                            lit=(-400, -300, -280), part=PART)
        with self.voiceover("Chapter ten. The Mohists and the School of Names."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mohists()
        self.parallel()
        self.canon()
        self.white_horse()

    def mohists(self):
        hc = history_card(r"c.\ 470--391 BCE", r"Mozi, and the Later Mohists (c.\ 300 BCE)", r"impartial care; "
                          r"standards (\textit{fa}) for judging; disputation (\textit{bian}) as a discipline",
                          width=6.2, color=HIST).to_corner(UL, buff=0.4)
        bian = definition_card(r"\textit{bian}, disputation", r"contending over a pair of contradictory claims; "
                               r"the one who wins is the one whose claim fits the facts", width=6.4, font_size=24,
                               color=P.TRUE).to_corner(UR, buff=0.4)
        src = cite(r"A.\ C.\ Graham, \textit{Later Mohist Logic, Ethics and Science} (1978), Canon A74")
        tasks = VGroup(label(r"names and objects", font_size=26), label(r"`this' and `not this'", font_size=26),
                       label(r"when does an inference carry over?", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.6, 0])
        with self.voiceover(
            "In China, the Mohists, followers of Mozi in the fifth century before our era, were famous for "
            "arguing for impartial care for everyone, against the Confucians' graded loyalties. <bookmark mark='a'/>"
            "Their later school, around 300 before our era, wrote Canons on disputation, bian: two people contend "
            "over a claim and its contradictory, and the winner is the one whose claim fits the facts. "
            "<bookmark mark='b'/>They studied how names attach to objects, and, most strikingly, when an inference "
            "carries over from one sentence to another."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bian, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tasks], lag_ratio=0.3))
        self.clear_scene()

    def parallel(self):
        r1 = cn_row("白馬，馬也；乘白馬，乘馬也。", r"A white horse is a horse; riding a white horse is riding a horse.",
                    ok=True)
        r2 = cn_row("其弟，美人也；愛弟，非愛美人也。", r"Her younger brother is a handsome man; loving her brother is not "
                    r"loving a handsome man.", ok=False)
        rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, 0.7, 0])
        src = cite(r"\textit{Xiaoqu} (`Lesser Selection'), the Mohist canons; trans.\ after Graham")
        pattern = MathTex(r"X \text{ is } Y \ \Rightarrow\ \text{verb}(X) \text{ is } \text{verb}(Y)\ ?", font_size=36,
                          color=GOAL).move_to([0, -1.5, 0])
        link = label(r"the same failure as the \textit{Euthyphro}'s `because' (Chapter 4), and Frege's puzzle (Part 27)",
                     font_size=24, color=GREY_A).next_to(pattern, DOWN, buff=0.4)
        with self.voiceover(
            "The Mohists called it parallelizing: from 'this is that', infer 'doing something to this is doing it "
            "to that'. <bookmark mark='a'/>A white horse is a horse; so riding a white horse is riding a horse. "
            "Fine. <bookmark mark='b'/>But: her younger brother is a handsome man; and yet loving her brother is not "
            "loving a handsome man. Her love for her brother is not a love for handsome men. <bookmark mark='c'/>The "
            "Mohists had found contexts where you cannot swap terms for the same thing: the very failure we met in "
            "the Euthyphro's 'because', and the one that Frege will make the center of the philosophy of language in "
            "Part 27."
        ) as vo:
            self.play(FadeIn(src), Write(pattern))
            vo.wait_until("a")
            self.play(FadeIn(r1, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(r2, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(Indicate(pattern, color=GOAL), FadeIn(link))
        self.clear_scene()

    def white_horse(self):
        hc = history_card(r"c.\ 320--250 BCE", r"Gongsun Long, School of Names", r"`A white horse is not a horse'",
                          width=5.4, color=HIST).to_corner(UL, buff=0.4)
        q = cn_row("白馬非馬。", r"A white horse is not a horse.", color=GOAL)
        q.next_to(hc, DOWN, buff=0.5).align_to(hc, LEFT)
        big = Ellipse(width=5.2, height=3.4, stroke_color=P.CLAIM, stroke_width=3).move_to([3.0, -0.4, 0])
        small = Ellipse(width=2.0, height=1.4, stroke_color=P.AGENT, stroke_width=3).move_to([2.2, -0.8, 0])
        lb = label(r"horses", font_size=26, color=P.CLAIM).next_to(big.get_top(), DOWN, buff=0.25)
        ls = label(r"white horses", font_size=22, color=P.AGENT).move_to(small)
        readings = VGroup(
            label(r"`is' as inclusion: \ white horse $\subseteq$ horse \ \ true", font_size=24, color=OK),
            label(r"`is' as identity: \ white horse $=$ horse \ \ false", font_size=24, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.9)
        test = label(r"Gongsun Long's test: \ ask for a horse, and a yellow one will do; \ ask for a white horse, "
                     r"and it will not", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The most famous argument of the School of Names sounds like a joke. <bookmark mark='a'/>Gongsun Long "
            "argued that a white horse is not a horse. <bookmark mark='b'/>His test: if you ask for a horse, a "
            "yellow or a black one will do; ask for a white horse, and they will not. So 'white horse' and 'horse' "
            "cannot be the same. <bookmark mark='c'/>In modern terms he is playing on two meanings of 'is'. As "
            "inclusion, white horses are among the horses: true. As identity, white horse is horse: false. "
            "<bookmark mark='d'/>Aristotle's 'all S are P' is the first reading. Telling the readings of 'is' apart "
            "is the first job of any logic, and Part 3 does it with symbols."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(test), Create(big), FadeIn(lb))
            vo.wait_until("c")
            self.play(Create(small), FadeIn(ls), FadeIn(readings))
            vo.wait_until("d")
            self.play(Indicate(readings[0], color=OK))
        self.clear_scene()

    def canon(self):
        r1 = cn_row("或謂之牛，或謂之非牛，是爭彼也。", r"One calls it an ox, the other calls it not an ox: this is contending "
                    r"over a converse.")
        r2 = cn_row("是不俱當。", r"They do not both fit.", color=P.CLAIM)
        rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.8, 0])
        laws = VGroup(label(r"not both fit: \ non-contradiction", font_size=28, color=OK),
                      label(r"and `to say neither wins is not fitting': \ one must win", font_size=26, color=OK)).arrange(
            DOWN, buff=0.2).move_to([0, -1.6, 0])
        src = cite(r"Mohist Canons A74, B35; trans.\ after Graham")
        with self.voiceover(
            "The Canons even state laws for contradictory claims. <bookmark mark='a'/>One person calls a thing an ox, "
            "another calls it not an ox: that is a contest over a claim and its converse. <bookmark mark='b'/>They do "
            "not both fit. And the Canons add that it is wrong to say neither side wins. <bookmark mark='c'/>That is "
            "the law of non-contradiction, and the law of excluded middle, for a pair of contradictory claims: "
            "stated in China, independently of Aristotle, at about the same time."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(r2))
            vo.wait_until("c")
            self.play(FadeIn(laws))
        self.clear_scene()
