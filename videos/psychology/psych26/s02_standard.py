from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Standard(VoiceoverScene):
    def construct(self):
        self.card()
        self.expected()
        self.petersburg()
        self.bernoulli()
        self.axioms()

    def card(self):
        card = chapter_card(1, r"The standard: \ expected value and utility", r"What would a perfectly consistent "
                            r"chooser do?", lit={1654: r"Pascal \& Fermat", 1738: r"Bernoulli",
                                                 1944: r"von Neumann \& Morgenstern"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. The standard: expected value and utility."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def expected(self):
        head = heading(r"Expected value: \ the first rule")
        tab = VGroup(
            label(r"a gamble: \ 100 with probability 0.3, \ else 0", font_size=28, color=RISKY),
            MathTex(r"\mathrm{EV} = \sum_i p_i\,x_i = 0.3 \times 100 + 0.7 \times 0 = 30", font_size=40),
            label(r"a sure 25, \ or the gamble? \ by expected value, \ the gamble", font_size=26, color=NORM),
        ).arrange(DOWN, buff=0.45).move_to([0, 0.9, 0])
        rows = rows_of([
            (r"Pascal and Fermat, \ 1654: \ how to split the stakes of an unfinished game; \ the birth of "
             r"probability, \ and of the rule \emph{weight each outcome by its chance}", WHITE),
            (r"over many plays the average prize tends to the expected value: \ so a gambler who plays often should "
             r"maximize it", NORM),
            (r"but people buy insurance, \ which has a lower expected value than not buying it; \ and so the rule "
             r"needed amending", LOSS),
        ], 11.8, 25, 0.32).move_to([0, -1.7, 0])
        tag = historical_tag(r"Pascal--Fermat letters (1654); \ Huygens (1657)")
        with self.voiceover(
            "The first standard for a choice under risk is about as old as probability itself. <bookmark mark='a'/> "
            "Take a gamble that pays a hundred with probability point three, and nothing otherwise. Its expected "
            "value is the sum of each outcome times its chance: thirty. Offered a sure twenty-five instead, the rule "
            "says take the gamble. <bookmark mark='b'/> The rule comes from 1654, when Blaise Pascal and Pierre de "
            "Fermat worked out by letter how to split the stakes of a game interrupted before its end. "
            "<bookmark mark='c'/> Over many plays, the average prize tends to the expected value, so a gambler who "
            "plays often should maximize it. <bookmark mark='d'/> But everyone who buys insurance pays more, on "
            "average, than they get back. If they're not simply wrong, the rule needs amending."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), Write(tab[1]))
            self.play(FadeIn(tab[2]))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def petersburg(self):
        d = load("stpete")
        head = heading(r"The St Petersburg game")
        rule = wrapped_label(r"toss a coin until it lands heads; \ heads first on toss $k$ pays $2^k$ ducats",
                             12.0, 26, RISKY).next_to(head, DOWN, buff=0.3)
        A = axes([0, 30], [0, 30], x_length=5.2, y_length=3.4, xticks=[0, 10, 20, 30], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"tosses allowed before the game stops",
                 ylabel=r"expected prize, \ ducats", center=[-3.4, -1.0, 0], font_size=16)
        stair = curve(A.ax, np.arange(1, 31), d["cut"], NORM, stroke_width=4)
        B = axes([0, 5], [0, 30], x_length=5.2, y_length=3.4, xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: f"10^{{{v:.0f}}}", yfmt=lambda v: f"{v:.0f}", xlabel=r"plays",
                 ylabel=r"average prize so far", center=[3.4, -1.0, 0], font_size=16)
        x = np.log10(d["plays"])
        run = curve(B.ax, x, np.minimum(d["avg"], 30), RISKY, stroke_width=3)
        lg = curve(B.ax, x, np.log2(d["plays"]), GREY_B, stroke_width=2)
        lgl = label(r"$\log_2 n$ \ (Feller)", font_size=18, color=GREY_B).next_to(B.ax.c2p(4.0, np.log2(10 ** 4.0)),
                                                                              DOWN, buff=0.15)
        tag = psyche_tag(r"\texttt{choice.st\_petersburg\_ev}; \ 100{,}000 plays, \ the median run of 101")
        with self.voiceover(
            "Here is the problem that forced the amendment. <bookmark mark='a'/> Toss a coin until it lands heads. "
            "If heads comes first on toss k, you win two to the k ducats: two, four, eight, and so on. "
            "<bookmark mark='b'/> A head on the first toss has probability one half and pays two; on the second, "
            "one quarter and pays four. Every toss adds exactly one ducat to the expected prize, so if the game may "
            "go on for ever, its expected value is infinite. <bookmark mark='c'/> Yet nobody will pay more than a "
            "few ducats to play. And they're not obviously wrong. Here are a hundred thousand plays, the median "
            f"of a hundred and one such runs: the average prize creeps up like the logarithm of the number of "
            f"plays, reaching about {d['final_median']:.0f} ducats, not infinity. The infinite expectation comes "
            "from prizes so rare that you'll never see them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(stair), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(B), Create(run), run_time=3)
            self.play(Create(lg), FadeIn(lgl))
        self.clear_scene()

    def bernoulli(self):
        d = load("stpete")
        head = heading(r"Bernoulli's answer: \ utility")
        A = axes([0, 4], [0, 1.5], x_length=5.4, y_length=3.8, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0, 1.5],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"wealth", ylabel=r"utility",
                 center=[-3.3, -0.2, 0], font_size=16)
        xs = np.linspace(0.05, 4, 200)
        u = lambda w: np.log1p(w) / np.log1p(4) * 1.4  # noqa: E731
        cu = curve(A.ax, xs, u(xs), NORM, stroke_width=4)
        lo, hi = 0.5, 3.5
        chord = Line(A.ax.c2p(lo, u(lo)), A.ax.c2p(hi, u(hi)), color=RISKY, stroke_width=3)
        mid = Dot(A.ax.c2p((lo + hi) / 2, (u(lo) + u(hi)) / 2), color=RISKY, radius=0.08)
        ce_x = float(np.expm1((u(lo) + u(hi)) / 2 * np.log1p(4) / 1.4))
        ce = Dot(A.ax.c2p(ce_x, (u(lo) + u(hi)) / 2), color=SURE, radius=0.08)
        gap = Line(ce.get_center(), mid.get_center(), color=LOSS, stroke_width=4)
        glab = label(r"risk premium", font_size=17, color=LOSS).next_to(gap, UP, buff=0.12)
        prices = VGroup(label(r"what a log-utility player pays to play", font_size=21, color=NORM))
        for w, pr in zip(d["wealth"], d["price"]):
            prices.add(label(rf"wealth {num(w)}: \ {pr:.1f} ducats", font_size=21, color=WHITE))
        prices.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, 1.1, 0])
        rows = rows_of([
            (r"a concave utility: \ each extra ducat is worth less than the last", NORM),
            (r"the average utility of a 50--50 gamble lies on the chord, \ below the curve: \ a sure amount less "
             r"than the expected value is worth as much", RISKY),
        ], 5.6, 21, 0.25).move_to([3.4, -2.1, 0])
        tag = psyche_tag(r"\texttt{choice.st\_petersburg\_ce}: \ Bernoulli's (1738) logarithm")
        with self.voiceover(
            "Daniel Bernoulli's answer, in 1738: what matters is not the money but its utility to you, and a "
            "thousand ducats mean less to a rich man than to a poor one. <bookmark mark='a'/> So utility is a "
            "concave curve: each extra ducat adds less than the last. He chose the logarithm. "
            "<bookmark mark='b'/> Concavity explains risk aversion. A fifty-fifty gamble between two amounts has an "
            "average utility on the straight chord between them, which lies below the curve, so a sure amount less "
            "than the expected value is worth just as much. The gap is the premium you'd pay to be rid of the risk, "
            "which is what an insurance company sells. <bookmark mark='c'/> And it tames the St Petersburg game. "
            f"With logarithmic utility, someone with ten ducats should pay about {d['price'][0]:.0f} to play, and "
            f"a millionaire about {d['price'][-1]:.0f}. Finite prices, rising slowly with wealth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(mid), FadeIn(ce))
            self.play(Create(gap), FadeIn(glab), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in prices], lag_ratio=0.3), run_time=2.5)
        self.clear_scene()

    def axioms(self):
        head = heading(r"Four axioms, \ one theorem")
        ax_rows = VGroup()
        for name, txt, col in [
            (r"completeness", r"of any two options, \ you prefer one or are indifferent", NORM),
            (r"transitivity", r"if A over B and B over C, \ then A over C", NORM),
            (r"continuity", r"if A over B over C, \ some mixture of A and C is as good as B", NORM),
            (r"independence", r"if A over B, \ then A-or-C over B-or-C, \ mixed with the same C in the same "
                              r"proportion", LOSS),
        ]:
            ax_rows.add(VGroup(label(name, font_size=26, color=col),
                               wrapped_label(txt, 8.6, 25, WHITE)).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        for r in ax_rows:
            r[1].shift(RIGHT * (2.8 - r[0].width))
        ax_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, 0.75, 0])
        thm = VGroup(
            label(r"then there is a utility $u$, \ and you choose as if maximizing", font_size=26, color=GREY_A),
            MathTex(r"\mathrm{EU} = \sum_i p_i\, u(x_i)", font_size=44, color=NORM),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.75, 0])
        note = wrapped_label(r"von Neumann and Morgenstern, \ 1944 and 1947; \ Savage, \ 1954, \ for personal "
                             r"probabilities; \ the normative case is \emph{Philosophy, Built}, \ Part 33",
                             12.0, 22, GREY_B).to_edge(DOWN, buff=0.75)
        tag = historical_tag(r"von Neumann \& Morgenstern (1944, \ 1947); \ Savage (1954)")
        with self.voiceover(
            "In 1944 John von Neumann and Oskar Morgenstern turned Bernoulli's idea into a theorem. "
            "<bookmark mark='a'/> Suppose your preferences are complete: of any two options you prefer one or are "
            "indifferent. Transitive: if you prefer A to B and B to C, you prefer A to C. And continuous: if A beats "
            "B and B beats C, some mixture of A and C is exactly as good as B. <bookmark mark='b'/> And add the "
            "fourth, the one that matters most today: independence. If you prefer A to B, you should still prefer "
            "A when both are mixed, in the same proportion, with the same third option C. The common part shouldn't "
            "matter. <bookmark mark='c'/> Then there is a utility function, and you choose as if maximizing "
            "expected utility. Leonard Savage extended the result in 1954 to probabilities that are your own "
            "beliefs. <bookmark mark='d'/> Whether a rational chooser must obey these axioms is a question for "
            "philosophy, taken up in Part 33 of Philosophy, Built. Our question is whether people do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ax_rows[:3]], lag_ratio=0.8),
                      run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(ax_rows[3], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(thm))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()
