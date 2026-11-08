from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403

SHORT = {"D1": r"justice $=$ giving back what is owed", "o": r"returning the weapon $=$ giving back what is owed",
         "nj": r"returning it is not just", "D2": r"justice $=$ help friends, harm enemies",
         "h": r"the just will sometimes harm an enemy", "H": r"harming makes a person less just",
         "N": r"justice makes no one less just"}


class Elenchus(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Socrates as a SAT solver", r"When your beliefs contradict each other, what are "
                            r"your options?", lit=(-380,), part=PART)
        with self.voiceover("Chapter fourteen. Socrates as a SAT solver."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.d = load("elenchus")
        self.cephalus()
        self.polemarchus()
        self.machine()
        self.positions()

    def claim(self, key, color=P.CLAIM, font_size=24, width=4.4):
        t = wrapped_label(SHORT[key], width - 0.3, font_size, WHITE)
        b = RoundedRectangle(width=max(t.width + 0.35, 2.0), height=t.height + 0.3, corner_radius=0.12,
                             stroke_color=color, stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
        return VGroup(b, t.move_to(b))

    def cephalus(self):
        q = quote_card(r"Suppose that a friend, when in his right mind, has deposited arms with me and he asks for "
                       r"them when he is not in his right mind, ought I to give them back to him?",
                       r"Socrates to Cephalus, \textit{Republic} I, 331c", r"trans.\ Jowett", width=10.2,
                       font_size=26).to_edge(UP, buff=0.4)
        cs = VGroup(*[self.claim(k) for k in ("D1", "o", "nj")])
        pos = [[-4.2, -1.0, 0], [0, -2.6, 0], [4.2, -1.0, 0]]
        for c, p in zip(cs, pos):
            c.move_to(p)
        tri = Polygon(*[c.get_center() for c in cs], stroke_color=BAD, stroke_width=3)
        tri.set_z_index(-1)
        with self.voiceover(
            "Socrates' method was a kind of calculation. In Book One of Plato's Republic, the old man Cephalus "
            "suggests that justice is telling the truth and giving back what one owes. <bookmark mark='a'/>Socrates "
            "asks: suppose a friend, in his right mind, leaves weapons with you, then goes mad and asks for them back. "
            "Ought you to return them? <bookmark mark='b'/>Three claims. Justice is giving back what is owed. "
            "Returning the weapons is giving back what is owed. And returning them, to a madman, is not just. "
            "<bookmark mark='c'/>Each is plausible; together they are inconsistent."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q, color=P.HIST, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cs], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(Create(tri))
        self.clear_scene()

    def polemarchus(self):
        cs = VGroup(*[self.claim(k) for k in ("D2", "h", "H", "N")])
        pos = [[-4.0, 1.0, 0], [4.0, 1.0, 0], [4.0, -1.8, 0], [-4.0, -1.8, 0]]
        for c, p in zip(cs, pos):
            c.move_to(p)
        quad = Polygon(*[c.get_center() for c in cs], stroke_color=BAD, stroke_width=3)
        quad.set_z_index(-1)
        src = cite(r"\textit{Republic} I, 332d--335e")
        with self.voiceover(
            "Cephalus leaves to see to a sacrifice, and his son Polemarchus takes over the argument with a new "
            "definition: <bookmark mark='a'/>justice is helping one's friends and harming one's enemies. "
            "<bookmark mark='b'/>So the just will sometimes harm an enemy. <bookmark mark='c'/>Socrates presses. "
            "Harming a person makes him worse in human excellence, and justice is a human excellence: harming makes a "
            "person less just. <bookmark mark='d'/>But it cannot be the work of justice to make anyone less just. Four "
            "more claims, a second contradiction."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(c.copy().set_opacity(0.15)) for c in cs])
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cs[k], scale=0.9))
            self.play(Create(quad))
        self.clear_scene()

    def machine(self):
        d = self.d
        keys = [c["key"] for c in d["claims"]]
        rows = VGroup()
        for c in d["claims"]:
            rows.add(VGroup(MathTex(rf"\mathrm{{{c['key']}}}", font_size=26, color=ATOM),
                            fmath(c["formula"], font_size=30),
                            label(SHORT[c["key"]], font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.35))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        mus = d["mus"]
        mus_g = VGroup()
        for i, S in enumerate(mus):
            mus_g.add(MathTex(r"\{" + r",\ ".join(rf"\mathrm{{{k}}}" for k in S) + r"\}", font_size=34, color=BAD))
        mus_g.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        mh = label(r"minimal unsatisfiable subsets", font_size=26, color=BAD)
        mbox = VGroup(mh, mus_g).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        cnt = label(rf"{d['subsets_checked']} subsets checked", font_size=24, color=GREY_A).next_to(mbox, DOWN,
                                                                                                buff=0.4)
        cnt.align_to(mbox, LEFT)
        hl = [VGroup(*[rows[keys.index(k)] for k in S]) for S in mus]
        with self.voiceover(
            f"Feed all {len(keys)} claims to the Reasoner, each as a formula: o for 'returning the weapons is giving "
            "back what is owed', j for 'it is just', and so on. <bookmark mark='a'/>It checks every one of the "
            f"{d['subsets_checked']} subsets of claims for consistency, and returns the minimal inconsistent ones: "
            "sets that are contradictory, but stop being so if any single claim is removed. <bookmark mark='b'/>There "
            f"are exactly {len(mus)}: the two contradictions Socrates found, and no others hiding in the mixture."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(mh), FadeIn(cnt))
            vo.wait_until("b")
            for S, g, m in zip(mus, hl, mus_g):
                self.play(FadeIn(m), Indicate(g, color=BAD, scale_factor=1.03))
        self.clear_scene()

    def positions(self):
        d = self.d
        mus, mcs = d["mus"], d["mcs"]
        assert len(mcs) == len(mus[0]) * len(mus[1])
        left = VGroup(*[MathTex(rf"\mathrm{{MUS}}_{i + 1}", font_size=32, color=BAD) for i in range(len(mus))])
        left.arrange(DOWN, buff=1.6).move_to([-4.6, 0.2, 0])
        keys = [c["key"] for c in d["claims"]]
        right = VGroup(*[MathTex(rf"\mathrm{{{k}}}", font_size=30, color=ATOM) for k in keys])
        right.arrange(DOWN, buff=0.35).move_to([-1.6, 0.2, 0])
        edges = VGroup()
        for i, S in enumerate(mus):
            for k in S:
                edges.add(Line(left[i].get_right(), right[keys.index(k)].get_left(), color=BAD, stroke_width=2,
                               stroke_opacity=0.6))
        thm = theorem_card(r"Hitting-set duality", r"the minimal correction sets are exactly the minimal hitting "
                           r"sets of the minimal unsatisfiable subsets", who=r"Reiter 1987", width=6.2,
                           font_size=22).to_corner(UR, buff=0.35)
        grid = VGroup(*[MathTex(r"\{" + r",".join(rf"\mathrm{{{k}}}" for k in S) + r"\}", font_size=26,
                                color=P.PRICE) for S in mcs]).arrange_in_grid(rows=4, cols=3, buff=(0.45, 0.22))
        grid.next_to(thm, DOWN, buff=0.4)
        gl = label(rf"{len(mcs)} minimal ways out", font_size=24, color=P.PRICE).next_to(grid, DOWN, buff=0.25)
        soc = mcs.index(next(S for S in mcs if set(S) == {"D1", "D2"}))
        sbox = SurroundingRectangle(grid[soc], color=GOAL, buff=0.08)
        sl = label(r"Socrates' choice: \ drop both definitions", font_size=24, color=GOAL).next_to(gl, DOWN,
                                                                                               buff=0.25)
        with self.voiceover(
            "Now the question an interlocutor actually faces: which claims to give up? <bookmark mark='a'/>A minimal "
            "correction set is a smallest set of claims whose removal restores consistency. <bookmark mark='b'/>Here "
            f"there are {len(mcs)}: one claim from the first contradiction and one from the second, in every "
            "combination. <bookmark mark='c'/>That is no accident. A theorem of Raymond Reiter, from 1987, says the "
            "minimal correction sets are exactly the minimal hitting sets of the minimal inconsistent ones: the "
            "smallest ways of breaking every contradiction at once."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), Create(edges))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.08), FadeIn(gl), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(thm, color=CONN))
        with self.voiceover(
            "Socrates' own choice was one of these: give up both definitions. <bookmark mark='a'/>The logic did not "
            "choose for him. It showed exactly where the choices were. <bookmark mark='b'/>This is the engine of the "
            "series' Price List. For each great puzzle we will state the plausible claims, let the machine find "
            "every exit, and label each exit with the philosophers who take it, and, where the 2020 PhilPapers "
            "survey asked, how many philosophers take it."
        ) as vo:
            self.play(Create(sbox), FadeIn(sl))
            vo.wait_until("a")
            self.play(Indicate(grid, color=P.PRICE, scale_factor=1.03))
            vo.wait_until("b")
        self.clear_scene()
