from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Superval(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Sharpenings and degrees", r"Can a vague word be true without a sharp line?",
                            lit=(1975,), part=PART)
        with self.voiceover("Chapter eleven. Sharpenings and degrees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sharpen()
        self.verdicts()
        self.price()
        self.degrees()

    def sharpen(self):
        d = load("superval")
        n = d["n"] + 1
        heads = men_row(d["bald"], width=12.2, r=0.22, y=1.0)
        idx = VGroup(*[MathTex(str(i), font_size=18, color=GREY_B).next_to(h, DOWN, buff=0.12) for i, h in
                       enumerate(heads)])
        step = 12.2 / (n - 1)
        x0 = -6.1
        pen = Rectangle(width=step * (d["hi"] - d["lo"]), height=1.3, stroke_width=0, fill_color=HALF,
                        fill_opacity=0.12).move_to([x0 + step * (d["lo"] + d["hi"]) / 2, 1.0, 0])
        pl = label(r"the penumbra: \ borderline cases", font_size=22, color=HALF).next_to(pen, UP, buff=0.12)
        hc = history_card(1975, r"Kit Fine", r"`Vagueness, truth and logic' \ (after Mehlberg 1958)", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        lines = VGroup()
        for k in range(d["lo"] + 1, d["hi"] + 1):
            x = x0 + step * (k - 0.5)
            lines.add(DashedLine([x, 1.75, 0], [x, 0.25, 0], color=CONN, stroke_width=2.5))
        sh = label(rf"{d['sharpenings']} admissible sharpenings: \ draw the line anywhere in the penumbra", font_size=24,
                   color=CONN).move_to([0, -0.4, 0])
        defs = VGroup(label(r"super-true: \ true on every admissible sharpening", font_size=26, color=OK),
                      label(r"super-false: \ false on every one", font_size=26, color=BAD),
                      label(r"otherwise: \ neither", font_size=26, color=HALF)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.18).move_to([0, -1.9, 0])
        with self.voiceover(
            "The first theory says: 'bald' has no single boundary, but it could be made sharp in many acceptable "
            "ways. <bookmark mark='a'/>Here are twenty-one men. The first seven are clearly bald, the last eight "
            "clearly not. Between them lies the penumbra, the borderline cases. <bookmark mark='b'/>A sharpening "
            "draws a line somewhere in the penumbra. Any such line is admissible; none is the right one. "
            "<bookmark mark='c'/>Kit Fine, in 1975, following Henryk Mehlberg, defined truth for a vague language as "
            "truth on every admissible sharpening: super-truth. A sentence is super-false if false on every one, "
            "and otherwise it is neither. This is supervaluationism."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.05), FadeIn(idx))
            self.play(FadeIn(pen), FadeIn(pl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.25), FadeIn(sh))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in defs], lag_ratio=0.3))
        self.clear_scene()

    def verdicts(self):
        d = load("superval")
        head = label(r"The supervaluationist's verdicts, \ computed on 21 men", font_size=30, color=CONN).to_edge(
            UP, buff=0.4)
        s1 = VGroup(label(r"`man $i$ is bald'", font_size=22, color=GREY_A), status_strip(d["bald"], width=8.4)
                    ).arrange(RIGHT, buff=0.3)
        s2 = VGroup(label(r"`if $i$ is bald, so is $i{+}1$'", font_size=22, color=GREY_A),
                    status_strip(d["conditionals"] + ["T"], width=8.4)).arrange(RIGHT, buff=0.3)
        s3 = VGroup(label(r"`$i$ is bald or not bald'", font_size=22, color=GREY_A), status_strip(d["lem"], width=8.4)
                    ).arrange(RIGHT, buff=0.3)
        strips = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=RIGHT, buff=0.35).next_to(head, DOWN, buff=0.5)
        s2[1][-1].set_opacity(0)
        cut = VGroup(MathTex(r"\exists i\, (B_i \land \lnot B_{i+1})", font_size=36, color=GOAL),
                     label(r"`there is a last bald man': \ super-true", font_size=24, color=OK)).arrange(RIGHT, buff=0.4)
        wit = label(r"yet for no particular $i$ is `$i$ is the last bald man' super-true", font_size=24, color=BAD)
        lem = label(r"excluded middle is super-true for everyone; \ bivalence fails in the penumbra", font_size=24,
                    color=GREY_A)
        low = VGroup(cut, wit, lem).arrange(DOWN, buff=0.25).next_to(strips, DOWN, buff=0.55)
        assert d["cutoff"] == "T" and d["no_witness"]
        with self.voiceover(
            "The Reasoner computes the verdicts. <bookmark mark='a'/>'Man i is bald' is super-true for the first "
            "seven, super-false for the last eight, and neither in between. <bookmark mark='b'/>Each tolerance "
            "conditional is super-true outside the penumbra. Inside it, each one fails on exactly one sharpening, "
            "the one that draws its line there, so none of them is super-true. Tolerance, as a universal claim, "
            "is rejected. <bookmark mark='c'/>'Man i is bald or not bald' is super-true for everyone: on every "
            "sharpening, one disjunct holds. <bookmark mark='d'/>And here is the strange verdict: 'there is a last "
            "bald man' is super-true, because every sharpening has one. <bookmark mark='e'/>Yet for no particular "
            "man is it super-true that he is the last. <bookmark mark='f'/>Excluded middle survives; bivalence, "
            "the claim that each sentence is true or false, does not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(s1))
            vo.wait_until("b")
            self.play(FadeIn(s2))
            vo.wait_until("c")
            self.play(FadeIn(s3))
            vo.wait_until("d")
            self.play(FadeIn(cut))
            vo.wait_until("e")
            self.play(FadeIn(wit))
            vo.wait_until("f")
            self.play(FadeIn(lem))
        self.clear_scene()

    def price(self):
        head = label(r"The price of super-truth", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"$\exists i\, \varphi(i)$ true, \ every instance $\varphi(i)$ untrue: \ a strange existential",
                  font_size=26),
            label(r"`it is true that $p$ or $q$' \ without `it is true that $p$' or `it is true that $q$'",
                  font_size=26),
            label(r"classical theorems, \ but not classical rules: \ with `definitely', \ conditional proof and "
                  r"contraposition fail \ (Williamson 1994)", font_size=26),
            label(r"and the penumbra's own edges are sharp: \ exactly where does it begin? \ (Chapter 13)",
                  font_size=26, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Supervaluationism keeps every classical law, but it pays. <bookmark mark='a'/>It says there is a last "
            "bald man, while denying of each man that he is the one. <bookmark mark='b'/>So a disjunction can be "
            "true without any disjunct being true, which is not how 'or' seems to work. <bookmark mark='c'/>It "
            "keeps the classical theorems, but not all the classical rules. Timothy Williamson showed that once "
            "you add an operator for 'definitely', familiar steps such as conditional proof and contraposition "
            "fail. <bookmark mark='d'/>And the penumbra itself has sharp edges in this model. Where exactly do the "
            "borderline cases begin? That is the problem of Chapter 13."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def degrees(self):
        d = load("degrees")
        n = len(d["degrees"])
        G = axes([0, n - 1], [0, 1.05], x_length=8.6, y_length=3.6, xticks=[0, 30, 70, 100], yticks=[0, 0.5, 1],
                 xlabel=r"man $i$ \ (hundreds of hairs)", center=[-1.6, -0.2, 0])
        ax = G.ax
        xs = list(range(n))
        deg = VMobject(stroke_color=OK, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in
                                                                                zip(xs, d["degrees"])])
        cond = VMobject(stroke_color=CONN, stroke_width=3).set_points_as_corners(
            [ax.c2p(x + 0.5, y) for x, y in zip(xs[:-1], d["conditionals"])])
        mp = VMobject(stroke_color=BAD, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in
                                                                               zip(xs, d["mp_bound"])])
        leg = legend([(OK, r"degree of `man $i$ is bald'"), (CONN, r"degree of `if $i$, then $i{+}1$'"),
                      (BAD, r"what chained modus ponens guarantees")], font_size=22).move_to([4.6, 1.8, 0])
        eq = MathTex(r"v(B) \ \ge\ v(A) + v(A \to B) - 1", font_size=32, color=GREY_A).move_to([4.4, 0.0, 0])
        cap = label(rf"every conditional has degree $\ge {d['min_conditional']:.3f}$: \ nearly true; \ the guarantee "
                    rf"is used up by man {d['exhausted_at']}", font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        obj = VGroup(label(r"but why 0.975, \ and not 0.974?", font_size=22, color=BAD),
                     label(r"the objection of artificial precision", font_size=22, color=BAD)).arrange(
            DOWN, buff=0.1).move_to([4.4, -1.1, 0])
        with self.voiceover(
            "The second theory takes degrees seriously. <bookmark mark='a'/>Being bald is a matter of degree: one, "
            "for the first thirty men; zero, from man seventy; and falling steadily in between. "
            "<bookmark mark='b'/>Then each tolerance conditional, in Łukasiewicz's logic, has degree at least "
            f"{d['min_conditional']:.3f}. Tolerance is not true, but very nearly true, and that explains its pull. "
            "<bookmark mark='c'/>And the argument? In this logic, modus ponens guarantees only that the conclusion's "
            "degree is at least the premises' degrees added, minus one. <bookmark mark='d'/>Each step loses a "
            f"little, and by man {d['exhausted_at']} the guarantee is gone. The sorites is an argument whose "
            "premises are almost true and whose small losses add up. <bookmark mark='e'/>The standard objection: "
            "why should the degree of 'bald' be exactly this number, and not one slightly different? Degrees "
            "replace one sharp line with infinitely many."
        ) as vo:
            self.play(FadeIn(G), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(deg), run_time=2)
            vo.wait_until("b")
            self.play(Create(cond), FadeIn(leg[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(eq))
            vo.wait_until("d")
            self.play(Create(mp), FadeIn(leg[2]), run_time=2.5)
            self.play(FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(obj))
        self.clear_scene()
