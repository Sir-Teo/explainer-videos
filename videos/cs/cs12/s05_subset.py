from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)

NAMES = "ABCDE"
POS5 = {"A": (-5.2, -0.2), "B": (-1.9, 1.3), "C": (-1.9, -1.7), "D": (1.6, 1.3), "E": (4.9, 1.3)}


def dfa5(delta, accept):
    edges = []
    bend = {("A", "B"): 0, ("A", "C"): 0, ("B", "D"): 0, ("D", "E"): 0, ("C", "B"): 0.35, ("D", "B"): -1.0,
            ("E", "B"): 0.8, ("E", "C"): -0.5}
    loops = {"B": UP, "C": DOWN}
    for s, row in enumerate(delta):
        for a, t in row.items():
            S, T = NAMES[s], NAMES[t]
            edges.append((S, T, a, loops.get(S) if S == T else bend.get((S, T), 0)))
    return StateDiagram(POS5, edges, radius=0.42, font_size=24, edge_font=19, accept=tuple(NAMES[k] for k in accept))


class Subset(VoiceoverScene):
    def construct(self):
        self.card()
        self.subsets()
        self.minimize()
        self.blowup()
        self.nerode()
        self.lazy()

    def card(self):
        card = chapter_card(4, r"The subset construction", r"Can a deterministic machine do what an NFA does?",
                            lit=(1959,), extra=((1959, r"Rabin and Scott"),), part=PART)
        with self.voiceover("Chapter four. The subset construction, and minimization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def subsets(self):
        s = load("subset")
        d = s["dfa"]
        head = label(r"Make each \textit{set} of NFA states one DFA state", font_size=34).to_edge(UP, buff=0.3)
        sd = dfa5(d["delta"], d["accept"]).shift(DOWN * 0.2)
        names = VGroup()
        for k, S in enumerate(d["sets"]):
            names.add(Text(f"{NAMES[k]} = {{{', '.join(map(str, S))}}}", font="DejaVu Sans Mono", font_size=15,
                           color=DATA if k not in d["accept"] else YES))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DR, buff=0.35)
        order = ["A", "B", "C", "D", "E"]
        note_ = label(r"Rabin and Scott, \ 1959: \ every NFA has an equivalent DFA", font_size=20,
                      color=HEAD).to_corner(DL, buff=0.35)
        with self.voiceover(
            "The simulation of the last chapter suggests something. At any moment the NFA is in some set of "
            "states, and which set it is in next depends only on that set and the next character. <bookmark "
            "mark='a'/> So make each set one state of a new, deterministic machine. The start state A is the set "
            "the simulation started with. <bookmark mark='b'/> From A, reading an a or a b gives two new sets, B "
            "and C; from those, more; and so on, until no new sets appear. For a b star a b b, only five of the "
            "sixteen thousand possible subsets ever turn up. <bookmark mark='c'/> A set is accepting if it "
            "contains the NFA's accepting state, here only E. This is the subset construction, published by "
            "Michael Rabin and Dana Scott in 1959; it was part of the work that won them the Turing Award."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sd.node["A"]), FadeIn(names[0]))
            vo.wait_until("b")
            for X in order[1:]:
                k = NAMES.index(X)
                es = [e for e in sd.edge if e.dst == X and NAMES.index(e.src) < k]
                self.play(FadeIn(sd.node[X]), *[FadeIn(e) for e in es], FadeIn(names[k]), run_time=0.8)
            rest = [e for e in sd.edge if not (NAMES.index(e.src) < NAMES.index(e.dst))]
            self.play(*[FadeIn(e) for e in rest])
            vo.wait_until("c")
            self.play(Indicate(sd.node["E"], color=YES), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def minimize(self):
        s = load("subset")
        d = s["dfa"]
        rounds = s["rounds"]
        head = label(r"Minimization: \ merge states no string can tell apart", font_size=34).to_edge(UP, buff=0.3)
        sd = dfa5(d["delta"], d["accept"]).scale(0.8).shift(UP * 0.95)
        palette = [GREY_B, YES, CTRL, FUNC, DATA]
        steps = VGroup(
            label(r"round 0: \ accepting \ $\{E\}$ \ against the rest \ $\{A, B, C, D\}$", font_size=20, color=GREY_A),
            label(r"round 1: \ $D$ reaches $E$ on \texttt{b}, \ the others do not: \ split off $\{D\}$",
                  font_size=20, color=GREY_A),
            label(r"round 2: \ $B$ reaches $D$ on \texttt{b}: \ split off $\{B\}$", font_size=20, color=GREY_A),
            label(r"round 3: \ nothing splits. \ $A$ and $C$ behave identically on every string: \ merge them",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)

        def paint(k):
            r = rounds[min(k, len(rounds) - 1)]
            return [sd.node[NAMES[i]].circle.animate.set_fill(palette[r[i] % len(palette)], opacity=0.45)
                    for i in range(5)]
        res = label(rf"{s['dfa']['n']} states $\to$ {s['minimal']['n']}: \ the smallest DFA for this language, \ "
                    r"and it is unique", font_size=21, color=HEAD).next_to(steps, UP, buff=0.3)
        with self.voiceover(
            "The machine is correct, but not always as small as it could be. <bookmark mark='a'/> Two states are "
            "equivalent if every possible remaining input leads both to accept or both to reject. Edward Moore's "
            "algorithm finds them. Start by separating the accepting states from the rest. <bookmark mark='b'/> "
            "Then look at where each state's arrows go. D, on a b, reaches the accepting group; A, B and C do not. "
            "So D is different: split it off. <bookmark mark='c'/> Now B reaches D on a b, and A and C do not: "
            "split again. <bookmark mark='d'/> Now nothing splits. A and C go to the same groups on every symbol, "
            "so no string can ever tell them apart, and they merge. <bookmark mark='e'/> Four states: and the "
            "Myhill–Nerode theorem says this minimal machine is unique, the same whichever way you started."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd))
            vo.wait_until("a")
            self.play(*paint(0), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(*paint(1), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(*paint(2), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), Indicate(sd.node["A"], color=YES), Indicate(sd.node["C"], color=YES))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def blowup(self):
        s = load("subset")
        rows = s["blowup"]
        head = label(r"The price: \ sometimes $2^n$ states", font_size=36).to_edge(UP, buff=0.3)
        lang = label(r"$L_n$: \ strings over $\{0, 1\}$ whose $n$-th symbol from the end is 1", font_size=22,
                     color=GREY_A).next_to(head, DOWN, buff=0.3)
        rx = Text("(0|1)*1(0|1)(0|1)...", font="DejaVu Sans Mono", font_size=20, color=CODE).next_to(lang, DOWN,
                                                                                                   buff=0.2)
        ax = Axes(x_range=[0, 12.5, 2], y_range=[0, 4, 1], x_length=6.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=1.0).shift(DOWN * 1.2)
        yl = VGroup(*[label(t, font_size=14, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v, t in ((0, "1"), (1, "10"), (2, "100"), (3, "1,000"), (4, "10,000"))])
        xl = label(r"$n$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        xt = VGroup(*[label(str(n), font_size=14, color=GREY_B).next_to(ax.c2p(n, 0), DOWN, buff=0.08)
                      for n in range(2, 13, 2)])
        nfa = VMobject(color=DATA, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], math.log10(r["nfa"])) for r in rows])
        dfa = VMobject(color=NO, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], math.log10(r["minimal"])) for r in rows])
        nl = label(r"NFA: \ $n + 1$ states", font_size=19, color=DATA).next_to(ax.c2p(12, math.log10(13)), UP,
                                                                            buff=0.15).shift(LEFT * 0.8)
        dl = label(r"smallest DFA: \ $2^n$", font_size=19, color=NO).next_to(ax.c2p(10.5, 3.6), LEFT, buff=0.1)
        last = rows[-1]
        tab = VGroup(label(r"computed here, \ $n = 12$:", font_size=20, color=GREY_B),
                     label(rf"Thompson NFA: \ {last['thompson']} states", font_size=20, color=DATA),
                     label(rf"subset construction: \ {last['dfa']:,}", font_size=20, color=CTRL),
                     label(rf"minimized: \ {last['minimal']:,} $= 2^{{12}}$", font_size=20, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, RIGHT, buff=0.9).shift(UP * 0.4)
        with self.voiceover(
            "Determinism has a price. <bookmark mark='a'/> Take the strings of zeros and ones whose n-th symbol "
            "from the end is a one. An NFA for it is tiny: it guesses when the last n symbols begin, and checks. "
            "It needs n plus one states. <bookmark mark='b'/> But the smallest deterministic machine has two to the "
            "n. We built them all here: <bookmark mark='c'/> for n equals twelve, the subset construction gives "
            "four thousand and ninety-seven states, and minimizing removes just one of them. The guess an NFA gets "
            "for free, a DFA has to pay for in memory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lang), FadeIn(rx))
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(xt), Create(nfa), FadeIn(nl))
            vo.wait_until("b")
            self.play(Create(dfa), FadeIn(dl), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in tab], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    def nerode(self):
        m = load("myhill")
        head = label(r"Why no DFA can do better \ (Myhill and Nerode, \ 1957--58)", font_size=32).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"take two different $n$-bit strings $u \neq v$; \ say they first differ at position $i$", font_size=21,
                  color=GREY_A),
            label(r"append $z = 0^{i}$: \ now that position is $n$-th from the end, \ 1 in one string, \ 0 in "
                  r"the other", font_size=21, color=GREY_A),
            label(r"so $uz \in L_n$ and $vz \notin L_n$ \ (or the reverse): \ after reading $u$ and $v$ the machine "
                  r"must be in \textit{different} states", font_size=21, color=HEAD),
            label(r"$2^n$ strings, \ pairwise distinguishable \ $\Rightarrow$ \ at least $2^n$ states", font_size=23,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.4)
        ex = []
        for k, (pair, d) in enumerate(m["table"].items()):
            if k in (0, 1, 3, 9):
                u, v = pair.split(",")
                z = d["z"] or "ε"
                ex.append([u, v, z, r"yes" if d["u"] else r"no", r"yes" if d["v"] else r"no"])
        t = grid_table([r"$u$", r"$v$", r"$z$", r"$uz \in L_3$", r"$vz \in L_3$"], ex, [1.4, 1.4, 1.2, 1.8, 1.8],
                       row_h=0.45, font_size=19, colors=[[CODE, CODE, HEAD, GREY_A, GREY_A]] * len(ex),
                       mono_cols=(0, 1, 2)).next_to(pts, DOWN, buff=0.4)
        cap = label(rf"all {len(m['table'])} pairs of 3-bit strings checked: \ every one is told apart", font_size=19,
                    color=GREY_B).next_to(t, DOWN, buff=0.15)
        with self.voiceover(
            "And no cleverer machine exists; the reason is the Myhill–Nerode theorem. <bookmark mark='a'/> Take "
            "any two different strings of n bits, and suppose they first differ at position i. <bookmark mark='b'/> "
            "Append i zeros. Now that position is exactly n-th from the end: a one in one string and a zero in the "
            "other. <bookmark mark='c'/> So one extended string is in the language and the other is not, and a "
            "machine that had reached the same state after both would give the same answer to both. It must keep "
            "them apart. <bookmark mark='d'/> Two to the n strings, every pair distinguishable: at least two to the "
            "n states. We checked every pair for n equals three."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]), FadeIn(t), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def lazy(self):
        lz = load("lazy")
        head = label(r"In practice: \ build the DFA lazily", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"grep and RE2 run the NFA simulation, \ but remember every state set they meet, \ with its "
                  r"transitions: \ a DFA built on demand", font_size=20, color=GREY_A),
            label(rf"on the first {lz['chars']:,} characters of \textit{{Pride and Prejudice}}: \ ``the $n$-th "
                  r"character back is \texttt{e}''", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.4)
        rows = [[str(r["n"]), f"{r['possible']:,}", f"{r['built']:,}",
                 f"{100 * r['built'] / r['possible']:.1f}\\%"] for r in lz["rows"]]
        t = grid_table([r"$n$", r"states possible \ ($2^n$)", r"states the text reached", r"share"], rows,
                       [1.0, 3.4, 3.8, 1.8], row_h=0.5, font_size=20, colors=[[GREY_A, NO, YES, HEAD]] * len(rows),
                       mono_cols=()).next_to(pts, DOWN, buff=0.45)
        ok = all(r["hits"] == r["check"] for r in lz["rows"])
        cap = label(rf"every match checked against counting the \texttt{{e}}'s directly: \ "
                    rf"{'all agree' if ok else 'disagree'}", font_size=19, color=GREY_B).next_to(t, DOWN, buff=0.2)
        punch = label(r"the worst case is real, \ but text is not the worst case: \ a cache of a few thousand states "
                      r"is enough", font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Real engines use a compromise. <bookmark mark='a'/> GNU grep and Google's RE2 run the NFA simulation, "
            "but remember each state set they meet, along with its transitions, so that the next time the text "
            "reaches it the step is a single table lookup. The DFA is built lazily, only where the text goes. "
            "<bookmark mark='b'/> We tried it on the first three hundred thousand characters of Pride and "
            "Prejudice, with the pattern: the n-th character back is an e. <bookmark mark='c'/> For n equals "
            "twelve, the text reaches six hundred and eighty-two of the four thousand and ninety-six possible "
            "states; for sixteen, about three thousand of sixty-five thousand. <bookmark mark='d'/> The worst case "
            "is real, but ordinary text is not the worst case, and a cache of a few thousand states is enough."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.4),
                      FadeIn(cap), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
