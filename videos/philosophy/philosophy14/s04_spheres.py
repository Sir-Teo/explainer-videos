from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403

DEG = PI / 180
ANG = {"pqr": PI / 2, "pq~r": 90 * DEG, "p~qr": 210 * DEG, "~pqr": 330 * DEG, "p~q~r": 150 * DEG,
       "~pq~r": 30 * DEG, "~p~qr": 270 * DEG, "~p~q~r": 210 * DEG}


class Spheres(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Spheres and remainders", r"What do the postulates look like?", lit=(1985, 1988),
                            part=PART)
        with self.voiceover("Chapter three. Spheres and remainders."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grove()
        self.contraction()
        self.identities()

    def grove(self):
        d = load("spheres")
        hc = history_card(1988, r"Adam Grove", r"`Two Modellings for Theory Change'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        sp = SphereView(d["rank"], center=[-3.0, -0.75, 0], step=0.9, font_size=18, angles=ANG, ring_labels=True)
        rule = label(r"$K * A$: \ the $A$-worlds in the smallest sphere that meets $A$", font_size=23,
                     color=GOAL).move_to([3.4, 2.0, 0])
        cases = list(d["revisions"].items())
        texts = {"~p": r"\lnot p", "~p | ~q": r"\lnot p \lor \lnot q", "~p & ~q": r"\lnot p \land \lnot q",
                 "~r": r"\lnot r"}
        results = VGroup()
        for f, res in cases:
            results.add(MathTex(r"K * " + texts[f] + r" = \{" + r",\ ".join(wtex(w) for w in res) + r"\}",
                                font_size=28, color=NEW))
        results.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.2, 0])
        thm = label(r"Grove: \ AGM revisions are exactly the sphere revisions", font_size=22, color=OK).move_to(
            [3.4, -2.2, 0])
        thm2 = label(r"also: \ entrenchment orders; \ faithful preorders \ (Katsuno--Mendelzon)", font_size=19,
                     color=GREY_A).next_to(thm, DOWN, buff=0.15)
        with self.voiceover(
            "Adam Grove gave the postulates a picture in 1988. <bookmark mark='a'/>Arrange the possible worlds in "
            "nested spheres around your beliefs. The inner disc holds the worlds you think possible: here, one world, "
            "where p, q and r are all true. Each ring outward holds worlds a step less plausible. "
            "<bookmark mark='b'/>To revise by A, grow the spheres outward until one meets A, and believe the A-worlds "
            "there. <bookmark mark='c'/>Learn not p: the first ring has one such world. <bookmark mark='d'/>Learn not "
            "p or not q: two worlds on the first ring qualify. <bookmark mark='e'/>Learn not p and not q: you must go "
            "to the second ring. <bookmark mark='f'/>Learn not r: one world. <bookmark mark='g'/>Grove's theorem: the "
            "revisions satisfying all eight AGM postulates are exactly the sphere revisions. The same class arises from "
            "orderings of beliefs by entrenchment, and from the faithful preorders of Katsuno and Mendelzon."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sp))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            prev = []
            for mk, (f, res), r in zip("cdef", cases, results):
                vo.wait_until(mk)
                A = [w for w in d["rank"] if w in set(R.P(f, ("p", "q", "r")))]
                halos = sp.halo(res)
                self.play(*sp.paint(prev, WHITE), *sp.paint(A, NEW))
                self.play(Create(halos), FadeIn(r))
                self.play(FadeOut(halos), run_time=0.5)
                prev = A
            vo.wait_until("g")
            self.play(*sp.paint(prev, WHITE), FadeIn(thm), FadeIn(thm2))
        self.clear_scene()

    def contraction(self):
        d = load("spheres")
        head = label(r"Contraction: \ remainders, \ and choosing among them", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        lead = label(r"to give up $p$, \ keep a maximal part of $K$ that does not imply $p$: \ a \textit{remainder}",
                     font_size=23).next_to(head, DOWN, buff=0.3)
        rem = VGroup(*[MathTex(r"\{" + r",\ ".join(wtex(w) for w in r) + r"\}", font_size=26, color=BEL)
                       for r in d["remainders"]]).arrange(RIGHT, buff=0.45).next_to(lead, DOWN, buff=0.35)
        remlab = label(r"each remainder adds one $\lnot p$ world to $K$", font_size=20, color=GREY_A).next_to(
            rem, DOWN, buff=0.15)
        rows = VGroup(
            VGroup(label(r"maxichoice: \ pick one", font_size=23, color=BAD),
                   MathTex(r"\{" + r",\ ".join(wtex(w) for w in d["maxichoice"]) + r"\}", font_size=24),
                   label(r"too bold: \ settles every question about the $\lnot p$ worlds", font_size=19,
                         color=GREY_A)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"full meet: \ keep what all share", font_size=23, color=BAD),
                   MathTex(r"\{" + r",\ ".join(wtex(w) for w in d["full meet"]) + r"\}", font_size=22),
                   label(r"too timid: \ keeps almost nothing", font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"partial meet: \ the \textit{best} remainders", font_size=23, color=OK),
                   label(r"a selection function chooses", font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(remlab, DOWN, buff=0.45)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        thm = label(r"AGM (1985): \ partial meet contractions = the contractions satisfying the basic postulates",
                    font_size=22, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Contraction has its own construction. <bookmark mark='a'/>To give up p, keep as much of your beliefs as "
            "you can without implying p. A maximal such part is called a remainder. <bookmark mark='b'/>Here there are "
            "four, one for each world where p is false: each remainder admits exactly one of them. "
            "<bookmark mark='c'/>Which do you keep? Pick just one, maxichoice, and you are too bold: you settle every "
            "question about how things would be without p. <bookmark mark='d'/>Keep only what all the remainders share, "
            "full meet, and you are too timid: almost nothing survives. <bookmark mark='e'/>The right answer is in "
            "between: keep what the best remainders share, chosen by a selection function. "
            "<bookmark mark='f'/>AGM's representation theorem: these partial meet contractions are exactly the "
            "contractions satisfying the basic postulates; when the selection comes from an ordering, they satisfy "
            "the supplementary ones too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lead))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rem], lag_ratio=0.3), FadeIn(remlab))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(thm))
        self.clear_scene()

    def identities(self):
        d = load("spheres")
        head = label(r"Revision from contraction, \ and back", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        levi = VGroup(label(r"Levi identity", font_size=24, color=BEL),
                      MathTex(r"K * A = (K \div \lnot A) + A", font_size=34),
                      label(r"to accept $A$: \ first make room by giving up $\lnot A$, \ then add $A$", font_size=20,
                            color=GREY_A), mark(d["identities"]["levi"], 28)).arrange(DOWN, buff=0.18)
        harper = VGroup(label(r"Harper identity", font_size=24, color=BEL),
                        MathTex(r"K \div A = K \cap (K * \lnot A)", font_size=34),
                        label(r"keep what you would keep anyway \ if you learned $\lnot A$", font_size=20,
                              color=GREY_A), mark(d["identities"]["harper"], 28)).arrange(DOWN, buff=0.18)
        VGroup(levi, harper).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.5)
        chk = label(r"the Reasoner: \ both hold for every proposition, \ on the three-atom spheres", font_size=21,
                    color=OK).next_to(VGroup(levi, harper), DOWN, buff=0.35)
        ent = d["entrenchment"]
        etex = {"p & q": r"p \land q", "p": r"p", "p | q": r"p \lor q", "p | q | r": r"p \lor q \lor r"}
        bars = bar_row([ent[k] for k in ("p & q", "p", "p | q", "p | q | r")],
                       [rf"${etex[k]}$" for k in ("p & q", "p", "p | q", "p | q | r")], [BEL] * 4, width=3.0,
                       font_size=21, vmax=3, fmt=lambda v: f"{v:.0f}").to_edge(DOWN, buff=0.55).shift(LEFT * 2.6)
        el = stack([(r"entrenchment: \ how far out the nearest world without it lies", GREY_A),
                    (r"give up the least entrenched first \ (Gärdenfors and Makinson, \ 1988)", GOAL)],
                   font_size=21, aligned_edge=LEFT).next_to(bars, RIGHT, buff=0.6)
        with self.voiceover(
            "The three operations are linked. <bookmark mark='a'/>Isaac Levi's identity builds revision from "
            "contraction: to accept A, first make room by giving up not A, then add A. <bookmark mark='b'/>William "
            "Harper's goes the other way: to give up A, keep just what you would also keep if you learned not A. "
            "<bookmark mark='c'/>The Reasoner checks both, for every proposition, on these spheres. "
            "<bookmark mark='d'/>And the spheres give an order of entrenchment: a belief is as entrenched as the "
            "nearest world where it fails is far. p and q together, and p alone, are lost at the first ring; p or q at "
            "the second; p or q or r only at the third. <bookmark mark='e'/>Gärdenfors and Makinson showed that "
            "contraction can be defined from such an order: when something must go, give up what is least entrenched."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(levi))
            vo.wait_until("b")
            self.play(FadeIn(harper))
            vo.wait_until("c")
            self.play(FadeIn(chk))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.25), FadeIn(el[0]))
            vo.wait_until("e")
            self.play(FadeIn(el[1]))
        self.clear_scene()
