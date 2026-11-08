from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403


def text_arg(prem, concl, width=7.2, font_size=30, color=WHITE):
    rows = VGroup(*[label(p, font_size=font_size, color=color) for p in prem])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    bar = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_B)
    c = label(rf"So {concl[0].lower()}{concl[1:]}", font_size=font_size, color=GOAL)
    g = VGroup(rows, bar, c).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    bar.align_to(rows, LEFT)
    g.rows, g.bar, g.concl = rows, bar, c
    return g


class Argument(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"What an argument is", r"When does a conclusion follow?", part=PART)
        with self.voiceover("Chapter two. What an argument is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.parts()
        self.validity()
        self.form()
        self.peirce()

    def parts(self):
        d = load("forms")["forms"]
        a = text_arg(d[0]["premises"], d[0]["conclusion"]).move_to([-1.7, 0.6, 0])
        pl = brace_note(a.rows, r"premises", direction=LEFT, color=P.CLAIM)
        cl = brace_note(a.concl, r"conclusion", direction=LEFT, color=GOAL)
        dfn = definition_card(r"Argument", r"a set of premises offered in support of a conclusion", width=5.4,
                              font_size=24).to_corner(UR, buff=0.4)
        with self.voiceover(
            "An argument is a set of claims, the premises, offered in support of another claim, the conclusion. "
            "<bookmark mark='a'/>All humans are mortals; all Greeks are humans; so all Greeks are mortals. "
            "<bookmark mark='b'/>These are the premises. <bookmark mark='c'/>That is the conclusion. An argument can "
            "fail in two quite different ways, and the whole of logic rests on keeping them apart."
        ) as vo:
            self.play(FadeIn(dfn))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeIn(cl))
        self.clear_scene()

    def validity(self):
        d = load("forms")["forms"]
        a = text_arg(d[1]["premises"], d[1]["conclusion"], font_size=28).move_to([-3.2, 1.0, 0])
        assert d[1]["valid"]
        v = definition_card(r"Valid", r"it is impossible for the premises to be true and the conclusion false",
                            width=6.0, font_size=23, color=OK).move_to([3.4, 1.6, 0])
        s = definition_card(r"Sound", r"valid, and the premises are in fact true", width=6.0, font_size=23,
                            color=P.WORLD).next_to(v, DOWN, buff=0.3)
        tick = label(r"valid \ $\checkmark$", font_size=30, color=OK).next_to(a, DOWN, buff=0.35).align_to(a, LEFT)
        cross = label(r"not sound: \ whales are not fish", font_size=28, color=BAD).next_to(tick, DOWN, buff=0.2)
        cross.align_to(tick, LEFT)
        grid = VGroup(
            label(r"true premises, \ true conclusion: \ valid or not", font_size=24),
            label(r"true premises, \ false conclusion: \ \textbf{never} valid", font_size=24, color=BAD),
            label(r"false premises: \ anything goes", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grid.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "First failure: the premises might be false. Second: even if they were true, the conclusion might not "
            "follow. Logic is about the second. <bookmark mark='a'/>An argument is valid if it is impossible for the "
            "premises to be true and the conclusion false. <bookmark mark='b'/>It is sound if, in addition, its "
            "premises really are true. <bookmark mark='c'/>So here is a valid argument with a false conclusion. All "
            "fish are things with gills; all whales are fish; so all whales are things with gills. "
            "<bookmark mark='d'/>The form is "
            "flawless; a premise is false. Valid, but not sound. <bookmark mark='e'/>Validity only ever rules out "
            "one combination: true premises with a false conclusion."
        ) as vo:
            self.play(FadeIn(v, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(Indicate(v, color=OK))
            vo.wait_until("b")
            self.play(FadeIn(s, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(a))
            vo.wait_until("d")
            self.play(FadeIn(tick), FadeIn(cross))
            vo.wait_until("e")
            self.play(FadeIn(grid))
        self.clear_scene()

    def form(self):
        d = load("forms")["forms"]
        good = text_arg(d[0]["premises"], d[0]["conclusion"], font_size=26, width=6.0)
        bad = text_arg(d[2]["premises"], d[2]["conclusion"], font_size=26, width=6.0)
        assert not d[2]["valid"]
        good.move_to([-3.4, 1.4, 0])
        bad.move_to([3.4, 1.4, 0])
        sg = MathTex(r"\text{All } M \text{ are } P;\ \text{all } S \text{ are } M;\ \text{so all } S \text{ are } P",
                     font_size=30, color=OK).next_to(good, DOWN, buff=0.5)
        sb = MathTex(r"\text{All } P \text{ are } M;\ \text{all } S \text{ are } M;\ \text{so all } S \text{ are } P",
                     font_size=30, color=BAD).next_to(bad, DOWN, buff=0.5)
        for form in (sg, sb):
            if form.width > 6.0:
                form.scale_to_fit_width(6.0)
        cm = label(r"same form as: \ all cats are mortals; all dogs are mortals; so all dogs are cats", font_size=24,
                   color=BAD).to_edge(DOWN, buff=1.2)
        rule = label(r"to refute a form: \ one instance with true premises and a false conclusion", font_size=28,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "What makes an argument valid is its form, not its subject matter. <bookmark mark='a'/>Replace the words "
            "with letters, and Greeks, humans and mortals become S, M and P. Every argument of that shape is valid, "
            "about anything at all. <bookmark mark='b'/>Now a shape that looks similar: all P are M; all S are M; "
            "so all S are P. <bookmark mark='c'/>To show a form is invalid, one instance is enough: all cats are "
            "mortal, all dogs are mortal, so all dogs are cats. True premises, false conclusion. "
            "<bookmark mark='d'/>This is the oldest method in logic, the counterexample. And because validity "
            "depends only on form, it can, in principle, be checked without understanding the words at all. That "
            "is the first step toward Leibniz's machine."
        ) as vo:
            self.play(FadeIn(good))
            vo.wait_until("a")
            self.play(Write(sg))
            vo.wait_until("b")
            self.play(FadeIn(bad), Write(sb))
            vo.wait_until("c")
            self.play(FadeIn(cm))
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.clear_scene()

    def peirce(self):
        hc = history_card(1878, r"Charles Sanders Peirce", r"`Deduction, Induction, and Hypothesis'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.4)
        R = label(r"Rule: \ all the beans from this bag are white", font_size=26, color=P.CLAIM)
        Cc = label(r"Case: \ these beans are from this bag", font_size=26, color=P.AGENT)
        Rs = label(r"Result: \ these beans are white", font_size=26, color=P.TRUE)
        props = VGroup(R, Cc, Rs).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hc, DOWN, buff=0.4)
        props.align_to(hc, LEFT)
        rows = VGroup(
            label(r"deduction: \ Rule + Case $\Rightarrow$ Result \quad (certain)", font_size=26, color=OK),
            label(r"induction: \ Case + Result $\Rightarrow$ Rule \quad (may fail)", font_size=26, color=GOAL),
            label(r"abduction: \ Rule + Result $\Rightarrow$ Case \quad (may fail)", font_size=26, color=P.AGENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.4, -0.4, 0])
        fwd = label(r"deduction: Parts 1--9; \ induction: Part 15; \ abduction: Part 18", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Validity is not the only way premises can support a conclusion. In 1878 Charles Sanders Peirce showed "
            "three kinds of inference with one bag of beans. <bookmark mark='a'/>Take three statements. The rule: all "
            "the beans from this bag are white. The case: these beans are from this bag. The result: these beans are "
            "white. <bookmark mark='b'/>From the rule and the case, the result follows necessarily: that is "
            "deduction. <bookmark mark='c'/>From the case and the result, you might generalize to the rule: "
            "induction, which can fail. <bookmark mark='d'/>From the rule and the result, you might guess the case, "
            "that the beans came from this bag: abduction, inference to an explanation, which can fail too. "
            "<bookmark mark='e'/>Deduction preserves truth; induction and abduction extend what we know, at a risk. "
            "The first parts of this series are about deduction; induction gets Part 15, and abduction runs through "
            "Part 18, on science."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in props], lag_ratio=0.3))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(fwd))
        self.clear_scene()
