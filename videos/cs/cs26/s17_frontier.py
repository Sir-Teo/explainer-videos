from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, bar_chart, fit_right, grid_table,
                                   load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.formulas()
        self.lower()
        self.meta()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ complexity about complexity", r"How hard is it to tell how hard a "
                            r"function is?", lit=(1949, 2022), extra=((1949, r"Shannon"), (2020, r"Liu--Pass"),
                                                                        (2022, r"Hirahara")), part=PART)
        with self.voiceover("Chapter sixteen, the frontier. Complexity about complexity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def formulas(self):
        f = load("formulas")
        head = label(r"How big a formula does each function need?", font_size=32).to_edge(UP, buff=0.3)
        hist = {int(k): v for k, v in f["hist"].items() if k != "None"}
        ks = sorted(hist)
        ch = bar_chart([hist[k] for k in ks], [str(k) for k in ks], [YES if k <= 5 else (HEAD if k < 10 else NO)
                                                                    for k in ks], height=3.0, bar_w=0.42, gap=0.22,
                       fmt_=lambda v: f"{int(v)}", font_size=18)
        ch.next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        cl = label(r"leaves in the smallest AND/OR formula \ (literals as leaves)", font_size=18,
                   color=GREY_A).next_to(ch, DOWN, buff=0.15)
        notes = VGroup(
            label(rf"all {f['functions']} Boolean functions of 3 inputs, \\ exactly, \ by dynamic programming",
                  font_size=20, color=WHITE),
            label(rf"majority: \ {f['majority']} leaves; \\ parity: \ {f['parity']}, \ the most of all", font_size=20,
                  color=NO),
            label(r"Khrapchenko \ (1971): \ parity of $n$ bits \\ needs $n^2$; \ here 9 $\le$ 10", font_size=20,
                  color=HEAD),
            label(r"Shannon \ (1949): \ counting shows \\ \textbf{almost every} function of $n$ inputs \\ needs circuits of "
                  r"size $2^n / n$", font_size=20, color=DATA),
            label(r"yet for no \textbf{explicit} function in NP \\ can we prove more than about $3.1\,n$ gates",
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ch, RIGHT, buff=0.7).align_to(ch, UP)
        fit_right(notes)
        with self.voiceover(
            "The frontier asks about the complexity of complexity itself. <bookmark mark='a'/> We computed, exactly, "
            "the smallest formula of ANDs and ORs for every one of the two hundred and fifty-six Boolean functions "
            "of three inputs. <bookmark mark='b'/> Majority needs five leaves. Parity needs ten, more than any other. "
            "<bookmark mark='c'/> Valeriy Khrapchenko proved in 1971 that the parity of n bits needs n squared, so "
            "nine here; the truth is ten. <bookmark mark='d'/> Claude Shannon showed in 1949, by counting, that "
            "almost every function of n inputs needs circuits of exponential size. <bookmark mark='e'/> And yet, for "
            "no specific function in NP can anyone prove a lower bound beyond about three point one times n gates, "
            "the 2022 record of Jiatu Li and Tianqi Yang. Hard functions are everywhere, and we cannot point to one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(cl), FadeIn(notes[0]))
            for mk, n_ in zip("bcde", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"The state of lower bounds", font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"general circuits", r"$3.1\,n - o(n)$", r"Li and Yang \ (2022)"],
                [r"formulas \ (De Morgan)", r"$n^{3 - o(1)}$", r"H\aa stad \ (1998); \ Tal \ (2014)"],
                [r"constant depth", r"exponential, \ for parity", r"H\aa stad \ (1986)"],
                [r"ACC$^0$", r"NQP $\not\subseteq$ ACC$^0$", r"Williams \ (2011); \ Murray and Williams \ (2018)"],
                [r"what we need for P $\ne$ NP", r"superpolynomial, \ for SAT", r"open"]]
        tab = grid_table([r"model", r"best bound known", r"by"], rows, widths=[4.0, 3.6, 5.2], row_h=0.52,
                         font_size=20, mono_cols=(), colors=[[WHITE, DATA, GREY_A]] * 4 + [[WHITE, NO, NO]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"\textbf{geometric complexity theory} \ (Mulmuley and Sohoni, 2001): \ attack the algebraic "
                  r"version with representation theory", font_size=20, color=LAM),
            label(r"its simplest form was ruled out in 2016 \ (B\"urgisser, \ Ikenmeyer, \ Panova); \ the "
                  r"programme continues", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Here is how far lower bounds have come. <bookmark mark='a'/> For general circuits, three point one n. "
            "For formulas, about n cubed, from Johan Håstad and Avishay Tal. For constant-depth circuits, "
            "exponential bounds for parity. For the class ACC zero, Williams's algorithmic method now separates it "
            "from nondeterministic quasi-polynomial time. And what P versus NP needs is a superpolynomial bound for "
            "SAT against general circuits, far beyond all of these. <bookmark mark='b'/> A different programme, "
            "geometric complexity theory, proposed by Ketan Mulmuley and Milind Sohoni, attacks an algebraic "
            "version of the question with representation theory. <bookmark mark='c'/> Its simplest form was ruled "
            "out in 2016, and the programme continues with subtler tools."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5), run_time=6.0)
            for mk, n_ in zip("bc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def meta(self):
        head = label(r"Meta-complexity", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{MCSP}: \ given a truth table and $s$, \ is there a circuit of size $\le s$?", font_size=22,
                  color=WHITE),
            label(r"in NP \ (the circuit is the certificate); \ studied since the 1950s in the USSR \ (\textit{perebor})",
                  font_size=21, color=GREY_A),
            label(r"is it NP-complete? \ Unknown. \ Hirahara \ (2022): \ a \textbf{partial} version is", font_size=22,
                  color=HEAD),
            label(r"Liu and Pass \ (2020): \ \textbf{one-way functions exist} $\iff$ \ a time-bounded Kolmogorov "
                  r"complexity is hard on average", font_size=22, color=YES),
            label(r"so the existence of cryptography is a question about \textbf{compressing strings} \ (Part 25, "
                  r"chapter 10)", font_size=22, color=DATA),
            label(r"meta-complexity may connect Pessiland to Minicrypt: \ the most active frontier of the 2020s",
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The newest frontier is called meta-complexity: how hard is it to measure how hard something is? "
            "<bookmark mark='a'/> The minimum circuit size problem asks, given the full truth table of a function and "
            "a number s, whether some circuit of size s computes it. <bookmark mark='b'/> It is in NP, since the "
            "circuit is the certificate, and Soviet researchers studied it as a problem of brute-force search, "
            "perebor, before P and NP had names. <bookmark mark='c'/> Is it NP-complete? Nobody knows. In 2022 "
            "Shuichi Hirahara proved that a partial-function version is. <bookmark mark='d'/> And in 2020 Yanyi Liu "
            "and Rafael Pass proved that one-way functions exist if and only if a time-bounded version of Kolmogorov "
            "complexity is hard on average. <bookmark mark='e'/> So whether cryptography is possible is a question "
            "about compressing strings, Part 25's Kolmogorov complexity with a clock. <bookmark mark='f'/> These "
            "results may one day connect the worlds of the last chapter. They are among the most active research in "
            "the field."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ P vs NP; \ NP vs coNP; \ P vs PSPACE; \ L vs P", font_size=22, color=WHITE),
            label(r"2. \ Is MCSP NP-complete?", font_size=22, color=WHITE),
            label(r"3. \ Is factoring, \ or graph isomorphism, \ in P?", font_size=22, color=WHITE),
            label(r"4. \ Where exactly is the random 3-SAT threshold? \ Is it the predicted 4.267?", font_size=22,
                  color=WHITE),
            label(r"5. \ Can time $t$ be simulated in space $t^{1/2 - \varepsilon}$, \ or even $t^{\varepsilon}$?",
                  font_size=22, color=WHITE),
            label(r"6. \ A superlinear circuit lower bound, \ $5n$ or $n \log n$, \ for any explicit function",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the fourth", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> P versus NP itself, and its cousins: NP versus coNP, P versus "
            "PSPACE, logarithmic space versus P. <bookmark mark='b'/> Whether the minimum circuit size problem is "
            "NP-complete. <bookmark mark='c'/> Whether factoring or graph isomorphism is in P. <bookmark mark='d'/> "
            "The exact location of the three-SAT threshold. <bookmark mark='e'/> How far Williams's simulation can be "
            "pushed. <bookmark mark='f'/> And any superlinear lower bound on circuit size for an explicit function. "
            "<bookmark mark='g'/> This part's research problem takes a small, computable case of the fourth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
