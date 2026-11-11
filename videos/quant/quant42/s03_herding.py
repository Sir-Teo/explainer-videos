from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, comma,
                                         fit_right, load)


class Herding(VoiceoverScene):
    def construct(self):
        k = load("kirman")
        self.card(k)
        self.ants()
        self.paths(k)
        self.theorem()
        self.proof()
        self.check(k)
        self.swing(k)
        self.edges(k)
        self.market(k)
        self.lux()
        self.measured()
        self.cascade(k)
        self.question()

    def card(self, k):
        c = chapter_card(2, r"Herding", r"Where does a crowd that copies itself spend its time?", part=PART)
        with self.voiceover(
            "Chapter two, and the answer to the pause: at the extremes. When copying dominates, the crowd spends most "
            "of its time almost unanimous, one way or the other, and swings between the two from time to time. It is "
            f"evenly split only rarely. With a hundred agents, as here, it is unanimous {100 * k['bi']['p_edges']:.0f} "
            "percent of the time."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ants(self):
        rows = [cmath(r"\text{each step}", r":", r"\text{one agent, chosen at random}", font_size=38),
                cmath(r"\text{alone}", r":", '\\text{spontaneous term }\\varepsilon\\text{ in switching probability}', font_size=38,
                      colors={r"\text{alone}": COMP_C}),
                cmath(r"\text{copying}", r":", '\\text{plus imitation: }(1-\\delta)\\,k_{\\mathrm{other}}/(N-1)',
                      font_size=34, colors={r"\text{copying}": SHARE_C}),
                cmath(r"k", r"\to", r"k \pm 1", font_size=40)]
        whys = [why(r"Alan Kirman's model (1993), built from an entomologists' puzzle about ants"),
                why(r"an idiosyncratic change of mind"),
                why(r"recruitment: the probability of conversion is the share holding the other view"),
                why(r"the number $k$ holding view A is a birth--death chain on $0, \ldots, N$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Kirman's ant-model illustration, using the exact chain in this module. <bookmark mark='a'/> One agent is selected at each step. <bookmark mark='b'/> Spontaneous switching contributes epsilon. <bookmark mark='c'/> Imitation contributes an additional rate proportional to the number holding the opposite view: it is added, not multiplied by one minus epsilon. The displayed up and down probabilities must define a valid chain. <bookmark mark='d'/> The number holding A moves by at most one, giving a birth-and-death chain."
        ) as vo:
            step(0)
            for k_, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def paths(self, k):
        h = np.asarray(k["herd"], float)
        u = np.asarray(k["indep"], float)
        t = np.arange(len(h))
        g1 = axes([0, len(h)], [0, 1], x_length=11.6, y_length=2.0, xlabel=r"", ylabel=r"share holding A, herding",
                  xticks=[], yticks=[0, 0.5, 1], font_size=14).move_to(UP * 1.5)
        g2 = axes([0, len(u)], [0, 1], x_length=11.6, y_length=2.0, xlabel=r"400,000 steps",
                  ylabel=r"share holding A, higher spontaneous switching", xticks=[], yticks=[0, 0.5, 1], font_size=14
                  ).move_to(DOWN * 1.7)
        l1 = curve(g1.ax, t, h, SHARE_C, stroke_width=2)
        l2 = curve(g2.ax, t, u, COMP_C, stroke_width=2)
        with self.voiceover(
            "A hundred agents. <bookmark mark='a'/> With copying far more common than independent switching, the share "
            "sits near zero or one, and lurches across. <bookmark mark='b'/> Ten times "
            "more independent switching, and the same crowd hovers around a half. The agents are identical; only "
            "the balance between thinking alone and copying has changed."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(l1), run_time=2.5)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(l2), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\pi(k) = \binom{N}{k}\frac{B(k + \alpha,\ N - k + \alpha)}{B(\alpha, \alpha)},\qquad "
                            r"\alpha = \frac{\varepsilon (N - 1)}{1 - \delta}", font_size=32),
                    wrapped_label('valid irreducible chain: exactly beta-binomial; at fixed $\\alpha$ as $N$ grows, $k/N$ tends to Beta$(\\alpha,\\alpha)$, U-shaped for $\\alpha<1$', 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Herding's stationary law (after Kirman 1993)", st, r"this part's proof", width=11.8,
                            font_size=22)
        with self.voiceover(
            "The exact finite-population law. <bookmark mark='a'/> For positive epsilon, delta below one, N above one and valid transition probabilities, the stationary distribution is beta-binomial with alpha equal to epsilon times N minus one divided by one minus delta. <bookmark mark='b'/> The Beta limit holds when alpha stays fixed as N grows, so epsilon scales inversely with N minus one. Alpha below one gives a U-shaped limiting density; above one gives a central hump. Keeping epsilon fixed is a different asymptotic regime."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\frac{\pi(k+1)}{\pi(k)}", r"=", r"\frac{u(k)}{d(k+1)}", font_size=40, colors={r"=": HURDLE}),
                cmath(r"u(k)", r"=", r"\bigl(1 - \tfrac kN\bigr)\tfrac{1 - \delta}{N - 1}\,(\alpha + k)", font_size=38),
                cmath(r"d(k+1)", r"=", r"\tfrac{k+1}{N}\,\tfrac{1 - \delta}{N - 1}\,(\alpha + N - k - 1)", font_size=38),
                cmath(r"\Rightarrow", r"", r"\frac{(N - k)(\alpha + k)}{(k + 1)(\alpha + N - k - 1)}\ \ \text{: beta-binomial's ratio}",
                      font_size=34, colors={r"\Rightarrow": GOOD})]
        whys = [why(r"a birth--death chain is reversible: detailed balance fixes the stationary law step by step"),
                why(r"up: pick a B agent, then convert alone ($\varepsilon$) or meet one of the $k$ A agents; factor out "
                    r"$(1 - \delta)/(N - 1)$ and $\varepsilon$ becomes $\alpha$"),
                why(r"down from $k + 1$, the same way"),
                why(r"the factors cancel, leaving exactly the beta-binomial's ratio of successive probabilities: the two "
                    r"laws agree at every $k$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof is four lines. <bookmark mark='a'/> A birth-and-death chain is reversible, so detailed balance "
            "fixes its stationary law one step at a time. <bookmark mark='b'/> The chance of moving up: pick an agent "
            "holding B, then it converts on its own or meets one of the k holding A. Factor out one minus delta over N "
            "minus one, and epsilon becomes alpha. <bookmark mark='c'/> The chance of moving down, the same way. "
            "<bookmark mark='d'/> The factors cancel, and what is left is exactly the ratio of successive "
            "beta-binomial probabilities."
        ) as vo:
            step(0)
            for k_, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def check(self, k):
        N = k["N"]
        x = np.arange(N + 1) / N
        out = VGroup()
        for name, col, ttl in (("bi", SHARE_C, rf"herding, $\alpha = {k['bi']['alpha']:.1f}$"),
                               ("uni", COMP_C, rf"higher switching, $\alpha = {k['uni']['alpha']:.0f}$")):
            ex = np.asarray(k[name]["exact"], float)
            sm = np.asarray(k[name]["sim"], float)
            top = float(max(ex.max(), sm.max()) * 1.1)
            g = axes([0, 1], [0, top], x_length=5.4, y_length=3.2, xlabel=r"share holding A", ylabel=ttl,
                     xticks=[0, 0.5, 1], yticks=[], font_size=14)
            bars = VGroup(*[Rectangle(width=5.4 / (N + 1) * 0.9, height=max(1e-3, g.ax.c2p(0, sm[i])[1] - g.ax.c2p(0, 0)[1]),
                                      stroke_width=0, fill_color=col, fill_opacity=0.6)
                            .move_to(g.ax.c2p(x[i], sm[i] / 2)) for i in range(N + 1)])
            ln = curve(g.ax, x, ex, WHITE, stroke_width=2)
            out.add(VGroup(g, bars, ln))
        out.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.1)
        cap = label(rf"total variation, simulation against the exact law: {k['bi']['tv_exact_sim']:.3f} and "
                    rf"{k['uni']['tv_exact_sim']:.3f}; exact against beta-binomial: below $10^{{-14}}$", font_size=17,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"The check: forty million steps against the exact law", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"""Two forty-million-step runs, after the stated burn-in, are compared with their exact stationary probabilities. <bookmark mark='a'/> The low-switching case puts more mass near the extremes. <bookmark mark='b'/> The higher-switching chain is centrally concentrated, but still contains imitation and is not a population of independent agents. <bookmark mark='c'/> Total-variation differences are {k['bi']['tv_exact_sim']:.3f} and {k['uni']['tv_exact_sim']:.3f}; the two exact finite-state formulas agree to numerical precision. A single long run is a check, not a proof of sampling error bounds."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(out[0][0]), FadeIn(out[0][1]), Create(out[0][2]))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(FadeIn(out[1][0]), FadeIn(out[1][1]), Create(out[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def swing(self, k):
        sw = k["swing"]
        b, u = sw["bi"], sw["uni"]
        rows = [cmath(r"m_k", r"=", r"\frac{1 + u(k)\,m_{k+1}}{d(k)},\quad m_N = \frac{1}{d(N)}", font_size=40,
                      colors={r"m_k": SHARE_C}),
                cmath(r"\mathbb E\,T_{90 \to 10}", r"=", r"\textstyle\sum_{k=11}^{90} m_k", font_size=40),
                cmath(r"\text{herding}", r":", rf"{comma(b['theory'])}\ \text{{steps; simulated }} {comma(b['sim'])}", font_size=36,
                      colors={r"\text{herding}": SHARE_C}),
                cmath(r"\text{higher switching}", r":", rf"{comma(u['theory'])}\ \text{{steps; simulated }} {comma(u['sim'])}",
                      font_size=36, colors={r"\text{higher switching}": COMP_C})]
        whys = [why(r"the mean time to step down from $k$: one step, plus, if the chain first goes up, the time to come "
                    r"back down from $k + 1$"),
                why(r"a swing from 90\% holding A to 10\% is the sum of those steps"),
                why(rf"averaged over {b['n']} simulated swings: hundreds of decisions per agent before the crowd turns"),
                why(rf"averaged over {u['n']} swings: higher-switching crowds cross the middle often but rarely reach the "
                    r"extremes")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        bt, bs, ut, us = b["theory"], b["sim"], u["theory"], u["sim"]
        with self.voiceover(
            f"""The recursion gives an exact mean first-passage time for this specified finite chain. <bookmark mark='a'/> The mean time to step down from k satisfies the displayed recursion from the top state. <bookmark mark='b'/> Summing from eleven through ninety gives passage from exactly ninety to exactly ten. <bookmark mark='c'/> The low-switching value is {bt:,.0f} steps, versus {bs:,.0f} in the sampled simulation. <bookmark mark='d'/> The higher-switching values are {ut:,.0f} and {us:,.0f}. Simulation is inspected only every ten steps, starts when the sampled state is at least ninety and ends at at most ten. It includes sampling delay and possible overshoot, so it is not an exact observation of the theoretical passage."""
        ) as vo:
            step(0)
            for k_, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def edges(self, k):
        e = k["edges"]
        rows = VGroup(*[label(rf"$N = {comma(x['N'])}$: unanimous {100 * x['p']:.0f}\% of the time", font_size=24,
                              color=SHARE_C) for x in e]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.4)
        note_ = wrapped_label('at a fixed $\\alpha$ of 0.2; the probability of unanimity falls like $N^{-\\alpha}$, so slowly in this fixed-alpha model; this is not a quantitative law for real crowds', 11.0, 19,
                              GREY_A).next_to(rows, DOWN, buff=0.6)
        with self.voiceover(
            f"""Keep alpha fixed at nought point two, adjusting spontaneous switching as population size changes. <bookmark mark='a'/> The exact model probability of unanimity is {100 * e[0]['p']:.0f} percent at a hundred agents, {100 * e[1]['p']:.0f} at a thousand, and {100 * e[2]['p']:.0f} at ten thousand. <bookmark mark='b'/> It falls at the stated power rate. These stationary probabilities concern this chain, not how long real investors agree or a universal empirical scaling law."""
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4), run_time=2)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def market(self, k):
        mk = k["market"]
        h, u = mk["herd"], mk["indep"]
        rh = np.asarray(mk["r_herd"], float)[:1500]
        ri = np.asarray(mk["r_indep"], float)[:1500]
        sc = 1 / (max(np.abs(rh).max(), np.abs(ri).max()) * 1.05)
        g1 = axes([0, len(rh)], [-1, 1], x_length=11.6, y_length=1.9, xlabel=r"", ylabel=r"returns, herding crowd",
                  xticks=[], yticks=[], font_size=14).move_to(UP * 1.6)
        g2 = axes([0, len(ri)], [-1, 1], x_length=11.6, y_length=1.9, xlabel=r"", ylabel='returns, higher-switching crowd',
                  xticks=[], yticks=[], font_size=14).move_to(DOWN * 0.9)
        b1 = VGroup(*[Line(g1.ax.c2p(i, 0), g1.ax.c2p(i, rh[i] * sc), color=SHARE_C, stroke_width=1.2)
                      for i in range(0, len(rh), 2)])
        b2 = VGroup(*[Line(g2.ax.c2p(i, 0), g2.ax.c2p(i, ri[i] * sc), color=COMP_C, stroke_width=1.2)
                      for i in range(0, len(ri), 2)])
        cap = label(rf"lag-5 autocorrelation of $|r|$: {h['acf_abs'][2]:.2f} against {u['acf_abs'][2]:.2f}; excess "
                    rf"kurtosis {h['kurt']:.1f} against {u['kurt']:.1f}", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.45)
        a5h, a5u, kh, ku = h["acf_abs"][2], u["acf_abs"][2], h["kurt"], u["kurt"]
        with self.voiceover(
            f"""The chosen illustrative price adds a sentiment premium to fundamental noise. <bookmark mark='a'/> Low spontaneous switching can create bursts when sentiment changes. <bookmark mark='b'/> Compare the higher-switching case, which still has imitation. <bookmark mark='c'/> Lag-five absolute-return dependence is {a5h:.2f} versus {a5u:.2f}; excess kurtosis is {kh:.1f} versus {ku:.1f}. These chosen simulations show different strengths and misses. They do not prove imitation necessary for observed market tails or identify a unique empirical mechanism."""
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), LaggedStart(*[Create(b_) for b_ in b1], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b_) for b_ in b2], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def lux(self):
        cards = VGroup(
            desk_question(r"Lux and Marchesi (1999)", r"chartists, split into optimists and pessimists who herd, and "
                          r"fundamentalists; switching by contagion and by profits", width=12.4, font_size=19),
            desk_question(r"what it produced", r"fat tails and volatility clustering as bursts of chartist "
                          r"dominance, while prices still track fundamentals on average", width=12.4, font_size=19),
            desk_question(r"Alfarano, Lux and Wagner (2005)", r"a Kirman herding process inside a market model, simple "
                          r"enough to estimate, with a Beta law for the sentiment index", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Herding in a market. <bookmark mark='a'/> Thomas Lux and Michele Marchesi built chartists, divided into "
            "optimists and pessimists who herd, alongside fundamentalists, all switching by contagion and by profits. "
            "<bookmark mark='b'/> It produced fat tails and clustered volatility as bursts of chartist dominance, while "
            "prices still tracked fundamentals on average. <bookmark mark='c'/> And Simone Alfarano, Lux and Friedrich "
            "Wagner put Kirman's process inside a market model simple enough to estimate, with this chapter's Beta law "
            "for sentiment."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        cards = VGroup(
            desk_question(r"herding measured", r"Lakonishok, Shleifer and Vishny (1992): do more funds trade a stock in "
                          r"the same direction than chance would give? A little, mostly in small stocks", width=12.4,
                          font_size=19),
            desk_question(r"rational herding", r"Banerjee (1992); Bikhchandani, Hirshleifer and Welch (1992): when "
                          r"others' actions carry information, copying is rational, and cascades can be wrong", width=12.4,
                          font_size=19),
            desk_question(r"why it matters here", r"machines that learn from the same data, or the same model, copy each "
                          r"other without meeting: Chapter 7", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In real markets. <bookmark mark='a'/> Josef Lakonishok, Andrei Shleifer and Robert Vishny measured whether "
            "more pension funds trade a stock in the same direction than chance would give: a little, mostly in small "
            "stocks. <bookmark mark='b'/> And herding can be rational: when others' actions carry information, copying "
            "them is sensible, and an information cascade can still be wrong. <bookmark mark='c'/> Machines trained on "
            "the same data, or calling the same model, copy each other without ever meeting. That is Chapter seven."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k_, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cascade(self, k):
        cs = k["cascade"]
        c7 = [x for x in cs if abs(x["p"] - 0.7) < 1e-9][0]
        rows = [cmath(r"\text{each agent}", r":", r"\text{a private signal, right with probability } p", font_size=36,
                      colors={r"\text{each agent}": COMP_C}),
                cmath(r"\text{revealed evidence leads by two}", r"\Rightarrow", r"\text{everyone after copies them}", font_size=38,
                      colors={r"\text{revealed evidence leads by two}": SHARE_C}),
                cmath(r"P(\text{wrong cascade})", r"=", r"\frac{q^2}{p^2 + q^2}", font_size=40, colors={r"P(\text{wrong cascade})": BAD}),
                cmath(r"p = 0.7", r"\Rightarrow", rf"{100 * c7['wrong']:.1f}\%\ \ (\text{{simulated }} {100 * c7['sim']['wrong']:.1f}\%)",
                      font_size=40)]
        whys = [why(r"Bikhchandani, Hirshleifer and Welch (1992): agents act in turn, seeing earlier actions but not "
                    r"earlier signals"),
                why(r"once the actions lead by two, the public evidence outweighs any one signal: a cascade, and later "
                    r"actions carry no information"),
                why(r"in pairs: a pair agreeing starts a cascade, a disagreeing pair cancels out; so the first agreeing "
                    r"pair decides, with odds $p^2 : q^2$"),
                why(r"200,000 simulated sequences of 40 agents; information that would be decisive if pooled is lost "
                    r"for good")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        pw, ps = 100 * c7["wrong"], 100 * c7["sim"]["wrong"]
        with self.voiceover(
            f"""A specific information-cascade model. <bookmark mark='a'/> Two equally likely states, conditionally independent binary signals correct with probability point seven, and sequential observation of actions rather than signals. Before a cascade, an exact posterior tie follows the private signal. <bookmark mark='b'/> When revealed evidence leads by two, one private signal cannot overturn it; later choices reveal no new information. <bookmark mark='c'/> Disagreeing signal pairs cancel; the first agreeing pair has correct-to-wrong odds p squared to q squared. <bookmark mark='d'/> The infinite-horizon wrong-cascade probability is {pw:.1f} percent. The finite forty-agent simulation reports {ps:.1f}. This conclusion depends on the information and tie-breaking rules; copying in general need not obey it."""
        ) as vo:
            step(0)
            for k_, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a simulated market matches the real one on every stylised fact. Is a strategy that works in it "
                       r"likely to work in the real market?")
        with self.voiceover(
            "Pause and predict. A simulated market matches the real one on every stylised fact. Is a strategy that "
            "works in it likely to work in the real market?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
