from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class PBR(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Is the wavefunction real?", r"State of the world, \ or state of knowledge?",
                            lit=(2012,), part=PART)
        with self.voiceover("Chapter nine. Is the wavefunction real?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.views()
        self.toy()
        self.table()
        self.verdict()

    def views(self):
        head = label(r"Two readings of $\psi$", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ax_l = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.5], x_length=4.6, y_length=2.0, tips=False,
                    axis_config={"color": GREY_D}).move_to([-3.4, -0.4, 0])
        ax_r = ax_l.copy().move_to([3.4, -0.4, 0])
        g1 = ax_l.plot(lambda x: math.exp(-((x - 1.4) / 0.35) ** 2), x_range=[0, 4], color=WAVE)
        g2 = ax_l.plot(lambda x: math.exp(-((x - 2.6) / 0.35) ** 2), x_range=[0, 4], color=ALICE)
        h1 = ax_r.plot(lambda x: math.exp(-((x - 1.7) / 0.55) ** 2), x_range=[0, 4], color=WAVE)
        h2 = ax_r.plot(lambda x: math.exp(-((x - 2.3) / 0.55) ** 2), x_range=[0, 4], color=ALICE)
        tl = label(r"$\psi$-ontic: \ different states, \ disjoint realities", font_size=20, color=OK).next_to(
            ax_l, UP, buff=0.3)
        tr = label(r"$\psi$-epistemic: \ the states overlap: \ knowledge of a reality", font_size=20,
                   color=BAD).next_to(ax_r, UP, buff=0.3)
        lab = label(r"the space of real, \ underlying states $\lambda$", font_size=17, color=GREY_A)
        lab_l = lab.copy().next_to(ax_l, DOWN, buff=0.15)
        lab_r = lab.copy().next_to(ax_r, DOWN, buff=0.15)
        foot = label(r"if epistemic, \ collapse is just updating, \ like Bayes: \ an attractive way out", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Is the wavefunction a feature of reality, or a summary of what we know? Think of a deeper space of "
            "real states, lambda, and ask how a quantum state relates to it. <bookmark mark='a'/>On a psi-ontic "
            "view, two different quantum states always correspond to disjoint sets of real states: the wavefunction "
            "is part of reality. <bookmark mark='b'/>On a psi-epistemic view, two different quantum states can "
            "correspond to overlapping distributions over the same real states, as two probability distributions "
            "can overlap. <bookmark mark='c'/>The epistemic view is attractive: collapse would just be learning, "
            "like updating by Bayes's rule in Part 14."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax_l), Create(g1), Create(g2), FadeIn(tl), FadeIn(lab_l))
            vo.wait_until("b")
            self.play(Create(ax_r), Create(h1), Create(h2), FadeIn(tr), FadeIn(lab_r))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def toy(self):
        d = load("toy")
        head = label(r"Spekkens' toy theory", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["n_states"] == 6 and d["mixtures_equal"] and set(d["overlaps"].values()) == {4}
        cells = VGroup(*[Square(0.7, color=GREY_B, stroke_width=2) for _ in range(4)]).arrange(RIGHT, buff=0.12)
        nums = VGroup(*[label(str(k), font_size=22, color=GREY_A).move_to(c) for k, c in zip((1, 2, 3, 4), cells)])
        onto = VGroup(cells, nums).move_to([-3.6, 1.7, 0])
        otag = label(r"four real states", font_size=18, color=GREY_A).next_to(onto, UP, buff=0.12)
        know = VGroup(*[c.copy().set_fill(WAVE, opacity=0.5) for c in cells[:2]])
        ktag = label(r"knowledge balance: \ know at most half: \ `1 or 2'", font_size=19, color=WAVE).next_to(
            onto, DOWN, buff=0.2)
        ms = d["measurements"]
        assert ms == [["12", "34"], ["13", "24"], ["14", "23"]]
        hd = [r"\text{state}", r"\{12 \,|\, 34\}", r"\{13 \,|\, 24\}", r"\{14 \,|\, 23\}"]
        rows = [[MathTex(r["state"][0] + r"\vee " + r["state"][1], font_size=24, color=WAVE)] +
                [MathTex(f"{p_:g}", font_size=24, color=(OK if p_ == 1 else BAD if p_ == 0 else GREY_A))
                 for p_ in r["p"]] for r in d["table"]]
        grid = ValueGrid(hd, rows, col_w=[1.3, 1.6, 1.6, 1.6], cell_h=0.42, font_size=20).move_to([3.4, 0.3, 0])
        gtag = label(r"$P$(first outcome): \ certain once, \ 50/50 twice, \ like a qubit's six axis states",
                     font_size=18, color=GREY_A).next_to(grid, DOWN, buff=0.15)
        side = stack([(r"distinct states overlap: \ `1 or 2' and `1 or 3' share state 1 \ ($\psi$-epistemic)", ABS),
                      (r"collapse is learning; \ $\tfrac12(12) + \tfrac12(34) = \tfrac12(13) + \tfrac12(24)$", ALICE),
                      (r"it mimics complementarity, \ no-cloning, \ teleportation; \ not Bell violations", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.2, buff=0.25).move_to([-3.4, -1.7, 0])
        with self.voiceover(
            "Before the theorem, a model that shows what the epistemic view hoped for. <bookmark mark='a'/>In 2007 "
            "Robert Spekkens built a toy theory. A system has four possible real states. <bookmark mark='b'/>One "
            "rule, a knowledge balance principle: you may know at most half of what there is to know. So the most "
            "you can know is a pair, such as: the real state is one or two. That gives six states of maximal "
            "knowledge. <bookmark mark='c'/>There are three ways of measuring, each splitting the four into two "
            "pairs. The Reasoner computes the table. Each state is certain under one measurement and fifty-fifty "
            "under the other two, just like a qubit's six states along three axes. <bookmark mark='d'/>Distinct "
            "states overlap: one or two, and one or three, share the real state one. Collapse is just learning. "
            "And an even mixture of one-or-two and three-or-four is the same as one of one-or-three and "
            "two-or-four, as for a qubit. <bookmark mark='e'/>The toy mimics complementary measurements, a version "
            "of no-cloning, and even teleportation. It cannot mimic Bell violations or contextuality, because it is "
            "a local, non-contextual model of hidden states. PBR asks whether any model like it can reproduce all "
            "of quantum mechanics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(onto), FadeIn(otag))
            vo.wait_until("b")
            self.play(FadeIn(know), FadeIn(ktag))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.3)
            self.play(FadeIn(gtag))
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def table(self):
        d = load("pbr")
        head = label(r"The PBR measurement, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{prepared}", r"\xi_1", r"\xi_2", r"\xi_3", r"\xi_4"]
        names = {"00": r"|0\rangle|0\rangle", "0+": r"|0\rangle|{+}\rangle", "+0": r"|{+}\rangle|0\rangle",
                 "++": r"|{+}\rangle|{+}\rangle"}
        rows = []
        for k, row in d["table"].items():
            rows.append([MathTex(names[k], font_size=24, color=WAVE)] +
                        [MathTex(f"{v:.2f}", font_size=24, color=BAD if v < 1e-9 else WHITE) for v in row])
        grid = ValueGrid(hd, rows, col_w=[2.6, 1.4, 1.4, 1.4, 1.4], cell_h=0.55, font_size=22).move_to([-2.2, -0.4, 0])
        side = stack([(r"prepare two systems, \ each in $|0\rangle$ or $|{+}\rangle$, \ independently", WAVE),
                      (r"measure the pair in an entangled basis $\xi_1, \dots, \xi_4$", ABS),
                      (r"each outcome has probability 0 for one preparation", BAD),
                      (r"if $|0\rangle$ and $|{+}\rangle$ shared real states, \ some runs would be compatible with "
                       r"all four: \ yet some outcome must occur", GOAL)], font_size=20, aligned_edge=LEFT, width=4.6,
                     buff=0.3).move_to([4.5, -0.4, 0])
        assert d["orthonormal"] and sorted(i for v in d["forbidden"].values() for i in v) == [0, 1, 2, 3]
        with self.voiceover(
            "In 2012 Matthew Pusey, Jonathan Barrett and Terry Rudolph proved that, under a natural assumption, the "
            "epistemic view is false. <bookmark mark='a'/>Prepare two systems independently, each in zero or in "
            "plus: four possible preparations. <bookmark mark='b'/>Measure the pair in a particular entangled basis "
            "with four outcomes. The Reasoner builds it and checks that it is orthonormal. "
            "<bookmark mark='c'/>The probability table has a striking pattern: each outcome has probability zero for "
            "exactly one of the four preparations. <bookmark mark='d'/>Now suppose zero and plus overlapped in "
            "reality. Then, sometimes, both systems would be in real states compatible with both preparations, so "
            "the pair's real state would be compatible with all four. On such a run, every outcome is forbidden by "
            "one of them. But some outcome always occurs. So the states cannot overlap."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("c")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def verdict(self):
        head = label(r"What PBR shows", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the conclusion", r"if there are real states, \ and independent preparations have independent real "
                                r"states, \ $\psi$ is part of reality", OK),
            (r"the assumption", r"preparation independence: \ some deny it, \ and keep an epistemic view", BAD),
            (r"who escapes", r"QBism and Copenhagen: \ they deny that there is a deeper real state to talk about", ABS),
            (r"the pressure", r"Bohm and Everett already treat $\psi$ as real; \ PBR says the epistemic middle way is "
                              r"narrow", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "What does it show? <bookmark mark='a'/>If there are underlying real states at all, and systems "
            "prepared independently have independent real states, then the wavefunction is part of reality, not "
            "just knowledge. <bookmark mark='b'/>The second assumption, preparation independence, can be denied, and "
            "some do deny it to keep an epistemic view. <bookmark mark='c'/>QBism and some readings of Copenhagen "
            "escape differently, by refusing to posit any deeper real state. <bookmark mark='d'/>Bohm and Everett "
            "already treat the wavefunction as real. PBR narrows the epistemic middle way."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
