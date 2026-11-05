from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         era_strip, load)


class Bachelier(VoiceoverScene):
    def construct(self):
        self.card()
        self.april()
        self.normal_vols()
        self.formulas()
        self.prices(load("bachelier"))
        self.fair_game()
        self.thesis()
        self.timeline()
        self.question()

    def card(self):
        c = chapter_card(8, r"Back to Bachelier", r"Where did the series begin, and where has it arrived?", part=PART)
        with self.voiceover(
            "Chapter eight, and the answer to the pause: the twenty-second of April twenty twenty. Two days earlier, "
            "the May contract for West Texas crude oil had settled at minus thirty-seven dollars and sixty-three cents a "
            "barrel. Black and Scholes cannot price an option on a negative price; Bachelier, in nineteen hundred, could. "
            "The world's largest futures exchange switched its oil options to his model."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def april(self):
        cards = VGroup(
            desk_question(r"20 April 2020", r"with storage full, holders of the expiring May WTI contract paid to be "
                          r"rid of it: a settlement of $-\$37.63$, the first negative oil price, as CME reported",
                          width=12.4, font_size=19),
            desk_question(r"21--22 April", r"CME Clearing announced that options on several energy contracts would be "
                          r"valued with the Bachelier model, which allows negative prices, effective 22 April", width=12.4,
                          font_size=19),
            desk_question(r"Part 10's warning, in practice", r"a model's assumptions are part of the product; "
                          r"lognormal prices cannot be negative, and a market did not care", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The episode, from the public record. <bookmark mark='a'/> On the twentieth of April twenty twenty, with "
            "storage nearly full, holders of the expiring May contract paid others to take it: a settlement of minus "
            "thirty-seven sixty-three. <bookmark mark='b'/> The exchange's clearing house announced that options on "
            "several energy contracts would be valued with the Bachelier model, effective the twenty-second. "
            "<bookmark mark='c'/> Part ten's warning, in practice: a model's assumptions are part of the product, and "
            "a lognormal price cannot be negative. The market did not care."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def normal_vols(self):
        cards = VGroup(
            desk_question(r"negative rates (Part 19)", r"when euro and yen rates went below zero in the 2010s, swaption "
                          r"markets moved to quoting normal, Bachelier, volatilities, as lognormal quotes broke down", width=12.4,
                          font_size=19),
            desk_question(r"spreads and differences", r"spread options, calendar spreads and other quantities that can "
                          r"be negative are naturally Bachelier's", width=12.4, font_size=19),
            desk_question(r"the lesson", r"the model that survives is not the most elegant one but the one whose "
                          r"assumptions the market does not violate", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And oil was not the first time. <bookmark mark='a'/> When euro and yen interest rates went below zero in "
            "the twenty tens, swaption markets moved to quoting Bachelier's normal volatilities, as lognormal quotes "
            "broke down: Part nineteen. <bookmark mark='b'/> Spreads, and anything that can be negative, are naturally "
            "his. <bookmark mark='c'/> The model that survives is not the most elegant, but the one whose assumptions "
            "the market does not break."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = [cmath(r"dS_t", r"=", r"\sigma_N\,dW_t", font_size=42, colors={r"dS_t": MKT_C}),
                cmath(r"C", r"=", r"(S - K)\,\Phi(d) + \sigma_N\sqrt T\,\varphi(d),\quad d = \frac{S - K}{\sigma_N\sqrt T}",
                      font_size=34),
                cmath(r"dS_t", r"=", r"\sigma\,S_t\,dW_t\ \ \Rightarrow\ \ S_t > 0", font_size=40, colors={r"dS_t": ACT_C})]
        whys = [why(r"Bachelier (1900): prices move by normal increments of fixed size, so they can cross zero"),
                why(r"his call price, at zero rate: one line, and it prices options on negative prices"),
                why(r"Black, Scholes and Merton (1973): increments proportional to the price, which keeps it positive; "
                    r"the better model for stocks, the wrong one for a negative oil price")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The two models. <bookmark mark='a'/> Bachelier's: prices move by normal increments of fixed size, so they "
            "can cross zero. <bookmark mark='b'/> His call price, in one line. <bookmark mark='c'/> Black, Scholes and "
            "Merton's: increments proportional to the price, so it stays positive. Better for stocks; wrong, for a few "
            "days, for oil."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def prices(self, b):
        tab = VGroup(VGroup(label(r"strike", font_size=19, color=QC.IDEA), label(r"Bachelier", font_size=19, color=QC.IDEA),
                            label(r"Black--Scholes", font_size=19, color=QC.IDEA)))
        for x in b["rows"]:
            bs_txt = r"undefined" if not np.isfinite(x["bs"]) else rf"{x['bs']:.2f}"
            tab.add(VGroup(label(rf"{x['K']:+.0f}", font_size=20), label(rf"{x['bachelier']:.2f}", font_size=20, color=MKT_C),
                           label(bs_txt, font_size=20, color=ACT_C if np.isfinite(x["bs"]) else BAD)))
        xs = [-3.0, 0.6, 3.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.4 - 0.65 * j, 0])
        note_ = label(rf"a one-month call on a \$10 future; the normal volatility matched at the money "
                      rf"($\sigma_N\sqrt T = {b['sigma_n_sqrtT']:.2f}$)", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.5)
        r = b["rows"]
        k0, khi_b, khi_bs = r[1]["bachelier"], r[4]["bachelier"], r[4]["bs"]
        with self.voiceover(
            "The two models side by side, for a one-month call on a ten-dollar oil future, with their volatilities "
            "matched at the money. <bookmark mark='a'/> At the money they agree, to a few cents. <bookmark mark='b'/> "
            f"Far above, Black and Scholes charges {khi_bs:.2f} against Bachelier's {khi_b:.2f}: lognormal prices have a "
            "longer right tail. <bookmark mark='c'/> And at a strike of zero or below, Black and Scholes has no answer, "
            f"while Bachelier prices the zero-strike call at {k0:.2f}. In April twenty twenty, that row was the one "
            "that mattered."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(tab[4]))
            vo.wait_until("b")
            self.play(FadeIn(tab[5]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def fair_game(self):
        rows = [cmath(r"\mathbb E[S_{t+1} \mid \mathcal F_t]", r"=", r"S_t", font_size=44, colors={r"=": HURDLE}),
                cmath(r"\Rightarrow", r"", r"\mathbb E[\text{gain of any strategy}] = 0", font_size=40),
                cmath(r"\text{this part}", r":", r"\text{after costs, the average investor cannot do better}", font_size=36,
                      colors={r"\text{this part}": REC_C})]
        whys = [why(r"Part 1: Bachelier's ``fair game'', the martingale, under the measure that prices"),
                why(r"Part 4: the gain of any predictable strategy against a martingale has zero mean"),
                why(r"Sharpe's arithmetic is the fair game in accounting form; skill is what earns a premium over it, "
                    r"and Grossman and Stiglitz say it earns about its cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And Bachelier's deeper idea, where Part one began. <bookmark mark='a'/> The fair game: the expected price "
            "tomorrow, given today, is today's price. <bookmark mark='b'/> Part four's theorem: then no strategy built "
            "from what you know can have a positive expected gain. <bookmark mark='c'/> This part's arithmetic is the "
            "same idea in accounting form. What earns more than the fair game is risk, or skill, and skill earns about "
            "what it costs."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def thesis(self):
        cards = VGroup(
            desk_question(r"Paris, 29 March 1900", r"Louis Bachelier defended ``Théorie de la spéculation'', with Henri "
                          r"Poincaré on the committee; it received a respectable but not the highest mention, as "
                          r"historians report", width=12.4, font_size=19),
            desk_question(r"what was in it", r"the random walk, the diffusion equation five years before Einstein's "
                          r"paper, and option prices tested on Paris rentes", width=12.4, font_size=19),
            desk_question(r"forgotten, then found", r"rediscovered in the 1950s by Savage and Samuelson; this series "
                          r"began with it in Part 1", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the man. <bookmark mark='a'/> On the twenty-ninth of March nineteen hundred, Louis Bachelier defended "
            "his thesis on the theory of speculation in Paris, with Henri Poincaré on the committee. "
            "<bookmark mark='b'/> It contained the random walk, the diffusion equation five years before Einstein's "
            "paper on Brownian motion, and option prices tested on French government bonds. <bookmark mark='c'/> It was "
            "forgotten for half a century, until Leonard Savage and Paul Samuelson found it. This series began there."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def timeline(self):
        I = QC.IDEA
        R = BAD
        entries = [(1900, r"Bachelier", I), (1952, r"Markowitz", I), (1965, r"Samuelson, Fama", I),
                   (1973, r"Black--Scholes--Merton", I), (1979, r"Harrison--Kreps", I), (1987, r"the crash", R),
                   (1992, r"Fama--French", I), (1998, r"LTCM", R), (2008, r"the crisis", R), (2014, r"rough volatility", I),
                   (2020, r"negative oil; the dash for cash", R), (2025, r"the hold-out closes", REC_C)]
        strip = era_strip(entries, y0=1895, y1=2030, font_size=12, step=20).move_to(DOWN * 0.3)
        head = label(r"A hundred and twenty-five years", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "The whole arc. Bachelier's thesis; Markowitz's portfolios; Samuelson and Fama on efficient prices; Black, "
            "Scholes and Merton. <bookmark mark='a'/> Harrison and Kreps's measures; the crash of nineteen eighty-seven; "
            "the factors of Fama and French; LTCM. <bookmark mark='b'/> The crisis; rough volatility; negative oil and "
            "the dash for cash; and the closing of the House's hold-out, at the end of twenty twenty-five."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House began as an empty building and a sealed envelope. Name one thing each of the seven acts "
                       r"added to it.")
        with self.voiceover(
            "Pause and predict. The House began as an empty building and a sealed envelope. Name one thing each of the "
            "series' seven acts added to it."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
