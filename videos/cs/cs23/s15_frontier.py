from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.fast()
        self.hirsch()
        self.hardness()
        self.open_()

    def card(self):
        card = chapter_card(14, r"Frontier: \ faster LPs, \ the Hirsch question \ and the UGC",
                            r"What is still open about optimization?", lit=(2010, 2022),
                            extra=((2010, r"Santos"), (2022, r"almost-linear max flow")), part=PART)
        with self.voiceover("Chapter fourteen. Frontier: faster linear programs, the Hirsch question, and the unique "
                            "games conjecture."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fast(self):
        head = label(r"How fast can a linear program be solved?", font_size=32).to_edge(UP, buff=0.35)
        bars = VGroup(
            label('selected dense-LP arithmetic bounds; \\ dated results, \\ not a speed benchmark', font_size=22, color=WHITE),
            MathTex(r'O((n^{\omega}+n^{2.5-\alpha/2}+n^{2+1/6})\log(n/\delta))', font_size=31, color=HEAD),
            label('Cohen--Lee--Song (2019): \\ at the published exponent estimates, \\ the $n^\\omega$ term dominates', font_size=22, color=YES),
            label('van den Brand: \\ a related deterministic bound; \\ reading dense input already needs $\\Omega(n^2)$ entries', font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=.26).next_to(head, DOWN, buff=.45)
        if bars.width > 13: bars.width=13
        cap = label('$\\alpha$: \\ rectangular matrix exponent; \\ $\\delta$: \\ accuracy; \\ retain input scaling assumptions',font_size=19,color=GREY_A).next_to(bars,DOWN,buff=.3)
        notes = VGroup(*[label(text,font_size=21,color=color) for text,color in (
            ('maintain successive Newton systems; \\ arithmetic work is distinct from bit complexity',WHITE),('the full bound has additional exponent terms and a log accuracy factor',YES),
            ('Chen et al. (2022): \\ exact directed max flow and min-cost flow in $m^{1+o(1)}$',LAM),('polynomially bounded integral data; \\ theorem algorithms are not executed here',LAM),
        )]).arrange(DOWN,buff=.23).next_to(cap,DOWN,buff=.35)
        if notes.width > 13: notes.width=13
        with self.voiceover(
            (
            "The first frontier is complexity under a stated input model. <bookmark mark='a'/> Interior-point "
            'advances reduce both iteration count and the cost of maintaining successive linear systems. '
            "Arithmetic-operation bounds and bit complexity are different. <bookmark mark='b'/> The selected "
            '2019 Cohen-Lee-Song result gives a dense-LP bound involving n to omega, two additional exponent '
            "terms, and a log accuracy factor. At the paper's exponent estimates the matrix-multiplication term "
            'dominates. Van den Brand gives a related deterministic bound. These dated theorems do not make '
            "every LP inherently equivalent to one matrix product. <bookmark mark='c'/> The selected 2022 "
            'six-author flow result gives almost-linear exact directed max-flow and min-cost flow for '
            "polynomially bounded integral input data. <bookmark mark='d'/> Dynamic graph and interior-point "
            'machinery are central to that result. The input assumptions and hidden factors belong to the '
            'theorem; none of these asymptotic algorithms is executed by our small Python examples.'
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]), FadeIn(cap),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(bars[3]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def hirsch(self):
        f = load("frontier")
        d = f["draw"]
        V = [tuple(v) for v in d["V"]]
        head = label(r"How long can the walk be? \ The Hirsch conjecture", font_size=30).to_edge(UP, buff=0.3)
        view = View3(origin=np.array([-3.6, -0.4, 0]), scale=1.45, th=-0.5, ph=0.4)
        path = d["path"]

        def scene3():
            g = view.polytope(V, d["faces"], color=DATA, opacity=0.14, width=1.4)
            pth = VGroup(*[Line(view.p(V[a]), view.p(V[b]), color=HEAD, stroke_width=4.5)
                           for a, b in zip(path, path[1:])])
            ends = VGroup(Dot(view.p(V[path[0]]), radius=0.08, color=YES), Dot(view.p(V[path[-1]]), radius=0.08,
                                                                               color=NO))
            return VGroup(g, pth, ends)
        poly = always_redraw(scene3)
        cap = label(rf"{d['facets']} random facets, \ {d['vertices']} vertices: \ the two farthest vertices are "
                    rf"{d['diam']} edges apart", font_size=18, color=GREY_A).to_corner(DL, buff=0.4)
        rows = [[str(r["n"]), str(r["hirsch"]), f"{r['mean_diam']:.1f}", str(r["max_diam"])] for r in f["rows"]]
        tab = grid_table([r"facets $n$", r"Hirsch: $n - 3$", r"mean diameter", r"worst"], rows,
                         widths=[1.5, 2.0, 2.0, 1.1], row_h=0.38, font_size=19, mono_cols=(),
                         colors=[[WHITE, NO, YES, GREY_A]] * len(rows))
        tab.to_edge(RIGHT, buff=0.35).shift(UP * 1.35)
        tcap = label('20 certified bounded 3D samples per size; \\ rejected draws retained', font_size=17, color=GREY_A).next_to(tab, UP, buff=0.12)
        notes = VGroup(
            label(r"Hirsch \ (1957): \ any two vertices of a $d$-polytope with $n$ facets \\ are at most $n - d$ edges "
                  r"apart", font_size=20, color=WHITE),
            label(r"\textbf{false}: \ Santos \ (2010), \ a 43-dimensional polytope with 86 facets \\ and diameter "
                  r"at least 44", font_size=20, color=NO),
            label('historical: \\ Kalai--Kleitman (1992); \\\\ Todd (2014) refines to $(n-d)^{\\log_2 d}$',
                  font_size=20, color=HEAD),
            label(r"\textbf{polynomial Hirsch}: \ is the diameter at most a polynomial in $n$ and $d$? \\ No simplex "
                  r"rule can be polynomial unless it is", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        room = 7.0 - notes.get_left()[0]
        if notes.width > room:
            notes.width = room
            notes.next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        with self.voiceover(
            (
            "The second frontier concerns paths along polytope edges. <bookmark mark='a'/> Our drawn bounded "
            'three-dimensional polytope has twenty-four facets, forty-four vertices and diameter eight. '
            "Independent breadth-first searches check every vertex's eccentricity. <bookmark mark='b'/> Hirsch "
            "conjectured diameter at most facets minus dimension. <bookmark mark='c'/> Each displayed row "
            'contains twenty seeded, certified bounded three-dimensional samples. We reject uncertified draws '
            'before construction; these finite means support no universal growth law or high-dimensional claim. '
            "<bookmark mark='d'/> Santos disproved the original conjecture with a forty-three-dimensional "
            "example having eighty-six facets and diameter at least forty-four. <bookmark mark='e'/> Kalai and "
            "Kleitman's 1992 quasipolynomial bound is historical, not the latest bound. Todd's 2014 refinement "
            "is at most n minus d to the power log base two d. <bookmark mark='f'/> A polynomial general "
            'diameter bound would be necessary but not sufficient for an efficient pivot rule: the rule must '
            'also find appropriate objective-improving paths. Our exercise compares finite routing rules without '
            'attempting to settle the open conjecture.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(poly))
            vo.wait_until("a")
            self.play(FadeIn(cap), view.th.animate.set_value(0.9), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(tcap), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25),
                      view.th.animate.set_value(2.2), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(FadeIn(notes[3]), view.th.animate.set_value(3.2), run_time=3.0)
        self.wait(0.3)
        poly.clear_updaters()
        self.clear_scene()

    def hardness(self):
        head = label(r"How good can an approximation be?", font_size=32).to_edge(UP, buff=0.35)
        rows = [[r"vertex cover", r"$2$", r"$\sqrt2$ \ (Khot, \ Minzer, \ Safra 2018)", r"$2$ \ (Khot--Regev)"],
                [r"MAX-CUT", r"$0.878$", r"$16/17 \approx 0.941$ \ (H\aa stad)", r"$0.878$ \ (KKMO)"],
                [r"MAX-3SAT", r"$7/8$", r"$7/8$ \ (H\aa stad 2001)", r"---"],
                [r"set cover", r"$\ln n$", r"$(1 - \varepsilon)\ln n$ \ (Dinur--Steurer)", r"---"],
                [r"metric TSP", '$1.5-\\varepsilon$ (2021)', r"$123/122$ \ (Karpinski et al.)", r"---"]]
        tab = grid_table([r"problem", 'selected guarantee', r"NP-hard to beat", r"hard if UGC holds"], rows,
                         widths=[2.3, 2.3, 4.6, 3.0], row_h=0.46, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, NO, LAM]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label('PCP: \\ polynomial NP-witness encoding; \\ constant queries; \\ completeness and soundness gap', font_size=21, color=WHITE),
            label(r"so approximating past a threshold is as hard as solving: \ Part 27 builds it", font_size=21,
                  color=NO),
            label(r"Khot's \textbf{unique games conjecture} \ (2002): \ one more step, \ and many gaps close "
                  r"exactly", font_size=21, color=LAM),
            label('Raghavendra (2008), \\ under UGC: \\ appropriate SDP rounding is optimal for each fixed finite-domain CSP', font_size=21, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            (
            "The third frontier asks how close polynomial algorithms can get. <bookmark mark='a'/> The table "
            'distinguishes selected algorithmic guarantees, unconditional NP-hardness thresholds and conditional '
            "Unique Games thresholds; fixed epsilon qualifications matter. <bookmark mark='b'/> The PCP theorem "
            'gives polynomial-size encodings of NP witnesses with a randomized verifier using logarithmically '
            'many random bits and constantly many queries. Completeness and a fixed soundness gap concern valid '
            "versus false statements, not perfect error detection in arbitrary proofs. <bookmark mark='c'/> Gap "
            "reductions yield approximation hardness, including Håstad's seven-eighths-plus-epsilon barrier for "
            "MAX-3SAT unless P equals NP. <bookmark mark='d'/> Under the Unique Games Conjecture the "
            'corresponding fixed-factor thresholds for vertex cover and MAX-CUT match their standard '
            'approximation guarantees. The two-to-two theorem yields a separate vertex-cover hardness result. '
            "<bookmark mark='e'/> Raghavendra's conditional optimality theorem concerns each fixed finite-domain "
            'constraint-satisfaction problem and its appropriate SDP rounding framework, not every problem '
            'called constraint satisfaction with unrestricted representation.'
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            for mk, n_ in zip("bcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label(r"a \textbf{strongly} polynomial algorithm for LP: \ steps depending on the size, \ not the bits \ "
                  r"(Smale's 9th problem)", font_size=23, color=NO),
            label(r"the polynomial Hirsch conjecture, \ or a polytope that defeats it", font_size=23, color=HEAD),
            label(r"is the unique games conjecture true?", font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.8)
        if qs.width > 13.0:
            qs.width = 13.0
        star = label('$\\bigstar$ \\ finite study: \\ bounded samples, \\ BFS distances and a specified routing rule', font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            (
            "Three questions organize this frontier. <bookmark mark='a'/> Strongly polynomial LP asks for an "
            'arithmetic-operation count polynomial in dimensions and independent of coefficient bit lengths, '
            'while also controlling intermediate encoding size. This is not a claim that reading '
            "arbitrary-precision input is free. <bookmark mark='b'/> A general polynomial bound on polytope "
            "diameter remains a separate geometric question. <bookmark mark='c'/> The Unique Games Conjecture "
            "governs conditional approximation thresholds. <bookmark mark='d'/> Our research-style exercise "
            'stays finite: generate certified bounded polytopes, compute exact graph distances, and compare a '
            'specified routing rule with shortest paths. Report seeds, failures and model limits; a successful '
            'finite experiment does not settle any of these open questions.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
