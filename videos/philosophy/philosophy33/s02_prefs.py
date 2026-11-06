from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Preferences(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Preferences", r"What must a rational agent's preferences be like?", lit=(1944,),
                            part=PART)
        with self.voiceover("Chapter one. Preferences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.parity()
        self.pump()
        self.ordinal()
        self.revealed()

    def axioms(self):
        head = label(r"Two conditions on preference", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"\text{completeness:}\quad A \succeq B \;\;\text{or}\;\; B \succeq A", font_size=34, color=PREF)
        f2 = MathTex(r"\text{transitivity:}\quad A \succeq B,\; B \succeq C \;\Rightarrow\; A \succeq C", font_size=34,
                     color=PREF)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0, 0.8, 0])
        rows = stack([(r"$\succeq$: \ `at least as good as', \ revealed in choice", GREY_A),
                      (r"completeness can fail for incommensurable options: \ a career against a family", RISK),
                      (r"transitivity is the one almost everyone defends: \ the next section shows why", GOAL)],
                     font_size=20, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Decision theory starts from preferences between options. <bookmark mark='a'/>Completeness: for any two "
            "options, you weakly prefer one to the other. <bookmark mark='b'/>Transitivity: if you weakly prefer A to "
            "B, and B to C, you weakly prefer A to C. <bookmark mark='c'/>The symbol means at least as good as, and "
            "economists read it off choices. <bookmark mark='d'/>Completeness can fail when options are "
            "incommensurable, a career against a family, and some philosophers think rationality does not require it. "
            "<bookmark mark='e'/>Transitivity is the one almost everyone defends, for a reason the next section "
            "builds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pump(self):
        d = load("pump")
        head = label(r"A money pump, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["trades"] == 15 and d["paid"] == 0.15 and d["holding"] == "A"
        pos = {"A": [-3.0, 1.2, 0], "B": [-1.2, -1.6, 0], "C": [-4.8, -1.6, 0]}
        nodes = {k: VGroup(Circle(radius=0.45, color=PREF, fill_opacity=0.12), label(k, font_size=26, color=PREF)
                           ).move_to(p) for k, p in pos.items()}
        arr = VGroup()
        for a, b in (("A", "B"), ("B", "C"), ("C", "A")):
            v = np.array(pos[b]) - np.array(pos[a])
            v = v / np.linalg.norm(v)
            arr.add(Arrow(np.array(pos[a]) + v * 0.5, np.array(pos[b]) - v * 0.5, buff=0, color=GREY_B))
        al = label(r"arrow: \ strictly prefers the tail to the head", font_size=16, color=GREY_A).next_to(
            VGroup(*nodes.values()), DOWN, buff=0.35)
        token = Dot(pos["A"], radius=0.14, color=MONEY)
        ledger = VGroup(label(r"paid", font_size=20, color=MONEY), DecimalNumber(0, num_decimal_places=2,
                                                                                    font_size=36, color=MONEY))
        ledger.arrange(RIGHT, buff=0.3).move_to([3.4, 1.2, 0])
        rows = stack([(r"prefers A to B, \ B to C, \ C to A", GREY_A),
                      (r"holding A, \ pays a cent to swap for C, \ then B, \ then A again", RISK),
                      (r"five times round: \ 15 trades, \ 15 cents, \ and back where it started", BAD),
                      (r"cyclic preferences can be exploited without limit", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=5.6, buff=0.3).move_to([3.4, -1.1, 0])
        with self.voiceover(
            "Here is the argument for transitivity, in its classic form. <bookmark mark='a'/>An agent strictly "
            "prefers A to B, B to C, and C to A: a cycle. <bookmark mark='b'/>It holds A. Offer it C for A and a cent: "
            "it prefers C, so it pays. Offer B for C and a cent: it pays again. Offer A for B and a cent: it pays, and "
            "holds A once more. <bookmark mark='c'/>The Reasoner runs the pump five times round: fifteen trades, "
            "fifteen cents, and the agent is back where it started, poorer. <bookmark mark='d'/>An agent with "
            "cyclic preferences can be exploited without limit. Whether that shows such preferences irrational, "
            "or only imprudent in markets, is itself debated."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(arr), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(token), FadeIn(ledger), FadeIn(rows[1]))
            for k, (_, offer, paid) in enumerate(d["log"][:3]):
                self.play(token.animate.move_to(pos[offer]), ledger[1].animate.set_value(paid), run_time=0.8)
            vo.wait_until("c")
            for _, offer, paid in d["log"][3:6]:
                self.play(token.animate.move_to(pos[offer]), ledger[1].animate.set_value(paid), run_time=0.4)
            self.play(ledger[1].animate.set_value(d["paid"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ordinal(self):
        head = label(r"From preference to utility", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"A \succeq B \;\iff\; u(A) \ge u(B)", font_size=40, color=PREF).move_to([0, 1.4, 0])
        rows = stack([(r"complete and transitive preferences over finitely many options have such a $u$", GREY_A),
                      (r"but only an ordinal one: \ any increasing transform of $u$ will do", RISK),
                      (r"to say how much better, \ and to handle risk, \ we need more: \ lotteries", GOAL)],
                     font_size=21, buff=0.3).move_to([0, -0.8, 0])
        with self.voiceover(
            "Preferences that are complete and transitive can be represented by numbers. <bookmark mark='a'/>Over "
            "finitely many options there is a utility function u such that you weakly prefer A to B exactly when "
            "u of A is at least u of B. <bookmark mark='b'/>But it is only ordinal: it records the order and nothing "
            "else, so any increasing transformation of it would serve as well. <bookmark mark='c'/>To say how much "
            "better one option is than another, and to choose under risk, we need preferences over gambles."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def parity(self):
        head = label(r"Can completeness fail? \ The small-improvement argument", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        a = VGroup(RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=AGENT, fill_opacity=0.1),
                   label(r"$A$: \ a career as a lawyer", font_size=20, color=AGENT)).move_to([-4.0, 1.0, 0])
        a[1].move_to(a[0])
        b = VGroup(RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=PREF, fill_opacity=0.1),
                   label(r"$B$: \ a career as a clarinettist", font_size=20, color=PREF)).move_to([4.0, 1.0, 0])
        b[1].move_to(b[0])
        b2 = VGroup(RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=MONEY, fill_opacity=0.1),
                    label(r"$B^+$: \ $B$ plus \$1,000 a year", font_size=20, color=MONEY)).move_to([4.0, -1.0, 0])
        b2[1].move_to(b2[0])
        r1 = MathTex(r"A \not\succ B, \quad B \not\succ A", font_size=30, color=GREY_A).move_to([0, 1.0, 0])
        r2 = MathTex(r"B^+ \succ B", font_size=28, color=OK).move_to([4.0, 0.0, 0])
        r3 = MathTex(r"A \not\succ B^+, \quad B^+ \not\succ A", font_size=30, color=GREY_A).move_to([-0.3, -1.0,
                                                                                                         0])
        rows = stack([(r"if $A \sim B$, \ then $B^+ \succ A$ by transitivity: \ it is not; \ so not $A \sim B$",
                       BAD),
                      (r"neither better, \ nor worse, \ nor equal: \ incomparable \ (de Sousa, \ 1974), \ or "
                       r"`on a par' \ (Chang, \ 2002)", GOAL),
                      (r"rational choice without completeness: \ Aumann \ (1962); \ choice among the undominated",
                       HIST)], font_size=19, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Consider completeness first. <bookmark mark='a'/>Suppose you must choose between a career in law and a "
            "career as a clarinettist, and on reflection neither seems better than the other. "
            "<bookmark mark='b'/>Now improve the second slightly: the same musical career, with a thousand dollars "
            "more a year. It is better than the original, <bookmark mark='c'/>but it still does not seem better than "
            "the law. <bookmark mark='d'/>If the two careers had been exactly equal in value, the small improvement "
            "should have tipped the balance. It does not, so they were not equal. <bookmark mark='e'/>Neither better, "
            "nor worse, nor equal: Ronald de Sousa called such options incomparable, and Ruth Chang argues that "
            "they are on a par, a fourth relation. <bookmark mark='f'/>Robert Aumann showed in 1962 that expected "
            "utility can be rebuilt without completeness, at the cost of a set of utility functions rather than "
            "one, and a rule that only says which options are not beaten."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b))
            self.play(Write(r1))
            vo.wait_until("b")
            self.play(FadeIn(b2))
            self.play(Write(r2))
            vo.wait_until("c")
            self.play(Write(r3))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def revealed(self):
        d = load("revealed")
        head = label(r"Rationality tested on data: \ revealed preference", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        bad = d["inconsistent"]
        assert d["consistent"]["garp"] and not bad["garp"] and bad["ccei"] == 0.9167
        assert [(o["spent"], o["other_costs"]) for o in bad["obs"]] == [(6.0, 5.5), (8.0, 6.0)]
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-3.6, -0.6, 0])
        xl = label(r"good 1", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"good 2", font_size=16, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        (p1, x1), (p2, x2) = [(o["prices"], o["bundle"]) for o in bad["obs"]]
        m1, m2 = bad["obs"][0]["spent"], bad["obs"][1]["spent"]
        b1 = Line(ax.c2p(m1 / p1[0], 0), ax.c2p(0, m1 / p1[1]), color=EVID, stroke_width=3)
        b2 = Line(ax.c2p(m2 / p2[0], 0), ax.c2p(0, min(m2 / p2[1], 6)), color=RISK, stroke_width=3)
        if m2 / p2[1] > 6:
            b2 = Line(ax.c2p(m2 / p2[0], 0), ax.c2p((m2 - 6 * p2[1]) / p2[0], 6), color=RISK, stroke_width=3)
        d1 = VGroup(Dot(ax.c2p(*x1), radius=0.09, color=EVID), label(r"$x_1$", font_size=18, color=EVID).next_to(
            ax.c2p(*x1), UR, buff=0.05))
        d2 = VGroup(Dot(ax.c2p(*x2), radius=0.09, color=RISK), label(r"$x_2$", font_size=18, color=RISK).next_to(
            ax.c2p(*x2), UR, buff=0.05))
        bl = VGroup(label(r"budget 1: \ prices (1, 2), \ \$6", font_size=15, color=EVID).next_to(
            ax.c2p(0, 3), RIGHT, buff=0.15).shift(UP * 0.25),
            label(r"budget 2: \ prices (2, 1), \ \$8", font_size=15, color=RISK).next_to(ax.c2p(3.2, 2), RIGHT,
                                                                                            buff=0.25))
        side = stack([(r"week 1: \ $x_2$ cost \$5.50, \ affordable; \ chose $x_1$: \ so $x_1 \succeq x_2$", EVID),
                      (r"week 2: \ $x_1$ cost \$6, \ cheaper than the \$8 spent; \ chose $x_2$: \ so $x_2 \succ x_1$",
                       RISK),
                      (r"a violation of GARP: \ no utility rationalizes these choices", BAD),
                      (r"Afriat \ (1967): \ GARP holds iff some monotone concave utility does", PREF),
                      (r"efficiency index 0.917: \ the choices waste up to 8.3\% of the budget", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=5.6, buff=0.25).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Economists turned these axioms into tests on data. Paul Samuelson's idea of 1938 was revealed "
            "preference: if you chose one bundle when another was affordable, you revealed that you like the first "
            "at least as much. <bookmark mark='a'/>Here is a shopper the Reasoner made up, over two weeks and two "
            "goods. In week one, prices are one and two, and she spends six dollars on bundle one; bundle two would "
            "have cost five fifty, so she reveals bundle one at least as good. <bookmark mark='b'/>In week two, "
            "prices are two and one, and she spends eight dollars on bundle two, when bundle one would have cost "
            "only six. So she reveals bundle two strictly better. <bookmark mark='c'/>That is a violation of the "
            "generalized axiom of revealed preference. <bookmark mark='d'/>Sydney Afriat proved in 1967 that a "
            "finite set of choices passes that test exactly when some increasing, concave utility function explains "
            "them all: a complete test of rationality for a consumer. <bookmark mark='e'/>And Afriat's efficiency "
            "index says how bad a violation is: shrink every budget to ninety one point seven percent, and these "
            "choices pass. Experimental economists compute it for thousands of subjects; most come close to one."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(b1), FadeIn(bl[0]), FadeIn(d1), FadeIn(d2[0]))
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(b2), FadeIn(bl[1]), FadeIn(d2[1]))
            self.play(FadeIn(side[1]))
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
