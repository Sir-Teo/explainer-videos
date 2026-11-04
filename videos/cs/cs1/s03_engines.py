from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, load


def cell(text, color=WHITE, w=1.25, h=0.5, font_size=28, fill=None):
    r = Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.2, fill_color=fill or BACKGROUND,
                  fill_opacity=1 if fill else 0)
    t = MathTex(text, font_size=font_size, color=color)
    return VGroup(r, t.move_to(r))


class Engines(VoiceoverScene):
    def construct(self):
        self.card()
        self.tables()
        self.differences()
        self.analytical()
        self.lovelace()

    def card(self):
        card = chapter_card(2, r"The engines", r"Can a machine do what the clerk does?", lit=(1822, 1837, 1843),
                            part=PART)
        with self.voiceover("Chapter two. The engines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tables(self):
        hc = history_card(1821, r"Charles Babbage and John Herschel",
                          r"checking two clerks' hand-computed astronomical tables against each other, and finding error "
                          r"after error", width=6.0).to_corner(UL, buff=0.4)
        quote = label(r"``I wish to God these calculations \\ had been executed by steam.''", font_size=36)
        quote.move_to([2.4, 1.6, 0])
        who = note(r"Babbage's recollection, \textit{Passages from the Life of a Philosopher} (1864)", font_size=22)
        who.next_to(quote, DOWN, buff=0.25)
        rows = VGroup()
        rng = np.random.default_rng(3)
        for i in range(6):
            x = 12 + i
            v = np.log10(x)
            txt = f"{v:.7f}"
            bad = i in (2, 4)
            if bad:
                k = rng.integers(3, 8)
                txt = txt[:k] + str((int(txt[k]) + 3) % 10) + txt[k + 1:]
            row = VGroup(MathTex(rf"\log {x}", font_size=28, color=GREY_A),
                         MathTex(txt, font_size=28, color=NO if bad else WHITE)).arrange(RIGHT, buff=0.6)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.6, -1.6, 0])
        tag = note(r"illustrative: two digits miscopied", font_size=20).next_to(rows, DOWN, buff=0.2)
        why_ = label(r"tables of logarithms, tides and stars \\ were computed by hand, \ by people called \\ "
                     r"\textit{computers}", font_size=30, color=GREY_A).move_to([3.0, -1.6, 0])
        with self.voiceover(
            "For centuries, anyone who navigated a ship or aimed a cannon used printed tables: logarithms, tides, the "
            "positions of the stars. <bookmark mark='a'/> They were computed by hand, by people whose job title was "
            "computer, and they were full of mistakes. <bookmark mark='b'/> In 1821 Charles Babbage and John Herschel "
            "spent a day checking two clerks' calculations against each other and kept finding errors. Babbage later "
            "remembered saying: I wish to God these calculations had been executed by steam."
        ) as vo:
            self.play(FadeIn(rows), FadeIn(why_))
            vo.wait_until("a")
            self.play(FadeIn(tag), *[Indicate(rows[i][1], color=NO) for i in (2, 4)])
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(quote), FadeIn(who))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def differences(self):
        d = load("difference")
        p, d1, d2 = d["values"], d["d1"], d["d2"]
        head = cmath(r"p(x)", r"=", r"x^2", r"+", r"x", r"+", r"41", font_size=44,
                     colors={r"p(x)": DATA}).to_edge(UP, buff=0.35)
        sub = label(r"Babbage's demonstration polynomial (and Euler's prime generator)", font_size=24,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        cols = [r"x", r"p(x)", r"\Delta", r"\Delta^2"]
        ccol = [GREY_A, DATA, CTRL, HEAD]
        X0, Y0, W, H = -5.6, 1.6, 1.35, 0.52
        hdr = VGroup(*[cell(c, ccol[j], w=W, h=H, font_size=30) for j, c in enumerate(cols)])
        for j, h in enumerate(hdr):
            h.move_to([X0 + j * W, Y0, 0])
            h[0].set_stroke(opacity=0)

        def row(x):
            vals = [str(x), str(p[x]), str(d1[x]) if x < len(d1) else "", str(d2[x]) if x < len(d2) else ""]
            g = VGroup(*[cell(v, ccol[j], w=W, h=H) for j, v in enumerate(vals)])
            for j, c in enumerate(g):
                c.move_to([X0 + j * W, Y0 - (x + 1) * H, 0])
            return g

        first = VGroup(*[row(x) for x in range(3)])
        note1 = label(r"the second differences are constant: \ $\Delta^2 = 2$", font_size=28, color=HEAD)
        note1.move_to([3.4, 0.8, 0])
        how = VGroup(label(r"so each new row needs only additions:", font_size=26, color=GREY_A),
                     cmath(r"\Delta_{\text{new}}", r"=", r"\Delta", r"+", r"\Delta^2", font_size=32,
                           colors={r"\Delta_{\text{new}}": CTRL, r"\Delta": CTRL, r"\Delta^2": HEAD}),
                     cmath(r"p_{\text{new}}", r"=", r"p", r"+", r"\Delta", font_size=32,
                           colors={r"p_{\text{new}}": DATA, r"p": DATA, r"\Delta": CTRL})).arrange(DOWN, buff=0.18)
        how.next_to(note1, DOWN, buff=0.35)
        with self.voiceover(
            "Babbage's idea was that many tables need only addition. Take his favourite demonstration, the polynomial "
            "x squared plus x plus forty-one. <bookmark mark='a'/> Tabulate it: forty-one, forty-three, forty-seven. "
            "Next to each value, the difference to the next one: two, four. And the difference of the differences: two. "
            "<bookmark mark='b'/> For any quadratic, the second differences are constant. So once the first few rows are "
            "in place, every new row comes from two additions: add the constant to the difference, then add the "
            "difference to the value. No multiplication, no thought: a job for gears."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(r) for r in first], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(first[k][3][1], color=HEAD) for k in range(len(first)) if first[k][3][1].tex_string])
            vo.wait_until("b")
            self.play(FadeIn(note1), FadeIn(how))
        # the engine at work: rows appear by additions, the carry flowing right to left
        rows = VGroup(*first)
        with self.voiceover(
            "Watch the engine turn. The two flows down into the difference column, the difference flows into the "
            "value column, and a new value appears: fifty-three, sixty-one, seventy-one. <bookmark mark='a'/> Faster. "
            "Every value up to x equals thirty-nine is a prime number, which is why the polynomial was famous. "
            "<bookmark mark='b'/> At x equals forty it gives sixteen hundred and eighty-one, which is forty-one "
            "squared. The engine does not care. It only adds."
        ) as vo:
            for x in range(3, 7):
                new = row(x)
                prev = rows[-1]
                a1 = CurvedArrow(prev[3].get_left() + DOWN * 0.1, new[2].get_right() + UP * 0.05, angle=-0.9,
                                 color=HEAD, stroke_width=2.5, tip_length=0.14)
                a2 = CurvedArrow(prev[2].get_left() + DOWN * 0.1, new[1].get_right() + UP * 0.05, angle=-0.9,
                                 color=CTRL, stroke_width=2.5, tip_length=0.14)
                self.play(FadeIn(new[0]), FadeIn(new[3]), run_time=0.3)
                self.play(Create(a1), FadeIn(new[2], shift=LEFT * 0.2), run_time=0.6)
                self.play(Create(a2), FadeIn(new[1], shift=LEFT * 0.2), run_time=0.6)
                self.play(FadeOut(a1), FadeOut(a2), run_time=0.25)
                rows.add(new)
            vo.wait_until("a")
            # fast-forward: a scrolling column of x and p(x) down to 41, primes ticked
            self.play(FadeOut(rows), FadeOut(hdr), FadeOut(note1), FadeOut(how), run_time=0.6)
            grid = VGroup()
            for x in range(0, 42):
                ok = d["prime"][x]
                t = MathTex(rf"{p[x]}", font_size=24, color=YES if ok else NO)
                grid.add(t)
            grid.arrange_in_grid(rows=6, cols=7, buff=(0.55, 0.32)).move_to(DOWN * 0.3)
            lab = VGroup(label(r"$p(0), p(1), \dots, p(41)$:", font_size=28), label(r"prime", font_size=28, color=YES),
                         label(r"or", font_size=28), label(r"not", font_size=28, color=NO)).arrange(RIGHT, buff=0.18)
            lab.next_to(grid, UP, buff=0.4)
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(t, scale=0.7) for t in grid], lag_ratio=0.04), run_time=2.6)
            vo.wait_until("b")
            fc = d["first_composite"]
            box = SurroundingRectangle(grid[fc], color=NO, buff=0.08)
            eq = label(rf"$p({fc}) = {p[fc]} = 41^2$", font_size=34, color=NO).next_to(grid, DOWN, buff=0.4)
            self.play(Create(box), FadeIn(eq))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analytical(self):
        store = node_box(r"the store \\ \small 1{,}000 numbers of 40 digits", DATA, font_size=26)
        mill = node_box(r"the mill \\ \small $+\ -\ \times\ \div$", CTRL, font_size=26)
        cards = node_box(r"punched cards \\ \small operations and variables", CODE, font_size=26)
        printer = node_box(r"printer, \ bell, \ curve plotter", GREY_A, font_size=24)
        store.move_to([-3.4, 0.9, 0])
        mill.move_to([1.4, 0.9, 0])
        cards.move_to([1.4, -1.6, 0])
        printer.move_to([5.0, 0.9, 0])
        if printer.get_right()[0] > 6.9:
            printer.shift(LEFT * (printer.get_right()[0] - 6.9))
        ar = VGroup(
            DoubleArrow(store.get_right(), mill.get_left(), buff=0.1, color=GREY_B, stroke_width=3),
            Arrow(cards.get_top(), mill.get_bottom(), buff=0.1, color=CODE, stroke_width=3),
            Arrow(mill.get_right(), printer.get_left(), buff=0.1, color=GREY_B, stroke_width=3),
        )
        branch = label(r"cards can be skipped or repeated \\ depending on a result: \ \textbf{branches and loops}",
                       font_size=26, color=HEAD).next_to(cards, DOWN, buff=0.3)
        head = label(r"The Analytical Engine \ (designed 1834--1871, \ never built)", font_size=34).to_edge(UP,
                                                                                                         buff=0.35)
        jac = history_card(1804, r"Joseph-Marie Jacquard", r"a loom whose patterns are punched into a chain of cards",
                           width=5.2, font_size=22).to_corner(DL, buff=0.35)
        modern = VGroup(*[label(t, font_size=26, color=c) for t, c in
                          ((r"memory", DATA), (r"processor", CTRL), (r"program", CODE), (r"output", GREY_A))])
        for m, b in zip(modern, (store, mill, cards, printer)):
            m.next_to(b, UP, buff=0.15)
        with self.voiceover(
            "Babbage built a working piece of his Difference Engine. Then he designed something far more ambitious. "
            "<bookmark mark='a'/> The Analytical Engine had a store, holding a thousand numbers of forty digits each, "
            "<bookmark mark='b'/> and a mill that did arithmetic on numbers brought from the store. <bookmark mark='c'/> "
            "It was controlled by punched cards, borrowed from Jacquard's loom, which wove patterns from chains of cards. "
            "<bookmark mark='d'/> And crucially, the engine could skip or repeat cards depending on a result: it could "
            "branch and loop. <bookmark mark='e'/> In today's words: memory, a processor, a program, and output. It was "
            "never built; Babbage died in 1871 still revising the design. A Difference Engine was finally built from his "
            "drawings by the Science Museum in London, in 1991. It works."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(store))
            vo.wait_until("b")
            self.play(FadeIn(mill), GrowArrow(ar[0]))
            vo.wait_until("c")
            self.play(FadeIn(cards), GrowArrow(ar[1]), FadeIn(jac))
            vo.wait_until("d")
            self.play(FadeIn(branch), FadeIn(printer), GrowArrow(ar[2]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in modern], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lovelace(self):
        B = load("bernoulli")["B"]
        hc = history_card(1843, r"Ada Lovelace",
                          r"translates an article on the Analytical Engine and adds seven notes, three times its length",
                          width=6.0, font_size=22).to_corner(UL, buff=0.4)
        defn = cmath(r"\frac{x}{e^x - 1}", r"=", r"\sum_{n \ge 0}", r"B_n", r"\frac{x^n}{n!}", font_size=38,
                     colors={r"B_n": FUNC}).move_to([2.7, 2.6, 0])
        rec = cmath(r"\sum_{k=0}^{m}", r"\binom{m+1}{k}", r"B_k", r"=", r"0", font_size=38,
                    colors={r"B_k": FUNC}).next_to(defn, DOWN, buff=0.35)
        rlab = label(r"each $B_m$ from the ones before: \ a loop", font_size=24, color=GREY_A).next_to(rec, DOWN,
                                                                                                buff=0.15)

        def frac(n, d):
            if d == 1:
                return rf"{n}"
            return (r"-" if n < 0 else "") + rf"\tfrac{{{abs(n)}}}{{{d}}}"

        vals = VGroup()
        for i, (n, d) in enumerate(B[:11]):
            vals.add(cmath(rf"B_{{{i}}}", r"=", frac(n, d), font_size=30, colors={rf"B_{{{i}}}": FUNC}))
        vals.arrange_in_grid(rows=4, cols=3, buff=(0.7, 0.25), cell_alignment=LEFT).move_to([2.6, -1.3, 0])
        hl = SurroundingRectangle(vals[8], color=HEAD, buff=0.08)
        hlt = label(r"Note G's target: \ the one she called $B_7$", font_size=24, color=HEAD).next_to(vals, DOWN,
                                                                                                   buff=0.3)
        q1 = label(r"``The Analytical Engine weaves algebraical patterns \\ just as the Jacquard-loom weaves flowers "
                   r"and leaves.''", font_size=24, color=GREY_A).to_corner(DL, buff=0.4)
        with self.voiceover(
            "In 1843 Ada Lovelace translated an Italian article about the Analytical Engine, and added seven notes of "
            "her own, three times as long as the article. <bookmark mark='a'/> The last, Note G, works out in full how "
            "the engine would compute the Bernoulli numbers, the coefficients of this series, which appear all over "
            "mathematics. <bookmark mark='b'/> They obey a recurrence: each one follows from all the ones before. So the "
            "program is a loop, with variables in the store reused on every pass. <bookmark mark='c'/> Here they are, "
            "computed exactly. Her table ends at the one she called B seven, which today is written B eight: minus one "
            "thirtieth. It is the first published program for a general-purpose machine, written for a computer that "
            "did not exist."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(Write(rec), FadeIn(rlab))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.12), run_time=2.0)
            self.play(Create(hl), FadeIn(hlt))
        q2 = label(r"``[It] might compose elaborate and scientific pieces of music \\ of any degree of complexity or "
                   r"extent.''", font_size=26).move_to(UP * 1.4)
        q3 = label(r"``The Analytical Engine has no pretensions whatever \\ to \textit{originate} anything. \ It can do "
                   r"whatever we \\ know how to order it to perform.''", font_size=26).move_to(DOWN * 0.9)
        src = note(r"Lovelace, Notes A and G (1843)", font_size=22).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Lovelace saw further than the arithmetic. <bookmark mark='a'/> The engine weaves algebraic patterns, she "
            "wrote, the way the loom weaves flowers and leaves. Its operations need not be on numbers at all: "
            "<bookmark mark='b'/> if the relations of musical sounds could be expressed in its notation, it might "
            "compose elaborate pieces of music. Symbols, not just numbers. <bookmark mark='c'/> And she drew a line: the "
            "engine originates nothing; it does whatever we know how to order it to do. Turing would answer her "
            "objection by name, a century later. <bookmark mark='d'/> But notice what neither Babbage nor Lovelace "
            "asked: what can such orders do at all? What is the set of everything a machine like this could ever "
            "compute? That question came from somewhere else entirely: from the foundations of mathematics."
        ) as vo:
            self.play(FadeOut(defn), FadeOut(rec), FadeOut(rlab), FadeOut(vals), FadeOut(hl), FadeOut(hlt),
                      FadeIn(q1))
            vo.wait_until("a")
            self.play(Indicate(q1, color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(q2))
            vo.wait_until("c")
            self.play(FadeIn(q3), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeOut(q1), q2.animate.set_opacity(0.4), q3.animate.set_opacity(0.4))
        self.wait(0.3)
        self.clear_scene()
