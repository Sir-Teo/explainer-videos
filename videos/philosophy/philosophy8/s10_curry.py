from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Curry(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Curry's paradox", r"Can a paradox prove anything at all, without negation?",
                            lit=(1942,), part=PART)
        with self.voiceover("Chapter nine. Curry's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.derive()
        self.threat()
        self.lob()
        self.st()
        self.vcurry()

    def derive(self):
        d = load("curry")
        hc = history_card(1942, r"Haskell Curry", r"`The inconsistency of certain formal logics'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        c = label(r"$C$: \ `if $C$ is true, \ then the moon is made of cheese'", font_size=30, color=SELF).move_to(
            [0, 1.6, 0])
        steps = [(r"T(\ulcorner C \urcorner) \leftrightarrow (T(\ulcorner C \urcorner) \to q)", r"the T-schema for C"),
                 (r"\text{suppose } T(\ulcorner C \urcorner)", r""),
                 (r"\text{then } T(\ulcorner C \urcorner) \to q, \ \text{so } q", r"modus ponens, twice"),
                 (r"\text{so } T(\ulcorner C \urcorner) \to q", r"conditional proof: \ the supposition used twice"),
                 (r"\text{so } T(\ulcorner C \urcorner), \ \text{and so } q", r"by the first line; \ modus ponens")]
        rows = VGroup()
        for i, (f, why) in enumerate(steps):
            y = 0.7 - 0.62 * i
            rows.add(VGroup(MathTex(f, font_size=32).move_to([-5.6, y, 0], aligned_edge=LEFT),
                            label(why, font_size=20, color=GOAL).move_to([1.6, y, 0],
                                                                                          aligned_edge=LEFT)))
        res = label(r"the moon is made of cheese: \ any $q$ at all, \ and no negation was used", font_size=26,
                    color=BAD).to_edge(DOWN, buff=0.45)
        assert d["classical_entails_q"]
        with self.voiceover(
            "Haskell Curry found, in 1942, a liar that needs no negation at all. <bookmark mark='a'/>Take the "
            "sentence C: if C is true, then the moon is made of cheese. <bookmark mark='b'/>By the T-schema, C is "
            "true exactly when, if C is true, the moon is made of cheese. <bookmark mark='c'/>Suppose C is true. "
            "Then, by the schema, if C is true then the moon is cheese; and C is true; so the moon is cheese. "
            "<bookmark mark='d'/>Discharging the supposition: if C is true, the moon is cheese. But that is what C "
            "says, so C is true, and so the moon is made of cheese. <bookmark mark='e'/>Any sentence whatever can "
            "replace the cheese. The Reasoner confirms, as in Part 6, that C if and only if C implies q, entails q."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(c))
            for mk, r in zip("bcd", (rows[0], VGroup(rows[1], rows[2]), VGroup(rows[3], rows[4]))):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.clear_scene()

    def threat(self):
        d = load("curry")
        head = label(r"Why Curry matters", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"no negation, \ so denying excluded middle \ or accepting contradictions \ does not block it",
                  font_size=24),
            label(r"the culprit is \textit{contraction}: \ using the supposition twice \ (the linear logic of Part 5 "
                  r"drops it)", font_size=24, color=GOAL),
            label(rf"in Kripke's fixed point, \ $C$ is simply neither \ (the Reasoner: \ `{d['kleene']}'): \ its "
                  r"conditional is too weak to detach", font_size=24),
            label(r"so every theory of truth needs a conditional strong enough to reason with, \ and weak enough to "
                  r"survive Curry", font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(
            [0, -0.2, 0])
        with self.voiceover(
            "Curry's paradox is the hardest test for a theory of truth. <bookmark mark='a'/>It uses no negation, so "
            "neither denying excluded middle nor accepting contradictions is enough on its own. "
            "<bookmark mark='b'/>What it uses is contraction: the supposition that C is true is used twice. The "
            "substructural logics of Part 5, like linear logic, drop that rule. <bookmark mark='c'/>In Kripke's "
            "fixed point, the Curry sentence is simply neither true nor false, because the material conditional "
            "of Kleene's logic does not support modus ponens across gaps. <bookmark mark='d'/>So every theory of "
            "truth needs a conditional strong enough to reason with, and weak enough to survive Curry. Field's and "
            "Priest's theories are, in large part, theories of that conditional."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()


    def lob(self):
        head = label(r"Curry and Löb: \ one argument, \ two predicates", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(label(r"Curry", font_size=28, color=SELF),
                      MathTex(r"C \leftrightarrow (T\ulcorner C \urcorner \to q)", font_size=30),
                      label(r"with `true': \ $q$, whatever it is", font_size=22, color=BAD)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"Löb \ (Part 7)", font_size=28, color=GOAL),
                       MathTex(r"L \leftrightarrow (\Box L \to A)", font_size=30),
                       label(r"with `provable': \ if $\Box A \to A$ is provable, \ so is $A$", font_size=22,
                             color=OK)).arrange(DOWN, buff=0.25)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to([0, 0.6, 0])
        moral = label(r"the same nine lines: \ for truth they prove everything, \ for provability a theorem",
                      font_size=26, color=GOAL).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Curry's paradox has a twin in Part 7. <bookmark mark='a'/>The Curry sentence says: if I am true, then "
            "q. <bookmark mark='b'/>Löb's sentence said: if I am provable, then A. Run the same argument with "
            "'true' and you prove anything at all; run it with 'provable' and the derivability conditions, and you "
            "prove Löb's theorem. <bookmark mark='c'/>The same nine lines. For truth they are a paradox; for "
            "provability, a theorem. The difference is that provability does not satisfy the T-schema: PA does "
            "not prove that whatever it proves is true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def st(self):
        d = load("st")
        hc = history_card(2012, r"Cobreros, Égré, Ripley \& van Rooij", r"strict-tolerant logic: \ from vagueness "
                          r"(Part 5) to the liar", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        defn = VGroup(label(r"ST: \ an argument is valid if, \ whenever the premises are \textit{strictly} true \ (t),",
                            font_size=24),
                      label(r"the conclusion is at least \textit{tolerantly} true \ (t or n)", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(hc, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        rows = VGroup(
            VGroup(MathTex(r"\vdash T\ulcorner L \urcorner", font_size=36), label(r"valid", font_size=24, color=OK)),
            VGroup(MathTex(r"T\ulcorner L \urcorner \vdash q", font_size=36), label(r"valid", font_size=24, color=OK)),
            VGroup(MathTex(r"\vdash q", font_size=36), label(r"\textit{not} valid", font_size=24, color=BAD)),
            VGroup(MathTex(r"\vdash A \vee \lnot A", font_size=36), label(r"valid: \ every classical law survives",
                                                                          font_size=24, color=OK)))
        for r in rows:
            r.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-1.0, -1.2, 0])
        moral = label(r"cut fails: \ two valid steps \ do not chain", font_size=26, color=GOAL).to_edge(DOWN, buff=0.4)
        moral.to_edge(RIGHT, buff=0.6)
        assert d["proves_L"] and d["L_entails_q"] and not d["proves_q"] and d["excluded_middle"]
        with self.voiceover(
            "Curry and the liar can also be blocked by giving up a structural rule that almost no one questions. "
            "<bookmark mark='a'/>In strict-tolerant logic, developed by Pablo Cobreros, Paul Égré, David Ripley and "
            "Robert van Rooij, first for vagueness, an argument is valid if, whenever its premises are strictly "
            "true, its conclusion is at least tolerantly true: true, or neither. <bookmark mark='b'/>The Reasoner "
            "checks it on the liar's fixed point. The liar is tolerantly true, so 'the liar is true' is a valid "
            "conclusion from nothing. The liar is never strictly true, so from it anything follows. "
            "<bookmark mark='c'/>But the conclusion 'q', from nothing, is not valid. Two valid steps do not chain: "
            "the rule of cut fails. <bookmark mark='d'/>And yet every classical law, excluded middle included, is "
            "valid in ST. The liar argument is stopped not by changing logic's laws, but by refusing to chain them "
            "through a paradoxical sentence."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(defn))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(moral))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def vcurry(self):
        hc = history_card(2013, r"Jc Beall \& Julien Murzi", r"`Two flavors of Curry's paradox'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        pi = label(r"$\pi$: \ the argument \ `$\pi$ is valid, \ therefore $q$'", font_size=30, color=SELF).move_to(
            [0, 1.6, 0])
        steps = VGroup(
            label(r"suppose $\pi$ is valid; \ its premise holds, \ so by its own validity, \ $q$", font_size=24),
            label(r"so the argument from `$\pi$ is valid' to $q$ is valid: \ that is, \ $\pi$ is valid", font_size=24),
            label(r"and so, \ applying $\pi$, \ $q$", font_size=24, color=BAD),
            label(r"no conditional at all: \ the fixes for Curry's conditional do not touch it", font_size=24,
                  color=GOAL),
            label(r"what it uses: \ the supposition twice, \ again: \ contraction", font_size=24,
                  color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pi, DOWN, buff=0.5)
        with self.voiceover(
            "Curry has a second flavour, which Jc Beall and Julien Murzi made famous in 2013. <bookmark mark='a'/>"
            "Take the argument pi: 'pi is valid, therefore the moon is cheese'. <bookmark mark='b'/>Suppose pi is "
            "valid. Its premise then holds, so by its own validity the moon is cheese. <bookmark mark='c'/>So the "
            "argument from 'pi is valid' to the cheese is valid: which is to say, pi is valid. And so, applying pi, "
            "the moon is cheese. <bookmark mark='d'/>No conditional appears anywhere, so the special conditionals "
            "of Field and Priest do not help. <bookmark mark='e'/>What the argument uses, once more, is the "
            "supposition twice. Contraction, or the transitivity of ST's last section, is where the remaining "
            "defences are dug."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(pi))
            for mk, st in zip("bcde", (steps[0], VGroup(steps[1], steps[2]), steps[3], steps[4])):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
        self.clear_scene()
