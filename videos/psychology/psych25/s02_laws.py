from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Laws(VoiceoverScene):
    def construct(self):
        self.card()
        self.hick()
        self.fitts()

    def card(self):
        card = chapter_card(1, r"Two old laws", r"Why does each doubling of the choices cost the same time?",
                            lit={1952: r"Hick", 1953: r"Hyman", 1954: r"Fitts", 1963: r"Crossman \& Goodeve"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. Two old laws."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hick(self):
        d = load("hick")
        head = heading(r"Hick's law: \ time grows with the bits to be decided")
        lamps = VGroup()
        for k, n in enumerate((2, 4, 8)):
            row = VGroup(*[Circle(radius=0.13, color=GREY_B, fill_color=BOUND if j == 1 else "#20262F",
                                  fill_opacity=1, stroke_width=2) for j in range(n)]).arrange(RIGHT, buff=0.1)
            lab = label(rf"{n} lamps: \ {int(np.log2(n))} bit{'s' if n > 2 else ''}", font_size=19, color=GREY_A)
            lamps.add(VGroup(row, lab).arrange(RIGHT, buff=0.3))
        lamps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.6, 2.0, 0])
        A = axes([0, 4.5], [0, 2.2], x_length=5.4, y_length=2.6, xticks=[1, 2, 3, 4], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"$\log_2 n$, \ bits",
                 ylabel=r"mean decision time, \ model units", center=[-3.5, -1.15, 0], font_size=16)
        bits, mt = d["bits"], d["mean_dt"]
        pts = scatter(A.ax, bits, mt, MODEL, 0.09, 1)
        xs = np.linspace(0.6, 4.3, 50)
        line = DashedVMobject(curve(A.ax, xs, d["intercept"] + d["slope"] * xs, MODEL, 2), num_dashes=22)
        nl = VGroup(*[label(rf"$n = {n}$", font_size=18, color=GREY_A).next_to(A.ax.c2p(b, m), UP, buff=0.12)
                      for n, b, m in zip(d["n"], bits, mt)])
        assert d["max_resid"] < 0.06 and np.all(np.diff(mt) > 0) and np.all(np.abs(d["acc"] - 0.9) < 0.015)
        rows = rows_of([
            (r"Hick, \ 1952: \ press the key under whichever of up to ten lamps lights; \ time grows with the "
             r"logarithm of the number of lamps", WHITE),
            (r"Hyman, \ 1953: \ it is the information, \ not the count: \ make some lamps more likely, \ and time "
             r"follows the bits", BOUND),
            (r"Psyche: \ a race of accumulators that must stay 90\% right needs a higher bound for more rivals; "
             r"\ its time then grows with $\log_2 n$", MODEL),
            (r"each doubling of the alternatives adds about the same time: \ a constant cost per bit", DRIFT),
        ], 5.8, 23, 0.34).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.race\_hick}; \ Hick (1952); \ Hyman (1953)")
        with self.voiceover(
            "The first law is from 1952. <bookmark mark='a'/> William Hick put ten lamps in front of people, each "
            "with a key beneath it, and asked them to press the key under whichever lamp lit. The more lamps in play, "
            "the longer they took, and the time grew not with the number of lamps but with its logarithm: every "
            "doubling added about the same amount. <bookmark mark='b'/> A year later Ray Hyman showed that it's the "
            "information that matters, not the count. Make some lamps light more often than others, and the time "
            "follows the bits of information in each choice. <bookmark mark='c'/> Why a logarithm? Here is one "
            "answer Psyche can compute. Let a separate accumulator gather evidence for each lamp, in a race, and "
            "demand ninety percent accuracy. With more rivals, one of them is more likely to reach the line by "
            "chance, so the line must be raised, and the time grows almost exactly with the log of the number of "
            "alternatives. <bookmark mark='d'/> A constant cost per bit: the first sign that deciding is "
            "accumulating."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lamps), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts), FadeIn(nl), Create(line), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fitts(self):
        d = load("fitts")
        head = heading(r"Fitts's law, \ derived from corrections")
        y0 = 1.6
        x0, scale = -6.2, 0.62
        start = Dot([x0, y0, 0], radius=0.08, color=WHITE)
        W = d["path_W"] * scale
        tx = x0 + d["path_D"] * scale
        target = Rectangle(width=W, height=0.9, stroke_color=BOUND, fill_color=BOUND, fill_opacity=0.35
                           ).move_to([tx, y0, 0])
        dl = DoubleArrow([x0, y0 - 0.75, 0], [tx, y0 - 0.75, 0], buff=0, color=GREY_B, stroke_width=2, tip_length=0.15)
        dlab = label(r"$D$", font_size=24, color=GREY_A).next_to(dl, DOWN, buff=0.08)
        wlab = label(r"$W$", font_size=24, color=BOUND).next_to(target, UP, buff=0.1)
        rem = d["remaining"]
        hops = VGroup()
        pos = [tx - r_ * scale for r_ in rem]
        for k in range(len(pos) - 1):
            a, b = np.array([pos[k], y0, 0]), np.array([pos[k + 1], y0, 0])
            hops.add(ArcBetweenPoints(a, b, angle=-PI / 2.5, color=EVIDENCE, stroke_width=3))
        A = axes([1, 7], [0, 4], x_length=5.2, y_length=2.4, xticks=[1, 3, 5, 7], yticks=[0, 1, 2, 3, 4],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"$\log_2(2D/W)$, \ bits",
                 ylabel=r"submovements", center=[-3.4, -1.5, 0], font_size=16)
        stairs = curve(A.ax, d["ID"], d["k_steps"], EVIDENCE, 3)
        ln = curve(A.ax, d["ID"], d["k_exact"], MODEL, 3)
        assert len(rem) - 1 == int(np.ceil(d["path_ID"] / np.log2(1 / d["r"]) - 1e-9))
        eqs = VGroup(
            MathTex(r"D_k = D\,r^k", font_size=32, color=EVIDENCE),
            MathTex(r"D\,r^k < \tfrac{W}{2} \;\Longleftrightarrow\; k > \frac{\log_2 (2D/W)}{\log_2 (1/r)}",
                    font_size=30, color=WHITE),
            MathTex(r"MT = a + b \log_2\!\frac{2D}{W}", font_size=34, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.4, 0])
        rows = rows_of([
            (r"Fitts, \ 1954: \ tap between two plates as fast as you can; \ the time grows with $\log_2(2D/W)$", WHITE),
            (r"Crossman \& Goodeve, \ 1963: \ each corrective submovement covers all but a share $r$ of what is "
             r"left; \ the count of corrections is the logarithm", EVIDENCE),
            (r"real movements blend into fewer, \ variable corrections, \ and the staircase smooths into the line",
             GREY_A),
        ], 6.0, 22, 0.3).move_to([3.4, -1.7, 0])
        tag = psyche_tag(r"\texttt{fitts}: \ iterative corrections, \ $r = 0.25$; \ Fitts (1954)")
        with self.voiceover(
            "The second law is about moving. <bookmark mark='a'/> In 1954 Paul Fitts had people tap back and forth "
            "between two metal plates as fast as they could. The time per movement grew with the logarithm of twice "
            "the distance over the width of the target. Double the distance, or halve the width, and you add the "
            "same time. <bookmark mark='b'/> Why a logarithm again? In 1963 Crossman and Goodeve suggested that an "
            "aimed movement is a series of corrections. Each one covers most of the remaining distance, leaving a "
            "fixed share of it, so after k corrections what's left is D times r to the k. <bookmark mark='c'/> You "
            "stop when that's inside half the target, and solving for k gives the logarithm of two D over W. "
            "<bookmark mark='d'/> Count the corrections and you get a staircase. Real movements blend their "
            "corrections and vary from one to the next, and the staircase smooths into Fitts's straight line, which "
            "still guides the design of every screen you touch."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(start), FadeIn(target), FadeIn(wlab), GrowFromCenter(dl),
                      FadeIn(dlab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(h) for h in hops], lag_ratio=0.8), Write(eqs[0]), FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(Write(eqs[1]), Write(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(A), Create(stairs), Create(ln), FadeIn(rows[2]))
        self.clear_scene()
