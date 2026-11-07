from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class OptionalStopping(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.ruin()
        self.table()
        self.doubling()
        self.wald()

    def card(self):
        card = chapter_card(3, r"Optional stopping", r"Can you beat a fair game by quitting at the right time?", part=PART)
        with self.voiceover("Chapter three. Optional stopping: can you beat a fair game by choosing when to quit?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\tau", r":", r"\text{a stopping time: } \{\tau \le n\} \in \mathcal F_n \ \ \text{(no peeking ahead)}", font_size=32),
            cmath(r"E M_\tau", r"=", r"E M_0 \ \ \text{if} \ \ \tau \le N, \ \text{or } (M_{n \wedge \tau}) \text{ is UI}, \ \text{or}", font_size=32),
            cmath(r"\phantom{E}", r"\;", r"E\tau < \infty \text{ and } |M_{n+1} - M_n| \le c", font_size=32),
            cmath(r"\text{proof}", r":", r"M_{n \wedge \tau} \text{ is a martingale; \ let } n \to \infty \text{ (DCT or UI)}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        whys = [why(r"decided by the past"), why(r"Doob's optional stopping"), why(r"bounded steps"), why(r"stopped martingales")]
        with self.voiceover(
            "<bookmark mark='a'/> A stopping time is a rule for quitting that uses only the past: whether you have "
            "stopped by time n must be decided by time n. <bookmark mark='b'/> Doob's optional stopping theorem: at a"
            " stopping time, the expected value of a martingale is its starting value, provided the stopping time is "
            "bounded, or the stopped martingale is uniformly integrable and the stopping time is almost surely "
            "finite, <bookmark mark='c'/> or the expected stopping time is finite and the steps are bounded. "
            "<bookmark mark='d'/> The proof: the martingale stopped at tau is again a martingale, so its mean never "
            "changes, and one of the conditions lets the limit pass inside the expectation. No stopping rule can turn"
            " a fair game into a favourable one, unless the conditions fail."
        ) as vo:
            heading=label('Optional stopping needs a valid limit interchange',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ruin(self):
        rows = [
            cmath(r"p = \tfrac12", r":", r"S_n \text{ is a martingale: } a = E S_\tau = b\, P(\text{reach } b)", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"P(\text{reach } b) = a / b, \ \ \text{and from } S_n^2 - n: \ E\tau = a(b - a)", font_size=30),
            cmath(r"p \ne \tfrac12", r":", r"(q/p)^{S_n} \text{ is a martingale} \Rightarrow P(\text{reach } b) = \frac{1 - (q/p)^a}{1 - (q/p)^b}", font_size=30),
            cmath(r"\text{roulette}", r":", r"p = \tfrac{18}{38}: \ \text{from 10 to 20, } \ 0.259; \ \text{from 100 to 200, } \ 0.00003", font_size=30),
        ]
        rows[3][-1].set_color(BADC)
        whys = [why(r"optional stopping, \ bounded steps"), why(r"the second martingale"), why(r"de Moivre's martingale"), why(r"the house edge, \ compounded")]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem's classic use is the gambler's ruin. Start with a pounds and play a "
            "fair game until you reach b or go broke. Your fortune is a martingale with bounded steps, and the exit "
            "time has finite mean, so its expected final value is a, which is b times the chance of reaching b. "
            "<bookmark mark='b'/> So that chance is a over b, and applying the theorem to the second martingale, S n "
            "squared minus n, the expected length of play is a times b minus a. <bookmark mark='c'/> For an unfair "
            "game, q over p to the power S n is a martingale, de Moivre's, and it gives the chance of reaching b in "
            "closed form. <bookmark mark='d'/> At an American roulette wheel, betting red, the chance of doubling ten"
            " pounds before losing them is about a quarter; of doubling a hundred, three in a hundred thousand. A "
            "small house edge, compounded over a long game, is decisive."
        ) as vo:
            heading=label("Stopping two martingales solves gambler's ruin",font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("ruin")
        rows = [[r"game", r"start", r"target", r"P(reach target)", r"expected length"]]
        for r in d["rows"]:
            rows.append([r"fair coin" if r["name"] == "fair" else r"roulette, red", f"{r['a']}", f"{r['b']}",
                         f"{r['win']:.5f}" if r["win"] < 0.01 else f"{r['win']:.3f}", f"{r['duration']:,.0f}"])
        tab = table_rows(rows, font_size=26, col_buff=0.6, row_buff=0.2,
                         colors=[GREY_A, None, None, None, BADC, BADC, BADC]).move_to([0, 0.4, 0])
        msg = label(r"exact, \ from two martingales and optional stopping", font_size=22, color=GREY_B).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The exact answers, for a fair coin and for roulette, at three scales. A fair game is fair "
            "at every scale: half the time you double your money, and the game lasts a times b minus a rounds. <bookmark "
            "mark='b'/> Roulette is not: the larger the target relative to each bet, the more certainly the house wins, "
            "though the game ends sooner."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(msg))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*tab[4:])))
        self.clear_scene()

    def doubling(self):
        d = load("ruin")
        rows = fit_rows(VGroup(
            label(r"the doubling strategy: \ bet 1; \ after each loss, \ double; \ stop at the first win", font_size=26),
            label(r"you always end exactly 1 ahead: \ $M_\tau = 1$, \ but $M_0 = 0$", font_size=26, color=S.ACCENT),
            label(rf"with unlimited credit: \ total funding $2^T-1$ including the winning bet has infinite mean \ (simulated: \ max {d['max_need']:,.0f})", font_size=24, color=BADC),
            label(rf"with a bankroll of {d['bank']:,}: \ ten losses ruin you; \ fair coin: \ expected gain {d['ev_fair']:.0f}", font_size=24, color=GOODC),
            label(rf"roulette: \ ruin with probability {d['lose_all_roulette']:.4f}, \ expected gain ${d['ev_roulette']:.2f}$ per strategy cycle", font_size=24, color=BADC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Then why does the doubling strategy, the martingale of the casinos, seem to work? Bet one; after each loss, double the bet; stop at the first win. <bookmark mark='b'/> You always finish exactly one ahead, so the expected final fortune is one, not zero: the optional-stopping equality does not apply. <bookmark mark='c'/> The stopping time is finite, but the conditions are not met: the losses before the first win are unbounded, and their expected size is infinite; in two hundred thousand simulated strategy cycles, one needed over a million in credit. <bookmark mark='d'/> Give the gambler a real bankroll, one thousand and twenty-three, enough for ten losing bets, one through five hundred and twelve, and the theorem applies: on a fair coin the expected gain is exactly zero, many small wins balanced by a rare ruin. <bookmark mark='e'/> At the roulette wheel ruin comes once in about six hundred rounds, and the strategy loses {say(-d['ev_roulette'], 2)} per strategy cycle on average."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wald(self):
        rows = [
            cmath(r"S_n - n\mu", r":", r"\text{a martingale for i.i.d.\ steps with mean } \mu", font_size=32),
            cmath(r"\text{Wald}", r":", r"E\tau < \infty \Rightarrow E S_\tau = \mu \, E\tau", font_size=34),
            cmath(r"\text{e.g.}", r":", r"\text{the SPRT's expected sample size (Wald 1945)}", font_size=32),
            cmath(r"\text{statistics}", r":", r"\text{a stopping rule changes the sample size, \ not the likelihood}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        whys = [why(r"centred sums"), why(r"Wald's identity"), why(r"Part 58 returns to it"), why(r"the likelihood principle")]
        with self.voiceover(
            "<bookmark mark='a'/> For independent identically distributed integrable steps of mean mu, with a "
            "stopping time adapted to their history and finite expected duration, S n minus n mu is a martingale, "
            "<bookmark mark='b'/> and optional stopping gives Wald's identity: the expected sum at a stopping time is"
            " mu times the expected number of steps. <bookmark mark='c'/> Abraham Wald used it in 1945 to compute the"
            " expected sample size of his sequential probability ratio test. <bookmark mark='d'/> A stopping rule "
            "based on the data can change frequentist calibration. Its likelihood contribution is parameter "
            "independent when the stopping mechanism is parameter free; under that condition the likelihood remains "
            "proportional to the fixed-sample likelihood; Part fifty-eight will reconcile the two views with "
            "martingales."
        ) as vo:
            heading=label("Wald's identity needs integrable iid steps and a finite mean time",font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
