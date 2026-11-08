from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Agree(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Agreeing to disagree", r"Can rational people agree to differ?", lit=(1976,),
                            part=PART)
        with self.voiceover("Chapter eight. Agreeing to disagree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.dialogue()
        self.trade()

    def theorem(self):
        hc = history_card(1976, r"Robert Aumann", r"`Agreeing to Disagree', \ \textit{Annals of Statistics}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"two agents with the same prior, \ different information", font_size=24),
            label(r"if their posteriors for an event are common knowledge,", font_size=24, color=COMMON),
            label(r"then the posteriors are equal", font_size=27, color=GOAL),
            label(r"proof idea: \ each posterior is an average over the common-knowledge cell \ (the meet),",
                  font_size=21, color=GREY_A),
            label(r"and averaging a constant over the same cell \ gives the same number to both", font_size=21,
                  color=GREY_A),
            label(r"so honest Bayesians who know each other's opinions \ cannot agree to disagree", font_size=24,
                  color=OK)).arrange(DOWN, buff=0.27).move_to([0, -0.6, 0])
        with self.voiceover(
            "Common knowledge also constrains disagreement. <bookmark mark='a'/>Robert Aumann, in 1976, considered "
            "two agents with the same prior probabilities but different information. <bookmark mark='b'/>Suppose "
            "their posterior probabilities for some event are common knowledge between them. <bookmark mark='c'/>"
            "Then those posteriors must be equal. <bookmark mark='d'/>The proof is a few lines. Each agent's "
            "posterior is the same in every one of her cells within the common-knowledge cell, so it equals the "
            "probability of the event given that whole cell. <bookmark mark='e'/>And that is one number, the same for "
            "both. <bookmark mark='f'/>So two honest Bayesians, starting from the same prior, who come to know each "
            "other's opinions, cannot agree to disagree."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dialogue(self):
        d = load("agree")
        head = label(r"Geanakoplos and Polemarchakis (1982): \ talk until you agree", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        cell = 0.75
        grid = VGroup()
        sq = {}
        for k in range(9):
            r, c = divmod(k, 3)
            s_ = k + 1
            box = Square(side_length=cell, stroke_color=GREY_C, stroke_width=1.5,
                         fill_color=COMMON if s_ in d["event"] else "#111", fill_opacity=0.35 if s_ in d["event"]
                         else 0.3).move_to([-4.5 + c * cell, 1.0 - r * cell, 0])
            t = label(str(s_), font_size=22).move_to(box)
            sq[s_] = box
            grid.add(VGroup(box, t))
        a_cells = VGroup(*[SurroundingRectangle(VGroup(*[sq[s_] for s_ in c]), color=AG["A"], buff=0.04,
                                                stroke_width=3) for c in d["A"]])
        b_lines = VGroup()
        for ci, c in enumerate(d["B"]):
            tag = [r"i", r"ii", r"iii"][ci]
            b_lines.add(VGroup(*[label(tag, font_size=15, color=AG["B"]).move_to(sq[s_].get_center() + DOWN * 0.24)
                                 for s_ in c]))
        act = Circle(radius=0.3, color=WHITE, stroke_width=3).move_to(sq[d["actual"]])
        key = VGroup(label(r"nine equally likely states; \ the event: \ $\{3, 4\}$", font_size=20, color=COMMON),
                     label(r"A learns the row \ (blue boxes)", font_size=20, color=AG["A"]),
                     label(r"B learns $\{1..4\}$ (i), \ $\{5..8\}$ (ii) \ or $\{9\}$ (iii)", font_size=20,
                           color=AG["B"]),
                     label(r"actual state: \ 1", font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.12).next_to(grid, DOWN,
                                                                                                         buff=0.35)
        lines = VGroup()
        for i, r in enumerate(d["dialogue"]):
            if r["speaker"] == "both":
                t = label(rf"now both: \ ${r['says']}$ \ \ agreement", font_size=24, color=OK)
            else:
                t = label(rf"{r['speaker']} says: \ `my probability is ${r['says']}$' \quad (A: ${r['A']}$, \ "
                          rf"B: ${r['B']}$)", font_size=22, color=AG[r["speaker"]])
            lines.add(t)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.2, 0])
        foot = label(r"each announcement tells the listener where the speaker could not be", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.0)
        with self.voiceover(
            "John Geanakoplos and Heraklis Polemarchakis turned Aumann's theorem into a conversation. "
            "<bookmark mark='a'/>Nine equally likely states, and an event: the state is three or four. A learns "
            "which row the state is in. B learns whether it is one to four, five to eight, or nine. In fact it is "
            "one. <bookmark mark='b'/>A's row holds one, two and three, one of which is in the event, so A says: my "
            "probability is a third. <bookmark mark='c'/>That tells B that the state is not seven, eight or nine, "
            "where A would have said zero. B's own cell, one to four, is untouched; two of its four states are in the "
            "event, so B says a half. <bookmark mark='d'/>B's half tells A that the state is one to four, since in "
            "five to eight B would now have said zero. A's row is untouched, so A says a third again. But this "
            "repeated third tells B something new: in state four, A, knowing from B's half that the state was one to "
            "four, would have known it was four, and said one. <bookmark mark='e'/>So the state is not four. B's "
            "cell shrinks to one, two, three, and B says a third. They have agreed, as Geanakoplos and Polemarchakis "
            "proved they always must, on any finite space."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), Create(a_cells), FadeIn(b_lines), Create(act), FadeIn(key))
            for mk, i in zip("bcde", range(len(lines))):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.1))
            if len(lines) > 4:
                self.play(FadeIn(lines[4:]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def trade(self):
        head = label(r"The no-trade theorem", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Milgrom and Stokey (1982): \ if it is common knowledge that both sides accept a trade,",
                  font_size=23),
            label(r"and both are rational with a common prior, \ then neither expects to gain from it", font_size=23,
                  color=GREY_A),
            label(r"`if you're willing to sell me that share, \ what do you know that I don't?'", font_size=25,
                  color=GOAL),
            label(r"yet markets trade billions a day: \ different priors, \ liquidity needs, \ or less than "
                  r"rationality", font_size=23, color=BAD),
            label(r"the theorems tell us what real disagreement must involve", font_size=24,
                  color=OK)).arrange(DOWN, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "The same reasoning gives a startling result in economics. <bookmark mark='a'/>Paul Milgrom and Nancy "
            "Stokey proved in 1982 that if it is common knowledge that both sides accept a trade, <bookmark mark='b'/>"
            "and both are rational with a common prior, then neither can expect to gain from it. "
            "<bookmark mark='c'/>If you are willing to sell me that share at that price, what do you know that I "
            "don't? <bookmark mark='d'/>Yet markets trade billions every day. So real traders must differ in their "
            "priors, or trade for reasons like needing cash, or be less than perfectly rational. "
            "<bookmark mark='e'/>The theorems do not describe us. They tell us what real disagreement must involve. "
            "We return to disagreement between peers in chapter thirteen."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
