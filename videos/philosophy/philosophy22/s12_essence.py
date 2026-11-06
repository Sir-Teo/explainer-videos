from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Essence(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Essence without modality", r"Is essence just necessity?", lit=(1994, 2013),
                            part=PART)
        with self.voiceover("Chapter eleven. Essence without modality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.modal()
        self.socrates()
        self.asymmetry()
        self.payoff()

    def modal(self):
        head = label(r"The modal account of essence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"F \text{ is essential to } x \;\iff\; \Box\,(\exists y\,(y = x) \to Fx)", font_size=38,
                    color=ABS).next_to(head, DOWN, buff=0.5)
        rows = [
            (r"origin", r"Kripke: \ this table could not have been made of ice; \ the Queen could not have had other "
                        r"parents", NAME),
            (r"kind", r"water is essentially H$_2$O; \ a tiger is essentially of its species", WORLD),
            (r"the attraction", r"essence becomes something we already understand: \ necessity, \ and worlds", OK),
            (r"Fine \ (1994)", r"`Essence and Modality': \ the account gets the extension wrong", BAD),
        ]
        g = rows_table(rows, top=0.9, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "If necessity is truth at all worlds, perhaps essence can be defined in the same terms. "
            "<bookmark mark='a'/>The modal account: a property is essential to a thing if, necessarily, if the thing "
            "exists, it has the property. <bookmark mark='b'/>Kripke's examples fit: this wooden table could not have "
            "been made of ice; the Queen could not have had different parents. Origin is essential. "
            "<bookmark mark='c'/>So does kind: water is essentially H two O. <bookmark mark='d'/>The attraction is "
            "that essence becomes something we already understand, necessity, and so, ultimately, worlds. "
            "<bookmark mark='e'/>In 1994 Kit Fine argued that the account gets even the simplest cases wrong."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def socrates(self):
        d = load("essence")
        head = label(r"Socrates and his singleton", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lay = {"@": [-5.2, 1.4, 0], "w1": [-1.8, 1.4, 0], "w2": [1.6, 1.4, 0], "w3": [5.0, 1.4, 0]}
        isl = VGroup()
        for k, (w, c) in enumerate(lay.items()):
            I = island(c, w=3.0, h=1.6, seed=180 + k, color=NAME if w == "@" else WORLD,
                       name=r"actual" if w == "@" else rf"$w_{k}$", font_size=18)
            xs = d["worlds"][w]
            items = VGroup()
            for j, x in enumerate(xs):
                p = np.array(c) + np.array([-0.6 + 1.2 * j, 0.15, 0])
                items.add(label(x if x != "Eiffel" else r"the Eiffel Tower", font_size=15, color=DESC if
                                x == "Socrates" else GREY_A).move_to(p))
            if "Socrates" in xs:
                items.add(MathTex(r"\{\text{Socrates}\}", font_size=22, color=CPT).move_to(np.array(c) + DOWN * 0.4))
            isl.add(VGroup(I, items))
        hd = [r"\text{property of Socrates}", r"\text{modal account}", r"\text{part of what he is?}"]
        rows = []
        for r in d["rows"]:
            rows.append([label(r["property"], font_size=19), mark(r["modal"]), mark(r["real"])])
        grid = ValueGrid(hd, rows, col_w=[5.4, 2.6, 2.8], cell_h=0.45, font_size=19).move_to([0, -1.75, 0])
        with self.voiceover(
            "Fine's example. <bookmark mark='a'/>Take worlds where Socrates exists, and worlds where he does not. "
            "Wherever Socrates exists, so does his singleton: the set whose only member is Socrates. Set theory "
            "guarantees it. <bookmark mark='b'/>Now ask which properties Socrates has at every world where he "
            "exists. Being human: yes, and that is plausibly part of what he is. <bookmark mark='c'/>Being a member "
            "of his singleton: also yes. So on the modal account it is essential to Socrates that he belongs to a "
            "set. <bookmark mark='d'/>Being distinct from the Eiffel Tower: yes, necessarily. Being such that two "
            "plus two is four: yes, trivially. On the modal account these are all essential to Socrates. "
            "<bookmark mark='e'/>But it is no part of what Socrates is, of his nature, that he belongs to a set, or "
            "differs from a tower, or coexists with arithmetic. Teaching Plato and being seated are contingent, and "
            "the account rightly leaves them out. The Reasoner's table shows the gap: three properties the modal "
            "account counts as essential that are not part of his essence at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in isl], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[0][c]) for c in range(3)])
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[1][c]) for c in range(3)])
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][c]) for r in (2, 3) for c in range(3)])
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[r][c]) for r in (4, 5) for c in range(3)])
            self.play(*[Indicate(grid.cell[r][1], color=BAD) for r in (1, 2, 3)])
        self.clear_scene()

    def asymmetry(self):
        head = label(r"The asymmetry modality cannot see", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        s = person([-3.0, 1.3, 0], color=DESC, name=r"Socrates", font_size=20, r=0.25)
        brace = MathTex(r"\{\qquad\qquad\}", font_size=80, color=CPT).move_to([3.0, 1.3, 0])
        s2 = Dot([3.0, 1.3, 0], radius=0.18, color=DESC)
        bl = label(r"the singleton", font_size=20, color=CPT).next_to(brace, DOWN, buff=0.1)
        ar = Arrow([-2.5, 1.3, 0], [1.45, 1.3, 0], buff=0.1, color=GREY_B, stroke_width=3)
        al = label(r"is a member of", font_size=18, color=GREY_A).next_to(ar, UP, buff=0.08)
        rows = stack([(r"necessarily, \ if either exists, \ Socrates is a member of \{Socrates\}: \ modality is "
                       r"symmetric here", ABS),
                      (r"but it lies in the nature of the singleton to contain Socrates, \ not in the nature of "
                       r"Socrates to be contained", GOAL),
                      (r"Fine: \ essence is real definition: \ $\Box_x\, \varphi$, \ `it is true in virtue of the "
                       r"nature of $x$ that $\varphi$'", NAME),
                      (r"and necessity is derived: \ true in virtue of the natures of all things", OK)],
                     font_size=21, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The failure has a structure. <bookmark mark='a'/>Necessarily, if either exists, Socrates is a member of "
            "his singleton. As far as modality goes, the connection runs equally in both directions. "
            "<bookmark mark='b'/>But essence is not symmetric. It lies in the nature of the singleton to have "
            "Socrates as its member: a set is defined by its members. It does not lie in the nature of Socrates to "
            "be a member of anything. <bookmark mark='c'/>Fine's alternative: essence is real definition, the "
            "definition of a thing rather than of a word. He wrote it with a box indexed to the thing: it is true in "
            "virtue of the nature of x that phi. <bookmark mark='d'/>And then the order of explanation reverses. "
            "Necessity is not prior to essence. What is metaphysically necessary is what is true in virtue of the "
            "natures of all things."
        ) as vo:
            self.play(FadeIn(head), FadeIn(s), FadeIn(brace), FadeIn(s2), FadeIn(bl))
            vo.wait_until("a")
            self.play(GrowArrow(ar), FadeIn(al), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def payoff(self):
        head = label(r"Why essence might be deeper", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"explanation", r"why is water necessarily H$_2$O? \ because that is what water is", NAME),
            (r"knowledge", r"we know necessities by knowing natures \ (Lowe; \ Hale, \ 2013), \ sometimes by "
                           r"experiment", WORLD),
            (r"grounding", r"essence and ground together: \ Part 20's `in virtue of' meets the theory of natures", CPT),
            (r"the other side", r"modalists reply: \ define essence with finer modal notions, \ or with sparse "
                                r"properties", GREY_A),
            (r"the stakes", r"which is fundamental: \ worlds, \ or natures?", GOAL),
        ]
        g = rows_table(rows, top=1.8, gap=0.48, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "If Fine is right, essence explains necessity. <bookmark mark='a'/>Why is water necessarily H two O? "
            "Because that is what water is. <bookmark mark='b'/>Then we can know necessities by knowing natures, as "
            "Jonathan Lowe and Bob Hale argued; and sometimes, as with water, we learn a nature by experiment. That "
            "is the necessary a posteriori, explained. <bookmark mark='c'/>Essence also joins hands with grounding: "
            "Part 20's in virtue of. <bookmark mark='d'/>Modalists have replies: refine the modal definition, for "
            "instance by requiring the property to be sparse, or intrinsic. <bookmark mark='e'/>The stakes are which "
            "notion is fundamental: worlds, or natures."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
