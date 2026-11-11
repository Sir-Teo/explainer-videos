from __future__ import annotations


import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BUY_C, GOOD, HURDLE, IMPACT_C, PART, SELL_C, SIM_C, fit_right,
                                         load)


class Sqrt(VoiceoverScene):
    def construct(self):
        lt = load("latent")
        self.answer()
        self.card()
        self.law()
        self.universal()
        self.bitcoin_sizes()
        self.puzzle()
        self.dimensions()
        self.visible()
        self.latent_picture()
        self.derive()
        self.sim(lt)
        self.decay(lt)
        self.fair_pricing()
        self.invariance()
        self.question()

    def answer(self):
        rows = [cmath(r"\sqrt{4}\times 10", r"=", r"20\ \text{bp}", font_size=40, colors={r"20\ \text{bp}": GOOD}),
                cmath(r"4 \times 10", r"=", r"40\ \text{bp}", font_size=40),
                cmath(r"\text{per unit bought}", r":", '\\text{average shortfall grows as the square root}', font_size=34)]
        whys = [why(r"the square root: four times the size, twice the impact"),
                why(r"a straight line: four times the size, four times the impact"),
                why('if the path is $I(q)=c\\sqrt q$, average impact paid is $(2/3)c\\sqrt Q$; $I(Q)/Q$ falls, but cost per share rises')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The pause answer. <bookmark mark='a'/> Four times the size gives twice the terminal displacement, twenty basis points. <bookmark mark='b'/> Linear scaling gives forty. <bookmark mark='c'/> Be careful with units: average price shortfall per share grows with the square root of total size. For a path c times root q, integrating execution prices gives total impact cost two-thirds c Q to the three-halves, and average cost two-thirds c root Q. It is displacement divided by total quantity that decreases, not cost per share."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def card(self):
        c = chapter_card(2, r"The square-root law", r"Why does impact grow like the square root of size?", part=PART)
        with self.voiceover("Chapter two. The most robust empirical regularity in market microstructure, and a puzzle "
                            "about why it holds. Then a model of hidden liquidity that explains it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def law(self):
        rows = [cmath(r"I(Q)", r"\approx", r"Y\,\sigma_{\text{day}}\,\sqrt{\frac{Q}{V_{\text{day}}}}", font_size=44,
                      colors={r"I(Q)": IMPACT_C}),
                cmath(r"Y", r"\approx", r"0.5\text{--}1", font_size=40, colors={r"Y": HURDLE}),
                cmath('\\text{approximation omits}', r":", '\\text{duration and participation omitted in this approximation}', font_size=34)]
        whys = [why(r"Loeb (1983) and Torre (1997) for equities; Almgren, Thum, Hauptmann and Li (2005); Tóth et al. (2011): "
                    r"the impact of a metaorder in units of the daily volatility, against its share of daily volume"),
                why('a convention-specific calibrated coefficient, often of order one'),
                why('duration and participation may matter in a richer impact surface')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The empirical approximation. <bookmark mark='a'/> Terminal signed price impact is often modeled as Y times daily return volatility times the square root of order size over daily volume. Use matching base-volume units for Q and V. Loeb, Torre, Almgren and colleagues, and Toth and colleagues document related patterns. <bookmark mark='b'/> Y is calibrated for the measurement convention and sample; it is not a universal constant. <bookmark mark='c'/> The displayed size-only formula omits duration and participation. Those variables can matter in richer impact surfaces, and the same Y cannot be assumed for terminal displacement and average execution cost."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def universal(self):
        cards = VGroup(
            desk_question(r"equities and futures", r"brokers' and funds' records across thousands of stocks and dozens of "
                          r"futures: exponents near one half over several decades of size", width=12.4, font_size=19),
            desk_question(r"Bitcoin", r"Donier and Bonart (2015) reconstructed about a million metaorders from the Mt.Gox "
                          r"exchange's leaked account-level records, and found the square root there too", width=12.4,
                          font_size=19),
            desk_question(r"its limits", r"very small orders show linear impact (Bucci et al. 2019); some data sets fit a "
                          r"logarithm better (Zarinelli et al. 2015); the prefactor varies with the market", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "How universal. <bookmark mark='a'/> Across thousands of stocks and dozens of futures, exponents near one "
            "half over several decades of size. <bookmark mark='b'/> On Bitcoin, Jonathan Donier and Julius Bonart "
            "reconstructed about a million metaorders from the account-level records leaked from the Mt. Gox exchange, "
            "and found a square root there too. <bookmark mark='c'/> With limits: very small orders show linear impact, "
            "some data fit a logarithm better, and the prefactor varies."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def bitcoin_sizes(self):
        ac = load("ac")
        sig = ac["sigma_day"] / ac["price"]
        v_usd = ac["v_day"] * ac["price"]
        shares = (0.001, 0.01, 0.1)
        costs = [1e4 * sig * (s ** 0.5) for s in shares]
        m01 = shares[0] * v_usd / 1e6
        rows = [cmath(rf"{100 * s:g}\%\ \text{{of a day}}", r":", rf"\${s * v_usd / 1e6:,.0f}\text{{m}} \to {c:.0f}\ "
                      r"\text{bp}".replace(",", "{,}"), font_size=36, colors={rf"{c:.0f}\ \text{{bp}}": IMPACT_C})
                for s, c in zip(shares, costs)]
        whys = [why(rf"Bitcoin's perpetual: daily volatility {100 * sig:.1f}\%, daily volume about "
                    rf"\${v_usd / 1e9:.0f}bn, with $Y = 1$"),
                why(r"ten times the size, about three times the impact"),
                why(r"a tenth of the day's volume: an order that moves the price by a third of a day's volatility")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""An illustrative extrapolation for Bitcoin, setting Y to one. <bookmark mark='a'/> A tenth of a percent of mean recorded volume, about {m01:.0f} million dollars at the reference price, gives terminal displacement about {costs[0]:.0f} basis points. <bookmark mark='b'/> One percent gives {costs[1]:.0f}. <bookmark mark='c'/> Ten percent gives {costs[2]:.0f}. The daily volatility here is a square-root-of-1440 extrapolation of minute volatility, while volume is mean recorded file volume; incomplete spans and intraday seasonality limit this calibration. These are model outputs, not measured executions or average shortfalls."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def puzzle(self):
        cards = VGroup(
            desk_question(r"not Kyle", r"a square root gives sublinear terminal displacement; it does not lower average cost per share", width=12.4, font_size=19),
            desk_question(r"not the visible book", r"the displayed book holds a tiny fraction of a day's volume; a "
                          r"metaorder of 1\% of the day would empty it many times over", width=12.4, font_size=19),
            desk_question(r"so where is the liquidity?", r"in orders that are not yet in the book: traders who would buy "
                          r"or sell at a price, and reveal it only when the price comes near", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why is it a puzzle? <bookmark mark='a'/> Kyle's model gives a straight line. A square root means the market "
            "absorbs large orders more cheaply than any fixed depth would. <bookmark mark='b'/> The visible book is no "
            "help: it holds a tiny fraction of a day's volume, and a metaorder of one percent would empty it many times "
            "over. <bookmark mark='c'/> So the liquidity must be latent: traders who would buy or sell at some price, "
            "and reveal it only when the price comes near."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def dimensions(self):
        rows = [cmath(r"\frac{I}{\sigma}", r"=", r"F\!\left(\frac{Q}{V},\ \frac{T}{T_{\text{day}}}\right)", font_size=40),
                cmath(r"\text{no } T", r"\Rightarrow", r"F = F(Q/V)", font_size=40),
                cmath('\\text{additional supply and risk scaling assumptions}', r"\Rightarrow", r"F \propto \sqrt{Q/V}", font_size=36,
                      colors={r"F \propto \sqrt{Q/V}": GOOD})]
        whys = [why('an assumed reduced description, after choosing the relevant scales'),
                why('dropping duration is a reduced empirical approximation'),
                why(r"one argument: liquidity providers demand compensation proportional to the risk of the position they "
                    r"absorb, $\sigma\sqrt{T}$, while the volume they supply in that time is $\propto V T$; eliminating "
                    r"$T$ leaves a square root (a heuristic, not a theorem)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Dimensions organize assumptions but do not determine a square-root law. <bookmark mark='a'/> If volume share and normalized duration are the only chosen variables, normalized impact can be a function of them; other liquidity and market scales may enter. <bookmark mark='b'/> Dropping duration is an empirical approximation, not a consequence of units. <bookmark mark='c'/> A heuristic adds both diffusive price risk and liquidity supply proportional to elapsed time, then eliminates time. Those added assumptions suggest a square root. Dimensional consistency alone leaves the function undetermined."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def visible(self):
        ac = load("ac")
        best = 10.0
        share = 100 * best / ac["v_day"]
        rows = [cmath(r"\text{best queues}", r"\approx", r"10\ \text{BTC}", font_size=38),
                cmath(r"V_{\text{day}}", r"\approx", rf"{ac['v_day'] / 1000:.0f}{{,}}000\ \text{{BTC}}", font_size=38),
                cmath(r"\text{displayed}", r"\approx", rf"{share:.3f}\%\ \text{{of a day}}", font_size=38,
                      colors={r"\text{displayed}": HURDLE})]
        whys = [why(r"Part 36: the two best queues of Bitcoin's perpetual hold about ten bitcoin at a time"),
                why(r"against the day's volume on the same contract"),
                why('two best queues are not full displayed depth; refilling and deeper liquidity matter')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""What the visible comparison actually measures. <bookmark mark='a'/> Ten bitcoin is a rounded illustrative scale for the two best queues, not full displayed depth across all levels. <bookmark mark='b'/> Against mean recorded trade-file volume of {ac['v_day']/1000:.0f} thousand bitcoin, <bookmark mark='c'/> this is {share:.3f} percent. Quotes refresh and deeper orders may exist, so this ratio is not a count of how many times a metaorder must empty the full book. Latent liquidity is one model of replenishment and hidden intentions, not an inference established by the ratio alone."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def latent_picture(self):
        g = axes([-4, 4], [-4, 4], x_length=7.4, y_length=4.4, xlabel=r"price, relative to the current price",
                 ylabel=r"latent volume", xticks=[0], yticks=[0], font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        bids = Polygon(ax.c2p(-4, 0), ax.c2p(0, 0), ax.c2p(-4, 4), fill_color=BUY_C, fill_opacity=0.45, stroke_width=0)
        asks = Polygon(ax.c2p(0, 0), ax.c2p(4, 0), ax.c2p(4, -4), fill_color=SELL_C, fill_opacity=0.45, stroke_width=0)
        eaten = Polygon(ax.c2p(0, 0), ax.c2p(2, 0), ax.c2p(2, -2), fill_color=IMPACT_C, fill_opacity=0.9, stroke_width=0)
        mark = DashedLine(ax.c2p(2, -4), ax.c2p(2, 4), color=HURDLE, stroke_width=2)
        labs = VGroup(label(r"latent bids", font_size=18, color=BUY_C).move_to(ax.c2p(-2.6, 1.5)),
                      label(r"latent offers", font_size=18, color=SELL_C).move_to(ax.c2p(2.8, -1.0)),
                      label(r"a buyer eats a triangle", font_size=18, color=IMPACT_C).next_to(ax.c2p(1, -2), DOWN,
                                                                                         buff=0.6))
        with self.voiceover(
            "The picture of latent liquidity. <bookmark mark='a'/> Hidden intentions to buy below the price and to sell "
            "above it. Jonathan Donier, Julius Bonart, Iacopo Mastromatteo and Bouchaud showed that if these latent "
            "orders keep arriving, being cancelled and revising their prices at random, the density near the price is "
            "a V: it grows linearly with the distance from the price. <bookmark mark='b'/> A buyer must eat the offers "
            "between the old price and the new one: a triangle."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(bids), FadeIn(asks), FadeIn(labs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(eaten), Create(mark), FadeIn(labs[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\rho(x)", r"=", r"\mathcal L\,|x|", font_size=40),
                cmath(r"Q", r"=", r"\int_0^{\Delta} \mathcal L\,x\,dx = \tfrac12\,\mathcal L\,\Delta^2", font_size=40),
                cmath(r"\Delta", r"=", r"\sqrt{2Q/\mathcal L}", font_size=44, colors={r"\Delta": IMPACT_C}),
                cmath(r"\mathcal L", r"\propto", r"V_{\text{day}} / \sigma_{\text{day}}^2", font_size=38)]
        whys = [why(r"the latent density near the price: linear, with slope $\mathcal L$"),
                why(r"to move the price from 0 to $\Delta$, a buyer must absorb all the offers in between: the area of the "
                    r"triangle"),
                why(r"invert: the square root, from nothing but the V shape"),
                why('proposed slope scaling requires a calibration constant and compatible time scales; units alone do not establish it')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A static triangular-book calculation. <bookmark mark='a'/> Assume nonnegative offer density L times distance from the old price. <bookmark mark='b'/> Buying every offer up to delta consumes one half L delta squared. <bookmark mark='c'/> Invert to obtain delta equal to the square root of two Q over L. This assumes a static linear profile over the whole consumed region; the dynamic latent model requires a separate argument. <bookmark mark='d'/> A proposed scaling L proportional to daily volume divided by daily variance introduces a calibration constant and matching time conventions. Units permit it but do not establish it."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, lt):
        rows = lt["rows"]
        x = np.log10([r["Q"] for r in rows])
        y = np.log10([r["I"] for r in rows])
        g = axes([-2, 3], [float(np.floor(y.min())), float(np.ceil(y.max()))], x_length=6.4, y_length=4.4,
                 xlabel=r"metaorder size $Q$, executed in one unit of time", ylabel=r"impact at the end",
                 xticks=[-2, 0, 2], yticks=[float(np.floor(y.min())), 0, float(np.ceil(y.max()))],
                 xfmt=lambda v: f"10^{{{v:.0f}}}", yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=SIM_C) for a, b in zip(x, y)])
        sq = DashedLine(ax.c2p(0, 0.5 * np.log10(2)), ax.c2p(3, 0.5 * np.log10(2) + 1.5), color=GOOD, stroke_width=2)
        st = VGroup(label(rf"small orders: slope {lt['slope_small']:.2f}", font_size=18, color=SIM_C),
                    label(rf"large orders: slope {lt['slope_large']:.2f}", font_size=18, color=SIM_C),
                    label(r"$\sqrt{2Q/\mathcal L}$, the static book", font_size=18, color=GOOD))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            f"""Now the unchanged finite-difference latent-book simulation: fixed execution duration, diffusion, finite boundaries and a source near the zero of density. <bookmark mark='a'/> A log fit to the four smallest sampled orders gives slope {lt['slope_small']:.2f}. <bookmark mark='b'/> The four largest give {lt['slope_large']:.2f}. These are finite-grid fits, affected by source placement and boundaries, and are not a convergence proof of one half. The static triangle is a reference curve; the small-to-large crossover is qualitatively related to Bucci and colleagues' empirical discussion."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(Create(sq))
        self.wait(0.4)
        self.clear_scene()

    def decay(self, lt):
        t = np.asarray(lt["path_t"], float)
        p = np.asarray(lt["path_p"], float)
        top = float(np.ceil(p.max()))
        g = axes([0, float(t[-1])], [0, top], x_length=8.4, y_length=4.2, xlabel=r"time (the order runs from 0 to 1)",
                 ylabel=r"price", xticks=[0, 1, 5, 10], yticks=[0, top], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(DOWN * 0.2)
        c_ = curve(g.ax, t, p, IMPACT_C, stroke_width=3)
        stop = DashedLine(g.ax.c2p(1, 0), g.ax.c2p(1, top), color=GREY_B, stroke_width=1.5)
        peak = float(p.max())
        end = float(p[-1])
        with self.voiceover(
            f"""The same simulated order stops near time one. <bookmark mark='a'/> Its sampled price reaches {peak:.1f}, <bookmark mark='b'/> then falls to {end:.1f} by the end of the recorded path. A diffusion model on an effectively unbounded linear profile can have slow inverse-root decay; this finite horizon and fixed-boundary discretization do not establish that asymptotic rate. Persistent real-market displacement may involve information or future correlated trading, neither included in this illustration."""
        ) as vo:
            self.play(FadeIn(g), Create(stop))
            vo.wait_until("a")
            self.play(Create(c_), run_time=3)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def fair_pricing(self):
        rows = [cmath(r"I(q)", r"=", r"c\sqrt q\quad (0 \le q \le Q)", font_size=40, colors={r"I(q)": IMPACT_C}),
                cmath(r"\bar p - p_0", r"=", r"\frac1Q\int_0^Q c\sqrt q\,dq = \tfrac23\,c\sqrt Q", font_size=36),
                cmath(r"\text{fair pricing}", r":", r"p_\infty = \bar p \Rightarrow \frac{I_\infty}{I(Q)} = \frac23",
                      font_size=36, colors={r"\frac{I_\infty}{I(Q)} = \frac23": GOOD})]
        whys = [why(r"the price impact after the first $q$ units of a metaorder: a square root"),
                why(r"the average price the buyer paid lies two-thirds of the way up"),
                why('Farmer, Gerig, Lillo and Waelbroeck (2013): imposing eventual conditional price equal to average fills gives two-thirds; this needs an extra equilibrium assumption')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A conditional fair-pricing calculation. <bookmark mark='a'/> Assume an execution path c root q, with no separate spread or fees. <bookmark mark='b'/> Its quantity-weighted average displacement is two-thirds of the terminal peak. <bookmark mark='c'/> If one additionally imposes Farmer and colleagues' fair-pricing relation that the eventual conditional price equals this average fill price, two-thirds remains. That relation is an equilibrium modeling assumption; it is not implied by the square root alone or by a generic assertion that neither side profits."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def invariance(self):
        rows = [cmath(r"W", r"=", r"\sigma\,P\,V", font_size=40, colors={r"W": HURDLE}),
                cmath(r"B\ \text{bets per day}", r"\propto", r"(W/W_0)^{2/3}", font_size=38),
                cmath(r"\frac{I}{\sigma}", r"=", r"B^{-1/2} f\!\left(\frac{QB}{V}\right)", font_size=40,
                      colors={r"\frac{I}{\sigma}": IMPACT_C})]
        whys = [why(r"Kyle and Obizhaeva (2016): trading activity, volatility times dollar volume"),
                why(r"their invariance hypothesis: bets arrive in business time, and their dollar risk transfer is the "
                    r"same in every market; this fixes how the number of bets, and so their typical share of volume, scale "
                    r"with activity"),
                why(r"schematic business-time scaling includes volatility per bet and requires calibrated reference scales")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A different scaling hypothesis. <bookmark mark='a'/> Trading activity W is volatility times dollar volume, with units and reference scales fixed. <bookmark mark='b'/> Kyle and Obizhaeva's invariance motivates a number B of bets per day proportional to relative activity to the two-thirds power. <bookmark mark='c'/> In a reduced business-time representation, order size in bets is Q B over V, and volatility per bet is daily volatility divided by root B. Thus normalized impact includes a B to the minus one-half prefactor as well as a function of size in bets. This schematic representation needs calibration; invariance alone does not force that function to be a square root."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        head = label('2. A static latent triangle', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$\\rho(x)=\\mathcal Lx$ for $x\\ge0$, $\\mathcal L=2$ units per tick squared, $Q=9$ units.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Integrate the consumed density and solve for the price displacement in ticks.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause two. A static offer density is L times distance from the old price, with L equal to two units per tick squared. A buyer consumes nine units. Integrate the triangle and find the displacement in ticks.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
