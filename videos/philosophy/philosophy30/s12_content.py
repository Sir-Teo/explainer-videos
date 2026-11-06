from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Content(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Content, \ naturalized", r"How can a physical state be about something?",
                            lit=(1981, 1984), part=PART)
        with self.voiceover("Chapter eleven. Content, naturalized."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dretske()
        self.gauge()
        self.millikan()
        self.fodor()

    def dretske(self):
        hc = history_card(1981, r"Fred Dretske", r"\textit{Knowledge and the Flow of Information}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"tree rings carry information about the tree's age; \ smoke, \ about fire", GREY_A),
                      (r"a signal carries the information that $s$ is $F$ \ iff \ $P(s \text{ is } F \mid "
                       r"\text{signal}) = 1$", SYM),
                      (r"the hope: \ meaning is information, \ and information is physics", GOAL)], font_size=22,
                     aligned_edge=LEFT, width=12.0, buff=0.35).move_to([0, -0.2, 0])
        with self.voiceover(
            "Brentano's question, from Part 29, is how a physical state could be about anything. Fred Dretske's answer "
            "began with information. <bookmark mark='a'/>Tree rings carry information about a tree's age; smoke, "
            "about fire. <bookmark mark='b'/>Precisely: a signal carries the information that s is F if, given the "
            "signal, the probability that s is F is one. <bookmark mark='c'/>If mental content is a kind of "
            "information, and information is a matter of physical law, then meaning would be part of nature."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gauge(self):
        d = load("gauge")
        head = label(r"A fuel gauge, \ in bits", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = {r["noise"]: r for r in d["rows"]}
        assert d["levels"] == 4 and d["max_bits"] == 2.0
        assert rows_d[0.0]["bits"] == 2.0 and rows_d[0.0]["readings_certain"] == 4
        assert rows_d[0.1]["bits"] == 1.4792 and rows_d[0.3]["bits"] == 0.9524 and rows_d[0.6]["bits"] == 0.6631
        assert all(rows_d[e]["readings_certain"] == 0 for e in (0.1, 0.3, 0.6))
        tank = Rectangle(width=1.2, height=2.6, color=PHYS).move_to([-5.0, 0.0, 0])
        fuel = Rectangle(width=1.16, height=1.3, stroke_width=0, fill_color=PHYS, fill_opacity=0.5).align_to(tank,
                                                                                                         DOWN).set_x(-5.0)
        dial = Arc(radius=1.0, start_angle=PI, angle=-PI, color=SYM).move_to([-2.4, 0.3, 0])
        needle = Line(dial.get_center() + DOWN * 0.5, dial.get_center() + DOWN * 0.5 + 0.9 * np.array(
            [math.cos(2 * PI / 3), math.sin(2 * PI / 3), 0]), color=SYM, stroke_width=4)
        marks = VGroup(*[label(t, font_size=15, color=GREY_A).move_to(dial.get_center() + DOWN * 0.5 + 1.25 * np.array(
            [math.cos(a), math.sin(a), 0])) for t, a in zip(["E", "1/3", "2/3", "F"], np.linspace(PI, 0, 4))])
        hd = [r"\text{needle error rate}", r"\text{bits about the tank}", r"\text{readings that are certain}"]
        cells = [[MathTex(f"{e:g}", font_size=22), MathTex(f"{rows_d[e]['bits']:.2f}", font_size=22, color=SYM),
                  MathTex(f"{rows_d[e]['readings_certain']} \\text{{ of }} 4", font_size=22,
                          color=OK if rows_d[e]['readings_certain'] else BAD)] for e in (0.0, 0.1, 0.3, 0.6)]
        grid = ValueGrid(hd, cells, col_w=[2.4, 2.6, 2.9], cell_h=0.5, font_size=18).move_to([2.75, 0.2, 0])
        foot = stack([(r"with any noise, \ no reading carries the information that the tank is at any level", BAD),
                      (r"yet a gauge reading `full' on a half-empty tank \textit{misrepresents}: \ information alone "
                       r"cannot say what it was supposed to indicate", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=12.0, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner tests the idea on a fuel gauge with four marks. <bookmark mark='a'/>With a perfect needle, "
            "a reading carries two bits about the tank, and every reading is certain: read two thirds, and the tank "
            "is at two thirds. <bookmark mark='b'/>Let the needle err one time in ten, to a neighbouring mark. The "
            "gauge still carries one point four eight bits. At three errors in ten, under one bit; at six in ten, "
            "about two thirds of a bit. <bookmark mark='c'/>But with any error at all, not one reading makes any level "
            "certain, so on Dretske's strict definition no reading carries the information that the tank is at any "
            "level. <bookmark mark='d'/>And that exposes the deeper problem. A gauge that reads full on a half-empty "
            "tank is not carrying no information; it is misrepresenting. Representation can be wrong; information, "
            "in this sense, cannot. Something must say what the gauge is supposed to indicate."
        ) as vo:
            self.play(FadeIn(head), Create(tank), FadeIn(fuel), Create(dial), FadeIn(marks), Create(needle))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            for r in range(1, 4):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def millikan(self):
        hc = history_card(1984, r"Ruth Millikan", r"\textit{Language, Thought, and Other Biological Categories}",
                          width=7.6, color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"teleosemantics", r"content comes from function: \ what a state was selected to indicate", FUNC),
            (r"the frog", r"its tongue-snap detector was selected because it caught flies: \ it means `fly', \ even "
                          r"when it fires at a pellet", OK),
            (r"misrepresentation", r"a system misrepresents when it fails to do what it was selected for", MIND),
            (r"the puzzle", r"`fly', \ `food', \ or `small dark moving thing'? \ selection does not choose \ (Fodor, "
                            r"\ 1990)", BAD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5)
        with self.voiceover(
            "Ruth Millikan, in 1984, supplied the missing ingredient: function. <bookmark mark='a'/>On her "
            "teleosemantics, a state means what it was selected, by evolution or learning, to indicate. "
            "<bookmark mark='b'/>A frog's tongue snaps at small dark moving things. The detector was selected because "
            "it caught flies, so it means fly, even when it fires at a pellet flicked past by a scientist. "
            "<bookmark mark='c'/>Misrepresentation is failing to do what the system was selected for. "
            "<bookmark mark='d'/>Fodor pressed a puzzle. The frog's ancestors were selected for catching flies, but "
            "also for catching food, and for catching small dark moving things, since around ponds these came to the "
            "same. Which is the content? Selection alone does not seem to choose."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fodor(self):
        head = label(r"Asymmetric dependence \ (Fodor, \ 1987, \ 1990)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        cow = VGroup(label(r"cows", font_size=24, color=PHYS), MathTex(r"\longrightarrow", font_size=32),
                     label(r"`cow'", font_size=24, color=SYM)).arrange(RIGHT, buff=0.3).move_to([-2.8, 1.0, 0])
        horse = VGroup(label(r"horses on a dark night", font_size=24, color=GREY_A), MathTex(r"\longrightarrow",
                                                                                            font_size=32),
                       label(r"`cow'", font_size=24, color=SYM)).arrange(RIGHT, buff=0.3).move_to([2.8, 1.0, 0])
        dep = Arrow([1.0, 0.5, 0], [-1.0, 0.5, 0], color=BAD, buff=0.1)
        dl = label(r"depends on", font_size=17, color=BAD).next_to(dep, DOWN, buff=0.08)
        rows = stack([(r"`cow' means cow, \ not cow-or-horse: \ the disjunction problem", MIND),
                      (r"break the cow law, \ and the horse law breaks too; \ not the other way round", SYM),
                      (r"so the cow law is basic, \ and fixes what `cow' means", OK),
                      (r"critics: \ the counterfactuals are hard to assess, \ and the account seems tailored to its "
                       r"examples", BAD)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.24).to_edge(DOWN,
                                                                                                   buff=0.4)
        with self.voiceover(
            "Fodor's own answer was asymmetric dependence. <bookmark mark='a'/>Cows cause tokens of the mental word "
            "cow. <bookmark mark='b'/>So, sometimes, do horses on a dark night. Why does cow mean cow, and not cow or "
            "horse on a dark night? This is the disjunction problem. <bookmark mark='c'/>Fodor: the horse-to-cow law "
            "depends on the cow-to-cow law, and not the other way round. If cows did not cause cow, horses would not "
            "either; but cows would go on causing cow even if horses stopped. <bookmark mark='d'/>So the cow law is "
            "basic, and it fixes the content. <bookmark mark='e'/>Critics found the counterfactuals hard to assess, "
            "and the account tailored to its examples. Naturalizing content remains an open problem, and it is "
            "exactly the problem of saying what a language model's internal states are about."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cow))
            vo.wait_until("b")
            self.play(FadeIn(horse), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(GrowArrow(dep), FadeIn(dl), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
