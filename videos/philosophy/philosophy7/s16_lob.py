from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Lob(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Löb's theorem", r"What does arithmetic believe about itself?", lit=(1955,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Löb's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.henkin()
        self.proof()
        self.fixed()

    def henkin(self):
        hc = history_card(1952, r"Leon Henkin", r"a question in the \textit{Journal of Symbolic Logic}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        h = MathTex(r"H \ \leftrightarrow\ \mathrm{Prov}(\ulcorner H \urcorner)", font_size=52, color=SELF).move_to(
            [0, 1.2, 0])
        cap = label(r"$H$ says: \ `I am provable'. \ \ Is it?", font_size=30, color=GOAL).next_to(h, DOWN, buff=0.4)
        two = VGroup(label(r"if provable, \ then true: \ consistent with itself", font_size=24, color=GREY_A),
                     label(r"if unprovable, \ then false: \ also consistent", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.2).next_to(cap, DOWN, buff=0.45)
        ans = VGroup(history_card(1955, r"Martin Löb", r"`Solution of a problem of Leon Henkin': \ $H$ is provable",
                                  width=6.4, color=HIST)).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Gödel's sentence says 'I am not provable'. In 1952 Leon Henkin asked about its opposite. "
            "<bookmark mark='a'/>Take a sentence H that says 'I am provable'. Is H provable? "
            "<bookmark mark='b'/>Either answer looks consistent. If H is provable, it is true; if it is not, it is "
            "false. Nothing seems to decide. <bookmark mark='c'/>In 1955 Martin Löb answered: H is provable. And he "
            "proved much more."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(h), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(two))
            vo.wait_until("c")
            self.play(FadeIn(ans))
        self.clear_scene()

    def proof(self):
        thm = theorem_card(r"Löb's theorem", r"if \ $\mathrm{PA} \vdash \Box A \to A$, \ then \ $\mathrm{PA} \vdash A$",
                           width=7.6, font_size=28).to_corner(UL, buff=0.35)
        steps = [(r"L \leftrightarrow (\Box L \to A)", r"diagonal lemma"),
                 (r"\Box L \to \Box(\Box L \to A)", r"D1, D2"),
                 (r"\Box L \to (\Box\Box L \to \Box A)", r"D2"),
                 (r"\Box L \to \Box\Box L", r"D3"),
                 (r"\Box L \to \Box A", r"from the last two"),
                 (r"\Box L \to A", r"with $\Box A \to A$, \ the hypothesis"),
                 (r"L", r"by the first line"),
                 (r"\Box L", r"D1"),
                 (r"A", r"from the last three")]
        rows = VGroup()
        for i, (f, why) in enumerate(steps):
            y = 2.0 - 0.56 * i
            n = label(rf"{i + 1}.", font_size=22, color=GREY_B).move_to([-0.3, y, 0])
            m = MathTex(f, font_size=32, color=GOAL if i == len(steps) - 1 else WHITE).move_to([0.15, y, 0],
                                                                                              aligned_edge=LEFT)
            w = label(why, font_size=20, color=NUM).move_to([3.7, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(n, m, w))
        side = VGroup(label(r"$\Box$ \ = \ `PA proves'", font_size=24, color=PROV),
                      label(r"with $A = \bot$: \ $\Box\bot \to \bot$ is consistency,", font_size=22),
                      label(r"so Löb gives Gödel II", font_size=22, color=OK),
                      label(r"with $A = H$: \ $\Box H \to H$ holds, \ so $H$ is provable", font_size=22,
                            color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(thm, DOWN, buff=0.5).align_to(
            thm, LEFT)
        with self.voiceover(
            "Löb's theorem: if PA proves 'if A is provable, then A', then PA proves A. <bookmark mark='a'/>The proof "
            "is nine lines, using the three derivability conditions. First, the diagonal lemma gives a sentence L "
            "that says: if I am provable, then A. <bookmark mark='b'/>Apply the conditions: if L is provable, then "
            "so is 'if L is provable then A', and so, since provable things are provably provable, A is provable. "
            "<bookmark mark='c'/>Now use the hypothesis that provability of A gives A: if L is provable, then A. "
            "But that is L itself. So L is proved, hence provable, hence A. <bookmark mark='d'/>Take A to be a "
            "contradiction, and Löb's theorem is Gödel's second theorem. Take A to be Henkin's sentence, and it "
            "answers Henkin: H is provable. PA believes 'if I prove A, then A' only for the A it already proves."
        ) as vo:
            self.play(FadeIn(thm), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[1:5]], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[5:]], lag_ratio=0.4), run_time=4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s) for s in side[1:]], lag_ratio=0.4))
        self.clear_scene()

    def fixed(self):
        d = load("gl")
        head = label(r"The fixed points of provability logic", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"Gödel: \ $p \leftrightarrow \lnot\Box p$", r"p := \lnot\Box\bot", r"`I am unprovable' is "
                 r"equivalent to `PA is consistent'", "godel_fixed"),
                (r"Henkin: \ $p \leftrightarrow \Box p$", r"p := \top", r"`I am provable' is equivalent to a "
                 r"tautology", "henkin_fixed"),
                (r"uniqueness", r"\boxdot(p \leftrightarrow \lnot\Box p) \wedge \boxdot(q \leftrightarrow \lnot\Box q) "
                 r"\to (p \leftrightarrow q)", r"any two Gödel sentences are equivalent \ ($\boxdot$: \ true and "
                 r"provable)", "unique")]
        tab = VGroup()
        for i, (a, b, c, k) in enumerate(rows):
            y = 1.5 - 1.15 * i
            la = label(a, font_size=26, color=SELF).move_to([-6.3, y + 0.2, 0], aligned_edge=LEFT)
            lb = MathTex(b, font_size=30, color=GOAL).move_to([-1.6, y + 0.2, 0], aligned_edge=LEFT)
            lc = label(c, font_size=22, color=GREY_A).move_to([-6.3, y - 0.3, 0], aligned_edge=LEFT)
            ok = label(r"$\checkmark$", font_size=30, color=OK).move_to([5.8, y + 0.2, 0])
            assert d[k]["valid"]
            tab.add(VGroup(la, lb, lc, ok))
        chk = label(rf"the Reasoner checks each on all {d['godel_fixed']['frames']} finite GL frames up to four "
                    rf"worlds", font_size=22, color=OK).to_edge(DOWN, buff=1.0)
        sol = label(r"de Jongh and Sambin (1975): \ every such equation has a unique solution; \ Solovay (1976): \ "
                    r"GL is exactly PA's logic of proof", font_size=22, color=GREY_A).next_to(chk, DOWN, buff=0.2)
        with self.voiceover(
            "Provability logic, the GL of Part 4, now pays off. <bookmark mark='a'/>Gödel's sentence is a fixed "
            "point: p if and only if not box p. GL solves it. The solution is not box falsum: Gödel's sentence is "
            "equivalent to the statement that PA is consistent. <bookmark mark='b'/>Henkin's sentence, p if and "
            "only if box p, has the solution truth itself: it is equivalent to a tautology, which is why it is "
            "provable. <bookmark mark='c'/>And the solutions are unique: any two Gödel sentences are provably "
            "equivalent. <bookmark mark='d'/>The Reasoner checks each of these on all two hundred and forty-two "
            "finite GL frames with up to four worlds. Dick de Jongh and Giovanni Sambin proved that every such "
            "equation has a unique solution, and Robert Solovay that GL captures exactly what PA can prove about "
            "its own provability."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(chk), FadeIn(sol))
        self.clear_scene()
