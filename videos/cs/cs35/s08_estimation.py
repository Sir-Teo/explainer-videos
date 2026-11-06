from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, COST, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, num)


class Estimation(VoiceoverScene):
    def construct(self):
        self.card()
        self.statistics()
        self.skew()
        self.compound()

    def card(self):
        card = chapter_card(7, r"Guessing sizes", r"How many rows will this return?", lit=(1991, 2015),
                            extra=((1991, r"Ioannidis and Christodoulakis: \ errors compound"),
                                   (2015, r"Leis et al.: \ how good are optimizers?")), part=PART)
        with self.voiceover("Chapter seven. Guessing sizes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def statistics(self):
        e = load("estimation")
        head = label(r"Every cost rests on a guessed size", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            label(r"\texttt{ANALYZE} keeps, \ per table, \ the row count; \ per column, \ the number of distinct "
                  r"values, \ min, \ max", font_size=20, color=WHITE),
            label(r"equality: \ selectivity $1/\text{distinct}$; \ a range: \ the fraction of $[\min, \max]$ it "
                  r"covers", font_size=20, color=HEAD),
            label(r"two conditions: \ multiply \ (assume they are \textbf{independent})", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(head, DOWN, buff=0.35)
        rows = []
        for r in e["rows"]:
            cond = r["sql"].split("WHERE ")[1].replace("'", "")
            rows.append([cond, num(r["estimate"]), num(r["actual"])])
        tab = grid_table([r"100{,}000 people: \ \texttt{WHERE} \dots", r"estimate", r"actual"], rows,
                         widths=[6.6, 1.8, 1.8], row_h=0.42, font_size=19, mono_cols=(0,))
        tab.next_to(rules, DOWN, buff=0.45).set_x(0)
        for r, row in enumerate(e["rows"], start=1):
            ok = 0.5 < row["estimate"] / max(row["actual"], 1) < 2
            tab.cells[r][1].set_color(YES if ok else NO)
        foot = label(r"200 cities, \ ten to a country: \ knowing the city \textit{fixes} the country, \ so "
                     r"multiplying by $1/20$ is wrong by twenty times", font_size=19, color=NO).next_to(tab, DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            "The optimizer's costs depend on how many rows each step produces, and it cannot know that without "
            "running the query. It guesses, from statistics. <bookmark mark='a'/> Our database keeps, for each "
            "table, the number of rows, and for each column the number of distinct values and the smallest and "
            "largest. <bookmark mark='b'/> An equality condition is guessed to keep one row in the number of distinct "
            "values; a range, the fraction of the span it covers. <bookmark mark='c'/> And two conditions together "
            "are assumed independent, so their fractions multiply. <bookmark mark='d'/> Here are a hundred thousand "
            "people. One city: the guess is five hundred, the truth 492. An age range: almost exact. A city and an "
            "age, which really are independent: right again. <bookmark mark='e'/> But a city and its own country: "
            "the guess is twenty-five, the truth 492. The country adds nothing once the city is known, and the "
            "independence assumption cannot see that."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeIn(foot), Indicate(tab.cells[2][1], color=NO))
        self.wait(0.3)
        self.clear_scene()

    def skew(self):
        e = load("estimation")
        head = label(r"Skew: \ one guess for every word", font_size=36).to_edge(UP, buff=0.3)
        sub = label(rf"{num(e['n'])} words of the novels, \ {num(e['ndv'])} distinct: \ the guess for "
                    rf"\texttt{{word = w}} is {e['n']} / {e['ndv']} $\approx$ {e['skew'][0]['estimate']:.1f}, \ "
                    r"for any $w$", font_size=20, color=WHITE).next_to(head, DOWN, buff=0.35)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=7.0, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-1.6, -0.2, 0])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.12)
                      for k in range(0, 5)])
        guess = DashedLine(ax.c2p(0, np.log10(e["skew"][0]["estimate"])), ax.c2p(4, np.log10(e["skew"][0]["estimate"])),
                           color=HEAD)
        gl = label(r"the guess", font_size=18, color=HEAD).next_to(guess, RIGHT, buff=0.1)
        bars = VGroup()
        for k, s in enumerate(e["skew"]):
            v = max(s["actual"], 1)
            h = ax.c2p(0, np.log10(v))[1] - ax.c2p(0, 0)[1]
            c = YES if 0.5 < s["actual"] / s["estimate"] < 2 else NO
            b = Rectangle(width=0.9, height=max(h, 0.03), stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(k + 0.5, 0), aligned_edge=DOWN)
            t = label(num(s["actual"]), font_size=18, color=c).next_to(b, UP, buff=0.08)
            n = mono(s["word"], 17, CODE).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.15)
            bars.add(VGroup(b, t, n))
        lines = VGroup(
            label(r"word frequencies follow Zipf's law \ (Part 17): \ a few words are everywhere", font_size=19,
                  color=WHITE),
            label(r"\texttt{the}: \ guessed 10, \ actually 6{,}776: \ a nested loop chosen for 10 rows runs "
                  r"6{,}776 probes", font_size=19, color=NO),
            label(r"the cure: \ \textbf{histograms} and lists of the most common values \ (PostgreSQL keeps 100 "
                  r"of each per column)", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Distinct counts assume every value is equally common, and real data is rarely like that. "
            "<bookmark mark='a'/> In a sample of the novels, a hundred and twenty thousand words with twelve thousand "
            "distinct, the guess for any single word is ten rows. <bookmark mark='b'/> Whale, eighty-one. Ship, "
            "twenty-six. Zeal, none at all. <bookmark mark='c'/> And the: six thousand, seven hundred and seventy-six. "
            "Word frequencies follow Zipf's law, which we met in Part 17, and the guess is wrong by a factor of almost "
            "seven hundred. <bookmark mark='d'/> A plan chosen for ten rows, a nested loop with an index probe per "
            "row, is a disaster for seven thousand. <bookmark mark='e'/> So real systems keep histograms, and a list "
            "of each column's most common values with their counts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), Create(ax), FadeIn(yt), Create(guess), FadeIn(gl))
            vo.wait_until("b")
            self.play(*[FadeIn(b) for b in bars[1:]])
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def compound(self):
        o = load("optimizer")
        head = label(r"Errors multiply through joins", font_size=36).to_edge(UP, buff=0.3)
        joins = [(k, v) for k, v in o["stats"].items() if k.startswith("Nested loops")]
        est = {ln.strip().split("   (")[0]: float(ln.split("rows ~")[1].split(",  ")[0].split(", cost")[0].replace(",", ""))
               for ln in o["explain"].splitlines() if "Nested loops" in ln}
        ests = [est[k] for k, _ in joins]
        rows = [[k.replace("Nested loops join on ", ""), num(e_), num(v)] for (k, v), e_ in zip(joins, ests)]
        tab = grid_table([r"our chain query: \ join", r"estimated rows", r"actual rows"], rows,
                         widths=[4.0, 2.4, 2.4], row_h=0.42, font_size=19, mono_cols=(0,))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        lines = VGroup(
            label(r"each join's estimate multiplies its inputs' estimates by a guessed selectivity, \ so errors "
                  r"\textbf{multiply}", font_size=20, color=WHITE),
            label(r"Ioannidis and Christodoulakis \ (1991): \ the error can grow exponentially in the number of "
                  r"joins", font_size=20, color=HEAD),
            label(r"Leis et al. \ (2015), \ real queries on real data: \ estimates off by $10^4$ and more, \ in "
                  r"every system tested", font_size=20, color=NO),
            label(r"and yet: \ the plan only has to be \textit{good}; \ here, \ off by two in rows, \ it was still "
                  r"the best", font_size=20, color=YES),
            label(r"responses: \ re-optimize mid-query, \ sample, \ learn the estimates \ (chapter 16)",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "In a query with several joins, the errors compound. <bookmark mark='a'/> Each join's output is "
            "estimated from the estimates of its inputs, times a guessed fraction, so the errors multiply. "
            "Our chain query's guesses drift: four hundred rows guessed where 376 came, then 343, and by the end, "
            "thirty-nine thousand guessed for twenty thousand. <bookmark mark='b'/> Ioannidis and Christodoulakis "
            "proved in 1991 that such errors can grow exponentially with the number of joins. <bookmark mark='c'/> "
            "And when Viktor Leis and colleagues tested real optimizers on real data in 2015, they found estimates "
            "wrong by factors of ten thousand and more in every system. <bookmark mark='d'/> What saves us is that a "
            "plan only has to be good, not perfect, and a factor of two rarely changes the choice. <bookmark mark='e'/> "
            "When it does, systems now re-optimize in the middle of a query, or sample the data, or learn the "
            "estimates from experience, which is where the frontier is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (COST, DATA, LAM, KERN)
