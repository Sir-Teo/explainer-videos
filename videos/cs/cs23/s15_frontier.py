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
        algs = [(r"Karmarkar \ (1984)", 3.5, NO), (r"Vaidya \ (1989)", 2.5, HEAD),
                (r"Cohen, \ Lee and Song \ (2019)", 2.372, YES), (r"just reading the input", 2.0, GREY_B)]
        sc = 1.9
        x0 = -2.2
        bars = VGroup()
        for k, (name, e, col) in enumerate(algs):
            y = 1.6 - 0.62 * k
            r = Rectangle(width=e * sc, height=0.38, stroke_width=0).set_fill(col, 0.75)
            r.move_to([x0 + e * sc / 2, y, 0])
            nm = label(name, font_size=20, color=col).next_to(r, LEFT, buff=0.25)
            ex = MathTex(rf"n^{{{e:g}}}", font_size=28, color=col).next_to(r, RIGHT, buff=0.2)
            bars.add(VGroup(r, nm, ex))
        cap = label(r"arithmetic for an LP with $n$ variables and $O(n)$ constraints, \ to fixed accuracy \ "
                    r"(logarithmic factors dropped)", font_size=18, color=GREY_A).next_to(bars, DOWN, buff=0.3)
        notes = VGroup(
            label(r"interior points \ (chapter 5), \ but the Newton steps barely change: \ \textbf{update} the inverse, "
                  r"\ don't recompute it", font_size=21, color=WHITE),
            label(r"$n^{\omega}$ with $\omega \approx 2.372$, \ the exponent of matrix multiplication: \ an LP is now "
                  r"as easy as one product \ (van den Brand, 2020)", font_size=21, color=YES),
            label(r"Chen, \ Kyng, \ Liu, \ Peng, \ Probst Gutenberg and Sachdeva \ (2022): \ \textbf{max flow in "
                  r"$m^{1 + o(1)}$ time}", font_size=21, color=LAM),
            label(r"an interior-point method on Part 18's flow LP, \ each step a tiny change kept up by dynamic data structures",
                  font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.22).next_to(cap, DOWN, buff=0.4)
        with self.voiceover(
            "The first front is speed. <bookmark mark='a'/> Karmarkar's method needed about n to the three and a half "
            "operations for a linear program with n variables. Pravin Vaidya brought it to n to the two and a half, with fewer steps and the "
            "observation that consecutive Newton steps barely change the matrix, so its inverse can be updated instead of "
            "recomputed. <bookmark mark='b'/> In 2019 Michael Cohen, Yin Tat Lee and Zhao Song pushed the idea to its "
            "natural end: n to the omega, where omega, about two point three seven, is the exponent of matrix "
            "multiplication. Jan van den Brand made it deterministic a year later. Solving a linear program now costs "
            "about as much as multiplying two matrices, and the floor, just reading the input, is n squared. "
            "<bookmark mark='c'/> The same machinery produced the biggest algorithms result of the decade. In 2022, "
            "Li Chen, Rasmus Kyng, Yang Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva solved "
            "maximum flow in almost linear time, m to the one plus a vanishing exponent. <bookmark mark='d'/> It is an "
            "interior-point method on Part 18's flow program, where each step changes the flow so little that clever "
            "dynamic data structures keep it up to date."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars[:2]], lag_ratio=0.4), FadeIn(cap),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2], shift=RIGHT * 0.2), FadeIn(bars[3], shift=RIGHT * 0.2), FadeIn(notes[1]))
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
        tcap = label(r"20 random 3D polytopes of each size", font_size=17, color=GREY_A).next_to(tab, UP, buff=0.12)
        notes = VGroup(
            label(r"Hirsch \ (1957): \ any two vertices of a $d$-polytope with $n$ facets \\ are at most $n - d$ edges "
                  r"apart", font_size=20, color=WHITE),
            label(r"\textbf{false}: \ Santos \ (2010), \ a 43-dimensional polytope with 86 facets \\ and diameter "
                  r"at least 44", font_size=20, color=NO),
            label(r"best upper bound: \ quasi-polynomial, \ $n^{\log_2 d + 2}$ \ (Kalai and Kleitman, 1992)",
                  font_size=20, color=HEAD),
            label(r"\textbf{polynomial Hirsch}: \ is the diameter at most a polynomial in $n$ and $d$? \\ No simplex "
                  r"rule can be polynomial unless it is", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        room = 7.0 - notes.get_left()[0]
        if notes.width > room:
            notes.width = room
            notes.next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        with self.voiceover(
            "The second front is the simplex method's own question. Could there be a pivot rule that always takes "
            "polynomially many steps? <bookmark mark='a'/> Then every polytope would have to have a short path "
            "between any two vertices. Here is one with twenty-four random facets and forty-four vertices; its two "
            "farthest vertices are eight edges apart. <bookmark mark='b'/> In 1957 Warren Hirsch conjectured that the "
            "distance is never more than the number of facets minus the dimension. <bookmark mark='c'/> On random "
            "polytopes it holds easily: the diameter grows roughly like the square root of the number of facets, far "
            "below the bound. <bookmark mark='d'/> But in 2010 Francisco Santos built a counterexample, a polytope in "
            "forty-three dimensions with eighty-six facets whose diameter is at least forty-four. <bookmark mark='e'/> "
            "The best upper bound known is not even polynomial: Gil Kalai and Daniel Kleitman's n to the log d plus "
            "two. <bookmark mark='f'/> Whether the diameter is bounded by some polynomial, the polynomial Hirsch "
            "conjecture, is open, and until it is settled nobody can hope to prove a simplex rule polynomial."
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
                [r"metric TSP", r"$1.5 - 10^{-36}$", r"$123/122$ \ (Karpinski et al.)", r"---"]]
        tab = grid_table([r"problem", r"best algorithm", r"NP-hard to beat", r"hard if UGC holds"], rows,
                         widths=[2.3, 2.3, 4.6, 3.0], row_h=0.46, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, NO, LAM]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label(r"the \textbf{PCP theorem} \ (1992): \ every proof can be checked by reading a constant number of "
                  r"its bits", font_size=21, color=WHITE),
            label(r"so approximating past a threshold is as hard as solving: \ Part 27 builds it", font_size=21,
                  color=NO),
            label(r"Khot's \textbf{unique games conjecture} \ (2002): \ one more step, \ and many gaps close "
                  r"exactly", font_size=21, color=LAM),
            label(r"Raghavendra \ (2008): \ if it holds, \ the SDP of chapter 10 is optimal for \textbf{every} "
                  r"constraint problem", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "The third front is the other side of approximation: proving that nothing does better. <bookmark "
            "mark='a'/> Here are this part's problems, with the best known algorithm and the thresholds below which "
            "approximation is known to be hard. <bookmark mark='b'/> The tool is the PCP theorem of 1992: any proof "
            "can be rewritten so that a verifier checking a few random bits catches any error with good probability. "
            "<bookmark mark='c'/> It turns approximation into decision: getting closer than a threshold would solve "
            "an NP-complete problem. Johan Håstad showed that for MAX-3SAT the trivial seven-eighths is exactly "
            "right. Part 27 builds the theorem. <bookmark mark='d'/> For the other problems there are gaps, and in "
            "2002 Subhash Khot proposed the unique games conjecture. If it is true, vertex cover cannot beat two and "
            "MAX-CUT cannot beat Goemans and Williamson's zero point eight seven eight, so both algorithms in this "
            "part are optimal. In 2018 Khot, Dor Minzer and Muli Safra proved a weaker cousin, the two-to-two "
            "theorem, which already makes vertex cover hard below the square root of two. <bookmark mark='e'/> And "
            "Prasad Raghavendra showed that if the conjecture holds, one semidefinite program is the best possible "
            "algorithm for every constraint satisfaction problem at once."
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
        star = label(r"$\bigstar$ \ the part's research problem takes the second", font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Is there a strongly polynomial algorithm for linear "
            "programming, one whose number of steps depends only on the numbers of variables and constraints, not on "
            "how many bits the coefficients have? Max flow has one; general linear programming does not, and Steve "
            "Smale listed the question among his problems for this century. <bookmark mark='b'/> Is the diameter of "
            "every polytope bounded by a polynomial? <bookmark mark='c'/> And is the unique games conjecture true? "
            "<bookmark mark='d'/> This part's research problem takes the second."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
