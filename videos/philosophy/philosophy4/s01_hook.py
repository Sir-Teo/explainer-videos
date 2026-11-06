from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.readings()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        ex = VGroup(label(r"`It might have rained.'", font_size=30, color=GREY_A),
                    label(r"`Two plus two must be four.'", font_size=30, color=GREY_A),
                    label(r"`You ought to keep your promise.'", font_size=30, color=GREY_A),
                    label(r"`The lift will always come.'", font_size=30, color=GREY_A)).arrange(
            DOWN, buff=0.22).next_to(t, DOWN, buff=0.7)
        with self.voiceover(
            "Parts 2 and 3 built the logic of what is the case. But most of what we say goes beyond that. "
            "<bookmark mark='a'/>It might have rained. Two plus two must be four. You ought to keep your promise. "
            "The lift will always come eventually. <bookmark mark='b'/>Might, must, ought, always: these are "
            "modalities, ways in which a sentence is true. This part builds their logic, and it turns out to be one "
            "logic with many readings, from metaphysics to the chips in your phone."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.15) for e in ex], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(*[Indicate(e, color=GOAL) for e in ex])
        self.clear_scene()

    def readings(self):
        head = VGroup(MathTex(r"\Box\varphi", font_size=48, color=GOAL), label(r"is read as", font_size=26,
                                                                               color=GREY_A)).arrange(RIGHT, buff=0.3)
        head.to_edge(UP, buff=0.5)
        rows = [(r"necessarily $\varphi$", r"metaphysics", r"Leibniz, Kripke"),
                (r"the agent knows $\varphi$", r"epistemology", r"Hintikka 1962"),
                (r"$\varphi$ is obligatory", r"ethics and law", r"von Wright 1951"),
                (r"always in the future, $\varphi$", r"time", r"Prior 1957"),
                (r"$\varphi$ is provable", r"arithmetic", r"Gödel, Löb, Solovay"),
                (r"after every run of the program, $\varphi$", r"computer science", r"Hoare, Pratt, Pnueli")]
        tab = VGroup()
        for a, b, c in rows:
            tab.add(VGroup(label(a, font_size=26), label(b, font_size=22, color=P.CLAIM),
                           label(c, font_size=22, color=GREY_B)))
        for i, r in enumerate(tab):
            y = 1.6 - 0.62 * i
            r[0].move_to([-5.9 + r[0].width / 2, y, 0])
            r[1].move_to([1.4 + r[1].width / 2, y, 0])
            r[2].move_to([4.2 + r[2].width / 2, y, 0])
        one = label(r"one logic, \ one semantics: \ worlds, and which worlds can be seen from which", font_size=26,
                    color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Write a box for 'necessarily'. <bookmark mark='a'/>The same box can mean that something is necessary, "
            "that an agent knows it, that it is obligatory, that it will always be so, that it is provable in "
            "arithmetic, or that it holds after every run of a program. <bookmark mark='b'/>The remarkable "
            "discovery of the twentieth century is that all of these share one logic and one semantics: possible "
            "worlds, and a relation saying which worlds can be seen from which."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab], lag_ratio=0.35), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(one))
        self.clear_scene()

    def preview(self):
        d = load("kripke")
        pos = {0: (-2.4, 0.0, 0), 1: (0.0, 1.4, 0), 2: (0.0, -1.4, 0), 3: (2.4, -1.4, 0)}
        g = WorldGraph(d["worlds"], d["R"], {"p": set(d["p"])}, pos=pos, center=[-2.2, -0.2, 0])
        rules = VGroup(
            VGroup(MathTex(r"\Box p", font_size=40, color=GOAL),
                   label(r"$p$ is true in every world you can see", font_size=24)).arrange(RIGHT, buff=0.3),
            VGroup(MathTex(r"\Diamond p", font_size=40, color=GOAL),
                   label(r"$p$ is true in some world you can see", font_size=24)).arrange(RIGHT, buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 1.6, 0])
        tags = VGroup(*[g.tag(w, b) for w, b in zip(d["worlds"], d["table"]["[]p"])])
        tl = MathTex(r"\Box p:", font_size=30, color=GOAL).next_to(rules, DOWN, buff=0.6).align_to(rules, LEFT)
        wall_ = label(r"this part's brick: \ some modal axioms have no first-order meaning \ (Goldblatt, Thomason "
                      r"1975)", font_size=24, color=P.WALL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the whole idea in one picture. <bookmark mark='a'/>Four worlds, and arrows saying which "
            "worlds are possible from which. In two of them, p is true. <bookmark mark='b'/>'Necessarily p' is true "
            "at a world when p is true in every world it can see; 'possibly p', when p is true in at least one. "
            "<bookmark mark='c'/>So at world zero, necessarily p is false, because world two is visible and lacks "
            "p; at world one it is true. <bookmark mark='d'/>We will build this into a calculator, prove which "
            "axioms match which shapes of arrows, check a real concurrent program with it, and find the place "
            "where modal logic and first-order logic part ways: this part's brick in the Wall."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g.discs), LaggedStart(*[Create(a) for a in g.arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(rules))
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(t, scale=0.6) for t in tags], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(wall_))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Aristotle's sea battle and Diodorus's master argument",
            r"Lewis's strict implication; \ the systems; \ S4's fourteen modalities",
            r"Kripke semantics; \ axioms and frames, \ checked on every frame of up to four worlds",
            r"Löb's axiom, \ canonical models, \ bisimulation, \ filtration",
            r"quantified modal logic and the Barcan formula",
            r"obligation and Chisholm's paradox; \ time and the branching future",
            r"temporal logic, \ a model checker for Peterson's algorithm, \ Hoare logic, \ industry",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>the ancient puzzles about the future and the possible. Lewis's systems, and "
            "the fourteen modalities of S4. <bookmark mark='b'/>Kripke's semantics, and the exact match between "
            "axioms and shapes of frames, checked by the Reasoner on every frame of up to four worlds. "
            "<bookmark mark='c'/>Löb's axiom, completeness, what modal logic cannot see, and why it is decidable. "
            "Quantifiers and the Barcan formula. <bookmark mark='d'/>Then the applied logics: obligation, time, "
            "and the temporal logics that verify hardware and software, with a model checker we build ourselves."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mk, idx in (("a", [1]), ("b", [2]), ("c", [3, 4]), ("d", [5, 6])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()
