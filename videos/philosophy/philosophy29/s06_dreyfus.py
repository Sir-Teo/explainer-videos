from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Dreyfus(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"What computers can't do", r"Is intelligence the following of rules?",
                            lit=(1965, 1972), part=PART)
        with self.voiceover("Chapter five. What computers can't do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.critique()
        self.skill()
        self.answer()

    def critique(self):
        hc = history_card(1972, r"Hubert Dreyfus", r"\textit{What Computers Can't Do}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"biological", r"the brain processes information in discrete steps, \ like switches", GREY_A),
            (r"psychological", r"the mind operates on bits of information by formal rules", ACT),
            (r"epistemological", r"all knowledge can be formalized \ as explicit rules", SIGN),
            (r"ontological", r"the world is a set of independent, \ context-free facts", OBJ),
        ]
        g = rows_table(rows, top=0.9, gap=0.45)
        foot = label(r"Dreyfus: \ each assumption fails, \ for Heideggerian reasons", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1965 the RAND Corporation published a memo by a young philosopher at MIT, Hubert Dreyfus, called "
            "Alchemy and Artificial Intelligence. The researchers were furious, and when, in 1967, Dreyfus lost a game "
            "of chess to one of their programs, they made sure everyone knew. In 1972 the memo became a book, What "
            "Computers Can't Do. <bookmark mark='a'/>He argued that symbolic AI rested on four assumptions. "
            "Biological: the brain processes information in discrete steps, like switches. "
            "<bookmark mark='b'/>Psychological: the mind operates on bits of information according to formal rules. "
            "<bookmark mark='c'/>Epistemological: all knowledge can be formalized. <bookmark mark='d'/>Ontological: "
            "the world consists of independent, context-free facts. <bookmark mark='e'/>Every one, he argued, is "
            "false, and the reasons are Heidegger's: what we know is mostly know-how, not facts; and what a fact "
            "means depends on a situation that no list of facts can capture."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def skill(self):
        head = label(r"Five stages of skill \ (Dreyfus and Dreyfus, \ 1980)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        stages = [(r"novice", r"context-free rules: \ `shift at 20 mph'"),
                  (r"advanced beginner", r"situational aspects: \ the sound of the engine"),
                  (r"competent", r"a chosen plan, \ and responsibility for it"),
                  (r"proficient", r"sees what to do, \ still decides how"),
                  (r"expert", r"sees what to do, \ and does it: \ no rules consulted")]
        steps = VGroup()
        for i, (n, d) in enumerate(stages):
            x, y = -5.2 + 2.3 * i, -1.9 + 0.75 * i
            blk = Rectangle(width=2.2, height=0.5, color=ACT, fill_opacity=0.15 + 0.15 * i, stroke_width=2).move_to(
                [x, y, 0])
            nm = label(n, font_size=18, color=WHITE).move_to(blk)
            ds = wrapped_label(d, 2.2, 15, GREY_A).next_to(blk, DOWN, buff=0.12)
            steps.add(VGroup(blk, nm, ds))
        rules = label(r"explicit rules", font_size=18, color=SIGN).move_to([-5.2, 1.6, 0])
        rule_bar = Rectangle(width=11.0, height=0.18, stroke_width=0).move_to([-0.3, 1.2, 0])
        rule_bar.set_fill(color=[SIGN, BLACK], opacity=0.8)
        rules2 = label(r"intuitive response to the situation", font_size=18, color=WORLD).move_to([3.8, 1.6, 0])
        with self.voiceover(
            "Hubert and his brother Stuart, an engineer, studied how people actually acquire skills: drivers, chess "
            "players, pilots. <bookmark mark='a'/>The novice follows context-free rules: shift gear at twenty miles "
            "an hour. <bookmark mark='b'/>The advanced beginner learns aspects that no rule defines, like the sound "
            "of the engine. <bookmark mark='c'/>The competent performer chooses a plan, and feels responsible for "
            "it. <bookmark mark='d'/>The proficient performer sees what needs doing, but still decides how. "
            "<bookmark mark='e'/>The expert sees what to do and does it, without consulting any rules at all. "
            "<bookmark mark='f'/>Rules are the ladder, not the skill. If expertise is the end of rule-following, "
            "then a system made only of rules is a permanent novice."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(rule_bar), FadeIn(rules), FadeIn(rules2))
        self.clear_scene()

    def answer(self):
        head = label(r"What learning answered, \ and what it did not", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        rows = [
            (r"answered", r"skills learned from examples, \ with no explicit rules: \ vision, \ speech, \ AlphaGo's "
                          r"`intuition' \ (2016)", OK),
            (r"Dreyfus \ (2007)", r"`Why Heideggerian AI failed': \ the embodied robotics of the 1990s still "
                                  r"represented the world", HIST),
            (r"not answered", r"relevance in an open situation: \ the frame problem, \ next", BAD),
            (r"not answered", r"mattering: \ `the trouble with artificial intelligence is that computers don't give a "
                              r"damn' \ (Haugeland)", BAD),
            (r"open", r"do models trained on what people wrote inherit their background? \ Parts 41 and 42", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Fifty years on, how did the critique fare? <bookmark mark='a'/>Part of it was answered by a kind of AI "
            "Dreyfus himself favoured over symbols: learning. Vision, speech and the game of Go are now handled by "
            "networks trained on examples, with no explicit rules; AlphaGo's moves in 2016 were described, by "
            "professionals, as intuitive. <bookmark mark='b'/>Dreyfus was not satisfied. In 2007 he argued that even "
            "the embodied robotics of the 1990s still represented the world rather than coping with it. "
            "<bookmark mark='c'/>Two problems remain open. The first is relevance: knowing, in a situation never met "
            "before, what matters and what can be ignored. That is the frame problem, the next chapter. "
            "<bookmark mark='d'/>The second is mattering itself. As John Haugeland put it, the trouble with "
            "artificial intelligence is that computers don't give a damn. <bookmark mark='e'/>Whether models "
            "trained on what people have written inherit some of their background, or only its traces, is a "
            "question for the last parts of this series."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
