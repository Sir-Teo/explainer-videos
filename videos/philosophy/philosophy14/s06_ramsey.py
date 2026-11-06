from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

DET = {"b~m": r"\text{butler}", "bm": r"\text{both}", "~bm": r"\text{maid}", "~b~m": r"\text{neither}"}


class Ramsey(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"If", r"What does a conditional say?", lit=(1929, 1968), part=PART)
        with self.voiceover("Chapter five. If."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.material()
        self.strict()
        self.oswald()
        self.test()

    def material(self):
        head = label(r"The material conditional", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"A", r"C", r"A \to C"]
        rows = [[True, True, True], [True, False, False], [False, True, True], [False, False, True]]
        grid = ValueGrid(hd, rows, col_w=[1.2, 1.2, 1.8], cell_h=0.55, font_size=28).move_to([-4.0, 0.2, 0])
        para = stack([
            (r"false only when $A$ is true and $C$ false", WHITE),
            (r"`if the moon is made of cheese, \ then $2 + 2 = 5$': \ true", BAD),
            (r"`if I win the lottery, \ I'll be poor': \ true, \ if I don't win", BAD),
            (r"$\lnot(A \to C) \vDash A$: \ deny `if God exists, prayers are answered', \ and you've proved God "
             r"exists", BAD),
            (r"logic's `if' \ is not quite our `if'", GOAL),
        ], font_size=22, aligned_edge=LEFT, width=7.6).move_to([2.6, 0.0, 0])
        with self.voiceover(
            "Logic's own conditional is the material conditional. <bookmark mark='a'/>It is false only when the "
            "antecedent is true and the consequent false, and true in every other row. <bookmark mark='b'/>So, if the "
            "moon is made of cheese, two plus two is five: true, because the moon isn't. <bookmark mark='c'/>If I win "
            "the lottery, I'll be poor: true, as long as I don't win. <bookmark mark='d'/>Worse: denying a material "
            "conditional commits you to its antecedent. Deny that if God exists, prayers are answered, and you have "
            "proved that God exists. <bookmark mark='e'/>These are the paradoxes of material implication. Logic's "
            "`if' is not quite ours."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid))
            for mk, r in zip("bcde", para[1:]):
                vo.wait_until(mk)
                if mk == "b":
                    self.play(FadeIn(para[0]))
                self.play(FadeIn(r))
        self.clear_scene()

    def strict(self):
        head = label(r"Two repairs from logic itself", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(label(r"the strict conditional \ (C.\ I.\ Lewis, \ 1912)", font_size=24, color=BEL),
                      MathTex(r"\Box(A \to C)", font_size=36),
                      label(r"no world where $A$ and not $C$: \ Part 4", font_size=20, color=GREY_A),
                      label(r"but: \ an impossible $A$ strictly implies everything", font_size=20, color=BAD)).arrange(
            DOWN, buff=0.2)
        right = VGroup(label(r"the relevant conditional \ (Anderson and Belnap)", font_size=24, color=BEL),
                       MathTex(r"A \to C \text{ needs } A \text{ and } C \text{ to share content}", font_size=28),
                       label(r"no `cheese, \ so $2 + 2 = 5$': \ Part 5", font_size=20, color=GREY_A),
                       label(r"but: \ still no account of `if Oswald didn't\dots'", font_size=20, color=BAD)).arrange(
            DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(head, DOWN, buff=0.7)
        foot = label(r"both fix the logic; \ neither captures how `if' depends on what we know", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Logic has offered two repairs, met earlier in the series. <bookmark mark='a'/>C. I. Lewis's strict "
            "conditional, from Part 4: necessarily, if A then C. No world has A without C. But an impossible "
            "antecedent strictly implies everything. <bookmark mark='b'/>And the relevant conditional of Alan "
            "Anderson and Nuel Belnap, from Part 5, which demands that antecedent and consequent share content, and so "
            "rejects the cheese and the arithmetic. <bookmark mark='c'/>Both improve the logic. Neither explains how "
            "if depends on what we know, which is where the rest of this part looks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def oswald(self):
        hc = history_card(1970, r"Ernest Adams", r"`Subjunctive and Indicative Conditionals'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        ind = VGroup(label(r"indicative", font_size=24, color=NEW),
                     label(r"`If Oswald didn't kill Kennedy, \ someone else did.'", font_size=24),
                     label(r"true: \ Kennedy was killed by someone", font_size=20, color=OK)).arrange(DOWN, buff=0.2)
        sub = VGroup(label(r"subjunctive \ (counterfactual)", font_size=24, color=BEL),
                     label(r"`If Oswald hadn't killed Kennedy, \ someone else would have.'", font_size=24),
                     label(r"probably false: \ no second gunman was waiting", font_size=20, color=BAD)).arrange(
            DOWN, buff=0.2)
        VGroup(ind, sub).arrange(DOWN, buff=0.7).next_to(hc, DOWN, buff=0.6).set_x(0)
        foot = label(r"same antecedent, \ same consequent, \ different truth values: \ two kinds of `if'",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Ernest Adams pointed out that English has at least two conditionals. <bookmark mark='a'/>If Oswald didn't "
            "kill Kennedy, someone else did. True: Kennedy was killed by someone. <bookmark mark='b'/>If Oswald hadn't "
            "killed Kennedy, someone else would have. Probably false, unless there was a second gunman waiting. "
            "<bookmark mark='c'/>Same antecedent, same consequent, different truth values. The first, the indicative, "
            "is about how things are, given what we know. The second, the counterfactual, is about how things would "
            "have been. Chapters seven and eight take them in turn."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ind))
            vo.wait_until("b")
            self.play(FadeIn(sub))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def test(self):
        d = load("moves")
        q = quote_card(r"If two people are arguing `If p will q?' and are both in doubt as to p, they are adding p "
                       r"hypothetically to their stock of knowledge and arguing on that basis about q.",
                       r"Frank Ramsey", r"`General Propositions and Causality' \ (1929)", width=11.0,
                       font_size=24).to_edge(UP, buff=0.4)
        rt = MathTex(r"A > C \in K \iff C \in K * A", font_size=40, color=NEW).next_to(q, DOWN, buff=0.45)
        rl = label(r"the Ramsey test \ (Stalnaker, \ 1968; \ Gärdenfors)", font_size=22, color=GREY_A).next_to(
            rt, DOWN, buff=0.15)
        sp = SphereView(d["rank"], center=[-3.6, -2.0, 0], step=0.62, names=DET, font_size=16, dot_r=0.08,
                        angles={"b~m": PI, "bm": 0.0, "~bm": PI / 2, "~b~m": -PI / 2})
        rows = stack([
            (r"`if the butler didn't do it, \ the maid did'", WHITE),
            (r"revise by $\lnot b$: \ the nearest world is the maid's", NEW),
            (r"so the detective believes the conditional", OK),
            (r"conditionals read off the spheres: \ belief revision as a semantics for `if'", GOAL),
        ], font_size=22, aligned_edge=LEFT, width=7.0).move_to([2.6, -2.0, 0])
        with self.voiceover(
            "Frank Ramsey, in 1929, gave a test for conditionals that has shaped everything since. "
            "<bookmark mark='a'/>To decide whether if p, then q, add p hypothetically to what you know, and see whether "
            "q follows. <bookmark mark='b'/>Robert Stalnaker and then Gärdenfors made it a principle: you believe if A "
            "then C exactly when revising by A would bring you to believe C. <bookmark mark='c'/>Take the detective. "
            "If the butler didn't do it, the maid did? <bookmark mark='d'/>Revise by the butler's innocence: the "
            "nearest such world is the maid's. <bookmark mark='e'/>So she believes the conditional. "
            "<bookmark mark='f'/>The Ramsey test turns belief revision into a semantics for conditionals. It seems "
            "obviously right. The next chapter shows that, combined with the AGM postulates, it is impossible."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(Indicate(q, color=NEW, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Write(rt), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(sp), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), *sp.paint(d["revise ~b"], NEW), Create(sp.halo(d["revise ~b"])))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
