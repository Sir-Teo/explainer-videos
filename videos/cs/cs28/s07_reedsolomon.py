from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load)


class ReedSolomon(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.decode()
        self.erasures()
        self.uses()

    def card(self):
        card = chapter_card(6, r"Reed--Solomon codes", r"How do polynomials survive damage?", lit=(1960, 1969),
                            extra=((1960, r"Reed and Solomon"), (1968, r"Berlekamp"), (1969, r"Massey")), part=PART)
        with self.voiceover("Chapter six. Reed-Solomon codes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def axes(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 240, 50], x_length=6.2, y_length=4.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.4)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in range(1, 10)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (50, 100, 150, 200)])
        return ax, VGroup(xt, yt)

    def idea(self):
        r = load("rs")
        head = label(r"A message is a polynomial; \ a codeword is its values", font_size=32).to_edge(UP, buff=0.3)
        ax, ticks = self.axes()
        a0, a1, a2 = r["msg"]
        graph = ax.plot(lambda x: a0 + a1 * x + a2 * x * x, x_range=[0.5, 9.6], color=DATA, stroke_width=3)
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=HEAD) for x, y in zip(r["xs"], r["y"])])
        vals = VGroup(*[label(str(y), font_size=14, color=HEAD).next_to(p, UL, buff=0.05) for y, p in zip(r["y"], pts)])
        lines = VGroup(
            label(rf"message \ ({a0}, {a1}, {a2}) \ $\to$ \ $f(x) = {a2}x^2 + {a1}x + {a0}$", font_size=22, color=WHITE),
            label(rf"codeword: \ $f(1), \ldots, f(9)$ \ = \ {', '.join(map(str, r['y']))}", font_size=20, color=HEAD),
            label(r"$k$ = 3 numbers in, \ $n$ = 9 out", font_size=22, color=GREY_A),
            label(r"two different quadratics agree on at most 2 points, \\ so two codewords differ in at least 7 of "
                  r"the 9", font_size=22, color=YES),
            label(r"in general: \ $d = n - k + 1$, \ the Singleton bound met with equality: \\ Reed--Solomon codes are "
                  r"\textbf{MDS}", font_size=22, color=DATA),
            label(rf"(the arithmetic is modulo the prime {r['p']}, \\ larger than every value here, \\ so the "
                  r"picture is honest)", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(lines)
        with self.voiceover(
            "In 1960 Irving Reed and Gustave Solomon turned the root-counting fact into a code. <bookmark mark='a'/> "
            "Read the message, here three numbers, as the coefficients of a polynomial. <bookmark mark='b'/> The "
            "codeword is the list of its values at nine points. <bookmark mark='c'/> Three numbers in, nine out. "
            "<bookmark mark='d'/> Two different quadratics can agree at no more than two points, since their "
            "difference has at most two roots. So any two codewords differ in at least seven of the nine places. "
            "<bookmark mark='e'/> In general the distance is n minus k plus one: exactly the Singleton bound of "
            "chapter four. No code of this length and rate can do better. <bookmark mark='f'/> The arithmetic is "
            "really modulo a prime, one thousand and nine, but every value here is smaller, so you can picture it "
            "as an ordinary parabola."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks))
            vo.wait_until("a")
            self.play(Create(graph), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.1), FadeIn(vals),
                      FadeIn(lines[1]))
            for mk, ln in zip("cdef", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def decode(self):
        r = load("rs")
        head = label(r"Pulling the damaged points back", font_size=34).to_edge(UP, buff=0.3)
        ax, ticks = self.axes()
        a0, a1, a2 = r["decoded"]
        graph = ax.plot(lambda x: a0 + a1 * x + a2 * x * x, x_range=[0.5, 9.6], color=YES, stroke_width=3)
        good = VGroup()
        bad = VGroup()
        fixed = VGroup()
        for x, y, yb in zip(r["xs"], r["y"], r["y_bad"]):
            if x in r["bad"]:
                bad.add(Dot(ax.c2p(x, yb), radius=0.09, color=NO))
                fixed.add(Dot(ax.c2p(x, y), radius=0.09, color=YES))
            else:
                good.add(Dot(ax.c2p(x, yb), radius=0.08, color=HEAD))
        lines = VGroup(
            label(rf"three values corrupted, \ at $x$ = {', '.join(map(str, r['bad']))}: \\ the receiver does not "
                  r"know which", font_size=20, color=NO),
            label(r"\textbf{Berlekamp--Welch}: \ an unknown error locator $E$, \\ zero at the bad points; \ "
                  r"$y_i E(x_i) = Q(x_i)$ \\ at all nine: \ a linear system", font_size=20, color=WHITE),
            label(rf"solved: \ $Q/E$ = ({a0}, {a1}, {a2}); \\ the roots of $E$: \ $x$ = "
                  rf"{', '.join(map(str, r['found']))}", font_size=20, color=YES),
            label(r"up to $\lfloor (n-k)/2 \rfloor$ = 3 errors", font_size=20, color=HEAD),
            label(rf"\textbf{{erasures}}: \ lose any 6; \ the other 3 \\ fix $f$ by Lagrange \ $\to$ "
                  rf"({', '.join(map(str, r['lagrange']))})", font_size=20, color=DATA),
            label(r"in practice: \ Berlekamp--Massey \ (1968--69), \\ then Chien's search and Forney's formula",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(lines)
        head2 = VGroup(ax, ticks, good, bad)
        with self.voiceover(
            "Now damage the codeword. <bookmark mark='a'/> Three of the nine values arrive wrong, and the receiver "
            "does not know which. <bookmark mark='b'/> Lloyd Welch and Elwyn Berlekamp's method introduces an "
            "unknown error-locator polynomial E, which is zero exactly at the bad points. Then y times E equals f "
            "times E at every point, good or bad, and with Q standing for f times E, that is a system of linear "
            "equations. <bookmark mark='c'/> Solving it and dividing Q by E gives back the message, five, three, "
            "two, and the roots of E are exactly the three corrupted positions. The red points snap back onto the "
            "curve. <bookmark mark='d'/> With nine values and three unknowns, up to three errors can be fixed: "
            "half the redundancy. <bookmark mark='e'/> Erasures are even easier: lose any six values, and the three "
            "that remain determine the parabola by Lagrange interpolation. <bookmark mark='f'/> Real decoders use "
            "the faster Berlekamp-Massey algorithm, with Chien's search and Forney's formula; our QR decoder does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(head2))
            vo.wait_until("a")
            self.play(Indicate(bad, color=NO), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(graph), FadeIn(lines[2]))
            self.play(*[Transform(b_, f_) for b_, f_ in zip(bad, fixed)])
            for mk, ln in zip("def", lines[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def erasures(self):
        r = load("rs")
        head = label(r"Erasures: \ three survivors are enough", font_size=34).to_edge(UP, buff=0.3)
        ax, ticks = self.axes()
        a0, a1, a2 = r["msg"]
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=HEAD) for x, y in zip(r["xs"], r["y"])])
        keep = [i for i, x in enumerate(r["xs"]) if x not in r["erased"]]
        gone = [i for i in range(len(r["xs"])) if i not in keep]
        crosses = VGroup(*[Cross(pts[i], stroke_color=NO, stroke_width=4).scale(1.6) for i in gone])
        graph = ax.plot(lambda x: a0 + a1 * x + a2 * x * x, x_range=[0.5, 9.6], color=YES, stroke_width=3)
        back = VGroup(*[Dot(ax.c2p(r["xs"][i], r["y"][i]), radius=0.08, color=YES) for i in gone])
        xs_keep = [r["xs"][i] for i in keep]
        lines = VGroup(
            label(rf"six values lost, \\ and the receiver \textbf{{knows}} which: \ only $x$ = "
                  rf"{', '.join(map(str, xs_keep))} remain", font_size=21, color=NO),
            label(r"a quadratic through three points is unique: \\ \textbf{Lagrange interpolation}", font_size=21,
                  color=WHITE),
            label(r"$f(x) = \sum_i y_i \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}$", font_size=24, color=HEAD),
            label(rf"computed mod {r['p']}: \ ({', '.join(map(str, r['lagrange']))}): \\ the message, \ and "
                  r"every lost value with it", font_size=21, color=YES),
            label(r"$n - k$ erasures repaired, \ twice as many as errors: \\ the RAID and QR stories of "
                  r"chapters 7 and 13", font_size=21, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(lines)
        with self.voiceover(
            "Erasures are easier still. <bookmark mark='a'/> Suppose six of the nine values are lost, and the "
            "receiver knows which six. <bookmark mark='b'/> Only one quadratic passes through the three that "
            "remain, and Lagrange's formula writes it down directly: <bookmark mark='c'/> a sum over the surviving "
            "points, each multiplied by a polynomial that is one at its own point and zero at the others. <bookmark "
            "mark='d'/> Computed modulo a thousand and nine, it gives back five, three, two: the message, and with "
            "it every lost value. <bookmark mark='e'/> So a Reed-Solomon code repairs as many erasures as it has "
            "check symbols, twice as many as unknown errors. Chapters seven and thirteen use exactly this."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(pts))
            vo.wait_until("a")
            self.play(Create(crosses), *[pts[i].animate.set_opacity(0.15) for i in gone], FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]))
            vo.wait_until("d")
            self.play(Create(graph), FadeOut(crosses), FadeIn(back), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        head = label(r"Reed--Solomon at work", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"compact disc \ (1982)", r"two RS codes over $\mathrm{GF}(256)$, \ interleaved \ (CIRC)",
                 r"a scratch of about 4,000 bits"],
                [r"deep space", r"RS(255,223) \ with a convolutional code \ (CCSDS)", r"Voyager after Saturn; \ Mars "
                 r"rovers"],
                [r"QR codes", r"RS over $\mathrm{GF}(256)$, \ four levels", r"up to 30\% of the bytes"],
                [r"RAID-6, \ cloud storage", r"RS as an erasure code", r"any 2 \ (or $n - k$) lost disks"],
                [r"DSL, \ DVB, \ SSDs", r"RS, \ often with an inner code", r"bursts"]]
        tab = grid_table([r"where", r"how", r"survives"], rows, widths=[3.4, 5.6, 4.0], row_h=0.55, font_size=20,
                         mono_cols=(), colors=[[WHITE, DATA, YES]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"why so popular: \ symbols are bytes, \ so a burst of bad bits spoils only a few symbols",
                  font_size=22, color=HEAD),
            label(r"and erasures are free information: \ a disk that is gone is \textbf{known} to be gone",
                  font_size=22, color=DATA),
        ).arrange(DOWN, buff=0.3).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Reed-Solomon codes are everywhere. <bookmark mark='a'/> Compact discs use two interleaved ones, and "
            "survive scratches thousands of bits long. Deep-space missions since Voyager pair one with a "
            "convolutional code, chapter ten's. QR codes use them, as do RAID-6 arrays and the storage systems of "
            "chapter thirteen, and modems, digital television and solid-state drives. <bookmark mark='b'/> The "
            "reason is that their symbols are bytes: a burst of bad bits corrupts only a few symbols. <bookmark "
            "mark='c'/> And they use erasures well: a dead disk or an unreadable spot is known to be bad, and each "
            "such erasure costs only one check symbol instead of two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.4), run_time=4.0)
            for mk, ln in zip("bc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
