from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

POS9 = [(-5.8, 1.4), (-4.6, 2.2), (-4.4, 0.8), (-3.2, 0.2), (-2.6, 1.6), (-1.8, 0.2), (-2.4, -1.2), (-3.8, -1.6),
        (-1.4, -2.2)]


class Approximation(VoiceoverScene):
    def construct(self):
        self.card()
        self.vertex_cover()
        self.measured()
        self.set_cover()

    def card(self):
        card = chapter_card(8, r"Approximation: \ covers", r"Can we be provably close when exact is hopeless?",
                            lit=(1974, 1979), extra=((1974, r"Johnson's greedy bound"), (1979, r"Chv\'atal")),
                            part=PART)
        with self.voiceover("Chapter eight. Approximation: covers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def graph(self, d, hl=(), col=YES):
        P = [np.array([x, y, 0]) for x, y in POS9]
        E = [tuple(e) for e in d["E"]]
        lines = VGroup(*[Line(P[u], P[v], buff=0.22, color=GREY_B, stroke_width=2) for u, v in E])
        nodes = VGroup(*[Circle(radius=0.22, color=col if i in hl else DATA, fill_opacity=0.8 if i in hl else 0.0)
                         .move_to(P[i]) for i in range(len(P))])
        return lines, nodes, P, E

    def vertex_cover(self):
        a = load("approx")
        d = a["draw"]
        head = label(r"Vertex cover: \ two ways to be within 2", font_size=32).to_edge(UP, buff=0.3)
        lines, nodes, P, E = self.graph(d)
        # the maximal matching the algorithm picked: pairs inside its cover
        mt = set(d["matching"])
        chosen = []
        used = set()
        for u, v in E:
            if u in mt and v in mt and u not in used and v not in used:
                chosen.append((u, v))
                used |= {u, v}
        mlines = VGroup(*[Line(P[u], P[v], buff=0.22, color=HEAD, stroke_width=5) for u, v in chosen])
        mnodes = VGroup(*[Circle(radius=0.22, color=HEAD, fill_opacity=0.7).move_to(P[i]) for i in sorted(mt)])
        onodes = VGroup(*[Circle(radius=0.26, color=YES, stroke_width=4).move_to(P[i]) for i in d["opt_set"]])
        halves = VGroup(*[MathTex(r"\tfrac12", font_size=24, color=LAM).next_to(P[i], UP, buff=0.22)
                          for i in range(len(P))])
        side = VGroup(
            label(r"choose vertices touching every edge; \ fewest possible: \ NP-hard", font_size=21, color=WHITE),
            label(r"\textbf{matching}: \ take an uncovered edge, \ add \textbf{both} ends, \ repeat", font_size=21,
                  color=HEAD),
            label(r"those edges share no vertex, \ and any cover needs one end of each: \\ so $|C| = 2|M| \le 2\,"
                  r"\mathrm{OPT}$", font_size=21, color=HEAD),
            label(rf"here: \ {len(mt)} vertices, \ against the optimum {d['opt']} \ (green rings)", font_size=21,
                  color=YES),
            label(r"\textbf{LP rounding}: \ $\min \sum x_v$, \ $x_u + x_v \ge 1$; \ keep every $x_v \ge \tfrac12$",
                  font_size=21, color=LAM),
            label(rf"the LP is half-integral: \ here all $\tfrac12$, \ value {d['lp']:.1f} $\le$ OPT; \\ rounding keeps "
                  rf"all {len(d['rounded'])}: \ $\le 2 \cdot \mathrm{{LP}} \le 2\,\mathrm{{OPT}}$", font_size=21,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 6.8:
            side.width = 6.8
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "When the exact answer is out of reach, ask for an answer provably close to it. <bookmark mark='a'/> A "
            "vertex cover is a set of vertices touching every edge, and finding the smallest one is NP-hard. "
            "<bookmark mark='b'/> Here is a two-line algorithm. Take any edge whose ends are both uncovered and add "
            "both ends. Repeat until every edge is covered. <bookmark mark='c'/> The edges it took share no vertex, "
            "and any cover at all must contain at least one end of each of them, so the optimum is at least half "
            "of what we took. That is a factor two guarantee, proved without knowing the optimum. <bookmark mark='d'/> "
            "Here it takes eight vertices, against an optimum of six. <bookmark mark='e'/> The second way uses the "
            "linear program: give each vertex a fraction, require each edge's two fractions to sum to at least one, "
            "and minimize the total. Then keep every vertex whose fraction is at least a half. <bookmark mark='f'/> "
            "The relaxation's vertices only take the values zero, a half and one. Here it puts a half everywhere, "
            "four and a half in all, a lower bound on the optimum, and rounding keeps all nine. Again at most twice "
            "the linear program, so at most twice the optimum."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), LaggedStart(*[Create(x) for x in mlines], lag_ratio=0.4), FadeIn(mnodes))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(onodes))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeOut(mlines), FadeOut(mnodes))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), FadeIn(halves))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        a = load("approx")
        vc = a["vc"]
        head = label(r"Measured on 100 random graphs", font_size=34).to_edge(UP, buff=0.35)
        mr = [r["matching"] / r["opt"] for r in vc]
        rr = [r["rounded"] / r["opt"] for r in vc]
        lr = [r["lp"] / r["opt"] for r in vc]
        rows = [[r"maximal matching", f"{np.mean(mr):.2f}", f"{max(mr):.2f}"],
                [r"LP rounding", f"{np.mean(rr):.2f}", f"{max(rr):.2f}"],
                [r"the LP itself \ (a lower bound)", f"{np.mean(lr):.2f}", f"{min(lr):.2f} \\ (min)"]]
        tab = grid_table([r"16 vertices, \ $p = 0.25$", r"mean ratio to OPT", r"worst"], rows, widths=[4.4, 3.0, 2.0],
                         row_h=0.5, font_size=22, mono_cols=(), colors=[[HEAD, HEAD, HEAD], [LAM, LAM, LAM],
                                                                         [GREY_A, GREY_A, GREY_A]])
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        notes = VGroup(
            label('finite ratios stay within 2; \\ tightness depends on the graph and actual tie policy', font_size=22, color=WHITE),
            label(r"nothing better than $2 - \varepsilon$ is known; \ under the Unique Games Conjecture, \ nothing better "
                  r"exists \ (Khot and Regev, 2008)", font_size=22, color=NO),
            label(r"the LP's integrality gap is 2: \ on a complete graph, \ $\mathrm{LP} = n/2$ \ but \ "
                  r"$\mathrm{OPT} = n - 1$", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            (
            'We checked both methods on a hundred seeded sixteen-vertex graphs against exhaustive optima. '
            "<bookmark mark='a'/> Their finite ratios stay within two. Tightness needs the right examples and "
            "the actual tie policy; it does not follow from this table. <bookmark mark='b'/> Khot and Regev "
            'show, assuming the Unique Games Conjecture, hardness for every fixed factor two minus epsilon. That '
            "is a conditional asymptotic statement, not a limit measured by our sample. <bookmark mark='c'/> On "
            'the complete graph the fractional cover value is n over two and the integer optimum n minus one. '
            'Their ratio approaches two as n grows. This relaxation therefore cannot certify a uniformly smaller '
            'factor on all graphs.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            for mk, n_ in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def set_cover(self):
        a = load("approx")
        head = label(r"Set cover: \ greedy, \ and the harmonic number", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"cover a universe of $n$ elements with the fewest of some given sets", font_size=22, color=WHITE),
            label(r"greedy: \ take the set covering the most uncovered elements; \ repeat", font_size=22, color=LAM),
            MathTex(r"|\text{greedy}| \;\le\; H_n \cdot \mathrm{OPT}, \qquad H_n = 1 + \tfrac12 + \cdots + \tfrac1n "
                    r"\approx \ln n", font_size=32, color=YES),
            label(r"proof: \ charge each element $1/(\text{its set's new elements})$; \ the optimal sets' $k$-th "
                  r"newest element pays at most $1/k$ of OPT's share", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.4)
        rows = [[str(r["n"]), str(r["opt"]), str(r["greedy"])] for r in a["setcover"]]
        tab = grid_table([r"elements", r"OPT", r"greedy"], rows, widths=[2.0, 1.4, 1.6], row_h=0.4, font_size=21,
                         mono_cols=(), colors=[[WHITE, YES, NO]] * len(rows))
        cap = label(r"the trap: \ two rows cover all; \\ greedy takes columns of sizes \\ $2^{k-1}, \dots, 4, 2$ "
                    r"instead", font_size=19, color=GREY_A)
        g = VGroup(tab, cap).arrange(RIGHT, buff=0.5).next_to(lines, DOWN, buff=0.4)
        rs = a["random_setcover"]
        foot = VGroup(
            label(rf"on {len(rs)} random instances: \ greedy averaged {np.mean([r['greedy'] / r['opt'] for r in rs]):.2f} "
                  rf"$\times$ OPT, \ worst {max(r['greedy'] / r['opt'] for r in rs):.2f}", font_size=21, color=WHITE),
            label('Dinur--Steurer (2014): \\ fixed $\\varepsilon>0$, \\ $(1-\\varepsilon)\\ln n$ hardness unless $P=NP$', font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Set cover asks for the fewest sets covering every element. <bookmark mark='a'/> Greedy chooses a "
            'set covering the most currently uncovered elements. Our domain rejects families that cannot cover '
            "the universe. <bookmark mark='b'/> The classic guarantee is H n times optimum, with n the universe "
            "size. <bookmark mark='c'/> Charge each newly covered element an equal share of its chosen set's "
            'unit cost. Elements of any optimum set pay at most the harmonic sum, so all chosen costs total at '
            "most H n times OPT. <bookmark mark='d'/> The retained doubling-column examples have optimum two; "
            'their actual greedy choices and all sixty random instances are checked by an independent '
            "subset-union dynamic program. <bookmark mark='e'/> Selected hardness results have distinct "
            "premises: Feige's 1998 threshold uses a stronger complexity assumption, while Dinur and Steurer "
            'establish fixed-epsilon logarithmic NP-hardness. Observed small average gaps do not weaken these '
            'worst-case statements.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abc", lines[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            self.play(FadeIn(lines[3]))
            vo.wait_until("d")
            self.play(FadeIn(g))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
