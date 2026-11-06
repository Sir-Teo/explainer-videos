from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Thesis(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The Church--Turing thesis, \ and Rice", r"What has been defined, and what can "
                            r"never be checked?", lit=(1936,), part=PART)
        with self.voiceover("Chapter eleven. The Church-Turing thesis, and Rice's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.not_say()
        self.rice()

    def thesis(self):
        head = label(r"Many definitions, \ one class of functions", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        models = [(r"Turing machines", 1936), (r"$\lambda$-calculus \ (Church)", 1936), (r"recursive functions \ (Gödel, Herbrand, "
                  r"Kleene)", 1934), (r"Post systems", 1936),
                  (r"register machines", 1963), (r"the cellular automaton Rule 110", 2004),
                  (r"every programming language", None)]
        centre = Circle(radius=1.0, color=GOAL, fill_color=GOAL, fill_opacity=0.15).move_to([0, -0.2, 0])
        cl = label(r"the computable \\ functions", font_size=24, color=GOAL).move_to(centre)
        spokes = VGroup()
        for i, (m, y) in enumerate(models):
            ang = PI / 2 + i * TAU / len(models)
            p = centre.get_center() + 2.75 * np.array([np.cos(ang) * 1.35, np.sin(ang), 0])
            t = label(m + (rf" \ ({y})" if y else ""), font_size=21, color=TAPE).move_to(p)
            a = Arrow(t.get_center() + (centre.get_center() - t.get_center()) * 0.28,
                      centre.get_center() + (t.get_center() - centre.get_center()) / np.linalg.norm(
                          t.get_center() - centre.get_center()) * 1.05, buff=0, color=GREY_B, stroke_width=2,
                      max_tip_length_to_length_ratio=0.12)
            spokes.add(VGroup(t, a))
        thesis = label(r"the thesis: \ every function a human can compute by rule \ is Turing-computable",
                       font_size=24, color=SELF).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why believe that Turing caught the right notion? <bookmark mark='a'/>Because every serious attempt to "
            "define mechanical computation has produced exactly the same class of functions: Turing's machines, "
            "Church's lambda calculus, the recursive functions of Gödel, Herbrand and Kleene, Post's systems, "
            "register machines, even a one-dimensional cellular automaton called Rule 110, and every programming "
            "language ever built. <bookmark mark='b'/>The Church-Turing thesis says that this class is the right "
            "one: whatever a human can compute by following rules, a Turing machine can "
            "compute. It is not a theorem, because 'compute by following rules' is not a mathematical notion. It "
            "is a claim about the fit between a definition and an idea, and the evidence for it is overwhelming."
        ) as vo:
            self.play(FadeIn(head), FadeIn(centre), FadeIn(cl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s[0]), GrowArrow(s[1])) for s in spokes], lag_ratio=0.35),
                      run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(thesis))
        self.clear_scene()

    def not_say(self):
        head = label(r"What the thesis does \textit{not} say", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            VGroup(label(r"not: \ the mind is a Turing machine", font_size=26, color=BAD),
                   label(r"the thesis is about clerks following rules, \ not about everything a mind does \ "
                         r"(Chapter 16; Part 30)", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12),
            VGroup(label(r"not: \ every physical process is computable", font_size=26, color=BAD),
                   label(r"that is a separate, empirical thesis about physics \ (Gandy 1980; Part 26)", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"not: \ everything computable is computable \textit{quickly}", font_size=26, color=BAD),
                   label(r"quantum computers compute no new functions, \ but may compute some much faster \ "
                         r"(Shor 1994)", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        with self.voiceover(
            "The thesis is often stretched. Here is what it does not say. <bookmark mark='a'/>It does not say that "
            "the mind is a Turing machine: it is about a clerk following rules, not about everything a mind can do. "
            "That question comes back in Chapter 16, and in Part 30. <bookmark mark='b'/>It does not say that every "
            "physical process is computable. That is a different claim, about physics, which Robin Gandy analysed "
            "in 1980, and which might be false. <bookmark mark='c'/>And it says nothing about speed. Quantum "
            "computers compute no function a Turing machine cannot, but Peter Shor showed in 1994 that they could "
            "factor numbers far faster than any known classical method."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def rice(self):
        hc = history_card(1953, r"Henry Gordon Rice", r"`Classes of recursively enumerable sets and their decision "
                          r"problems'", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        thm = theorem_card(r"Rice's theorem", r"every non-trivial property of what a program \textit{does} \ (as "
                           r"opposed to how it is written) \ is undecidable", width=10.0, font_size=26).move_to(
            [0, 1.0, 0])
        proof = VGroup(label(r"given $M$ and $x$, \ build $M'$: \ `run $M$ on $x$; \ then behave like a program "
                             r"with the property'", font_size=24),
                       label(r"$M'$ has the property \ iff \ $M$ halts on $x$: \ a decider for the property decides "
                             r"halting", font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                           buff=0.22).next_to(thm, DOWN, buff=0.4)
        ex = VGroup(label(r"does this program ever print `hello'? \quad does it compute $x^2$? \quad is it malware?",
                          font_size=22, color=TAPE),
                    label(r"so every bug-finder must sometimes say `don't know', \ or be wrong: \ the abstractions "
                          r"of Part 4's model checkers", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The halting problem is the first of an endless family. <bookmark mark='a'/>Henry Rice proved in 1953 "
            "that every non-trivial property of what a program does, as opposed to how its text looks, is "
            "undecidable. <bookmark mark='b'/>The proof is one line. Given a machine M and an input x, build a new "
            "program that first runs M on x, and then, if that ever finishes, behaves like some program that has "
            "the property. The new program has the property exactly when M halts on x. So a decider for the "
            "property would decide halting. <bookmark mark='c'/>Does this program ever print hello? Does it compute "
            "the squaring function? Is it malware? No algorithm answers any of these for all programs. Every bug "
            "finder must sometimes say 'I don't know', or be wrong, which is why the model checkers of Part 4 work "
            "with abstractions."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in proof], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()
