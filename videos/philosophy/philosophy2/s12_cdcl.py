from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403

FN = "abcdefgh"


def lt(l):
    return (r"\lnot " if l < 0 else "") + FN[abs(l) - 1]


def node(l, color, decision=False):
    c = Circle(radius=0.34, stroke_color=color, stroke_width=3 if decision else 2, fill_color="#0B0F17",
               fill_opacity=1)
    if decision:
        c.set_fill(color, opacity=0.25)
    t = MathTex(lt(l), font_size=32, color=color).move_to(c)
    return VGroup(c, t)


class CDCL(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Learning from conflict", r"Can a search learn from its mistakes?",
                            lit=(1996,), part=PART)
        with self.voiceover("Chapter eleven. Learning from conflict."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.intro()
        self.graph()
        self.measure()

    def intro(self):
        hcs = VGroup(history_card(1996, r"João Marques-Silva \& Karem Sakallah", r"GRASP: learn a clause from "
                                  r"every conflict; jump back past irrelevant choices", width=6.0, color=HIST),
                     history_card(2001, r"Moskewicz, Madigan, Zhao, Zhang \& Malik", r"Chaff: watched literals, "
                                  r"activity-based choices; industrial-scale SAT", width=6.0, color=HIST))
        hcs.arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        forget = VGroup(label(r"DPLL backs up one step", font_size=30, color=GREY_A),
                        label(r"and may rediscover the same dead end", font_size=30, color=GREY_A),
                        label(r"elsewhere in the tree, again and again", font_size=30, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "DPLL forgets. When a branch fails, it backs up one step and tries again; and if the same mistake lurks "
            "elsewhere in the tree, it rediscovers it, again and again. <bookmark mark='a'/>In 1996 João Marques-Silva "
            "and Karem Sakallah, with their solver GRASP, taught the search to learn from every failure. "
            "<bookmark mark='b'/>Five years later, the solver Chaff made the idea fast. Conflict-driven clause "
            "learning is inside every serious SAT solver today."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in forget], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(hcs[0], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1], shift=LEFT * 0.2))
        self.clear_scene()

    def graph(self):
        d = load("cdcl")
        ev = d["events"]
        clauses = d["clauses"]
        kinds = [e["kind"] for e in ev]
        # the run this chapter narrates: decide a; propagate b c d e f; conflict; learn ¬a; backjump to 0; ...
        assert kinds[:9] == ["decide"] + ["propagate"] * 5 + ["conflict", "learn", "backjump"], kinds
        assert ev[0]["lit"] == 1 and [e["lit"] for e in ev[1:6]] == [2, 3, 4, 5, 6]
        assert ev[7]["lit"] == [-1]
        fm = VGroup(*[MathTex(clause_tex(frozenset(c), list(FN)), font_size=26) for c in clauses]).arrange(
            RIGHT, buff=0.25)
        if fm.width > 13.4:
            fm.width = 13.4
        fm.to_edge(UP, buff=0.3)
        pos = {1: [-5.4, 0.2, 0], 2: [-3.6, 1.3, 0], 3: [-3.6, -0.9, 0], 4: [-1.6, 0.2, 0], 5: [0.2, 1.3, 0],
               6: [1.8, 0.2, 0]}
        nodes = {1: node(1, CONN, decision=True).move_to(pos[1])}
        for e in ev[1:6]:
            nodes[e["lit"]] = node(e["lit"], P.WORLD).move_to(pos[e["lit"]])
        arrows = VGroup()
        edge_of = {}
        for e in ev[1:6]:
            l = e["lit"]
            for x in clauses[e["clause"]]:
                if x != l:
                    src = -x
                    a = Arrow(nodes[src].get_center(), nodes[l].get_center(), buff=0.38, color=GREY_B,
                              stroke_width=3, max_tip_length_to_length_ratio=0.12)
                    arrows.add(a)
                    edge_of.setdefault(l, []).append(a)
        conf_clause = clauses[ev[6]["clause"]]
        boom = VGroup(Star(n=8, outer_radius=0.42, inner_radius=0.2, stroke_color=BAD, fill_color=BAD,
                           fill_opacity=0.4), MathTex(r"\bot", font_size=34, color=BAD)).move_to([3.8, 0.2, 0])
        boom[1].move_to(boom[0])
        conf_arrows = VGroup()
        for x in conf_clause:
            src = nodes[-x]
            if abs(src.get_y() - boom.get_y()) < 0.1 and src.get_x() < pos[4][0]:  # a: arc below the graph
                conf_arrows.add(CurvedArrow(src.get_bottom() + DOWN * 0.05, boom.get_bottom() + DOWN * 0.05,
                                            angle=PI / 3, color=BAD, stroke_width=3, tip_length=0.2))
            else:
                conf_arrows.add(Arrow(src.get_center(), boom.get_center(), buff=0.4, color=BAD, stroke_width=3,
                                      max_tip_length_to_length_ratio=0.12))
        lvl = label(r"decision level 1", font_size=22, color=CONN).next_to(nodes[1], UP, buff=0.25)
        conf_l = MathTex(clause_tex(frozenset(conf_clause), list(FN)), r"\text{ fails}", font_size=30, color=BAD)
        conf_l.next_to(boom, DOWN, buff=0.3)
        learned = MathTex(lt(ev[7]["lit"][0]), font_size=48, color=LEARN)
        ll = VGroup(label(r"learned clause:", font_size=26, color=LEARN), learned).arrange(RIGHT, buff=0.3)
        ll.to_edge(DOWN, buff=1.2)
        cut = DashedLine([-4.6, 2.2, 0], [-4.6, -1.8, 0], color=LEARN, stroke_width=3)
        with self.voiceover(
            f"Watch it on a formula of {len(clauses)} clauses in eight atoms, the Reasoner's own run. "
            "<bookmark mark='a'/>First decision: a is true. <bookmark mark='b'/>Propagation follows. a forces b, and "
            "c. b and c together force d. d forces e. d and e force f. <bookmark mark='c'/>Draw each forced value "
            "with arrows from the values that forced it, and you have the implication graph. <bookmark mark='d'/>"
            "Then a clause fails: not f or not a. Conflict."
        ) as vo:
            self.play(FadeIn(fm))
            vo.wait_until("a")
            self.play(FadeIn(nodes[1], scale=0.8), FadeIn(lvl))
            vo.wait_until("b")
            for e in ev[1:6]:
                l = e["lit"]
                self.play(*[GrowArrow(a) for a in edge_of[l]], FadeIn(nodes[l], scale=0.8),
                          Indicate(fm[e["clause"]], color=P.WORLD), run_time=0.9)
            vo.wait_until("c")
            self.play(Indicate(arrows, color=P.WORLD))
            vo.wait_until("d")
            self.play(*[Create(a) for a in conf_arrows], FadeIn(boom, scale=0.6), FadeIn(conf_l),
                      Indicate(fm[ev[6]["clause"]], color=BAD))
        with self.voiceover(
            "Now ask why. Trace the conflict back through the graph toward the decisions that caused it. "
            "<bookmark mark='a'/>Every path leads back to one cause: deciding a. <bookmark mark='b'/>So learn a clause "
            "that forbids that cause: not a. It follows from the formula, by resolving along the graph, so adding it "
            "rules out no satisfying valuation; but the solver will never make this mistake again, anywhere in the "
            "search."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(cut), *[a.animate.set_color(LEARN) for a in arrows],
                      nodes[1][0].animate.set_stroke(LEARN, width=4))
            vo.wait_until("b")
            self.play(FadeIn(ll, shift=UP * 0.2))
        rest = [e for e in ev[9:] if e["kind"] in ("propagate", "decide")]
        assert [(e["kind"][0], e["lit"]) for e in rest] == [("p", -1), ("p", 7), ("p", 8), ("p", 2), ("d", 4),
                                                            ("p", 5), ("p", 6), ("d", 3)]
        after = VGroup()
        for e in rest:
            l = e["lit"]
            after.add(node(l, CONN if e["kind"] == "decide" else (LEARN if l == -1 else P.WORLD),
                           decision=e["kind"] == "decide"))
        after.arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        model = d["model"]
        assert model is not None
        sat = label(r"every clause holds", font_size=28, color=OK).next_to(after, UP, buff=0.2)
        with self.voiceover(
            "Then jump back: not one step, but to the level where the learned clause first becomes useful, here "
            "the very top, before any decision. <bookmark mark='a'/>The learned clause forces not a at once. Then "
            "propagation forces g, h and b. Deciding d forces e and f, and one last decision, c, leaves every clause "
            "satisfied. One conflict, one lesson, and the search never returned to the dead end."
        ) as vo:
            lv = VGroup(label(r"level 1", font_size=26, color=CONN), MathTex(r"\longrightarrow", font_size=40,
                                                                              color=LEARN),
                        label(r"level 0", font_size=26, color=LEARN)).arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
            self.play(FadeOut(VGroup(*nodes.values(), arrows, conf_arrows, boom, conf_l, lvl, cut)),
                      ll.animate.to_corner(UR, buff=0.4).shift(DOWN * 0.9), FadeIn(lv), FadeIn(after[0], scale=0.8))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a, scale=0.8) for a in after[1:]], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(sat))
        self.clear_scene()

    def measure(self):
        rnd = load("solvers")["random"]
        ns = [r["n"] for r in rnd]
        G = axes([0, len(ns)], [0, 3.6], x_length=6.0, y_length=4.2, yticks=[0, 1, 2, 3],
                 yfmt=lambda v: f"10^{{{int(v)}}}", ylabel=r"decisions (median of seeds)", center=[-3.1, -0.6, 0])
        ax = G.ax
        bars = VGroup()
        for i, r in enumerate(rnd):
            for k, (key, col) in enumerate((("dpll_decisions_median", BAD), ("cdcl_decisions_median", OK))):
                v = np.log10(max(r[key], 1))
                h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
                b = Rectangle(width=0.4, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to(ax.c2p(i + 0.3 + 0.42 * k, 0), aligned_edge=DOWN)
                bars.add(b)
            G.add(MathTex(str(r["n"]), font_size=24, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12))
        xl = label(r"atoms, random 3-SAT at 4.26 clauses per atom", font_size=22, color=GREY_A).next_to(G, DOWN,
                                                                                                    buff=0.1)
        leg = legend([(BAD, r"DPLL"), (OK, r"CDCL")]).next_to(G, UP, buff=0.15).align_to(G, RIGHT)
        r50 = next(r for r in rnd if r["n"] == 50)
        seeds = r50["seeds"]
        notes_ = VGroup(
            label(rf"at 50 atoms: \ {r50['dpll_decisions_median']:.0f} decisions against "
                  rf"{r50['cdcl_decisions_median']:.0f}", font_size=24, color=GOAL),
            label(r"learned clauses are resolvents: \ CDCL is resolution in disguise", font_size=24),
            label(r"with restarts it can simulate any resolution proof", font_size=24),
            label(r"(Pipatsrisawat \& Darwiche 2011)", font_size=20, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.18)
        if notes_.width > 6.0:
            notes_.width = 6.0
        notes_.to_edge(RIGHT, buff=0.3).set_y(0.3)
        with self.voiceover(
            "Does learning pay? Here are random formulas at the ratio of clauses to atoms where they are hardest, "
            f"{seeds} formulas at each size, solved by the Reasoner's DPLL and its CDCL. <bookmark mark='a'/>As the "
            f"formulas grow, CDCL needs far fewer decisions: at fifty atoms, a median of "
            f"{r50['cdcl_decisions_median']:.0f}, against {r50['dpll_decisions_median']:.0f}. Industrial solvers add "
            "much more, and handle formulas with millions of atoms. <bookmark mark='b'/>Underneath is a deep fact: "
            "what CDCL learns are resolvents, so it is resolution in disguise. With restarts it can simulate any "
            "resolution proof, as Knot Pipatsrisawat and Adnan Darwiche showed in 2011. Which means that whatever "
            "makes resolution slow makes CDCL slow too. That is the next chapter."
        ) as vo:
            self.play(FadeIn(G), FadeIn(xl), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(notes_[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n) for n in notes_[1:]], lag_ratio=0.3))
        self.clear_scene()
