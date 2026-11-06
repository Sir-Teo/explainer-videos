from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Kripke(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Kripke's theory of truth", r"Can a language contain its own truth predicate?",
                            lit=(1975,), part=PART)
        with self.voiceover("Chapter four. Kripke's theory of truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.world()
        self.stages()

    def idea(self):
        hc = history_card(1975, r"Saul Kripke", r"`Outline of a theory of truth', \textit{Journal of Philosophy}",
                          width=6.8, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"one language, \ one predicate $T$, \ which applies to sentences of that same language",
                            font_size=26),
                      label(r"three values, \ as in Part 5's $K_3$: \ true, false, \ and neither", font_size=26),
                      label(r"learn `true' as a child might: \ assert `$A$ is true' \ once you are entitled to assert "
                            r"$A$", font_size=26, color=GOAL),
                      label(r"and repeat, \ until nothing new can be said", font_size=26, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.4, 0])
        with self.voiceover(
            "Kripke's own theory, in the same paper of 1975, keeps a single language that contains its own truth "
            "predicate. <bookmark mark='a'/>One predicate, T, that applies to the sentences of the very language it "
            "belongs to. <bookmark mark='b'/>The price is a third value. Some sentences are neither true nor false, "
            "using the strong Kleene logic, K3, of Part 5. <bookmark mark='c'/>Kripke described the construction as "
            "the way someone might learn the word: you may assert that a sentence is true as soon as you are "
            "entitled to assert the sentence itself. <bookmark mark='d'/>And then you repeat, applying what you have "
            "learned, until nothing new can be said."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def world(self):
        d = load("kripke")
        g = world_graph(d).shift(DOWN * 0.3)
        head = label(r"A small world of thirteen sentences", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        tags = VGroup(label(r"facts", font_size=22, color=GREY_B).next_to(g.node["s1"], UP, buff=0.2),
                      label(r"the liar", font_size=22, color=SELF).next_to(g.node["L"], UP, buff=0.08, aligned_edge=LEFT),
                      label(r"the truth-teller", font_size=22, color=SELF).next_to(g.node["H"], UP, buff=0.08, aligned_edge=LEFT),
                      label(r"a liar cycle", font_size=22, color=SELF).next_to(VGroup(g.node["A"], g.node["B"]), DOWN,
                                                                               buff=0.12))
        with self.voiceover(
            "Here is a small language, built into the Reasoner. <bookmark mark='a'/>Two plain facts: snow is white, "
            "and grass is red. Sentences about them: 's1' is true, 's2' is not true, and both of those are true. "
            "<bookmark mark='b'/>Sentences that mix: 's1' or the liar is true; 's2' or the liar is true. "
            "<bookmark mark='c'/>And the troublemakers. The liar, L, says that L is not true. The truth-teller, H, "
            "says that H is true. A says that B is true, and B says that A is not: a liar in two steps. And two "
            "more, about the liar and the truth-teller. Each arrow points to a sentence that the sentence talks "
            "about."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for n in ("s1", "s2", "s3", "s4", "s5"):
                self.play(FadeIn(g.node[n]), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(g.node["s9"]), FadeIn(g.node["s10"]))
            vo.wait_until("c")
            self.play(*[FadeIn(g.node[n]) for n in ("L", "H", "A", "B", "s8", "s13")], FadeIn(tags))
            self.play(Create(g.edges), run_time=2)
        self.wait(1)
        self.world_mob = VGroup(head, g, tags)
        self.g = g

    def stages(self):
        d = load("kripke")
        g = self.g
        stages = d["stages"]
        panel = VGroup(label(r"stage 0: \ nothing is true, \ nothing false", font_size=22, color=GREY_B)).to_corner(
            DL, buff=0.25)
        notes = [r"stage 1: \ the facts", r"stage 2: \ sentences about the facts", r"stage 3: \ sentences about "
                 r"those", r"stage 4: \ nothing new: \ the least fixed point"]
        key = VGroup(*[VGroup(value_chip(v, 22), label(t, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.12)
                       for v, t in (("t", r"true"), ("f", r"false"), ("n", r"neither"))]).arrange(
            RIGHT, buff=0.4).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Now run the construction. <bookmark mark='a'/>At stage zero, the truth predicate applies to nothing, "
            "and its negation to nothing. Every sentence about truth is neither true nor false. "
            "<bookmark mark='b'/>Stage one: the facts settle themselves. Snow is white is true, grass is red is "
            "false. <bookmark mark='c'/>Stage two: now ''s1' is true' is true, ''s2' is not true' is true, and "
            "''s1' or the liar is true' is true, because one disjunct already is. <bookmark mark='d'/>Stage three: "
            "the sentence about s3 and s4. <bookmark mark='e'/>Stage four: nothing changes. The process has reached "
            "its least fixed point. Because each stage only adds, never retracts, a fixed point must be reached: "
            "here after three steps; in a language like arithmetic, after transfinitely many. The extension of "
            "truth grows like a crystal, and the liar, the truth-teller and the cycle are never touched."
        ) as vo:
            self.play(FadeIn(panel), FadeIn(key))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*g.node.values()), color=GREY_B, scale_factor=1.01))
            for k, mk in zip(range(1, 4), "bcd"):
                vo.wait_until(mk)
                new = [n for n in d["names"] if stages[k][n] != "n" and stages[k - 1][n] == "n"]
                np_ = label(notes[k - 1], font_size=22, color=GOAL).to_corner(DL, buff=0.25)
                self.play(*[paint(g.node[n], stages[k][n]) for n in new], ReplacementTransform(panel, np_), run_time=1.4)
                panel = np_
            vo.wait_until("e")
            np_ = label(notes[3], font_size=22, color=OK).to_corner(DL, buff=0.25)
            self.play(ReplacementTransform(panel, np_))
            self.play(*[Indicate(g.node[n], color=SELF, scale_factor=1.06) for n in ("L", "H", "A", "B")])
        self.clear_scene()
