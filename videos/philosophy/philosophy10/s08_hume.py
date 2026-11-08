from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Hume(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Impressions and ideas", r"Can we think anything we have never experienced?",
                            lit=(1739, 1748), part=PART)
        with self.voiceover("Chapter seven. Impressions and ideas."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.copy()
        self.shade()
        self.fork()

    def copy(self):
        hcs = VGroup(history_card(1739, r"David Hume", r"\textit{A Treatise of Human Nature}", width=4.8, color=HIST),
                     history_card(1748, r"David Hume", r"\textit{An Enquiry Concerning Human Understanding}", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        left = VGroup(label(r"impressions", font_size=30, color=SENSE),
                      label(r"what we feel and see: \ vivid", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        right = VGroup(label(r"ideas", font_size=30, color=REASON),
                       label(r"faint copies of impressions", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        pair = VGroup(left, right).arrange(RIGHT, buff=2.6).move_to([0, 0.6, 0])
        arr = Arrow(left.get_right(), right.get_left(), buff=0.3, color=GREY_B)
        rows = VGroup(label(r"the copy principle: \ every simple idea comes from a simple impression", font_size=24,
                            color=GOAL),
                      label(r"a golden mountain: \ gold, \ and a mountain, \ joined", font_size=22, color=GREY_A),
                      label(r"a test for meaning: \ from what impression is this idea derived?", font_size=24,
                            color=OK)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "David Hume's Treatise of 1739, and his Enquiry of 1748, push empiricism to its conclusions. "
            "<bookmark mark='a'/>The contents of the mind are of two kinds: impressions, what we feel and see, which "
            "are vivid; and ideas, which are fainter copies of them. <bookmark mark='b'/>Every simple idea comes from "
            "a simple impression that it resembles. <bookmark mark='c'/>Complex ideas are built from simple ones: a "
            "golden mountain is gold and a mountain, joined in thought. <bookmark mark='d'/>This gives Hume a weapon. "
            "When a philosopher uses a word, ask: from what impression is this idea derived? If there is none, the "
            "word has no meaning."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(FadeIn(left), GrowArrow(arr), FadeIn(right))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shade(self):
        d = load("shades")
        head = label(r"The missing shade of blue", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        sw = VGroup(*[RoundedRectangle(width=0.95, height=1.6, corner_radius=0.08, stroke_width=0, fill_color=c,
                                       fill_opacity=1) for c in d["shades"]]).arrange(RIGHT, buff=0.12).move_to(
            [0, 0.8, 0])
        gap = sw[d["missing"]]
        hole = RoundedRectangle(width=0.95, height=1.6, corner_radius=0.08, stroke_color=GOAL, stroke_width=3,
                                fill_opacity=0).move_to(gap)
        qmark = label(r"?", font_size=48, color=GOAL).move_to(gap)
        rows = VGroup(label(r"someone has seen every shade of blue but one", font_size=24),
                      label(r"set out in order, \ the gap is obvious: \ can they imagine the missing shade?",
                            font_size=24, color=GOAL),
                      label(r"Hume: \ yes, \ though it never came from an impression", font_size=24, color=OK),
                      label(r"`so particular and singular' \ that it is not worth changing the principle", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Hume himself gave the best counterexample to his principle. <bookmark mark='a'/>Imagine someone who has "
            "seen every shade of blue but one. <bookmark mark='b'/>Set the shades out in order, from light to dark, "
            "and there is an obvious gap where the missing one belongs. <bookmark mark='c'/>Can they imagine it? Hume "
            "thought they could, though no impression gave it to them. <bookmark mark='d'/>And he shrugged: the case "
            "is so particular and singular, he wrote, that it is scarce worth our observing, and does not merit that "
            "for it alone we should alter our general maxim."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for i, s_ in enumerate(sw) if i != d["missing"]], lag_ratio=0.1),
                      FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(hole), FadeIn(qmark), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(qmark), FadeIn(gap), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fork(self):
        head = label(r"Hume's fork", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(label(r"relations of ideas", font_size=28, color=REASON),
                      label(r"`the square of the hypotenuse \ equals the sum of the squares'", font_size=21),
                      label(r"known by thought alone; \ its denial is a contradiction", font_size=20, color=GREY_A),
                      label(r"certain, \ but says nothing about what exists", font_size=20, color=REASON)).arrange(
            DOWN, buff=0.18)
        right = VGroup(label(r"matters of fact", font_size=28, color=SENSE),
                       label(r"`the sun will rise tomorrow'", font_size=21),
                       label(r"known only by experience; \ its denial is conceivable", font_size=20, color=GREY_A),
                       label(r"about the world, \ but never certain", font_size=20, color=SENSE)).arrange(DOWN,
                                                                                                    buff=0.18)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.4).move_to([0, 0.6, 0])
        q = quote_card(r"Commit it then to the flames: for it can contain nothing but sophistry and illusion.",
                       r"David Hume", r"\textit{Enquiry}, \ the last sentence", width=9.6, font_size=26).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Hume then divided all reasoning in two. <bookmark mark='a'/>Relations of ideas, like Pythagoras's "
            "theorem, are known by thought alone, and denying them is a contradiction. They are certain, but they say "
            "nothing about what exists. <bookmark mark='b'/>Matters of fact, like the sun rising tomorrow, are known "
            "only by experience, and their denial is perfectly conceivable. They are about the world, but never "
            "certain. <bookmark mark='c'/>Anything that is neither is worthless. The Enquiry ends: if we take in our "
            "hand any volume of divinity or school metaphysics, and it contains no abstract reasoning concerning "
            "quantity or number, and no experimental reasoning concerning matter of fact, commit it then to the "
            "flames: for it can contain nothing but sophistry and illusion."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()
