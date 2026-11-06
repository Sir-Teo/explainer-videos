from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403


def worldset(ws, center, r=0.22, col=BEL, label_text=None) -> VGroup:
    """Three world slots a, b, c in a row; the ones in ``ws`` filled."""
    g = VGroup()
    for i, w in enumerate("abc"):
        on = w in ws
        disc = Circle(radius=r, color=col if on else GREY_D, fill_color=col, fill_opacity=0.45 if on else 0,
                      stroke_width=3).move_to(np.asarray(center) + np.array([(i - 1) * 0.62, 0, 0]))
        t = MathTex(w, font_size=22, color=WHITE if on else GREY_D).move_to(disc)
        g.add(VGroup(disc, t))
    if label_text:
        g.add(MathTex(label_text, font_size=26, color=col).next_to(g, LEFT, buff=0.3))
    return g


class Gardenfors(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Gärdenfors's impossibility", r"Can the Ramsey test live with revision?",
                            lit=(1986,), part=PART)
        with self.voiceover("Chapter six. Gärdenfors's impossibility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ingredients()
        self.proof()
        self.responses()

    def ingredients(self):
        hc = history_card(1986, r"Peter Gärdenfors", r"`Belief Revisions and the Ramsey Test for Conditionals'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        mono = VGroup(label(r"monotonicity, \ from the Ramsey test", font_size=24, color=NEW),
                      MathTex(r"K \subseteq H \ \Rightarrow\ K * A \subseteq H * A", font_size=32),
                      label(r"$H$ believes all of $K$'s conditionals, \ so revises at least as boldly", font_size=20,
                            color=GREY_A)).arrange(DOWN, buff=0.18)
        pres = VGroup(label(r"preservation, \ from AGM", font_size=24, color=BEL),
                      MathTex(r"\lnot A \notin K \ \Rightarrow\ K \subseteq K * A", font_size=32),
                      label(r"news that fits loses nothing \ (vacuity)", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.18)
        VGroup(mono, pres).arrange(RIGHT, buff=1.0).next_to(hc, DOWN, buff=0.6).set_x(0)
        thm = label(r"Theorem: \ no non-trivial revision system has both", font_size=28, color=BAD).to_edge(
            DOWN, buff=0.8)
        nt = label(r"non-trivial: \ some $K$ is consistent with three pairwise incompatible $A$, $B$, $C$",
                   font_size=21, color=GREY_A).next_to(thm, DOWN, buff=0.2)
        with self.voiceover(
            "Gärdenfors proved it in 1986. Two ingredients. <bookmark mark='a'/>First, the Ramsey test makes revision "
            "monotone. If belief set H includes belief set K, it includes K's conditionals; by the Ramsey test, those "
            "conditionals say what K's revisions contain; so H's revisions contain at least as much. "
            "<bookmark mark='b'/>Second, preservation, which follows from AGM's vacuity: news consistent with your "
            "beliefs costs you nothing. <bookmark mark='c'/>The theorem: no non-trivial system of revision satisfies "
            "both. Non-trivial means only that some belief set leaves open three propositions that exclude one "
            "another."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(mono))
            vo.wait_until("b")
            self.play(FadeIn(pres))
            vo.wait_until("c")
            self.play(FadeIn(thm), FadeIn(nt))
        self.clear_scene()

    def proof(self):
        d = load("gardenfors")
        head = label(r"The proof, \ on three worlds", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        sub = label(r"$A = \{a\}$, \ $B = \{b\}$, \ $C = \{c\}$: \ shaded worlds are the ones a belief set leaves open",
                    font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.15)
        xs = -3.2
        K = worldset(d["K"], [xs, 1.6, 0], label_text=r"K")
        K1 = worldset(d["K1"], [xs, 0.6, 0], label_text=r"K_1 = K + (A \lor B)")
        K2 = worldset(d["K2"], [xs, -0.4, 0], label_text=r"K_2 = K + (A \lor C)")
        H = worldset(d["H"], [xs, -1.4, 0], label_text=r"H = K + A")
        xr = 3.6
        r1 = worldset(d["K1*(BvC)"], [xr, 0.6, 0], col=NEW, label_text=r"K_1 * (B \lor C)")
        r2 = worldset(d["K2*(BvC)"], [xr, -0.4, 0], col=NEW, label_text=r"K_2 * (B \lor C)")
        pres_note = label(r"preservation: \ consistent news is just added", font_size=20, color=BEL).move_to(
            [xr - 0.6, 1.6, 0])
        incl = label(r"$H$ includes $K_1$ and $K_2$, \ conditionals and all", font_size=20, color=NEW).move_to(
            [-2.6, -2.3, 0])
        need = MathTex(r"H * (B \lor C) \subseteq \{b\} \cap \{c\} = \varnothing", font_size=32, color=BAD).move_to(
            [-2.6, -3.0, 0])
        cands = VGroup()
        for i, row in enumerate(d["candidates"]):
            ws = row["H*(BvC)"]
            c = worldset(ws, [xr + 0.4, -1.4 - 0.0, 0], col=GREY_B)
            cands.add(c)
        cand_lab = MathTex(r"H * (B \lor C)\, ?", font_size=26, color=GREY_B).next_to(cands[0], LEFT, buff=0.3)
        verdicts = [label(r"$\{b\}$: \ not within $K_2 * (B \lor C)$", font_size=19, color=BAD),
                    label(r"$\{c\}$: \ not within $K_1 * (B \lor C)$", font_size=19, color=BAD),
                    label(r"$\{b, c\}$: \ within neither", font_size=19, color=BAD)]
        for v in verdicts:
            v.next_to(cands[0], DOWN, buff=0.15)
        assert d["survivors"] == []
        with self.voiceover(
            "Here is the proof, on three worlds. <bookmark mark='a'/>A, B and C are true in one world each. Start from "
            "a belief set K that leaves all three open. <bookmark mark='b'/>Expand it by A or B, giving K one, and by A "
            "or C, giving K two. <bookmark mark='c'/>And expand it by A alone, giving H. <bookmark mark='d'/>Now revise "
            "K one and K two by B or C. That news is consistent with each of them, so by preservation it is simply "
            "added: K one now believes B, and K two believes C. <bookmark mark='e'/>H includes everything K one and K "
            "two believe, their conditionals included. So by monotonicity, H's revision by B or C must lie within "
            "both of theirs: within b, and within c. <bookmark mark='f'/>The Reasoner tries every candidate. "
            "Believing b fails the second constraint; <bookmark mark='g'/>believing c fails the first; "
            "<bookmark mark='h'/>leaving both open fails both. <bookmark mark='i'/>Nothing is left: H's revision by a "
            "consistent proposition would have to be inconsistent. The contradiction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(K))
            vo.wait_until("b")
            self.play(FadeIn(K1), FadeIn(K2))
            vo.wait_until("c")
            self.play(FadeIn(H))
            vo.wait_until("d")
            self.play(FadeIn(pres_note), FadeIn(r1), FadeIn(r2))
            vo.wait_until("e")
            self.play(FadeIn(incl), Write(need))
            vo.wait_until("f")
            self.play(FadeIn(cand_lab), FadeIn(cands[0]), FadeIn(verdicts[0]))
            for mk, k in zip("gh", (1, 2)):
                vo.wait_until(mk)
                self.play(Transform(cands[0], cands[k]), Transform(verdicts[0], verdicts[k]))
            vo.wait_until("i")
            self.play(Indicate(need, color=BAD, scale_factor=1.06))
        self.clear_scene()

    def responses(self):
        head = label(r"Which ingredient goes?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        items = [
            (r"conditionals are not beliefs", r"Levi: \ they express how one would revise; \ keep them out of $K$",
             BEL),
            (r"weaken preservation", r"revise with conditionals in view: \ some news costs you conditionals", BEL),
            (r"revise by update instead", r"Grahne \ (1998): \ the Ramsey test is consistent with Katsuno--Mendelzon "
                                          r"update", NEW),
            (r"restrict the test", r"apply it only to factual antecedents and consequents", GREY_A),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(items):
            x = label(a, font_size=23, color=c)
            y = label(b, font_size=20, color=GREY_A)
            if y.width > 7.2:
                y.width = 7.2
            x.move_to([-6.4 + x.width / 2, 1.7 - i * 1.0, 0])
            y.move_to([-1.2 + y.width / 2, 1.7 - i * 1.0, 0])
            g.add(VGroup(x, y))
        foot = label(r"half of this part's brick in the Wall: \ conditionals resist being ordinary beliefs",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Something has to give. <bookmark mark='a'/>Isaac Levi's answer: conditionals are not beliefs at all. They "
            "express how you are disposed to revise, and so do not belong in the belief set. "
            "<bookmark mark='b'/>Or weaken preservation: once conditionals are beliefs, consistent news can cost you "
            "some of them. <bookmark mark='c'/>Gösta Grahne showed that the Ramsey test is consistent with update, in "
            "Katsuno and Mendelzon's sense, rather than revision. <bookmark mark='d'/>Or restrict the test to factual "
            "sentences. <bookmark mark='e'/>Every answer concedes that conditionals resist being treated as ordinary "
            "beliefs. That is half of this part's brick in the Wall; Lewis supplies the other half in chapter eight."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
