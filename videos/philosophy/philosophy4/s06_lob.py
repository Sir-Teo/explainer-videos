from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Lob(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Löb's axiom and the limits of correspondence", r"Does every axiom say something about "
                            r"the arrows?", lit=(1975,), part=PART)
        with self.voiceover("Chapter five. Löb's axiom, and the limits of correspondence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.provability()
        self.second()
        self.frames()
        self.not_first_order()
        self.brick()
        self.sahlqvist()

    def provability(self):
        hcs = VGroup(history_card(1955, r"Martin Löb", r"if arithmetic proves `if $\varphi$ is provable then "
                                  r"$\varphi$', it proves $\varphi$", width=6.0, color=HIST),
                     history_card(1976, r"Robert Solovay", r"GL is exactly the logic of provability in arithmetic",
                                  width=6.0, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        ax = VGroup(MathTex(r"\Box(\Box p \to p) \to \Box p", font_size=50, color=GOAL),
                    label(r"Löb's axiom: \ read $\Box$ as `arithmetic proves'", font_size=26, color=GREY_A)).arrange(
            DOWN, buff=0.3).move_to([0, -0.6, 0])
        fwd = label(r"the provability reading of Gödel's theorems: \ Part 7", font_size=24, color=GREY_A).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Here is an axiom with a stranger meaning. <bookmark mark='a'/>In 1955 Martin Löb proved a theorem about "
            "arithmetic: if arithmetic proves 'if phi is provable, then phi', then arithmetic proves phi itself. "
            "<bookmark mark='b'/>Read the box as 'arithmetic proves', and Löb's theorem becomes a modal axiom. Add "
            "it to K and you get the system GL. <bookmark mark='c'/>In 1976 Robert Solovay proved that GL is exactly "
            "the logic of provability: every modal law of 'provable' is a theorem of GL. <bookmark mark='d'/>Gödel's "
            "incompleteness theorems become one-line theorems of this logic, in Part 7."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(Write(ax[0]), FadeIn(ax[1]))
            vo.wait_until("c")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(fwd))
        self.clear_scene()

    def second(self):
        steps = VGroup(
            MathTex(r"\Box(\Box p \to p) \to \Box p", font_size=40),
            label(r"take $p = \bot$, \ a contradiction", font_size=24, color=GREY_A),
            MathTex(r"\Box(\Box \bot \to \bot) \to \Box \bot", font_size=40),
            label(r"$\Box\bot \to \bot$ is $\lnot\Box\bot$: \ `arithmetic is consistent'", font_size=24,
                  color=GREY_A),
            MathTex(r"\Box\,\lnot\Box\bot \;\to\; \Box\bot", font_size=46, color=GOAL)).arrange(DOWN, buff=0.22)
        steps.move_to([-3.4, -0.1, 0])
        read = VGroup(label(r"if arithmetic proves its own consistency,", font_size=26),
                      label(r"then arithmetic proves a contradiction", font_size=26),
                      label(r"Gödel's second incompleteness theorem (1931), \ in one line", font_size=22,
                            color=OK)).arrange(DOWN, buff=0.2).move_to([3.3, -0.3, 0])
        with self.voiceover(
            "Here is what Löb's axiom can do. <bookmark mark='a'/>Take the axiom, and let p be a contradiction, "
            "falsum. <bookmark mark='b'/>Then 'if falsum is provable, then falsum' just says that falsum is not "
            "provable: arithmetic is consistent. <bookmark mark='c'/>So the instance reads: if arithmetic proves that "
            "it is consistent, then arithmetic proves a contradiction. <bookmark mark='d'/>That is Gödel's second "
            "incompleteness theorem, a consistent arithmetic cannot prove its own consistency, as a one-line "
            "consequence of a modal axiom. Part 7 builds the theorem itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), FadeIn(steps[3]))
            vo.wait_until("c")
            self.play(Write(steps[4]), FadeIn(read[:2]))
            vo.wait_until("d")
            self.play(FadeIn(read[2]))
        self.clear_scene()

    def frames(self):
        d = load("lob")
        rows = d["lob"]
        thm = label(r"Löb's axiom is valid on a frame \ $\iff$ \ $R$ is transitive \ and has no infinite chain "
                    r"$w_0 R w_1 R w_2 \cdots$", font_size=26, color=GOAL).to_edge(UP, buff=0.5)
        fin = label(r"on finite frames: \ transitive with no cycles, \ that is, a strict partial order", font_size=24,
                    color=GREY_A).next_to(thm, DOWN, buff=0.25)
        bars = bar_row([r["valid"] for r in rows], [rf"{r['worlds']} worlds" for r in rows], [OK] * len(rows),
                       width=5.0, height=0.42, font_size=24, log=True).move_to([-1.2, -0.6, 0])
        tot = VGroup(*[label(rf"of {r['frames']:,} frames".replace(",", "{,}"), font_size=22, color=GREY_A).next_to(
            b, RIGHT, buff=0.9) for r, b in zip(rows, bars)])
        for t, b in zip(tot, bars):
            t.next_to(b.value, RIGHT, buff=0.4)
        agree = label(r"valid exactly on the strict partial orders: \ 3, 19, 219, \ on every frame checked",
                      font_size=24, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Löb's axiom has a frame condition too. <bookmark mark='a'/>It is valid exactly when the arrows are "
            "transitive and there is no infinite chain of them: no world sees a world that sees a world, forever. "
            "<bookmark mark='b'/>On a finite frame that means no cycles at all: the arrows form a strict partial "
            "order. <bookmark mark='c'/>The Reasoner checked: of the frames with two, three and four worlds, the "
            "axiom is valid on three, nineteen and two hundred and nineteen, <bookmark mark='d'/>which are exactly "
            "the strict partial orders, on every frame."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(fin))
            vo.wait_until("c")
            for r, t in zip(bars, tot):
                self.play(FadeIn(r.name), GrowFromEdge(r.bar, LEFT), FadeIn(r.value), FadeIn(t), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(agree))
        self.clear_scene()

    def not_first_order(self):
        head = label(r"But `no infinite chain' is not first-order", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"suppose a first-order sentence $\sigma$ said it, \ for transitive frames", font_size=24),
            MathTex(r"\sigma,\ \ c_0 R c_1,\ \ c_1 R c_2,\ \ c_2 R c_3,\ \dots", font_size=38, color=GOAL),
            label(r"every finite part has a model: \ a finite chain $c_0 R c_1 R \cdots R c_n$", font_size=24,
                  color=OK),
            label(r"compactness (Part 3): \ the whole set has a model, \ with an infinite chain, \ yet $\sigma$ holds",
                  font_size=24, color=BAD),
            label(r"contradiction: \ Löb's axiom has no first-order frame condition", font_size=28,
                  color=BAD)).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Now a surprise, proved with a tool from Part 3. <bookmark mark='a'/>Suppose some first-order sentence "
            "sigma said 'there is no infinite chain', at least for transitive frames. <bookmark mark='b'/>Add new "
            "names c zero, c one, c two, and so on, with c zero seeing c one, c one seeing c two, forever. "
            "<bookmark mark='c'/>Every finite part of this set has a model: a finite chain, with no infinite chain in "
            "it. <bookmark mark='d'/>So by compactness the whole set has a model. It contains an infinite chain, and "
            "yet it satisfies sigma. <bookmark mark='e'/>Contradiction. Löb's axiom corresponds to a condition on "
            "the arrows, but no first-order sentence can state that condition."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=UP * 0.15))
        self.clear_scene()

    def brick(self):
        w = wall(upto=4, current=4).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(4, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        gt = label(r"Goldblatt and Thomason (1975): \ which first-order conditions an axiom can express; \ "
                   r"McKinsey's $\Box\Diamond p \to \Diamond\Box p$ expresses none", font_size=22,
                   color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This is the fourth brick in the Wall. <bookmark mark='a'/>The dream was to read every modal axiom off "
            "the frames as a plain statement about arrows, in the logic of Part 3. The wall: some axioms correspond "
            "to no first-order condition at all. Modal logic, read on frames, is a fragment of second-order logic. "
            "<bookmark mark='b'/>Robert Goldblatt and Steven Thomason characterized in 1975 exactly which classes of "
            "frames modal axioms can define. McKinsey's axiom, necessarily possibly p implies possibly necessarily "
            "p, is another axiom with no first-order condition."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(wc, shift=LEFT * 0.2), Indicate(w.brick[4], color=P.WALL))
            vo.wait_until("b")
            self.play(FadeIn(gt))
        self.clear_scene()

    def sahlqvist(self):
        thm = theorem_card(r"Sahlqvist's theorem (1975)", r"every axiom of a certain syntactic shape (a Sahlqvist "
                           r"formula) has a first-order frame condition, computed by an algorithm, and gives a "
                           r"complete logic", width=9.4, font_size=24).move_to([0, 1.3, 0])
        ex = VGroup(label(r"T, D, B, 4, 5 \ are all Sahlqvist formulas", font_size=26, color=OK),
                    label(r"Löb's and McKinsey's axioms are not", font_size=26, color=BAD)).arrange(DOWN, buff=0.25)
        ex.move_to([0, -0.6, 0])
        alg = label(r"the algorithm (SQEMA, Ackermann's lemma) is built into tools that translate modal logics into "
                    r"first-order provers", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There is good news on the other side of the wall. <bookmark mark='a'/>In 1975 Henrik Sahlqvist proved "
            "that every axiom of a certain syntactic shape has a first-order frame condition, which an algorithm "
            "can compute, and that adding such axioms to K always gives a complete logic. <bookmark mark='b'/>T, D, "
            "B, four and five all have that shape. Löb's and McKinsey's axioms do not, which is exactly why they "
            "escape. <bookmark mark='c'/>Today the algorithm runs inside tools that translate modal problems into "
            "first-order ones for the provers of Part 3."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(alg))
        self.clear_scene()
